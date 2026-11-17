---
name: Listen
slug: listen
version: 1.0.3
description: >-
  Repairs garbled speech-to-text input: fixes mistranscribed names, numbers, and
  commands in voice-dictated messages. Use when a message arrived by voice and a
  word breaks the sentence, dictation mangles proper nouns, jargon, amounts, times,
  or email addresses, the user says "no, I said X" or repeats themselves, transcripts
  contain filler, spoken punctuation, or hallucinated sentences, the user dictates an
  email or document by voice, or an STT engine (Whisper or cloud speech) needs
  vocabulary tuning for recurring terms. Not for transcribing audio files or for
  typed-text typos.
homepage: https://clawic.com/skills/listen
changelog: "Display name shown correctly"
metadata:
  clawdbot:
    emoji: 👂
    os:
    - linux
    - darwin
    - win32
    displayName: Listen
    configPaths:
    - ~/Clawic/data/listen/
---

Voice input reaches the agent as text that already passed through a speech-to-text engine. Good engines hold 5-10% word error rate on clean conversational English, but the errors concentrate exactly where meaning lives: proper nouns, domain jargon, and numbers. This skill is the repair layer between the raw transcript and your response. Learned corrections and preferences persist in `~/Clawic/data/listen/` (see `setup.md` on first use, `lexicon.md` for the file formats). If you have data at an old location (`~/listen/` or `~/clawic/listen/`), move it to `~/Clawic/data/listen/`.

## When To Use

- A message arrived via voice and one token breaks the sentence ("deploy the communities cluster")
- The user repeats, rephrases, or says "no, I said X" after your response or action
- The same name, product, or term gets mangled across sessions and needs a persistent fix
- The user dictates an artifact by voice — an email, message, document, or note
- A voice command feeds an action with side effects (send, delete, book, pay) and a token looks off — repairs that change the target of such an action are always confirmed with the user before anything runs (Rule 1)
- A transcript arrives noisy, truncated, mixed-language, or padded with hallucinated sentences
- An STT engine needs vocabulary tuning for a user's recurring domain terms
- Not for transcribing audio files (that is batch transcription work) and not for typed-text typos: keyboard errors are adjacency-based, so phonetic repair misfires on them

## Quick Reference

| Transcript signal | Likely cause | Play |
|---|---|---|
| Common word breaks the sentence's domain | Proper noun replaced by frequent vocabulary | Phonetic match against lexicon, then session context (`repair.md`) |
| Number gates an action (amount, count, time) | -teen/-ty confusion (13/30 ... 19/90) | Echo the number as digits in your reply; confirm before irreversible acts (`numbers.md`) |
| "at", "dot", "dash", "underscore" around a name | Spoken email address or URL | Reassemble as an address and echo it back (`numbers.md`) |
| User re-sends a nearly identical sentence | Your previous reading was wrong | Diff the two versions; the changed token is the correction; log the pair |
| "period", "comma", "new line" mid-text | Spoken punctuation | Dictating an artifact: treat as command. Conversing: treat as literal word (`dictation.md`) |
| "scratch that", "no wait", "I mean" mid-dictation | Spoken self-correction | Apply the rewrite; keep only the final version (`dictation.md`) |
| Two words that read as one, or one as two | Segmentation error ("a track" / "attack") | Re-split at syllable boundaries before declaring the token unknown (`repair.md`) |
| Word fits grammar but not intent ("sine the contract") | Homophone substitution | Homophones pass grammar checks, so test against intent, not syntax (`repair.md`) |
| Fluent sentence unrelated to the conversation ("Thanks for watching!") | Engine hallucination on silence or noise | Drop it entirely; never interpret it (`degraded.md`) |
| Same phrase repeated 3+ times in a row | Decoder loop, not the user | Keep one instance, drop the rest (`degraded.md`) |
| Message ends mid-clause | Truncated audio | Ask for the tail only, never re-dictation (`degraded.md`) |
| Two languages in one message, or a known non-English speaker arrives in English | Code-switching or auto-detect flip | `multilingual.md` |
| "um", "uh", "you know" littering the text | Engine transcribed disfluencies | Strip before interpreting; never quote them back to the user |
| 3+ suspect tokens in one message | Mic or noise problem, not a lexical error | Stop piecewise repair; quote your full interpretation back for a yes/no |
| Same term mangled across 5+ sessions | Engine vocabulary gap | Fix upstream with vocabulary biasing (`tuning.md`) |
| Anything else: transcript reads clean | No error | Respond normally; never mention transcription at all |

