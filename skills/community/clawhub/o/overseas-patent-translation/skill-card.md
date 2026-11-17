## Description:

Translates and formats Chinese patent application materials for Europe, United States, Japan, and Korea filings while preserving claim scope, terminology consistency, and jurisdiction-specific structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent teams, patent agents, and technical translators use this skill to convert Chinese claims, specifications, abstracts, drawings notes, priority documents, or technical disclosures into EP, US, JP, or KR filing text. The skill also provides terminology glossaries, jurisdiction-specific formatting, and concise translation QA or risk notes.

### Deployment Geography for Use:

Global; outputs are tailored for Europe, United States, Japan, and Korea patent filing formats.

## Known Risks and Mitigations:

Risk: The workflow may send confidential or unpublished patent materials to external PatSnap MCP services.

Mitigation: Use external MCP tools only with authorization for the patent materials involved, and confirm which configured MCP service will receive the text before use.

Risk: The required PatSnap MCP service set is broader than basic translation requires.

Mitigation: Install only the MCP services needed for the intended workflow and review enabled tools before processing sensitive materials.

Risk: Patent translations can unintentionally alter claim scope, terminology, or priority support.

Mitigation: Review the generated claims, terminology glossary, section formatting, and QA notes with qualified patent counsel or filing specialists before submission.

## Reference(s):

- [Europe Patent Translation Reference](artifact/references/europe.md)
- [United States Patent Translation Reference](artifact/references/united-states.md)
- [Japan Patent Translation Reference](artifact/references/japan.md)
- [Korea Patent Translation Reference](artifact/references/korea.md)
- [PatSnap Open Platform](https://open.zhihuiya.com/)
- [PatSnap MCP Server Marketplace](https://open.zhihuiya.com/marketplace/mcp-servers)
- [PatSnap Authentication Guide](https://open.zhihuiya.com/devportal/guides/authentication)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance, Configuration instructions]

**Output Format:** [Markdown or plain text patent-application translations with terminology glossaries and QA notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce one output package per selected jurisdiction; PatSnap MCP-backed features require user authorization and configured external services.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
