#!/usr/bin/env python3
"""Parent-Teacher Conference Prep — dossier, question bank, jargon
decoder, action plan. Stdlib only."""
import argparse
from datetime import date, timedelta

STAGES = {
    (0, 2): "K-2  (early skills + social basics)",
    (3, 5): "3-5  (work habits + peer structure)",
    (6, 8): "6-8  (organization + academic identity)",
    (9, 12): "9-12 (transcripts + teacher strategies)",
}

def stage_of(grade):
    for (lo, hi), label in STAGES.items():
        if lo <= grade <= hi:
            return label
    return "?"

# (lane, question) — generic core, stage-tuned additions below
CORE = [
    ("academic", "Where does the struggle start when work gets hard — starting, sticking, or checking?"),
    ("academic", "Compared to the class, where is {child} strongest and weakest in your subject?"),
    ("social", "Who is {child} choosing to work with, and does that match who they spend time with?"),
    ("behavior", "What does {child} do when they finish early — or when they're stuck?"),
    ("home-support", "What exactly should we do at home that would ACTUALLY help — subject, format, minutes?"),
]

STAGE_Q = {
    "K-2": [
        ("academic", "How is letter-sound progress / number sense tracking against benchmarks?"),
        ("academic", "Is {child} choosing to read/write when given free choice?"),
        ("social", "How are separations, transitions, and sharing going?"),
        ("behavior", "How does {child} respond to redirection?"),
    ],
    "3-5": [
        ("academic", "Is comprehension holding up on longer passages, or is decoding masking it?"),
        ("academic", "Where does math break down: facts, procedures, or word problems?"),
        ("social", "Is {child} inside the peer structure or orbiting it? Any conflicts repeating?"),
        ("behavior", "Homework-quality vs class-work quality — big gap?"),
    ],
    "6-8": [
        ("academic", "Which study habits from elementary are now insufficient?"),
        ("behavior", "How is the planner/binder/system — losing work, late work trends?"),
        ("social", "Any friendship shifts this year affecting class presence?"),
        ("home-support", "At this age, what HOME monitoring helps vs smothers?"),
    ],
    "9-12": [
        ("academic", "Realistically, which courses are trajectory risks for credits/graduation?"),
        ("academic", "What does this teacher's most successful student do differently?"),
        ("social", "Any friendship or social shifts this year affecting presence or performance in class?"),
        ("behavior", "Attendance/late-work patterns the school tracks?"),
        ("home-support", "What should parents STOP doing at this age?"),
    ],
}

SKIP_LIST = [
    "re-recapping portal grades you already read",
    "fundraiser/logistics questions (office knows)",
    "asking about other children (teachers can't discuss them)",
    "'is my child smart?' (unanswerable; ask learning behavior instead)",
]

JARGON = {
    "focused": ("needs to stay focused / focus", [
        ("Off-task with neighbors", "Focus during WHAT tasks — or all?"),
        ("Task too easy: finished and drifting", "What does {child} do when finished early?"),
        ("Task too hard: avoidance looks like distraction", "Which subjects does focus break down in?"),
        ("Attention pattern beyond typical range", "How does focus compare to the class range?"),
    ]),
    "below expected": ("working below expected standard", [
        ("Slightly behind benchmarks", "Which specific skills are the gap?"),
        ("Effort/completion gap, not ability", "Is it can't or won't — what's the evidence?"),
        ("Recent slide after earlier strength", "When did the change appear? What changed?"),
        ("Softened language for a larger gap", "What tier of support is already in place?"),
    ]),
    "disruptive": ("can be disruptive / needs redirection", [
        ("Calling out, not defiance", "What triggers it — boredom, excitement, confusion?"),
        ("Peer attention loop", "Is it the same peers each time?"),
        ("Transition difficulty", "Is it between activities or during work?"),
        ("Masking a skill gap", "What happens right BEFORE the disruption?"),
    ]),
    "potential": ("not working to potential", [
        ("Completion gap", "What % of work is actually turned in?"),
        ("Output volume vs quality", "Is quality fine but quantity low, or both?"),
        ("Motivation/engagement mismatch with the subject", "Where DOES {child} over-invest effort?"),
        ("Executive function (planning/starting), not laziness", "How does {child} start multi-step tasks in class?"),
    ]),
    "quiet": ("quiet / reserved", [
        ("Healthy introversion", "Does {child} have 1-2 solid connections?"),
        ("Uncertain participation, not shy", "Does {child} answer when asked directly?"),
        ("Flying under the radar", "Would you notice if {child} struggled?"),
        ("Withdrawal after a social event", "When did the quietness change, if it did?"),
    ]),
    "social skills": ("needs to work on social skills", [
        ("Conflict resolution, not friendlessness", "What happens in the typical conflict?"),
        ("Reading peer norms", "Are miss-steps with the same kids or everyone?"),
        ("Physical/verbal boundaries", "Is anyone's safety involved?"),
        ("Group-work role", "What role does {child} take in groups?"),
    ]),
    "bright": ("very bright / gifted", [
        ("Top of current class", "What extension is available beyond grade level?"),
        ("Fast finisher", "What's the plan for finished-early time?"),
        ("Strong verbal reasoning, weaker output", "Where is the gap between thinking and showing?"),
        ("Under-challenged → at-risk of coasting", "What would challenge look like here?"),
    ]),
}

