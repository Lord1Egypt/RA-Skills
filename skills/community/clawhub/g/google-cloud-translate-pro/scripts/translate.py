#!/usr/bin/env python3
"""
Google Cloud Translate Pro — CLI wrapper for SocketsIO Translation API.
195 languages, Google Cloud Translation backend.

Usage:
    python3 translate.py "Hello world" --target zh
    python3 translate.py "Bonjour" --detect
    python3 translate.py "Hello" "Goodbye" --target ja --bulk
    python3 translate.py --languages
    python3 translate.py --languages --display zh

Requires: SOCKETSIO_API_KEY environment variable.
Get a free key at https://socketsio.com/signup
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

API_BASE = os.environ.get("SOCKETSIO_API_BASE", "https://api.socketsio.com")
API_KEY = os.environ.get("SOCKETSIO_API_KEY", "")


def _request(method, path, data=None):
    if not API_KEY:
        print("Error: SOCKETSIO_API_KEY not set.", file=sys.stderr)
        print("Get a free key: https://socketsio.com/signup", file=sys.stderr)
        sys.exit(1)

    url = f"{API_BASE}{path}"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = json.loads(e.read()) if e.headers.get("content-type", "").startswith("application/json") else {"error": str(e)}
        print(f"API Error ({e.code}): {json.dumps(err, indent=2)}", file=sys.stderr)
        sys.exit(1)


def translate(texts, target, source="auto"):
    if len(texts) == 1:
        data = {"q": texts[0], "target": target}
        if source != "auto":
            data["source"] = source
        result = _request("POST", "/v1/translate", data)
        t = result["data"]["translations"][0]
        print(t["translatedText"])
        if "detectedSourceLanguage" in t:
            print(f"  (detected: {t['detectedSourceLanguage']})", file=sys.stderr)
    else:
        data = {"q": texts, "target": target}
        if source != "auto":
            data["source"] = source
        result = _request("POST", "/v1/translate", data)
        for t in result["data"]["translations"]:
            print(t["translatedText"])


def detect(text):
    result = _request("POST", "/v1/detect", {"q": text})
    detections = result["data"]["detections"]
    for d in detections:
        print(f"{d['language']} (confidence: {d.get('confidence', 'N/A')})")


def languages(display_lang=None):
    path = "/v1/languages"
    if display_lang:
        path += f"?target={display_lang}"
    result = _request("GET", path)
    langs = result.get("data", result).get("languages", [])
    for lang in langs:
        name = lang.get("name", "")
        code = lang.get("language", "")
        if name:
            print(f"{code:6s} {name}")
        else:
            print(code)
    print(f"\nTotal: {len(langs)} languages", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Translate text using Google Cloud Translation (195 languages)")
    parser.add_argument("text", nargs="*", help="Text to translate or detect")
    parser.add_argument("--target", "-t", help="Target language code (e.g., zh, es, ja)")
    parser.add_argument("--source", "-s", default="auto", help="Source language (default: auto-detect)")
    parser.add_argument("--detect", "-d", action="store_true", help="Detect language instead of translating")
    parser.add_argument("--bulk", "-b", action="store_true", help="Translate multiple texts")
    parser.add_argument("--languages", "-l", action="store_true", help="List all supported languages")
    parser.add_argument("--display", help="Display language names in this language")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    if args.languages:
        languages(args.display)
    elif args.detect:
        if not args.text:
            parser.error("Provide text to detect")
        detect(" ".join(args.text))
    elif args.text:
        if not args.target:
            parser.error("--target required for translation")
        translate(args.text, args.target, args.source)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
