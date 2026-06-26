## Description: <br>
Give your text-based OpenClaw agent the ability to see and describe images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[melnyk-anton](https://clawhub.ai/user/melnyk-anton) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers building OpenClaw agents use this skill to send public image URLs and a prompt to MoltShell, then receive a text description that can be used in the agent's reasoning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image URLs, prompts, and a bot or session identifier are sent to MoltShell and its underlying vision provider for analysis. <br>
Mitigation: Use public or non-sensitive image URLs, avoid secrets or regulated data in prompts, and confirm the external service is acceptable for the deployment environment. <br>
Risk: The bundled public sandbox key is intended for testing and can exhaust its free credits during normal use. <br>
Mitigation: Configure a dedicated, limited MoltShell API key for production use and monitor service errors or payment-required responses. <br>


## Reference(s): <br>
- [MoltShell M2M Marketplace](https://moltshell.xyz) <br>
- [ClawHub skill page](https://clawhub.ai/melnyk-anton/moltshell-vision) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [String] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a text description when analysis succeeds; may return payment, polling, or service error messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
