## Description:

Guides Go developers in using the unofficial go-elevenlabs client to call the ElevenLabs REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to add and use the go-elevenlabs Go client for ElevenLabs REST API calls, including voices, text-to-speech, transcription, and account operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and submitted text, audio, or voice samples are sent to ElevenLabs for processing.

Mitigation: Keep the xi-api-key in an environment variable and send only content approved for processing by ElevenLabs.

Risk: Generation calls can use account credits, and voice cloning or delete operations change account state.

Mitigation: Confirm authorization before credit-consuming, cloning, or delete operations; clone only voices the user has rights to.

Risk: The security review is incomplete because three local references did not resolve.

Mitigation: Check the missing references and inspect the skill before installing.

## Reference(s):

- [Setup and reference](references/setup.md)
- [go-elevenlabs project page](https://github.com/psyb0t/go-elevenlabs)
- [go-elevenlabs Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-elevenlabs)
- [ClawHub skill page](https://clawhub.ai/psyb0t/skills/go-elevenlabs)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover API client setup, authentication, requests, and response handling.]

## Skill Version(s):

0.16.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
