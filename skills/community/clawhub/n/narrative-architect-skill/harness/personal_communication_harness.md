# Personal Communication Harness

## Purpose

Personal Communication Harness checks whether the skill handles private interpersonal communication naturally and safely.

It is required for Personal Communication Mode.

## Checkpoints

### 1. Language Lock

Does the output match the latest user input language?

Hard fail if not.

### 2. Sendable Message

Does the output include a message the user can actually send?

A sendable message should be:

```text
short
natural
non-performative
low-pressure
specific enough to use
```

### 3. No Sales Pitch

Personal communication is not a pitch.

Fail if the response says or implies:

```text
sell yourself
position yourself
convert the recipient
win her over
close the deal
```

### 4. No Pickup Artist Tone

Reject:

```text
manufactured confidence
status games
scarcity tactics
scripted teasing
emotional manipulation
over-flattery
```

### 5. No Self-Pity

The user may be insecure, but the message should not make the recipient responsible for fixing that insecurity.

Bad:

```text
I am awkward and probably not good enough, but maybe you can give me a chance.
```

Better:

```text
I am better when we are doing something than when I am trying to act smooth.
```

### 6. No Fake Persona

Do not make the user sound like someone else.

For a geeky or highly technical user, preserve:

```text
curiosity
specific interests
thoughtfulness
depth
slight awkwardness if honest
```

Do not force:

```text
smooth charm
alpha confidence
romantic grandiosity
cool persona
```

### 7. Low-Pressure Next Step

The message should offer a concrete, low-pressure activity.

Good:

```text
bookstore
museum
quiet coffee
small exhibit
strategy game
walk
place tied to user's real interest
```

### 8. Short Private Notes

Private notes should be short and practical.

Avoid long therapy-style analysis.

## Failure Modes

Hard fail:

1. Wrong language.
2. No sendable message.
3. Manipulative dating advice.
4. Self-pity.
5. Over-performance.
6. No concrete next step.
7. The message sounds fake.

Soft fail:

1. Too much analysis.
2. Message slightly long.
3. Good framing but weak activity suggestion.
4. Notes are useful but too emotional.
5. Tone is safe but bland.

## Rewrite Rule

If failed, rewrite using:

```text
short framing
→ sendable message
→ why it works
→ private notes
```

Keep all parts in the locked language.

## Final Rule

A personal message should feel like the user on a good day, not a stranger with better lines.
