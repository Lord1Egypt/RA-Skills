## Description: <br>
Orchestrates the QUALITY pipeline stage for egregore work items, running code review, unbloat, and test updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run egregore quality checks before or during PR review, collect findings, update tests or docs, and determine whether a work item can pass or needs fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger words may cause the skill to run outside the intended quality-gate workflow. <br>
Mitigation: Invoke it for explicit egregore quality tasks and confirm the target work item, branch, or PR before acting. <br>
Risk: PR-review mode can lead to public-facing review comments or GitHub review actions. <br>
Mitigation: Review proposed comments, gh commands, and target PR details before allowing the agent to post or request changes. <br>


## Reference(s): <br>
- [Claude Night Market egregore plugin](https://github.com/athola/claude-night-market/tree/master/plugins/egregore) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON decision snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose GitHub PR review actions when used in PR-review mode.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
