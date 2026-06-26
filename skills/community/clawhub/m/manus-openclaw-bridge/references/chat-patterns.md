# Chat patterns

## Recommended direct-message trigger

Treat messages in these forms as Manus jobs:

- `Manus, generate an image of a rainy forest`
- `Manus, research the robotics industry`
- `manus: create a 10-slide deck about AI hardware`

Strip the prefix and send the remainder to `scripts/manus_prompt.sh`.

## Recommended group-chat trigger

Use a stricter trigger in groups, for example:

- require an @mention
- require the message to start with `Manus,` or `manus:`

That avoids accidental task launches when people casually mention Manus.

## Result handling

- For image outputs: send the image file(s) back directly.
- For slide/report outputs: send the file if available, otherwise send the task URL and a short summary.
- For long-running jobs: acknowledge quickly, then poll every few seconds with a bounded timeout.

## Failure handling

If Manus returns no files:
- inspect the raw task via `scripts/manus_get_task.sh`
- check whether output is text-only
- send the useful text/status instead of saying only "failed"
