## Description: <br>
Delegates tasks to Qwen CLI via delegation-core for Alibaba's models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate large-context code analysis, summarization, and batch processing tasks to the Qwen CLI through a shared delegation executor. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated prompts can include local files and send their contents to a third-party Qwen service. <br>
Mitigation: Review selected paths and prompts before execution; avoid sending secrets, private data, or regulated content unless approved for that service. <br>
Risk: The workflow may use Qwen login state or QWEN_API_KEY credentials. <br>
Mitigation: Use scoped credentials where possible and avoid storing API keys in files, prompts, logs, or shell history. <br>
Risk: Model access, rate limits, and costs vary by Qwen model and provider. <br>
Mitigation: Verify available models, quotas, and pricing before batch or large-context delegation. <br>
Risk: The skill depends on the shared night-market.delegation-core configuration. <br>
Mitigation: Install and review the delegation-core dependency before relying on Qwen auto-selection or executor behavior. <br>


## Reference(s): <br>
- [Qwen-specific configuration](modules/qwen-specifics.md) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conjure) <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-conjure-qwen-delegation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Qwen CLI command examples, delegation executor usage, model selection guidance, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
