## Description:

Generates a 400-500 character cultural relic narration from a relic name, optional museum and audience context, and a configured OpenAI-compatible model API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangzw0707](https://clawhub.ai/user/jiangzw0707)

### License/Terms of Use:

MIT-0

## Use Case:

Museum educators, cultural content creators, and agent users can use this skill to draft Chinese narration for cultural relics and museum exhibits with audience-adapted style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials can be stored in config/user_config.json and sent to the configured API endpoint.

Mitigation: Treat config/user_config.json as a secret, keep it out of shared workspaces, use HTTPS or trusted local loopback endpoints, and rotate keys exposed to untrusted endpoints.

Risk: Relic, museum, audience, and question details are included in prompts sent to the configured model API.

Mitigation: Avoid entering sensitive or unpublished collection details unless the selected endpoint and data handling terms are approved.

## Reference(s):

- [Cultural Relics Guide ClawHub listing](https://clawhub.ai/jiangzw0707/skills/guide)

## Skill Output:

**Output Type(s):** [text, files, configuration, shell commands]

**Output Format:** [Plain text narration with optional saved .txt output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local configuration file with API endpoint, API key, narration model, optional style model, and timeout.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
