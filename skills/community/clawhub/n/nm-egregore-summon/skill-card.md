## Description: <br>
Autonomous orchestrator for manifest work items through the development lifecycle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to run manifest-defined work items through intake, build, quality, and shipping stages. It coordinates specialist skills, local state files, branches, pull request work, retries, budget checks, and resumable autonomous execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can continue autonomous development work without asking for clarification. <br>
Mitigation: Run it only for work items that are actionable, review the manifest and decision logs, and prefer bounded mode for normal releases. <br>
Risk: The skill may create or switch git branches, use worktrees, prepare pull requests, and merge when auto_merge is enabled. <br>
Mitigation: Review .egregore configuration before launch, keep auto_merge disabled unless automated merging is intended, and inspect pull requests before merging. <br>
Risk: The skill may read GitHub issue comments and local .egregore state while orchestrating work. <br>
Mitigation: Use it only in repositories where that access is acceptable and avoid placing secrets or sensitive data in issue text or orchestration state files. <br>
Risk: Indefinite mode and scheduled resume prompts can keep work running longer than expected. <br>
Mitigation: Use bounded mode by default and cancel scheduled resume prompts or watchdogs when the run should stop. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-egregore-summon) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/egregore) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local .egregore state files, git branches, worktrees, pull requests, and scheduled resume prompts when executed by an agent.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
