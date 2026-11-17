## Description:

Verify real outcomes before saying work is complete. Use when implementing, fixing, configuring, or automating something where behavior must be confirmed, not just command success or edited text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisang1000](https://clawhub.ai/user/jisang1000)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents and coding assistants use this skill to verify user-visible results after setup work, bug fixes, automation changes, configuration updates, browser flows, or script tasks before reporting completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause the agent to run extra checks, smoke tests, browser inspections, or state inspections before saying work is done.

Mitigation: Review task-specific commands when they affect real systems, and report exactly what was verified and what remains unverified.

## Reference(s):

- [Skill source](SKILL.md)
- [Publish Notes](references/publish-notes.md)
- [Final Review](references/final-review.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown status updates with verification results and any remaining uncertainty]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prompt the agent to run task-appropriate checks before final reporting.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
