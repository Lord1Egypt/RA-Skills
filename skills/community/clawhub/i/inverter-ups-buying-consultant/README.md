# Inverter UPS Buying Consultant

> Turns any AI agent into an expert inverter UPS buying consultant.

## What it does

Guides first-time inverter UPS buyers through a structured consultation to identify exactly which specs they need for their specific situation, usage, and region — without relying on biased sales advice. Delivers a prioritised spec list and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user with targeted, research-backed questions covering load, backup needs, waveform sensitivity, grid quality, region, and battery preference
2. Applies verified industry formulas — load calculation, VA sizing (with inrush margin), battery Ah sizing, and backup time estimation — to the user's specific numbers
3. Delivers a structured spec recommendation: non-negotiable → recommended → optional
4. Suggests up to 5 real products matching the user's confirmed specs, region-tailored

## Key formulas used

- **VA Rating** = (Total Load W + inrush margin) ÷ Power Factor × 1.25 safety margin
- **Battery Ah** = (Load W × Backup Hours) ÷ (Battery Voltage × Efficiency × DoD)
- **Backup Time** = (Battery Ah × Battery Voltage × Efficiency × DoD) ÷ Load W

## Requirements

- No external APIs or environment variables required
- No runtime dependencies
- Works with any AI agent that supports SKILL.md (OpenClaw, ClawHub, etc.)
- Pure instruction-based — agent reasoning does the work

## Installation

Add via ClawHub or reference the SKILL.md directly in your agent configuration.

## License

MIT

## Homepage

https://github.com/arbazex/power-energy-buying-consultants/tree/master/inverter-ups-buying-consultant
