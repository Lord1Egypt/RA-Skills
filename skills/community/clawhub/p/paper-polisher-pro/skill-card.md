## Description:

Paper Polisher Pro helps academic writers review drafts for AI-like patterns, style and terminology consistency, and disclosure requirements, then provides reports and sentence-level revision suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[docsor1212](https://clawhub.ai/user/docsor1212)

### License/Terms of Use:

MIT-0

## Use Case:

Academic writers use this skill to review their own drafts for writing patterns, consistency, and disclosure requirements, and to get evidence reports and revision guidance. Follow institutional AI-use policies; the skill is not intended to evade academic integrity checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious because scanners report cross-origin access to local MCP tools; the review is incomplete and does not establish that the skill is safe.

Mitigation: Review local MCP exposure and settings before enabling MCP access, and account for the partial scan coverage described in the security guidance.

Risk: ClawScan reports mismatches between the advice-only description and reported editing or verdict behavior.

Mitigation: Inspect outputs before relying on them, keep use focused on reviewing your own writing, and follow institutional AI-use and disclosure policies.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/docsor1212/skills/paper-polisher-pro)
- [Source repository](https://github.com/docsor1212/paper-polisher-pro)
- [ModelScope mirror](https://modelscope.cn/skills/Docsor/paper-polisher-pro)
- [Best practices](artifact/references/best-practices.md)
- [FAQ](artifact/references/faq.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, JSON, Markdown, HTML reports, CSV, Shell commands]

**Output Format:** [Terminal text, JSON, Markdown, HTML, and CSV, depending on the command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-document reports or directory-level batch summaries; short texts under 100 characters receive no AI-risk verdict by design.]

## Skill Version(s):

7.9.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
