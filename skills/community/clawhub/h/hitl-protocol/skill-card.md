## Description: <br>
HITL Protocol teaches agents and service builders how to add human review steps to autonomous workflows using HTTP 202 responses, review URLs, polling, optional SSE or webhooks, inline actions, and structured decision results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rotorstar](https://clawhub.ai/user/rotorstar) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers, service builders, and agent builders use this skill to implement HITL-compliant services or handle human-in-the-loop responses in agents. It covers approval, selection, input, confirmation, escalation, polling, SSE, webhooks, inline actions, and metadata for declaring HITL support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review links, submit tokens, human decisions, or private form data could be exposed if forwarded or logged carelessly. <br>
Mitigation: Send review links only through trusted channels, require HTTPS, avoid logging sensitive fields or tokens, keep review and submit tokens separate, and minimize callback payloads. <br>
Risk: Webhook or callback integrations may accept forged or excessive decision payloads if callbacks are not authenticated and scoped. <br>
Mitigation: Verify webhook signatures or equivalent authentication, use separate credentials for review and submit flows, and pass only the decision data needed to continue the workflow. <br>


## Reference(s): <br>
- [HITL Protocol Specification](https://github.com/rotorstar/hitl-protocol/blob/main/spec/v0.7/hitl-protocol.md) <br>
- [Interactive Playground](https://rotorstar.github.io/hitl-protocol/playground/index.html) <br>
- [HITL Protocol - Agent Integration Guide](references/agent-integration.md) <br>
- [HITL Protocol - Service Integration Guide](references/service-integration.md) <br>
- [RFC 9110 - HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) <br>
- [RFC 6750 - Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, code blocks, JSON examples, implementation checklists, and integration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; does not execute tools or make network calls.] <br>

## Skill Version(s): <br>
0.7.2 (source: server release metadata; protocol metadata 0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
