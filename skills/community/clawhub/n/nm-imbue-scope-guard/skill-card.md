## Description: <br>
Scores feature worthiness and enforces branch-size limits against overengineering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill during brainstorming, planning, and execution to score proposed work, compare it with backlog items, and keep branches within scope budgets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can push internal planning details into GitHub issues or discussions by default. <br>
Mitigation: Require explicit confirmation before every GitHub issue, comment, or discussion; avoid publishing sensitive reasoning; and limit use to repositories where disclosure and write actions are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-imbue-scope-guard) <br>
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/imbue) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with inline shell commands and issue templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose GitHub issue or discussion content for deferred work; review before publishing.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
