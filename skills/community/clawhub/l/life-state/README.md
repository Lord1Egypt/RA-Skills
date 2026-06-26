# life-state

A boring, durable daily-state primitive for the [lifekit](https://github.com/dsdevq/lifekit) ecosystem. Captures mood, energy, soreness, and sleep quality to `~/.life/state/<date>.json` so other personal-AI skills can give state-aware suggestions instead of generic templates.

Not a chat experience — integration glue.

## Install

```bash
git clone https://github.com/dsdevq/life-state.git
cd life-state
npm install
npm run build
npm install -g .
```

Requires Node >= 20.

## Usage

```bash
life-state set --mood tired --energy 4 --sore chest,triceps --sleep poor --note "late night"
life-state get
life-state get --date 2026-05-15
life-state week
life-state week --days 14
```

All flags on `set` are optional but at least one is required. Multiple `set` calls on the same day merge — morning check-in + post-workout check-in compose cleanly.

## Data shape

One JSON file per day at `~/.life/state/<YYYY-MM-DD>.json`:

```json
{
  "date": "2026-05-15",
  "mood": "tired",
  "energy": 4,
  "soreness": ["chest", "triceps"],
  "sleep_quality": "poor",
  "note": "headache, late night",
  "updated_at": "2026-05-15T19:30:00.000Z"
}
```

Stable layout — other skills should read this directly.

## Why

Part of the [lifekit](https://github.com/dsdevq/lifekit) personal-AI memory framework: file-based, tool-agnostic, plain JSON/Markdown/YAML. Readable by Claude Code, any other agent, or a human with `cat`.

The companion `SKILL.md` ships in this repo and is what OpenClaw / Claude Code load to discover the CLI.

## License

MIT. See [LICENSE](LICENSE).
