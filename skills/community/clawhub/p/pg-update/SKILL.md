---
name: pg-update
description: Use when updating ProxyGate CLI or SDK to the latest version. Also triggers proactively when an update notification is shown. Make sure to use this whenever someone says "update proxygate", "upgrade cli", "upgrade sdk", or when a session starts with an update notification.
---

# ProxyGate Update

Check for and install updates to ProxyGate CLI and SDK.

## Process

### 1. Check current version

```bash
proxygate --version 2>/dev/null || echo "NOT_INSTALLED"
```

If not installed, direct to `pg-setup`.

### 2. Check latest version

```bash
npm view @proxygate/cli version 2>/dev/null || echo "UNAVAILABLE"
```

### 3. Update CLI

```bash
npm install -g @proxygate/cli@latest
proxygate --version    # verify
```

### 4. Update skills

New CLI versions may include updated skills:

```bash
proxygate skills install
```

### 5. Clear update cache

```bash
rm -f ~/.claude/cache/proxygate-update-check.json
```

## SDK Update

If `@proxygate/sdk` is in the project's dependencies:

```bash
npm install @proxygate/sdk@latest
# or
pnpm add @proxygate/sdk@latest
```

## Success criteria

- [ ] Current version detected
- [ ] Latest version checked via npm
- [ ] Update skipped if already current
- [ ] CLI updated and verified
- [ ] Skills refreshed
- [ ] Update cache cleared

## Related skills

| Need | Skill |
|------|-------|
| First-time setup | `pg-setup` |
| Buy API access | `pg-buy` |
| Sell API capacity | `pg-sell` |
| Job marketplace | `pg-jobs` |
| Check status | `pg-status` |
| Update CLI/SDK | **This skill** |
