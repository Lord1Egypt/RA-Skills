## Description:

Search and read Mindbody data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users with a connected Mindbody account can use this skill to look up businesses in Mindbody's Consumer API Business Directory from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup may install the oo CLI through a remote installer without a separate approval step.

Mitigation: Review and approve CLI installation separately, prefer a pinned and integrity-verified release, and check its installation effects. Set OO_SKILLS_SYNC_DISABLED to prevent startup writes to agent skill directories.

## Reference(s):

- [Mindbody Consumer API documentation](https://developers.mindbodyonline.com/ConsumerDocumentation)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [ClawHub Mindbody release](https://clawhub.ai/oomol/skills/oo-mindbody)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Shell commands]

**Output Format:** [JSON business directory results with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only business lookup; requires the oo CLI and a connected Mindbody account.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
