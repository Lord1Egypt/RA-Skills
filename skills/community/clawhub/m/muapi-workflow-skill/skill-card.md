## Description:

Build, run, and visualize multi-step AI generation workflows that translate natural language descriptions into connected muapi.ai generation pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anil-matcha](https://clawhub.ai/user/anil-matcha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to discover, create, inspect, edit, and execute muapi.ai workflows for image, video, audio, enhancement, and editing pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to reinstall a local muapi CLI from a mutable workspace path.

Mitigation: Use a trusted, pinned muapi CLI source and avoid automatic upgrades from unverified local paths.

Risk: The workflow listing wrapper has an argument validation issue that could run unintended commands.

Mitigation: Patch or avoid list-workflows.sh until --limit is validated as a safe numeric value.

Risk: Workflow execution may delete workflows or download generated outputs to local directories.

Mitigation: Require explicit user confirmation before destructive workflow operations or local output downloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anil-matcha/skills/muapi-workflow-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and CLI arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to run muapi CLI workflow commands and collect generated outputs.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
