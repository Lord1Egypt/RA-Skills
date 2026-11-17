## Description:

Publish, edit, or configure rich-text Mowen notes through the Mowen Open API, including images, tags, privacy, sharing, and expiration settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacobluo](https://clawhub.ai/user/jacobluo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to create, edit, and configure Mowen notes with rich text, images, tags, privacy controls, sharing controls, and expiration settings through the Mowen Open API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be exposed if passed directly on the command line.

Mitigation: Prefer MOWEN_API_KEY or a secret manager over the --api-key argument.

Risk: Using autoPublish or public privacy can publish note content before a human has reviewed it.

Mitigation: Review generated content and privacy settings before enabling autoPublish or public visibility.

Risk: Editing replaces the entire note body.

Mitigation: Confirm the target noteId and intended full replacement content before running edit operations.

Risk: Local image paths and remote image URLs may upload content to Mowen.

Mitigation: Include only images that are intended for upload and publication.

## Reference(s):

- [Mowen Open API Reference](references/mowen_api.md)
- [Mowenskill Publish on ClawHub](https://clawhub.ai/jacobluo/skills/mowenskill-publish)
- [Mowen Open API Base URL](https://open.mowen.cn)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON payloads and bash command snippets; the bundled script returns JSON responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and a MOWEN_API_KEY or equivalent API key argument when executing Mowen API calls.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
