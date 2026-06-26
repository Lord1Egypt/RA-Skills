## Description: <br>
Transparent LLM proxy that monitors and enforces policies on AI agent behavior, evaluating responses against configurable rules for hallucinations, PII leaks, prompt injection, and workflow violations before they reach users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sentinel199](https://clawhub.ai/user/sentinel199) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and teams use this skill to configure Open Sentinel as a transparent proxy for OpenAI-compatible LLM clients, adding policy checks for agent responses and multi-turn workflows. It helps route setup, policy authoring, CLI usage, and configuration for response monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overstate blocking protection because the documented default judge engine evaluates asynchronously and some failures pass requests through. <br>
Mitigation: Test the selected engine and mode against expected unsafe outputs before relying on it as a safety boundary, and use critical blocking paths where immediate enforcement is required. <br>
Risk: Provider API keys are required and proxy traffic may include sensitive prompts or responses. <br>
Mitigation: Scope provider API keys carefully, keep credentials in environment variables, and disable or tightly control tracing for sensitive traffic. <br>
Risk: The release depends on the upstream opensentinel package distributed outside NVIDIA. <br>
Mitigation: Review the upstream PyPI package and installation source before deployment. <br>


## Reference(s): <br>
- [Open Sentinel GitHub](https://github.com/open-sentinel/open-sentinel) <br>
- [Open Sentinel Documentation](https://github.com/open-sentinel/open-sentinel/tree/main/docs) <br>
- [Open Sentinel PyPI Package](https://pypi.org/project/opensentinel) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell, Python, and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proxy setup steps, policy examples, CLI commands, and configuration guidance.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
