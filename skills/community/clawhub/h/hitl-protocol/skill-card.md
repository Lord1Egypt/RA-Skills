## Description:

HITL Protocol teaches agents and service builders how to route human decisions through HTTP 202 review URLs, structured polling results, and optional inline, SSE, or webhook transports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rotorstar](https://clawhub.ai/user/rotorstar)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and engineers use this skill to build HITL-compliant services or agents that pause autonomous workflows for human approval, selection, input, confirmation, or escalation decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents or services may trust externally supplied review, poll, events, submit, or callback URLs with credentials or review data.

Mitigation: Validate all HITL URLs, bind endpoints to trusted origins, revalidate or disable redirects, and block private or metadata network targets before sending credentials or review data.

Risk: Broad authorization headers forwarded to arbitrary HITL endpoints can leak credentials.

Mitigation: Use endpoint-specific credentials, avoid forwarding broad auth headers, and require callback registration or allowlisting before sending review results.

Risk: Inline submit tokens or sensitive form values can be exposed through messaging-platform callback data or logs.

Mitigation: Keep submit tokens in agent-side storage only, never place them in callback data, and suppress logging for sensitive fields and token-bearing review URLs.

## Reference(s):

- [HITL Protocol Specification v0.7](https://github.com/rotorstar/hitl-protocol/blob/main/spec/v0.7/hitl-protocol.md)
- [Interactive Playground](https://rotorstar.github.io/hitl-protocol/playground/index.html)
- [Agent Integration Guide](references/agent-integration.md)
- [Service Integration Guide](references/service-integration.md)
- [RFC 9110 - HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)
- [RFC 3339 - Date and Time on the Internet](https://www.rfc-editor.org/rfc/rfc3339)
- [RFC 6750 - Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code blocks, API examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Protocol-oriented guidance for HTTP 202 HITL flows, review URLs, polling, SSE, webhooks, inline actions, and security practices.]

## Skill Version(s):

0.7.2 (source: server release metadata; protocol metadata version 0.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
