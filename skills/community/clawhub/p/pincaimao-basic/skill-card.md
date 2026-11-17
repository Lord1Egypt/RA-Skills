## Description:

聘才猫平台基础能力 Use when calling any Pincaimao platform API: file upload, presigned URL, conversation list, message history, audio-to-text, resume JSON upload, or the base chat-messages interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pincaimao](https://clawhub.ai/user/pincaimao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building Pincaimao agent skills use this shared helper to call authenticated Pincaimao platform APIs for chat messages, file upload, temporary file links, conversation retrieval, audio-to-text, and resume JSON upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send resumes, uploaded files, job descriptions, contract text, audio-derived text, and conversation history to Pincaimao's hosted API.

Mitigation: Use it only with data you are authorized to share with api.pincaimao.com under the configured API key.

Risk: Returned cos_key values and presigned links may grant access to uploaded content.

Mitigation: Treat cos_key values and presigned links as sensitive and avoid exposing them in logs, tickets, or shared chat transcripts.

## Reference(s):

- [Pincaimao Homepage](https://www.pincaimao.com)
- [Pincaimao ClawHub Skill Page](https://clawhub.ai/pincaimao/skills/pincaimao-basic)
- [Pincaimao Publisher Profile](https://clawhub.ai/user/pincaimao)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON examples and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses authenticated HTTPS API calls to api.pincaimao.com and returns API response fields such as answers, conversation IDs, uploaded file cos_key values, presigned URLs, and transcription text.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
