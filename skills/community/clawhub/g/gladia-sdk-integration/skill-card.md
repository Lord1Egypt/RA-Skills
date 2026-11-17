## Description:

Guides developers in installing and configuring Gladia's JavaScript/TypeScript and Python SDKs for speech-to-text integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gladiaio](https://clawhub.ai/user/gladiaio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to choose, install, and configure Gladia's JavaScript/TypeScript or Python SDK for speech-to-text applications, including browser and live-session integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exposing Gladia API keys in browser code can compromise credentials.

Mitigation: Keep API keys server-side and use a backend proxy for browser integrations.

Risk: Recording or streaming microphone audio may capture sensitive speech without consent.

Mitigation: Get consent before recording or streaming audio and handle it as sensitive data.

Risk: Deleting a transcription job or live session removes stored data.

Mitigation: Confirm the intended job or session before invoking delete methods.

## Reference(s):

- [Gladia SDK integration guide](https://docs.gladia.io/chapters/integrations/sdk)
- [Client configuration reference](references/client-config.md)
- [JavaScript/TypeScript SDK reference](references/javascript.md)
- [Python SDK reference](references/python.md)
- [SDK versions](references/sdk-versions.md)
- [JavaScript SDK package](https://www.npmjs.com/package/@gladiaio/sdk)
- [Python SDK package](https://pypi.org/project/gladiaio-sdk/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
