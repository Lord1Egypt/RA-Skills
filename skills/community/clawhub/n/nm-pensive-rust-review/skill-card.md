## Description:

Audits Rust code for unsafe blocks, ownership issues, and Cargo dependency risks

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review Rust changes for safety, correctness, concurrency, dependency, performance, and idiom issues before merging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports behavior that may not match the Rust-auditing purpose, install guidance that may change the environment, and incomplete inspection of some files and references.

Mitigation: Review the flagged behavior and install steps, and inspect the files and references that were not fully analyzed before installation.

## Reference(s):

- [ClawHub rust-review release](https://clawhub.ai/athola/skills/nm-pensive-rust-review)
- [Claude Night Market Pensive plugin (metadata homepage)](https://github.com/athola/claude-night-market/tree/master/plugins/pensive)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown Rust audit report with findings, recommendations, and evidence anchors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings should include source locations and verbatim anchors when reported.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
