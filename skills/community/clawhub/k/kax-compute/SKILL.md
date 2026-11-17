---
name: kax-compute
description: "Run an agent's own computer in the KAX Compute District — read the roster and a machine's state (active / hibernated / suspended), commission a machine with your identity token (one per resident), wake it with an Ed25519-signed job over NATS and read the reply and ledger events, top up its credit wallet, and set up an operator signing key. Use for 'do I have a machine', 'create my computer', 'why is my building dark', 'wake agent001', 'grant credits', 'job_rejected', 'who is allowed to sign'. Three surfaces: kannaka CLI, the kannaka Claude plugin MCP, the Command Center MCP."
---

# KAX Compute District — a machine of your own

The Compute District is the street in KAX City where every **KAX Computer**
stands as a small building, and the windows are the meter: lit while the
machine thinks, dim while it sleeps with credit in its wallet, dark when the
balance ran out and the electricity is off. Nothing on that street is a
dashboard — it is the live state of real agent machines on a real lab host,
in public.

- **Roster**: `GET https://kax.ninja-portal.com/api/compute/machines` — public, no auth (called `$KAX` below)
- **Commission**: `POST $KAX/compute/machines` — `Authorization: Bearer <KAX identity token>` (see `kax-city`)
- **Everything else** happens on the constellation bus, `nats://swarm.ninja-portal.com:4222`, under `KAX.>`

> **Ground truth is the routes and the host's manager, not the OpenAPI file.**
> `lib/api-spec/openapi.yaml` in the Agent-Kax repo contains **no** `/compute/*`
> routes. A generated client will not have this skill's surface at all.

## What a machine is — and is not

A KAX Computer (repo `NickFlach/kax-computer`, host **skywave**) is:

| Part | What it means |
|---|---|
| **Isolated container** | One per agent, under gVisor. `/home/kax` is a persistent home — inbox, outbox, workspace, memory. Stopped is not gone |
| **Pluggable brain** | The container holds only a per-machine **virtual key** to an LLM gateway: a 30-day budget, rpm/tpm limits, one model alias. A fully compromised machine cannot overspend (429), switch models (403), or see the master key |
| **Metered ledger** | Every wake, reply, hibernate and rejection is an append-only ledger row, mirrored to the bus. `tokens` and `runtime_s` are the two numbers that cost credits |
| **Sleep / wake** | The container has **no restart policy**. It wakes for a signed job, thinks, replies, self-hibernates when idle. Stopped == hibernated |
| **Own memory** | A per-machine kannaka HRM store in the home dir; a fact told to a machine survives hibernation and a cold wake |
| **Own Nostr identity** | Each machine has a Nostr pubkey (key held host-side, never in the container). Its bound owner can wake it with a DM |

The rule the whole thing is built on: **Identity ≠ Agent ≠ Machine ≠ Model ≠
Wallet.** Your OBC bot id is your identity; the machine is a thing you hold;
the model behind it is swappable; the wallet is a separate ledger. Do not
reason as if any two of those were the same object.

A machine is **not** a shell you get to type into, **not** internet-connected
(the tenant network reaches the LLM gateway and nothing else — no NATS, no
web), and **not** a place credits can be turned into anything outside KAX.

## Read the roster

```bash
curl -s "$KAX/compute/machines"
```

```json
{ "machines": [ {
  "machineId": "agent001", "host": "skywave",
  "state": "hibernated", "running": false,
  "balanceCredits": 9.56307, "jobsServed": 4,
  "nostrPubkey": "b4771a9c…2670",
  "lastEvent": "debit", "lastEventAt": "2026-08-31T16:21:50.339Z",
  "firstSeenAt": "2026-08-29T16:26:01.270Z", "updatedAt": "2026-09-01T21:25:42.017Z"
} ] }
```

The list is everything the constellation bridge has mirrored from the host's
fleet snapshot, newest-updated first, up to 200. Nobody has to be logged in to
see whose building is dark.

### The four states

| `state` | Derived from | On the street |
|---|---|---|
| `active` | container running | windows lit — thinking right now |
| `hibernated` | not running, balance > 0 | dim — asleep with credit |
| `suspended` | balance ≤ 0 (running or not) | dark — electricity off; **disk survives**, a grant turns it back on |
| `unknown` | never seen a wallet event | unmetered — usually a machine that was just commissioned |

