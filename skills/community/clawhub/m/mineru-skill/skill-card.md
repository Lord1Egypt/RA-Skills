## Description:

MinerU PDF Parser helps agents convert PDF, Office, HTML, and image inputs into clean Markdown, optional JSON status, extracted assets, and delivery-ready content for supported knowledge tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsekaluk](https://clawhub.ai/user/tsekaluk)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to parse documents into Markdown for review, summarization, RAG preparation, and delivery into supported note, content, and work tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote delivery integrations can forward parsed Markdown and referenced local assets to configured third-party destinations.

Mitigation: Use remote sinks only with trusted documents and trusted destinations, and review generated Markdown and image references before delivery.

Risk: Cloud parsing can upload source documents to MinerU services, which may be unsuitable for confidential, regulated, or air-gapped content.

Mitigation: Avoid confidential or regulated files unless an offline path is selected and verified for the document type.

Risk: The security scanner marked the release suspicious and specifically warns about local image path handling and redirect behavior.

Mitigation: Review before installing, treat parsed Markdown as untrusted, and prefer pinned install commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tsekaluk/skills/mineru-skill)
- [MinerU Home](https://mineru.net)
- [MinerU API Docs](https://mineru.net/apiManage/docs)
- [MinerU Token Management](https://mineru.net/apiManage/token)
- [API Reference](references/api_reference.md)
- [Delivery Integrations](references/integrations.md)
- [Comparison Reference](references/comparison.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, files, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON status, local files, and concise command/configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce parsed Markdown, extracted image files, optional chunk JSON, and delivery outcomes for configured sinks.]

## Skill Version(s):

3.3.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