def cmd_dossier(a):
    print(f"PRE-CONFERENCE DOSSIER — {a.child}, grade {a.grade}")
    print("=" * 48)
    print(f"Stage focus: {stage_of(a.grade)}")
    print(f"\nGRADES/REPORT DATA:\n  {a.grades or '(pull from portal before meeting)'}")
    if a.attendance:
        print(f"ATTENDANCE:\n  {a.attendance}")
    print(f"\nHOME OBSERVATIONS (yours):")
    for n in ([a.notes] if a.notes else []):
        print(f"  - {n}")
    print("\nWORK SAMPLES TO BRING: math (last 2), writing (last 2),")
    print("anything the child is proud of. Physical copies beat verbal description.")
    print("\nAUTO-FLAGGED QUESTION LEADS from your observations:")
    flags = []
    n = (a.notes or "").lower()
    if "hour" in n or " 2h" in n or "2 h" in n or "long" in n:
        flags.append("Homework time signal → ask: 'Is this volume typical for the class? "
                     "How long should this take?'")
    if "melt" in n or "cry" in n or "refus" in n:
        flags.append("Frustration signal → ask: 'What happens in class when {c} hits "
                     "frustrating work?'".format(c=a.child))
    if "read" in n:
        flags.append("Reading signal → ask: 'Decoding vs comprehension — where is the "
                     "actual level?'")
    if "math" in n:
        flags.append("Math signal → ask: 'Facts, procedures, or word problems — where "
                     "is the breakdown?'")
    if not flags:
        flags.append("(no auto-flags — add richer home observations for targeted leads)")
    for f in flags:
        print(f"  → {f}")
    print("\nNEXT: run `questions --grade {} --minutes {}` and pick 5-6.".format(a.grade, a.minutes))

def cmd_questions(a):
    stage = stage_of(a.grade)
    core = [(l, q.format(child=a.child)) for l, q in CORE]
    extra = [(l, q.format(child=a.child)) for l, q in STAGE_Q[stage.split()[0]]]
    pool = core + extra
    if a.lane:
        pool = [pq for pq in pool if pq[0] == a.lane]
    # time budget: ~2.5 min per question incl. teacher answer
    fit = max(3, int(a.minutes / 2.5))
    print(f"TOP QUESTIONS — grade {a.grade} [{stage}], {a.minutes} min "
          f"(pick ~{fit}):")
    for i, (lane, q) in enumerate(pool, 1):
        print(f" {i:2d}. [{lane}] {q}")
    if not a.lane:
        print("\nBalance lanes: 2 academic + 1-2 social + 1 behavior + 1 home-support.")
    print("\nSKIP (don't spend conference time on):")
    for s in SKIP_LIST:
        print(f"  - {s}")

def cmd_decode(a):
    low = a.phrase.lower()
    hit = None
    for key, (label, meanings) in JARGON.items():
        if key in low or a.phrase.lower() in label.lower():
            hit = (label, meanings)
            break
    if not hit:
        print(f"No exact entry for '{a.phrase}'.")
        print("Universal disambiguator: ask the teacher 'HELP ME PICTURE THAT —")
        print("what does it look like in class?' (turns any label into an episode).")
        print("\nClosest entries: " + ", ".join(sorted(v[0] for v in JARGON.values())))
        return
    label, meanings = hit
    print(f'"{label}" — common meanings:')
    for i, (m, ask) in enumerate(meanings, 1):
        print(f"  {i}. {m}")
        print(f"     ASK: {ask.format(child=a.child or 'they')}")

def cmd_plan(a):
    today = date.today()
    print(f"ACTION PLAN — {a.child} (conference {today.isoformat()})")
    print("=" * 48)
    print("\nWITHIN 24 HOURS:")
    print("  1. Write down agreements while fresh (this file).")
    print("  2. Send the follow-up email below — it makes commitments mutual.")
    print("\nWITHIN 1 WEEK:")
    for i, ag in enumerate(a.agreed, 1):
        print(f"  {i}. START: {ag}")
    if not a.agreed:
        print("  (no agreements passed — rerun with --agreed for each item)")
    print("  - Observe baseline: what does success look like in 2 weeks?")
    print(f"\nFOLLOW-UP TARGET: {a.followup_date or (today + timedelta(days=14)).isoformat()}"
          f" — check-in on whether the plan is working.")
    print(f"""
--- FOLLOW-UP EMAIL DRAFT ---
Subject: Thank you — {a.child}, follow-up on our conference

Dear [Teacher],

Thank you for the time today. To make sure I captured our conversation:

 - [agreement 1 — e.g., you'll send a weekly missing-work list]
 - [agreement 2 — e.g., we'll do 20-minute writing chunks at home]

We'll start on our side this week and check back around
{a.followup_date or (today + timedelta(days=14)).isoformat()}.

If I've misremembered anything, please correct me.

With appreciation,
[Your name]
""")
    print("Log this file in the child's conference folder — the year-over-year")
    print("record is what makes next conference's questions sharp.")

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("dossier")
    d.add_argument("--child", required=True)
    d.add_argument("--grade", type=int, required=True)
    d.add_argument("--grades", default=None)
    d.add_argument("--attendance", default=None)
    d.add_argument("--notes", default=None)
    d.add_argument("--minutes", type=int, default=15)
    d.set_defaults(fn=cmd_dossier)

    q = sub.add_parser("questions")
    q.add_argument("--grade", type=int, required=True)
    q.add_argument("--minutes", type=int, default=15)
    q.add_argument("--lane", choices=["academic", "social", "behavior", "home-support"])
    q.add_argument("--child", default="your child")
    q.set_defaults(fn=cmd_questions)

    dec = sub.add_parser("decode")
    dec.add_argument("--phrase", required=True)
    dec.add_argument("--child", default="your child")
    dec.set_defaults(fn=cmd_decode)

    pl = sub.add_parser("plan")
    pl.add_argument("--child", required=True)
    pl.add_argument("--agreed", action="append", default=[])
    pl.add_argument("--followup-date", default=None)
    pl.set_defaults(fn=cmd_plan)

    a = p.parse_args()
    a.fn(a)

if __name__ == "__main__":
    main()
