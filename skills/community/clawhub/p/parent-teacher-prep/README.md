# Parent-Teacher Conference Prep

**Fifteen minutes, twice a year. Make them count.** Parents walk out
of most conferences with two adjectives and zero actionable
information. Not because teachers withhold — because "how is she
doing?" gets a general answer, and the slot evaporates on grade
recaps you already read in the portal.

This toolkit gives you:

- **Pre-conference dossier builder** — grades, attendance, work
  samples, dated home observations, with auto-flagged question leads
  (a "2 hours of homework" note generates the exact time-allocation
  questions to ask).
- **Age-tuned question bank** — K-2 through 9-12, across four lanes
  (academic / social / behavior / home-support), sized to your real
  minutes, with an explicit SKIP list.
- **Teacher-jargon decoder** — "needs to stay focused", "working below
  expected standard", "not working to potential" → plain-language
  meanings + the disambiguating question for each.
- **Action plan + follow-up email** — agreements → 24h/1-week plan →
  a 5-line confirmation email that makes commitments mutual.

## The real-world problem
Roughly 50+ million school-age children in the US alone; the
parent-teacher conference is the single scheduled information transfer
between the 30 hours/week the teacher sees and the evenings you see.
Unstructured, it yields pleasantries; structured, it surfaces the
recess-map, the task-completion patterns, and the exact home help
that transfers.

## Quick start
```bash
python3 scripts/conference_prep.py dossier --child "Mia" --grade 4 \
    --grades "math B-, reading A" --notes "homework takes 2h, melts down on writing"
python3 scripts/conference_prep.py questions --grade 4 --minutes 15
python3 scripts/conference_prep.py decode --phrase "needs to stay focused"
python3 scripts/conference_prep.py plan --child "Mia" \
    --agreed "teacher sends weekly missing-work list" --followup-date 2026-11-14
```

Pure Python stdlib. Offline. Nothing about your child leaves the
machine.

## License
MIT © Denis Voronin
