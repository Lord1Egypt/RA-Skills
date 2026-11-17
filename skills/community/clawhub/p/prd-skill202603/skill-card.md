## Description:

Create and manage Product Requirements Documents (PRDs) by defining user stories with verifiable acceptance criteria and tracking progress by priority order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhao202404](https://clawhub.ai/user/zhao202404)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and AI-agent operators use this skill to structure feature planning into PRD task lists with user stories, acceptance criteria, priority order, and completion tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended coding-agent loops that bypass permission checks can modify repositories without enough user control.

Mitigation: Use manual story-by-story execution, bounded runs, sandboxing, and human review of diffs and commits; do not run the unattended --dangerously-skip-permissions loop on real repositories or with credentials available.

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

**Output Format:** [Markdown guidance with JSON templates and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide creation or updates of PRD files such as agents/prd.json and progress-tracking notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
