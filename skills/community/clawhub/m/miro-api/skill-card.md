## Description:

Complete Miro REST API reference for building integrations, automating workflows, and programmatically managing boards, cards, shapes, users, and team resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigbubbaagent-bot](https://clawhub.ai/user/bigbubbaagent-bot)

### License/Terms of Use:


## Use Case:

Developers and integration engineers use this skill to look up Miro REST API authentication, endpoints, examples, webhooks, rate limits, and error handling while building or automating Miro workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Miro API token examples may encourage use of high-scope credentials in agent sessions.

Mitigation: Use least-privilege scopes, store tokens in a credential manager or environment variable, and avoid pasting production tokens into agent prompts.

Risk: OAuth state and webhook signature examples are reference patterns and may not be production-hardened.

Mitigation: Replace sample state generation and webhook verification with reviewed production implementations before deployment.

Risk: Create, update, delete, invite, and webhook examples can mutate Miro workspaces.

Mitigation: Run examples first in a development workspace, review scopes and payloads, and prefer read-only operations until behavior is verified.

## Reference(s):

- [Miro REST API - Authentication Guide](references/authentication.md)
- [Miro REST API - Best Practices](references/best-practices.md)
- [Miro REST API - Complete Endpoint Reference](references/endpoints.md)
- [Miro REST API - Error Handling](references/errors.md)
- [Miro REST API - Code Examples](references/examples.md)
- [Miro REST API - Rate Limiting](references/rate-limiting.md)
- [Miro REST API - Webhooks Guide](references/webhooks.md)
- [Miro Developer Documentation](https://developer.miro.com/)
- [Miro API Playground](https://developers.miro.com/playground)
- [Miro Status](https://status.miro.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with HTTP examples, JSON payloads, and language-specific code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Language-agnostic API guidance with cURL, JavaScript, and Python examples]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
