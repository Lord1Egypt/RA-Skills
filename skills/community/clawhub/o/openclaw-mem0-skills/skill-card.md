## Description:

Persistent long-term memory across sessions that remembers identity, preferences, rules, tech stack, and projects so new conversations can start with user context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kartik-mem0](https://clawhub.ai/user/kartik-mem0)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to build, review, export, and hand off persistent Mem0-backed profile context across agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can retain personal or work context longer than intended.

Mitigation: Review stored memories periodically and delete stale or sensitive entries.

Risk: Users may accidentally provide credentials, secrets, or confidential business data during onboarding or review.

Mitigation: Do not store credentials or secrets; configure API keys through the plugin setup and environment only.

Risk: Memory workflows depend on the Mem0 plugin and API key being available.

Mitigation: Confirm the plugin is installed and MEM0_API_KEY is configured before relying on onboarding, review, export, or handoff workflows.

## Reference(s):

- [Mem0](https://mem0.ai)
- [Mem0 API Keys](https://app.mem0.ai/dashboard/api-keys)
- [ClawHub Skill Page](https://clawhub.ai/kartik-mem0/skills/openclaw-mem0-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with occasional shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Mem0 plugin and MEM0_API_KEY for memory operations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
