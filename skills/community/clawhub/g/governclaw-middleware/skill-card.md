## Description: <br>
GovernClaw Policy Enforcer provides a governed HTTP wrapper for OpenClaw agents that asks a GovernClaw policy service to allow or block requests before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aakash2289](https://clawhub.ai/user/aakash2289) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route OpenClaw HTTP API calls through GovernClaw for policy checks and block reasons before external requests are sent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTTP request bodies and headers are forwarded to the GovernClaw policy service, which can expose secrets such as Authorization headers, cookies, API keys, or tokens. <br>
Mitigation: Use only a GovernClaw endpoint you operate or strongly trust, keep it authenticated and protected, and avoid sending unnecessary secrets. <br>
Risk: The policy service can modify the final HTTP request before it is sent. <br>
Mitigation: Review policy rules and audit logs before deployment, and use a governance mode that matches the environment's tolerance for uncertainty. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aakash2289/governclaw-middleware) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON-like HTTP response or block/error object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a policy block reason and audit log when GovernClaw blocks a request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
