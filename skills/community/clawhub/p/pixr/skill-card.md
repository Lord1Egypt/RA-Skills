## Description:

Drives the local pixr Gemini image CLI for generation, editing, variations, model selection, saved defaults, profile-based defaults, reference-image workflows, and output sizing or format conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dishant0406](https://clawhub.ai/user/dishant0406)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and image-focused users use this skill to have an agent operate the local pixr CLI for image generation, editing, variations, model selection, saved defaults, profiles, and reusable reference-image workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to change persistent pixr defaults such as model, save directory, or profiles under ~/.pixr.

Mitigation: Review intended configuration changes before applying them, then confirm the resulting state with pixr config --json or profile inspection commands.

Risk: Generation and model operations use the configured pixr/Gemini credentials and quota.

Mitigation: Confirm PIXR_API_KEY is intended for the session and validate generation commands before running them.

## Reference(s):

- [Command Reference](artifact/references/command-reference.md)
- [Defaults And Files](artifact/references/defaults-and-files.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated image output paths or saved pixr configuration state when a command is run.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
