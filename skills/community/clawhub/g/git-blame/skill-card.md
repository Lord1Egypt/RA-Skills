## Description:

Production code audit via git blame with natural-language risk analysis for overtime commits, scattered changes, no-PR-review merges, and impact domain tracing for suspicious lines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security auditors, tech leads, and on-call engineers use this skill to inspect git blame data for code safety concerns, author patterns, review gaps, and affected domains during audits or incident triage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can surface local git history, author identities, commit timing, and other repository metadata.

Mitigation: Use it only in repositories where the agent is allowed to inspect and summarize that metadata.

Risk: Broad audit requests may inspect more repository history than intended.

Mitigation: Prefer explicit targets such as a file path and line number when a narrow review is sufficient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/git-blame)
- [Project homepage](https://github.com/harry)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown risk reports with inline shell commands and structured findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include risk scores, author and commit metadata, impact domains, and recommended review actions.]

## Skill Version(s):

1.0.0 (source: release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
