## Description:

Guides agents using the local pixr CLI to generate, edit, and organize images across supported providers and manage saved defaults.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dishant0406](https://clawhub.ai/user/dishant0406)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other pixr users can guide an agent through image generation, edits, variations, model discovery, and configuration of local defaults and profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected external providers may receive prompts or source images and consume paid API quota.

Mitigation: Confirm the provider and model, review images before submission, and check expected API costs.

Risk: Changing saved defaults or profiles can redirect later image outputs or alter later runs.

Mitigation: Review model, save-directory, and profile changes before making them persistent.

Risk: Provider credentials may be exposed if copied into configuration or shared output.

Mitigation: Keep API keys in environment variables rather than saved config or responses.

## Reference(s):

- [pixr CLI release](https://clawhub.ai/dishant0406/skills/pixr-cli)
- [Command Reference](references/command-reference.md)
- [Defaults And Files](references/defaults-and-files.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration guidance, Text]

**Output Format:** [Markdown with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can report CLI output paths, resolved settings, and model options.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
