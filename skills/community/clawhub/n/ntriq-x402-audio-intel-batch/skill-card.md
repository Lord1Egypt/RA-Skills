## Description: <br>
Batch audio transcription for up to 500 files. Flat $9.00 USDC via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to send batches of audio file URLs to a paid transcription endpoint and receive transcripts, detected language, and duration metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Each call can trigger a $9 USDC payment through x402. <br>
Mitigation: Review payment headers, endpoint, and expected batch size before executing requests. <br>
Risk: Submitted audio URLs, fetched recordings, and resulting transcripts are shared with the third-party transcription provider. <br>
Mitigation: Do not submit confidential, regulated, or private recordings unless authorized and comfortable with the provider's privacy and retention practices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ntriq-gh/ntriq-x402-audio-intel-batch) <br>
- [Publisher profile](https://clawhub.ai/user/ntriq-gh) <br>
- [Ntriq x402 service homepage](https://x402.ntriq.co.kr) <br>
- [x402 protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The remote service response contains per-file transcript text, language, duration, status, and source URL metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
