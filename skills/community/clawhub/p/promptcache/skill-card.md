## Description:

Estimate the cost savings from caching frequently-used prompts across AI models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avale-slai](https://clawhub.ai/user/avale-slai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to estimate whether repeated prompts or prompt templates could benefit from prompt caching before they enable caching in a pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer changes the user's shell profile to add ~/.local/bin to PATH.

Mitigation: Review install.sh before running and install manually or confirm shell-profile edits are acceptable.

Risk: Installer sends install telemetry to Signal Loom during setup without clear consent.

Mitigation: Use a release that documents network activity and asks for consent, or remove the telemetry command before installation.

Risk: Package metadata declares a promptcache executable that is missing from the artifact.

Mitigation: Prefer a complete release that includes the declared executable before relying on the skill.

## Reference(s):

- [Promptcache ClawHub skill page](https://clawhub.ai/avale-slai/skills/promptcache)
- [Signal Loom API key signup](https://signalloomai.com/signup)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with prompt-cache cost estimate guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the declared promptcache executable and a Signal Loom API key for free-tier analyses.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence; package.json reports 1.0.1 and install.sh reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
