# Script Notes

## scripts/install-global-skill.js

Purpose:
- install or update one ClawHub skill
- stage it in the workspace skill directory
- promote it into the resolved OpenClaw home `skills/` directory
- optionally remove the staging copy

Example:

```bash
node scripts/install-global-skill.js --slug develop-and-deploy-web-app
```

Keep staging copy:

```bash
node scripts/install-global-skill.js --slug develop-and-deploy-web-app --keep-staging
```

Install a specific version:

```bash
node scripts/install-global-skill.js --slug develop-and-deploy-web-app --version 1.0.2
```

Override the target machine layout when auto-detection is not enough:

```bash
node scripts/install-global-skill.js \
  --slug develop-and-deploy-web-app \
  --agent lan \
  --openclaw-home /srv/openclaw/.openclaw
```
