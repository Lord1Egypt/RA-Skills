## Description:

Check PyTorch, Transformers, and CUDA compatibility. Detect GPU, driver mismatches, and version conflicts in ML environments. Use when the user sets up ML/AI tools, installs torch or transformers, hits dependency errors, or asks about compatible versions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmed-eladl](https://clawhub.ai/user/ahmed-eladl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose ML dependency, PyTorch, Transformers, GPU, CUDA, driver, and Python compatibility issues and to get actionable version or install guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running diagnostics in a privileged or global Python environment can affect the user's active ML setup.

Mitigation: Install and run Harmonia in a project virtual environment unless the user explicitly chooses a different environment.

Risk: Diagnostic output may reveal system, GPU, driver, Python, and package details.

Mitigation: Review diagnostic output before sharing it publicly or with third parties.

Risk: The skill proposes commands based on local compatibility diagnostics.

Mitigation: Review proposed commands before execution and apply changes only after confirming they match the target environment.

## Reference(s):

- [Harmonia homepage](https://github.com/ahmed-eladl/harmonia)
- [harmonia-ml on PyPI](https://pypi.org/project/harmonia-ml/)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON from harmonia]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include full local diagnostic output, compatibility recommendations, and suggested install commands.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
