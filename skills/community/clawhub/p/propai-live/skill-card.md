## Description:

PropAI Live is the complete AI-powered realtor automation suite, bundling OpenClaw core, PropAI Sync for WhatsApp lead management, Social Flow for Meta operations, and essential realtor skills for lead processing and AI assistance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vishalgojha](https://clawhub.ai/user/vishalgojha)

### License/Terms of Use:


## Use Case:

External real estate teams and agents use PropAI Live to route lead follow-up, WhatsApp messaging, social posting, and general assistant requests into proposed CLI actions with license checks and explicit confirmation for writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose high-impact messaging, social posting, spending, or lead-storage actions.

Mitigation: Require explicit user confirmation before message sending, posting, spending, or data mutation, and keep write commands visible for review before execution.

Risk: License keys and tokens could be exposed if they are sent to an untrusted or plain-HTTP license API endpoint.

Mitigation: Use the documented HTTPS production endpoint or a trusted local development endpoint, and do not pass license keys to untrusted services.

Risk: Connected WhatsApp, Meta, and lead-storage permissions may grant broader access than a task needs.

Mitigation: Review connected account scopes before use and gate write flows with the license guard and feature-specific entitlements.

Risk: Cached local license state and offline grace behavior can allow operation without a fresh remote validation check.

Mitigation: Force remote validation before high-impact writes when connectivity is available, and treat degraded validation status as a reason to pause sensitive actions.

## Reference(s):

- [PropAI Live on ClawHub](https://clawhub.ai/vishalgojha/skills/propai-live)
- [Publisher profile](https://clawhub.ai/user/vishalgojha)
- [OpenClaw docs](https://openclaw.ai)
- [PropAI Live License API Contract](references/license-api-contract.md)
- [License API starter template](assets/license-api/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with command code blocks, status summaries, assumptions, and risk labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asks for confirmation before write actions and avoids printing secrets in output.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
