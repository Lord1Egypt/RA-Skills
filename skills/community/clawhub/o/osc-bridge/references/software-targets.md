# DAW and live-coding targets

Eight software drivers (`device.kind: "software"`, `transport.kind: "osc"`).
Each has a companion `.md` in the repo, readable via `get_device_docs(slug)`.

| Slug | Driver file (`devices/…`) | Mode | Bridge → host | Host → bridge |
| --- | --- | --- | --- | --- |
| `ableton` | `ableton/live.third-party-osc.fw-12.2.json` | declarative | 11000 | 11001 |
| `bitwig` | `bitwig/bitwig-studio.third-party-osc.fw-5.json` | declarative | 8000 | 9000 |
| `reaper` | `cockos/reaper.vendor-osc-api.fw-7.json` | declarative | 8000 | 9000 |
| `sonicpi` | `sonic-pi/sonic-pi.vendor-osc-api.fw-4.5.json` | passthrough | 4560 | 4570 |
| `sclang` | `supercollider/sclang.vendor-osc-api.fw-3.13.json` | passthrough | 57120 | 57130 |
| `pd` | `pure-data/puredata.vendor-osc-api.fw-0.55.json` | passthrough | 9000 | 9001 |
| `td` | `touchdesigner/touchdesigner.vendor-osc-api.fw-2023.json` | passthrough | 7000 | 7001 |
| `vcv` | `vcv-rack/vcv-rack.third-party-osc.fw-2.5.json` | passthrough | 7770 | 7771 |

**Declarative** targets expose named `commands` — use `list_routes(slug)`.
**Passthrough** targets have no commands: `list_routes` returning empty arrays is
expected, not a bug. Anything sent as `/<slug>/foo/bar args` is forwarded
verbatim minus the slug (`/foo/bar args`); replies arriving on the reply port are
re-emitted with the slug prefixed back on.

**Port collisions**: Bitwig, Reaper (both 8000/9000) and Pure Data (9000) cannot
run simultaneously without overriding ports in an orchestrator config.

## Host-side setup (required — the bridge alone is not enough)

### Ableton Live
Install AbletonOSC as a Remote Script:
`~/Music/Ableton/User Library/Remote Scripts/AbletonOSC` (macOS) or
`Documents\Ableton\User Library\Remote Scripts\AbletonOSC` (Windows).
**Restart Live entirely** — Remote Scripts are only scanned at startup. Then
Preferences → Link/Tempo/MIDI → Control Surface → **AbletonOSC**; the status bar
should show `Listening for OSC on port 11000`.

- Indices are **0-based** (track 0 = leftmost).
- **Floats must be floats**: `/ableton/transport/tempo 120` is silently ignored;
  send `120.0`.
- Volume is 0..1 (≈0.85 ≈ 0 dB).

### Bitwig Studio
DrivenByMoss: Dashboard → Settings → Controllers → Add Controller → Generic →
OSC (or drop the release into `~/Documents/Bitwig Studio/Extensions/`). Set
*Port to receive on* = 8000 and *Host/Port to send to* = 127.0.0.1 / 9000, then
toggle the controller off and on.

- Indices are **1-based**; the bank size is 8, so `/track/9/...` requires
  changing the bank inside Bitwig.
- State changes are auto-emitted — no subscription needed.

### Reaper
Preferences → Control/OSC/web → Add → OSC. Mode = *Configure device IP + local
port*; Device IP `127.0.0.1`, Device port `9000`, Local listen port `8000`;
leave the pattern config on `Default.ReaperOSC`. No restart needed.

- Indices are **1-based**; the driver declares tracks 1..8.

### Sonic Pi
Bridge → Sonic Pi on **4560** (its default OSC input). Sonic Pi → bridge on
**4570**:

```ruby
osc_send "127.0.0.1", 4570, "/beat", 1
```

Receive in a `live_loop` with `sync "/osc*/trigger/kick"`. Useful prelude:
`use_osc_logging false` and `set_sched_ahead_time! 0.5`.

### SuperCollider
Targets **sclang** on 57120, replies on 57130:

```supercollider
OSCdef(\trigger, { |msg| /* ... */ }, "/trigger");
NetAddr("127.0.0.1", 57130).sendMsg("/beat", 1);
```

To drive **scsynth** directly (port 57110), copy the driver and change
`osc_prefix` and `port`. A wrapper class ships at
`examples/sc-quark/OscBridge.sc`.

### Pure Data
Receive: `[netreceive -u -b 9000] → [oscparse] → [route /trigger /set_volume]`.
Send: `[oscformat /beat] → [netsend -u -b]` with `connect 127.0.0.1 9001`.

### TouchDesigner
OSC In CHOP/DAT on 7000; OSC Out pointed at 7001.

### VCV Rack
No built-in OSC — requires the `vcv-osc` plugin
(<https://github.com/roomi-fields/vcv-osc>), ports 7770 / 7771.
