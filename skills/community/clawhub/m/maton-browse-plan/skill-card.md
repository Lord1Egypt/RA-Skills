## Description:

Guides agents to help users install the Maton browsing capture extension and use exported matonPlan signals with API Gateway to suggest Maton OAuth connectors based on real browsing activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robert0812](https://clawhub.ai/user/robert0812)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect browsing-derived Maton plan signals with the API Gateway skill, compare those signals with existing Maton connections, and ask before starting relevant OAuth connector flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to a browser extension that can access browsing history and tabs and make browsing-derived plans available to an agent.

Mitigation: Install only when comfortable with those permissions, review captured data before sharing it, and prefer one-shot downloaded JSON for tighter control.

Risk: The skill can repeatedly read browsing-derived data through a local relay when the relay is running.

Mitigation: Run the relay only when needed, use the narrowest browser and install option available, and fall back to downloaded JSON when continuous relay access is unnecessary.

Risk: The optional native-host installer expands local browser integration for popup-controlled relay start and stop.

Mitigation: Avoid the native-host installer unless that control is needed and verify the browser extension ID before registering it.

## Reference(s):

- [Maton browse plan homepage](https://github.com/Robert0812/maton-browse-plan)
- [Maton API Plan browsing capture Chrome Web Store listing](https://chromewebstore.google.com/detail/dgecpbbjdgiindogaboidejihbmkhnai)
- [API Gateway skill](https://clawhub.ai/byungkyu/api-gateway)
- [Maton plan JSON schema](https://maton-browse-plan/schema/maton-plan/v1.json)
- [ClawHub skill page](https://clawhub.ai/robert0812/skills/maton-browse-plan)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MATON_API_KEY for Maton operations; uses user-provided or relay-fetched matonPlan JSON as input evidence.]

## Skill Version(s):

1.3.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
