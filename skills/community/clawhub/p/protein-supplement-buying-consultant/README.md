# Protein Supplement Buying Consultant

> Turns any AI agent into an expert protein supplement buying consultant.

## What it does

Guides protein supplement buyers through a structured consultation to identify exactly which protein type, content, amino acid profile, and purity certification they need for their specific goals, dietary restrictions, and health situation — without relying on biased supplement marketing. Calculates a personalised daily protein target, determines the supplement gap, and delivers a prioritised spec list and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user with targeted, research-backed questions across seven areas: goals and training type, dietary restrictions and allergies, health conditions, body weight and activity level (for protein target calculation), anti-doping status, form factor preferences, and country/region
2. Calculates daily protein target using evidence-based ranges (ACSM/AND joint position statement; Morton et al. 2017 meta-analysis) and determines the supplement gap to fill
3. Applies protein type selection logic: whey isolate, whey concentrate, micellar casein, pea+rice plant blend, soy isolate, or hydrolyzed collagen — matched to the user's goal, digestion, and dietary constraints
4. Delivers a structured spec recommendation: non-negotiable → recommended → optional, plus a health/safety flag section if triggered
5. Suggests up to 5 real products matching the user's confirmed specs, region-aware

## Key specs covered

- Protein type: whey isolate / concentrate / hydrolysate, micellar casein, pea+rice blend, soy isolate, hydrolyzed collagen peptides
- Protein content per serving (g), leucine content (g), protein percentage of scoop weight
- Amino acid completeness: complete vs incomplete; blending requirement for plant-based
- Third-party certification: NSF Certified for Sport®, Informed Sport, USP Verified, Informed Choice
- Allergen exclusions: dairy/lactose-free, soy-free, gluten-free, vegan
- Added sugar and artificial sweetener specs
- Nitrogen spiking red flags and COA (certificate of analysis) verification
- Daily protein target formula and supplement gap calculation

## Health safety guardrails

The skill flags health conditions (kidney/liver disease), pregnancy, breastfeeding, and under-18 users for mandatory referral to a healthcare provider before a recommendation is made. It does not provide medical nutrition therapy.

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

https://github.com/arbazex/fitness-equipment-buying-consultants/tree/master/protein-supplement-buying-consultant
