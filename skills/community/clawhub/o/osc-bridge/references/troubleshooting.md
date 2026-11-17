# When nothing happens

Every layer here fails silently by design (UDP, fire-and-forget). Check in this
order.

## 1. Did the MCP server index the catalogue?

Server stderr should read `indexed 849 device file(s)`. `indexed 0` means
`--devices-dir` is wrong — the npm package ships only the binary, the drivers
live in the git clone. Every device tool will fail with
`no device with slug '…'` until this is fixed.

## 2. Is a bridge process actually running?

The MCP server opens no MIDI port and does not forward to hardware. A separate
`osc-bridge run …` (or `orchestrate`) must be listening on the target port
(default `127.0.0.1:7777`). Its stderr ends with `Ready. Ctrl-C to stop.`

**Do not use `get_status` to check this** — it reports `replied:false` even when
the bridge is healthy, because `/bridge/status` replies are broadcast only to
the `--osc-client` addresses, never back to the requesting socket. To watch
traffic instead:

```bash
osc-bridge osc-listen --bind 127.0.0.1:8888
```

## 3. Is there an `--osc-client`?

With no client registered, every outbound event is dropped: MIDI-in knob turns,
SysEx replies, DAW replies, `/bridge/status`, `/bridge/docs`. The usual launch
pairs them: `--bind 127.0.0.1:7777 --osc-client 127.0.0.1:8888`.

## 4. Right MIDI port?

```bash
osc-bridge list
```

prints two **separate** numbered lists (inputs, outputs). `--out-port` takes an
index from the *outputs* list; reusing an input index is a common mistake.
`--out-port` is mandatory for hardware drivers — omitting it aborts with an
explicit message. For OSC-transport (software) drivers it is ignored.

## 5. Argument types

`send` mirrors the JSON literal: `124` → OSC int, `124.0` → OSC float. Many MCP
clients normalise `124.0` to `124`. AbletonOSC ignores an int where it expects a
float — the single most common "the DAW does nothing" cause.

## 6. Index base

AbletonOSC is **0-based**; DrivenByMoss (Bitwig) and Reaper are **1-based**, and
their drivers only declare tracks 1..8. Off-by-one here targets a track that
exists but is not the one intended.

## 7. Exact address

Addresses come from `list_routes(slug)`, prefixed with `/<slug>`. A typo is
silently dropped — `send` still returns `sent: true`.

## 8. Reply port bound?

For OSC drivers, a missing `transport.reply_port` logs
`WARN: device declares OSC replies but no transport.reply_port — they will never fire`.
Reply ports also collide across drivers (Bitwig / Reaper / Pure Data all want
9000); run one at a time or override the ports in an orchestrator config.

## 9. Windows 11 24H2+ — device invisible

`USBMidi2-ACX` (KB5079473) hides some devices from the legacy MME API used by
the bridge (confirmed on Polyend Synth / Play / Tracker / Mess / Step). Fix:
Device Manager → Update Driver → *Let me pick* → **USB Audio Device**, unplug and
replug, then re-run `osc-bridge list`.

## 10. Building from source

A stale prebuilt binary may sit in `target/release/`. Anything below 0.11.0
returns no `structuredContent` and no `expects` field. Run `cargo build --release`
after cloning; check with `osc-bridge --version`.

## Other useful CLI verbs

```bash
osc-bridge inspect <device.json>     # offline summary: prefix, IDs, commands, params
osc-bridge osc-send <addr> <args…>   # send without an MCP client
osc-bridge osc-listen --bind …       # watch what the bridge emits
osc-bridge lint <device.json>        # validate a driver
```
