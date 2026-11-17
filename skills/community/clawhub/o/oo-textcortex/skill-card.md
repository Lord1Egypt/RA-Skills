## Description:

Connect to TextCortex to create chat completions, list available models, and retrieve model details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request TextCortex chat completions and inspect model metadata through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute downloaded installation code and synchronize bundled skills.

Mitigation: Review the CLI installation and bundled-skill synchronization before enabling automatic setup.

Risk: Chat completion sends content to an external service and may incur charges.

Mitigation: Treat completion as external, potentially billable generation and send only content approved for OOMOL and TextCortex.

## Reference(s):

- [TextCortex API documentation](https://docs.textcortex.com/api)
- [TextCortex](https://textcortex.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses containing generated text or model metadata, with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chat completion output may be externally generated and billable.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
