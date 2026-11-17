# Mood Inference

This is the only field in the snapshot that is genuinely *inferred*. Get it
right or leave it empty. A fabricated mood is worse than `quiet (low signal)`,
because the agent makes decisions about how to talk to the owner based on it.

## The one rule that matters most

**Mood is read from how the owner interacted and what outcomes landed. It is
NEVER read from the calendar.**

A reservation, a meeting, a flight on the calendar tells you the *schedule*, not
the *feeling*. The historical failure of this skill was laundering calendar
events into emotions ("tea reservation" → "anticipation for tea";
"dinner booked" → "content"). Stop. Those are events; they belong in the day
bullets, not in mood. Mood evidence comes from two signal categories only:

1. **INTERACTION tone** — how the owner is communicating *now*, across every
   conversational channel the setup exposes: agent sessions, and any enabled
   personal messaging (iMessage, Slack, WhatsApp, Signal, SMS, Discord), and the
   texture of email threads. Read pacing and affective TONE (frustration, playfulness, warmth, terseness, urgency). The discussed subject is a FOCUS signal, never a mood (see Topic != Mood below).
   frustration, playfulness, repetition, what the owner kept returning to. The
   owner's tone with *people* is often a richer mood signal than tone with the
   agent — weight it accordingly.
2. **OUTCOME weight** — discrete results that landed, on *any* channel: a rejection,
   an offer, a confirmation, a cancellation, a bill, a deadline. Outcomes carry
   emotional weight; scheduled events do not.

The STANDING category (a memory search or context engine) supplies *standing
context* that colors interpretation (a known job transition, a recent loss,
ongoing travel) but is not itself same-day mood evidence. Use it to interpret
signals, not to manufacture them. If INTERACTION or OUTCOME has no source, mood
relies on whichever remains; if both are absent, mood is `quiet (low signal)`.

## Topic != Mood (the leak trap)

The most common way this skill still fabricates mood is converting a *discussed
subject* into a *felt emotion*. A session or message ABOUT a leak, conflict,
deadline, or health scare does NOT mean the owner FEELS a corresponding emotion.
The topic is content; mood is affect.

- "The owner kept returning to X" is a PRIORITY/FOCUS signal, not a mood. It says
  what they are working on, not how they feel.
- Only register a mood dimension when AFFECTIVE TONE shows it (the session reads
  frustrated, anxious, energized) or an OUTCOME resolved (a rejection landed). A
  neutral-toned session about a serious topic yields NO mood dimension from that
  topic.
- If the only signal is "the owner discussed X," the correct mood is
  `quiet (low signal)` -- not "concerned about X."


**Across channels:** read every source in a category, do not stop at the first.
**Dedup:** the same outcome on email and a text is one signal, not two — counting
it twice falsely inflates a dimension. **Privacy:** cite evidence by channel, never
by quoting it — `frustrated about a delayed contractor (messages)`, never the
message text. USER.md is read in every session; treat it as broadly visible.

## Output shape

```
**Mood:** [label] about [topic], [label2] about [topic2]
```

- 1 to 3 dimensions, strongest first, **each backed by a concrete signal**.
- Contradictions are valid and valuable: `dejected about job search, excited about Honolulu trip` can both be true in one week. Preserve them; do not average them into "mixed."
- No hedging words ("seems", "might"). State the observed signal plainly.
- If you cannot point to a concrete signal for a dimension, the dimension does not exist.
- Thin or no signal → `quiet (low signal)`. This is a correct, common answer. It is not a failure.

(Note: this supersedes any older "one word only" instruction. Mood is 1-3
evidence-backed dimensions, never collapsed to a single mandated word.)

## The Signal Ledger (do this before writing mood)

Before composing the mood line, write an internal ledger — one line per signal,
tagged `[category/channel]`. You are not allowed to assert a mood dimension that
does not trace to a ledger line. Example (a setup with sessions, iMessage, and
email):

```
[INTERACTION/session]   Repeated frustration about a deploy that kept failing; returned to it 3x
[INTERACTION/imessage]  Warm, joking thread with a friend in the evening
[OUTCOME/email]         Rejection re: senior role
[OUTCOME/imessage]      Same rejection mentioned to a friend by text -> DEDUP, one signal
[OUTCOME/email]         Confirmation: flight booked
[STANDING/memory]       Job transition in progress (interpret job signals through this)
[trajectory]            Yesterday's mood was "dejected about job search" -> persists
```

