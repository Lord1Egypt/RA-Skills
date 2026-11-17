## Description:

Gstack Pro turns an AI assistant into a structured software engineering team with roles for product planning, architecture, design review, code review, QA, shipping, retrospectives, and release documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to structure an AI-assisted development workflow across planning, architecture, design review, code review, browser QA, release, retrospectives, and documentation updates. It is suited to feature work, code review, QA runs, and release preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The QA and shipping workflows can lead an agent to make code changes, drive a browser session, run git operations, and push branches with high impact.

Mitigation: Require explicit confirmation of the target URL, repository, branch, staged file list, staged diff, and every git push before running QA or shipping workflows.

Risk: Running the ship workflow on protected branches or repositories with local secrets can expose sensitive data or create unwanted release changes.

Mitigation: Avoid protected branches and sensitive repositories unless branch protections, review gates, and secret scanning are in place.

## Reference(s):

- [Gstack Pro Skill Page](https://clawhub.ai/zmy1006-sudo/skills/gstack-pro)
- [Publisher Profile](https://clawhub.ai/user/zmy1006-sudo)
- [GStack](https://gstacks.org)
- [CEO Product Thinking SOP](references/plan-ceo.md)
- [Architecture Review SOP](references/plan-eng.md)
- [Automated QA SOP](references/qa.md)
- [Engineering Retro SOP](references/retro.md)
- [Paranoid Code Review SOP](references/review.md)
- [One-Command Ship SOP](references/ship.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with code blocks, shell commands, checklists, tables, and structured JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Health Score reports, QA findings, release reports, review findings, architecture plans, and retrospective summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
