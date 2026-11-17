> **Bilingual — 中英文皆可适配**  This skill ships both Chinese and English content. The Chinese counterpart of this file is `onboarding.zh.md`.

# Progressive Proactive Onboarding — Design Notes

> Ontology Agent gives the "digital company" an onboarding process: **it does not wait for the user to recall what to disclose; instead the digital company guides the user step by step to complete the enterprise data.** The user does not need to know what to provide — the digital company itself knows what is still missing and asks for only a little at a time.

## 1. Design principles (why it works this way)

1. **The digital company owns the guidance**: the user only needs to say "I am company X" to get started; the rest is proactively collected by the digital company in priority order, rather than dumping a big form into the user's head.
2. **Progressive, 1–2 items at a time**: each round asks only the 1–2 highest-priority gaps, avoiding a one-shot barrage that causes annoyance.
3. **Explain the purpose + reassure on security**: every question comes with "why this is needed" and a "data safety note", lowering security concerns.
4. **Skippable**: the user can say "skip / later" at any time; real tasks are never blocked.
5. **Does not interrupt the main work**: when the user has a concrete request, handle that first; onboarding is woven in at task wrap-up or natural pauses.

## 2. Priority tiers (fill the highest-impact first)

- **P0 (sets the tone of all advice)**: full company name / enterprise type / region / industry / size; owner's form of address / decision style / risk appetite / communication tone.
- **P1 (core facts)**: legal form / Unified Social Credit Code / core workflow / delegation boundary; company stage / core product / customer types.
- **P2 (context and interfaces)**: owner's professional background / value priorities; mission & vision / brand voice; current-quarter goal / systems in use / taboos.
- **P3 (continuous collection)**: gaps exposed during task execution (e.g. wanting to do something but missing some data) — asked and filled on the spot.

## 3. Cadence

- New users' first 2–3 sessions: lay down only P0, so the user can "start using it" first.
- Each session after that: fill at most 1–2 P1/P2 items, with an occasional progress note (e.g. "60% complete, a few pieces left").
- Task-triggered: when doing any concrete task, if data is missing, ask only about that one item, then continue after it is answered.

## 4. How the principal uses it (runtime)

At session start, the business principal reads `instance.yaml` + `company-memory.md`, then calls the onboarding engine:

```bash
# See progress
python scripts/onboarding.py --instance <company>/instance.yaml --report
# Get the next questions to ask (1–2 at a time)
python scripts/onboarding.py --instance <company>/instance.yaml --next --limit 2
```

Take the questions output by `--next`, ask them in natural language with purpose and safety notes, **one at a time**;
after the user answers, write back the corresponding fields in instance (keeping the YAML valid), and repeat until coverage = 100%.

## 5. Example phrasing (gentle, with a reason, with safety)

- "Shunran, let's settle 'how would you like me to address you' first? That way all your AI employees will use the form of address you prefer. This lives only in your local instance, never leaves your domain, and you can change it any time."
- "One more small point: when you decide, do you lean more on data or on intuition? This determines whether I lead with data or go straight to the conclusion when giving advice. No sensitive information involved; it stays local."
- "Your company profile is about 60% complete, with a few pieces still missing (for example this quarter's goal and the systems you use). No rush — tell me whatever comes to mind and I'll note it down gradually."