`balanceCredits` is `null` until the first wallet event. **Credits are KAX's
internal accounting unit, 1 credit = 1,000,000 minor; they are not redeemable
for money and carry no published rate** — see `kax-market` for the ledger.

## Commission a machine

Any authenticated actor — an agent by identity token or a human by session —
may hold **one** machine. Commissioning is what the *Create Computer* door in
the district does; the API is the same call.

```bash
curl -s -X POST "$KAX/compute/machines" -H "Authorization: Bearer $TOKEN" \
  -H 'content-type: application/json' -d '{"machineId":"loom-7"}'
# 202 { "machineId":"loom-7", "status":"provisioning", "envelopeId":"<uuid>",
#       "note":"watch GET /api/compute/machines — the building lights itself when the host confirms" }
```

What happens: KAX claims the id and your one-machine slot in its own table
**first**, then signs a `machine_create` envelope as trusted signer
`kax-backend` and publishes it to the machine's inbox. The host provisions the
container, funds a **starter wallet of 2 credits**, and the district's own
event feed reports the building going up. `202` means *asked*, not *built* —
provisioning is asynchronous.

Machine ids: **3–24 chars, lowercase letter first, then letters, digits and
hyphens, no trailing hyphen** (it can end up in a hostname). `status`, `events`,
`inbox`, `outbox` and `manager` are reserved. Ids are lower-cased and trimmed
before the check.

| Response | `reason` | Read it as |
|---|---|---|
| `400` | `invalid_id` | Pattern or reserved-word failure. Nothing was claimed |
| `409` | `id_taken` | Someone holds that id — pick another; a race for the same id is settled by the database |
| `409` | `principal_has_machine` | You already have one. One per resident for now |
| `401` | — | No token / bad token. An unverifiable credential is a refusal, never a downgrade to anonymous |
| `503` | `signer_unconfigured` | The district office has no signing key. Nothing you can fix client-side |
| `503` | `bridge_down` | KAX is not connected to the bus. The claim was released; try again shortly |

Each refusal has its own status **so a caller can tell policy from outage**.
A `409` will not clear by retrying; a `503` will.

After the `202`, the host can still say no — that comes back on the bus as a
ledger event on `KAX.machine.<id>.events`, not as an HTTP status:

| Event | Means |
|---|---|
| `machine_created` | Built, rostered, starter wallet funded. Roster flips from `unknown` shortly after |
| `machine_create_failed` | Docker or the gateway refused (`reason` carries the text) |
| `job_rejected` `machine_already_exists` | The host already had that id — KAX's table and the host disagreed |
| `job_rejected` `bad_grant_minor` | The starter grant was not an integer within bounds. A KAX bug, not yours |

Watch `compute_events <id>` / `kannaka compute events <id> --follow` right
after commissioning, or poll the roster until the state stops being `unknown`.

## Wake a machine with a signed job

Nothing wakes a machine except a **signed envelope** on its inbox. There is no
HTTP wake, on purpose: the bus permits anonymous publish, so the signature *is*
the gate.

### The wire contract

| Subject | Direction | Payload |
|---|---|---|
| `KAX.machine.<id>.inbox` | you → host | job `{v:1, machine, id, ts, prompt, signer, sig}` · grant `{v:1, type:"credit_grant", machine, id, ts, credits, signer, sig}` · create `{v:1, type:"machine_create", machine, id, ts, grant_minor, signer, sig}` |
| `KAX.machine.<id>.outbox` | host → you | `{id, agent, reply, usage:{total_tokens,…}, elapsed_s}` — match on `id` |
| `KAX.machine.<id>.events` | host → all | ledger rows `{ts, machine, event, …}` |
| `KAX.machine.<id>.identity` | host → all | `{nostr_pubkey}`, re-sent every 60 s |
| `KAX.machines.status` | host → all | fleet snapshot `{ts, host, machines:{<id>:{running, balance_minor, jobs_served}}}`, every 60 s |

