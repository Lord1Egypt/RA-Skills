## Description:

Polo score escrow for verified task completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to structure Pilot Protocol escrow flows for high-value task rewards, completion proof submission, verification, release, and disputes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example workflow can release escrow after a completion claim without verifying claimant identity or task results.

Mitigation: Require authenticated executor identity, validate completion evidence against the task specification, and require explicit approval before reward release.

Risk: Escrow actions depend on a trusted pilotctl environment and escrow agent.

Mitigation: Use only a trusted Pilot Protocol daemon and escrow agent, and configure an arbiter for dispute resolution before real escrow use.

Risk: Inline JSON construction in shell commands can mishandle untrusted values.

Mitigation: Construct JSON with jq arguments or another structured JSON builder before sending escrow messages.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [Pilot Escrow ClawHub page](https://clawhub.ai/teoslayer/skills/pilot-escrow)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl on PATH, jq for JSON parsing, a running Pilot Protocol daemon, a trusted escrow agent, and optional arbiter configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter metadata.version is 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
