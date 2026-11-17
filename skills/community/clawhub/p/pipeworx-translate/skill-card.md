## Description:

Translate text between multiple languages, detect text language, and list supported language codes and names.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to translate text, detect source language, and retrieve supported language codes during multilingual workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for translation or language detection is sent to a third-party remote service.

Mitigation: Avoid submitting secrets, credentials, regulated data, or confidential content unless the service and its data-handling practices are approved for that use.

Risk: Machine translation or language detection can be inaccurate or incomplete.

Mitigation: Review important translations before relying on them in customer-facing, legal, medical, or safety-sensitive contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-translate)
- [Pipeworx Translate MCP endpoint](https://gateway.pipeworx.io/translate/mcp)

## Skill Output:

**Output Type(s):** [text, configuration, shell commands, guidance]

**Output Format:** [Plain text, Markdown instructions, JSON configuration, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Translation and language detection results depend on the remote translation service.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
