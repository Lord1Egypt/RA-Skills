#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from _common import parse_frontmatter, save_json, sectionized_lines, split_sentences, strip_markdown, write_text

PAPER_TYPE_CUES = {
    "theory": ["theorem", "lemma", "proposition", "proof", "consistency", "convergence", "asymptotic"],
    "methods / ml / statistics": ["algorithm", "model", "objective", "loss", "training", "estimator", "benchmark"],
    "empirical / economics / social science": ["identification", "regression", "instrument", "difference-in-differences", "panel", "survey", "sample"],
    "systems": ["latency", "throughput", "memory", "cluster", "hardware", "serving", "system"],
    "survey / synthesis": ["survey", "review", "taxonomy", "overview", "synthesis"],
}
DOMAIN_CUES = {
    "machine learning / ai": ["neural", "transformer", "diffusion", "reinforcement learning", "llm", "benchmark"],
    "statistics / probability": ["estimator", "asymptotic", "likelihood", "posterior", "concentration", "probability"],
    "economics / econometrics": ["welfare", "policy", "identification", "instrumental variable", "regression discontinuity", "firm", "household"],
    "quantitative finance": ["option", "hedging", "portfolio", "volatility", "return", "martingale", "no-arbitrage"],
    "physics": ["hamiltonian", "lagrangian", "quantum", "field theory", "symmetry", "observable", "phase transition"],
    "computer systems": ["latency", "throughput", "distributed", "compiler", "storage", "kernel", "scheduling"],
}
CLAIM_CUES = ["we show", "we prove", "we find", "this paper shows", "results show", "we demonstrate", "we derive", "we identify"]
TECH_OBJECT_PATTERNS = [
    re.compile(r"\b(theorem|lemma|proposition|corollary)\b", re.I),
    re.compile(r"\b(loss|objective|likelihood|estimator|algorithm|policy|hamiltonian|lagrangian|portfolio|backtest|regression)\b", re.I),
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build a compact paper map from paper markdown or extracted text.")
    p.add_argument("input", help="Input markdown or text file")
    p.add_argument("--output", default="", help="Markdown output path")
    p.add_argument("--json-output", default="", help="Optional JSON output path")
    return p.parse_args()


def choose_best_label(text: str, cue_map: dict[str, list[str]], default: str) -> str:
    lower = text.lower()
    best_label = default
    best_score = 0
    for label, cues in cue_map.items():
        score = sum(lower.count(cue.lower()) for cue in cues)
        if score > best_score:
            best_score = score
            best_label = label
    return best_label


def title_from_text(md: str, path: str) -> str:
    m = re.search(r"^#\s+(.+)$", md, re.M)
    if m:
        return m.group(1).strip()
    lines = [ln.strip() for ln in md.splitlines() if ln.strip()]
    if lines:
        first = lines[0].strip("# ")
        if len(first.split()) <= 20:
            return first
    return Path(path).stem.replace("_", " ")


def get_section_text(md: str, name_keywords: list[str]) -> str:
    collected = []
    for title, body in sectionized_lines(md):
        tl = title.lower()
        if any(k in tl for k in name_keywords):
            collected.append(body)
    return "\n".join(collected)


def first_claim(text: str) -> str:
    sents = split_sentences(strip_markdown(text))
    for sent in sents:
        low = sent.lower()
        if any(cue in low for cue in CLAIM_CUES):
            return sent
    return sents[0] if sents else ""


def key_objects(text: str) -> list[str]:
    lower = text.lower()
    found = []
    for pat in TECH_OBJECT_PATTERNS:
        found.extend([m.group(1).lower() for m in pat.finditer(lower)])
    out = []
    for item in found:
        if item not in out:
            out.append(item)
    return out[:8]


def intellectual_load(md: str) -> str:
    heavy_sections = []
    for title, body in sectionized_lines(md):
        body_len = len(strip_markdown(body))
        if body_len < 200:
            continue
        tl = title.lower()
        if any(k in tl for k in ["method", "model", "theory", "proof", "experiment", "results", "appendix", "empirical", "analysis"]):
            heavy_sections.append(title)
    return ", ".join(heavy_sections[:6])


def build_map(md: str, path: str) -> tuple[dict, str]:
    abstract = get_section_text(md, ["abstract"]) or "\n".join(md.splitlines()[:40])
    intro = get_section_text(md, ["introduction"]) or abstract
    conclusion = get_section_text(md, ["conclusion", "discussion"]) or ""
    focus_text = "\n".join([abstract, intro, conclusion])
    cleaned = strip_markdown(focus_text)
    sents = split_sentences(cleaned)

    research_q = sents[0] if sents else ""
    main_claim = first_claim(focus_text)
    ptype = choose_best_label(cleaned, PAPER_TYPE_CUES, "mixed")
    domain = choose_best_label(cleaned, DOMAIN_CUES, "general scientific / interdisciplinary")
    objects = key_objects(focus_text)
    load = intellectual_load(md)

    data = {
        "title": title_from_text(md, path),
        "research_question": research_q,
        "problem_setting": sents[1] if len(sents) > 1 else "",
        "paper_type": ptype,
        "domain": domain,
        "main_claim": main_claim,
        "key_technical_objects": objects,
        "where_intellectual_load_sits": load,
        "map_sentence": f"The paper studies {research_q or '[research question]'} in the setting {sents[1] if len(sents) > 1 else '[setting]'}. Its main move is {main_claim or '[main move]'}. It claims gains in [outcome], supported by [evidence]. The key technical objects are {', '.join(objects) or '[objects]'}. The paper type is {ptype} and the domain is {domain}."
    }

    md_out = "\n".join([
        f"- **Research question:** {data['research_question']}",
        f"- **Problem setting / regime:** {data['problem_setting']}",
        f"- **Paper type:** {data['paper_type']}",
        f"- **Domain:** {data['domain']}",
        f"- **Main claim / central move:** {data['main_claim']}",
        f"- **Key technical objects:** {', '.join(data['key_technical_objects'])}",
        f"- **Where the intellectual load sits:** {data['where_intellectual_load_sits']}",
        "",
        "> " + data["map_sentence"],
        "",
    ])
    return data, md_out


def main() -> None:
    args = parse_args()
    md = Path(args.input).read_text(encoding="utf-8")
    _, md = parse_frontmatter(md)
    data, md_out = build_map(md, args.input)
    if args.output:
        write_text(args.output, md_out)
    else:
        print(md_out)
    if args.json_output:
        save_json(args.json_output, data)


if __name__ == "__main__":
    main()
