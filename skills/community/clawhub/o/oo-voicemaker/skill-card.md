## Description:

Connect to Voicemaker to list text-to-speech voices and generate speech from text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to browse Voicemaker voices and generate speech from text through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If first-time setup is needed, the provided installer executes remote code whose contents are unverified; startup skill synchronization may also affect other agent skills.

Mitigation: Review and install a verified CLI release yourself, and consider disabling startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1 as documented upstream.

Risk: Text submitted for speech generation passes through OOMOL and Voicemaker and may consume credit.

Mitigation: Treat submitted text as processed by both services and check expected credit use before generating speech.

## Reference(s):

- [Voicemaker API documentation](https://developer.voicemaker.in/apidocs/authentication)
- [Voicemaker](https://voicemaker.in/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Voicemaker ClawHub release](https://clawhub.ai/oomol/skills/oo-voicemaker)

## Skill Output:

**Output Type(s):** [Text, JSON, Audio URLs]

**Output Format:** [Structured JSON responses with generated audio URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Speech generation may use account credit.]

## Skill Version(s):

1.0.5 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
