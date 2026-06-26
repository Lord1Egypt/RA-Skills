## Description: <br>
Create and manage Product Requirements Documents (PRDs) by defining user stories with verifiable acceptance criteria and tracking progress by priority order. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhao202404](https://clawhub.ai/user/zhao202404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product managers, and AI coding agents use this skill to create PRD task lists, specify user stories with verifiable acceptance criteria, and track implementation progress in priority order. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes guidance for unattended agent loops and code commits, including an example that skips normal permission prompts. <br>
Mitigation: Run autonomous workflows only in an isolated branch or worktree, review every file change and commit, and avoid unattended permission-skipping loops in normal repositories. <br>
Risk: Under-scoped PRD stories or vague acceptance criteria can lead agents to make broad or incorrect code changes. <br>
Mitigation: Keep each story small enough for one context window, order stories by dependency, and require verifiable checks such as typecheck, lint, and tests before marking a story complete. <br>


## Reference(s): <br>
- [Agent Usage Patterns](references/agent-usage.md) <br>
- [Output Patterns and Templates](references/output-patterns.md) <br>
- [Workflow Patterns for PRD Skills](references/workflows.md) <br>
- [Ralph by snarktank](https://github.com/snarktank/ralph) <br>
- [Claude Code](https://github.com/anthropics/claude-code) <br>
- [Amp Code](https://ampcode.com) <br>
- [Tips for AI Coding with Ralph Wiggum](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON templates and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces PRD structures, acceptance criteria patterns, workflow guidance, and agent prompt templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
