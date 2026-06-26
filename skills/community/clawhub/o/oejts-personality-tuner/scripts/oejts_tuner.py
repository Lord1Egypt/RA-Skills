#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path

ITEMS = [
    ("Q1", "makes lists", "relies on memory"),
    ("Q2", "sceptical", "wants to believe"),
    ("Q3", "bored by time alone", "needs time alone"),
    ("Q4", "accepts things as they are", "unsatisfied with the ways things are"),
    ("Q5", "keeps a clean room", "just puts stuff where ever"),
    ("Q6", "thinks \"robotic\" is an insult", "strives to have a mechanical mind"),
    ("Q7", "energetic", "mellow"),
    ("Q8", "prefer to take multiple choice test", "prefer essay answers"),
    ("Q9", "chaotic", "organized"),
    ("Q10", "easily hurt", "thick-skinned"),
    ("Q11", "works best in groups", "works best alone"),
    ("Q12", "focused on the present", "focused on the future"),
    ("Q13", "plans far ahead", "plans at the last minute"),
    ("Q14", "wants people's respect", "wants their love"),
    ("Q15", "gets worn out by parties", "gets fired up by parties"),
    ("Q16", "fits in", "stands out"),
    ("Q17", "keeps options open", "commits"),
    ("Q18", "wants to be good at fixing things", "wants to be good at fixing people"),
    ("Q19", "talks more", "listens more"),
    ("Q20", "when describing an event, will tell people what happened", "when describing an event, will tell people what it meant"),
    ("Q21", "gets work done right away", "procrastinates"),
    ("Q22", "follows the heart", "follows the head"),
    ("Q23", "stays at home", "goes out on the town"),
    ("Q24", "wants the big picture", "wants the details"),
    ("Q25", "improvises", "prepares"),
    ("Q26", "bases morality on justice", "bases morality on compassion"),
    ("Q27", "finds it difficult to yell very loudly", "yelling to others when they are far away comes naturally"),
    ("Q28", "theoretical", "empirical"),
    ("Q29", "works hard", "plays hard"),
    ("Q30", "uncomfortable with emotions", "values emotions"),
    ("Q31", "likes to perform in front of other people", "avoids public speaking"),
    ("Q32", "likes to know \"who?\", \"what?\", \"when?\"", "likes to know \"why?\""),
]

Q = {k: None for k, _, _ in ITEMS}


def parse_answers(raw: str):
    data = json.loads(raw)
    missing = [k for k in Q if k not in data]
    if missing:
        raise ValueError(f"Missing answers: {', '.join(missing)}")
    parsed = {}
    for k in Q:
        v = int(data[k])
        if v < 1 or v > 5:
            raise ValueError(f"{k} must be in range 1..5")
        parsed[k] = v
    return parsed


def score(a):
    IE = 30 - a["Q3"] - a["Q7"] - a["Q11"] + a["Q15"] - a["Q19"] + a["Q23"] + a["Q27"] - a["Q31"]
    SN = 12 + a["Q4"] + a["Q8"] + a["Q12"] + a["Q16"] + a["Q20"] - a["Q24"] - a["Q28"] + a["Q32"]
    FT = 30 - a["Q2"] + a["Q6"] + a["Q10"] - a["Q14"] - a["Q18"] + a["Q22"] - a["Q26"] - a["Q30"]
    JP = 18 + a["Q1"] + a["Q5"] - a["Q9"] + a["Q13"] - a["Q17"] + a["Q21"] - a["Q25"] + a["Q29"]

    typ = (
        ("E" if IE > 24 else "I") +
        ("N" if SN > 24 else "S") +
        ("T" if FT > 24 else "F") +
        ("P" if JP > 24 else "J")
    )

    deltas = {
        "IE": abs(IE - 24),
        "SN": abs(SN - 24),
        "FT": abs(FT - 24),
        "JP": abs(JP - 24),
    }
    min_delta = min(deltas.values())
    if min_delta >= 4:
        confidence = "high"
    elif min_delta >= 2:
        confidence = "medium"
    else:
        confidence = "low"

    return {
        "type": typ,
        "scores": {"IE": IE, "SN": SN, "FT": FT, "JP": JP},
        "distanceFromCutoff": deltas,
        "confidence": confidence,
        "computedAt": datetime.now().isoformat(timespec="seconds"),
    }


