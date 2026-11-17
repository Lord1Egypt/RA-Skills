## Description:

Professional Patent Agents is a multi-agent suite for patent ideation, prior-art search, inventiveness evaluation, drafting, claims design, quality audit, valuation, and Markdown-to-Word conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigpipihua](https://clawhub.ai/user/bigpipihua)

### License/Terms of Use:

MIT

## Use Case:

Developers, inventors, patent teams, and IP service providers use this skill to turn technical ideas, draft patent documents, or agency feedback into patent-oriented reports, optimized drafts, claims structures, audit findings, and optional Word documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marked the release suspicious because it asks agents to install newly discovered skills, persist learned behavior globally, and run risky conversion setup or execution steps without enough user control.

Mitigation: Review before installing, disable or tightly review continuous learning and global instincts, and require approval before installing additional ClawHub skills.

Risk: The security guidance warns against the curl-to-bash setup path and unpinned dependency installation.

Mitigation: Do not run the curl-to-bash setup as written; pin and verify dependencies, and use an isolated non-root environment.

Risk: Patent files may contain confidential invention data, and the skill can perform search, conversion, or external API-assisted workflows.

Mitigation: Confirm every patent file path and external API use before search, conversion, or upload, and avoid sending confidential material to unapproved services.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bigpipihua/skills/professional-patent-agents)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and patent drafts, optional DOCX files, shell command snippets, configuration notes, and guidance text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual output is supported; patent conversion may require local document and diagram tooling.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
