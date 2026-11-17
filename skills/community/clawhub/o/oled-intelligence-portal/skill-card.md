## Description:

Generates a Chinese multi-page HTML intelligence portal for a user-provided technology keyword, using AI-assisted company and technology-branch discovery with Patsnap/Zhihuiya news and patent retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technology analysts use this skill to turn a technology keyword into a local HTML intelligence portal covering monitored companies, technology branches, news, major events, and patents. It is intended for users with configured Patsnap/Zhihuiya MCP access who need a generated briefing site rather than a conversational-only report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may include external news, patent, URL, and summary content without adequate sanitization.

Mitigation: Treat generated HTML as untrusted, review it before sharing, and add escaping plus URL validation before relying on it in a broader workflow.

Risk: The generated report writes files to a local output directory without adequate output-path containment.

Mitigation: Run the skill in a dedicated workspace and review the resolved output directory before generation.

Risk: The skill depends on configured Zhihuiya/Patsnap MCP services and account authorization for live retrieval.

Mitigation: Install only in environments where those services and credentials are expected, and confirm MCP configuration before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/oled-intelligence-portal)
- [Zhihuiya Open Platform](https://open.zhihuiya.com/)
- [HTML templates reference](references/html-templates.md)
- [Company mapping reference](references/company-mapping.md)
- [Technology tags reference](references/tech-tags.md)
- [Data processing reference](references/data-processing.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON and Python snippets plus generated multi-page HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated portal writes index.html, company pages, technology pages, and patents.html to a local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
