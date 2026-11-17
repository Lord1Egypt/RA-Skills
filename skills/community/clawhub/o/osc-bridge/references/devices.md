# Devices: finding drivers and how addresses map to the wire

## Finding a driver

849 driver files under `devices/<vendor-slug>/<device>.json`, 191 vendors.

1. **`docs/SUPPORTED_DEVICES.md`** (auto-generated, kept in sync by CI) — grouped
   by vendor; each entry gives the OSC prefix, the file, the source tier, and the
   coverage line. Grep this first; it is the cheapest lookup.
2. **`docs/devices.json`** — machine-readable index (`entries[]` with `vendor`,
   `name`, `path`, `source_types`, `coverage`).
3. **Web browser** — <https://roomi-fields.github.io/osc-bridge/> (search by
   vendor, model, author, source).
4. `list_devices` (MCP) only as a last resort: no filter parameter, ~237 KB.

**Slug = `device.osc_prefix` without the leading slash**, not the filename.
`devices/ableton/live.third-party-osc.fw-12.2.json` → slug `ableton`;
`devices/ableton/push-3.json` → `push3`.

**7 slug collisions** exist (`ms_20`, `prophet_12`, `biscuit`, `prophet_rev2`,
`ob_6`, `pro_3`, `toraiz_as_1`): only the first file walked is reachable by that
slug. `list_devices`' `file` field is the only way to tell which one you got.

## Coverage reality

- `cc_params` on **787** drivers — this is the usable surface for almost every
  device.
- `midi_out` (performance notes) on **837**.
- `commands` on **152**.
- SysEx `params` on **3 only** (`arturia/minilab3.json`, `arturia/matrixbrute.json`,
  and one stub). Do not expect SysEx parameter access on a random synth.

Source tiers (`_sources[0].type`, surfaced as `source_tier`): `electra-preset`
588, `pencilresearch` 244, `vendor-osc-api` 5, `vendor-doc` 4, `third-party-osc`
3, `hardware-verified` 1, `hardware-verified-partial` 1, `community-re` 1. Most
of the catalogue is imported from preset/community data, not verified on
hardware — treat an untested driver as plausible, not proven.

## Address → wire mapping

**CC** — `/<prefix>/filter/cutoff 64` → `[0xB0|channel, cc, value]`. An optional
**second OSC argument overrides the MIDI channel**: `/<prefix>/filter/cutoff 64 3`.

**14-bit CC** — when the entry has `cc_lsb`, `cc` is the MSB and `range` goes up
to 16383; both bytes are emitted.

**NRPN** — when the entry has `nrpn_msb` / `nrpn_lsb`, the bridge emits
CC99/CC98/CC6 (plus CC38 for 14-bit) automatically. Nothing to do by hand.

**Performance MIDI** (837 drivers, via `midi_out`):

```
/<prefix>/note/on {note} {velocity} [{channel}]
/<prefix>/note/off {note} [{velocity}] [{channel}]
/<prefix>/cc/{num} {value} [{channel}]
/<prefix>/pitchbend {u14}
/<prefix>/aftertouch {value}
/<prefix>/poly_aftertouch {note} {value}
/<prefix>/program_change {program}
```

**SysEx frames** — declared per command with byte placeholders: `{name}`
(clamped 0..127), `{name:u14_msb}`, `{name:u14_lsb}`, `{name:ascii}`,
`{name:bytes}`. Argument types: `u7`, `u14`, `enum`, `string`, `bool`.

**Raw SysEx escape hatch** — `/<prefix>/raw/syx "F0 00 20 6B … F7"`: a single
space-separated hex **string** argument. Silently ignored unless it starts with
`F0` and ends with `F7`.

**Bulk parameter read** (the 3 SysEx-param devices only) —
`/<prefix>/param/get <pr> <p> <c> <r>` with four int args.

## `expects` hints

`list_routes` entries carry an informative `expects`: `continuous` (default),
`switch`, `momentary`, `trigger`, `clock`, `discrete`. It documents intent — the
bridge does not enforce it. Absent on osc-bridge < 0.11.0.

## Rate limiting

Each driver declares `rate_limit_hz` (e.g. 800 for MiniLab 3, 1000 for imported
drivers) and the outbound queue is bounded at 1024 messages; saturating it logs
`queue full`. Pace parameter sweeps rather than blasting them.

## Running two units of the same model

Override the prefix per device in an orchestrator config
(`osc-bridge orchestrate --config bridge.toml`), e.g. `/matrixbrute-1` and
`/matrixbrute-2`. The same file can also map controls between devices:

```toml
[[routes]]
from = "/minilab3/cc/74"
to   = "/ableton/track/0/volume"
map.from = [0, 127]
map.to   = [0, 1]
```
