# Event Modeling

Use event records when the sentence describes an action, occurrence, or change, especially when time, place, or participant roles matter.

## When to create an event

Create an event if the text includes:
- a verb of action or occurrence
- multiple roles such as agent and object
- temporal information
- spatial information
- change over time

Examples:
- publication
- meeting
- acquisition
- release
- movement
- observation

## Minimal event fields

- `id`
- `type`
- `trigger`
- `participants`
- `time`
- `location`
- `evidence`
- `confidence`

## Do not over-flatten

Sentence:
"Apple released the iPhone in 2007 in the United States."

Prefer:
- event type `Release`
- agent `Apple`
- object `iPhone`
- time `2007`
- location `United States`

Then map to triples.

## When a simple triple is enough

If the statement is static and does not depend on participant roles, time, or place, a plain triple is enough.

Example:
- `(Paris, located_in, France)`
