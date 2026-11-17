## Description:

Before running shell commands, the skill tells an agent to route them through the PRECC hook to correct working-directory issues, compress command output, and apply learned command heuristics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yijunyu](https://clawhub.ai/user/yijunyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to have an agent pre-process shell commands through PRECC so command failures, verbose output, and repeated shell mistakes can be reduced during coding sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The PRECC hook can inspect and rewrite every shell command the agent runs.

Mitigation: Use the skill only in repositories where PRECC is trusted, review rewritten commands before execution in sensitive contexts, and avoid routing secrets through shell commands.

Risk: The setup flow includes a curl-to-bash installer.

Mitigation: Prefer the documented package-manager installation path when possible, or pin and verify the installer before running it.

Risk: History ingestion can process prior session data.

Mitigation: Run history ingestion only after confirming which histories will be read and that they do not contain sensitive material.

Risk: The hook is prompt-level in OpenClaw rather than platform-enforced.

Mitigation: Treat command rewriting as agent-enforced guidance, and verify high-impact commands manually before execution.

## Reference(s):

- [PRECC project homepage](https://github.com/yijunyu/precc-cc)
- [OpenClaw native PreToolUse tracking issue](https://github.com/openclaw/openclaw/issues/7597)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON hook examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill instructs the agent to parse PRECC hook JSON and execute a rewritten shell command when one is returned.]

## Skill Version(s):

0.1.8 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
