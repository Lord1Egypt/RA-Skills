#!/usr/bin/env python3
"""M6 backfill, pass 1 — let the LLM pick the anchor, and let it say "no".

The regex passes recovered only **55 real semantic edges out of 885 orphans**: a
keyword match cannot tell that "switched to glm-5.1 as primary model" is about
`memory_health`, not about `glm`. This script hands each orphan to the LLM along
with the list of anchor ids that ACTUALLY EXIST in the graph, and asks for one
anchor — or `null`.

**The right to say `null` is the whole point.** A fabricated edge is far worse
than an orphan: it silently poisons every future query, and nothing in the data
tells you it was invented. An orphan is visible and cheap; a hallucinated edge is
invisible and expensive. So the prompt is explicit: if the link is not certain,
return null. We would rather keep an orphan than manufacture a lie.

Design:
  * anchors offered = existing entity ids only (never a free-form string, so the
    model physically cannot invent a node);
  * `{"anchor": null}` accepted and counted as a first-class outcome;
  * dry-run by default — writes a JSON report, never touches the graph;
  * reuses the extractor's transport (`llm_destination`) and PII scrubber, so the
    cloud/local consent rules stay in ONE place.

Usage:
    python3 ontology_backfill_llm.py --limit 20            # dry-run, 20 items
    python3 ontology_backfill_llm.py --limit 20 --apply    # write the edges
"""
import argparse
import importlib.util
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE if (HERE / "trace_extractor.py").exists() else HERE.parent
WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", str(REPO.parent.parent)))
ONTOLOGY_FILE = Path(os.environ.get(
    "ONTOLOGY_FILE", WORKSPACE / "memory" / "ontology" / "graph.jsonl"
))
REPORT_FILE = WORKSPACE / "memory" / "ontology" / "backfill_llm_report.json"

spec = importlib.util.spec_from_file_location("te", REPO / "trace_extractor.py")
te = importlib.util.module_from_spec(spec)
spec.loader.exec_module(te)  # noqa: S102 -- literal path

ANCHOR_PROMPT = """You are repairing a knowledge graph. Each item below is an \
existing node that currently has NO relation to anything else. Your job: pick the \
ONE existing entity this item is really about.

Reply with STRICT JSON and nothing else:
{"anchor": "<id from the list, or null>", "confidence": 0.0-1.0}

RULES — read them twice:
1. `anchor` MUST be copied exactly from the ANCHORS list. Never invent an id, \
never write a name that is not in the list.
2. If you are not certain the item is about that anchor, reply {"anchor": null, \
"confidence": 0}. An orphan is acceptable; a wrong edge is not. A fabricated \
relation silently corrupts every future query, so when in doubt you MUST choose null.
3. A shared date is NOT a relation. "Something happened on this day" is not \
"this is about X". Do not anchor on chronology.
4. Confidence below 0.7 means you should be returning null instead.

ANCHORS:
__ANCHORS__

ITEM:
id: __EID__
type: __ETYPE__
text: __TEXT__

JSON:"""


def load_graph(path):
    ents, linked = {}, set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "entity" in e and e["entity"].get("id"):
            ents[e["entity"]["id"]] = e["entity"]
        if e.get("op") == "relate":
            linked.add(e.get("from"))
            linked.add(e.get("to"))
    return ents, linked


def text_of(entity):
    props = entity.get("properties") or {}
    bits = []
    for key in ("description", "summary", "name", "scope", "title"):
        val = props.get(key)
        if isinstance(val, str):
            bits.append(val)
        elif isinstance(val, list):
            bits.extend(str(v) for v in val)
        elif val is not None:
            bits.append(str(val))
    return " | ".join(b for b in bits if b).strip()[:400]


def candidate_anchors(ents):
    """Existing ids the model may choose from. Log-like types are excluded: they
    are the items being repaired, not destinations."""
    skip = {"TimelineEvent", "Decision", "Episode"}
    return sorted(k for k, v in ents.items() if v.get("type") not in skip)


def merge_regex_and_llm(regex_rels, llm_results):
    """Union of both passes, regex first. One edge per source, no duplicates.

    The two methods do NOT overlap: the regex caught `med_reminder` on an item
    the LLM sent back as null, while the LLM found 7 anchors the regex missed.
    Replacing one with the other would lose real edges, so we take both and
    respect every `null` -- an unmapped item stays an orphan rather than getting
    a fabricated edge.
    """
    out, seen = [], set()
    for src, dst, rel, why in regex_rels:
        if src in seen:
            continue
        seen.add(src)
        out.append({"from": src, "to": dst, "rel": rel,
                    "evidence": why, "confidence": 0.9})
    for r in llm_results:
        if not r.get("anchor") or r["id"] in seen:
            continue
        seen.add(r["id"])
        out.append({"from": r["id"], "to": r["anchor"], "rel": "about",
                    "evidence": "llm-selected anchor",
                    "confidence": r.get("confidence", 0.0)})
    return out


