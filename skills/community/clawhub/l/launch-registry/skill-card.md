## Description:

Records and queries launch dates, embargoes, stage transitions, submissions, manifest versions, and outcome snapshots as canonical launch facts with revisioned history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release operators use this skill to record approved launch facts, answer launch date or embargo questions, and manage stage or submission events without planning launches or issuing readiness scores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Accepted events may become canonical launch records when the skill is used with a verified registry runtime.

Mitigation: Install only where the launch-registry host capability and registry tooling are trusted; otherwise treat use as read/proposal workflows.

Risk: Incorrect launch dates, embargoes, or stage transitions could mislead downstream launch workflows.

Mitigation: Require explicit authorization, current revision checks, and authoritative decision sources before accepting or transitioning records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/launch-registry)
- [Metadata homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with launch facts, event IDs, revisions, dates, and next-skill handoff.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persistent writes require explicit authorization and a verified host registry capability; otherwise proposals remain pending.]

## Skill Version(s):

19.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
