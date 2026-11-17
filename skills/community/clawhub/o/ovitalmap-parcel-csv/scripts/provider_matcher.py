"""Match provider names conservatively without guessing identity."""

import json
import re
import sys


def _normalize(value):
    """Normalize spacing and common separators for exact comparisons."""
    return re.sub(r"[\s\-_.\u00b7]+", "", str(value).strip().casefold())


def match_provider(input_name, existing_names):
    """Return an existing name only when its normalized form is identical."""
    input_normalized = _normalize(input_name)
    exact_match = next(
        (
            name
            for name in dict.fromkeys(existing_names)
            if input_normalized and _normalize(name) == input_normalized
        ),
        None,
    )
    candidates = (
        [{"name": exact_match, "reason": "normalized_exact", "score": 100}]
        if exact_match
        else []
    )
    return {
        "exact_match": exact_match,
        "candidates": candidates,
        "ambiguous": False,
        "input_name": input_name,
    }


# Preserve the callable name used by the pipeline.
fuzzy_match = match_provider


def main():
    try:
        data = json.load(sys.stdin)
        result = match_provider(data["input_name"], data.get("existing_names", []))
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    except (KeyError, TypeError, ValueError) as exc:
        json.dump({"error": str(exc)}, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
        raise SystemExit(2)


if __name__ == "__main__":
    main()
