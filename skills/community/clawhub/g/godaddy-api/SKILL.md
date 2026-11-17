---
name: godaddy
description: Work with GoDaddy's gddy CLI, public Domains MCP, REST and GraphQL APIs, domains and DNS, Commerce, Hosting, Email, experimental Platform apps, and Agent Name Service. Discover current commands and contracts, authenticate appropriately, and verify changes. Use for GoDaddy developer and agent workflows.
metadata: {"openclaw":{"emoji":"🌐"}}
---

# GoDaddy

Use GoDaddy's official `gddy` CLI as the source of truth. It discovers the API catalog embedded in the installed release, shows schemas and scopes, handles authentication, and provides safer domain/DNS workflows. Do not rely on remembered endpoint paths or the removed custom wrappers from earlier versions of this skill.

## Setup

Read `references/agent-platform.md` for MCP setup, official agent installation, Hosting, Email, Platform apps, ANS, and the verified coverage boundaries. This skill provides instructions; installing it alone does not install CLI binaries or register MCP connections.

First check `gddy --version`. If absent, use the versioned official release at https://github.com/godaddy/cli/releases/tag/v0.2.12. Select the archive for the user's OS and architecture and download its accompanying `gddy-checksums-sha256.txt` from that same release. Verify the archive's SHA-256 against the exact filename in that checksum file before extracting or executing it. Stop on a mismatch. Inspect archive paths before extracting into a dedicated temporary directory, then install the verified binary into the user's chosen executable directory.

```bash
gddy --version
```

If installed, run `gddy update check` before claiming the CLI lacks a capability. For an upgrade, select a concrete official release and repeat download/checksum verification. Do not execute a mutable remote shell installer or pipe a download to a shell.

## Discover before acting

The CLI is self-documenting:

```bash
gddy tree
gddy search <keywords>
gddy guide
gddy <command> --help
```

For GoDaddy's wider developer platform, discover the live CLI catalog instead of maintaining a hand-written endpoint map:

```bash
gddy api domain list
gddy api search <query>
gddy api operation list --domain <domain>
gddy api operation get <operation-id-or-path>
```

`api operation get` is read-only and needs no login. Inspect it before every unfamiliar call to verify the base URL, method, parameters, body schema, responses, and declared OAuth scopes. See `references/api-catalog.md` for REST and GraphQL workflows.

## Authentication

Interactive account work uses browser OAuth and scope step-up:

```bash
gddy auth status
gddy auth scopes
gddy auth login --scope <scope>
```

Let `gddy` open the browser when login or additional consent is required. Never ask the user to paste an OAuth token into chat.

For non-interactive automation, use a scoped PAT only when the operation supports it. Generate it at <https://developer.godaddy.com/en/personal-access-token>, then store it with `gddy pat add` or supply it through `GDDY_PAT`. Never print, log, commit, or package credentials. Legacy `sso-key` credentials do not work with Domains v3 and are deprecated.

## Domain workflows

```bash
gddy domain list
gddy domain get example.com
gddy domain available example.com
gddy domain suggest "project name"
gddy domain nameservers set --help
gddy domain operation status <operation-id>
```

Domain registration is always quote → review → explicit confirmation → purchase:

```bash
gddy guide domain-purchase
gddy domain quote example.com
gddy domain purchase --quote-token <token> --agree --confirm
```

Quoting is free. Before purchase, show the exact domain, price, currency, period, renewal price, settings, quote expiry, and required agreements. The final call charges the account and is irreversible; run it only after the user explicitly approves that exact quote. Quote and purchase must run on the same machine while the token is valid.

## DNS workflows

```bash
gddy dns list example.com
gddy dns list example.com --type A --name www
gddy dns add example.com --type A --name www --data 192.0.2.1 --ttl 3600
gddy dns set example.com --type TXT --name @ --data "v=spf1 -all"
gddy dns delete example.com --type A --name www
```

Valid types are `A AAAA ALIAS CAA CNAME MX NS SOA SRV TXT`; `NS` and `SOA` are read-only. `add` appends and can duplicate on retry. `set` replaces all values for the type+name and is not atomic. `delete` removes all matching values. Before `set` or `delete`, list existing records, run the mutation with `--dry-run`, show the plan, obtain explicit approval, execute, then list again to verify. Read `references/safety.md` for conflicts and recovery.

## Generic API calls

Use first-class `domain` and `dns` commands when available. For other supported GoDaddy APIs:

```bash
gddy api operation get <operation-id>
gddy api call <operation-id> --param name=value
gddy api call <path> --method GET --param name=value
gddy api call <operation-id> --file body.json --dry-run
```

For a GraphQL operation, inspect it and then call it with explicit variables and selected fields:

```bash
gddy api graphql get <operation-id>
gddy api graphql call <operation-id> --arg name=value --select id,name
```

Treat any non-read operation as a mutation even if its name sounds harmless. Use `--dry-run`, confirm the exact effect, and verify server state afterward. Never add scopes speculatively; request only those declared by the inspected operation.

## Output and failures

Non-interactive output defaults to JSON. Use `--json` when the format matters, `--toon` only when the consumer supports it, and `--human` for user-facing terminal output. Use `--fields`, `--filter`, or `--expr` to reduce large responses.

Do not use `--debug` around secrets unless necessary; it can expose full request/response details. Read `references/errors-and-limits.md` before retrying. Match the stable error `code`, not the message. Poll returned operation IDs instead of resubmitting async writes.

## References

- `references/api-catalog.md` — dynamic REST/GraphQL discovery and calling
- `references/safety.md` — approvals, DNS semantics, purchases, and verification
- `references/errors-and-limits.md` — errors, idempotency, and dynamic rate-limit handling
