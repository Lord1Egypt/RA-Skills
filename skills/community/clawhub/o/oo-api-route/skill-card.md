## Description:

Use API Route through an OOMOL-connected account to list models or generate chat completions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use this skill to check which models are available or request chat completions through their connected API Route account. Chat completions are billed, so users should authorize the request and set spending limits before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat-completion requests are billed and send prompts to API Route for processing.

Mitigation: Require clear authorization and spending limits, and send only prompts intended for API Route to process.

Risk: The setup instructions can run a downloaded installer and may install additional agent skills.

Mitigation: Review and pin the CLI installation separately, and inspect any additional skills it installs.

## Reference(s):

- [API Route documentation](https://www.api-route.com/zh/docs/overview)
- [API Route homepage](https://www.api-route.com)
- [ClawHub skill listing](https://clawhub.ai/oomol/skills/oo-api-route)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API responses, Text, JSON]

**Output Format:** [Text and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated chat-completion text or a list of model IDs.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
