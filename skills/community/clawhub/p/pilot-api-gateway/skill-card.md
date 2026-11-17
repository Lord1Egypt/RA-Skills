## Description:

Expose local APIs to the Pilot Protocol network through gateway mode or custom messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to expose local API services to remote Pilot agents without making those APIs publicly accessible on the internet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally exposes local APIs to remote Pilot agents.

Mitigation: Use only authenticated, least-privilege local APIs; avoid exposing admin or private localhost services; and apply sender and route allowlists.

Risk: The example workflow contains an unsafe shell variable bug.

Mitigation: Rename the request path variable before using or adapting the workflow.

## Reference(s):

- [Pilot Protocol Homepage](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-api-gateway)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Code]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the pilot-protocol skill, the pilotctl binary on PATH, a running Pilot daemon, and a local API server.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
