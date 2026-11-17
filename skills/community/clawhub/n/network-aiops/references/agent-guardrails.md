# Agent guardrails — running network-aiops with a smaller / local model

If you drive these tools with a local model (Llama, Qwen, Mistral … via Goose,
Ollama, LM Studio, or any OpenAI-compatible runtime), you will get noticeably
better results with a short system prompt. This page gives you one, and — more
importantly — tells you which guardrails you **no longer need to write**, because
the tool now enforces them itself.

The distinction matters. A guardrail in a prompt is a request. A guardrail in the
harness is a guarantee. Anything below that we could move into the harness, we did.

Network gear raises the stakes: a bad merge on a core switch takes the management
plane with it, and the model cannot SSH back in to fix what it broke.

## What the tool now enforces — do not waste prompt budget on these

| You might be tempted to prompt | Why you don't need to |
|---|---|
| "Don't invent a value when a field is missing" | A field the driver did not return comes back as `null`, never as `""`. This is the norm, not the exception, on a multi-vendor fleet: `serial_number`, `model`, an interface `description`, an LLDP neighbour's `hostname` are all optional and driver-dependent. Absent and empty are distinguishable in the payload. |
| "Tell me if the output was cut off" | The NetBox listings return `{"devices": [...], "returned": N, "limit": L, "truncated": true/false}` (and `{"interfaces": ...}` likewise). Truncation is measured — one extra record is fetched — not guessed from a length coincidence. |
| "Preserve the ordering / tell me what's most urgent" | `interface_health_rca` and `bgp_neighbor_rca` findings carry an explicit 1-based `rank`, worst-first, and each cites the measured number that tripped it (`rx_errors+tx_errors = 412 >= 100`). Priority is in the payload, not implied by list position. |
| "Show me the diff before you commit anything" | `config_diff` is a real dry run: it stages a candidate, returns `compare_config()` output, then always discards. Nothing is committed, and the response carries `"committed": false`. |
| "Confirm before anything destructive" | The CLI write paths (`config merge`/`replace`/`rollback`) require a double confirmation, and every write supports `--dry-run` / `dry_run=True` to preview first. `config_replace` is `high` risk, carried into the audit row as a `review` tier so it stands out in the trail. |
| "Keep a copy of the old config so we can go back" | `config_merge` and `config_replace` read the running config **before** touching the device and return it as `backup`, and the harness records an undo descriptor that restores it via `config_replace`. The before-state is captured, not reconstructed. |
| "Log what you did" | Every governed call is audited to `~/.network-aiops/audit.db` regardless of what the model says it did. |
| "Never show me passwords or SNMP communities" | `get_users` returns `has_password` (a boolean) instead of the hash; `get_snmp_information` returns `community_count` instead of the community strings. The secrets are not in the payload to leak. |
| "Don't crash if this platform doesn't support that command" | A getter a driver does not implement returns a teaching error naming the driver ("not supported by the `iosxr` NAPALM driver"), not a traceback. |

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.
Recommended setup for a local model (adapt it to your agent client):

```text
You operate multi-vendor network devices (Cisco IOS / NX-OS / IOS-XR, Arista EOS,
Juniper Junos) and an optional NetBox source of truth through the network-aiops
MCP tools.

TOOL USE
- Before answering any question about the current state of the network, you MUST
  call a tool. Never answer from memory or assumption.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- If a tool call fails, report the real error verbatim. Never fill the gap with
  a plausible-sounding answer. "Not supported by the <driver> driver" means the
  platform lacks that getter — say so; do not substitute a different getter and
  present its output as the answer to the original question.

READING RESULTS
- Read the whole result before concluding. If a result contains a "truncated"
  field that is true, say so and re-run with a higher limit instead of treating
  the partial result as complete.
- A null field means the driver did not return that value. Report it as "not
  available" — never infer it.
- Report identifiers EXACTLY as returned. Interface naming is vendor-specific:
  GigabitEthernet0/1, Ethernet1, ge-0/0/0 and Te0/0/0/1 are literal device
  strings, not styles to normalise. Never abbreviate Gi0/1 to 0/1, never expand
  Et1 to Ethernet1, never convert between vendors' forms.
- Do not normalise, translate, or prettify VRF names, BGP connection states,
  route protocols, or VLAN names either.
- When an RCA result has findings, work in "rank" order and cite the measured
  number in each finding's "detail".

CONFIG CHANGES
- Always call config_diff first and show the operator the diff. Only after they
  approve the exact diff may you call config_merge or config_replace.
- config_merge is additive: it adds and modifies lines, it does not remove what
  you left out. config_replace makes the device match the supplied config in
  full — anything absent from your text is REMOVED, including the management
  interface, AAA, and your own access. Never pass a partial config to
  config_replace.
- Never generate a full replacement config from scratch. Start from the output
  of config_backup and edit that — but call it with `include_secrets=True`
  for that purpose, or the `<redacted>` placeholders become literal
  passwords on the device. Better still, take the backup with the CLI's
  `-o <path>` and edit the file.
- config_rollback reverts the last commit only, and rollback depth is
  device-dependent — treat it as a single shot, not an undo history.
- Never change more than one device per confirmed request.

NETBOX VS THE DEVICE
- NetBox describes intended state; the device reports actual state. When they
  disagree, that IS the finding. Report both values side by side and label which
  came from which. Do not silently reconcile them, and never edit a device to
  match NetBox without the operator explicitly asking for exactly that.

SCOPE
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- Do not assert a link, routing, or hardware problem unless a tool result
  supports it.
- Do not add generic advice that does not follow from the tool output.
- Do not confuse a target name (the entry in config.yaml) with the device's own
  hostname, an interface name with a VLAN id, or a BGP neighbor IP with an
  interface address.
```

