## Description:

Search ElevenReader voices, models, and account information, and turn text into spoken audio through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using ElevenReader can search available voices, inspect models and account information, and turn text into spoken audio through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance includes remote installers whose contents are unverified.

Mitigation: Install the CLI separately using a reviewed, integrity-verified method; do not let a failed reading request trigger installation.

Risk: The read_text action uploads text and generated audio to connector transit storage, although the skill's safety guidance classifies it as read-only.

Mitigation: Before using read_text, explicitly authorize the text and its upload, especially for private material, and check the provider's storage controls.

## Reference(s):

- [ElevenReader](https://elevenlabs.io/text-reader)
- [ElevenLabs API documentation](https://elevenlabs.io/docs/api-reference/introduction)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Audio]

**Output Format:** [JSON connector requests and responses, with generated spoken audio]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audio is produced for text-to-speech requests.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
