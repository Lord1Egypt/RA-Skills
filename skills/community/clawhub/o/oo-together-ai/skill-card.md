## Description:

Together AI (together.ai). Use this skill for ANY Together AI request — reading, creating, and updating data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users can use this skill to list Together AI models, create chat completions, and generate embeddings through an already connected Together AI account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote CLI installer and hosted connector are outside the inspected artifact, and setup may execute remote code.

Mitigation: Review the CLI installation separately and use a reviewed release before enabling setup.

Risk: CLI skill synchronization may make startup writes across agent applications.

Mitigation: Decide whether cross-application synchronization is acceptable; set OO_SKILLS_SYNC_DISABLED=1 to prevent startup skill writes when it is not.

Risk: Requests may include sensitive content and use paid inference.

Mitigation: Limit submitted content to what the request needs and set an inference spending limit.

## Reference(s):

- [Together AI API documentation: models](https://docs.together.ai/reference/models)
- [Together AI](https://www.together.ai)
- [oo CLI command controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Text]

**Output Format:** [JSON API responses with optional concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions use the connected Together AI account; embedding creation is a write action and requires confirmation of its exact payload and effect.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
