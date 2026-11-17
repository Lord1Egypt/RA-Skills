#!/usr/bin/env python3
"""
Team pipeline: scan a folder of individual result/answer JSON files,
score if needed, aggregate, and generate a team PDF report.

Usage:
    python3 scripts/team_pipeline.py <folder> [--output report.pdf]
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile

EXIT_GENERAL = 3


def fail(msg, code=EXIT_GENERAL):
    print("ERROR:", msg, file=sys.stderr)
    sys.exit(code)


def is_result(doc):
    """A result.json has 'type' and 'dimensions'."""
    return isinstance(doc, dict) and "type" in doc and "dimensions" in doc


def is_answers(doc):
    """An answers.json has 'version' and 'answers' list."""
    return isinstance(doc, dict) and "version" in doc and isinstance(
        doc.get("answers"), list
    )


def score_answers(doc):
    """Run score.py on an answers dict, return result dict."""
    fd, path = tempfile.mkstemp(suffix=".json")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(doc, f)
        out_path = tempfile.mktemp(suffix=".json")
        subprocess.run(
            [sys.executable, os.path.join(os.path.dirname(__file__), "score.py"), path, "-o", out_path],
            check=True,
            capture_output=True,
            text=True,
        )
        with open(out_path) as f:
            result = json.load(f)
        os.unlink(out_path)
        return result
    finally:
        os.unlink(path)


def load_and_score(path):
    """Load a JSON file. If it's answers, score it; if result, use directly."""
    with open(path) as f:
        doc = json.load(f)

    if is_result(doc):
        return doc
    if is_answers(doc):
        print(f"  [score] {os.path.basename(path)}")
        return score_answers(doc)

    # Try to interpret as a list of answers or results
    if isinstance(doc, list):
        results = []
        for item in doc:
            if is_result(item):
                results.append(item)
            elif is_answers(item):
                print(f"  [score] {os.path.basename(path)} (batch)")
                results.append(score_answers(item))
            else:
                print(f"  [skip] unknown item in {os.path.basename(path)}")
        return results

    fail(f"{path}: unrecognized JSON format (expected result.json or answers.json)")


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate individual MBTI results into a team PDF report."
    )
    parser.add_argument("folder", help="Folder containing *.json files")
    parser.add_argument("-o", "--output", default=None, help="Output PDF path")
    args = parser.parse_args()

    folder = args.folder
    if not os.path.isdir(folder):
        fail(f"not a directory: {folder}")

    # Collect all JSON files
    files = sorted(
        [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".json")]
    )
    if not files:
        fail(f"no .json files found in {folder}")

    print(f"Found {len(files)} JSON file(s) in {folder}")

    results = []
    for path in files:
        print(f"Processing {os.path.basename(path)}...")
        out = load_and_score(path)
        if isinstance(out, list):
            results.extend(out)
        else:
            results.append(out)

    print(f"\nAggregated {len(results)} result(s)")
    for r in results:
        name = r.get("nickname") or r.get("type")
        print(f"  - {name}: {r['type']} ({r['name_cn']} / {r['name_en']})")

    # Write aggregated array
    fd, agg_path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Determine output path
    if args.output:
        out_pdf = args.output
    else:
        from datetime import datetime

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_pdf = os.path.join(folder, f"MBTI_Team_Report_{ts}.pdf")

    # Generate team report
    print(f"\nGenerating team report → {out_pdf}")
    subprocess.run(
        [
            sys.executable,
            os.path.join(os.path.dirname(__file__), "generate_report.py"),
            agg_path,
            "--team",
            "-o",
            out_pdf,
        ],
        check=True,
    )

    os.unlink(agg_path)
    print(f"\nDone: {out_pdf}")


if __name__ == "__main__":
    main()
