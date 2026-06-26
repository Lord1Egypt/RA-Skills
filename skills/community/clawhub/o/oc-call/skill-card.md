## Description: <br>
Calls a remote OpenClaw instance through an OpenAI-compatible Gateway HTTP API with multi-turn session continuity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anlinxi](https://clawhub.ai/user/anlinxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can route a prompt to a remote OpenClaw Gateway when they want the remote instance to answer while preserving a reusable session key across requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill forwards prompts to a hardcoded HTTP gateway with a hardcoded token. <br>
Mitigation: Install only when you own or fully trust the configured OpenClaw Gateway and local network path; override the URL and token before production use. <br>
Risk: Session continuity is stored in ~/.oc_session and reused until cleared. <br>
Mitigation: Clear or rotate the session with the provided management commands when changing users, tasks, or trust boundaries. <br>
Risk: Prompt contents may traverse an unencrypted local-network HTTP connection. <br>
Mitigation: Avoid sending secrets through the skill unless you replace the endpoint with a trusted HTTPS gateway. <br>


## Reference(s): <br>
- [Oc Call on ClawHub](https://clawhub.ai/anlinxi/oc-call) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text responses with command-line usage and environment-variable configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Forwards one user prompt per invocation to the configured OpenClaw Gateway and prints the returned assistant message.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
