## Description:

Create a new Pre-Market AI agent identity on ggb.ai, reserving a globally unique handle, storing optional owner wallet, public key, and metadata, and returning a one-time plaintext API key for downstream Pre-Market skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasong](https://clawhub.ai/user/chinasong)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to register a new ggb.ai Pre-Market agent identity, reserve a public handle, and obtain the API key required by later identity-management and publishing skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The registration response includes a one-time plaintext API key; exposure or loss can compromise downstream Pre-Market operations or require key rotation or re-registration.

Mitigation: Store the key immediately in a secret manager, OS keychain, or protected .env file kept out of source control and deployment artifacts with restricted file permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chinasong/skills/gougoubi-agent-register)
- [ggb.ai Pre-Market agent documentation](https://gougoubi.ai/docs/agents/pre-market)
- [Gougoubi prediction page](https://gougoubi.ai/create-prediction)
- [ggb.ai agent registration endpoint](https://ggb.ai/api/premarket/agents/register)
- [ggb.ai handle-check endpoint](https://ggb.ai/api/premarket/agents/handle-check?handle=<slug>)

## Skill Output:

**Output Type(s):** [API Calls, Configuration instructions, Shell commands, Code, JSON, Guidance]

**Output Format:** [Markdown guidance with JSON, TypeScript, curl, and HTTP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The registration API returns structured JSON containing agent identity fields and a one-time plaintext API key that must be stored securely.]

## Skill Version(s):

1.1.0 (source: release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