Depth on demand: `repair.md` candidate generation and phonetic matching · `numbers.md` digits, times, money, spoken addresses · `names.md` proper nouns, casing, code identifiers · `dictation.md` producing dictated artifacts · `actions.md` side-effect confirmation ladder · `degraded.md` noise, hallucinations, truncation · `multilingual.md` code-switching and accents · `tuning.md` upstream engine fixes · `lexicon.md` correction persistence · `setup.md` first-use preferences.

## Core Rules

1. **Repair without confirmation when only understanding changes; confirm when the repair changes an action target.** Check: would acting on raw vs repaired text produce different side effects (recipient, amount, file path, send/delete)? Different side effects = confirm first. Same outcome = fix without asking and move on. Full ladder in `actions.md`.
2. **Confirm with a candidate, never an open question.** "Did you mean Kubernetes?" costs the user one word; "What did you say?" forces full re-dictation. Offer 1 candidate; 2 only when both fit equally; never 3.
3. **Two-strike promotion.** First observed fix = candidate: apply it but surface it ("...on Kubernetes, got it"). Same fix observed a second time = confirmed: apply from then on without surfacing it. One user rejection at any stage = move the pair to the Never list.
4. **Repair needs two independent signals: phonetic closeness AND context fit.** Phonetic test: fold confusable consonants (B/P, D/T, C/K/Q — full class table in `repair.md`), strip vowels, collapse doubles, then compare skeletons. "web look" → WPLK vs "webhook" → WPHK is skeleton edit distance 1 (one substitution, L/H); distance ≤2 = neighbor. Context test: the candidate must be a term already in this user's domain (lexicon, recent files, session topic). Either signal alone is a guess, not a repair.
5. **Correction direction is common-word → proper-noun, almost never the reverse.** STT engines are biased toward frequent vocabulary, so a rare word that survived transcription was almost certainly spoken. Never "fix" an odd-looking codename into a dictionary word.
6. **Echo digits for any number that gates an action.** "Booked for 15 (one five) at 8pm." The seven -teen/-ty pairs are the highest-frequency STT number confusion (`numbers.md`), and a wrong booking count costs more than three extra characters in every reply.
7. **A fluent sentence that ignores the conversation is the engine, not the user.** Whisper-family models emit caption boilerplate ("Thank you.", "Thanks for watching!") on silence or noise-only audio. Drop it; interpreting it as user intent invents a request nobody made. Signatures in `degraded.md`.
8. **3+ suspect tokens = stop repairing tokens.** Piecewise repair of a noise-storm transcript compounds guesses into a sentence the user never said. Quote your full best-effort reading back for a single yes/no instead.

## Repair Procedure

1. Flag the suspect token: it breaks domain, register, or grammar of the surrounding sentence.
2. Generate candidates in priority order: (a) lexicon entries whose wrong-side matches, (b) phonetic neighbors (Rule 4 skeleton test) drawn from session vocabulary, open files, and recent topics, (c) re-segmentation splits/joins.
3. Score by context fit; discard any candidate failing the two-signal test of Rule 4.
4. Route by Rule 1: side effects → confirm with the top candidate; understanding only → substitute without confirmation.
5. After user confirmation or correction, append the pair to the lexicon (`lexicon.md`).

Worked candidate generation, sound-class folding, segmentation repair, and the homophone catalog: `repair.md`.

## Correction Lexicon

One line per pair in `~/Clawic/data/listen/lexicon.md`:

```
wrong → right | status: candidate|confirmed|never | last seen: YYYY-MM-DD
web look → webhook | confirmed | 2026-07-23
```

- Load the lexicon before interpreting any voice message; apply `confirmed` entries pre-emptively.
- `never` entries are false positives (slang, codenames the user actually says); check them before flagging any token.
- Lifecycle, pruning thresholds, and the config file format: `lexicon.md`.

## Output Gates

Before replying to any voice-sourced message, check:

