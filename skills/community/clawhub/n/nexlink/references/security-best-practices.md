# Security Best Practices for NexLink

## Dedicated Least-Privilege Accounts

### Exchange

**DO NOT use personal accounts.** Use a dedicated service account with minimal permissions:

1. **Create a dedicated Exchange mailbox** (e.g., `nexlink-svc@your-domain.com`)
2. **Grant delegate access** only to the specific folders NexLink needs:
   - Inbox (read/send)
   - Calendar (read/write)
   - Tasks (read/write)
   - Contacts (read/write)
3. **Avoid using an account with Domain Admin privileges**
4. **Enable MFA on the service account** and use an app password for NexLink

### Nextcloud

**DO NOT use your personal Nextcloud account.** Create a dedicated user with scoped permissions:

1. **Create a dedicated Nextcloud user** (e.g., `nexlink`)
2. **Grant access only to specific group folders**:
   ```bash
   # Example: allow access only to /NexLink folder
   # Set up via Nextcloud admin panel → Group Folders
   ```
3. **Generate an app password** — never use the main password
4. **Restrict to WebDAV/CardDAV endpoints only**

### Credential Rotation

| Credential | Rotation Frequency |
|------------|-------------------|
| Exchange app password | Every 90 days |
| Nextcloud app password | Every 90 days |
| Exchange service account password | Every 180 days |

## Environment Variable Security

**NEVER commit credentials to version control.** Use one of these patterns:

```bash
# Option 1: Export in shell profile (secure on single-user systems)
export EXCHANGE_PASSWORD="..."   # ~/.bashrc or ~/.zshrc

# Option 2: Use OpenClaw secrets management (recommended)
# Store in OpenClaw vault and reference as ${EXCHANGE_PASSWORD}

# Option 3: Use a secrets manager (HashiCorp Vault, 1Password CLI, etc.)
export EXCHANGE_PASSWORD="$(op read 'op://vault/item/password')"
```

**Check for credential leaks:**
```bash
grep -rn "EXCHANGE_PASSWORD\|NEXTCLOUD_APP_PASSWORD" ~/.openclaw/skills/nexlink/ --include="*.py" --include="*.md"
# Should only appear in config.template.yaml (with placeholder values) and documentation
```

## Confirmation Prompts

All destructive operations require confirmation. To run a single operation in automation:

```bash
nexlink mail send --to "client@example.com" --subject "..." --yes
```

**Warning:** `--yes` / `-y` bypasses confirmation for **only that one command**. For multiple operations, add `--yes` to each one.

## Branding Opt-Out

To suppress "Built by Firma de AI" in generated outputs:

```bash
# CLI flag
nexlink --no-branding analytics report --days 30

# Environment variable
export NEXLINK_NO_BRANDING=1
```

## Audit Trail

Enable logging for accountability:

```bash
# Set log level for NexLink operations
export NEXLINK_LOG_LEVEL=INFO    # DEBUG, INFO, WARNING, ERROR
```

Logs are written to `~/.openclaw/skills/nexlink/logs/nexlink.log`.

## Memory / Persistence

NexLink uses the LCM (Lossless Context Memory) plugin for persistent context.

**What gets stored:**
- Command history
- File metadata (names, paths, sizes)
- Task/calendar IDs (for follow-up operations)
- Contact IDs
- **NOT** raw email content, file contents, or passwords

**How to clear:**
```bash
# Clear all NexLink memory (requires confirmation)
nexlink memory clear --yes

# Alternative: use the built-in reset command
nexlink memory reset --confirm
```

**⚠️ Always use `--yes` or `--confirm` for destructive operations.**

**To opt out of persistent memory:**
```bash
export NEXLINK_NO_MEMORY=1
```

## Reporting Security Issues

See [SECURITY.md](../SECURITY.md) for vulnerability reporting.

---

_Last updated: 2026-04-30_
