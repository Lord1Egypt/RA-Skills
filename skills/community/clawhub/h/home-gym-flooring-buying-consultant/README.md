# Home Gym Flooring Buying Consultant

> Turns any AI agent into an expert home gym flooring buying consultant.

## What it does

Guides home gym flooring buyers through a structured consultation to identify exactly which material type, thickness, and format they need for their specific space, subfloor, activity profile, and noise constraints — without relying on biased sales advice. Delivers a prioritised spec list, a coverage calculation, and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user with targeted, research-backed questions across six areas: space and location, subfloor type, activity profile, noise constraints, installation preferences, and surface requirements
2. Analyses answers using verified industry thickness guidelines, subfloor compatibility rules, coverage formulas, and acoustic isolation standards (IIC ratings)
3. Delivers a structured spec recommendation: non-negotiable → recommended → optional
4. Calculates the required coverage quantity with a 10% overage built in
5. Suggests up to 5 real products matching the user's confirmed specs, tailored to their region

## Key specs covered

- Material type: rubber (recycled vs virgin), EVA foam, vinyl
- Thickness: 4 mm through 25 mm+, matched to activity and dropped-weight loads
- Format: rubber rolls, interlocking tiles, individual mats, lifting platforms
- Subfloor compatibility: concrete, hardwood, tile, carpet
- Acoustic performance: IIC rating targets for multi-story or apartment installations
- VOC / indoor air quality: relevant for enclosed spaces and recycled rubber products
- Coverage calculation: length × width + 10% overage formula

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

https://github.com/arbazex/fitness-equipment-buying-consultants/tree/master/rowing-machine-buying-consultant
