## Description:

Transcribes videos from local files or supported links into readable text and can generate summaries, rewrites, and other copy from the content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, editors, and other users can turn a local or publicly accessible video into a transcript, summary, meeting notes, or reusable copy using a custom prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos, prompts, task IDs, and related metadata are sent to the Guaikei cloud service; actual data handling may differ from the skill's documentation.

Mitigation: Use only media approved for third-party processing; avoid confidential recordings unless the provider's retention practices are acceptable.

Risk: A supplied URL may cause the downloader to retrieve and upload unexpected content, including internal-network resources.

Mitigation: Use trusted, publicly accessible video URLs or approved local files; do not submit untrusted or internal-network URLs.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/engheng-art/skills/guaikei-video-speech-recognition)
- [Guaikei website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text transcript or prompt-directed prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Guaikei API token and cloud processing; transcription quality depends on audio clarity.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
