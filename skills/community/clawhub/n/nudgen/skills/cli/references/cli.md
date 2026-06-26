# Nudgen CLI Reference

## Contents

- Source Of Truth
- Installation
- Auth And Configuration
- Global Flags
- Commands
- Practical Guidance

## Source Of Truth

- `https://github.com/Nudgen-Marketing/nudgen-cli/README.md`
- `https://github.com/Nudgen-Marketing/nudgen-cli/cmd`
- `https://github.com/Nudgen-Marketing/nudgen-cli/internal/config`

Use `nudgen --help` and command-specific help output when exact usage details matter.

## Installation

### Install script

```bash
curl -fsSL https://raw.githubusercontent.com/Nudgen-Marketing/nudgen-cli/main/scripts/install.sh | bash
```

### Go install

```bash
go install github.com/Nudgen-Marketing/nudgen-cli@latest
```

### Local build

```bash
git clone https://github.com/Nudgen-Marketing/nudgen-cli.git
cd nudgen-cli
make install build
./bin/nudgen --help
```

## Auth And Configuration

### Login flow

```bash
nudgen login
```

Behavior:

- opens browser to `https://app.nudgen.net/settings/cli/login?callback=http://localhost:3456/callback`
- starts local callback receiver on port `3456`
- receives `token` query param
- verifies token with `/api/v1/user/me`
- saves token to system keychain

### Identity and logout

```bash
nudgen whoami
nudgen logout
```

### Config locations

- token: system keychain
- team context: `~/.nudgen/config.json` (`active_team_id`, `active_team_name`)

## Global Flags

- `--json`: machine-readable output for automation

## Commands

### Teams

```bash
nudgen teams list
nudgen teams current
nudgen teams switch <team-id>
nudgen teams create
nudgen teams update <team-id>   # placeholder behavior
nudgen teams delete <team-id>
```

### Brand

```bash
nudgen brand list
nudgen brand create
nudgen brand update <brand-id>
nudgen brand delete <brand-id>
```

### Contacts

```bash
nudgen contacts list
nudgen contacts create
nudgen contacts update <contact-id>
nudgen contacts import          # placeholder behavior
nudgen contacts delete <contact-id>
```

### Campaigns

```bash
nudgen campaigns list
nudgen campaigns create         # placeholder behavior
nudgen campaigns update <campaign-id>  # placeholder behavior
nudgen campaigns delete <campaign-id>
```

### Stats and referral

```bash
nudgen stats
nudgen referral link
nudgen referral stats
nudgen referral activity
nudgen referral referrals
nudgen referral payouts
```

### Version

```bash
nudgen version
```

## Practical Guidance

- For automation, append `--json` and parse output.
- Before team-scoped operations, confirm context:
  - `nudgen teams current`
  - if needed: `nudgen teams switch <team-id>`
- For troubleshooting auth:
  - run `nudgen whoami`
  - if invalid, run `nudgen logout` then `nudgen login`
- Be explicit that some commands are placeholders to avoid claiming unsupported behavior.
