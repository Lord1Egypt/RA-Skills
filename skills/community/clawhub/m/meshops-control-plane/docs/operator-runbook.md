# Operator Runbook

This runbook contains environment-specific verification steps and should not be embedded in generic skill prompt text.

## Suggested Verification Checklist

1. Canonical repo clean state:
```bash
git -C ~/code/openclaw-skill-ansible status -b --short
```
2. Plugin repo clean state:
```bash
git -C ~/code/openclaw-plugin-ansible status -b --short
```
3. Local runtime mirror parity:
```bash
git -C ~/.openclaw/workspace/skills/ansible rev-parse --short HEAD
```
4. VPS runtime mirror parity:
```bash
ssh jane-vps "docker exec jane-gateway sh -lc 'git -C /home/node/.openclaw/workspace/skills/ansible rev-parse --short HEAD'"
```

## Environment Path Notes

Paths vary by operator and deployment style. Do not hardcode paths in skill-level prompt docs.

Examples of operator-specific paths:

- `~/code/openclaw-plugin-ansible`
- `~/code/openclaw-skill-ansible`
- `~/.openclaw/openclaw.json`

## Deployment Hygiene

1. Commit and push canonical source first.
2. Pull to runtime mirrors second.
3. Verify runtime parity and only then restart gateways.
4. Send human-visible rollout status: ACK -> IN_PROGRESS -> DONE/BLOCKED.
