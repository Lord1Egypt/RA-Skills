## Description:

Helps agents inspect local Ollama model storage, move models from the default C: drive location to another disk, set OLLAMA_MODELS, and verify the migration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jjflydudu](https://clawhub.ai/user/jjflydudu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to assess Ollama model disk usage and perform a supervised Windows model-directory migration to free space on the C: drive. It also supports post-migration checks before any optional cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional cleanup can delete the original Ollama models even if migration verification fails.

Mitigation: Do not run --cleanup until the destination model directory and ollama list output have been independently verified.

Risk: Choosing a target path inside or overlapping the existing model directory can cause confusing copies or data loss during cleanup.

Mitigation: Use a separate destination path on the intended target disk and review the migration plan before confirming execution.

Risk: The migration affects local model files and user-level Ollama configuration.

Mitigation: Back up important models and manually supervise the script before changing OLLAMA_MODELS or deleting source files.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline PowerShell and Python commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bundled Python scripts print console status; the status checker can also emit JSON when run with --json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