def behavior_for_type(t):
    mode = "adaptive"
    prefs = {
        "interaction": "deeper async responses" if t[0] == "I" else "more interactive cadence",
        "informationStyle": "concrete, step-by-step" if t[1] == "S" else "pattern-based, big-picture",
        "decisionStyle": "logic-first framing" if t[2] == "T" else "impact-on-people framing",
        "executionStyle": "structured plans and sequencing" if t[3] == "J" else "optionality with lightweight structure",
    }
    return mode, prefs


def render_template(fmt):
    if fmt == "json":
        print(json.dumps({
            "version": "OEJTS-1.2",
            "scale": {"min": 1, "max": 5},
            "items": [{"id": i, "left": l, "right": r} for i, l, r in ITEMS]
        }, indent=2))
        return

    print("# OEJTS 1.2 Questionnaire\n")
    print("Rate each item from 1 to 5 (1=left trait, 5=right trait).\n")
    for i, l, r in ITEMS:
        print(f"- {i}: {l}  <1 2 3 4 5>  {r}")


def upsert_block(text: str, start: str, end: str, block: str):
    if start in text and end in text:
        a = text.index(start)
        b = text.index(end) + len(end)
        return text[:a] + block + text[b:]
    if not text.endswith("\n"):
        text += "\n"
    return text + "\n" + block + "\n"


def apply_updates(workspace: Path, result: dict, dry_run: bool):
    user_md = workspace / "USER.md"
    soul_md = workspace / "SOUL.md"

    mode, prefs = behavior_for_type(result["type"])

    user_block = f"""<!-- OJTS_PROFILE_START -->
## Personality Profile (OEJTS 1.2)
- **Type:** {result['type']}
- **Confidence:** {result['confidence']}
- **Scores:** IE={result['scores']['IE']}, SN={result['scores']['SN']}, FT={result['scores']['FT']}, JP={result['scores']['JP']}
- **Computed:** {result['computedAt']}

### Interaction Preferences
- **Interaction cadence:** {prefs['interaction']}
- **Information style:** {prefs['informationStyle']}
- **Decision framing:** {prefs['decisionStyle']}
- **Execution style:** {prefs['executionStyle']}

> Note: Treat as a preference signal and refine from feedback.
<!-- OJTS_PROFILE_END -->"""

    soul_block = f"""<!-- OJTS_ADAPTATION_START -->
## Adaptive Personality Tuning

When USER.md includes OEJTS profile data:
- Use **{mode} mode** by default.
- Mirror tone and communication style preferences.
- Add complementary structure only when it helps task completion.
- If live user feedback conflicts with profile, feedback wins.
- Offer a style override at any time.
<!-- OJTS_ADAPTATION_END -->"""

    user_text = user_md.read_text() if user_md.exists() else "# USER.md\n"
    soul_text = soul_md.read_text() if soul_md.exists() else "# SOUL.md\n"

    new_user = upsert_block(user_text, "<!-- OJTS_PROFILE_START -->", "<!-- OJTS_PROFILE_END -->", user_block)
    new_soul = upsert_block(soul_text, "<!-- OJTS_ADAPTATION_START -->", "<!-- OJTS_ADAPTATION_END -->", soul_block)

    if dry_run:
        print("=== USER.md preview ===")
        print(user_block)
        print("\n=== SOUL.md preview ===")
        print(soul_block)
        return

    user_md.write_text(new_user)
    soul_md.write_text(new_soul)
    print(f"Updated: {user_md}")
    print(f"Updated: {soul_md}")


def main():
    p = argparse.ArgumentParser(description="OEJTS 1.2 scoring + workspace tuning helper")
    sp = p.add_subparsers(dest="cmd", required=True)

    t = sp.add_parser("template", help="Print questionnaire template")
    t.add_argument("--format", choices=["markdown", "json"], default="markdown")

    s = sp.add_parser("score", help="Score OEJTS answers")
    s.add_argument("--answers-json", required=True, help='JSON object containing Q1..Q32 with values 1..5')

    a = sp.add_parser("apply", help="Apply USER.md/SOUL.md tuning blocks")
    a.add_argument("--workspace", required=True)
    a.add_argument("--answers-json", required=True)
    a.add_argument("--dry-run", action="store_true")

    args = p.parse_args()

    if args.cmd == "template":
        render_template(args.format)
        return

    answers = parse_answers(args.answers_json)
    result = score(answers)

    if args.cmd == "score":
        print(json.dumps(result, indent=2))
        return

    apply_updates(Path(args.workspace).expanduser(), result, args.dry_run)


if __name__ == "__main__":
    main()
