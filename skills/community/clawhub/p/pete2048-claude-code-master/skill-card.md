## Description:

Guides agents through Claude Code workflow optimization, including context engineering, spec-driven development, hooks, sub-agents, output styles, and SuperClaude usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pete2048](https://clawhub.ai/user/pete2048)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to improve Claude Code workflows, configure project context, design spec-driven development processes, define sub-agents and output styles, and apply token-saving hook patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent hooks can save Claude Code session output and signal OpenClaw, which could expose private code, session output, or credentials if enabled globally.

Mitigation: Review hook behavior before installation, prefer project-scoped hooks, store data in private 0700 directories, avoid full-output capture, use short-lived scoped tokens, and provide clear uninstall steps.

Risk: External CLI review workflows can send private files to a third-party provider.

Mitigation: Require explicit approval before using external review tools on private code and limit inputs to approved files.

Risk: Installer and npx command examples are unpinned and may run package or installer code that changes over time.

Mitigation: Pin package versions, verify package sources or checksums, and review installer scripts before execution.

## Reference(s):

- [Context Engineering and PRP Guide](references/context-engineering-prp.md)
- [Claude Code Hooks Mechanism](references/hooks-mechanism.md)
- [Output Styles Examples](references/output-styles-examples.md)
- [Sub Agents Examples](references/sub-agents-examples.md)
- [SuperClaude Guide](references/superclaude-guide.md)
- [Quick Reference](references/quick-reference.md)
- [Claude Code Official Documentation](https://docs.anthropic.com)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Context Engineering Intro](https://github.com/coleam00/Context-Engineering-Intro)
- [SuperClaude](https://github.com/NomenAK/SuperClaude)
- [Claude Code Hooks](https://github.com/win4r/claude-code-hooks)
- [AI超元域](https://www.aivi.fyi)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, and configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reusable templates for CLAUDE.md, PRPs, sub-agents, output styles, project initialization, and hook configuration.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
