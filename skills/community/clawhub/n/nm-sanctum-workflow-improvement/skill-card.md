## Description: <br>
Evaluates and improves skills, agents, commands, and hooks after a workflow slice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill after a workflow slice to identify friction in skills, agents, commands, and hooks, agree on bounded improvements, implement them, and validate the before-and-after effect. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow details may be published externally through GitHub issues or Discussions. <br>
Mitigation: Review and redact session context before any external posting, and require explicit confirmation before creating issues or Discussion posts. <br>
Risk: Automatic issue creation can expose deferred items, repository details, or sensitive workflow context. <br>
Mitigation: Use duplicate checks, restrict labels and issue bodies to necessary context, and give users a clear opt-out or approval step before publication. <br>
Risk: Workflow recommendations may change skills, agents, commands, or hooks in ways that degrade future agent behavior. <br>
Mitigation: Keep changes bounded, review proposed edits before deployment, and validate with before-and-after metrics and targeted tests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-sanctum-workflow-improvement) <br>
- [Project homepage from ClawHub metadata](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>
- [Auto issue creation module](modules/auto-issue-creation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include workflow improvement plans, validation metrics, issue creation guidance, and file-change recommendations.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
