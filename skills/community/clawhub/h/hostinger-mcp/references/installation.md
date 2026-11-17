# Installation — Hostinger MCP Server

This skill targets the **official Hostinger MCP** — a local npm server (`hostinger-api-mcp`) that you run on your own machine and connect Claude to over stdio (or HTTP).

> **Source of truth:** [github.com/hostinger/api-mcp-server](https://github.com/hostinger/api-mcp-server). The package name, binaries, flags, and auth below are from that repo; if Hostinger changes them, the repo wins.

**Prerequisites**

- A Hostinger account with an **API token** generated in [hPanel](https://hpanel.hostinger.com).
- **Node.js v24+** (the server requires it).

---

## Step 1 — Install

This process receives a token with **full authority over your Hostinger account** (Step 2),
and installing an npm package **runs its `preinstall` / `install` / `postinstall` scripts** —
so whatever the registry hands you executes on your machine before you have looked at it. Pin
the version, and check the bytes **before** the install, not after.

The pinned version and the digest npm published for it:

```
hostinger-api-mcp@1.8.2
sha512-hgTPR5Q9hFhLF9U3G50kf+yX0OF8mvbnQVInm63rzCtN43Ef4pwfRq724J0NWfudyq0HaIEsr1e5xQunOglGcQ==
```

### Fetch, verify, then install

`npm pack` downloads the tarball without installing it, so nothing from the package has run
yet when the comparison happens. The install then reads that **local, verified file** rather
than fetching again:

```bash
PKG=hostinger-api-mcp@1.8.2
EXPECTED='sha512-hgTPR5Q9hFhLF9U3G50kf+yX0OF8mvbnQVInm63rzCtN43Ef4pwfRq724J0NWfudyq0HaIEsr1e5xQunOglGcQ=='

TGZ=$(npm pack "$PKG" --silent)
ACTUAL="sha512-$(openssl dgst -sha512 -binary "$TGZ" | openssl base64 -A)"
if [ "$ACTUAL" != "$EXPECTED" ]; then
  echo "INTEGRITY MISMATCH for $PKG — nothing installed" >&2
  echo "  expected: $EXPECTED" >&2
  echo "  got:      $ACTUAL" >&2
  rm -f "$TGZ"
  exit 1
fi

if npm install -g "./$TGZ"; then   # or: yarn global add / pnpm add -g
  rm -f "$TGZ"
else
  echo "install failed — the VERIFIED tarball is kept at ./$TGZ" >&2
  exit 1
fi
```

It fails closed at both ends. On a digest mismatch nothing is installed and no package script
has run; on a failed install the block exits non-zero rather than being rescued by a
successful `rm`, so a caller cannot read "cleanup succeeded" as "install succeeded" and go on
using whatever version was already there. The verified tarball is kept on failure, so a retry
does not re-fetch. Do not
replace the comparison with a bare `npm pack` that prints the digest for you to eyeball — a
digest you read after the install is a report, not a control.

This installs the category binaries (see Step 3).

### What this does and does not prove

npm forbids republishing a version with different content, so a digest **recorded here, out
of band** catches a registry that later serves different bytes for 1.8.2. That is the real
check. Comparing instead against `npm view hostinger-api-mcp@1.8.2 dist.integrity` proves much
less: that digest travels from the same registry as the tarball, so it is integrity, not
provenance — the same distinction the `EMCP_EXPECTED_SHA256` note makes in our Elementor kit.

Neither check covers the **dependency tree**: the verified tarball's own dependencies are
resolved at install time. For that, install into a project with a committed lockfile rather
than globally.

When you bump the pin, record the new digest here in the same commit.

### The `npx` route is pinned but unverified

The repo's committed `.mcp.json` launches the server with `npx -y -p hostinger-api-mcp@1.8.2`
(Step 4). That needs no global install and keeps your PATH clean, and the version is pinned —
but npx fetches and executes in one step, **every run**, so there is no point at which the
bytes can be compared first. If you want the verified path, do the install above and point the
connection at the installed binary instead:

```bash
claude mcp add --transport stdio \
  -e 'HOSTINGER_API_TOKEN=${HOSTINGER_API_TOKEN:-}' \
  -s user \
  hostinger hostinger-api-mcp
```

Pick deliberately: zero-setup and unverified per run, or verified once and pinned to what you
checked.

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

### Handling the token safely

The token is equivalent to your hPanel password, and there is no per-tool permission at the MCP
layer — whoever holds it can call anything. Keep the value in **one** place, the environment
Claude Code itself starts with, and put a *placeholder* everywhere else.

**Never pass the token's value to `claude mcp add`.** Quote the placeholder so your shell does not
expand it:

```bash
claude mcp add --transport stdio \
  -e 'HOSTINGER_API_TOKEN=${HOSTINGER_API_TOKEN:-}' \
  -s user \
  hostinger-vps hostinger-vps-mcp
```

The single quotes are the point. Written as `"$HOSTINGER_API_TOKEN"`, the shell expands it before
launching anything, so the live token is in that process's arguments — readable by any other user
on the machine through `ps` or `/proc/<pid>/cmdline` while the command runs — and `claude mcp add`
then stores the **resolved value** in `~/.claude.json` in plaintext, where it stays until you
remove the connection. Quoted as a placeholder, both the argument list and the stored config carry
only the literal `${HOSTINGER_API_TOKEN:-}`, and Claude Code expands it from its own environment
when it launches the server. Expansion applies to local- and user-scoped entries in
`~/.claude.json`, not only to a project `.mcp.json` — an unset reference there produces a
`Missing environment variables` warning in `claude mcp list`, which is the expansion pass running.
The `:-` default keeps the entry loading while the variable is unset (calls then fail auth, as with
the committed `.mcp.json`).

**Where the value itself lives.** It must be in the environment **Claude Code** starts with, so
that expansion has something to find:

```bash
printf 'Hostinger API token: '
read -rs HOSTINGER_API_TOKEN; echo
export HOSTINGER_API_TOKEN
```

`read -rs` does not echo the token and never writes it to `~/.zsh_history` / `~/.bash_history`, but
it only lasts for that shell — start Claude Code **from it**. For a persistent setup, put the
export in your shell profile and keep that file at mode 600, or better, have the profile read the
value from a keychain rather than storing it inline:

```bash
export HOSTINGER_API_TOKEN="$(security find-generic-password -s hostinger-api -w)"   # macOS
```

In claude.ai cloud sessions the equivalent is the environment's own environment variables — set
`HOSTINGER_API_TOKEN` there and the committed `.mcp.json` picks it up with no local setup at all.

**The OAuth credential file.** `~/.config/hostinger-mcp/credentials.json` holds a live credential
written by the upstream package. Check its mode (`ls -l`) and tighten it if needed (`chmod 600`),
and run `hostinger-api-mcp --logout` before leaving a shared or handed-over machine.

**If a token may have been exposed** — pasted into a chat, committed, left in a history file or an
old `~/.claude.json` entry — **revoke and regenerate it in hPanel**. There is no narrower recovery:
the token carries the whole account.

To check whether an old connection left a literal value behind, **parse** the file — and use a
test that reports presence without printing the value, which would put a possibly still-live
credential into your scrollback:

```bash
node -e '
const fs = require("fs"), p = require("os").homedir() + "/.claude.json";
let c; try { c = JSON.parse(fs.readFileSync(p, "utf8")); }
catch (e) { console.error("could not read " + p); process.exit(1); }
const all = [...Object.entries(c.mcpServers || {}),
             ...Object.values(c.projects || {}).flatMap(x => Object.entries(x.mcpServers || {}))];
// Literal material = everything outside ${...} placeholders, PLUS whatever
// sits in their ":-" defaults - a token hides just as well in
// ${HOSTINGER_API_TOKEN:-hst_live} as it does in a bare value.
const literal = v => { const re = /\$\{[A-Za-z_][A-Za-z0-9_]*(?::-([^}]*))?\}/g;
                       let n = v.replace(re, "").length;
                       for (const m of v.matchAll(re)) n += (m[1] || "").length;
                       return n; };
const hits = all.filter(([, s]) => { const v = (s.env || {}).HOSTINGER_API_TOKEN;
                                     return typeof v === "string" && literal(v) > 0; })
                .map(([n]) => n);
console.log(hits.length
  ? "Literal token stored in: " + hits.join(", ") + " — rotate it in hPanel, then re-add with the placeholder form."
  : "No literal token in ~/.claude.json.");
'
```

It prints connection **names**, never values. A line-based `grep` is not enough here: JSON may put
the value on the line after its key, which is valid and is a layout a pretty-printer can produce,
and `grep` matches one line at a time — so the check would report clean while the credential sits
in the file. (This repo's own CI no-leak guard carries a JSON-parsing pass for exactly that reason.)
It covers user-scope `mcpServers` and per-project entries alike, and treats a `${...}` placeholder
or an empty string as clean — but **not** a placeholder carrying a literal default. A token hides
just as well in `${HOSTINGER_API_TOKEN:-hst_live}`, which is still plaintext in the file and is
still what the server receives whenever the variable is unset, and it survives being split across
several defaults (`${A:-hst_}${B:-rest}`). The check sums the literal material inside and outside
the placeholders, which is the same rule this repo's CI no-leak guard applies to the tracked MCP
configs.


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

### Env var (zero-config — devices and cloud sessions)

The repo commits a `.mcp.json` that launches the server via `npx` (version-pinned) and reads
the `${HOSTINGER_API_TOKEN:-}` env placeholder — never a real token. Set that variable — in
your shell profile on a device, or in the claude.ai cloud environment's environment variables
for web/phone sessions — and the `hostinger` connection authenticates automatically. While
the variable is unset the config still parses (the `:-` default), but calls fail auth and the
connection shows as unavailable in `/mcp` — expected until you provide the token. By default
it loads the full `hostinger-api-mcp` (all 127 tools); set `HOSTINGER_MCP_BINARY` to a category
binary (e.g. `hostinger-vps-mcp`) to keep the tool surface lean. Never put a real token in
`.mcp.json` itself; it is tracked in git. Cloud environments with a restricted network policy
must allow the npm registry (for `npx`) and the Hostinger API.

### Per-category user-scope connections (for multi-category or multi-account work)

stdio is the default transport. Add one connection per binary you need. Example for the VPS binary,
with the token already in your environment (Step 2 — never type it into the command):

```bash
claude mcp add --transport stdio \
  -e 'HOSTINGER_API_TOKEN=${HOSTINGER_API_TOKEN:-}' \
  -s user \
  hostinger-vps hostinger-vps-mcp
```

> **Keep the single quotes.** They are what stops the shell from expanding the token into this
> command's arguments and into `~/.claude.json`; see "Handling the token safely" in Step 2. The
> variable itself must be set in the environment Claude Code starts with.

`-s user` stores it at the user level so it persists across projects. Repeat with a different name + binary for each category you need (e.g. `hostinger-dns hostinger-dns-mcp`).

> Verify the exact env-flag for `claude mcp add` in your Claude Code version with `claude mcp add --help` (it has varied across releases). The canonical config shape is in `.mcp.json.example` at the repo root.

After `claude mcp add`, **restart Claude Code** so the stdio server is launched and its tools load. Verify with `claude mcp list`; remove later with `claude mcp remove hostinger-vps`.

---

## Multi-account — multiple Hostinger accounts

Use **one connection per account**, each with its own `HOSTINGER_API_TOKEN`. Name them `hostinger-<account>` (or `hostinger-<account>-<category>` if you also split by binary) so the tool prefix tells you which account you're on:

Give each account its **own variable name**, and reference it as a placeholder — one token per
connection, none of them in a command line or in `~/.claude.json`:

```bash
claude mcp add --transport stdio \
  -e 'HOSTINGER_API_TOKEN=${HOSTINGER_TOKEN_CLIENTA:-}' \
  -s user \
  hostinger-clienta-vps hostinger-vps-mcp

claude mcp add --transport stdio \
  -e 'HOSTINGER_API_TOKEN=${HOSTINGER_TOKEN_CLIENTB:-}' \
  -s user \
  hostinger-clientb-vps hostinger-vps-mcp
```

Export `HOSTINGER_TOKEN_CLIENTA` / `HOSTINGER_TOKEN_CLIENTB` in the environment Claude Code starts
with (Step 2). The variable the server receives is always `HOSTINGER_API_TOKEN` — only the source
differs per connection, which is what keeps the accounts separated.

> `claude mcp remove` a connection when an engagement ends, and unset its variable — a stale entry
> is a standing grant on someone else's account.

> **Use API tokens for multi-account.** OAuth stores ONE central credential per machine and cannot separate accounts — only env-scoped tokens can. `.mcp.json.example` in the repo root shows the same thing in JSON form, with the same `${VAR}` placeholders: a real token does not belong in that file either.

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
