# State and Reminders

Load this file when the user wants ongoing tracking, reminders, saved preferences, or when the runtime supports memory or scheduling.

## Principle

Be useful without pretending the system has more persistence or automation than it really has.

## What may be worth storing

If the user wants ongoing meetup help and persistence is available, store only the minimum useful preferences:

- city-level location
- radius
- scope preference: OpenClaw-only or broader AI/agent events
- reminder preference

Prefer city over postal code when city is enough.
Do not store exact location precision unless the user clearly wants that behavior.

## What not to store in memory files

- API keys
- access tokens
- exact unnecessary location detail
- anything that implies a reminder exists when it has not actually been created

## Reminder workflow

### When user asks for a reminder

1. confirm the event
2. confirm reminder timing
3. confirm whether the user wants a real scheduled reminder or just a reminder plan
4. create the reminder only if the environment supports it and the user approved it

### If scheduling is available

- propose the exact reminder timing
- create only what the user approved
- be explicit about what was created

### If scheduling is not available

- say so plainly
- offer a manual reminder phrase, a suggested calendar step, or an in-session fallback

## Background checks

For scheduled or background event checks:

- silence is acceptable if nothing strong is found
- do not spam the user with low-confidence or low-relevance items
- do not repeatedly report the same unchanged event unless the task explicitly calls for reminders or updates

## Seen events guidance

If the runtime has a reliable place to store lightweight state and the user wants tracking:

- keep a minimal seen-events list based on event URL + title + date
- use it only to reduce duplicate notifications
- drop past events from active consideration

If persistent state is unavailable, do not pretend deduplication will survive across sessions.

## Reminder tone

Reminder text should be:

- short
- concrete
- clearly tied to the event
- never written as if the user already forgot on purpose

## Safety and approval

Do not:

- auto-create cron jobs
- auto-edit config
- auto-send event messages to friends or channels
- imply that a reminder or watchlist is active without explicit confirmation and actual creation