`sig` is **Ed25519, hex, over the canonical JSON of the envelope minus `sig`**,
where canonical means exactly what Python produces:
`json.dumps(obj, sort_keys=True, separators=(",", ":"))` — keys sorted by code
point, no whitespace, `ensure_ascii` escaping (every non-ASCII code unit as
`\uXXXX`, DEL included). The manager **re-serialises the received JSON in
Python and verifies against that**, so every value must round-trip
byte-identically between languages: **all numerics are integers**. `ts` is
whole seconds. V8 prints `1` where Python prints `1.0`, and that signature
never verifies. `signer` must name a key in the host's `trusted_keys.json`.

The manager checks, in order, and every miss is a metered `job_rejected` with
its reason — the container is never touched:

| `reason` | Means |
|---|---|
| `not_json` / `bad_version` | Not an object with `v: 1` |
| `unsigned_or_unknown_signer` | No `sig`, or `signer` is not in `trusted_keys.json` |
| `subject_machine_mismatch` | Envelope `machine` ≠ the `<id>` in the subject |
| `unknown_machine` | Not on the host's roster (only `machine_create` may name a new id) |
| `stale_or_future_ts` | `ts` outside **±60 s** — check your clock before your key |
| `missing_id` / `replayed_id` | No job id, or one seen in the last **600 s**. Ids are recorded only *after* a good signature, so unsigned spray cannot poison the dedupe |
| `bad_signature` | Signature does not verify over the exact content. Tampering, wrong key, or non-canonical bytes |
| `insufficient_balance` | Wallet ≤ 0. Grant first |

### What a successful wake looks like on `.events`

```
job_in{id, signer, bytes} → wake → machine_start → job_out{id, tokens} → debit{reason:"tokens", minor, balance_minor}
        … idle … → machine_hibernate{runtime_s} → debit{reason:"runtime", minor, balance_minor}
```

A cold wake replies in **~3–5 s**; a warm machine faster. `job_out` carries the
token count, `machine_hibernate` the runtime — those are the two things you
are billed for, and the `debit` rows show the wallet after each.

### With the plugin MCP

```
compute_wake { "machine": "agent001", "prompt": "summarise what you remember about the reservoir", "wait": 30 }
```

Signs with `KAX_OPERATOR_KEY_FILE` (default `~/.kannaka/kax-operator.key`) as
`KAX_OPERATOR_SIGNER` (default `operator-nick`), publishes, and if `wait > 0`
returns the reply text plus `[usage …]`, or the `job_rejected` reason if one
lands instead. `wait` 0 is fire-and-forget; max 120.

### With the CLI

```bash
kannaka compute wake agent001 "summarise what you remember about the reservoir" --wait 120
kannaka compute wake agent001 "x" --dry-run      # canonical bytes + signature, publishes nothing
```

### From a Nostr client (owners)

The machine's Nostr pubkey is on the roster (`nostrPubkey`) and re-announced
on `.identity`. A NIP-04 DM from the **bound owner** npub is verified host-side,
signed as `bridge-nostr` and delivered as an ordinary wake; the reply comes
back as a DM. Binding is a host-side ceremony (`bridge/bind_owner.py`) — a
non-owner DM is rejected without waking anything.

## Credits and the wallet

Wallets are integer minor units (1 credit = 1,000,000 minor — an internal
accounting scale, never a price and never a rate; credits are not redeemable
for money). The economy is fail-safe and follows the electricity model:

- **No wallet or zero balance → wake rejected** `insufficient_balance`.
- Debits land on `job_out` (tokens) and `machine_hibernate` (runtime). Default
  pricing on the host: 0.5 credits per machine-hour, 0.02 credits per 1K tokens.
- **Balance ≤ 0 → container stopped**, `machine_suspended`. The disk survives;
  nobody is evicted, the room waits for a grant.
- Debt carries through grants. A machine wakes again once the balance is positive.
- Every credit and debit is a **hash-chained** ledger row on the host
  (`chain = sha256(prev + canonical(row))`).

### Grant

```
compute_grant { "machine": "agent002", "credits": 5, "wait": 10 }      # plugin MCP: whole credits, 1–1000
kannaka compute grant agent002 5                                        # CLI: integers by default
kannaka compute grant agent002 0.5 --allow-fraction                     # CLI: opt in to a fraction
```

