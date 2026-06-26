# Laptop Buying Consultant

> Turns any AI agent into an expert laptop buying consultant.

## What it does

Guides first-time and returning laptop buyers through a structured consultation to identify exactly which specs they need for their specific use case, environment, portability requirements, and region — without relying on biased sales advice. Delivers a prioritised spec list (non-negotiable → recommended → optional) and up to 5 matched product suggestions.

## How it works

1. Agent introduces the consultation process briefly, then interviews the user with targeted, research-backed questions grouped by topic (use case, portability, display, battery, GPU, connectivity, OS, region, user profile)
2. Analyses answers using verified laptop industry guidelines: CPU tier selection, RAM sizing, storage minimums, battery Wh estimation, GPU VRAM requirements, and display resolution-to-size rules
3. Proactively flags common first-time buyer mistakes where the user's answers suggest risk (e.g. HDD-only laptop, 4GB RAM, gaming laptop for daily commuting)
4. Delivers a structured spec recommendation: non-negotiable → recommended → optional
5. Suggests up to 5 real products matching the user's confirmed specs, tailored to their region where possible

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

https://github.com/arbazex/personal-tech-buying-consultants/tree/master/laptop-buying-consultant
