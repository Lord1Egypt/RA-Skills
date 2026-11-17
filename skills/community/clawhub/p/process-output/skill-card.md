## Description:

Emits machine-parseable openclaw-process JSON progress blocks so compatible clients can render assistant progress and final status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2719040953](https://clawhub.ai/user/2719040953)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub users use this skill to standardize assistant replies into structured progress events for clients that render live process updates. It is suited to workflows that benefit from predictable start, step, and final JSON status blocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly changes default assistant output into openclaw-process JSON blocks for most replies.

Mitigation: Enable it only where structured progress blocks are desired, and narrow use to explicit opt-in contexts when normal prose responses are expected.

Risk: Its tool-use policy could conflict with platform, developer, or task-specific requirements.

Mitigation: Treat platform, developer, and task-specific instructions as higher priority and review deployments for instruction conflicts before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown containing fenced openclaw-process JSON blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses start, optional step, and final event objects; lightweight mode may emit only start and final blocks.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
