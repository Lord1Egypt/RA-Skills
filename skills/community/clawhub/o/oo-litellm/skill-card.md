## Description:

Connects to LiteLLM to inspect available models and key limits or submit chat, message, and embedding requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use it to inspect available models and virtual-key limits, then send chat, message, or embedding requests through a connected LiteLLM account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model requests may incur charges even though the skill describes its actions as reads.

Mitigation: Require user-directed generation with agreed inputs, model, and spending limits; use a restricted LiteLLM key.

Risk: CLI setup may install software or affect managed-skill synchronization; installer behavior was not verified.

Mitigation: Review the CLI installer and its synchronization behavior, and disable synchronization if unwanted.

## Reference(s):

- [LiteLLM](https://www.litellm.ai)
- [LiteLLM virtual keys documentation](https://docs.litellm.ai/docs/proxy/virtual_keys)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-litellm)

## Skill Output:

**Output Type(s):** [API calls, JSON, Guidance]

**Output Format:** [Structured JSON responses and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the connected LiteLLM account and selected upstream model.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
