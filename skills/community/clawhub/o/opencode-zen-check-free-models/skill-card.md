## Description:

Monitors the OpenCode Zen pricing page for new free models and offers to update your default configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pranjal-joshi](https://clawhub.ai/user/pranjal-joshi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to monitor OpenCode Zen pricing for newly available free models and decide whether to update their default model configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Accepting an incorrect model change can affect all agents and related automation that rely on the default OpenClaw configuration.

Mitigation: Before accepting a model change, verify the suggested model ID and confirm which OpenClaw config file or environment setting will be changed.

## Reference(s):

- [OpenCode Zen pricing documentation](https://opencode.ai/docs/zen/#pricing)
- [ClawHub skill page](https://clawhub.ai/pranjal-joshi/skills/opencode-zen-check-free-models)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with user prompts, shell command guidance, JSON state updates, and configuration changes after confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and may write zen_seen_models.json plus confirmed OpenClaw configuration updates in the workspace.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
