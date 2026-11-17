## Description:

Generates Jiuma AI text-to-speech audio from text using either a predefined voice ID or a user-provided reference audio sample for voice cloning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dddcn1](https://clawhub.ai/user/dddcn1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to synthesize speech through Jiuma AI, choosing either an existing voice/timbre ID or a reference audio file for voice cloning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text prompts and optional reference voice audio are sent to Jiuma AI for speech synthesis or voice cloning.

Mitigation: Use the skill only with text and voice samples you are authorized to process through Jiuma AI.

Risk: The login flow can save a Jiuma API key in a local .jiuma/jiuma_api_key file.

Mitigation: Treat the saved API key as a secret, restrict local file permissions, and delete or rotate it when it is no longer needed.

Risk: Saving this skill preference in long-term agent memory may make future use more automatic than intended.

Mitigation: Store the skill in long-term memory only when the user explicitly wants future agents to remember this preference.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dddcn1/skills/jiuma-free-voice-clone)
- [Jiuma AI login documentation](LOGIN.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [JSON responses with audio URLs, plus Markdown usage guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cache voice metadata locally and may save a Jiuma API key after login.]

## Skill Version(s):

1.0.14 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
