from __future__ import annotations

import argparse
import json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--answer-json", required=True)
    parser.add_argument("--read-pages-json", required=True)
    args = parser.parse_args()
    answer = json.loads(open(args.answer_json, encoding="utf-8").read())
    read_pages = json.loads(open(args.read_pages_json, encoding="utf-8").read())
    allowed = {(p["repoFullName"], p["path"]) for p in read_pages}
    errors = []
    for citation in answer.get("citations", []):
        if (citation.get("repoFullName"), citation.get("path")) not in allowed:
            errors.append({"code": "CITATION_NOT_READ", "message": citation.get("path", "")})
    print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False))


if __name__ == "__main__":
    main()
