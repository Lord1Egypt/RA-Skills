# FM Synthesis Algorithm

## What FM Synthesis Does

Frequency Modulation (FM) synthesis creates complex timbres by modulating one oscillator's frequency with another. Two operators (carrier + modulator) can produce sounds ranging from simple sine tones to rich, bell-like harmonics.

## The Chowning Equation

```
y(t) = sin(2π · fc · t + I · sin(2π · fm · t))
```

Where:
- `fc` = carrier frequency (the pitch you hear)
- `fm` = modulator frequency (creates harmonics)
- `I` = modulation index (controls brightness/richness)
- `fc/fm` = ratio (controls harmonic vs inharmonic spectrum)

## Perception Mapping

| Perception Signal | FM Parameter | Range | Mapping Logic |
|-------------------|-------------|-------|---------------|
| Brightness (0-255) | Carrier `fc` | 65-1760 Hz | Low light = low pitch, bright = high pitch |
| RMS (0-1000+) | Modulation index `I` | 0.5-8.0 | Quiet = pure tone, loud = bright/harsh |
| Phase | Rhythm density | 0.0-1.0 | Night = sparse, day = dense |
| Temperature (°C) | Ratio `fc/fm` | 1.0-3.5 | Warm = harmonic, cold = inharmonic |

## Why FM (Not Diffusion)

- **Size**: 141KB binary vs multi-GB model
- **Speed**: 4s for 90s audio (22x realtime) vs minutes for diffusion
- **Deterministic**: Same input → same output (reproducible sonification)
- **No GPU/CPU requirement**: Runs on a 2014 Intel laptop
- **No API calls**: Fully local, fully offline

## Implementation

The synth is written in Zig 0.16, statically compiled:
- 2-operator FM with envelope (ADSR)
- Phase-driven rhythm generation
- Stereo output with simple spatialization
- WAV writer (PCM 16-bit, 44100Hz, stereo)

Build from source: `zig build -Doptimize=ReleaseSafe`
