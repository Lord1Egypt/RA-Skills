## Description:

Long Task Handler V2 helps agents manage work expected to run longer than 60 seconds by estimating duration, running appropriate tasks in the background, reporting quantified progress, and surfacing completion or issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrislawyeryounger-spec](https://clawhub.ai/user/chrislawyeryounger-spec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to keep long-running compile, deploy, training, migration, data processing, search, crawling, and multi-step writing tasks visible through early estimates, regular progress reports, and explicit completion or issue notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation rules may cause an agent to move likely long-running work into background execution or sub-agent handling without the user's explicit confirmation.

Mitigation: Review the activation rules and require explicit confirmation for background execution or sub-agent use in environments that need tighter operator control.

Risk: Progress estimates and percentages may be approximate for tasks with unclear step counts, silent commands, rate limits, or network delays.

Mitigation: Treat estimates as status guidance, require issue reports for silence or errors, and verify final command results before relying on task completion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chrislawyeryounger-spec/skills/long-task-handler-v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown progress updates with inline status, estimates, completion notices, and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Periodic reporting defaults to two-minute progress updates and a five-minute silent-task warning threshold.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
