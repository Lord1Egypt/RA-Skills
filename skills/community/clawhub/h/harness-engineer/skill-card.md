## Description:

Harness Engineer is a persistent autonomous engineering harness runtime for Claude Code and OpenClaw that helps developers orchestrate supervised, multi-agent, self-improving software development workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[louis-szeto](https://clawhub.ai/user/louis-szeto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to set up a supervised autonomous coding harness that researches, plans, implements, reviews, tests, and improves repository changes across long-running workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The harness can make broad repository changes across long-running autonomous workflows.

Mitigation: Install only in a sandboxed repository, start in single-pass mode, require human approval gates, and verify platform-enforced scoped git credentials and protected write blocking before broader use.

Risk: The harness can persist future agent rules that later runs may treat as authority.

Mitigation: Review generated constraints before allowing future runs to treat them as mandatory, and keep memory writes redacted and bounded.

Risk: The harness can load untrusted instruction files as authority.

Mitigation: Verify sensitive-path blocking, tool-router enforcement, output redaction, and sandboxed test execution before using the skill on a real repository.

Risk: Out-of-repository writes may occur when Obsidian-style vault export is enabled.

Mitigation: Avoid the Obsidian vault export unless out-of-repo writes are explicitly intended and reviewed.

## Reference(s):

- [Harness Engineer ClawHub Release](https://clawhub.ai/louis-szeto/skills/harness-engineer)
- [Platform Requirements and Verification Checklist](PLATFORM_REQUIREMENTS.md)
- [Harness Configuration](CONFIG.yaml)
- [Runtime Loop](runtime/loop.md)
- [Security and Performance](references/security-performance.md)
- [Testing Standards](references/testing-standards.md)
- [MCP Tools](references/mcp-tools.md)
- [Git Workflow](references/git-workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions, structured plans, review reports, test plans, configuration guidance, and proposed repository changes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only skill; safe operation depends on platform-enforced sandboxing, scoped tool access, protected writes, scoped git credentials, and human approval gates.]

## Skill Version(s):

5.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
