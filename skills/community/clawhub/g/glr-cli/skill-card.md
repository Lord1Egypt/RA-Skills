## Description:

Guides agents through configuring and operating an existing GameLearningRuntime project for bridge startup, bounded goal-driven training, review capture, run queries, knowledge transfer, and verified model playback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents operating an existing GLR project use this skill to configure its CLI, run bounded research and training, inspect evidence, transfer project knowledge, and play back verified models. Adapter implementation belongs to a separate skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A GLR update may change the installed runtime or project-owned skill files.

Mitigation: Review update behavior and request explicit approval before running an update.

Risk: Reports and portable packages may expose telemetry tokens or local window and process identifiers.

Mitigation: Review and remove sensitive tokens and local identifiers before sharing reports or packages.

Risk: Imported packages, model bundles, recordings, and checksums can be mistaken for trusted content or proof of gameplay success.

Mitigation: Verify source and admission evidence separately, and confirm outcomes against live runtime and evaluator evidence.

## Reference(s):

- [GLR CLI release](https://clawhub.ai/loonghao/skills/glr-cli)
- [GLR CLI command and contract reference](references/commands.md)
- [Collect, render, and trace training data](references/data-collection.md)
- [Offline packages](references/packages.md)
- [Recording](references/recording.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with CLI commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-specific paths, run evidence, and verification steps depend on the configured GLR project.]

## Skill Version(s):

0.26.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
