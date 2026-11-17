## Description:

MigraQ helps users plan Tencent Cloud migrations with cross-cloud resource scanning, target specification matching, TCO analysis, and migration planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haobinaa](https://clawhub.ai/user/haobinaa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud migration engineers, and Tencent Cloud customers use MigraQ to ask migration questions, scan or import resource context, compare target specifications, estimate costs, and plan Tencent Cloud migrations. Authenticated mode is intended only for actions that execute migrations or manage cloud resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Migration prompts, inventory, billing, and planning context may be sent to Tencent Cloud endpoints.

Mitigation: Send only migration context that is appropriate for Tencent Cloud processing and avoid placing secrets or unrelated sensitive data in prompts.

Risk: Authenticated migration or resource-management actions use Tencent Cloud AK/SK credentials and can affect cloud resources.

Mitigation: Use environment variables for credentials, prefer least-privilege keys, confirm before authenticated operations, and use separate sessions when moving from unauthenticated consultation to authenticated operations.

Risk: The security summary flags unsafe command templates and configurable forwarding paths, including endpoint overrides and dry-run output risks.

Mitigation: Run scripts through argument-array execution, review or remove CMG_NO_AUTH_* endpoint overrides before use, keep HTTPS trusted endpoints, and avoid dry-run commands with real credentials in shared logs.

## Reference(s):

- [MigraQChatCompletions API Reference](references/api/MigraQChatCompletions.md)
- [MigraQ ClawHub Skill Page](https://clawhub.ai/haobinaa/skills/migraq)
- [Tencent Cloud CMG API Endpoint](https://cmg.ai.tencentcloudapi.com)
- [Tencent Cloud MSP Endpoint](https://msp.cloud.tencent.com)
- [Tencent Cloud API Keys Console](https://console.cloud.tencent.com/cam/capi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote responses may stream for several minutes; authenticated resource operations require Tencent Cloud AK/SK environment variables.]

## Skill Version(s):

1.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
