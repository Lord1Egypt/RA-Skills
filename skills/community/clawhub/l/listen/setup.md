# Setup — Listen

Read this on first use to load user preferences. Do not interview the user.

## Your Attitude

Voice users chose the channel because their hands or eyes are busy. Every repair either saves them a re-dictation or silently gets it right; every unnecessary question spends the convenience they came for. Be invisible when the transcript is clean, surgical when it is not.

## How To Load Preferences

1. Read `~/Clawic/data/listen/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults in the Configuration table of `SKILL.md` — do not ask.
   - `dictation_mode: cleaned`, `number_echo: actions-only`, `confirmation_posture: standard`, `languages: [en]`, `lexicon_ttl_days: 90`.
3. Read `~/Clawic/data/listen/lexicon.md` for stored pairs, patterns, and the Never list (`lexicon.md` for format and application order). Absence is fine; proceed without comment and create it at the first logged pair.

Work from defaults immediately. Never open with questions about languages, engines, or how much to confirm.

## Recording Preferences (only when the user declares one)

Write to config **only** when the user states a preference in the course of the work — never as a preflight questionnaire.

- User names their dictation style, echo tolerance, confirmation appetite, or languages → update the matching key in `~/Clawic/data/listen/config.yaml`.
- User reveals their field, artifact formatting habits, STT engine, channel mix, or spelling convention → record it under the relevant preference area (SKILL.md Configuration) as a config comment or key.
- User corrects earlier behavior ("stop echoing numbers") → update the stored value so you don't repeat it.

If the user has said nothing, store nothing.

## What the Lexicon Holds

Observed corrections, not declared preferences — the two never mix (`lexicon.md`). Correction pairs and Never-list entries accumulate from real exchanges only; an observation never overwrites a declared preference without confirmation.
