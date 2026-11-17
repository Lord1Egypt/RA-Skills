## Description:

Use UnifAPI to read, create, and update data through the user's connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts can use this skill to retrieve or manage data with UnifAPI through an already connected account. Review the live action schema before sending data, and confirm the intended effect before using actions marked as writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs users to execute a downloaded CLI and installer that were not audited.

Mitigation: Review and install the CLI separately before allowing the skill to run. Check the publisher's documented controls for automatic skill synchronization and disable it if unwanted.

Risk: Actions that create or update data can change the connected UnifAPI account.

Mitigation: Review the live action schema and keep the skill's confirmation requirement for write actions.

## Reference(s):

- [UnifAPI documentation](https://docs.unifapi.com/)
- [UnifAPI homepage](https://unifapi.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-unifapi)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Structured API response data (JSON) with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read and write actions are identified in the skill instructions; review write effects before execution.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
