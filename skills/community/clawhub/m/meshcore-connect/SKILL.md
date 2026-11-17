---
name: meshcore-connect
description: Connect an OpenClaw gateway to a MeshCore LoRa mesh node in minutes — install the maintained channel plugin (@fintlp/openclaw-meshcore), run the probe-first setup wizard, and verify the first DM over radio. Use when a user wants their AI agent reachable via MeshCore, off-grid messaging, or LoRa mesh comms.
---

# MeshCore Connect

Get a user's OpenClaw agent onto their MeshCore mesh — reachable by DM from any node in range, fully local (no cloud). The path below is verified end-to-end against live hardware; follow it in order and the user is connected in minutes once their node is on the LAN.

## When to use this

- "I want my OpenClaw/agent to speak MeshCore"
- "Connect my AI to my LoRa mesh"
- "Let people DM my bot from the radio"

## Prerequisites (check BEFORE installing)

1. **A MeshCore node the gateway can reach.** An ESP32 board (Heltec WiFi LoRa 32 V3/V4 verified) flashed with the **MeshCore companion firmware with WiFi** — the build that speaks the Companion Protocol over TCP.
2. **The companion TCP server enabled** on the node (default port 5000) and the node on the same LAN as the gateway.
3. **Region/band set for the user's locale** (EU868 in Austria/EU — frequency is law, not preference).

## Compatibility (read before installing)

- **Minimum OpenClaw: 2026.10.1** — the plugin's declared floor (peerDependencies, compat.pluginApi and install.minHostVersion are all >=2026.10.1).
- **OpenClaw 2026.10.5 or newer requires plugin 2026.10.13 or newer.** 2026.10.5 removed the SDK export runStoppablePassiveMonitor; older plugin versions fail to register at gateway boot with: The requested module 'openclaw/plugin-sdk/extension-shared' does not provide an export named 'runStoppablePassiveMonitor'. Fix: update or reinstall to the current release, then restart the gateway.

## Fast path

```bash
openclaw plugins install clawhub:@fintlp/openclaw-meshcore
openclaw onboard   # choose MeshCore
```

The wizard **probes the node before writing any config** — with targeted fixes when it fails — and reads the node's identity (name, hardware, firmware, battery) as proof.

Non-interactive alternative:

```bash
openclaw channels add meshcore --host 192.168.1.20
# also: --dm-policy pairing|allowlist|open|disabled
```

## Verified traps (each one cost someone an evening)

- **ONE companion client at a time.** The node serves exactly one TCP companion. If the MeshCore phone app (or another gateway, or a second plugin instance) is connected, the new client fights it for the slot — connections drop, handshakes stall, and everyone blames the network. Disconnect the app before onboarding; the wizard's diagnosis knows this trap by name.
- **Current firmware silently drops DMs from senders not in the node's contact list.** If the self-test DM never arrives: enable auto-add contacts on the node, or add the peer in the MeshCore app. This looks like an agent failure and is not one.
- **Battery-powered nodes die quietly.** A node with a dead battery looks exactly like a network timeout while its TCP state lingers. If a previously-working node stops answering, check the device physically before debugging anything else.
- **IoT VLANs with client isolation** make a healthy node look dead. Probe from the same VLAN when in doubt.

## Access & safety defaults (do not loosen without a reason)

- `dmPolicy: "pairing"` — every new contact needs explicit approval.
- `groupPolicy: "disabled"` — group monitoring is **opt-in**: no public-channel traffic is admitted or recorded until the operator deliberately enables it. To switch it on (gateway stopped): `openclaw config set channels.meshcore.groupPolicy '"allowlist"'` + `openclaw config set channels.meshcore.groups '{ "channel:0": {} }'`; to switch off: `groupPolicy '"disabled"'`. Default monitor mode is `digest` — admitted messages land in `state/meshcore-group-log.jsonl` without waking the agent; the digest stores **full message text on disk in plain JSON** (treat as sensitive). `"session"` mode routes each admitted message to an agent session — only for tool-restricted agents.
- **Groups are receive-only by code-level design**: even with monitoring on, the agent can listen but never transmits on channels, in any policy or mode. LoRa airtime is a shared commons; there is no delete button on the airwaves.
- **Native DM commands are default-deny since plugin 2026.11.1** — `!status`, `!neighbours`, `!rstatus` and `!trace` stay off for everyone, including explicitly allowlisted peers, and this release has no re-enable option. The sole exception is budgeted `!ping` for allowlisted verified full keys (`commandPingAllowFrom`, canonical `!` + 64 hex, 3 replies / 10 min / account). Host slash-commands over MeshCore DMs remain disabled entirely (tracker #31).
- Flood guard caps outbound DM airtime; replies are chunked to mesh-safe sizes.


## Suggest a use (once connected)

When the user asks "what can I do with this now?", offer a recipe from docs/USE-CASES.md in the plugin repo — compressed here:

1. **Off-grid assistant** (default) — full agent sessions per admitted DM peer. Pair strangers deliberately (dmPolicy pairing).
2. **Emergency / backup channel** — add sendRetry.enabled:true; durability (on by default) replays undispatched messages after gateway updates/crashes, at-least-once (a restart mid-turn can duplicate a reply). Honest limits: nothing is received while the gateway itself is down, and a follow-up queued behind a busy session is only as durable as the host process.
3. **Unattended-node / repeater monitor** — groupMonitorMode digest + groupPolicy allowlist; node health comes from agent DM answers and the node's own status surface. (The native `!status` / `!neighbours` / `!rstatus` / `!trace` DM commands are default-deny since plugin 2026.11.1 — see Access & safety defaults.)
4. **Field-expedition hub** — base-camp gateway, approve each handheld once (pairing), hub answers everyone in DM.
5. **Festival / event bot** — pairing-gated; it can never spam the public channel (that boundary is code, not a promise).
6. **Cross-channel bridge** — a mesh DM can produce effects on the agent's other channels (WhatsApp, notes, reminders) — never for unpaired strangers, other channels' policies still apply.

Full recipes (scenario, config, can/cannot, reading): docs/USE-CASES.md in fintlp/openclaw-meshcore.

## Verify it works

1. `openclaw channels status --probe` → meshcore ok.
2. Self-test: DM the node's `!id` (shown by the wizard) from a MeshCore companion app on a second node. Expect the agent's reply within ~a minute — LoRa is slow, that is normal. If nothing arrives, re-read the contact-list trap above. On plugin 2026.11.1+ a DM the identity layer refuses surfaces in `openclaw logs` as a `dm-identity-no-evidence` / `-ambiguous` / `-stale` dead-letter — check there before suspecting the radio.

## Maintenance & support

Maintained line: `fintlp/openclaw-meshcore`. Issues: https://github.com/fintlp/openclaw-meshcore/issues
