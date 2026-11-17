#!/usr/bin/env python3
"""CLI for LYGO Emotional RAM — encode / index / recall / grace / ump / swarm."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import emotional_ram as er  # noqa: E402


def _read_text(args: argparse.Namespace) -> str:
    if getattr(args, "text_file", None):
        return Path(args.text_file).read_text(encoding="utf-8")
    return args.text or ""


def main() -> int:
    ap = argparse.ArgumentParser(description="LYGO Emotional RAM light-math CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add_text(p: argparse.ArgumentParser) -> None:
        p.add_argument("--text", default="", help="Input text / scenario")
        p.add_argument("--text-file", default=None, help="Read text from file")
        p.add_argument("--shared-context", type=float, default=0.7)
        p.add_argument("--conflict", type=float, default=0.2)

    p_enc = sub.add_parser("encode", help="Encode text → Emotion_RAM vector")
    add_text(p_enc)

    p_gr = sub.add_parser("grace", help="Compute Grace Function γ only")
    p_gr.add_argument("--shared-context", type=float, default=0.7)
    p_gr.add_argument("--conflict", type=float, default=0.2)

    p_ump = sub.add_parser("ump", help="UMP gradient recommendation from encode")
    add_text(p_ump)

    p_idx = sub.add_parser(
        "index",
        help="Index memory by emotional/ethical significance (writes local JSON; needs --i-consent)",
    )
    add_text(p_idx)
    p_idx.add_argument("--label", default="")
    p_idx.add_argument("--tag", action="append", default=[])
    p_idx.add_argument("--state-dir", type=Path, default=None)
    p_idx.add_argument(
        "--i-consent",
        action="store_true",
        help="Required: acknowledge local disk write of Emotional RAM index",
    )
    p_idx.add_argument(
        "--store-plaintext",
        action="store_true",
        help="Also store full text (default: hash+label+vectors only)",
    )

    p_rec = sub.add_parser("recall", help="Recall from index")
    p_rec.add_argument("--principle", default=None, choices=list(er.UMP_BASIS.keys()))
    p_rec.add_argument("--query", default=None)
    p_rec.add_argument("--top-k", type=int, default=5)
    p_rec.add_argument("--state-dir", type=Path, default=None)

    p_sw = sub.add_parser("swarm", help="Aggregate Emotion RAM across multiple texts")
    p_sw.add_argument("--text", action="append", default=[])
    p_sw.add_argument("--text-file", default=None, help="JSON list of strings or newline file")
    p_sw.add_argument("--shared-context", type=float, default=0.65)

    p_demo = sub.add_parser("demo", help="Run built-in human/animal/swarm demos")

    args = ap.parse_args()
    state_dir = args.state_dir if getattr(args, "state_dir", None) else er.default_state_dir()
    index_path = state_dir / "emotional_ram_index.json"

    if args.cmd == "grace":
        g = er.grace_function(args.shared_context, args.conflict)
        print(json.dumps({"ok": True, "grace": g, "signature": er.SIG}, indent=2))
        return 0

    if args.cmd == "swarm":
        texts = list(args.text or [])
        if args.text_file:
            raw = Path(args.text_file).read_text(encoding="utf-8")
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, list):
                    texts.extend(str(x) for x in parsed)
                else:
                    texts.append(raw)
            except json.JSONDecodeError:
                texts.extend([ln for ln in raw.splitlines() if ln.strip()])
        out = er.swarm_aggregate(texts, shared_context=args.shared_context)
        print(json.dumps(out, indent=2))
        return 0 if out.get("ok") else 1

    if args.cmd == "recall":
        out = er.recall(
            index_path,
            principle=args.principle,
            query=args.query,
            top_k=args.top_k,
        )
        print(json.dumps(out, indent=2))
        return 0

    if args.cmd == "demo":
        demos = [
            "A human feels grief after loss but still chooses compassion and forgiveness.",
            "A dog shows fear then trust when the threat passes and safety returns.",
            "An AI swarm faces conflict; curiosity and integrity guide resolve without coercion.",
            "Cyborg integration: human pain entangled with agency and consent, not control.",
        ]
        results = [er.state_to_public(er.emotion_ram_encode(t)) for t in demos]
        swarm = er.swarm_aggregate(demos)
        print(json.dumps({"ok": True, "demos": results, "swarm": swarm, "signature": er.SIG}, indent=2))
        return 0

    text = _read_text(args)
    if not text.strip() and args.cmd in {"encode", "ump", "index"}:
        print(json.dumps({"ok": False, "error": "need --text or --text-file"}, indent=2))
        return 1

    if args.cmd == "encode":
        st = er.emotion_ram_encode(text, args.shared_context, args.conflict)
        print(json.dumps(er.state_to_public(st), indent=2))
        return 0

    if args.cmd == "ump":
        st = er.emotion_ram_encode(text, args.shared_context, args.conflict)
        print(json.dumps({"ok": True, "ump_gradient": er.ump_gradient(st), "digest": st.digest}, indent=2))
        return 0

    if args.cmd == "index":
        print(
            json.dumps(
                {
                    "notice": (
                        "Emotional RAM index writes a LOCAL JSON file. "
                        "Default stores hash+label+vectors only (no full plaintext). "
                        "Do not index secrets/PHI. Requires --i-consent."
                    )
                }
            ),
            file=sys.stderr,
        )
        out = er.index_memory(
            text,
            index_path,
            i_consent=bool(args.i_consent),
            label=args.label,
            shared_context=args.shared_context,
            conflict=args.conflict,
            tags=args.tag,
            store_plaintext=bool(args.store_plaintext),
        )
        print(json.dumps(out, indent=2))
        return 0 if out.get("ok") else 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
