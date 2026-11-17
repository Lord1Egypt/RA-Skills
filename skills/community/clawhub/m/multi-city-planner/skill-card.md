## Description:

Multi City Planner helps agents compare multi-city, open-jaw, round-trip, and single-segment travel plans and produce standardized HTML itinerary reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danshaniusha](https://clawhub.ai/user/danshaniusha)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search and compare multi-destination travel options, optimize route order, and produce HTML reports with pricing, transportation comparisons, budgets, and trip notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied city and date values are passed into shell commands.

Mitigation: Run only in a restricted environment and avoid untrusted trip strings until command execution uses safe argument handling.

Risk: The skill depends on a broad globally installed FlyAI CLI.

Mitigation: Use a pinned local FlyAI CLI installation and review updates before deployment.

Risk: Live travel results can include booking links and time-sensitive prices.

Mitigation: Validate booking URLs and have users confirm prices, schedules, baggage rules, and visa requirements before purchase.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/danshaniusha/skills/multi-city-planner)
- [FlyAI Homepage](https://open.fly.ai/)
- [Usage Guide](references/usage.md)
- [FlyAI Flight Search Reference](skills/flyai/references/search-flight.md)
- [FlyAI Hotel Search Reference](skills/flyai/references/search-hotel.md)
- [FlyAI POI Search Reference](skills/flyai/references/search-poi.md)
- [FlyAI Keyword Search Reference](skills/flyai/references/keyword-search.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style console output and generated HTML itinerary reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live travel-search results when FlyAI CLI is available; prices, schedules, and booking links may change.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill frontmatter metadata, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
