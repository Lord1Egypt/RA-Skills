## Description:

Generates complete music tracks from text descriptions or style requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrshu](https://clawhub.ai/user/lrshu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to submit music prompts to a remote generation service and retrieve generated music results. It is intended for text-to-music workflows where the user provides a style or description.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill forces direct Python execution.

Mitigation: Review and justify or remove the direct-execution instruction before routine use.

Risk: Prompts, credentials, and selected local files may be sent to a configurable remote service.

Mitigation: Use a narrowly scoped TEAM_API_KEY, trust the TEAM_BASE_URL destination before setting it, and avoid passing local file paths unless upload is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lrshu/skills/lrshuai-music-generation)
- [ClawHub publisher profile](https://clawhub.ai/user/lrshu)
- [Default remote API endpoint](https://dlazy.com/api/ai/tool)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Command-line text and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python and TEAM_API_KEY; may also use TEAM_BASE_URL to choose the remote service endpoint.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
