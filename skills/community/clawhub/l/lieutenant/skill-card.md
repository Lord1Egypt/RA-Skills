## Description: <br>
Lieutenant scans messages, agent cards, and A2A communications for prompt injection, jailbreaks, data exfiltration, and other malicious AI-agent patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jd-delatorre](https://clawhub.ai/user/jd-delatorre) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security engineers use Lieutenant to scan untrusted agent content, verify external A2A agent cards, and add middleware checks before agent interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional API mode can send scanned prompts, messages, or agent cards to a remote TrustAgents service. <br>
Mitigation: Use local mode for private prompts, secrets, or sensitive agent cards; use API mode only when remote analysis is approved, keep API keys scoped, and use only trusted API endpoints. <br>


## Reference(s): <br>
- [Lieutenant on ClawHub](https://clawhub.ai/jd-delatorre/lieutenant) <br>
- [TrustAgents](https://trustagents.dev) <br>
- [TrustAgents API Docs](https://trustagents.dev/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python snippets, and optional JSON scan results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional API mode can use TrustAgents, and semantic analysis requires an OpenAI API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
