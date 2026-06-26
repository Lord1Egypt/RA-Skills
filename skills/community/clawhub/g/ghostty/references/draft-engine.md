# Draft Engine — How Ghostty Drafts in Your Voice

Ghostty's draft engine takes an incoming message and produces a reply that sounds like you. This document explains the methodology.

## The Drafting Algorithm

### Step 1 — Load Context

Before drafting, gather:
1. **Voice profile** — `ghostty/voice-profile.md` (non-negotiable)
2. **Per-person override** — `ghostty/per-person/{sender-name}.md` if exists
3. **Config** — `ghostty/config.md` (relationship to sender, ongoing projects)
4. **Conversation history** — last 3-5 messages in this thread
5. **Recency** — when was the last sent/received message?

### Step 2 — Classify the Message

Determine:
- **Intent**: question / request / update / acknowledgment / social / pitch / complaint / other
- **Tone needed**: warm / neutral / apologetic / assertive / celebratory
- **Length**: brief ack (1-2 sentences) / standard reply (3-5 sentences) / detailed response (full email)
- **Formality shift**: should this be more formal than usual? (e.g., first time contacting)

### Step 3 — Apply Voice Profile

From the voice profile, apply these constraints to the draft:

**Length matching:**
```
if my_avg_length == "short (1-2 sentences)":
    target_length = 1-3 sentences
elif my_avg_length == "medium (3-5 sentences)":
    target_length = 3-6 sentences
else:
    target_length = 5-8 sentences
```

**Sign-off selection:**
```
if formal_context: use my_professional_signoff
elif ongoing_thread: use my_casual_signoff or nothing
else: use my_default_signoff
```

**Tone enforcement:**
```
if confidence_score < 5: add hedging phrases I use (probably, I think, might)
if confidence_score >= 7: be direct, no filler
if warmth_score >= 7: add personal element (hope you're well, great to hear...)
if warmth_score < 4: drop pleasantries, get to the point
```

**Phrase injection:**
- Inject 1-2 of my pet phrases naturally into the draft
- If I never use "please" — don't add it just because it's polite
- If I always say "no worries" when apologizing — use that instead of "I apologize"

### Step 4 — Contextual Awareness

Good drafts reference ongoing context:

```
# Bad (generic AI):
"Thank you for your email. I will review the proposal and get back to you."

# Good (Ghostty, contextual):
"Thanks for sending over the Q4 proposal — I'll take a look through it this afternoon 
and ping you if I have any questions before our Tuesday call."
```

Add context by:
- Mentioning a shared project or prior discussion
- Referencing a specific time/date mentioned in prior messages
- Acknowledging continuity in an ongoing thread
- Being specific, not generic ("the deck" not "the document you sent")

### Step 5 — Self-Edit Check

Before finalizing, verify:
- [ ] Does this sound like ME, not AI? (read it aloud if unsure)
- [ ] Is the length appropriate for this context?
- [ ] Did I include my typical sign-off style?
- [ ] Are there 1-2 pet phrases or natural fillers I use?
- [ ] Is it specific, not generic?
- [ ] Would I actually send this?

If the draft fails the "would I actually send this" test, regenerate with different constraints.

## Response Templates by Intent

### Question → Direct Answer
```
[Open with acknowledgment if I typically do, e.g. "Hey, good question —"]
[Give the answer directly, matching my verbosity]
[Add follow-up if I typically do, e.g. "Let me know if that doesn't answer it"]
[Sign off in my style]
```

### Request → Acknowledgment + Action
```
[Confirm receipt in my style]
[State what I'll do / am doing]
[If delay: give realistic timeframe in my language]
[Sign off]
```

### Update → Acknowledgment + Reaction
```
[React in my style (enthusiastic / measured / brief)]
[If relevant: ask a follow-up question I would ask]
[End naturally]
```

### Apology Needed → Sincere + Fix
```
[Apologize in MY style (direct "sorry" vs. "my apologies" vs. "my mistake")]
[Explain briefly if appropriate (I usually do / don't over-explain)]
[State the fix/next step]
[Close without over-doing it]
```

### Social / Nudge → Light Touch
```
[Respond at my typical social energy level]
[If action needed: add light nudge without pressure]
[Keep it short if I typically keep social messages short]
```

## Draft Quality Anti-Patterns

AVOID these — they indicate generic AI voice, not you:
- "I hope this email finds you well"
- "Please do not hesitate to reach out"
- "I would be happy to assist"
- "As per our conversation"
- "Kindly note"
- "I trust you are well"
- Excessive exclamation marks (!!!)
- Starting with "Great question!" or "Thanks for reaching out!"
- Emoticons like 🙂 or 🙏 unless you actually use them
