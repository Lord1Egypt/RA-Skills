## Description:

Create and manage Product Requirements Documents with user stories, verifiable acceptance criteria, ordered implementation tasks, and progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhao202404](https://clawhub.ai/user/zhao202404)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product managers, and AI coding agents use this skill to turn feature plans into PRDs with user stories, acceptance criteria, dependency ordering, and progress tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation includes an unbounded autonomous coding loop that disables permission checks.

Mitigation: Do not copy the unattended loop into a real project unless it is isolated in a disposable worktree or container with minimal credentials, a bounded run count, and human review before writes or commits.

Risk: PRD guidance or generated task lists may introduce incorrect, oversized, or misleading implementation steps.

Mitigation: Review PRDs before execution, keep each story small enough for one context window, and require verifiable acceptance criteria such as typecheck, lint, or test results.

## Reference(s):

- [Agent Usage Patterns](references/agent-usage.md)
- [Output Patterns and Templates](references/output-patterns.md)
- [Workflow Patterns for PRD Skills](references/workflows.md)
- [Ralph by snarktank](https://github.com/snarktank/ralph)
- [Claude Code](https://github.com/anthropics/claude-code)
- [Amp Code](https://ampcode.com)
- [Tips for AI Coding with Ralph Wiggum](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JSON templates and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update prd.json, PRD markdown, and progress notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
