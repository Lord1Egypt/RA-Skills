## Description:

Create and manage Product Requirements Documents (PRDs). Use when: (1) Creating structured task lists with user stories, (2) Specifying features with acceptance criteria, (3) Planning feature implementation for AI agents or human developers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhao202404](https://clawhub.ai/user/zhao202404)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product managers, and coding agents use this skill to create PRD files with ordered user stories, verifiable acceptance criteria, and progress tracking for feature implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation includes an unattended coding-agent workflow that bypasses permission checks and can repeatedly modify a repository.

Mitigation: Keep normal permission prompts enabled, review each story and diff, and run autonomous implementation only in an isolated worktree or sandbox without secrets.

Risk: PRD-driven implementation can turn vague or oversized stories into broad repository changes.

Mitigation: Require each story to be completable in one context window, keep acceptance criteria verifiable, and approve stories before execution.

## Reference(s):

- [Agent Usage Patterns](references/agent-usage.md)
- [Output Patterns and Templates](references/output-patterns.md)
- [Workflow Patterns for PRD Skills](references/workflows.md)
- [Ralph by snarktank](https://github.com/snarktank/ralph)
- [Claude Code](https://github.com/anthropics/claude-code)
- [Amp Code](https://ampcode.com)
- [Tips for AI Coding with Ralph Wiggum](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces PRD structures such as prd.json, acceptance criteria, ordered user stories, progress notes, and agent prompts.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
