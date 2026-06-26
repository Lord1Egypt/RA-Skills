## Description: <br>
Delegate coding tasks to Codex, Claude Code, Pi, or OpenCode from bash with safe launch modes, background monitoring, and repo-isolated review workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielsinewe](https://clawhub.ai/user/danielsinewe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this playbook to delegate implementation, review, issue triage, and long-running verification loops to Codex, Claude Code, Pi, or OpenCode while keeping sessions scoped and review workflows isolated. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegating work to other coding agents can produce changes that are incorrect, over-scoped, or hard to review. <br>
Mitigation: Keep each delegated task narrowly scoped and review resulting changes before merging or deploying them. <br>
Risk: Full-auto or bypass-permission modes can execute high-trust coding workflows with less interactive oversight. <br>
Mitigation: Use these modes only in trusted repositories, avoid exposing production secrets, and inspect changes and command results afterward. <br>
Risk: Running review workflows in a live working tree can mix review artifacts with active development state. <br>
Mitigation: Use temporary clones or worktrees for reviews, as described by the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danielsinewe/openclaw-coding-agent-playbook) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and text code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes execution mode guidance, background session commands, review isolation workflow, prompt template, and failure recovery checklist.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
