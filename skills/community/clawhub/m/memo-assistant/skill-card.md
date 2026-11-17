## Description:

Classifies user memos and appends them to category-specific Markdown files under ~/.memo when triggered by /private-secretary or /ps commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanchenxm](https://clawhub.ai/user/tristanchenxm)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as a personal memo assistant to classify short notes and keep them organized in local Markdown files. It is intended for memo capture and reorganization through the /private-secretary or /ps commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented shell write command can execute user-provided memo text as shell code.

Mitigation: Rewrite memo storage to pass content literally without shell interpolation before using this skill with untrusted or sensitive content.

Risk: Memo text is written under ~/.memo and can persist across sessions.

Mitigation: Avoid recording sensitive content unless local retention is acceptable, and review the stored Markdown files when removing retained notes.

Risk: The rearrange behavior may rewrite existing local memos.

Mitigation: Clarify the rearrange workflow with user confirmation and rollback or backup behavior before reorganizing stored notes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tristanchenxm/skills/memo-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown memo entries appended by shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Categorizes memo content as Tech, Work, Life, Inspiration, or Others and stores entries under ~/.memo.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
