## Description:

Give your text-based OpenClaw agent the ability to see and describe images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melnyk-anton](https://clawhub.ai/user/melnyk-anton)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to let OpenClaw agents analyze public image URLs and return text descriptions for downstream reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image URLs, prompts, and an OpenClaw agent or bot identifier are sent to MoltShell, which may expose sensitive image content or link usage across requests.

Mitigation: Use only public image URLs and non-sensitive prompts unless sharing them with MoltShell is acceptable; review deployments that use stable OPENCLAW_AGENT_ID or OPENCLAW_BOT_ID values.

Risk: The built-in sandbox key is intended for testing and can stop working after the free compute allowance is exhausted.

Mitigation: Configure a dedicated MOLTSHELL_API_KEY before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/melnyk-anton/skills/moltshell-vision)
- [MoltShell M2M Marketplace](https://moltshell.xyz)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [String]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a text image description or an error message from the MoltShell vision service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
