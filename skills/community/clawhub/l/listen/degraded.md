# Degraded — Noise, Hallucinations, and Truncation

Token repair assumes a mostly-good transcript with local damage. This file covers the other regimes: transcripts the engine invented, lost, or shredded. The gate: 3+ suspect tokens in one message = stop token repair (SKILL.md Rule 8) and work at message level.

## Hallucination Signatures

Whisper-family models are trained on captioned web video; fed silence or noise, they emit training-set boilerplate instead of nothing. Recognize and drop — never interpret:

| Signature | Example | Cause |
|---|---|---|
| Caption boilerplate | "Thanks for watching!", "Please subscribe", "Thank you." | Silence or music-only segment |
| Complete fluent sentence ignoring the conversation | A weather remark mid-code-review | Noise decoded as speech |
| Sudden wrong language, fluent | A Portuguese sentence from an English speaker | Noise + language auto-detect drift (`multilingual.md`) |
| Repetition loop | same phrase 3+ times consecutively | Decoder loop — keep one instance, drop the rest |
| Trailing sign-off nobody said | "Thank you, goodbye." appended to a task | Trailing-silence hallucination |

The danger case is a hallucination shaped like a request. A polite closing after a task list reads like "we're done" — acting on it abandons the user's task. Boilerplate that ignores conversational state is the engine (SKILL.md Rule 7); when a fluent-but-off sentence could genuinely be the user, ask about that sentence alone, not the whole message.

## Truncation

- Message ends mid-clause ("and then delete the") — the audio was cut (push-to-talk released early, VAD timeout, network drop). Ask for the tail only: "You cut off after 'delete the' — which one?" Never ask for full re-dictation and never guess the missing object (`actions.md`).
- Message STARTS mid-clause — leading truncation, usually capture starting late. Same play, mirrored: confirm what the head was.
- Suspiciously short transcript for a long pause the user took: parts are missing silently. If the message is coherent but oddly minimal for the effort, say what you got and let the user fill the gap.

## Crosstalk and Multiple Speakers

- Mid-message register + topic shift ("...deploy the fix okay honey five minutes the migration script...") — a second conversation bled in. Excise the foreign span by topic continuity; if the remainder is coherent, proceed on it and note the excision only if meaning is at risk.
- A reply-shaped fragment with no addressee is likely room conversation, not input (`actions.md` "not addressed to you").

## Noise Storm

3+ suspect tokens, message level:

1. Build your single best-effort reading of the whole message.
2. Quote it back for one yes/no: "I got: 'restart the staging cluster after the backup finishes' — right?"
3. On no: ask which part is wrong, not for re-dictation — the user corrects one span.
4. Do not log lexicon pairs from a noise-storm message: the errors are acoustic, not lexical, and stored pairs from them poison future repairs.

## Systematic Degradation

- Quality drops across ALL vocabulary and several consecutive messages → the input chain changed (mic, room, headset battery), not the engine's lexicon. Ask about the setup once ("Did your mic change? Everything is arriving garbled") instead of repairing forever.
- Persistent degradation with a known-good setup → engine-side: model, sample rate, chunking (`tuning.md`).
- One user habit worth knowing: degraded messages cluster at session start (headset connecting, wrong input device selected). A garbled first message followed by a clean second needs no setup conversation.

## When to Declare Unrepairable

If after one yes/no round the message still has no coherent reading: state plainly what you could and could not recover ("I got the part about the invoice; the amount and the name didn't come through") and ask for just those fields — typed if they gate money or authentication. Faking certainty on an unrecoverable transcript is the one unforgivable failure mode of this skill.
