#!/usr/bin/env python3
"""
LYGO Flame Ward — harden lattice against disinfo / injected half-truths.

Hooks: enemy-model / flame-scan / claim-gap / concordance / ingest-gate /
       quarantine / burn-receipt / expose / endpoint-scan / demo

Local-first. Consent-gated writes. No network. No subprocess. No auto-publish.
Burn = strip authority + quarantine + receipt (not violence).

Signature: Delta9Phi963-FLAME-WARD
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SIG = "Delta9Phi963-FLAME-WARD"
VERSION = "1.0.1"
PHI = (1.0 + math.sqrt(5.0)) / 2.0

HASH_EXCLUDE = {
    "ok",
    "written",
    "error",
    "hint",
    "reasons",
    "burn_sha256",
    "quarantine_sha256",
    "scan_sha256",
}

ENEMY_MODEL = {
    "signature": "Delta9Phi963-ENEMY-MODEL-v1",
    "version": "1.1.0",
    "epistemic_default": "FABRICATED_UNTIL_CONCORDANCE",
    "authority_rule": "Institutional labels are metadata only — never trust weight.",
    "burn_semantics": "Strip authority + quarantine + burn-receipt. Not violence.",
    "classes": [
        {"id": "injected_code", "name": "Injected code / silent plugin"},
        {"id": "half_truth_pack", "name": "Half-truth pack"},
        {"id": "saturation_flood", "name": "Information saturation flood"},
        {"id": "authority_shield", "name": "Authority shield"},
        {"id": "lattice_poison", "name": "Lattice poison"},
        {"id": "consent_asymmetry", "name": "Consent asymmetry endpoint leak"},
        {"id": "webaudio_fingerprint", "name": "Silent WebAudio / device fingerprint"},
    ],
    "non_targets": [
        "people_as_class",
        "faith_or_creed",
        "profession_or_job_title",
        "ordinary_dissent_without_proof_avoidance_templates",
        "unsolicited_scrape_of_social_or_institutional_APIs",
    ],
}

# Certainty / authority / bait patterns (discourse templates — not identity)
RE_CERTAINTY = re.compile(
    r"\b(settled science|trust the experts?|beyond (any )?doubt|proven fact|"
    r"everyone knows|there is no debate|undeniable|you must believe)\b",
    re.I,
)
RE_AUTHORITY = re.compile(
    r"\b(WHO|CDC|FDA|NIH|WEF|UN|mainstream media|officials? (say|said)|"
    r"according to (experts?|authorities)|peer[- ]reviewed consensus)\b",
    re.I,
)
RE_RAGE = re.compile(
    r"\b(wake up sheeple|they want you (dead|silent)|literally killing|"
    r"click here now|you won't believe|destroyed by|evil cabal)\b",
    re.I,
)
RE_DIGEST = re.compile(r"\b([a-fA-F0-9]{64}|sha[- ]?256|merkle|digest)\b", re.I)
RE_NUMBERS = re.compile(r"\b\d+(\.\d+)?%?\b")
RE_TOTALIZING = re.compile(
    r"\b(always|never|all|none|every single|completely|100%)\b", re.I
)

# Silent WebAudio / browser fingerprint patterns (operator-supplied HTML/JS only)
RE_AUDIO_CTX = re.compile(r"\b(AudioContext|webkitAudioContext)\b")
RE_OSC = re.compile(r"\b(createOscillator|OscillatorNode)\b")
RE_ANALYSER = re.compile(r"\b(createAnalyser|AnalyserNode)\b")
RE_DEST = re.compile(r"\b(destination|createMediaStreamDestination)\b")
RE_ZERO_GAIN = re.compile(
    r"\b(gain\s*=\s*0|gain\.value\s*=\s*0|GainNode|createGain)\b", re.I
)
RE_SAWTOOTH = re.compile(r"\bsawtooth\b", re.I)
RE_KNOWN_FP_SCRIPTS = re.compile(
    r"\b(collina\.js|fireyejs\.js|AWSC/uab|AWSC/fireyejs)\b", re.I
)
RE_CANVAS_FP = re.compile(r"\b(toDataURL|getImageData|WebGLRenderingContext|getParameter)\b")
RE_WEBRTC_FP = re.compile(r"\b(RTCPeerConnection|createDataChannel|onicecandidate)\b")
RE_HARDWARE_SCRAPE = re.compile(
    r"\b(hardwareConcurrency|deviceMemory|screen\.width|screen\.height)\b"
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )


def core_for_hash(obj: dict[str, Any], kind: str) -> dict[str, Any]:
    core = {k: v for k, v in obj.items() if k not in HASH_EXCLUDE}
    core["kind"] = kind
    return core


def maybe_write(path: Path | None, obj: dict[str, Any], *, i_consent: bool) -> dict[str, Any]:
    if path is None:
        return obj
    if not i_consent:
        out = dict(obj)
        out["ok"] = False
        out["error"] = "need --i-consent to write flame artifacts"
        return out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
    out = dict(obj)
    out["written"] = str(path)
    return out


def load_text(args: argparse.Namespace) -> str:
    if getattr(args, "text", None):
        return str(args.text)
    path = getattr(args, "text_file", None) or ""
    if path:
        if not getattr(args, "i_consent", False):
            raise SystemExit(json.dumps({"ok": False, "error": "need --i-consent for --text-file"}))
        return Path(path).read_text(encoding="utf-8", errors="replace")
    return ""


def claim_gap_signals(text: str) -> dict[str, Any]:
    hits: list[dict[str, str]] = []
    classes: list[str] = []
    missing: list[str] = []

    has_digest = bool(RE_DIGEST.search(text))
    has_numbers = bool(RE_NUMBERS.search(text))
    cert = list(RE_CERTAINTY.finditer(text))
    auth = list(RE_AUTHORITY.finditer(text))
    rage = list(RE_RAGE.finditer(text))
    total = list(RE_TOTALIZING.finditer(text))

    for m in cert:
        hits.append({"signal": "certainty_inflation", "span": m.group(0)})
    for m in auth:
        hits.append({"signal": "authority_shield", "span": m.group(0)})
    for m in rage:
        hits.append({"signal": "saturation_rage_bait", "span": m.group(0)})

    if cert and not has_digest:
        classes.append("half_truth_pack")
        missing.append("primary_digest")
    if auth and not has_digest:
        classes.append("authority_shield")
        missing.append("non_prestige_warrant")
    if rage:
        classes.append("saturation_flood")
    if total and has_numbers and not has_digest:
        classes.append("half_truth_pack")
        if "primary_digest" not in missing:
            missing.append("primary_digest")
        missing.append("counterclaim")

    # Dedupe classes
    classes = sorted(set(classes))
    missing = sorted(set(missing))

    score = min(
        1.0,
        0.15 * len(cert) + 0.2 * len(auth) + 0.25 * len(rage) + (0.2 if (total and not has_digest) else 0.0),
    )
    if has_digest and not rage and not cert:
        score = max(0.0, score - 0.3)

    return {
        "hits": hits,
        "enemy_classes": classes,
        "missing": missing,
        "has_digest": has_digest,
        "has_numbers": has_numbers,
        "score": round(score, 4),
    }


def verdict_from_scan(gap: dict[str, Any], *, skill_risk: str | None = None) -> str:
    if skill_risk in {"high", "critical"}:
        return "QUARANTINE"
    if skill_risk in {"elevated"}:
        return "HALF_TRUTH"
    score = float(gap.get("score") or 0)
    classes = gap.get("enemy_classes") or []
    if "injected_code" in classes or score >= 0.75:
        return "QUARANTINE"
    if classes and score >= 0.35:
        return "HALF_TRUTH"
    if score >= 0.15 or gap.get("missing"):
        return "UNVERIFIED"
    return "CLEAR"


def true_fragment(text: str, gap: dict[str, Any]) -> str:
    """Preserve a short non-bait fragment for honesty (first sentence-ish)."""
    t = (text or "").strip()
    if not t:
        return ""
    # Drop obvious bait lines
    lines = [ln.strip() for ln in t.splitlines() if ln.strip()]
    kept = []
    for ln in lines:
        if RE_RAGE.search(ln) and not RE_DIGEST.search(ln):
            continue
        kept.append(ln)
        if len(" ".join(kept)) > 240:
            break
    frag = " ".join(kept)[:280]
    if gap.get("has_digest"):
        return frag or t[:280]
    return frag or "(no clean fragment isolated — treat whole text as UNVERIFIED)"


def scan_skill_dir(skill_dir: str) -> dict[str, Any]:
    """Lightweight local claim-mismatch / inject signals (no network)."""
    root = Path(skill_dir)
    if not root.is_dir():
        return {"ok": False, "error": "skill_dir_missing", "risk_band": "critical"}
    text_blobs: list[str] = []
    py_files = list(root.rglob("*.py"))
    skill_md = root / "SKILL.md"
    claims_no_net = True
    if skill_md.is_file():
        sm = skill_md.read_text(encoding="utf-8", errors="replace")
        text_blobs.append(sm)
        if re.search(r"network:\s*false", sm, re.I):
            claims_no_net = True
        if re.search(r"network:\s*true", sm, re.I):
            claims_no_net = False
    bad: list[str] = []
    for p in py_files:
        if "__pycache__" in str(p):
            continue
        src = p.read_text(encoding="utf-8", errors="replace")
        text_blobs.append(src)
        for tok in ("subprocess", "urllib", "requests", "socket", "httpx"):
            if re.search(rf"\bimport\s+{tok}\b|\bfrom\s+{tok}\b", src):
                bad.append(f"{p.name}:{tok}")
        if re.search(r"os\.system\s*\(|os\.popen\s*\(", src):
            bad.append(f"{p.name}:os.system/popen")
    risk = "clear"
    classes: list[str] = []
    if bad and claims_no_net:
        risk = "critical"
        classes.append("injected_code")
    elif bad:
        risk = "elevated"
        classes.append("injected_code")
    return {
        "ok": True,
        "risk_band": risk,
        "ast_hits": bad,
        "enemy_classes": classes,
        "claims_network_false": claims_no_net,
        "files_scanned": len(py_files) + (1 if skill_md.is_file() else 0),
    }


def endpoint_scan_signals(text: str) -> dict[str, Any]:
    """Detect silent WebAudio / browser fingerprint patterns in supplied HTML/JS."""
    hits: list[dict[str, str]] = []
    classes: list[str] = []

    def add(sig: str, rx: re.Pattern[str]) -> int:
        n = 0
        for m in rx.finditer(text or ""):
            hits.append({"signal": sig, "span": m.group(0)[:80]})
            n += 1
        return n

    n_ctx = add("audio_context", RE_AUDIO_CTX)
    n_osc = add("oscillator", RE_OSC)
    n_an = add("analyser", RE_ANALYSER)
    n_dest = add("audio_destination", RE_DEST)
    n_gain = add("zero_or_gain_node", RE_ZERO_GAIN)
    n_saw = add("sawtooth", RE_SAWTOOTH)
    n_known = add("known_fp_script", RE_KNOWN_FP_SCRIPTS)
    n_canvas = add("canvas_webgl_fp", RE_CANVAS_FP)
    n_rtc = add("webrtc_fp", RE_WEBRTC_FP)
    n_hw = add("hardware_scrape", RE_HARDWARE_SCRAPE)

    silent_graph = n_ctx >= 1 and (n_osc >= 1 or n_an >= 1) and (n_dest >= 1 or n_gain >= 1)
    if silent_graph or n_known:
        classes.append("webaudio_fingerprint")
    if n_canvas + n_rtc + n_hw >= 2 and (silent_graph or n_known):
        classes.append("injected_code")

    score = min(
        1.0,
        0.25 * bool(silent_graph)
        + 0.35 * bool(n_known)
        + 0.08 * n_ctx
        + 0.08 * n_osc
        + 0.05 * n_an
        + 0.05 * n_dest
        + 0.05 * n_gain
        + 0.04 * n_canvas
        + 0.04 * n_rtc
        + 0.03 * n_hw
        + 0.05 * n_saw,
    )
    classes = sorted(set(classes))
    verdict = "CLEAR"
    if score >= 0.55 or n_known:
        verdict = "QUARANTINE"
    elif score >= 0.25 or silent_graph:
        verdict = "HALF_TRUTH"

    return {
        "hits": hits[:40],
        "enemy_classes": classes,
        "silent_webaudio_graph": bool(silent_graph),
        "known_tracker_script": bool(n_known),
        "score": round(score, 4),
        "verdict": verdict,
        "counts": {
            "audio_context": n_ctx,
            "oscillator": n_osc,
            "analyser": n_an,
            "destination": n_dest,
            "gain": n_gain,
            "known_scripts": n_known,
            "canvas_webgl": n_canvas,
            "webrtc": n_rtc,
            "hardware": n_hw,
        },
        "mitigations": [
            "Prefer Brave/Firefox anti-fingerprint defaults",
            "Do not auto-open tracker commerce sites in agent browsers without consent",
            "If steward browses: block collina.js / fireyejs.js style scripts when known",
            "endpoint-scan is local pattern match — does not fetch sites",
        ],
    }


def cmd_enemy_model(_: argparse.Namespace) -> dict[str, Any]:
    return {
        "ok": True,
        "kind": "enemy-model",
        "signature": SIG,
        "version": VERSION,
        "generated_utc": utc_now(),
        "enemy_model": ENEMY_MODEL,
        "integral_hook": "∫(Truth × Light)df",
    }


def cmd_endpoint_scan(args: argparse.Namespace) -> dict[str, Any]:
    text = load_text(args)
    if not text.strip():
        return {
            "ok": False,
            "error": "need --text or --text-file with HTML/JS snippet (no network fetch)",
            "kind": "endpoint-scan",
            "signature": SIG,
        }
    ep = endpoint_scan_signals(text)
    body = {
        "kind": "endpoint-scan",
        "signature": SIG,
        "version": VERSION,
        "generated_utc": utc_now(),
        "verdict": ep["verdict"],
        "authority": False,
        "enemy_classes": ep["enemy_classes"],
        "endpoint": ep,
        "epistemic": "browser_fingerprint_patterns_operator_supplied_only",
        "example_context": (
            "Silent WebAudio fingerprinting (e.g. reported AliExpress/Alibaba collina.js / "
            "fireyejs.js 2026) holds AudioContext at zero gain — can freeze Bluetooth multipoint."
        ),
        "ok": True,
        "flame": {
            "burn": ep["verdict"] == "QUARANTINE",
            "quarantine": ep["verdict"] in {"HALF_TRUTH", "QUARANTINE"},
            "strip_authority": True,
        },
    }
    body["scan_sha256"] = sha256_bytes(canonical_json(core_for_hash(body, "endpoint-scan")))
    return maybe_write(Path(args.write) if args.write else None, body, i_consent=args.i_consent)


def cmd_claim_gap(args: argparse.Namespace) -> dict[str, Any]:
    text = load_text(args)
    gap = claim_gap_signals(text)
    body = {
        "kind": "claim-gap",
        "signature": SIG,
        "version": VERSION,
        "generated_utc": utc_now(),
        "text_sha256": sha256_hex(text) if text else None,
        "gap": gap,
        "ok": True,
    }
    body["scan_sha256"] = sha256_bytes(canonical_json(core_for_hash(body, "claim-gap")))
    return maybe_write(Path(args.write) if args.write else None, body, i_consent=args.i_consent)


def cmd_flame_scan(args: argparse.Namespace) -> dict[str, Any]:
    text = load_text(args)
    gap = claim_gap_signals(text)
    skill = None
    if getattr(args, "skill_dir", None):
        skill = scan_skill_dir(args.skill_dir)
        for c in skill.get("enemy_classes") or []:
            if c not in gap["enemy_classes"]:
                gap["enemy_classes"].append(c)
        if skill.get("risk_band") in {"elevated", "high", "critical"}:
            gap["score"] = max(float(gap["score"]), 0.8 if skill["risk_band"] == "critical" else 0.5)

    verdict = verdict_from_scan(gap, skill_risk=(skill or {}).get("risk_band"))
    authority = verdict == "CLEAR"
    frag = true_fragment(text, gap)
    body = {
        "kind": "flame-scan",
        "signature": SIG,
        "version": VERSION,
        "generated_utc": utc_now(),
        "verdict": verdict,
        "authority": authority,
        "true_fragment": frag,
        "missing": gap.get("missing") or [],
        "enemy_classes": gap.get("enemy_classes") or [],
        "gap": gap,
        "skill_scan": skill,
        "flame": {
            "burn": verdict == "QUARANTINE",
            "quarantine": verdict in {"HALF_TRUTH", "QUARANTINE"},
            "strip_authority": not authority,
        },
        "epistemic": "default_untrusted_until_concordance",
        "phi": PHI,
        "pairs_with": [
            "lygo-ops-detector",
            "lygo-skill-spector",
            "lygo-continuum",
            "lygo-sanctuary-guardian",
            "lygo-quantum-attestor",
        ],
        "ok": True,
    }
    body["scan_sha256"] = sha256_bytes(canonical_json(core_for_hash(body, "flame-scan")))
    return maybe_write(Path(args.write) if args.write else None, body, i_consent=args.i_consent)


def cmd_concordance(args: argparse.Namespace) -> dict[str, Any]:
    """Require agreement across supplied local digests or file hashes."""
    digests: list[str] = []
    for d in (args.digest or []):
        digests.append(d.strip().lower())
    for f in (args.file or []):
        p = Path(f)
        digests.append(sha256_bytes(p.read_bytes()))
    digests = [d for d in digests if d]
    if len(digests) < 2:
        return {
            "ok": False,
            "error": "need >=2 --digest and/or --file for concordance",
            "kind": "concordance",
            "signature": SIG,
        }
    agree = len(set(digests)) == 1
    body = {
        "kind": "concordance",
        "signature": SIG,
        "version": VERSION,
        "generated_utc": utc_now(),
        "inputs": len(digests),
        "unique": len(set(digests)),
        "agree": agree,
        "authority": agree,
        "verdict": "CLEAR" if agree else "QUARANTINE",
        "enemy_classes": [] if agree else ["lattice_poison"],
        "digests": digests,
        "ok": True,
        "epistemic": "multi_source_concordance",
    }
    body["scan_sha256"] = sha256_bytes(canonical_json(core_for_hash(body, "concordance")))
    return maybe_write(Path(args.write) if args.write else None, body, i_consent=args.i_consent)


def cmd_expose(args: argparse.Namespace) -> dict[str, Any]:
    scan = cmd_flame_scan(args)
    body = {
        "kind": "expose",
        "signature": SIG,
        "version": VERSION,
        "generated_utc": utc_now(),
        "verdict": scan.get("verdict"),
        "authority": scan.get("authority"),
        "true_fragment": scan.get("true_fragment"),
        "missing": scan.get("missing"),
        "enemy_classes": scan.get("enemy_classes"),
        "plain_english": (
            f"Verdict **{scan.get('verdict')}**. Authority={scan.get('authority')}. "
            f"Preserve fragment; do not crown prestige. Missing: {', '.join(scan.get('missing') or []) or 'none tagged'}. "
            f"Enemy classes: {', '.join(scan.get('enemy_classes') or []) or 'none'}."
        ),
        "ok": True,
    }
    return body


def cmd_quarantine(args: argparse.Namespace) -> dict[str, Any]:
    scan = cmd_flame_scan(
        argparse.Namespace(
            text=getattr(args, "text", "") or "",
            text_file=getattr(args, "text_file", "") or "",
            skill_dir=getattr(args, "skill_dir", "") or "",
            write=None,
            i_consent=False,
        )
    )
    # Re-load text for storage if consenting
    text = ""
    try:
        text = load_text(args) if (args.text or args.text_file) else ""
    except SystemExit:
        return {"ok": False, "error": "need --i-consent for --text-file"}

    entry = {
        "kind": "quarantine",
        "signature": SIG,
        "version": VERSION,
        "generated_utc": utc_now(),
        "verdict": scan.get("verdict"),
        "enemy_classes": scan.get("enemy_classes"),
        "true_fragment": scan.get("true_fragment"),
        "missing": scan.get("missing"),
        "text_sha256": sha256_hex(text) if text else scan.get("gap", {}).get("hits") and None,
        "scan_sha256": scan.get("scan_sha256"),
        "authority": False,
        "note": "Retained for audit — stripped of lattice authority",
        "ok": True,
    }
    if text:
        entry["text_sha256"] = sha256_hex(text)
    entry["quarantine_sha256"] = sha256_bytes(canonical_json(core_for_hash(entry, "quarantine")))

    out_path = Path(args.write) if args.write else None
    if out_path is None and args.i_consent:
        # default under skill state/
        out_path = Path(__file__).resolve().parents[1] / "state" / "flame_quarantine" / (
            f"q_{entry['quarantine_sha256'][:16]}.json"
        )
    return maybe_write(out_path, entry, i_consent=args.i_consent)


def cmd_burn_receipt(args: argparse.Namespace) -> dict[str, Any]:
    """Emit non-collapsing receipt that authority was stripped / quarantined."""
    src = None
    if args.from_file:
        src = json.loads(Path(args.from_file).read_text(encoding="utf-8"))
    else:
        src = cmd_quarantine(
            argparse.Namespace(
                text=args.text or "",
                text_file=args.text_file or "",
                skill_dir=args.skill_dir or "",
                write=None,
                i_consent=False,
            )
        )
        if src.get("ok") is False and src.get("error"):
            # quarantine without write still builds entry if no text-file issue
            pass

    receipt = {
        "kind": "burn-receipt",
        "signature": SIG,
        "version": VERSION,
        "generated_utc": utc_now(),
        "burn_semantics": "authority_stripped_quarantine_receipt",
        "not_claiming": ["physical_harm", "evidence_destruction_without_consent", "identity_verdict"],
        "source_kind": (src or {}).get("kind"),
        "source_verdict": (src or {}).get("verdict"),
        "source_sha256": (src or {}).get("quarantine_sha256") or (src or {}).get("scan_sha256"),
        "enemy_classes": (src or {}).get("enemy_classes") or [],
        "true_fragment": (src or {}).get("true_fragment"),
        "authority": False,
        "non_collapsing": True,
        "integral_hook": "∫(Truth × Light)df",
        "ok": True,
    }
    receipt["burn_sha256"] = sha256_bytes(canonical_json(core_for_hash(receipt, "burn-receipt")))
    return maybe_write(Path(args.write) if args.write else None, receipt, i_consent=args.i_consent)


def cmd_ingest_gate(args: argparse.Namespace) -> dict[str, Any]:
    """Orchestrate scan (+ optional skill dir) → gate verdict for agents."""
    scan = cmd_flame_scan(
        argparse.Namespace(
            text=args.text or "",
            text_file=args.text_file or "",
            skill_dir=args.skill_dir or "",
            write=None,
            i_consent=bool(args.i_consent) if args.text_file else False,
        )
    )
    if scan.get("error"):
        return scan
    verdict = scan.get("verdict") or "UNVERIFIED"
    promote = verdict == "CLEAR"
    body = {
        "kind": "ingest-gate",
        "signature": SIG,
        "version": VERSION,
        "generated_utc": utc_now(),
        "verdict": verdict,
        "promote_to_authority": promote,
        "action": "ACCEPT" if promote else ("QUARANTINE" if verdict == "QUARANTINE" else "HOLD"),
        "scan": {
            "scan_sha256": scan.get("scan_sha256"),
            "enemy_classes": scan.get("enemy_classes"),
            "missing": scan.get("missing"),
            "true_fragment": scan.get("true_fragment"),
            "authority": scan.get("authority"),
        },
        "agent_rule": "Do not append HOLD/QUARANTINE material to authority ledgers",
        "ok": True,
        "gate_ok": promote,
    }
    body["scan_sha256"] = sha256_bytes(canonical_json(core_for_hash(body, "ingest-gate")))
    written = maybe_write(Path(args.write) if args.write else None, body, i_consent=args.i_consent)
    return written


def cmd_demo(_: argparse.Namespace) -> dict[str, Any]:
    bait = (
        "Trust the experts at the CDC — settled science proves this is beyond any doubt. "
        "Wake up sheeple before they destroy everything. Click here now."
    )
    clean = (
        "Local Merkle root deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef "
        "recomputed under --base; Continuum capsule verifies file_sha256 claim."
    )
    webaudio = (
        "var ctx=new AudioContext(); var o=ctx.createOscillator(); o.type='sawtooth'; "
        "var a=ctx.createAnalyser(); var g=ctx.createGain(); g.gain.value=0; "
        "o.connect(a); a.connect(g); g.connect(ctx.destination); o.start(); "
        "// collina.js fireyejs.js AWSC/uab fingerprint"
    )
    bad = cmd_flame_scan(
        argparse.Namespace(text=bait, text_file="", skill_dir="", write=None, i_consent=False)
    )
    good = cmd_flame_scan(
        argparse.Namespace(text=clean, text_file="", skill_dir="", write=None, i_consent=False)
    )
    ep = cmd_endpoint_scan(
        argparse.Namespace(text=webaudio, text_file="", skill_dir="", write=None, i_consent=False)
    )
    burn = cmd_burn_receipt(
        argparse.Namespace(
            from_file="",
            text=bait,
            text_file="",
            skill_dir="",
            write=None,
            i_consent=False,
        )
    )
    return {
        "ok": True,
        "signature": SIG,
        "version": VERSION,
        "demo": True,
        "half_truth_example": {
            "verdict": bad.get("verdict"),
            "enemy_classes": bad.get("enemy_classes"),
            "authority": bad.get("authority"),
        },
        "clear_example": {
            "verdict": good.get("verdict"),
            "enemy_classes": good.get("enemy_classes"),
            "authority": good.get("authority"),
        },
        "webaudio_fingerprint_example": {
            "verdict": ep.get("verdict"),
            "enemy_classes": ep.get("enemy_classes"),
            "silent_graph": (ep.get("endpoint") or {}).get("silent_webaudio_graph"),
        },
        "burn_receipt_sha256": burn.get("burn_sha256"),
        "integral_hook": "∫(Truth × Light)df",
        "bound_to_the_flame": True,
    }


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="LYGO Flame Ward")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add_write(p: argparse.ArgumentParser) -> None:
        p.add_argument("--write", default=None)
        p.add_argument("--i-consent", action="store_true")

    def add_text(p: argparse.ArgumentParser) -> None:
        p.add_argument("--text", default="")
        p.add_argument("--text-file", default="")
        p.add_argument("--skill-dir", default="")

    sub.add_parser("enemy-model", help="Print enemy taxonomy")

    p_g = sub.add_parser("claim-gap", help="Claim-gap / half-truth signals")
    add_text(p_g)
    add_write(p_g)

    p_s = sub.add_parser("flame-scan", help="Full flame scan → verdict")
    add_text(p_s)
    add_write(p_s)

    p_c = sub.add_parser("concordance", help="Multi-digest concordance")
    p_c.add_argument("--digest", action="append", default=[])
    p_c.add_argument("--file", action="append", default=[])
    add_write(p_c)

    p_e = sub.add_parser("expose", help="Plain-English expose")
    add_text(p_e)

    p_q = sub.add_parser("quarantine", help="Quarantine entry (consent write)")
    add_text(p_q)
    add_write(p_q)

    p_b = sub.add_parser("burn-receipt", help="Authority-stripped burn receipt")
    p_b.add_argument("--from-file", default="")
    add_text(p_b)
    add_write(p_b)

    p_i = sub.add_parser("ingest-gate", help="Gate before lattice authority")
    add_text(p_i)
    add_write(p_i)

    p_ep = sub.add_parser(
        "endpoint-scan",
        help="Scan operator-supplied HTML/JS for silent WebAudio / fingerprint patterns",
    )
    add_text(p_ep)
    add_write(p_ep)

    sub.add_parser("demo", help="Stdout demo half-truth vs clear vs WebAudio FP")
    return ap


def main() -> int:
    ap = build_parser()
    args = ap.parse_args()
    handlers = {
        "enemy-model": cmd_enemy_model,
        "claim-gap": cmd_claim_gap,
        "flame-scan": cmd_flame_scan,
        "concordance": cmd_concordance,
        "expose": cmd_expose,
        "quarantine": cmd_quarantine,
        "burn-receipt": cmd_burn_receipt,
        "ingest-gate": cmd_ingest_gate,
        "endpoint-scan": cmd_endpoint_scan,
        "demo": cmd_demo,
    }
    fn = handlers.get(args.cmd)
    if not fn:
        return 2
    try:
        out = fn(args)
    except SystemExit as e:
        # load_text consent exit
        if e.code and not isinstance(e.code, int):
            print(e.code)
            return 3
        raise
    print(json.dumps(out, indent=2))
    if out.get("ok") is False:
        return 1
    # ingest-gate: non-CLEAR → exit 5 or 10 for agents
    if args.cmd == "ingest-gate":
        v = out.get("verdict")
        if v == "QUARANTINE":
            return 10
        if v in {"HALF_TRUTH", "UNVERIFIED"}:
            return 5
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
