## Description: <br>
Create and manage Product Requirements Documents by defining user stories with acceptance criteria, ordering tasks by dependencies, and tracking progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhao202404](https://clawhub.ai/user/zhao202404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product managers, and coding-agent operators use this skill to plan features as PRDs with ordered user stories, concrete acceptance criteria, and completion tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included unattended coding-agent loop can bypass permission prompts and repeatedly modify a repository. <br>
Mitigation: Keep approvals enabled, run agents in a separate branch or worktree, review commits before merge, and avoid unattended permission-skipping execution in real projects. <br>
Risk: PRD and progress files can become instruction sources for an agent and may contain secrets or untrusted content. <br>
Mitigation: Review prd.json and progress.txt before agent execution, keep secrets out of those files, and treat external or user-provided instructions as untrusted until checked. <br>


## Reference(s): <br>
- [Agent Usage Patterns](references/agent-usage.md) <br>
- [Workflow Patterns for PRD Skills](references/workflows.md) <br>
- [Output Patterns and Templates](references/output-patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/zhao202404/prd-skill20260303) <br>
- [Ralph implementation](https://github.com/snarktank/ralph) <br>
- [Claude Code](https://github.com/anthropics/claude-code) <br>
- [Amp Code](https://ampcode.com) <br>
- [Tips for AI Coding with Ralph Wiggum](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and inline shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended to help create, validate, and execute PRD files such as prd.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
