## Description:

Jd Translator analyzes job descriptions and turns role requirements into a structured interview-preparation report focused on business problems, capability mapping, key questions, and interview strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers, career coaches, and recruiting-preparation agents use this skill to convert a complete job description into a problem-oriented interview preparation plan. It helps identify business, team, and role-level problems, map JD requirements to employer needs, and draft self-introduction, follow-up questions, and resume-positioning guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Job descriptions, employer context, or candidate materials may contain private or sensitive information.

Mitigation: Remove confidential details before use and rely on public or approved company information when adding background research.

Risk: The generated interview strategy may include assumptions about the company, team, or role that are incomplete or wrong.

Mitigation: Review the analysis against the original JD and authoritative company sources before using it in interview preparation.

Risk: The skill is primarily written for Chinese-language JD workflows and may require adaptation for other hiring markets or languages.

Mitigation: Adjust terminology, examples, and market assumptions to match the target role, geography, and interview context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lj22503/skills/jd-translator)
- [Four-layer framework](artifact/references/four-layer-framework.md)
- [C-end JD analysis example](artifact/examples/c-end-analysis.md)
- [B-end JD analysis example](artifact/examples/b-end-analysis.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with optional plain-text parser output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a complete job description; the optional parser reads JD text from stdin or command-line arguments and prints extracted keywords, collaboration targets, capability requirements, and job-type signals.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
