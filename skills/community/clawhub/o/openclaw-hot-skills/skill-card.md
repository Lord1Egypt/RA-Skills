## Description:

Discover trending, must-have, and topic-specific high-value skills from ClawHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tengj](https://clawhub.ai/user/tengj)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to discover trending, must-have, and topic-specific ClawHub skills, compare candidates, see local installation status, and decide what to inspect or install next.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or invoke the `clawhub` CLI, query the ClawHub registry, and list locally installed skills.

Mitigation: Confirm the ClawHub CLI source and version in sensitive environments before use.

Risk: Recommended skills may carry separate security or permission risks if installed without review.

Mitigation: Inspect and scan each recommended skill before allowing installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tengj/skills/openclaw-hot-skills)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown shortlist with ranked items, ClawHub links, installation status, and recommended next actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Matches the user's language and may include CLI-backed popularity metrics when available.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