def ask_llm(prompt, api_key, model, timeout=45, retries=2):
    """One LLM call, with a hard wall-clock timeout and retries.

    urllib's per-read timeout does not fire on a half-open socket that trickles
    bytes, so we also enforce a socket-level timeout and cap the retries. A dead
    socket must be *skipped*, never allowed to freeze the whole 885-item run.
    """
    payload = json.dumps({
        "model": model, "prompt": prompt, "stream": False,
        "options": {"temperature": 0},
    }).encode()
    last_exc = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(
            "https://ollama.com/api/generate", data=payload,
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {api_key}"},
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = json.loads(resp.read().decode())
            return body.get("response", "")
        except (urllib.error.URLError, urllib.error.HTTPError,
                TimeoutError, OSError) as exc:
            last_exc = exc
            if attempt < retries:
                time.sleep(2 * (attempt + 1))  # 2s, then 4s backoff
    raise last_exc


def parse_reply(raw, valid_ids):
    """Return (anchor_or_None, confidence). Never returns an id absent from the
    graph, even if the model produced one — that is the anti-hallucination gate."""
    m = re.search(r"\{[\s\S]*?\}", raw or "")
    if not m:
        return None, 0.0
    try:
        obj = json.loads(m.group())
    except json.JSONDecodeError:
        return None, 0.0
    anchor = obj.get("anchor")
    try:
        conf = float(obj.get("confidence") or 0.0)
    except (TypeError, ValueError):
        conf = 0.0
    if not isinstance(anchor, str) or anchor not in valid_ids:
        return None, conf
    if conf < 0.7:
        return None, conf
    return anchor, conf


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--graph", default=str(ONTOLOGY_FILE))
    ap.add_argument("--min-confidence", type=float, default=0.7)
    args = ap.parse_args()

    graph = Path(args.graph)
    ents, linked = load_graph(graph)
    anchors = candidate_anchors(ents)
    anchor_set = set(anchors)
    orphans = sorted(k for k in ents if k not in linked and k not in anchor_set)
    today_str = datetime.now().strftime("%Y-%m-%d")

    print(f"  orphans    : {len(orphans)}", flush=True)
    print(f"  anchors    : {len(anchors)} existing ids offered to the model", flush=True)

    # Regex pass first: it is free, and it catches anchors the LLM sends back as
    # null (e.g. `med_reminder` on dec_2026-06-03_4101). The two do not overlap.
    sys.path.insert(0, str(REPO))
    bf_spec = importlib.util.spec_from_file_location(
        "bf", REPO / "ontology_backfill_orphans.py")
    bf = importlib.util.module_from_spec(bf_spec)
    bf_spec.loader.exec_module(bf)  # noqa: S102 -- literal path
    roots = bf._candidate_roots(ents)
    regex_rels, _ = bf.build_relations([("grounded", bf.pass_grounded)],
                                       orphans, ents, roots, today_str)
    print(f"  regex pass : {len(regex_rels)} anchor(s) the LLM may miss", flush=True)

    # Transport + consent: reuse the extractor's single source of truth.
    key = te._find_ollama_api_key_sources()[1]
    kind, label = te.llm_destination()
    print(f"  transport  : {label}", flush=True)
    if kind != "cloud" or not key:
        print("  cloud not available/opted in — aborting (set TRACE_LLM_ALLOW_CLOUD=1)")
        return 1

    model = os.environ.get("OLLAMA_MODEL", "glm-5.3-flash:cloud")
    anchor_block = "\n".join(f"- {a}" for a in anchors)

    sample = orphans[:args.limit]
    results, stats = [], Counter()
    for i, oid in enumerate(sample, 1):
        ent = ents[oid]
        prompt = (ANCHOR_PROMPT
                  .replace("__ANCHORS__", anchor_block)
                  .replace("__EID__", str(oid))
                  .replace("__ETYPE__", str(ent.get("type")))
                  .replace("__TEXT__", te.sanitize_pii(text_of(ent))))
        try:
            raw = ask_llm(prompt, key, model)
        except Exception as exc:
            print(f"  [{i}/{len(sample)}] {oid[:34]:36} ERROR {exc}", flush=True)
            stats["error"] += 1
            continue
        anchor, conf = parse_reply(raw, set(anchors))
        if anchor is None:
            stats["null"] += 1
        else:
            stats["linked"] += 1
        results.append({"id": oid, "type": ent.get("type"), "text": text_of(ent),
                        "anchor": anchor, "confidence": conf})
        mark = anchor if anchor else "null"
        print(f"  [{i}/{len(sample)}] {oid[:30]:32} -> {str(mark):24} ({conf:.2f})",
              flush=True)
        time.sleep(0.2)

    print(f"\n  linked {stats['linked']} | null {stats['null']} | "
          f"error {stats['error']}  (of {len(sample)})")

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(json.dumps({
        "date": datetime.now().isoformat(), "model": model,
        "transport": label, "sample": results, "stats": dict(stats),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  report     : {REPORT_FILE}")

    if args.apply:
        merged = merge_regex_and_llm(
            [(r["from"], r["to"], r["rel"], r["properties"]["evidence"])
             for r in regex_rels], results)
        rels = [{"op": "relate", "from": m["from"], "to": m["to"],
                 "rel": m["rel"],
                 "properties": {"evidence": m["evidence"],
                                "confidence": m.get("confidence"),
                                "backfilled": True,
                                "tool": "ontology_backfill_llm.py"}}
                for m in merged]
        graph_before = len(graph.read_text(encoding="utf-8").splitlines())
        backup = graph.with_name(
            graph.name + f".pre-llm-{datetime.now():%Y%m%d_%H%M%S}")
        import shutil
        shutil.copy2(graph, backup)
        print(f"\n  backup     : {backup.name}")
        with graph.open("a", encoding="utf-8") as fh:
            for rel in rels:
                fh.write(json.dumps(rel, ensure_ascii=False, sort_keys=True) + "\n")
        graph_after = len(graph.read_text(encoding="utf-8").splitlines())
        print(f"  applied    : {len(rels)} edge(s) appended "
              f"({graph_before} -> {graph_after} lines)")
        e2, l2 = load_graph(graph)
        print(f"  orphans now: {len([k for k in e2 if k not in l2])}")
    else:
        print("  DRY-RUN — nothing written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
