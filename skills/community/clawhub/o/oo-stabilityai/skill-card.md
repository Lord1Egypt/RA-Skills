## Description:

Stability AI (stability.ai). Use this skill for ANY Stability AI request — reading, creating, and updating data. Whenever a task involves Stability AI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can generate audio from text prompts with Stability AI through their OOMOL-connected account. The skill guides them through checking the connector action schema and submitting a matching request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified software, and startup synchronization may change other agents' skills.

Mitigation: Verify the oo CLI release and explicitly approve local installation; set OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization.

Risk: Prompts and generated audio pass through OOMOL and Stability AI, and audio is uploaded to connector storage.

Mitigation: Send only prompts and audio content suitable for processing by those services and storage in connector transit.

## Reference(s):

- [Stability AI API documentation](https://platform.stability.ai/docs/api-reference)
- [Stability AI](https://stability.ai)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Audio files, API responses, Shell commands]

**Output Format:** [Generated audio files and JSON action responses, with shell command examples in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audio is uploaded to connector transit storage.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
