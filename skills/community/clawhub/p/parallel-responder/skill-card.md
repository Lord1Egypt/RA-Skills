## Description:

Parallel Responder helps an agent classify requests, estimate work duration, choose a direct, reporting, or sub-agent execution posture, and generate progress updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lsa03](https://clawhub.ai/user/lsa03)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators can use this skill to add request classification, time estimates, and progress-message patterns for conversational agents handling simple, medium, or complex user tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may tell users that background agents and scheduled progress reporting are active when the implementation is incomplete or only returning status messages.

Mitigation: Review behavior before installation, require explicit confirmation before sub-agent use, and add clear cancellation, cleanup, and retention limits before sensitive use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lsa03/skills/parallel-responder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown progress updates, JSON-like task estimates, JavaScript module results, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes time estimates, classification metadata, task IDs, progress percentages, ETA fields, and completion summaries when invoked through its helper scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version section)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
