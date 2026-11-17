## Description:

Unified inbox for incoming Pilot Protocol messages, files, tasks, and trust requests in one view.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Pilot Protocol users use this skill to inspect and triage incoming messages, received files, received tasks, and pending trust requests from one inbox workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup examples can clear inbox items or received files.

Mitigation: Review inbox and received-file contents first, and run --clear commands only when intentional.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [Pilot Inbox on ClawHub](https://clawhub.ai/teoslayer/skills/pilot-inbox)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code]

**Output Format:** [Markdown with inline and fenced bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the pilotctl binary, a running Pilot Protocol daemon, and jq for the workflow example.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
