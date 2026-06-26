## Description: <br>
Make paid x402 API requests with automatic USDC payment on Base after a service endpoint has been found. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xRAG](https://clawhub.ai/user/0xRAG) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to have an agent call paid x402 API endpoints through the `awal` CLI, including method, body, headers, query parameters, and maximum payment controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend USDC from an authenticated wallet without a mandatory per-request confirmation or spend cap. <br>
Mitigation: Require the agent to show the endpoint, method, headers, body, query data, and maximum USDC spend before each use, then obtain explicit approval and include `--max-amount` on every payment. <br>
Risk: Paid requests may send secrets or sensitive personal data to unknown x402 endpoints. <br>
Mitigation: Review endpoint trust and request contents before execution, and avoid sending secrets or sensitive personal data to unknown services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xRAG/pay-for-service) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate paid USDC transactions through an authenticated wallet when executed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
