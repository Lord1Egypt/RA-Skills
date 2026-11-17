# Migrating notion-sync from v1/v2 to v3

Version 3.0.0 standardizes credentials on `NOTION_API_KEY` supplied by the host
runtime's secret manager. This is intentionally breaking: the skill no longer
reads `--token-file`, `--token-stdin`, or `~/.notion-token`.

The core client remains runtime-agnostic. OpenClaw users can additionally use
destination-bound protected egress without exposing the credential to the
agent process.

## Before upgrading

- Use Node.js 18 or later.
- Keep notion-sync v2.5.3 installed until the v3 verification step succeeds.
- Ensure the Notion integration is shared only with the pages and databases it
  needs.
- Choose a trusted secret manager that can inject `NOTION_API_KEY` into the
  process environment.

## 1. Store the token without exposing it

Store the token as `NOTION_API_KEY` in your platform's secret manager. Do not
put it in chat, command arguments, URLs, source control, or committed `.env`
files.

### OpenClaw protected mode

OpenClaw 2026.9.1+ users should:

1. List secret metadata with the OpenClaw `secrets` tool.
2. If `NOTION_API_KEY` is missing, request it as a protected secret with
   `allowedHosts: ["api.notion.com"]`.
3. Enter the token only in OpenClaw's masked prompt or trusted Control UI.
4. Enable protected egress and restart the Gateway:

   ```bash
   openclaw config set secrets.egressProxy.enabled true --strict-json
   openclaw gateway restart
   ```

5. Run the skill through Gateway-hosted exec.

Protected mode requires Node.js 22.21+ in the 22.x line, 24.5+ in the 24.x
line, or 25+. The proxy gives the process an opaque `NOTION_API_KEY` sentinel;
the real value is substituted only for the allowed HTTPS host.

## 2. Verify v3

Start a fresh process or agent run after saving or changing the secret. Perform
a read-only search for a known page.

Verification is complete when:

- no credential appears in chat, logs, commands, or process arguments;
- the request reaches `api.notion.com`; and
- the expected Notion result is returned.

For OpenClaw protected mode, also confirm that Gateway-hosted exec is used and
the secret is bound only to `api.notion.com`. Never verify by printing
`NOTION_API_KEY` or inspecting the command environment.

## 3. Remove legacy residue

Only after v3 works:

- remove old `--token-file` and `--token-stdin` arguments from scripts,
  automations, and documentation;
- remove obsolete `~/.notion-token` and other token files; and
- remove duplicate plaintext exports when a managed secret injection replaces
  them.

OpenClaw users should also run `openclaw secrets audit --check`.

If the token may have appeared in chat, shell history, logs, process listings,
or source control, rotate it in Notion after migration.

## Rollback

Pin notion-sync v2.5.3 while diagnosing secret injection. Do not pass the token
as a command argument. OpenClaw users should recheck the protected entry's host
binding, egress proxy setting, Gateway restart, execution host, and fresh-run
snapshot before retrying v3.

## Removed credential sources

| v1/v2 source | v3 action |
| --- | --- |
| bare `--token` | already unsupported; use secret-managed `NOTION_API_KEY` |
| `--token-file <path>` | migrate the value into your runtime's secret manager, then remove the file |
| `--token-stdin` | use runtime-managed environment injection |
| automatic `~/.notion-token` | migrate, verify, then securely remove |
| plaintext shell/service env | prefer managed injection; OpenClaw users should use a protected secret |
