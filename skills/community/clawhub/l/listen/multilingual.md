# Multilingual — Code-Switching, Accents, and Wrong-Language Transcripts

Multilingual users hit a distinct error class: the engine mishandles the language boundary itself. Gate on the `languages` config list — a monolingual profile makes most of this file inapplicable and its repairs harmful.

## Code-Switching

- Engines pinned to one language render embedded foreign phrases as phonetically similar nonsense in the pinned language ("déjà vu" → "day sha voo", "por favor" → "poor fav or"). Restore the foreign phrase verbatim when it is skeleton-close to a phrase in another `languages` entry.
- Auto-detect engines do the opposite failure: they flip language mid-message and shred BOTH sides. The fix is upstream — pin the primary language and handle embeds downstream (`tuning.md` holds the pinning guidance).
- Embedded proper nouns are the common case (Spanish name in an English sentence): "Juan" → "one", "Jorge" → "whore hey". Candidate pool: contacts and lexicon, same two-signal bar as any name (`names.md`).

## Whole-Message Wrong Language

- User's known language arrives as fluent English → the engine translated instead of transcribing (Whisper's translate task, or a product "helpfully" translating). This is an upstream misconfiguration, not a repair job: flag it once and point to `tuning.md`. Meanwhile, treat content as approximate — translation adds paraphrase on top of transcription error.
- A single fluent sentence in an unexpected language inside a clean message is usually a noise hallucination, not code-switching (`degraded.md`).

## Accent-Driven Substitution Patterns

Non-native accents shift errors systematically. When `languages` reveals the user's other languages, expect the matching pattern and widen the skeleton test accordingly:

| L1 background | Systematic confusion | Example miss |
|---|---|---|
| Spanish/Italian | b/v, added leading e- before s-clusters | "estate" for "state" |
| German/Dutch | w/v, final-consonant devoicing (d→t) | "vent" for "went" |
| French | h-dropping, th→z/s | "zis" fragments, "air" for "hair" |
| Japanese/Korean | r/l | "erection" for "election" — high-embarrassment class, repair silently |
| Mandarin/Cantonese | final consonant loss, th→s/f | "pass" for "path" |
| Arabic | p/b | "barking" for "parking" |
| Hindi/Urdu | v/w, t/d retroflex | "wery" fragments |

These are widened candidate signals, not stereotypes to apply blindly: the context test still decides, and a pattern only activates after it has actually been observed for this user (log it as a lexicon Pattern line, `lexicon.md`).

## What Not to Fix

- Non-native grammar (dropped articles, tense slips) is the speaker, not the engine. In conversation, just understand it. In dictated artifacts: cleaned mode fixes transcription, not language — grammar edits only if the user asked for them explicitly (that request is worth a config note under artifact formatting).
- Formality registers (tu/usted-shaped phrasing carried into English) are voice, not error.

## Diacritics and Script

- Restore diacritics per the rule in `names.md`: only for established canonical forms.
- Cross-script names (Cyrillic, Arabic, CJK users dictating in English) arrive romanized inconsistently; the user's chosen romanization, once seen in writing, goes to the lexicon as the canonical right side.

## Lexicon Entries for Multilingual Pairs

Tag language on pairs that only apply in one language context: `one → Juan (es name) | confirmed | <date>`. An untagged pair applies everywhere — which is wrong for "one", a word the user will legitimately say daily. Language-tagged entries fire only when the sentence context matches.
