## Description:

MusicGenerator helps users create AI-generated songs and audio tracks through the MakeBestMusic service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sthk-mbm](https://clawhub.ai/user/sthk-mbm)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, musicians, and developers use this skill to request custom AI-generated music with or without vocals, then check generation status and retrieve completed track links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the user's MakeBestMusic API key, music prompts, and task/status information to an external service.

Mitigation: Use a dedicated MakeBestMusic key, avoid confidential lyrics or private project ideas, and review the service terms before use.

Risk: The MBM_API_BASE environment variable can change the endpoint used by the scripts.

Mitigation: Run the skill only in an environment where MBM_API_BASE is unset or controlled by a trusted operator.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sthk-mbm/skills/musicgenerator)
- [MakeBestMusic Website](https://makebestmusic.com/?pid=PIDcLjhgCXUQ)
- [MakeBestMusic API Endpoint](https://api.makebestmusic.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON status results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MakeBestMusic apiKey; generation returns music IDs and status checks return processing, failed, or completed results with track links when available.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
