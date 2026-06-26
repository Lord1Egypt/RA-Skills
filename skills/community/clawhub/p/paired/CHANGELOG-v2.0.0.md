# Paired: Phone Agent — v2.0.0 — Voice cloning release

**Release date:** 2026-05-17

**Theme:** The skill grew up. v1 was "pair my Bluetooth headset." v2.0.0 is "give my agent a body — phone, voice, and all."

The name has been refined to **Paired: Phone Agent** in all public-facing documentation to reflect the actual scope of what the skill does. The ClawHub slug `paired` is unchanged so existing installs continue to work seamlessly.

---

## Major changes

### Added — voice cloning subsystem

Paired now optionally clones the user's own voice for all synthesised speech, with privacy-first design: no cloud calls, no upstream training data, all weights local.

* `skill/voice/paired-voice-synth.py` — TTS wrapper with 4-level fallback ladder
* `skill/engines/voxcpm-server.py` + `voxcpm.Dockerfile` — VoxCPM2 HTTP service (primary engine)
* `skill/engines/xtts.Dockerfile` — XTTS v2 HTTP service (fallback)
* `skill/setup/paired-voice-setup.py` — guided 5-minute training flow
* `skill/config-templates/voice.conf.example` — config template

### Added — word-level audio splicing

Pre-recorded clips of specific words (typically the user's name, family names, brand names) are spliced into synthesised output for 100% accurate pronunciation. Drop WAV files into `~/.config/paired/voice/word-clips/`; the synth wrapper detects matches at word boundaries (case-insensitive).

Solves the universal "AI mispronounces my name" problem permanently. Your name is now pronounced by you, every time.

### Added — 30-language multilingual

Via VoxCPM2: auto-detected language support across 30 languages from input text. No flag needed.

Supported languages: Arabic, Burmese, Chinese, Danish, Dutch, English, Finnish, French, German, Greek, Hebrew, Hindi, Indonesian, Italian, Japanese, Khmer, Korean, Lao, Malay, Norwegian, Polish, Portuguese, Russian, Spanish, Swahili, Swedish, Tagalog, Thai, Turkish, Vietnamese.

### Added — long-form chunking

The synth wrapper splits long text at sentence boundaries before calling the cloning engine, avoiding the ~400-token soft limit and GPU OOM seen on 1500+ character inputs. Concatenation is gap-free; listeners cannot hear the joins. Tested at 2-minute voice notes; scales cleanly to 10+ minutes.

### Added — public documentation

* `README.md` (top level) — rewritten for the v2.0.0 "Paired: Phone Agent" identity
* `skill/docs/VOICE-SETUP.md` — full voice setup, troubleshooting, multilingual
* `skill/marketing/README-marketing.md` — long-form public pitch
* `skill/THIRD_PARTY.md` — full attribution for all bundled and runtime dependencies

---

## Unchanged

All v1.x functionality is preserved exactly as it was: BlueZ pairing, ADB control, SMS receive (MAP/MNS), SMS send (ADB autosend), outgoing calls (HFP), incoming-call alerts, contacts pull (PBAP), media control (AVRCP), file transfer (OBEX), PAN tethering, trusted-numbers allowlist, HMAC-signed inbox command dispatch, mode 0600 secret-file enforcement.

v2.0.0 is strictly additive.

---

## Removed

Nothing.

---

## Compatibility

* All v1.x configs work unchanged
* If `voice.conf` is absent, paired falls back to piper or espeak-ng — the v1.x behaviour
* Voice cloning is **opt-in** — the skill does nothing voice-related until the user runs `paired-voice-setup.py reference`
* ClawHub slug remains `paired` — existing installs keep working without action

---

## Hardware requirements

| Use case | Floor |
|----------|-------|
| Full feature (cloned voice, 48kHz) | NVIDIA GPU with 6GB+ VRAM |
| Cloned voice (24kHz, XTTS only) | NVIDIA GPU with 4GB VRAM |
| Fallback (generic neural voice) | CPU only — no GPU required |
| Phone bridge alone (no voice cloning) | Same as v1.x — Linux host with BlueZ, Android phone with ADB |

---

## Acknowledgements

VoxCPM2 (OpenBMB), coqui-tts (idiap fork), piper (rhasspy), espeak-ng. Full attribution in [`THIRD_PARTY.md`](THIRD_PARTY.md).

Bug reports and hardware compatibility reports welcome at the issue tracker.
