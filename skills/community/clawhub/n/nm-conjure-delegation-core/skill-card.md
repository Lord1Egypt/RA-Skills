## Description: <br>
Delegates tasks to Gemini or Qwen with quota tracking and error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to decide when to delegate token-heavy or repetitive work to Gemini, Qwen, or subagents while retaining local review and integration control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegation can send files or task context to external LLM services. <br>
Mitigation: Review the context before delegation and avoid sending secrets or security-sensitive work to external services. <br>
Risk: Account IDs, emails, OAuth client secrets, and usage logs may be sensitive in delegation workflows. <br>
Mitigation: Treat credentials, account metadata, and usage logs as sensitive data and limit what is captured or shared. <br>
Risk: Delegated model output can be incorrect, incomplete, or mismatched to the expected format. <br>
Mitigation: Validate delegated results for format and correctness before integrating them into the local task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-conjure-delegation-core) <br>
- [Conjure source homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conjure) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with checklists, decision matrices, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires users to validate external LLM outputs before integrating results.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
