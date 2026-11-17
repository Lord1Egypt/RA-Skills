## Description:

AI audio transcription - speech-to-text for mp3/wav/m4a/ogg with language auto-detection, timestamps, and x402 payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to call a paid remote transcription service for audio files or base64 audio and receive text, detected language, timestamps, and segment details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio content or an audio URL is sent to a third-party remote transcription service.

Mitigation: Avoid sensitive, confidential, regulated, or biometric audio unless the provider supplies privacy and retention terms you trust.

Risk: Each service call requires an x402 payment.

Mitigation: Confirm the payment header, network, and listed USDC charge before submitting requests.

## Reference(s):

- [Service homepage](https://x402.ntriq.co.kr)
- [x402 protocol](https://x402.org)
- [ClawHub skill page](https://clawhub.ai/ntriq-gh/skills/ntriq-x402-audio-intel)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with HTTP and JSON examples; service responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcription responses may include full text, language probability, duration, and per-segment start/end timestamps.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
