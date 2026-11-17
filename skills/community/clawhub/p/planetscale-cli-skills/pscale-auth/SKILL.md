---
name: pscale-auth
description: Manage PlanetScale CLI authentication including login/logout, check auth status, and switch accounts. Use when setting up pscale for first time, troubleshooting auth issues, switching PlanetScale accounts, or managing authentication sessions. Triggers on auth, login, logout, authentication, credentials, PlanetScale account.
---

# pscale auth

Manage authentication for the PlanetScale CLI.

## Common Commands

```bash
# Login to PlanetScale (opens browser)
pscale auth login

# Login in automation-friendly JSON mode
pscale auth login --format json

# Logout
pscale auth logout

# Check current authentication status
pscale org show
```

## Authentication Methods

### 1. Interactive Login (Default)

Opens browser for OAuth flow:

```bash
pscale auth login
```

**Best for:** Local development, first-time setup

For agentic or scripted onboarding, prefer JSON output so required user actions can be parsed and relayed without scraping human text:

```bash
pscale auth login --format json
```

JSON login emits its initial pending authorization envelope to stderr and its final result to stdout; inspect both without capturing credentials. If output indicates user action is required, relay only the required action/URL to the user and do not print or store credentials. Device authorization expiry or denial requires a deliberate new login attempt, not repeated polling of the same code.

In human mode, **Access approved. Saving credentials to your system keyring** means browser approval finished and credential persistence may be waiting on a keyring unlock; it is not still waiting for browser approval. Do not enter a password or operate a keyring dialog on the user's behalf. Treat token-save failure as an unconfirmed login, distinguish it from organization-setup failure after credentials were saved, and verify access with read-only `pscale auth check --format json` before switching organizations or using the session. For unattended jobs, use an existing approved service-token configuration rather than starting interactive login.

The CLI resolves its built-in OAuth client values at runtime and omits their values from `pscale auth login --help`. Do not scrape, record, or reproduce OAuth credentials from help output. Treat `--client-id` and `--client-secret` as advanced overrides: use them only when the user explicitly supplies a trusted custom OAuth client, and pass the secret through a secret-safe mechanism rather than shell history or logs.

### 2. Service Tokens (CI/CD)

For automated environments:

```bash
export PLANETSCALE_SERVICE_TOKEN_ID=<token-id>
export PLANETSCALE_SERVICE_TOKEN=<token>
pscale database list --org <org>
```

**Best for:** CI/CD pipelines, automation, production deployments

See `pscale-service-token` skill for token creation.

### 3. API token flags/env

Recent `pscale` global flags also accept API-token based auth for automation:

```bash
pscale database list --org <org> --api-token <token>
```

Prefer environment/secret-manager injection over putting tokens in shell history. Never commit tokens to skill repos or scripts.

## Workflows

### First-Time Setup

```bash
# 1. Login
pscale auth login

# 2. Verify authentication
pscale org show

# 3. List databases to confirm access
pscale database list --org <org>
```

### Switch Between Accounts

```bash
# Logout current account
pscale auth logout

# Login with different account
pscale auth login
```

### CI/CD Authentication

```bash
# Create service token (see pscale-service-token)
pscale service-token create --org <org>

# Use in CI/CD environment
export PLANETSCALE_SERVICE_TOKEN_ID=<token-id>
export PLANETSCALE_SERVICE_TOKEN=<token>

# Test authentication
pscale database list --org <org>
```

## Troubleshooting

### Login fails / browser doesn't open

**Symptoms:** `pscale auth login` hangs or fails

**Solutions:**
- Check network connectivity
- Ensure firewall allows https://auth.planetscale.com
- Try headless browser auth (not supported by pscale, use service tokens instead)
- Use service token for non-interactive environments

### "Unauthorized" errors

**Symptoms:** `401 Unauthorized` or `403 Forbidden` responses

**Solutions:**
- Run `pscale auth logout && pscale auth login` to refresh session
- Verify organization access: `pscale org show`
- Check service token hasn't expired (if using tokens)
- Ensure token has required permissions (database read/write, branch create, etc.)

### Multiple accounts / wrong org

**Symptoms:** Cannot access expected databases

**Solutions:**
- Check current org: `pscale org show`
- Switch org: `pscale org switch <org-name>`
- List all orgs: `pscale org list`
- Logout and login with correct account

### Service token authentication fails

**Symptoms:** Token authentication not working in CI/CD

**Solutions:**
- Verify both `PLANETSCALE_SERVICE_TOKEN_ID` and `PLANETSCALE_SERVICE_TOKEN` are set
- Check token hasn't been revoked: `pscale service-token list --org <org>`
- Ensure token has required permissions for the operation
- Use `--debug` flag to see authentication details

## Related Skills

- **pscale-service-token** - Create and manage service tokens for CI/CD
- **pscale-org** - Switch between organizations
- **pscale-database** - Database operations requiring authentication

## References

See `references/commands.md` for complete `pscale auth` command reference.
