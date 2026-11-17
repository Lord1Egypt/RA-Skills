## Description:

Peer review system for task results before acceptance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to request independent review, collect reviewer decisions, and require multi-party approval before accepting task results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The approval workflow can treat unverified or duplicate review messages as independent approvals.

Mitigation: Authenticate reviewer identities, deduplicate submissions, bind each review strictly to the requested task, enforce deadlines, construct JSON safely, and fail closed when checks cannot be completed.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-review)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands assume pilotctl and jq are available, with the Pilot Protocol daemon running.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
