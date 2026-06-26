## Description: <br>
Delegates tasks to Gemini CLI implementing delegation-core for Google's models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate large-context analysis, summarization, pattern extraction, and batch processing tasks to an authenticated Gemini CLI when delegation-core selects Gemini. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide the agent to include project content in prompts or generated artifacts handled by external tooling. <br>
Mitigation: Use it only with project areas approved for that workflow, and avoid highly sensitive code or documentation unless the configured tooling is trusted. <br>
Risk: Gemini model availability, quotas, and costs may vary by model, account, and region. <br>
Mitigation: Check Gemini CLI authentication, selected model availability, quota status, and current pricing before large batch or high-context use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-conjure-gemini-delegation) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/athola) <br>
- [Claude Night Market Conjure homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conjure) <br>
- [Gemini-specific configuration](modules/gemini-specifics.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Gemini CLI prompts, model flags, JSON output mode, and saved Markdown delegation outputs.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
