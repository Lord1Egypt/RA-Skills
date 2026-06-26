## Description: <br>
Runtime prompt injection detection for AI agents. Checks tool outputs for hidden instructions before your agent acts on them. 98% detection rate on agent attacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dmilstein-match](https://clawhub.ai/user/dmilstein-match) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent operators use this skill to check external tool outputs for prompt injection before allowing an agent to act on retrieved content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends inspected tool outputs, task context, and an LLM API key to an external guard service. <br>
Mitigation: Use only an intentionally trusted mlayer-guard endpoint, use a low-limit revocable key, and avoid sending confidential content unless explicitly approved. <br>
Risk: The security review marks the release suspicious because sensitive context and credentials may be sent without enough safeguards. <br>
Mitigation: Review the endpoint, data handling, and key-management requirements before deployment. <br>
Risk: If the guard service is unreachable, external content may remain unchecked. <br>
Mitigation: Warn the user and request confirmation before acting on the external content. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration] <br>
**Output Format:** [Markdown instructions with a JSON request example] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The guard service returns decisions such as blocked, abstain, or safe.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
