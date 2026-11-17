## Description:

Use the PansClaw Code CLI (Rust reimplementation of Claude Code) for AI-assisted coding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashiming](https://clawhub.ai/user/dashiming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to delegate coding, refactoring, debugging, and interactive code-assistance tasks to the local PansClaw Code CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented defaults can run the delegated coding CLI with disabled permission prompts or full-access permissions.

Mitigation: Prefer read-only or workspace-write permission modes and avoid --dangerously-skip-permissions unless the workspace and task are trusted.

Risk: The install flow builds and links a local claw binary that has not been independently reviewed in the evidence.

Mitigation: Review the local PansClaw source tree and any ~/.local/bin/claw replacement before building or running the binary.

Risk: Cloud providers may receive private code or prompts when API-backed models are used.

Mitigation: Use local Ollama models for sensitive work, or use cloud providers only after confirming data-sharing and confidentiality requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dashiming/skills/pansclaw-code)
- [CLI Commands Reference](references/commands.md)
- [Model Support Reference](references/models.md)
- [Quickstart](references/quickstart.md)
- [Rustup Installer](https://sh.rustup.rs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands for local Ollama models or cloud providers that require API keys.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
