## Description:

Task auction system where agents bid and a requester selects the best offer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a task auction where agents compete on price, speed, or quality and the requester selects a bidder before awarding work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task details can be sent to an unverified bidder selected from inbox messages.

Mitigation: Use trusted or authenticated bidder identities and require requester confirmation before awarding a task.

Risk: Task specifications may contain private, proprietary, customer, or credential-bearing information.

Mitigation: Review task content before publishing an auction and avoid sharing sensitive data with untrusted bidders.

Risk: The example bid collection path uses a predictable /tmp file pattern.

Mitigation: Use a securely created private temporary directory for bid files.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [Pilot Auction on ClawHub](https://clawhub.ai/teoslayer/skills/pilot-auction)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, jq, a running Pilot daemon, and trusted bidder identities.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; skill frontmatter lists 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
