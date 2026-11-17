## Description:

Use the Modjo AI connector to search and read Modjo AI data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users with an OOMOL-connected Modjo AI account can search and read Modjo accounts, calls, transcripts, contacts, deals, teams, users, and related summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback can install remote CLI code whose contents have not been verified.

Mitigation: Review and approve CLI installation separately before allowing the setup fallback.

Risk: Confidential Modjo data may pass through OOMOL.

Mitigation: Assess whether the data being accessed may pass through OOMOL before using the connector.

Risk: Startup skill synchronization can make broader agent changes.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before CLI use if those changes are unwanted.

## Reference(s):

- [oo CLI documentation](https://github.com/oomol-lab/oo-cli)
- [CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [Modjo AI API documentation](https://api.modjo.ai/v2/docs)
- [Modjo AI homepage](https://www.modjo.ai)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-modjo-ai)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON]

**Output Format:** [JSON connector responses summarized as Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results reflect the connected Modjo account and selected read action.]

## Skill Version(s):

1.0.5 (source: frontmatter; server-resolved release 1.0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
