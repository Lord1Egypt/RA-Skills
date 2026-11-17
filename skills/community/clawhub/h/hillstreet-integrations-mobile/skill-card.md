## Description:

Set up, repair, and verify Composio and Open-Connect integrations for Open-Box, Open-TGate, Open-Teleset, Open-System, Twilio, GitHub, Docker Hub, Cloudflare, Supabase, Sentry, Zeabur, Proton Pass, and ChatGPT from Android Chrome using remotely hosted tools and OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace administrators use this skill to connect and troubleshoot supported integrations from Android Chrome and to report which authorization, discovery, and execution stages are verified.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports a low-probability concern about autonomous decision-making despite an overall benign verdict.

Mitigation: Review proposed changes before execution and require the concrete user request and applicable provider confirmation for messages, purchases, calls, exports, or permission changes.

Risk: Integration setup and administration can involve OAuth credentials or changes to account access.

Mitigation: Keep credentials out of chat, plugins, source files, and logs; use the provider's supported sign-in flow and preserve authorization and project-grant approval gates.

## Reference(s):

- [Admin access](artifact/references/admin-access.md)
- [Mobile use](artifact/references/mobile-use.md)
- [Service routes](artifact/references/service-routes.md)
- [Clawhub release](https://clawhub.ai/hillstreet-ph/skills/hillstreet-integrations-mobile)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration instructions]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup links, bounded verification results, and specific blockers; excludes credentials and session material.]

## Skill Version(s):

1.0.10 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
