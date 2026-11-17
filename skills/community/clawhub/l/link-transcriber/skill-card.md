## Description:

Turn a Douyin or Xiaohongshu link into a concise summary, an actionable todo list, and a recommended reminder time. The hosted service handles the platform access on the server side, and the user only needs to paste the link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobobo2026](https://clawhub.ai/user/bobobo2026)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to turn a supported Douyin or Xiaohongshu link into a concise summary, an actionable todo list, and a recommended reminder time. It is intended for content review and planning workflows where the user wants a structured result without managing platform credentials locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided Douyin or Xiaohongshu links are sent to the publisher-operated hosted service.

Mitigation: Install only when that link sharing is acceptable; use a self-hosted service for privacy-sensitive workflows.

Risk: Backend-provided comment candidates can be relayed verbatim as user-facing comment suggestions.

Mitigation: Review generated comment suggestions before posting or reusing them publicly.

Risk: The documented install commands use a mutable latest package with force installation.

Mitigation: Prefer a pinned, trusted install path or a reviewed release version for managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bobobo2026/skills/link-transcriber)
- [Publisher profile](https://clawhub.ai/user/bobobo2026)
- [Public service endpoint](https://linktranscriber.store)
- [Deployment notes](artifact/docs/DEPLOY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured Chinese sections for summary, todo list, reminder recommendation, and optional comment references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or poll a hosted transcription task, may return backend-provided comment candidates verbatim, and may coordinate a reminder only after user confirmation.]

## Skill Version(s):

0.1.26 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
