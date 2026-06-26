# Mac Health Check

`mac-health-check` is an OpenClaw / ClawHub skill for reading live macOS telemetry through [`macmon`](https://github.com/vladkens/macmon).

It helps an agent answer questions like:

- "What is my Mac temperature right now?"
- "Is the machine under heavy load?"
- "How much RAM and swap are in use?"
- "Give me a quick health snapshot of this Mac"

The skill wraps `macmon pipe -s 1` and turns a raw telemetry sample into a short, practical summary.

## Installation

### Via ClawHub

```bash
clawhub install mac-health-check
```

### Manual

```bash
git clone https://github.com/RuBAN-GT/mac-health-check-skill.git ~/.openclaw/skills/mac-health-check
```

## What is included

- `SKILL.md`
- `bin/macmon-safe.sh`
- `scripts/macmon_status.py`
- `scripts/test_macmon_status.py`
- `references/sample-output.md`

## Prerequisites

- macOS
- `macmon` installed and available in `PATH`

Recommended install:

```bash
brew install macmon
```

The skill metadata also declares a brew installer, so OpenClaw's macOS Skills UI can surface an `Install macmon (brew)` button when `macmon` is missing.

In some OpenClaw exec environments, Homebrew-installed binaries work only from a login shell. This repo includes `bin/macmon-safe.sh`, a small wrapper that retries `macmon` through `zsh -lic` when needed.

## Verify setup

Run:

```bash
bash bin/macmon-safe.sh pipe -s 1
```

If that prints a JSON object, the skill is ready to use.

## Local development

Run tests:

```bash
cd scripts
python3 -m unittest test_macmon_status.py
```

Build a `.skill` archive from the skill root:

```bash
mkdir -p dist
zip -r dist/mac-health-check.skill .
```

## Notes

- The skill is intentionally scoped to `darwin`.
- Runtime dependency checks and install UI are defined in `SKILL.md` via `metadata.openclaw.requires` and `metadata.openclaw.install`.
- The generated summary is a snapshot, not a long-term thermal diagnosis.

## Contributing

Forks, fixes, and improvements are welcome.

If you want to improve the skill, feel free to fork the repo, make changes, and open a pull request. Contributions are especially useful around:

- clearer skill instructions
- better telemetry interpretation
- parser robustness for future `macmon` output changes
- tests and sample inputs
