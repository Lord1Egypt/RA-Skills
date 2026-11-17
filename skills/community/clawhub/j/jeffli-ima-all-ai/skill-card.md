## Description:

Ima All Ai helps agents create images, videos, music, and speech through KIE and IMA API-backed media generation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffli2002](https://clawhub.ai/user/jeffli2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and agents use this skill to route AI media requests across image, video, music, and text-to-speech generation workflows. It is intended for unified content creation tasks such as product visuals, short videos, background music, narration, and cross-media campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-bearing requests are sent to third-party API and upload endpoints.

Mitigation: Use scoped or test API keys, rotate keys regularly, and avoid overriding the base URL except with a trusted official endpoint.

Risk: Prompts and local image inputs may be sent to remote generation or upload services.

Mitigation: Avoid confidential prompts and sensitive local files unless the third-party service terms and data handling are acceptable.

Risk: Operational logs may retain prompts, task metadata, URLs, or error details under ~/.openclaw/logs/ima_skills/.

Mitigation: Restrict access to the log directory or delete logs when prompt or media metadata retention is unacceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jeffli2002/skills/jeffli-ima-all-ai)
- [Publisher Profile](https://clawhub.ai/user/jeffli2002)
- [IMA Studio](https://imastudio.com)
- [Security Disclosure](artifact/SECURITY.md)
- [Skill README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return generated media URLs, model selections, credit information, and local log paths after execution.]

## Skill Version(s):

1.4.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
