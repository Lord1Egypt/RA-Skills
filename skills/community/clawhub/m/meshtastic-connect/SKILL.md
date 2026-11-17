---
name: meshtastic-connect
description: Connect an OpenClaw gateway to a Meshtastic LoRa mesh node in minutes — install the maintained channel plugin (@fintlp/openclaw-meshtastic), run the probe-first setup wizard, and verify the first DM over radio. Use when a user wants their AI agent reachable via Meshtastic, off-grid messaging, or LoRa mesh comms.
---

# Meshtastic Connect

Get a user's OpenClaw agent onto their Meshtastic mesh — reachable by DM from any node in range, fully local (no MQTT, no cloud). The path below is verified end-to-end against live hardware; follow it in order and the user is connected in ~3 minutes once their node is on the LAN.

## When to use this

- "I want my OpenClaw/agent to speak Meshtastic"
- "Connect my AI to my LoRa mesh"
- "Let people DM my bot from the radio"

## Prerequisites (check BEFORE installing)

1. **A Meshtastic node the gateway can reach.** Any device with WiFi (Heltec V3, T-Beam, LilyGo) on the same LAN, or a USB-serial node on the gateway machine.
2. **LoRa region set on the node** (Meshtastic phone app → LoRa → Region). Region UNSET = the node cannot transmit. This is also law, not preference.
3. Current firmware (2.7.15+ recommended — older releases carry the unpatched CVE-2025-53627 PKI vulnerability, and the plugin warns at startup below 2.7.15).

## Compatibility (read before installing)

- **Minimum OpenClaw: 2026.10.1** — the plugin's declared floor (peerDependencies, compat.pluginApi and install.minHostVersion are all >=2026.10.1).
- **OpenClaw 2026.10.5 or newer requires plugin 2026.10.24 or newer.** 2026.10.5 removed the SDK export runStoppablePassiveMonitor; older plugin versions fail to register at gateway boot with: The requested module 'openclaw/plugin-sdk/extension-shared' does not provide an export named 'runStoppablePassiveMonitor'. Fix: update or reinstall to the current release, then restart the gateway.

## Fast path

```bash
openclaw plugins install clawhub:@fintlp/openclaw-meshtastic
openclaw onboard   # choose Meshtastic
```

The wizard asks how the gateway reaches the node (TCP 4403 / HTTP 4433 / USB serial), **probes the connection before writing any config** — with targeted fixes when it fails — reads the node's identity (ID, name, region, firmware) off the radio as proof, and walks access policy with safe defaults pre-selected.

Non-interactive alternative:

```bash
openclaw channels add meshtastic --transport tcp --host 192.168.1.10
# also: --serial-path /dev/cu.usbserial-0001 --baud-rate 115200 --dm-policy pairing|allowlist|open|disabled --group-transmit
```

## Verified traps (each one cost someone an evening)

- **4403 ≠ 4433.** TCP (native protobuf stream) is port 4403 and works out of the box. HTTP (the node's web API) is port 4433 and must be explicitly enabled in the node's network settings. Mixing them up fails in ways that look like everything *except* a wrong port. When in doubt: `transport tcp`, port 4403. The wizard's probe detects this exact case and offers to switch.
- **TCP/serial payloads arrive encrypted** and `@meshtastic/core` does NOT decrypt them. The plugin decrypts client-side (per-channel PSKs, zero config). A raw TCP client shows ciphertext — that is not a bug.
- **Region UNSET.** The node receives but cannot transmit. Set the region in the phone app first; the wizard warns when it reads UNSET from the node.
- **Serial: only one process may own the port.** Stop other Meshtastic apps/CLIs first. And use a USB *data* cable — charge-only cables are the #1 serial trap.
- **IoT VLANs with client isolation** make a healthy node look dead. Probe from the same VLAN when in doubt.

## Access & safety defaults (do not loosen without a reason)

- `dmPolicy: "pairing"` — every new contact needs explicit approval.
- `groupTransmit: false` — the send path **refuses all channel/broadcast messages** until deliberately enabled (LoRa airtime is a shared commons; there is no delete button on the airwaves). Group listening with mention-gating is available either way.
- `dmIdentity: "known-keys"` (default since plugin 2026.11.1) — an inbound identity gate drops DMs from senders whose pinned or tombstoned key fails verification, before pairing or dispatch, logging one throttled line per sender (fingerprints only, never bodies or keys). Senders the gateway has never seen a key for still pass; `dmIdentity: "strict"` demands a verified key from everyone and locks out nodes on firmware before 2.5. HTTP transport carries no PKI provenance — use `tcp` or serial if verified identity matters to you.
- Flood guard: 20 DMs / 10 min, 3 channel msgs / 10 min — a message is sent whole or refused whole, never partially aired.

## Verify it works

1. `openclaw channels status --probe` → meshtastic ok.
2. Self-test: DM the node's `!id` (shown by the wizard) from a second device or phone app. Expect the agent's reply within ~a minute — LoRa is slow, that is normal. If nothing arrives, check the gateway log for a throttled `identity-gate` line first — a sender whose pinned key fails verification is a gate decision, not a radio fault.

## Node map on demand (once connected)

The plugin writes `~/.openclaw/state/meshtastic-nodes.json` (named accounts: `.<accountId>.json`): every known node with name, role, `lat`/`lon` (when shared), `lastHeard` (epoch s), `precisionBits`, `self`. These are the real-world positions of other people's radios — treat the file and anything derived from it as sensitive (it is written mode 0600; keep it out of shared folders).

For "show me the mesh", prefer the local path: keep nodes with lat/lon, build a GeoJSON FeatureCollection (coordinates `[lon, lat]`), write it to a local file and open it in a local/offline viewer — nothing leaves the machine.

The zero-airtime shortcut is a `https://geojson.io/#data=data:application/json,<encodeURIComponent(json)>` link — generate it only on explicit owner request, with the warning attached: the fragment is never sent to geojson.io's server (the page decodes it locally), but opening the link exposes every embedded coordinate to the third-party viewer's JavaScript and to basemap tile servers, and the full link persists in chat and browser history — anyone holding it sees the nodes. Owner only, never in reply to a mesh DM session. Full recipe: docs/meshtastic.md, "Node book".

## Maintenance & support

Maintained line: `fintlp/openclaw-meshtastic` (fork of the dormant skrashevich original). Issues: https://github.com/fintlp/openclaw-meshtastic/issues
