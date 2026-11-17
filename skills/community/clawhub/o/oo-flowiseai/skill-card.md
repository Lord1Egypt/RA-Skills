## Description:

Use this skill to read a connected FlowiseAI chatflow and send JSON-only prediction requests through OOMOL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can inspect the chatflow protected by their connected FlowiseAI API key and send JSON-only prediction requests. Prediction requests are write actions and require confirmation of the payload and effect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs downloaded CLI installers that were unavailable for inspection.

Mitigation: Review and approve the CLI installation separately before allowing setup to run.

Risk: Prediction requests submit FlowiseAI data through the OOMOL-connected integration.

Mitigation: Trust OOMOL with the submitted data and retain the skill's confirmation requirement for prediction requests.

## Reference(s):

- [FlowiseAI API documentation](https://docs.flowiseai.com/api-reference/chatflows)
- [FlowiseAI](https://flowiseai.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [ClawHub release](https://clawhub.ai/oomol/skills/oo-flowiseai)

## Skill Output:

**Output Type(s):** [API responses, JSON, Shell commands, Guidance]

**Output Format:** [JSON action responses and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses contain chatflow or prediction data; request fields follow the live action schema.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
