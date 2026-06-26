#!/usr/bin/env python3
import json
import sys

from job_models import dump_json, normalize_salary_text


def main():
    if len(sys.argv) < 2:
        print("Usage: normalize_salary.py '<salary text>'", file=sys.stderr)
        sys.exit(2)
    text = " ".join(sys.argv[1:])
    print(dump_json(normalize_salary_text(text)))


if __name__ == "__main__":
    main()