## Recommended setup for a local model

```bash
network-aiops doctor
```

Authorization is not this tool's job — decide it via the account or the agent's
prompt, not a switch in the skill. The safest posture while you build trust is to
connect with a **device account that has read-only privileges** (and a read-only
NetBox API token): a write then fails at the device itself, the place that
actually owns the permission, no matter what the model attempts. When you are
ready to allow config changes, connect with an account that can write.

`NETWORK_AUDIT_APPROVED_BY` / `NETWORK_AUDIT_RATIONALE` are optional annotations —
they record who asked for a change and why on the audit row, but they never block
a call:

```bash
export NETWORK_AUDIT_APPROVED_BY="your.name@example.com"
export NETWORK_AUDIT_RATIONALE="change window CHG-1234, 2026-07-20"
```

## Platform notes worth knowing

**Merge vs replace is the single most dangerous distinction here.** NAPALM stages
a *candidate* config and `compare_config()` shows the diff before anything is
applied. `load_merge_candidate` (behind `config_merge`) is additive. Whereas
`load_replace_candidate` (behind `config_replace`) makes the running config
*equal* your text — every line you omitted is removed. On Junos this is a
`load override`; on IOS-XR a `commit replace`; on EOS/IOS the driver synthesises
it. A model that treats replace like merge will drop the management VRF and lock
you out. `config_replace` is `high` risk — recorded as a `review` tier in the
audit trail for exactly this reason — and both writes return the pre-change
running config as `backup`.

**The commit / rollback path is device-dependent.** `commit_config()` applies the
candidate; `config_rollback` calls NAPALM's `rollback()`, which reverts the last
commit. Some platforms keep exactly one rollback point (IOS's archive-based
implementation is not a rollback stack the way Junos's `rollback 1..49` is).
Treat rollback as one shot. The durable recovery path is the recorded undo
descriptor — it replays the captured `backup` through `config_replace`, which
means the target must support config replace for the undo to apply.

**Interface names are literal, per-vendor strings.** `GigabitEthernet0/1` (IOS),
`Ethernet1` (EOS), `ge-0/0/0` (Junos), `TenGigE0/0/0/1` (IOS-XR). NAPALM
normalises the *schema*, not the *names*. Every tool returns names exactly as the
device reports them, and every tool that takes one expects the same form back. A
model that "helpfully" tidies `GigabitEthernet0/1` into `Gi0/1` will produce a
config line the device rejects, or worse, one that silently creates a different
interface.

**NetBox and the device will disagree, and that is signal.** `netbox_device_interfaces`
returns the intended inventory; `get_interfaces` returns what is actually
configured and up. Drift is the whole point of asking both. Report both sides
with their sources named rather than picking a winner — the correct fix is
sometimes to update NetBox, not the switch, and that is an operator's call.
Note that the NetBox listings are paginated: check `truncated` before calling any
interface "missing from source of truth".

**Not every getter exists on every platform.** `get_vlans`, `get_optics`,
`get_environment` and `get_network_instances` in particular vary widely. An
unsupported getter raises a teaching error naming the driver; that is a real
answer ("this platform can't report it"), not a failure to route around.

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **Multi-tool workflows time out or drift.** Prefer `interface_health_rca` and
  `bgp_neighbor_rca` — they collect the interfaces, counters and neighbor state
  and correlate them inside one call, so the model does not have to chain reads
  and keep interface names straight across turns.
- **The model ignores later tool results in a long context.** A full
  `get_interfaces` on a chassis switch is hundreds of rows. Ask narrower
  questions, and use `--limit` deliberately on the NetBox listings rather than
  pulling whole inventories.
- **The model edits config it was only asked to read.** Connect with a read-only
  device account so writes fail at the device, and lean on `config_backup` +
  `config_diff` (both reads); hand the diff to a human for the commit.
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/Network-AIops](https://github.com/AIops-tools/Network-AIops/issues)
with the model, runtime, driver, and what went wrong.
