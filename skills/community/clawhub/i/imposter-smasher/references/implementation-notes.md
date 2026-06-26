# Implementation Notes

## Scope
This skill is orchestration-first. It should sequence dependencies, delegate specialized work, and keep outputs compact and reliable.

## Minimal Runtime Plan
1. Resolve timezone and fetch next-day calendar events.
2. Get one selected event from user.
3. Run Contextual.ai research for topic + participants.
4. Draft executive summary and narration script using templates.
5. Validate narration runtime (3-5 min).
6. Call ElevenLabs or Chatterbox to render final audio.
7. Return prep package with citations and confidence levels.

## Validation Checklist
- Calendar data present or user supplied substitute.
- At least 3 credible sources for non-trivial meetings.
- Summary contains objective, risks, approach, and question bank.
- Audio duration between 180 and 300 seconds.
- Out-of-scope actions were not performed.
