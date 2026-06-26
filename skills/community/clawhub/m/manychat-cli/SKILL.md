---
name: manychat-cli
summary: Agent-friendly ManyChat automation CLI with playbook support for multi-step workflows.
---

# ManyChat CLI Skill

Use this skill when you need to automate ManyChat operations from OpenClaw or other AI agents.

## What this skill provides
- A local CLI wrapper at `/Users/danielfoch/manychat-cli/manychat_cli.py`
- Stable JSON output and exit codes for automation orchestration
- High-value ManyChat commands:
  - subscriber lookup and profile reads
  - tag add/remove
  - custom field updates
  - flow/content sends
  - create/update subscriber
  - raw endpoint passthrough
  - JSON playbook execution for sequential automation steps

## Requirements
- `MANYCHAT_API_KEY` environment variable must be set.
- Optional: `MANYCHAT_BASE_URL` to override API host.

## Usage

Validate token:
```bash
cd /Users/danielfoch/manychat-cli
./manychat_cli.py ping --pretty
```

Find by email:
```bash
./manychat_cli.py find-system --field-name email --field-value 'lead@example.com' --pretty
```

Run a multi-step playbook:
```bash
./manychat_cli.py playbook-run \
  --file /Users/danielfoch/manychat-cli/sample_playbook.json \
  --vars-json '{"email":"lead@example.com"}' \
  --pretty
```

## File references
- CLI: `/Users/danielfoch/manychat-cli/manychat_cli.py`
- Playbook example: `/Users/danielfoch/manychat-cli/sample_playbook.json`
- Shell example: `/Users/danielfoch/manychat-cli/example_automation.sh`
- Extended docs: `/Users/danielfoch/manychat-cli/README.md`
