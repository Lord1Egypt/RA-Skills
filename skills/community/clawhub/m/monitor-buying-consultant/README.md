# Monitor Buying Consultant

> Turns any AI agent into an expert monitor buying consultant.

## What it does

Guides first-time and returning monitor buyers through a structured consultation to identify exactly which specs they need for their specific use case, desk setup, hardware, ambient environment, and region — without relying on biased sales advice. Delivers a prioritised spec list (non-negotiable → recommended → optional) and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user with targeted, research-backed questions grouped by topic (use case, desk size, ambient lighting, GPU compatibility, port requirements, hours of use, ergonomics, region)
2. Analyses answers using verified display industry knowledge: PPI calculation by size and resolution, panel type selection criteria, connection bandwidth requirements (HDMI/DP version matching), USB-C Power Delivery wattage for laptop users, HDR practical thresholds, and flicker-free/burn-in risk assessment
3. Proactively flags common first-time buyer mistakes where the user's answers suggest risk (e.g. HDMI version mismatch for high-refresh 4K, DisplayHDR 400 without local dimming, OLED burn-in risk for heavy static-content workflows, mismatched GPU for high-Hz monitor, desk too shallow for chosen screen size)
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

https://github.com/arbazex/personal-tech-buying-consultants/tree/master/monitor-buying-consultant
