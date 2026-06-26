# ClawHub Security Check

Pre-installation security assessment for ClawHub skills with optional sandbox testing.

## Installation

```bash
openclaw skill install clawhub-security-check
```

## Usage

The skill activates automatically before any `openclaw skill install` command, or when you ask about skill safety.

## How It Works

1. Fetches skill metadata from ClawHub and GitHub
2. Calculates a risk score (0–100) based on source, code type, activity, and community
3. Runs sandbox testing if score is below 80 and skill has executables
4. Presents a security report and asks for confirmation before installing

## File Structure

```
├── SKILL.md                        # Core workflow (agent-level enforcement)
├── scripts/
│   ├── openclaw-security-wrapper.sh # CLI-level enforcement
│   └── setup-cli-enforcement.sh    # One-command installer
├── references/
│   ├── risk-scoring.md             # Scoring table & interpretation
│   ├── sandbox-procedure.md        # Sub-agent test template
│   └── report-templates.md         # Report formats
├── CHANGELOG.md                    # Version history
└── README.md                       # This file
```

## CLI Enforcement (Optional)

The SKILL.md enforces security checks through the assistant, but users can bypass it by running `openclaw skills install` directly in the terminal. The wrapper script prevents this.

```bash
cd scripts && bash setup-cli-enforcement.sh
```

This installs a CLI wrapper that intercepts `openclaw skills install` and blocks it unless the security check has been run and approved through the assistant.

## Troubleshooting

- **Check takes too long**: run `openclaw status`, kill hung subagents with `subagents kill <id>`
- **Sub-agent won't spawn**: run `/compact` to free context, or `openclaw gateway restart`
- **ClawHub unavailable**: retry, use GitHub-only analysis, or cancel
- **Cache issues**: `rm ~/.openclaw/skill-security-cache.json`

## License

MIT License - Free to use, modify, and distribute.
