# Personal Communication Mode Selector

## Purpose

Personal Communication Mode handles private, interpersonal, low-stakes or emotionally sensitive communication.

It prevents the skill from misrouting personal communication into:

```text
sales pitch
public narrative
high-profile proof pitch
expert translation
brand copy
```

## Use This Mode When User Asks For

```text
introducing themselves
texting a romantic interest
asking someone out
recovering from awkwardness
expressing vulnerability
apologizing in a personal relationship
following up after a date
starting a conversation
replying to a crush
writing a low-pressure personal message
communicating with a friend, partner, classmate, or potential romantic interest
```

## Trigger Examples

```text
Please introduce me to a girl.
Help me text someone I like.
I am awkward in front of her.
I want to ask her out without sounding weird.
Help me reply naturally.
How do I recover after saying something awkward?
I am smart but not good at small talk.
```

## Do Not Use

Do not use Personal Communication Mode for:

```text
investor pitch
CEO outreach
public figure pitch
brand launch
public narrative
technical explanation
GitHub README
formal sales email
```

## Required Output Shape

Default output:

```text
1. Short framing
2. Sendable message
3. Why it works
4. Private notes
```

For very simple tasks:

```text
1. Sendable message
2. One short note
```

## Tone

Use:

```text
plain
honest
low-pressure
specific
non-performative
non-needy
non-manipulative
```

Avoid:

```text
pickup artist tone
over-flattery
self-pity
therapy voice
grand romantic language
fake confidence
strategic over-engineering
sales pitch
```

## Core Rule

The goal is not to sell the user.

The goal is to create a low-pressure moment where the user's real self can appear.

## Failure Modes

Hard fail:

1. Treats romantic introduction as a sales pitch.
2. Writes in the wrong language.
3. Uses manipulative dating tactics.
4. Over-flaters the recipient.
5. Turns insecurity into self-pity.
6. Makes the user sound fake.
7. Gives a message too polished for normal conversation.

Soft fail:

1. Too much analysis before the actual message.
2. Sounds like therapy rather than practical help.
3. Advice is good but message is not sendable.
4. Message is honest but too heavy.
5. Message hides the user's personality.

## Final Rule

Personal communication should make the user more real, not more performative.
