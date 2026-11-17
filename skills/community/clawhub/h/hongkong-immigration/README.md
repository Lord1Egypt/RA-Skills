# Hong Kong Immigration Skill

A Codex/OpenClaw skill for answering Hong Kong visa, entry-permit, residency,
and immigration-pathway questions with official-source verification.

## Coverage

- Mainland residents: Exit-entry Permit for Travelling to and from Hong Kong
  and Macao, endorsements, and One-way Permit pathways.
- Overseas visitors: visa-free visits, visitor visas, and transit.
- Long-term pathways: TTPS, QMAS, ASMTP/GEP, IANG, students, dependants, and
  right-of-abode planning.
- Legal and compliance boundaries: conditions of stay, employer changes,
  overstaying, false statements, and source hierarchy.

## Install

From ClawHub:

```bash
clawhub install hongkong-immigration
```

Or clone directly:

```bash
git clone https://github.com/djanngau/hongkong-immigration-skill.git \
  ~/.codex/skills/hongkong-immigration
```

## Source policy

The skill separates legal authority, official policy, and practical experience.
Time-sensitive figures and eligibility rules must be checked against current
official sources before they are presented to a user. Community experience is
never treated as an official rule.

This skill provides general information, not legal or immigration advice.
Individual decisions remain subject to the relevant authorities.

## Validate

```bash
python3 scripts/validate.py
```

## Structure

```text
SKILL.md
references/
evals/evals.json
scripts/validate.py
```
