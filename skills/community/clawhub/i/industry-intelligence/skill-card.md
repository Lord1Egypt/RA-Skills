## Description:

行业情报 — 构建并维护某一行业的竞争对手资源库，持续采集监管动态/政策动态、媒体关注、企业官方发布、业务动态、企业数智化动态、国际同行、江湖传闻七大类信息，评估可信度与影响力，生成简报或详报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[citywanderr](https://clawhub.ai/user/citywanderr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to build reusable competitor resource libraries for an industry, collect current intelligence across official, media, international, and community sources, and generate concise or detailed reports. Developers can also use its templates and helper scripts to produce Markdown reports, optional PDFs, and collection logs in a workspace-scoped output directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs through browser automation and helper scripts without network-safety limits.

Mitigation: Install only in a sandboxed environment with restricted outbound network access, private-network and metadata-IP blocking, and workspace-scoped file permissions; review or patch URL fetchers before using untrusted resource files.

Risk: Generated reports include mandatory attribution that may not fit user-controlled or organization-branded reporting.

Mitigation: Remove or adjust attribution before using reports where branding, confidentiality, or user control requires it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/citywanderr/skills/industry-intelligence)
- [Artifact README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Resource Library Template](artifact/templates/resource.md)
- [Detail Report Template](artifact/templates/detail-report.md)
- [Brief Report Template](artifact/templates/brief-report.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files, optional PDF reports, resource-library files, and collection logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written under a workspace-scoped industry-intelligence directory; detailed reports can degrade to Markdown-only when PDF generation fails.]

## Skill Version(s):

1.3.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
