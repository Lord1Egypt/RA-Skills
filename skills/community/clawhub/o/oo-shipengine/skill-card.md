## Description:

ShipEngine (shipengine.com). Use this skill for ANY ShipEngine request — searching and reading data. Whenever a task involves ShipEngine, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Operations teams and developers can use the connected ShipEngine account to calculate or estimate shipping rates, retrieve rates, list carriers, and parse or validate mailing addresses. The skill guides agents to inspect each action's schema before submitting its inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs execution of a remote CLI installer, and automatic skill synchronization may introduce unreviewed changes.

Mitigation: Approve CLI installation separately, verify a specific release, and review or disable automatic skill synchronization.

Risk: Connecting ShipEngine allows OOMOL to process the shipping details submitted through the skill.

Mitigation: Submit only shipping details that are appropriate to share through the connected service.

## Reference(s):

- [ShipEngine](https://www.shipengine.com/)
- [ShipEngine API authentication documentation](https://www.shipengine.com/docs/auth/)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action inputs and results with concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs vary by operation; inspect the action schema before use.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
