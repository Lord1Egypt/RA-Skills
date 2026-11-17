## Description:

Create and manage Product Requirements Documents (PRDs) for structured user stories, acceptance criteria, and implementation planning for AI agents or human developers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjesuiter](https://clawhub.ai/user/bjesuiter)

### License/Terms of Use:


## Use Case:

Developers, product managers, and AI coding agents use this skill to create PRDs, break features into dependency-ordered user stories, and track verifiable acceptance criteria through implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unattended coding-agent loop disables permission checks and can continue making repository changes until manually stopped.

Mitigation: Use manual review, bounded iterations, normal permission prompts, and a disposable worktree or container unless unreviewed command execution is deliberately accepted.

Risk: Generated PRDs can drive implementation work, so vague or oversized stories may lead agents or developers toward incorrect changes.

Mitigation: Review each PRD before execution, split stories to fit one context window, and require verifiable acceptance criteria such as typecheck, lint, or tests.

## Reference(s):

- [Agent Usage Patterns](references/agent-usage.md)
- [Output Patterns and Templates](references/output-patterns.md)
- [Workflow Patterns for PRD Skills](references/workflows.md)
- [Ralph by snarktank](https://github.com/snarktank/ralph)
- [Claude Code](https://github.com/anthropics/claude-code)
- [Amp Code](https://ampcode.com)
- [Tips for AI Coding with Ralph Wiggum](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JSON templates and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces PRD structures, acceptance criteria, progress tracking notes, and optional agent execution prompts.]

## Skill Version(s):

2.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
