## Description:

Use the oo CLI to read and manage Doppler Marketing Automation subscribers and lists through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can query Doppler Marketing Automation subscribers and lists, and create, update, or remove list associations through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup can execute downloaded software and make persistent changes.

Mitigation: Review and approve CLI installation separately before enabling automatic setup; disable bundled-skill synchronization if it is not needed.

Risk: Write and destructive actions can change Doppler lists and subscriber associations.

Mitigation: Confirm the exact payload and effect before write actions, and get explicit approval before destructive actions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Doppler Marketing Automation](https://www.fromdoppler.com/en/)
- [Doppler REST API documentation](https://restapi.fromdoppler.com/docs/)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON connector requests and responses with concise results and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Doppler action.]

## Skill Version(s):

1.0.4 (source: frontmatter metadata.version; release evidence agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
