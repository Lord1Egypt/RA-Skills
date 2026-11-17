## Description:

Plans multi-night stargazing and astrophotography trips by comparing nightly candidates for route continuity, transfer distance, lodging continuity, executability, and main, backup, or far-line route tradeoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clhwbd](https://clawhub.ai/user/clhwbd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to build practical multi-day stargazing or astrophotography route plans from nightly location candidates. It helps choose a main route, backup route, and far-line option while explaining weather, continuity, and travel-risk tradeoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real-weather mode may use retries that disable HTTPS certificate checks.

Mitigation: Keep certificate verification enabled for every weather request before using the skill for travel planning.

Risk: The Python dependency lunarcalendar is unpinned.

Mitigation: Pin lunarcalendar to a reviewed version before installation or deployment.

Risk: Route and weather recommendations could be mistaken for final safety advice.

Mitigation: Treat outputs as planning support and confirm weather, road, lodging, and local safety conditions before travel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clhwbd/skills/go-stargazing-trip)
- [Photography agent responsibility contract](artifact/references/agent-contract.md)
- [Dynamic sampling implementation plan](artifact/references/dynamic-sampling-plan.md)
- [Current output schema](artifact/references/output-schema-current.md)
- [Scope scanning policy](artifact/references/scope-policy.md)
- [Lightweight scoring and dynamic sampling plan](artifact/references/scoring-lite.md)
- [Stargazing location scoring system](artifact/references/stargazing_scoring_system.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with optional JSON-producing shell command outputs from bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces route recommendations, risk notes, reference information, nightly suggestions, backup routes, and far-line options.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
