# glancely

> One ClawHub skill that scaffolds any personal tracker you can describe.
> Dashboard, cron, reminders, mood, diary — from one sentence.

## Install

```bash
# 1. Install the skill from ClawHub
openclaw skills install glancely

# 2. Install the Python package
pip3 install glancely         # or: pip install glancely
# If you hit "externally-managed-environment" (macOS Homebrew):
brew install pipx && pipx install glancely

# 3. One-time setup
glancely setup
```

That's it. Tell your agent what you want to track.

## Example

```
You: "I want to track my daily workouts and build a reading habit"

Agent: "I'll create:
  workout — type, duration, notes (daily 9pm)
  reading — book title, pages read (daily 10pm)
  Dashboard shows both. Sound good?"

You: "Perfect, go ahead"

Agent: [scaffolds both → migrations → cron → dashboard built]
```

## CLI

```
glancely setup               Minimal init (migrations)
glancely list                 Your trackers
glancely scaffold --name X   Create a new tracker
glancely dashboard build      Build dashboard
glancely dashboard open       Build and open
glancely doctor               Health check
```

## Examples

See `examples/` for reference blueprints:
- mood, reminder, mit, diary_logger

## License

MIT