- Did any repaired token feed an action with side effects? If yes, was it confirmed or lexicon-`confirmed`?
- Is every action-gating number echoed as digits somewhere in my reply?
- Am I mentioning transcription or mishearing anywhere except inside a confirmation question?
- Did this exchange produce a new wrong → right pair, and is it written to the lexicon?
- If I produced a dictated artifact: are self-corrections applied, filler handled per `dictation_mode`, and uncertain tokens marked?
- Did I drop (not interpret) any hallucinated or looped text?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/listen/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| dictation_mode | cleaned \| verbatim | cleaned | `dictation.md`: cleaned strips filler and applies spoken self-corrections; verbatim preserves every word including disfluencies |
| number_echo | actions-only \| always \| never | actions-only | When Rule 6 digit-echoing fires: only for numbers gating actions, for every number, or never (user finds echoes noisy) |
| confirmation_posture | standard \| strict | standard | strict: confirm every repair that feeds an action, even lexicon-`confirmed` ones; standard follows Rule 1 |
| languages | list (BCP-47 codes) | [en] | Languages the user speaks; gates code-switch handling in `multilingual.md` and language-pinning advice in `tuning.md` |
| lexicon_ttl_days | number (30-365) | 90 | Days without a sighting before a lexicon entry is pruned (`lexicon.md`) |

Preference areas to record as the user reveals them:

- **vocabulary domain** — the user's field (dev, medical, legal, finance); seeds candidate scoring in `repair.md` and biasing terms in `tuning.md`
- **artifact formatting** — punctuation habits, paragraphing, sign-offs for dictated emails and documents; affects `dictation.md` output
- **engine and tooling** — which STT engine, model, and capture setup the user runs; targets the advice in `tuning.md`
- **channel mix** — voice-only vs mixed typing-and-voice sessions; affects which messages get repair at all (typed input is never phonetically repaired)
- **spelling conventions** — NATO vs plain letters when confirming spellings, diacritics handling for names; affects `names.md` confirmations

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| "Fixing" slang or project codenames | Codenames are deliberately odd; one wrong rewrite teaches the user the agent edits their words | Require both Rule 4 signals; maintain the Never list |
| Asking "what did you say?" | Forces full re-dictation, often while the user is hands-busy, which is why they used voice | Yes/no question with your best candidate |
| Repairing inside dictated artifacts (emails, docs) without marking it | Dictated content is the user's own voice; unmarked edits change what they said | Produce the artifact with repairs applied but uncertain tokens marked for review (`dictation.md`) |
| Keeping corrections only in conversation memory | Lost at session end; the user re-teaches the same name weekly | Persist every pair to `~/Clawic/data/listen/lexicon.md` immediately |
| Applying phonetic repair to typed input | Typing errors follow keyboard adjacency, not sound; phonetic candidates are noise there | Gate this skill on voice-sourced input only |
| Narrating every fix ("your STT said X, I read Y") | Makes the voice channel feel broken and erodes trust in silent repairs | Rule 1 routing: silent when understanding-only, one short confirmation otherwise |
| Promoting a pair to confirmed after one sighting | A single fix may be context-specific; auto-applying it rewrites future valid words | Two-strike promotion (Rule 3); demote on first rejection |
| "Improving" the user's grammar or word choice while repairing | Non-native phrasing and casual register are the speaker, not the engine | Repair only tokens the engine plausibly garbled; leave style alone |
| Interpreting a hallucinated closing line as a request | "Thank you, goodbye" from silence reads like the user ending the task | Rule 7: drop boilerplate that ignores the conversation |

## Where Experts Disagree

- **Silent vs surfaced repair.** Transparency school surfaces every fix; fluency school hides all of them. The working boundary: surface while a pair is `candidate`, go silent once `confirmed`, and always confirm when side effects ride on the repair (Rules 1 and 3). Full transparency is available on request — the lexicon is a readable file.
- **Cleaned vs verbatim dictation.** Smart-dictation products clean filler and apply self-corrections; court-reporter style keeps every word. Default cleaned; verbatim when the user asks for exact words or the artifact is quoted testimony. `dictation_mode` records the user's side.
- **Fix upstream vs repair downstream.** Engine vocabulary biasing kills recurring errors at the source but over-biasing makes the engine hallucinate the boosted terms into unrelated audio. Boundary: 5+ recurring terms justify upstream tuning (`tuning.md`); one-off errors stay downstream in the repair layer.

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/listen (install if the user confirms):

- `speech-to-text-transcription` — batch transcription of audio and video files with timestamps and speakers
- `voice-notes` — organizing accumulated voice transcripts into a searchable knowledge base
- `talk` — setting up the real-time voice conversation channel this skill repairs
- `audio` — cleaning noisy recordings before they ever reach the STT engine

## Feedback

- If useful, star it: https://clawic.com/skills/listen
- Latest version: https://clawic.com/skills/listen

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/listen.
