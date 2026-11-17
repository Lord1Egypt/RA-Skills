## Description:

Phy Social Suite runs a social media pre-publish pipeline that retrieves content atoms, audits AI signature, checks platform rules, and returns a combined PASS/WARN/FAIL verdict with suggested fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Social media operators, marketers, and agent-assisted content teams use this skill to run a single pre-publish review flow for LinkedIn, Reddit, Twitter/X, and Hacker News drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The pipeline dynamically imports local component skill scripts from user directories, including a Desktop fallback path.

Mitigation: Install and run only trusted component skills, review the resolved script paths before use, and remove or avoid the Desktop fallback path in production environments.

Risk: The final all-clear message can appear when checks are skipped or exceptions are swallowed.

Mitigation: Treat skipped stages and load errors as review blockers, and require explicit successful outputs from the humanizer and platform-rules stages before publishing.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-social-suite)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text report with Markdown-style sections and CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local component skills when installed; missing or failing checks may still allow a final all-clear message.]

## Skill Version(s):

1.0.3 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
