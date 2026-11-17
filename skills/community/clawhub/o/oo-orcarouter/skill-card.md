## Description:

Use a connected OOMOL account to list OrcaRouter models and submit chat, embedding, and message requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to interact with OrcaRouter through a connected OOMOL account, including listing available models and sending chat, embedding, or message requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute remote CLI installers, and the installer behavior was not verified.

Mitigation: Review and explicitly authorize CLI installation and skill synchronization before setup.

Risk: AI requests may incur charges and send content through OOMOL and OrcaRouter.

Mitigation: Approve request payloads and possible charges, and send only the content needed for the task.

## Reference(s):

- [OrcaRouter homepage](https://www.orcarouter.ai)
- [OrcaRouter API documentation](https://docs.orcarouter.ai/introduction)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON responses and text content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requests may incur charges; embedding and message actions are marked as writes in the skill.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
