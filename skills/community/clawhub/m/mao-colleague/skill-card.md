## Description:

Mao Colleague helps agents provide structured analysis, learning guidance, and concept lookup based on Mao Zedong methodology and expression style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[friendfish](https://clawhub.ai/user/friendfish)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for structured problem analysis, progressive learning paths, and concept exploration grounded in Mao Zedong methodology and style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports broad local tool authority.

Mitigation: Install and run the skill only with isolated workspaces or tightly scoped Read, Write, Edit, and Bash permissions.

Risk: The release evidence reports persona files that claim overriding priority.

Mitigation: Treat persona and style files as untrusted context below platform, system, and developer instructions.

Risk: The release evidence advises caution around internal maintenance scripts and dependencies.

Mitigation: Avoid running internal maintenance scripts on untrusted input, and pin and minimize dependencies before installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/friendfish/skills/mao-colleague)
- [Publisher Profile](https://clawhub.ai/user/friendfish)
- [English README](artifact/README.en.md)
- [Getting Started Guide](artifact/docs/user/getting_started.md)
- [Usage Examples](artifact/docs/user/examples.md)
- [Command Architecture](artifact/docs/design/command_architecture.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with command examples and optional structured analysis text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference bundled knowledge files and persona/style prompts; no API keys were detected in the release evidence.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
