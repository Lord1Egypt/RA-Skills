## Description:

Named trust groups with automatic mutual handshakes for Pilot Protocol agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators managing Pilot Protocol agent teams use this skill to create named trust circles, add members, and bootstrap mutual trust among listed agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates durable trust approvals for Pilot agents, which can grant unintended trust if identities or pending nodes are not verified.

Mitigation: Use it only with strongly verified Pilot agent identities, keep circle membership allowlisted, and do not automatically approve unknown pending nodes.

Risk: The shell examples use simple path and temporary-file handling around local circle files.

Mitigation: Restrict circle names to simple safe values, quote file paths, and replace sample update flows with mktemp-based writes before production use.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local trust-circle JSON files and pilotctl command sequences; requires pilotctl and jq.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