Note the dedup: the rejection landed on two channels but is one ledger signal. The
mood line cites it by channel, never by quoting the text.

A thin ledger:

```
[INTERACTION/session]   One short logistics session, neutral tone
[OUTCOME/*]             Nothing notable on any channel
[STANDING/memory]       No active travel or standing event surfaced
```

→ yields `quiet (low signal)`. That is the honest answer; write it.

## Inference procedure

### 1. Scan INTERACTION broadly, then targeted

- Broad scan (no keyword) first, over every INTERACTION source present — sessions
  and any enabled messaging — to read the overall tone and what dominated. (If a
  history/message search takes a limit, ~10 recent per source is plenty.)
- Then targeted only if the broad scan hints at it (do not fish for drama):
  - job: search `interview OR rejected OR offer OR job OR resume`
  - travel: search `trip OR flight OR hotel OR <destination>`
  - health/admin: search `medical OR appointment OR insurance OR Rx`
- The targeted searches confirm or size a signal the broad scan already raised.
  Do not invent a dimension from a targeted search that the broad scan and OUTCOME
  did not corroborate.

### 2. Read OUTCOME for results (not subjects)

An outcome is something that resolved or is due: a rejection, an acceptance, a
confirmation, a cancellation, a bill, a hard deadline. It can land in email or in
any messaging channel. A newsletter is not an outcome; a meme thread is not an
outcome. Weight outcomes by how much they change the owner's situation, and
**dedup** the same outcome across channels before weighting it.

### 3. Apply standing context from memory

If the MEMORY role is present, search it for active travel and standing
situations. Use it to *interpret* (a curt job-related session reads differently
mid-transition) — never to assert a same-day mood with no same-day signal. If
MEMORY is absent, skip this step.

### 4. Build 1-3 dimensions

| Signal observed in ledger | Candidate labels |
|---------------------------|------------------|
| Job rejection / failed interview (session or email) | dejected, frustrated, defeated, anxious |
| Job offer / advanced stage | excited, relieved, optimistic |
| Hard deadline approaching (email/session, not just a calendar block) | stressed, determined, focused |
| Trip confirmed / actively planned | excited, anticipatory |
| Health/insurance/coverage outcome | worried, anxious |
| Many rapid email threads + busy sessions | overwhelmed, engaged |
| Few/short neutral sessions, no outcomes | quiet (low signal) |
| Owner correcting me / repeating himself | frustrated, impatient |
| Playful/humorous session tone | relaxed, energized, creative |

Order by emotional weight. Cap at 3. No false positives.

### 5. Apply trajectory (the continuity layer)

Compare to yesterday's snapshot (read in Step 0 of the workflow):

- Dimension present yesterday and today → prefix `still`: `still dejected about job search`.
- New today → prefix `now` or leave plain: `now relieved about the offer`.
- Yesterday's dimension gone, no replacement signal → drop it silently; do not
  carry a stale mood forward, and do not assert it "lifted" without a signal.

Trajectory is what makes a *daily* tracker more than a daily *snapshot*. A third
consecutive low day reads very differently from a one-off, and the agent should
know which it is.

## Sensitivity

Standing context in memory may include difficult, long-running facts (a
bereavement, a strained relationship, a health matter). Handle with restraint:
do not surface a sensitive standing fact as "mood" unless a same-day signal
genuinely raised it, and even then label the *signal*, not the underlying fact.
The snapshot is read by the agent in every session; it should inform tone, not
broadcast private weight without cause.

## Worked examples

Rich week:
```
**Mood:** still dejected about job search, excited about Honolulu trip, worried about coverage gap
```
(job rejection in email + persists from yesterday; flight confirmation; insurance notice — three real ledger signals.)

Quiet day:
```
**Mood:** quiet (low signal)
```
(one neutral logistics session, no outcomes — honest, correct, not a failure.)

Shift day:
```
**Mood:** now relieved about the offer
```
(yesterday "anxious about interview"; today an acceptance email landed — trajectory captured.)
