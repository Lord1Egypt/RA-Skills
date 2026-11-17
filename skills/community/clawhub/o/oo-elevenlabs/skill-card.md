## Description:

Use the OOMOL-connected ElevenLabs service to read, create, and delete ElevenLabs data through natural-language requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill through their OOMOL-connected ElevenLabs account to inspect voices, models, subscriptions, and generation history, or to create speech and sound effects. It also supports downloading audio for existing history items and deleting a history item with explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup may run downloaded installer code that has not been verified and may introduce additional agent skills.

Mitigation: Review the CLI installation separately, verify a specific release, and disable automatic skill synchronization unless additional skills are intended.

Risk: Creating speech or sound effects changes ElevenLabs account state, and deleting a history item removes account data.

Mitigation: Confirm the exact generation payload and effect before running write actions, and get explicit approval for the specific history item before deletion.

Risk: The OOMOL connection can perform the requested ElevenLabs operations and handle audio through transit storage.

Mitigation: Connect only the intended ElevenLabs account and keep the skill's approval requirements for generation and deletion.

## Reference(s):

- [ElevenLabs API authentication documentation](https://elevenlabs.io/docs/api-reference/authentication)
- [ElevenLabs](https://elevenlabs.io)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-elevenlabs)

## Skill Output:

**Output Type(s):** [API responses, JSON, Audio, Shell commands, Configuration instructions]

**Output Format:** [JSON responses and generated or retrieved audio]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audio is returned through connector transit storage; timestamped speech also includes character-level timing metadata.]

## Skill Version(s):

1.0.7 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
