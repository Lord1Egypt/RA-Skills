#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MBTI scoring script.

Usage:
    python3 score.py <answers.json> [-o result.json]

Reads the shared question bank, validates the selected version's dimension
matrix (fail loud), scores the answers and writes a result.json consumed by
generate_report.py.
"""

import argparse
import itertools
import json
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "data")

DIMENSIONS = ["E/I", "S/N", "T/F", "J/P"]
DIMENSION_POLES = {
    "E/I": ("E", "I"),
    "S/N": ("S", "N"),
    "T/F": ("T", "F"),
    "J/P": ("J", "P"),
}
# Tie-breaker: ties resolve to I / N / F / P.
TIE_WINNER = {"E/I": "I", "S/N": "N", "T/F": "F", "J/P": "P"}

# Version selection rules over questions.json.
VERSION_FILTERS = {
    "quick": lambda q: q["version_added"] == 1,
    "standard": lambda q: q["version_added"] <= 2,
    "pro": lambda q: True,
}

# Expected dimension distribution matrix per version (from data design).
EXPECTED_MATRIX = {
    "quick": {"E/I": 16, "S/N": 19, "T/F": 18, "J/P": 17},
    "standard": {"E/I": 21, "S/N": 26, "T/F": 24, "J/P": 22},
    "pro": {"E/I": 32, "S/N": 40, "T/F": 38, "J/P": 34},
}

CLARITY_BANDS = [
    (25, "Slight", "轻微"),
    (50, "Moderate", "中等"),
    (75, "Clear", "清晰"),
    (float("inf"), "Very Clear", "非常清晰"),
]

EXIT_DATA_ERROR = 2
EXIT_ANSWER_ERROR = 3
EXIT_GENERAL = 1


def fail(msg, code=EXIT_GENERAL):
    sys.stderr.write("ERROR: %s\n" % msg)
    sys.exit(code)


def load_json(path, what):
    if not os.path.isfile(path):
        fail("%s not found: %s" % (what, path), EXIT_DATA_ERROR)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as exc:
        fail("cannot read %s (%s): %s" % (what, path, exc), EXIT_DATA_ERROR)


def load_question_bank():
    questions = load_json(os.path.join(DATA_DIR, "questions.json"), "question bank")
    if not isinstance(questions, list) or not questions:
        fail("question bank is empty or malformed", EXIT_DATA_ERROR)
    for q in questions:
        for field in ("id", "version_added", "dimension", "choice_a", "choice_b"):
            if field not in q:
                fail("question missing field '%s': %r" % (field, q), EXIT_DATA_ERROR)
    return questions


def select_version(questions, version):
    """Select questions for a version and validate the dimension matrix."""
    subset = [q for q in questions if VERSION_FILTERS[version](q)]
    expected = EXPECTED_MATRIX[version]
    actual = {dim: 0 for dim in DIMENSIONS}
    for q in subset:
        if q["dimension"] not in actual:
            fail("question %s has unknown dimension %r" % (q["id"], q["dimension"]),
                 EXIT_DATA_ERROR)
        actual[q["dimension"]] += 1
    for dim in DIMENSIONS:
        if actual[dim] != expected[dim]:
            fail("dimension matrix mismatch for version '%s', dimension %s: "
                 "expected %d questions, got %d (dataset integrity failure)"
                 % (version, dim, expected[dim], actual[dim]), EXIT_DATA_ERROR)
    return subset


def clarity_band(clarity):
    for upper, band_en, band_zh in CLARITY_BANDS:
        if clarity <= upper:
            return band_en, band_zh
    return CLARITY_BANDS[-1][1], CLARITY_BANDS[-1][2]


def score(questions, answers_by_id):
    """Score answers; returns dimensions dict, type code, and derived metrics."""
    dimensions = {}
    type_letters = []
    tendency = {}  # dim -> percentage of the FIRST pole (for similarity)
    for dim in DIMENSIONS:
        pole_a, pole_b = DIMENSION_POLES[dim]
        counts = {pole_a: 0, pole_b: 0}
        total = 0
        for q in questions:
            if q["dimension"] != dim:
                continue
            total += 1
            choice = answers_by_id[q["id"]]
            option = q["choice_a"] if choice == "A" else q["choice_b"]
            value = option["value"]
            if value not in counts:
                fail("question %s has unknown pole value %r" % (q["id"], value),
                     EXIT_DATA_ERROR)
            counts[value] += 1
        if counts[pole_a] > counts[pole_b]:
            winner = pole_a
        elif counts[pole_b] > counts[pole_a]:
            winner = pole_b
        else:
            winner = TIE_WINNER[dim]
        pct = counts[winner] / total * 100.0
        clarity = abs(pct - 50.0) * 2.0
        band_en, band_zh = clarity_band(clarity)
        dimensions[dim] = {
            "counts": {pole_a: counts[pole_a], pole_b: counts[pole_b]},
            "total": total,
            "winner": winner,
            "pct": round(pct, 1),
            "clarity": round(clarity, 1),
            "band_zh": band_zh,
            "band_en": band_en,
        }
        type_letters.append(winner)
        # Tendency vector component: pct of pole_a in this dimension.
        tendency[dim] = pct if winner == pole_a else 100.0 - pct
    return dimensions, "".join(type_letters), tendency


def top3_similar(result_type, tendency):
    """Top 3 similar types via Manhattan distance over 4 tendency components."""
    scored = []
    for code in TYPE_CODES:
        std = {}
        for dim in DIMENSIONS:
            pole_a = DIMENSION_POLES[dim][0]
            std[dim] = 100.0 if code[DIMENSIONS.index(dim)] == pole_a else 0.0
        distance = sum(abs(tendency[dim] - std[dim]) for dim in DIMENSIONS)
        similarity = (1.0 - distance / 400.0) * 100.0
        if code == result_type:
            continue
        scored.append({"type": code, "similarity_pct": round(similarity, 1)})
    scored.sort(key=lambda item: (-item["similarity_pct"], item["type"]))
    return scored[:3]


def main():
    parser = argparse.ArgumentParser(description="Score MBTI quiz answers.")
    parser.add_argument("answers", help="path to answers.json")
    parser.add_argument("-o", "--output", help="path to result.json (default: "
                        "result.json next to the answers file)")
    args = parser.parse_args()

    answer_doc = load_json(args.answers, "answers file")
    if not isinstance(answer_doc, dict):
        fail("answers file must be a JSON object", EXIT_ANSWER_ERROR)
    version = answer_doc.get("version")
    if version not in VERSION_FILTERS:
        fail("answers file has invalid 'version' %r (expected quick/standard/pro)"
             % version, EXIT_ANSWER_ERROR)

    questions = load_question_bank()
    subset = select_version(questions, version)
    valid_ids = {q["id"] for q in subset}

    raw_answers = answer_doc.get("answers")
    if not isinstance(raw_answers, list):
        fail("answers file has no 'answers' list", EXIT_ANSWER_ERROR)
    answers_by_id = {}
    for item in raw_answers:
        if not isinstance(item, dict) or "id" not in item or "choice" not in item:
            fail("invalid answer entry: %r" % (item,), EXIT_ANSWER_ERROR)
        qid, choice = item["id"], item["choice"]
        if qid not in valid_ids:
            fail("answer id %r is not in version '%s' question set (exit 3)"
                 % (qid, version), EXIT_ANSWER_ERROR)
        if str(choice).upper() not in ("A", "B"):
            fail("answer for question %r must be 'A' or 'B', got %r (exit 3)"
                 % (qid, choice), EXIT_ANSWER_ERROR)
        if qid in answers_by_id:
            fail("duplicate answer for question %r (exit 3)" % qid, EXIT_ANSWER_ERROR)
        answers_by_id[qid] = str(choice).upper()

    missing = sorted(valid_ids - set(answers_by_id))
    if missing:
        fail("answers incomplete for version '%s': %d of %d answered, missing "
             "question ids: %s (exit 3)"
             % (version, len(answers_by_id), len(valid_ids), ", ".join(map(str, missing))),
             EXIT_ANSWER_ERROR)

    profiles = load_json(os.path.join(DATA_DIR, "type_profiles.json"), "type profiles")
    dimensions, result_type, tendency = score(subset, answers_by_id)
    if result_type not in profiles:
        fail("computed type %r missing from type_profiles.json" % result_type,
             EXIT_DATA_ERROR)

    clarity_values = [dimensions[d]["clarity"] for d in DIMENSIONS]
    overall_clarity = round(sum(clarity_values) / len(clarity_values), 1)
    borderline = [d for d in DIMENSIONS if dimensions[d]["clarity"] <= 25]

    result = {
        "version": version,
        "nickname": answer_doc.get("nickname") or "",
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "type": result_type,
        "name_cn": profiles[result_type]["name_cn"],
        "name_en": profiles[result_type]["name_en"],
        "dimensions": dimensions,
        "overall_clarity": overall_clarity,
        "top3_similar": top3_similar(result_type, tendency),
        "borderline_dimensions": borderline,
    }

    out_path = args.output or os.path.join(
        os.path.dirname(os.path.abspath(args.answers)), "result.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)

    print("Scored %d answers (version=%s)" % (len(answers_by_id), version))
    print("Type: %s  %s / %s" % (result_type, result["name_cn"], result["name_en"]))
    for dim in DIMENSIONS:
        info = dimensions[dim]
        counts = info["counts"]
        poles = DIMENSION_POLES[dim]
        print("  %s: %s=%d %s=%d -> %s %.1f%% | clarity %.1f (%s / %s)%s"
              % (dim, poles[0], counts[poles[0]], poles[1], counts[poles[1]],
                 info["winner"], info["pct"], info["clarity"],
                 info["band_zh"], info["band_en"],
                 "  [Borderline/边界倾向]" if dim in borderline else ""))
    print("Overall clarity: %.1f" % overall_clarity)
    print("Top 3 similar: %s" % ", ".join(
        "%s %.1f%%" % (s["type"], s["similarity_pct"]) for s in result["top3_similar"]))
    print("Result written to: %s" % os.path.abspath(out_path))


# Standard 16 type codes, generated from dimension poles (no external data needed).
TYPE_CODES = ["".join(combo) for combo in itertools.product(
    *(DIMENSION_POLES[d] for d in DIMENSIONS))]

if __name__ == "__main__":
    main()
