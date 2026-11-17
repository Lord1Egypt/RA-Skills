---
name: osc-bridge
description: This skill should be used when the user wants to control music hardware or software from Claude via osc-bridge — playing or tweaking a hardware synthesizer over MIDI/SysEx (849 device drivers), driving a DAW (Ableton Live, Bitwig, Reaper) over OSC, or sending OSC to live-coding environments (Sonic Pi, SuperCollider, Pure Data, TouchDesigner, VCV Rack). It covers finding the right device driver, reading its OSC surface, the two-process architecture (MCP server plus the running bridge), MIDI port discovery, and the failure modes that are silent by design.
---

# osc-bridge

## Overview

osc-bridge gives every synthesizer and music app a clean, named OSC surface:
send `/grandmother/filter/cutoff 64` and the bridge translates it to the right
MIDI CC, NRPN, or SysEx frame for that device. 849 hardware drivers plus 8
software targets (DAWs and live-coding environments). This skill drives it
through the `osc-bridge` MCP server.

## Critical: two things must be true before anything makes sound

**1. The MCP server needs the device catalogue, and npm does not ship it.**
The published package contains only the binary; the 849 driver JSONs live in
the git repo. `--devices-dir` defaults to the relative path `devices`, so a
default install indexes **0 devices** and every device tool fails with
`no device with slug '…'`. Clone the repo and point at it:

```json
{
  "mcpServers": {
    "osc-bridge": {
      "command": "npx",
      "args": ["-y", "@roomi-fields/osc-bridge", "mcp",
               "--devices-dir", "/absolute/path/to/osc-bridge/devices"]
    }
  }
}
```

Check the server's stderr for `indexed 849 device file(s)`. If it says
`indexed 0`, the path is wrong — nothing else will work.

**2. The MCP `send` tool talks to the *bridge*, not to the synth.**
The MCP server opens no MIDI port. A separate bridge process must be running
and listening, or messages vanish into a UDP void:

```bash
# hardware — --out-port is required
osc-bridge run --device devices/moog/grandmother.json \
  --out-port 4 --bind 127.0.0.1:7777 --osc-client 127.0.0.1:8888

# software (DAW / live coding) — no MIDI ports
osc-bridge run --device devices/ableton/live.third-party-osc.fw-12.2.json \
  --bind 127.0.0.1:7777 --osc-client 127.0.0.1:8888
```

`send` reports `sent: true` even when nothing is listening — it is
fire-and-forget UDP. Silence is the only failure signal.

## The five MCP tools

| Tool | Params | Use |
| --- | --- | --- |
| `list_devices` | none | Full catalogue dump — **~237 KB of JSON**. Avoid; grep the docs instead (below). |
| `get_device_docs` | `slug` | Companion notes. Only **10 devices have any**; `has_docs:false` elsewhere is normal. |
| `list_routes` | `slug` | **The workhorse** — every OSC address the device accepts, with CC/NRPN numbers and ranges. |
| `send` | `addr`, `args?`, `target?` | Send one OSC message to the bridge. |
| `get_status` | `target?` | **Do not use as a health check** — it reports `replied:false` even when the bridge is running (replies only go to `--osc-client` addresses). |

## Workflow

1. **Find the device.** Grep `docs/SUPPORTED_DEVICES.md` in the clone — it lists
   every device by vendor with its **OSC prefix**. The prefix minus the leading
   slash *is* the slug (`/grandmother` → `grandmother`). Do not call
   `list_devices` just to search; it dumps the whole catalogue into context.
2. **Read its surface.** `list_routes(slug)` returns `commands`, `cc_params`
   (with `cc`, `nrpn_msb/lsb`, `range`), `params` (SysEx), and `replies`.
3. **Start the bridge** (see above). For hardware, find the MIDI port first with
   `osc-bridge list` — it prints separate numbered lists for inputs and outputs;
   `--out-port` takes the **output** index.
4. **Send.** `send("/<slug>/<address>", [args])`, using the exact addresses from
   step 2.

For anything beyond a single message — device details, address→MIDI mapping,
per-DAW setup, or when something is silent — load the reference below that fits.

## References

- `references/devices.md` — finding drivers, slug rules, how OSC addresses map
  to CC / 14-bit CC / NRPN / SysEx / performance notes, the raw-SysEx escape
  hatch, and the coverage reality (most drivers are CC-only).
- `references/software-targets.md` — the 8 DAW / live-coding targets: ports,
  index bases, and the **host-side setup each one requires** (AbletonOSC,
  DrivenByMoss, Reaper OSC prefs, Sonic Pi, SuperCollider, Pure Data,
  TouchDesigner, VCV Rack).
- `references/troubleshooting.md` — the silent failure modes, in the order worth
  checking.

## Typing matters

`send` mirrors the JSON literal type into OSC: `124` becomes an int, `124.0` a
float. AbletonOSC silently ignores an int where it expects a float — when a DAW
command does nothing, check this first.
