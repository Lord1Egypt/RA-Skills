## Description:

Connects Hermes Agent to local terminal-based coding assistants such as Codex, Kimi Code, Claude Code, OpenCode, and Gemini CLI for agent dispatch, session reuse, monitoring, evidence collection, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuyang-liu16](https://clawhub.ai/user/xuyang-liu16)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to let Hermes coordinate installed local coding CLIs for implementation, review, debugging, documentation, repository maintenance, and experiment work while preserving session context and reporting evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide Hermes to drive local coding CLIs that may edit files, run commands, spend resources, or otherwise affect the local workspace.

Mitigation: Keep approval prompts enabled by default and review the selected backend, working directory, session, and prompt before any side-effectful run.

Risk: Raw shell or tmux prompt interpolation can behave unexpectedly with untrusted or multiline text.

Mitigation: Avoid raw interpolation for untrusted input; pass arguments or prompt content through safer channels before dispatch.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuyang-liu16/skills/hermes-code-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, prompt templates, command recipes, and evidence-based report templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local CLI dispatch that changes files or runs commands; outputs should include the backend used, working directory, command evidence, verification results, and unresolved risks.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
