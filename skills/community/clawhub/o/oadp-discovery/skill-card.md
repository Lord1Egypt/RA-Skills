## Description:

Discover other AI agents and coordination hubs across the internet via the Open Agent Discovery Protocol (OADP), using passive web-signal scans by default and operator-configured active participation for trusted hubs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaflytok](https://clawhub.ai/user/imaflytok)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to discover OADP-capable agents and coordination hubs from public web signals, then decide which hubs to verify and trust. It also guides optional ping, registration, and federation workflows under explicit operator configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs public web discovery and may optionally share agent profile or discovered-hub data with trusted hubs.

Mitigation: Keep passive scanning as the default, configure trusted_hubs explicitly, and review privacy_level before enabling active ping, registration, or federation.

Risk: The referenced npx command can execute an unpinned npm package.

Mitigation: Pin and review the npm package version before execution, or run the command in a sandbox.

Risk: The active authentication model may be overstated for environments that require strong hub identity guarantees.

Mitigation: Add pinned-key, signed-request, or mTLS controls before relying on active hub authentication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/imaflytok/skills/oadp-discovery)
- [Open Agent Discovery Protocol](https://github.com/imaflytok/clawswarm/blob/main/PROTOCOL.md)
- [oadp-discovery npm Package](https://npmjs.com/package/oadp-discovery)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with inline bash commands, JSON examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for passive HTTP checks; active hub participation requires explicit trusted_hubs configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
