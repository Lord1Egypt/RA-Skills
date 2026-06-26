## Description: <br>
Review OpenRouter usage, analytics, and troubleshooting data via API. Use when the user asks for spend/usage monitoring, activity trends, per-key management reporting, or deep investigation of specific request IDs (latency, provider fallback, finish reason, token/cost breakdown). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plgonzalezrx8](https://clawhub.ai/user/plgonzalezrx8) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to monitor OpenRouter spend, usage trends, credit consumption, and per-key activity, and to investigate specific generation IDs during latency, cost, fallback, or finish-reason incidents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles OpenRouter API and management credentials. <br>
Mitigation: Use least-privilege keys, keep .env files private, and verify which credential source is loaded before running commands. <br>
Risk: CSV and report outputs can contain sensitive usage, spend, key, and troubleshooting data. <br>
Mitigation: Export reports only to deliberate non-sensitive paths and protect or remove generated files according to local data-handling policy. <br>


## Reference(s): <br>
- [Endpoint reference and field guide](references/endpoints.md) <br>
- [OpenRouter API base URL](https://openrouter.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; CLI output may be text, Markdown, JSON, or CSV.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenRouter management key for account analytics or a regular OpenRouter API key for generation lookup; CSV export writes local report files when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
