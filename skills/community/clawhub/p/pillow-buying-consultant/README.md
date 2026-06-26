# Pillow Buying Consultant

> Turns any AI agent into an expert pillow buying consultant.

## What it does

Guides pillow buyers through a structured consultation to identify exactly which specs they need for their specific sleep position, body proportions, health conditions, fill preferences, and climate — without relying on biased sales advice. Delivers a prioritised spec list and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user with targeted, research-backed questions across six areas: sleep position, body proportions, health, fill preferences, pillow dimensions, and region
2. Applies verified pillow-sizing principles (loft by sleep position and shoulder width, firmness by position and build, fill suitability by allergies and climate)
3. Delivers a structured spec recommendation: non-negotiable → recommended → optional
4. Flags common buyer mistakes proactively (e.g., hot sleeper choosing solid memory foam)
5. Suggests up to 5 real products matching the user's confirmed specs, tailored to their region

## Specs covered

| Spec           | What it determines                                                            |
| -------------- | ----------------------------------------------------------------------------- |
| Loft height    | Gap-fill between head and mattress based on sleep position and shoulder width |
| Firmness       | Spinal alignment support based on position and body frame                     |
| Fill material  | Allergy safety, heat retention, reshapability, durability                     |
| Pillow size    | Bed size and sleep behaviour match                                            |
| Certifications | Regional safety and material standards (OEKO-TEX, CertiPUR-US, RDS)           |

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

https://github.com/arbazex/bedroom-essentials-buying-consultants/tree/master/pillow-buying-consultant
