## Description:

Run personalized email outreach campaigns via Lemlist. Manage campaigns, sequences, and tasks, track lead engagement, search people and company databases, and automate outreach workflows with labeling and scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and sales teams use this skill to manage Lemlist outreach workflows, including campaigns, leads, sequences, schedules, tasks, suppression lists, analytics, and team information through a connected Lemlist account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned external plugin for OAuth-backed Lemlist access.

Mitigation: Review the ClawLink plugin source, publisher, version, and update policy before installing or enabling it.

Risk: Lemlist write operations can affect campaigns, lead statuses, schedules, unsubscribe or suppression settings, and exports.

Mitigation: Connect an account with the minimum needed permissions and verify previews before any write operation.

## Reference(s):

- [Lemlist API Documentation](https://docs.lemlist.com/)
- [Lemlist Campaign Management](https://help.lemlist.com/en/)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/lemlist-outreach)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute Lemlist read and write operations through ClawLink after connection checks and user confirmation for writes.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
