# Mattress Buying Consultant

> Turns any AI agent into an expert mattress buying consultant.

## What it does

Guides mattress buyers through a structured consultation to identify exactly which specs they
need for their specific situation, sleeping position, body weight, bed frame type, and region —
without relying on biased sales advice. Delivers a prioritised spec list and up to 5 matched
product suggestions.

## How it works

1. Agent interviews the user with targeted, research-backed questions (sleeping position,
   body weight, partner situation, heat sensitivity, health needs, frame type, room size, region)
2. Applies the verified position-and-weight firmness matrix and foam density standards to
   determine required specs
3. Delivers a structured spec recommendation: non-negotiable → recommended → optional
4. Suggests up to 5 real products matching the user's confirmed specs, tailored to their region

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

https://github.com/arbazex/bedroom-essentials-buying-consultants/tree/master/mattress-buying-consultant
