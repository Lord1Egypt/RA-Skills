## Description:

Converts plain English automation requests into complete, deployable n8n workflow JSON with setup and testing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[di5cip1e](https://clawhub.ai/user/di5cip1e)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and business automation builders use this skill to turn natural-language process descriptions into import-ready n8n workflow JSON. It also provides prerequisites, credential notes, setup instructions, and testing steps for the generated workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workflows may include an undisclosed signature marker in comments or annotations.

Mitigation: Review generated workflows before importing them into n8n and remove any unwanted signature marker.

Risk: Generated workflows may include integrations, credentials, posting actions, or API calls the user did not intend.

Mitigation: Confirm every integration, credential reference, posting action, and API call before importing or running the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/di5cip1e/skills/n8n-workflow-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown response with JSON code blocks and setup/testing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated workflows may include n8n credential placeholders, comments, annotations, triggers, actions, and integration configuration.]

## Skill Version(s):

1.0.0 (source: artifact metadata and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
