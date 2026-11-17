## Description:

NeetoCal (neeto.com). Use this skill for ANY NeetoCal request — searching and reading data. Whenever a task involves NeetoCal, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to search and read NeetoCal bookings, scheduling links, and available calendar slots through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If setup is needed, the fallback runs an online installer whose exact payload and scope were unavailable for verification.

Mitigation: Review and approve the CLI installation separately, prefer a pinned and verified release, and check whether it installs other agent skills.

Risk: Connecting NeetoCal gives OOMOL access to the connected account and calendar requests.

Mitigation: Connect only an account appropriate for the requested calendar access and review the permissions granted to OOMOL.

## Reference(s):

- [NeetoCal](https://www.neeto.com/neetocal)
- [NeetoCal API authentication documentation](https://apidocs.neetocal.com/getting-started/authentication)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release](https://clawhub.ai/oomol/skills/oo-neetocal)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON]

**Output Format:** [NeetoCal query results as text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only booking, scheduling-link, and availability results]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
