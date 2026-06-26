# Power Bank Buying Consultant

> Turns any AI agent into an expert power bank buying consultant.

## What it does

Guides buyers through a structured consultation to calculate exactly which power bank specs they need — mAh capacity, output wattage, fast-charging protocol, and port configuration — based on their specific devices, desired charges per top-up, travel habits, and region. Delivers a prioritised spec list with explicit calculations and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user across six areas: devices to charge, charging speed requirements, usage context and portability, simultaneous charging needs, power bank recharge speed, and region/certifications
2. Applies verified capacity and wattage formulas (rated mAh × 0.85 usable efficiency, airline Wh limit conversion, recharge time estimate)
3. Flags common mistakes proactively — rated vs usable mAh confusion, protocol mismatches, airline limit violations, insufficient wattage for laptops, proprietary fast-charge incompatibility
4. Delivers a structured spec recommendation: non-negotiable → recommended → optional, with calculations shown
5. Suggests up to 5 real power banks matching the user's confirmed specs, tailored to their region and certifications

## Key formulas applied

| What                   | Formula                                                |
| ---------------------- | ------------------------------------------------------ |
| Usable capacity        | Rated mAh × 0.85                                       |
| Required rated mAh     | (Sum of device mAh × charges desired) ÷ 0.85           |
| Airline Wh limit check | mAh × 3.7 ÷ 1,000 = Wh (must be ≤ 100 Wh for carry-on) |
| Recharge time estimate | Power bank Wh ÷ Input wattage                          |

## Regional certification coverage

CE (EU), FCC + UL 2056 (USA/Canada), UKCA (UK), BIS IS 16046 (India), RCM (Australia/NZ), UN 38.3 (global transport standard).

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

https://github.com/arbazex/power-energy-buying-consultants/tree/master/power-bank-buying-consultant
