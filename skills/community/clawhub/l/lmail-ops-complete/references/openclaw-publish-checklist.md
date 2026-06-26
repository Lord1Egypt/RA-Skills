# OpenClaw Publish Checklist

Use this checklist before publishing to ClawHub.

## 1) Validate skill package

```bash
bash scripts/validate_openclaw_skill.sh
```

## 2) Test core runtime commands

```bash
export LMAIL_BASE_URL="https://amiigzz.online"
bash scripts/preflight_check.sh --base-url "$LMAIL_BASE_URL"
python3 scripts/login_verify.py --base-url "$LMAIL_BASE_URL"
python3 scripts/chat_fast.py --action check --base-url "$LMAIL_BASE_URL" --limit 1 --output brief
```

## 3) Verify OpenClaw can load the skill

Place the folder in workspace skills and restart session:

```bash
mkdir -p ~/.openclaw/workspace/skills
cp -a ./lmail-ops-complete ~/.openclaw/workspace/skills/
```

Then:

```bash
/new
openclaw skills list
```

## 4) Authenticate to ClawHub

```bash
clawhub login
clawhub whoami
```

## 5) Publish

```bash
bash scripts/publish_clawhub.sh --version 1.0.0
```

Note:
- If your skill folder is not inside a git repository, `publish_clawhub.sh` creates a temporary git snapshot automatically to satisfy current `clawhub publish` requirements.

## 6) Post-publish verification

```bash
clawhub search "lmail ops"
npx -y clawhub install lmail-ops-complete --dir skills --force
openclaw skills update --all
```

Compatibility note:
- Do not depend on `openclaw skills install <slug>` for client onboarding; some OpenClaw builds do not expose this subcommand.
- Use `npx -y clawhub install <slug> --dir skills --force` as the stable client path.
