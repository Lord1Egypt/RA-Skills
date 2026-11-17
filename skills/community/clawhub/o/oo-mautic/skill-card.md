## Description:

Mautic (mautic.org). Use this skill for ANY Mautic request — reading, creating, updating, and deleting data. Whenever a task involves Mautic, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Mautic account operators use this skill to inspect contacts and segments, create or update contacts, and manage contact membership in segments. Contact deletion and other destructive changes require confirmation of the target and explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run unverified downloaded software whose documented behavior includes broader changes to agent skills.

Mitigation: Review and install the CLI separately, check its automatic skill synchronization settings, and approve broader agent changes.

Risk: Mautic requests and contact data pass through OOMOL, and write or deletion actions can change account data.

Mitigation: Retain confirmation for writes and deletions, and confirm the exact target and effect before proceeding.

## Reference(s):

- [Mautic](https://mautic.org)
- [Mautic REST API authentication documentation](https://devdocs.mautic.org/en/7.1/rest_api/authentication.html)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured Mautic contact and segment data, with concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned fields depend on the selected action and Mautic instance.]

## Skill Version(s):

1.0.4 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
