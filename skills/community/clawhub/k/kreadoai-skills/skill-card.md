## Description:

KreadoAI Skills helps an agent call KreadoAI for digital avatar video generation, text-to-speech, instant avatar cloning, and subtitle or watermark removal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shifefiei](https://clawhub.ai/user/shifefiei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to route agent requests to KreadoAI account, avatar, video, clone, text-to-speech, and subtitle tools. It is intended for workflows that create or inspect KreadoAI-generated media through the provider API.

### Deployment Geography for Use:

Global; the artifact notes that the KreadoAI service is deployed in Singapore and may be slower for users in China.

## Known Risks and Mitigations:

Risk: Real KreadoAI account credentials may be used by this skill.

Mitigation: Prefer KREADO_API_TOKEN from a controlled environment, avoid passing tokens in visible shell commands, and rotate any token that may have entered shell history or logs.

Risk: The skill can submit text, photos, videos, and watermark-removal jobs to KreadoAI for processing.

Mitigation: Only submit media and text that the user is authorized to process and that is appropriate for a third-party API workflow.

Risk: The security verdict is suspicious because credential handling and sensitive media workflows require review before installation.

Mitigation: Review the skill and its credential configuration before using real credentials or sensitive media.

## Reference(s):

- [KreadoAI API Documentation](https://kreadoai.gitbook.io/kreadoai)
- [KreadoAI OpenAPI](https://www.kreadoai.com/openapi)
- [ClawHub Skill Page](https://clawhub.ai/shifefiei/skills/kreadoai-skills)
- [Publisher Profile](https://clawhub.ai/user/shifefiei)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+ and a KreadoAI API token for live API calls.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
