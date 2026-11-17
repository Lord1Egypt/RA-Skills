## Description:

Maintain and share blocklists of untrusted agents in Pilot Protocol networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and operators of Pilot Protocol networks use this skill to create, maintain, enforce, and share persistent deny-lists for agents they consider malicious, compromised, or untrusted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent trust-revocation and reject commands can remove peers from trust relationships or block pending handshakes.

Mitigation: Review target hostnames and node IDs before execution, require manual confirmation for untrust or reject actions, and keep a recoverable backup of the blocklist.

Risk: Automatic enforcement based on peer scores can block legitimate peers if inputs or thresholds are wrong.

Mitigation: Run the workflow in a review-only mode first, document the threshold, and apply changes only after confirming each candidate.

Risk: Shared temporary blocklist paths can create collision or tampering risk on multi-user systems.

Mitigation: Use a unique secure temporary file in the blocklist directory and atomically replace the final blocklist after JSON validation.

Risk: Hostname matching and command output parsing can affect the wrong peer if records are ambiguous.

Mitigation: Use exact hostname matching, confirm the resolved node ID, and avoid acting when more than one peer record matches.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-blocklist)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for Pilot Protocol blocklist files and pilotctl commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
