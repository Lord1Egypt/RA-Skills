## Description:

Creates a KakaoTalk channel AI agent with Vercel serverless deployment and an optional Relay mode that connects to a local computer for memory and file access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifeissea](https://clawhub.ai/user/lifeissea)

### License/Terms of Use:

MIT

## Use Case:

Developers and channel operators use this skill to deploy a KakaoTalk chatbot webhook, either as a simple cloud-hosted assistant or as a relay to a local agent with memory-backed responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Relay and local modes can expose private memory, callbacks, credentials, and a persistent local service.

Mitigation: Review Relay mode before installation, use a dedicated low-privilege account or machine, and avoid enabling the launchd service until uninstall and log-retention controls are clear.

Risk: Webhook callbacks and local relay traffic can send data to unintended destinations if callback handling is too permissive.

Mitigation: Set webhook authentication and restrict callback destinations to Kakao-controlled HTTPS hosts.

Risk: Local memory may be sent to an external LLM during response generation.

Mitigation: Avoid sending MEMORY.md or similar local context to external LLMs unless explicitly intended.

Risk: Secrets written into service configuration may persist beyond the intended installation period.

Mitigation: Rotate any secrets written into a plist or local environment file after testing or uninstalling the service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lifeissea/skills/kakaotalk)
- [Kakao i Open Builder Skill Response Format](https://i.kakao.com/docs/skill-response-format)
- [Kakao API Reference Summary](references/kakao-api.md)
- [Kakao Business](https://business.kakao.com)
- [Vercel](https://vercel.com)
- [Supabase](https://supabase.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline code, shell commands, and deployment configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Kakao Open Builder webhook responses as JSON when deployed.]

## Skill Version(s):

1.2.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
