## Description: <br>
Helps an agent route x402-enabled API requests through the Obul proxy with authentication guidance, health checks, and automatic payment negotiation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[notbdu](https://clawhub.ai/user/notbdu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to proxy x402-enabled HTTP requests through Obul with an OBUL_API_KEY, check proxy health, and understand error handling for paid upstream endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send arbitrary requests through a paid third-party proxy, which may expose sensitive request data or incur unexpected charges. <br>
Mitigation: Confirm the destination endpoint, expected price, and request contents before use; prefer scoped API keys and account spending limits when available. <br>
Risk: Exposure of OBUL_API_KEY could allow unauthorized proxy usage. <br>
Mitigation: Store the key in an environment variable, keep it out of logs and client-side code, and rotate or scope the key according to Obul account controls. <br>


## Reference(s): <br>
- [Obul homepage](https://obul.ai) <br>
- [Obul proxy health endpoint](https://proxy.obul.ai/healthz) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OBUL_API_KEY and may send requests through a paid third-party proxy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
