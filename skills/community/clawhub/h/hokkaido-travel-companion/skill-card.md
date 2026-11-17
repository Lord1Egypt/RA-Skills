## Description:

Hokkaido Travel Companion helps agents collect, verify, store, and reuse Sapporo, Otaru, Yoichi, and Chitose travel knowledge with local notes, live source checks, route details, weather, budget tracking, and GO/NOGO guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ico1036](https://clawhub.ai/user/ico1036)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to plan Hokkaido trips, verify restaurant, transport, weather, and closure details, and make budget-aware GO/NOGO decisions. It is scoped to Sapporo, Otaru, Yoichi, and Chitose Airport.

### Deployment Geography for Use:

Global, for Hokkaido travel planning.

## Known Risks and Mitigations:

Risk: The skill may save personal trip details such as itinerary notes, hotel-adjacent context, budgets, and visit notes in local files.

Mitigation: Avoid entering sensitive travel details that should not be retained, and review or delete local vault and budget files before sharing or publishing the skill directory.

Risk: Restaurant hours, closures, fares, walking times, and weather can change or become stale.

Mitigation: Verify stale or high-risk travel details with official or trusted live sources before making recommendations.

## Reference(s):

- [Hokkaido Travel Companion on ClawHub](https://clawhub.ai/ico1036/skills/hokkaido-travel-companion)
- [Travel Vault README](references/vault/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with structured travel planning, route, budget, weather, and source-check details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation or updates of local travel vault notes and budget JSON files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
