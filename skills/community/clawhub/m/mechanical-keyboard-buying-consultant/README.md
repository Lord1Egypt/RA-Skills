# Mechanical Keyboard Buying Consultant

> Turns any AI agent into an expert mechanical keyboard buying consultant.

## What it does

Guides first-time and upgrading mechanical keyboard buyers through a structured consultation to identify exactly which specs they need for their specific use case, environment, and region — without relying on biased sales advice or influencer recommendations. Delivers a prioritised spec list (non-negotiable → recommended → optional), a scannable Spec Summary Card, and up to 5 matched product suggestions.

## How it works

1. Agent introduces the consultation process briefly, then asks targeted, research-backed questions grouped by theme (use case, environment/noise, typing feel, layout, connectivity, build quality, customisation, region)
2. Analyses answers using verified mechanical keyboard industry specs: switch actuation data, layout standards, connectivity latency figures, keycap material properties, and regional layout standards
3. Flags common first-time buyer mistakes proactively (e.g., clicky switches in a shared office, Bluetooth for competitive gaming, 60% layout without realising F-key dependency)
4. Delivers a structured spec recommendation: non-negotiable → recommended → optional, plus a Spec Summary Card
5. Suggests up to 5 real keyboards matching the user's confirmed specs — only after the full spec list is complete

## Requirements

- No external APIs or environment variables required
- No runtime dependencies
- Works with any AI agent that supports SKILL.md (OpenClaw, ClawHub, etc.)
- Pure instruction-based — agent reasoning does the work

## Specs covered

| Dimension            | What the skill determines                            |
| -------------------- | ---------------------------------------------------- |
| Switch category      | Linear / tactile / clicky / silent variant           |
| Actuation force      | Light (35–45 g) / medium (45–55 g) / heavy (60–80 g) |
| Key travel           | Standard 4 mm total / low-profile 3 mm total         |
| Layout / form factor | 100% / TKL / 75% / 65% / 60%                         |
| Regional standard    | ANSI / ISO / QWERTZ / AZERTY                         |
| Connectivity         | Wired / 2.4 GHz wireless / Bluetooth                 |
| Keycap material      | ABS vs PBT; pad-printed vs doubleshot legends        |
| Keycap profile       | OEM / Cherry / SA / DSA / XDA                        |
| Hot-swap PCB         | Required / preferred / not needed                    |
| OS compatibility     | Windows / Mac / Linux                                |
| Switch durability    | Minimum rated keystroke lifespan                     |

## Installation

Add via ClawHub or reference the SKILL.md directly in your agent configuration.

## License

MIT

## Homepage

https://github.com/arbazex/personal-tech-buying-consultants/tree/master/mechanical-keyboard-buying-consultant
