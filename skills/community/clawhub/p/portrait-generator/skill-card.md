## Description:

Generates hyper-detailed AI portraits through the ComfyDeploy Morfeo Portrait workflow with structured control over facial features such as eyes, nose, lips, jawline, skin, hair, and expression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pauldelavallaz](https://clawhub.ai/user/pauldelavallaz)

### License/Terms of Use:


## Use Case:

Content creators, campaign teams, and agent users use this skill to turn natural-language portrait requests into structured ComfyDeploy Morfeo Portrait parameters and retrieve generated portrait outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portrait descriptions and structured facial attributes are sent to ComfyDeploy.

Mitigation: Avoid using the skill for real people or sensitive personal traits unless consent and the external service's privacy, retention, and access controls have been reviewed.

Risk: The skill depends on an external ComfyDeploy API service to generate and retrieve portrait outputs.

Mitigation: Confirm the service is available and that API credentials are handled through approved secret-management practices before use.

## Reference(s):

- [ClawHub Portrait Generator skill page](https://clawhub.ai/pauldelavallaz/skills/portrait-generator)
- [Publisher profile](https://clawhub.ai/user/pauldelavallaz)
- [ComfyDeploy queue endpoint](https://api.comfydeploy.com/api/run/deployment/queue)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Image URL]

**Output Format:** [Structured JSON request parameters followed by a generated portrait image URL when the external run succeeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses predefined portrait attribute values where available and free-text brief details for unmapped attributes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
