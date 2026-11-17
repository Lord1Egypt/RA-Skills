## Description:

Operate Eraser to read, create, update, and delete files and diagrams through your connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to manage Eraser files and diagrams, including generating and revising diagrams through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to execute downloaded CLI installation code without a separate approval or verification step.

Mitigation: Review the installer and approve it separately before allowing setup.

Risk: Eraser requests and results pass through OOMOL, which may affect the suitability of data shared with the service.

Mitigation: Assess whether OOMOL is an appropriate intermediary for the data before using the skill.

Risk: Write and destructive actions can change or remove Eraser files and diagrams.

Mitigation: Keep the documented approval requirements for changes and deletions.

## Reference(s):

- [Eraser](https://www.eraser.io)
- [Eraser API documentation](https://docs.eraser.io/reference/getting-started)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Diagram and file content]

**Output Format:** [Markdown guidance with oo CLI commands and JSON payload examples; action results are returned as data and metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read, create, update, archive, or delete Eraser files and diagrams, depending on the selected action.]

## Skill Version(s):

1.0.5 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
