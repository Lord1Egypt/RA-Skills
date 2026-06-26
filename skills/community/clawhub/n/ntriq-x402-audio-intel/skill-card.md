## Description: <br>
AI audio transcription - speech-to-text for mp3/wav/m4a/ogg with language auto-detection, timestamps, and $0.05 USDC x402 payment per call. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit audio by URL or base64 payload to a paid transcription API and receive transcript text, detected language, timestamps, and segment details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio submitted by URL or base64 is processed by a third-party ntriq x402 service and may contain personal or confidential speech. <br>
Mitigation: Use non-sensitive audio unless the provider's privacy and retention practices are acceptable for the intended data. <br>
Risk: Each service call is disclosed as a paid $0.05 USDC x402 transaction. <br>
Mitigation: Confirm the payment amount and x402 charge before sending the request. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ntriq-gh/ntriq-x402-audio-intel) <br>
- [ntriq x402 service homepage](https://x402.ntriq.co.kr) <br>
- [x402 protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API Calls, shell commands, guidance] <br>
**Output Format:** [JSON transcription response with transcript text, language metadata, duration, timestamps, and segment objects; documentation may include Markdown and curl examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts an audio_url or audio_base64 input, optional language hint, and requires an x402 payment header for paid service calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
