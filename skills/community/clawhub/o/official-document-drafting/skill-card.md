## Description:

公文写作 helps agents draft, revise, summarize, standardize, and export Chinese official documents and formal administrative materials using document-type rules, fact boundaries, and layout profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaohui-yang](https://clawhub.ai/user/zhaohui-yang)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and agents use this skill to prepare Chinese official-document drafts, administrative reports, briefings, notices, requests, replies, meeting minutes, speeches, work plans, and similar formal texts. It is suited for structure selection, formal wording, placeholder-based fact handling, Markdown drafts, and optional Word export before human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional font workflow downloads mutable font binaries without integrity checks and can install fonts persistently for the user.

Mitigation: Prefer trusted local fonts, verify downloaded font hashes independently, and review the font scripts before running them.

Risk: Official or administrative drafts can create policy, legal, confidentiality, privacy, or operational risk if unverified facts are treated as final text.

Mitigation: Keep missing information as placeholders or marked for verification, and require review by authorized personnel before formal use or external submission.

## Reference(s):

- [Project homepage](https://github.com/zhaohui-yang/official-document-drafting)
- [ClawHub skill page](https://clawhub.ai/zhaohui-yang/skills/official-document-drafting)
- [文种说明](references/document-types.md)
- [字体速查](references/font-usage.md)
- [版式规范](references/layout-rules.md)
- [行文规范](references/style-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, guidance]

**Output Format:** [Markdown drafts with optional DOCX files and shell commands for validation or export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses placeholders for missing facts and requires human review for official, policy-sensitive, legal-sensitive, confidential, privacy-sensitive, or externally submitted documents.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
