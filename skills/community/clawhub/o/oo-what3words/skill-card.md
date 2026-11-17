## Description:

what3words (what3words.com). Use this skill for ANY what3words request — searching and reading data. Whenever a task involves what3words, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users can use the skill to search for what3words addresses, convert between three-word addresses and coordinates, and retrieve supported languages or grid sections through their connected what3words service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup runs a remote CLI installer whose contents have not been verified.

Mitigation: Review and approve installation separately using a verified release.

Risk: The CLI may synchronize additional agent skills at startup, and connector requests can share locations with OOMOL and what3words.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization, and submit only locations intended to be shared with both services.

## Reference(s):

- [what3words API documentation](https://developer.what3words.com/public-api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [what3words](https://what3words.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action results and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
