## Description: <br>
Delegates tasks to Qwen CLI via delegation-core for Alibaba's models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate batch processing, summarization, code analysis, and multi-file review tasks to Qwen CLI when the shared delegation core selects Qwen or a large context window is useful. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected files included with @path or recursive globs may be sent to Qwen or Alibaba-backed services. <br>
Mitigation: Review selected paths before delegation and exclude secrets, private code, or data that should not leave the local environment. <br>
Risk: Broad CLI or delegation triggers may activate the skill when Qwen delegation was not intended. <br>
Mitigation: Narrow local triggers or confirm the selected delegation target before running generated Qwen commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-conjure-qwen-delegation) <br>
- [Clawdis homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conjure) <br>
- [Qwen-specific configuration](modules/qwen-specifics.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and Qwen CLI prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Qwen CLI commands, model choices, file inclusion patterns, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
