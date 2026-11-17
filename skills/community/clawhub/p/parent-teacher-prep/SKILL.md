---
name: parent-teacher-prep
description: "Use before any parent-teacher conference or school progress meeting (K-12) — builds your child's pre-conference dossier (grades, attendance, work samples, your observations at home), generates an age-tuned question bank (academic, social, classroom behavior, support-at-home) so the 15 minutes actually surface what report cards don't, decodes teacher jargon ('working below expected standard', 'needs to stay focused') into plain language with what-it-may-mean and follow-ups, and produces a disciplined 24h/1week action plan with a follow-up email draft thanking and confirming agreements."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [parenting, school, education, communication, meetings]
---

# Parent-Teacher Conference Prep

## Overview
Conferences are 10-20 minutes, twice a year, with a teacher who sees
your child 30 hours a week in ways you never will. Parents walk out of
most conferences with two adjectives ("she's a pleasure") and zero
actionable information — not because teachers withhold, but because
unprompted, general questions get general answers.

This skill makes the 15 minutes count:

1. **dossier** — structured pre-conference evidence file: what you
   already know (grades, attendance, work samples, homework battles at
   home), so questions target gaps, not recaps.
2. **questions** — age-tuned question bank across four lanes:
   academics, social, classroom behavior, home-support. Ranked by
   information yield; fits the real time budget.
3. **decode** — teacher-speak → plain English. "Needs to stay focused"
   may mean anything from boredom to ADHD-adjacent attention patterns
   to seating; the decoder lists what it can mean and the exact
   follow-up question that disambiguates.
4. **plan** — conference notes → 24h/1-week action plan + follow-up
   email draft that confirms agreements in writing (the step everyone
   skips, which is why agreements evaporate).

Pure stdlib, offline.

## When to Use
- Any scheduled parent-teacher conference or progress meeting (K-12)
- Mid-year check-ins, IEP/504-type support meetings (prep layer only)
- "The teacher wrote X on the report card — what does that actually mean?"
- After a concerning grade report and you're requesting a meeting
- Building a year-over-year conference log per child

**Don't use for:** formal dispute/advocacy with a school district
(that's special-education advocacy territory), or diagnosing any
condition — this organizes questions, teachers and specialists
evaluate.

## How It Works — Numbered Steps
1. Build the dossier a few days before:
   ```
   python3 scripts/conference_prep.py dossier --child "Mia" --grade 4 \
       --grades "math B-, reading A, science B" \
       --notes "homework takes 2h, melts down on writing tasks"
   ```
   → prints the evidence file + auto-flagged question leads from your
   own observations (the 2h-homework flag generates time-allocation
   and task-breakdown questions).
2. Pick questions for the real time budget and the child's stage:
   ```
   python3 scripts/conference_prep.py questions --grade 4 --minutes 15
   python3 scripts/conference_prep.py questions --grade 9 --minutes 10 --lane social
   ```
   → top questions ranked; skip-list marks what NOT to spend time on.
3. After the meeting (or on the report card), decode the phrases:
   ```
   python3 scripts/conference_prep.py decode --phrase "needs to stay focused"
   python3 scripts/conference_prep.py decode --phrase "working below expected standard"
   ```
4. Convert notes into commitments:
   ```
   python3 scripts/conference_prep.py plan --child "Mia" \
       --agreed "teacher sends weekly missing-work list" \
       --agreed "we try 20-min writing chunks at home" \
       --followup-date 2026-11-14
   ```
   → 24h/1-week plan + follow-up email draft.

## Question Lanes and Why
| Lane | What it surfaces that report cards don't |
|---|---|
| academic | Actual mastery vs grade inflation; where breakdown happens (retrieval? speed? concepts?) |
| social | Peer dynamics, isolation, who they sit with — strongest predictor axis teachers see and parents don't |
| behavior | Attention patterns BY TIME OF DAY, task completion, response to correction |
| home-support | Exactly what help at home helps: subjects, format, cadence — teachers know what transfers |

Stage tuning: K-2 questions probe early-literacy/numeracy mechanics and
separation/social basics; 3-5 probe work habits solidifying and peer
structures; 6-8 probe organization systems and academic identity;
9-12 probe transcripts, credit trajectories, and teacher-specific
strategies.

## Common Pitfalls
1. **Leading with "how is she doing?"** — invites the two-adjective
   answer. Lead with specific: "Where does she struggle first when
   work gets hard?"
2. **Defending the child.** You're there to collect information, not
   contest it. If a claim seems off: "help me understand what that
   looks like in class."
3. **Spending the slot on grade recaps** you already read in the
   portal. Skip-list exists for this.
4. **No written follow-up.** Verbal agreements with busy teachers
   evaporate; a 5-line confirmation email makes commitments mutual.
5. **Asking "is he smart?"** — unanswerable and useless. Ask "what
   does he do when he doesn't know the answer?" (learning behavior
   beats ability labels).
6. **Ignoring the social lane entirely.** For many kids the conference
   gold is here: friendships, conflicts, recess map.
7. **Treating one teacher's frame as the whole child.** Note who said
   what; specialists (PE, music) see different repertoires.
8. **Never asking the growth question:** "What will be different by
   March if our home plan works?" — defines measurable success.

## Example
```
$ conference_prep.py questions --grade 4 --minutes 15
TOP QUESTIONS (grade 4, 15 min — pick 5-6):
 1. [academic] Where does she struggle FIRST when work gets hard —
    starting, sticking, or checking?
 2. [academic] Reading: is she decoding fine but comprehension
    dropping on longer passages?
 3. [social] Who does she choose to work with? Does that match who
    she plays with?
 ...
 SKIP (don't spend conference time):
  - portal grades recap, fundraiser logistics, other kids' business

$ conference_prep.py decode --phrase "needs to stay focused"
"needs to stay focused" — common meanings:
  1. Off-task with neighbors → ask: "Focus during WHAT tasks — or all?"
  2. Task too easy (finished, drifting) → ask: "What does he do when
     he finishes early?"
  3. Task too hard (avoidance looks like distraction) → ask: "Which
     subjects does focus break down in?"
  4. Attention pattern beyond typical → ask: "How does his focus
     compare to the class range?"
```

## Verification Checklist
- [ ] Dossier built before meeting; own observations listed
- [ ] 5-6 lane-balanced questions chosen for the time budget
- [ ] Notes taken IN the meeting (phrases verbatim for decode)
- [ ] Agreements converted to a written plan within 24h
- [ ] Follow-up email sent (thanks + confirmations)
- [ ] Log appended to the child's year file for the next conference
