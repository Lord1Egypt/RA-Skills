## Description:

Search and read Snipe-IT data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use the skill to retrieve Snipe-IT user, category, company, hardware, and status-label data through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required oo CLI may persistently change other agents’ installed skills.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 for every CLI invocation, as described in the upstream reference.

Risk: Remote CLI installer scripts were unavailable for inspection, and the connected account’s requests and records are handled by OOMOL.

Mitigation: Install a verified CLI release separately, use a read-only Snipe-IT API key, and proceed only if you accept OOMOL handling the connected account’s requests and records.

## Reference(s):

- [Snipe-IT](https://snipeitapp.com)
- [Snipe-IT API overview](https://snipe-it.readme.io/reference/api-overview)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Snipe-IT data returned by read and search actions.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
