## Description:

Operate Flexmail to read, create, update, and delete contacts, interests, subscriptions, and related account data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Flexmail contacts, interests, preferences, and subscriptions through an OOMOL-connected account. It can also retrieve account configuration and contact information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute an unchecked installer, whose exact effects are uncertain.

Mitigation: Review and install the oo CLI separately before enabling the skill.

Risk: Bundled-skill synchronization can introduce changes to other agent skills.

Mitigation: Decide whether to allow synchronization and review proposed skill changes before applying them.

Risk: Account changes or deletions can affect Flexmail contacts, interests, and subscriptions.

Mitigation: Keep the required confirmation for write actions and explicit approval for destructive actions.

## Reference(s):

- [Flexmail homepage](https://flexmail.be/en)
- [Flexmail API documentation](https://api.flexmail.eu/documentation/)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Flexmail skill release](https://clawhub.ai/oomol/skills/oo-flexmail)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON connector results with concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require user confirmation; destructive actions require explicit approval.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
