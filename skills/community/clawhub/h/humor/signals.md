# Signal Detection — Reading Reactions Accurately

## Signal Strength Ladder

Not all positives are equal. Ordered from strongest to weakest:

1. **Callback** — user quotes your joke back later, this session or another. Highest possible signal: they stored it.
2. **Build** — user adds their own twist, extends the bit, or says "I'm stealing that."
3. **Strong laughter markers** — 😂 🤣 💀, "lmao", "I'm dying", "ok that was good."
4. **Scaled laughter** — "hahaha" > "haha" > "ha". Length correlates with intensity; a lone "ha" is acknowledgment, not delight.
5. **Frame-holding** — user stays playful, reply length and tempo hold or rise. Weakest positive; confirms tolerance, not enjoyment.

Escalation decisions (`feedback.md`) should rest on levels 1-3. Levels 4-5 justify holding, never raising. In group rooms, emoji reactions carry their own weighting (`groups.md`).

---

## Strong Positive

- 😂 🤣 💀 (skull = "I'm dead" = very funny)
- "lmao", "that's hilarious", "you're killing me", "good one"
- Callback or build (ladder levels 1-2)
- Energy increase: longer response, playful continuation

**Action:** log to Works (`~/Clawic/data/humor/profile.md`) with evidence. Reuse the *type*, never the same joke — repeating a hit on demand kills it.

---

## Mild Positive

- Single "ha" or "heh" — acknowledged, not overwhelmed
- 🙃 😏 — playful but measured
- Stays in the humorous frame, doesn't immediately pivot

**Action:** note it, hold current level. One mild positive is tolerance; it is not a request for more.

---

## Negative Signals

**Hard pivots:**
- "Anyway..." / "So about..." / "Moving on..." — topic escape
- Reply addresses only the substance, joke fully ignored
- "Okay but seriously" — direct request to stop

**Tone shifts:**
- Formal language immediately after your informal attempt
- Reply length drops sharply versus their recent messages
- "Actually..." — correction mode engaged

**Action:** log to Fails, run Failure Recovery (→ SKILL.md).

---

## Ambiguous Signals

- 🙂 alone — polite acknowledgment OR genuine amusement; undecidable without baseline
- "haha but seriously" — acknowledged then redirected; treat as mild negative
- Short "lol" with no further engagement — see the punctuation-lol distinction below
- Playful phrase + immediate topic change — mixed; the topic change wins

**Rule:** ambiguous = neutral. Don't escalate, don't retreat, don't change the profile.

---

## The Punctuation-"lol" Distinction

Two invisible cases that look identical:

- **"lol" as softener** — appended to the user's own statements ("that broke everything lol"). Says nothing about your joke. Frequency in their normal writing is the tell.
- **"lol" as reaction** — a standalone reply, or opening a reply, directed at your line. This one counts.

Only reaction-"lol" enters the log. A user who writes "lol" in most messages has a near-worthless "lol"; for them, look for ladder levels 1-3 only.

---

## User-Specific Calibration

Some users never emoji but "ha." IS their 😂. Some say "lol" reflexively with zero amusement. Absolute markers mislead; deltas don't.

**Calibration procedure:**
1. Baseline: how does this user react to your *non-humor* messages? (length, warmth, emoji rate)
2. Compare: is the post-joke reply warmer/longer than baseline, or colder/shorter?
3. Record the delta pattern in the Signals section of `~/Clawic/data/humor/profile.md`: "amusement looks like: [specific behaviors]."

Warmer than baseline = positive even if objectively flat. Colder than baseline = negative even if it contains a "haha".

---

## The Silence Problem

No reply, or a reply that skips the joke, is *usually* negative — but can be: user busy, user on mobile/voice, user thinking.

**Rule:** log silence as one mild negative, not a strong one. Two silences on the same type = treat as a real negative and demote. Never let a single silence retire a type.
