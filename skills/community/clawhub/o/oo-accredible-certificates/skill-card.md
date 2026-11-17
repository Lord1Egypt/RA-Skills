## Description:

Accredible Certificates (accredible.com). Use this skill for ANY Accredible Certificates request — reading, creating, updating, and deleting data. Whenever a task involves Accredible Certificates, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to read, search, create, and delete Accredible credentials and groups through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run downloaded installer code whose contents were not inspected.

Mitigation: Review and approve a verified CLI installation before allowing setup to run, including any automatic installation of additional agent skills.

Risk: Creating credentials changes account data, and deleting a credential is destructive.

Mitigation: Confirm the exact payload and effect before creating a credential, and explicitly approve the target before deleting one.

## Reference(s):

- [Accredible Certificates](https://www.accredible.com/)
- [Accredible API documentation](https://docs.api.accredible.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release](https://clawhub.ai/oomol/skills/oo-accredible-certificates)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON payloads, oo CLI commands, and JSON connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports read, create, and delete operations; creation requires confirmation and deletion requires explicit approval.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
