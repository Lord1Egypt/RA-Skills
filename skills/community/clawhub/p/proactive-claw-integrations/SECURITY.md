# Proactive Claw Integrations — Security Notes

This bundle contains optional integrations that may contact third-party services.
Use only what you need.

## External network-capable scripts

- `scripts/cross_skill.py`
  - GitHub via `gh` CLI (read-only metadata)
  - Notion API search (`https://api.notion.com/v1/search`)
- `scripts/team_awareness.py`
  - Reads calendars shared with the authenticated account
- `scripts/optional/setup_clawhub_oauth.sh`
  - Optional `credentials.json` fetch from `https://clawhub.ai`
  - Fail-closed pinning checks are enforced

## Local automation helpers

- `scripts/install_daemon.sh`
  - Installs user-level periodic execution for proactive workflows

## Recommendation

For strict privacy deployments, keep only core installed and do not install this bundle.
