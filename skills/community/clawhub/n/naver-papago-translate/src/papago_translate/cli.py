import argparse
import json
import sys
from pathlib import Path
from .core import translate_text, detect_language, PapagoError


def parse_args(argv=None):
    p = argparse.ArgumentParser(prog="papago-translate", description="Naver Papago NMT translation CLI")
    p.add_argument("text", nargs="?", help="Text to translate (omit if using --file)")
    p.add_argument("--source", "-s", dest="source", default=None, help="Source language code (e.g., ko, en, ja, zh-CN, zh-TW)")
    p.add_argument("--target", "-t", dest="target", required=True, help="Target language code")
    p.add_argument("--file", "-f", dest="file", type=str, help="Read input text from file path")
    p.add_argument("--detect", action="store_true", help="Auto-detect source language via Papago detectLangs")
    p.add_argument("--json", dest="json_out", action="store_true", help="Output JSON with metadata")
    p.add_argument("--timeout", type=float, default=15.0, help="HTTP timeout seconds")
    p.add_argument("--client-id", dest="client_id", default=None, help="Override NAVER_CLIENT_ID")
    p.add_argument("--client-secret", dest="client_secret", default=None, help="Override NAVER_CLIENT_SECRET")
    p.add_argument("--verbose", "-v", action="store_true", help="Verbose logging to stderr")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    else:
        text = args.text or ""

    if not text.strip():
        print("Error: No input text provided (arg or --file)", file=sys.stderr)
        return 2

    try:
        source = args.source
        if args.detect:
            source = detect_language(text, client_id=args.client_id, client_secret=args.client_secret, timeout=args.timeout)
            if args.verbose:
                print(f"Detected source language: {source}", file=sys.stderr)
        translated = translate_text(source, args.target, text, client_id=args.client_id, client_secret=args.client_secret, timeout=args.timeout)
        if args.json_out:
            out = {
                "source": source,
                "target": args.target,
                "input_length": len(text),
                "translated": translated,
            }
            print(json.dumps(out, ensure_ascii=False))
        else:
            print(translated)
        return 0
    except PapagoError as e:
        if args.verbose:
            print(f"PapagoError: {e}", file=sys.stderr)
        else:
            print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
