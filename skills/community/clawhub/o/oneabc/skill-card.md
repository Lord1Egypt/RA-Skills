## Description:

Access OpenAI-, Claude-, DeepSeek-, Sora-, Midjourney-, and Suno-compatible models through the oneabc.io API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xingfan0828](https://clawhub.ai/user/xingfan0828)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to call OneABC-compatible chat, image, video, music, and model-listing endpoints from a local Node wrapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can transmit prompts and API credentials to the configured OneABC-compatible API endpoint.

Mitigation: Use a dedicated OneABC-scoped API key, avoid sending sensitive prompts, and only configure ONEABC_BASE_URL for endpoints you fully trust.

Risk: The script automatically falls back to OPENAI_API_KEY when ONEABC_API_KEY is not set.

Mitigation: Set ONEABC_API_KEY explicitly for this skill and avoid relying on the OPENAI_API_KEY fallback.

## Reference(s):

- [OneABC API endpoint](https://api.oneabc.org)
- [ClawHub skill page](https://clawhub.ai/xingfan0828/skills/oneabc)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a configured ONEABC_API_KEY or intentional OPENAI_API_KEY fallback.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
