## Description: <br>
Automatically switches between cloud and local LLMs when rate limits occur, with explicit user confirmation before local code generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dhardie](https://clawhub.ai/user/dhardie) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to keep agents responsive during cloud LLM rate limits by switching to a local Ollama fallback while requiring confirmation before local-model code tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change agent LLM profiles and persist the active cloud or local mode across new agents. <br>
Mitigation: Review the active mode with /llm status and use /llm switch cloud or /llm switch local when operators need to control the profile explicitly. <br>
Risk: Local model fallback can affect code quality compared with the default cloud model. <br>
Mitigation: Keep confirmation required for local code tasks and require operators to provide the configured confirmation phrase before proceeding. <br>
Risk: Any user message containing the configured confirmation phrase is treated as approval for local-model code tasks. <br>
Mitigation: Limit use of the confirmation phrase to deliberate approvals and adjust the configured phrase if a deployment needs a more specific approval token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dhardie/llm-supervisor-agent) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/dhardie) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown command replies and notifications with LLM profile configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists cloud or local mode and uses the configured local model and confirmation phrase.] <br>

## Skill Version(s): <br>
0.2.0 (source: skill.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
