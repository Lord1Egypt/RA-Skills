## Description:

MCM Agent helps users save and recall explicitly approved cross-device AI memories through a configured cloud memory account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoxuan0820-ctrl](https://clawhub.ai/user/xiaoxuan0820-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage AI memory across supported agent environments, saving or recalling categorized memory only after explicit user requests and consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected memory content may be stored in a third-party cloud account.

Mitigation: Sync only after explicit save or recall requests, avoid sensitive secrets, and confirm the provider's retention controls before use.

Risk: The skill requires a service API key.

Mitigation: Configure only the intended service key, keep it out of shared transcripts and source files, and rotate or revoke it if exposure is suspected.

Risk: Activation triggers are broader than ideal for a memory-sync skill.

Mitigation: Require explicit user intent and confirmation before applying, saving, or retrieving memories.

## Reference(s):

- [ClawSafe homepage](https://clawsafe.vip)
- [ClawHub skill page](https://clawhub.ai/xiaoxuan0820-ctrl/skills/mcm-agent)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, API Calls, Text]

**Output Format:** [Markdown or plain text guidance with user prompts and categorized memory content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided API key and explicit user consent before save or recall sync actions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
