# 专项练习打卡助手

A public-safe OpenClaw skill for structured practice task intake, start confirmation, reminder flow, completion checks, and follow-up tracking.

Published on ClawHub as `practice-session-checkin@1.0.1`.

## What it does

This skill supports a simple practice-session loop:

- a sender provides a practice task
- the assistant records the task as provided
- the assistant confirms when the task should begin
- the assistant sends a reminder at the confirmed time
- the assistant checks whether the task was completed
- the assistant tracks follow-up if unfinished

## Why it exists

It is a reusable template for:

- structured practice coordination
- simple reminder workflows
- completion check flows
- public-safe OpenClaw skill examples

## Where to use it

- dance practice reminders
- music practice check-ins
- sports drill practice
- speaking or reading practice
- public-safe local workflow demos

## Safety boundaries

Keep this skill public-safe:

- no real names
- no institution names
- no group IDs or account IDs
- no private schedules tied to identity
- no sensitive personal or health information

## Examples

### Sender example

- Sender: `Today the practice task is piano scales for 20 minutes.`
- Assistant: `Recorded as provided. What time should practice begin today?`

### Reminder example

- Assistant: `It is time to begin today's practice.`
- Assistant: `Please start the session now.`

### Completion example

- Assistant: `Was the practice completed?`
- Sender: `Not yet, there is one section left.`
- Assistant: `Understood. I will record that the session is unfinished and ask how you would like to continue later.`

For the full example files, see [examples/](./examples/).

For version notes, see [CHANGELOG.md](./CHANGELOG.md).
