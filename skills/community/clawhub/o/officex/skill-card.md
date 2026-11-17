## Description:

Complete OfficeX platform skill for end-user consumers and app developers interacting with the OfficeX REST API and its credit-based app marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mevdragon](https://clawhub.ai/user/mevdragon)

### License/Terms of Use:


## Use Case:

External OfficeX users and app developers use this skill to make OfficeX API calls, build and publish marketplace apps, manage installs and wallets, implement credit billing, handle webhooks, embed iframe app experiences, and debug authentication or API errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill covers broad billing, wallet, payout, deletion, and admin workflows that could cause unwanted financial or account changes.

Mitigation: Use a dedicated low-privilege OfficeX account and require explicit confirmation before any billing, deletion, payout, wallet, or admin operation.

Risk: The skill discusses master keys, superadmin secrets, payment tokens, install secrets, and reusable third-party API credentials.

Mitigation: Avoid giving the agent master keys, superadmin secrets, payment tokens, or reusable third-party API keys; scope credentials narrowly and rotate them when exposure is suspected.

Risk: App documentation, context_prompt, downloaded skill text, iframe parameters, and agent_context values may be untrusted.

Mitigation: Review and isolate those inputs before use, and do not let them override local security policy or approval requirements.

## Reference(s):

- [OfficeX Developer Portal](https://officex.app/store/en/developer/)
- [OfficeX Production API](https://cloud.officex.app/v1)
- [OfficeX Staging API](https://staging-backend.cloud.officex.app/v1)
- [OfficeX Skill Page](https://clawhub.ai/mevdragon/skills/officex)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash, TypeScript, JavaScript, Python, JSON, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes REST endpoint patterns, authentication header guidance, billing flow examples, webhook handling, iframe embedding configuration, and fault-tolerance guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
