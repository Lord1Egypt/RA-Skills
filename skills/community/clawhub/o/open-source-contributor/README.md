# open-source-contributor

Autonomous GitHub contribution agent for OpenClaw. Scouts small repositories, analyzes issues, writes fixes using AI, and submits PRs.

**ClawHub:** https://clawhub.ai/wahajahmed010/open-source-contributor  


## Overview

This skill enables autonomous open-source contributions during quiet hours with **graduated complexity levels**:

- **Level 1:** Typo/link fixes (3 repos/night)
- **Level 2:** README/documentation (3 repos, >50% approval)
- **Level 3:** Simple code fixes (2 repos, >70% approval)
- **Level 4:** Moderate code (1 repo, >90% approval)

## Safety Features

- ✅ **Approval-based progression** — complexity increases only with positive track record
- ✅ **Scope understanding requirement** — unclear issues are skipped
- ✅ **Security pattern blocking** — auth/crypto/token files excluded
- ✅ **Test validation** — must pass existing test suite
- ✅ **AI disclosure** — every PR includes disclosure
- ✅ **Auto-pause** — stops if rejection rate >30%
- ✅ **Append-only logging** — full audit trail

## Architecture

```
Scout-Agent → finds candidates (5 max)
     ↓
Analyzer-Agent → scope understanding + complexity check
     ↓
Coder-Agent (qwen3-coder:480b:cloud) → writes fix
     ↓
Tester-Agent → validates fix
     ↓
Reviewer-Agent → pre-flight checklist
     ↓
Submitter-Agent → opens PR with disclosure
```

## Installation

### Via ClawHub (Recommended)

```bash
# Install via ClawHub CLI
clawhub install wahajahmed010/open-source-contributor

# Or via OpenClaw
openclaw skill install open-source-contributor
```

**ClawHub Page:** https://clawhub.ai/wahajahmed010/open-source-contributor

### Via GitHub

```bash
# Clone to OpenClaw skills directory
cd ~/.openclaw/skills
git clone https://github.com/wahajahmed010/open-source-contributor.git

# Install dependencies
pip install -r requirements.txt

# Configure
export GITHUB_TOKEN="ghp_your_token_here"
python3 open-source-contributor/scripts/setup.py
```

## Configuration

`~/.openclaw/workspace/contrib-scout/config.json`:

```json
{
  "github_token": "ghp_xxxxxxxxxxxx",
  "max_repos_per_night": 3,
  "complexity_level": 1,
  "approval_threshold": 0.5,
  "quiet_hours": {
    "start": "23:00",
    "end": "07:00"
  },
  "blocked_patterns": [
    "auth", "crypto", "token", "key",
    "password", "credential", "secret"
  ]
}
```

## Usage

### Manual Run

```bash
python3 ~/.openclaw/skills/open-source-contributor/scripts/contrib-pipeline.py
```

### Cron Schedule

```bash
# Run nightly at 23:00
0 23 * * * cd ~/.openclaw/skills/open-source-contributor && python3 scripts/contrib-pipeline.py
```

### Check Status

```bash
# View recent activity
tail -20 ~/.openclaw/workspace/contrib-scout/logs/contributions.jsonl

# Check approval rate
python3 ~/.openclaw/skills/open-source-contributor/scripts/stats.py
```

## Requirements

- Python 3.10+
- Git
- GitHub Personal Access Token with `public_repo` scope
- OpenClaw with sessions_spawn capability

## GitHub Token Setup

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `public_repo`
4. **Never** grant `repo` scope (includes private repos)
5. Copy token to `GITHUB_TOKEN` environment variable

## Complexity Level Details

| Level | Examples | Max Repos | Approval Required |
|-------|----------|-----------|-------------------|
| 1 | Typo fixes, dead links, formatting | 3 | None |
| 2 | README updates, doc improvements | 3 | >50% |
| 3 | Simple code fixes (1-2 functions) | 2 | >70% |
| 4 | Multi-file logic changes | 1 | >90% |

## PR Template

Every PR includes:

```markdown
## Description
[Brief description of fix]

## Changes
- [Specific change 1]
- [Specific change 2]

## Testing
- [ ] Tests pass (or N/A)

## Disclosure
This contribution was generated with AI assistance and reviewed before submission.
```

## Monitoring

Track contributions:

```bash
# Daily summary
python3 scripts/stats.py --today

# Weekly report
python3 scripts/stats.py --week

# Check for paused status
python3 scripts/status.py
```

## Troubleshooting

**Pipeline paused?**
- Check rejection rate: `cat logs/contributions.jsonl | grep rejected`
- If rate >30%, system auto-pauses. Review recent PRs.

**No candidates found?**
- Scout searches for `good first issue` + `help wanted` labels
- Try broadening language filter in config

**Tests failing?**
- Tester-Agent reports which tests failed
- Review logs in `logs/contributions.jsonl`

## Development

```bash
# Run tests
pytest tests/

# Type check
mypy scripts/

# Lint
ruff check scripts/
```

## Acknowledgments

**Inspiration:** This skill was inspired by [Dreaming](https://clawhub.ai/briancolinger/dreaming) by briancolinger — a creative skill that uses quiet hours for freeform reflection. While Dreaming focuses on introspective journaling, open-source-contributor takes a similar "quiet hours automation" approach but directs it toward actionable, measurable contributions to the open-source community.

## License

MIT © wahajahmed010

## Disclaimer

This tool makes commits under your GitHub identity. Review the safety features before use. You are responsible for all contributions made under your account.
