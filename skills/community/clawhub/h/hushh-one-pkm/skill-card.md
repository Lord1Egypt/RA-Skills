## Description:

Use when an OpenClaw agent needs to access a Hushh One user's Personal Knowledge Model through the Hushh MCP bridge, covering developer-token setup, dynamic scope discovery, explicit consent, consent polling, scoped export retrieval, and privacy boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hushh](https://clawhub.ai/user/hushh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to connect an agent to Hushh One PKM data through the Hushh MCP bridge with explicit user consent, narrow dynamic scopes, and controlled export handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Developer tokens could be exposed if pasted into chat, URLs, prompts, committed files, or tool arguments.

Mitigation: Store HUSHH_DEVELOPER_TOKEN only in the local secret or environment mechanism and refresh it through the Hushh developer workspace if authorization fails.

Risk: An agent could request overly broad PKM access or reuse a broader grant than the task requires.

Mitigation: Discover user-specific scopes, choose the least-privilege returned scope, require explicit consent, and pass expected_scope when retrieving an export.

Risk: Plaintext personal data may leave Hushh's zero-knowledge boundary when delivered to downstream systems.

Mitigation: Define explicit purpose, retention, encryption or masking, access control, deletion, and audit ownership before any downstream system receives plaintext data.

Risk: Personal data handling may exceed the granted purpose after consent is approved.

Mitigation: Treat decrypted payloads as purpose-bound, scoped, and time-boxed; store workflow metadata by default instead of raw PKM, KYC documents, full email bodies, vault data, user keys, or broad profiles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hushh/skills/hushh-one-pkm)
- [Hushh developer workspace](https://uat.one.hushh.ai/developers)
- [Publisher profile](https://clawhub.ai/user/hushh)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown instructions with tool names, setup steps, and consent-flow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs agents to use scoped MCP tools and purpose-bound handling for personal data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
