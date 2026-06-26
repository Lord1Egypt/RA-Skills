# Installation — Hostinger MCP Server

This skill targets the **official Hostinger MCP** — a local npm server (`hostinger-api-mcp`) that you run on your own machine and connect Claude to over stdio (or HTTP).

> **Source of truth:** [github.com/hostinger/api-mcp-server](https://github.com/hostinger/api-mcp-server). The package name, binaries, flags, and auth below are from that repo; if Hostinger changes them, the repo wins.

**Prerequisites**

- A Hostinger account with an **API token** generated in [hPanel](https://hpanel.hostinger.com).
- **Node.js v24+** (the server requires it).

---

## Step 1 — Install

```bash
npm install -g hostinger-api-mcp
# or
yarn global add hostinger-api-mcp
# or
pnpm add -g hostinger-api-mcp
```

This installs the category binaries (see Step 3) globally on your PATH.

---

## Step 2 — Get the API token

1. Log in to [hPanel](https://hpanel.hostinger.com).
2. Open **API** and generate a token.
3. Copy the token.

The server sends it as a Bearer `Authorization` header. Set it in the `HOSTINGER_API_TOKEN` environment variable.

> The token grants everything the account can do via the API. Treat it like a password — never commit it or print it in responses.

**OAuth alternative (stdio only).** Instead of a token you can authenticate interactively with OAuth 2.0 + PKCE:

```bash
hostinger-api-mcp --login    # opens a browser flow
hostinger-api-mcp --logout   # clears stored credentials
```

Credentials are stored at `~/.config/hostinger-mcp/credentials.json` as a **single central credential per machine**. Because OAuth can store only one credential, it **cannot separate accounts** — for multi-account use, prefer API tokens (see below).

---

## Step 3 — Pick category binaries

The package ships seven binaries. Each exposes a subset of the 127 tools. Connect only the **smallest set** that covers your task — fewer tools keeps Claude's context lean and tool selection accurate.

| Binary | Tools | Use for |
|--------|-------|---------|
| `hostinger-vps-mcp` | 62 | VPS lifecycle, firewalls, snapshots, backups, public keys, post-install scripts |
| `hostinger-hosting-mcp` | 22 | shared hosting websites, subdomains, parked domains, databases, deployments |
| `hostinger-domains-mcp` | 18 | domain registration, forwarding, WHOIS profiles, locks, privacy, nameservers |
| `hostinger-reach-mcp` | 10 | Reach contacts, segments, groups, profiles |
| `hostinger-dns-mcp` | 8 | DNS records and snapshots |
| `hostinger-billing-mcp` | 7 | subscriptions, payment methods, catalog, auto-renewal |
| `hostinger-api-mcp` | all 127 | everything (only when you genuinely need broad coverage) |

---

## Step 4 — Connect Claude Code (stdio)

stdio is the default transport. Add one connection per binary you need. Example for the VPS binary:

```bash
claude mcp add --transport stdio \
  -e HOSTINGER_API_TOKEN=YOUR_TOKEN \
  -s user \
  hostinger-vps hostinger-vps-mcp
```

`-s user` stores it at the user level so it persists across projects. Repeat with a different name + binary for each category you need (e.g. `hostinger-dns hostinger-dns-mcp`).

> Verify the exact env-flag for `claude mcp add` in your Claude Code version with `claude mcp add --help` (it has varied across releases). The canonical config shape is in `.mcp.json.example` at the repo root.

After `claude mcp add`, **restart Claude Code** so the stdio server is launched and its tools load. Verify with `claude mcp list`; remove later with `claude mcp remove hostinger-vps`.

---

## Multi-account — multiple Hostinger accounts

Use **one connection per account**, each with its own `HOSTINGER_API_TOKEN`. Name them `hostinger-<account>` (or `hostinger-<account>-<category>` if you also split by binary) so the tool prefix tells you which account you're on:

```bash
claude mcp add --transport stdio \
  -e HOSTINGER_API_TOKEN=ACCOUNT_A_TOKEN \
  -s user \
  hostinger-clienta-vps hostinger-vps-mcp

claude mcp add --transport stdio \
  -e HOSTINGER_API_TOKEN=ACCOUNT_B_TOKEN \
  -s user \
  hostinger-clientb-vps hostinger-vps-mcp
```

> **Use API tokens for multi-account.** OAuth stores ONE central credential per machine and cannot separate accounts — only env-scoped tokens can. See `.mcp.json.example` in the repo root for the JSON form across accounts.

---

## HTTP mode (optional)

To run over HTTP instead of stdio:

```bash
hostinger-api-mcp --http --host 127.0.0.1 --port 8100
```

The API token (`HOSTINGER_API_TOKEN`) is **required** in HTTP mode. OAuth is **not supported** over HTTP — it works in stdio mode only.

---

## Verify the connection

In Claude, ask:

- **"List my Hostinger VPS"** → calls `VPS_getVirtualMachinesV1`, or
- **"List my domains"** → calls `domains_getDomainListV1`.

That round-trip confirms the install + token.

| Symptom | Meaning | Fix |
|---------|---------|-----|
| No `mcp__hostinger*__*` tools | stdio server not loaded | restart Claude Code |
| `401 Unauthorized` | bad or missing token | re-check `HOSTINGER_API_TOKEN` against the token in hPanel |
| Node engine / version error | Node too old | install Node.js v24+ |

---

## Notes

- API reference: <https://developers.hostinger.com/>
- Tool names throughout this skill use the `Category_actionVn` convention and match `tools-catalog.md`. In Claude they appear as `mcp__<connection-name>__<tool>`. The **live** tools remain the source of truth if Hostinger adds or renames any.
