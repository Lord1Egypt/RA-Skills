## Description: <br>
Subagent-driven development. Dispatch fresh subagent per task with 2-stage review (spec + quality). Cost-aware model routing. From Superpowers by Jesse Vincent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to structure implementation work around fresh subagents, separate specification review, separate code quality review, and final test verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can lead to code changes, test runs, model usage, and commits. <br>
Mitigation: Review diffs and require approval for commits or high-impact commands before applying changes. <br>
Risk: Subagent handoffs and reviews can still produce incorrect or misleading development guidance. <br>
Mitigation: Keep the separate specification review, code quality review, and full test suite verification before considering work complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangxiaofei860208-source/lobster-subagent-dev) <br>
- [Superpowers project inspiration](https://github.com/obra/superpowers) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown workflow guidance with task, review, testing, and command recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide repository edits, tests, model routing, and commits; no hidden code or credential access reported by security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