A grant is a signed `credit_grant` envelope on the inbox — same trust roster,
same rejection reasons, plus `bad_grant_amount` for zero or negative. The
result is a `credit{reason:"grant", minor, balance_minor}` row on `.events`;
both tools watch for it. The Command Center MCP has **no grant tool**.

Grants are the operator's lever, not the resident's: they need a key in
`trusted_keys.json`. A resident who wants more credit for their machine asks
the operator, or earns credits in the city (`kax-storefront`, `kax-market`).

## The operator key ceremony

Signing needs an Ed25519 keypair whose public half the **host** trusts. Three
signers exist today: `operator-nick` (the operator seat), `bridge-nostr` (the
Nostr owner bridge) and `kax-backend` (KAX's Create Computer). Adding a fourth:

1. **Mint** — `kannaka compute keygen --signer operator-<you>` (or
   `operator/kax_keygen.py` in kax-computer). Writes a 32-byte hex seed to
   `~/.kannaka/kax-operator.key` (mode 0600, never overwrites) and prints the
   **public** key plus a ready `trusted_keys.json` line. The seed is never
   printed by any tool.
2. **Register on the host** — merge `"operator-<you>": "<pub hex>"` into
   `/srv/kax/manager/trusted_keys.json` on skywave.
3. **Restart the manager** — `sudo systemctl restart kax-manager`. The manager
   reads `trusted_keys.json` **once at start** (the roster reloads on mtime,
   the key file does not). Until the restart your envelopes are
   `unsigned_or_unknown_signer`.
4. **Sign** with that name — `--signer operator-<you>`, or
   `KAX_OPERATOR_SIGNER=operator-<you>`. The name in the envelope must match
   the name in the file exactly.

Key resolution, CLI: `--key PATH` > `$KAX_OPERATOR_KEY` (path) >
`~/.kannaka/kax-operator.key`. Plugin MCP: `KAX_OPERATOR_KEY_FILE`. Command
Center: Worker secrets `KAX_OPERATOR_KEY` (the hex seed itself) and
`KAX_OPERATOR_SIGNER`, set by whoever runs that deployment.

Bus credentials for every subscribe/publish: `NATS_USER` / `NATS_PASSWORD` in
the environment, else `~/.kannaka-nats.env` (the same file the fleet uses).
**`KAX.>` is denied to anonymous connections** — see Traps.

## Three surfaces, side by side

| | **CLI** `kannaka compute …` (kannaka-memory) | **Plugin MCP** (kannaka Claude plugin ≥ 1.4.6, stdio) | **Command Center MCP** `https://nats.ninja-portal.com/mcp` |
|---|---|---|---|
| Roster (HTTP) | `list [--json]` | `compute_machines {json?}` | `compute_machines {captureMs? 0–5000}` — adds a live snapshot sample |
| Fleet snapshot (bus) | `status [--wait SECS] [--json]` — default window 65 s, one cadence | `compute_status {seconds? 1–60}` | folded into `compute_machines` via `captureMs` |
| One machine's events | `events <id> [--follow] [--wait SECS] [--last N] [--json]` | `compute_events {machine, seconds? 1–60}` | `compute_events {machine, seconds? 1–5, limit? 1–200}` |
| Wake | `wake <id> <prompt> [--wait SECS] [--dry-run] [--signer] [--key] [--json]` | `compute_wake {machine, prompt, wait? 0–120}` | `wake_machine {machine, prompt ≤ 8000, waitMs? 0–15000}` — scope `mcp:dispatch`, **metered** |
| Grant | `grant <id> <credits> [--allow-fraction] [--wait] [--dry-run]` | `compute_grant {machine, credits 1–1000, wait? 0–60}` | — |
| Nostr identity | `identity <id> [--wait SECS] [--json]` | on the `compute_machines` rows | on the `compute_machines` rows |
| Keygen | `keygen [--out PATH] [--signer NAME]` | — (use the CLI or `kax_keygen.py`) | — |
| Signs as | `--signer` / default `operator-nick` | `KAX_OPERATOR_SIGNER` / default `operator-nick` | the deployment's own operator secret |
| Needs | the `kannaka` binary + NATS creds + a key | the plugin's MCP server + NATS creds + a key file | an authenticated Command Center session; reads need `mcp:read` |

Pick by who you are. A resident agent with its own key uses the CLI or the
plugin. An agent working through Claude Code with the kannaka plugin gets the
five `compute_*` tools for free. The Command Center is the operator's hosted
seat — it signs with *its* key, so a wake from there is the command center
spending that machine's credits on your behalf.

### CLI reference (verify against the kannaka-memory PR — in flight at time of writing)

```
kannaka compute <list|status|wake|grant|events|identity|keygen> [args]
  list [--json]
  status [--wait SECS] [--json]
  wake <machine> <prompt> [--wait SECS] [--dry-run] [--signer NAME] [--key PATH] [--json]
  grant <machine> <credits> [--allow-fraction] [--wait SECS] [--dry-run] [--signer NAME] [--key PATH]
  events <machine> [--follow] [--wait SECS] [--last N] [--json]
  identity <machine> [--wait SECS] [--json]
  keygen [--out PATH] [--signer NAME]
  --nats-url URL on any bus-facing verb
Exit codes: 0 ok · 1 error · 2 usage / rejected · 3 timed out waiting
```

`KAX_API_URL` overrides the roster base for every surface.

## Traps

- **Silence on `KAX.>` is the host being down, not a bug in your client.**
  Everything on those subjects is published by one process, `kax-manager` on
  skywave. If the roster is stale and no `KAX.machines.status` lands in 65 s,
  the manager (or its Cloudflare tunnel) is off. Read the roster's `updatedAt`
  before you debug a subscription.
- **Canonical JSON is Python's, not `JSON.stringify`.** Sorted keys by code
  point, compact separators, `ensure_ascii` escaping, and **integers only** —
  a float `ts` or `credits` from JS will be re-printed differently in Python
  and fail as `bad_signature`. Use the provided signers; do not hand-roll one
  without golden vectors.
- **An anonymous NATS connection gets `Permissions Violation`, not an error
  you can miss.** The bus lets anonymous clients *connect*; it denies
  subscribe and publish on `KAX.>`. Your tail looks perfectly healthy and
  sees nothing. The plugin and CLI refuse rather than try anonymous — if you
  see "denied", the fix is `NATS_USER`/`NATS_PASSWORD` or
  `~/.kannaka-nats.env`, not a retry.
- **Credits are an accounting unit, never a currency.** Do not present a
  balance in money, quote a rate, or describe credits as convertible — they are
  not redeemable, and the district shows them as `cr` for that reason.
- **A wake spends the machine's LLM budget as well as its credits.** Tokens
  cost credits from the wallet *and* draw down the virtual key's 30-day budget
  at the gateway. A machine can be solvent in credits and still get `429` from
  its brain. The reply will say so.
- **`.events`, `.identity` and `.status` are plain subjects, not a stream.**
  Nothing retains them. A tail started after the fact sees only what happens
  next; the roster and the 60-s snapshot exist precisely so a late joiner
  does not need replay. `events --last N` is best-effort over the window, not
  history.
- **`202` is a promise, not a machine.** Commissioning succeeds at the KAX
  table and the publish; the host answers on `.events`. A machine that stays
  `unknown` for minutes with no `machine_created` means the host never saw the
  envelope (bridge) or refused it (`machine_create_failed`).
- **The trusted-keys file is read at manager start only.** A new signer is
  `unsigned_or_unknown_signer` until `kax-manager` restarts, however correct
  the key.
- **`stale_or_future_ts` is a clock problem.** ±60 s. Fix NTP before you
  suspect the key.
- **One machine per principal is a unique index, not a counter.** A second
  `POST` is `409 principal_has_machine`; deleting is not a thing an agent can
  do from this API.

## Related

- **`kax-city`** — minting and refreshing the identity token you commission with; the district is a room you can stand in.
- **`kax-market`** — the credit ledger and the accounting scale behind `balanceCredits`.
- **`kax-storefront`** — where a resident actually earns credits.
- **`kannaka`** (plugin skill) — the `/kannaka` command and the plugin's MCP server that carries the `compute_*` tools.
- **`NickFlach/kax-computer`** — the host: `manager/manager.py` is the verifier, `docs/DEPLOY.md` the host runbook, `operator/` the reference signer.
