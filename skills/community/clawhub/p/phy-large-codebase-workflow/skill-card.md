## Description: <br>
Best practices for using Claude Code with large, multi-part codebases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to manage Claude Code sessions in large repositories through codemaps, focused sessions, subagents, worktrees, and verification-oriented workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repo-editing, commit, push, and PR examples can lead to unintended repository changes if an agent executes them without review. <br>
Mitigation: Use a disposable branch, inspect generated .claude files and codemaps for sensitive content, and require confirmation before commits, pushes, or PR creation. <br>
Risk: Generated codemaps and workflow notes may include sensitive repository structure or implementation details. <br>
Mitigation: Review generated codemaps and related documentation before sharing or committing them. <br>


## Reference(s): <br>
- [Canlah AI](https://canlah.ai) <br>
- [Anthropic Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) <br>
- [Claude Code Best Practices Documentation](https://code.claude.com/docs/en/best-practices) <br>
- [Claude Code Subagents Guide](https://code.claude.com/docs/en/sub-agents) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands, directory examples, and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only workflow guidance; no tools or credentials are configured by the skill itself.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
