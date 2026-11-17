## Description:

Use AIsa for model routing, provider setup, and Chinese LLM access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure AIsa-backed model routing, inspect supported model options, and prepare workflows for Chinese LLM access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, messages, and image URLs are sent to AIsa and may be routed to downstream model providers.

Mitigation: Use the skill only for data allowed by the user's AIsa account terms and downstream provider policies; avoid secrets, private documents, and sensitive image URLs.

Risk: API-backed operations require an AISA_API_KEY credential.

Mitigation: Provide the key through the expected environment variable and avoid pasting credentials into prompts, command arguments, or shared logs.

## Reference(s):

- [LLM Router ClawHub Skill Page](https://clawhub.ai/baofeng-tech/skills/llm-router)
- [baofeng-tech Publisher Profile](https://clawhub.ai/user/baofeng-tech)
- [AIsa API Endpoint](https://api.aisa.one/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; bundled CLI commands return JSON or streamed text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [AISA_API_KEY is required for API-backed chat, vision, and compare operations; model listing can run without an API key.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
