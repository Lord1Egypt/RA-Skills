## Description:

用于按审稿意见完成论文诊断、批注、分级改写和终审自检的学术论文润色修改 SOP。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuwenqi123123](https://clawhub.ai/user/liuwenqi123123)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, authors, editors, and writing support agents use this skill to revise academic manuscripts against reviewer comments, journal constraints, AI-writing-pattern checks, and final quality criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may expose manuscript, reviewer, or unpublished research content if shared broadly or hosted on a trusted web origin.

Mitigation: Keep generated reports in a controlled local output location and review excerpts before distribution.

Risk: The server security verdict notes under-disclosed browser, network, and injection risks in generated HTML reports.

Mitigation: Avoid using the skill on confidential material unless the CDN script is disabled or replaced and HTML escaping issues are fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liuwenqi123123/skills/paper-revision-sop)
- [AI Writing Flavor Pattern Lexicon](references/ai-flavor-patterns.md)
- [Final Quality Checklist](references/quality-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance, JSON diagnostics, HTML reports, and revised DOCX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports may include source manuscript excerpts and should be handled as sensitive local files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
