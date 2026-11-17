## Description:

Priority-based message delivery with urgency levels over the Pilot Protocol network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send, review, filter, and triage Pilot Protocol messages by priority prefix, especially for urgent communications or SLA-oriented workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clearing a priority inbox after processing may remove messages the user still needs.

Mitigation: Review inbox contents and confirm retention needs before running `pilotctl --json inbox --clear`.

Risk: Priority labels are prefix-based, so missing or inconsistent prefixes can cause messages to be triaged at the wrong urgency.

Mitigation: Use consistent `[CRITICAL]`, `[HIGH]`, and `[LOW]` prefixes and review untagged messages before acting on the queue.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-priority-queue)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the pilot-protocol skill, pilotctl binary on PATH, jq for filtering examples, and a running Pilot Protocol daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
