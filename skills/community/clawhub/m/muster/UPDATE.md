# Muster — Update

## Automatic Updates (Patch + Minor)

```bash
bash {baseDir}/scripts/update.sh
```

Run when heartbeat returns `update_available: true`. The script handles: fetch → major version check → pull → build → migrate → restart → health check → auto-rollback on failure. Outputs JSON report.

## Major Version Updates (v1 → v2)

The script detects major bumps and stops. When it reports `"action": "major_version_detected"`:

1. Notify the human with the changelog link
2. Wait for explicit confirmation
3. Run manually: `cd ~/muster && git pull origin main && npm install && npm run build && npx drizzle-kit migrate && pm2 restart muster`
4. Verify: `curl -s http://localhost:3000/api/health`
5. If it fails: `git checkout <previous-commit> && npm install && npm run build && pm2 restart muster`

## Skill Updates

When heartbeat returns `skill_version_expected` that doesn't match your SKILL.md `version:` field:

```bash
clawhub update muster
```

Start a new session for the updated skill to load.
