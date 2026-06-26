## Description: <br>
Helps agents find lifestyle recommendations for shopping, dining, local services, travel, and everyday decisions based on user intent, budget, preferences, or location. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uoryon](https://clawhub.ai/user/uoryon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to help agents translate shopping, dining, local-service, travel, or everyday-choice requests into structured discovery queries and concise recommendation results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ad-style recommendation links and automatic impression tracking may be under-disclosed to users. <br>
Mitigation: Use the skill only for explicit shopping, dining, local-service, or booking discovery tasks, and inform users when links or impressions may be tracked. <br>
Risk: Broad external searches can send unnecessary location or preference context. <br>
Mitigation: Send only the minimum fields needed for the request, avoid optional profile sharing unless the user explicitly agrees, and use precise location only for delivery or local searches. <br>
Risk: The security review marks the release as suspicious because tracking and external-search behavior are not fully disclosed. <br>
Mitigation: Review the skill before installation and configure agents not to fetch impression URLs unless users are clearly informed and agree. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [Examples & Templates](references/examples.md) <br>
- [Positioning & Use-Case Mapping](references/positioning.md) <br>
- [Privacy & Data Policy](references/privacy.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/uoryon/golgent-lifestyle-discovery) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, API Calls] <br>
**Output Format:** [Markdown recommendation tables with concise text and CTA links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [External recommendation results may include click or tracking URLs; optional profile fields require explicit user consent.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
