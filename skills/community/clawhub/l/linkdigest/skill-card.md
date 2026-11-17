## Description:

Reads hard-to-access social links and returns transcripts, on-screen text, image descriptions, captions, and post metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents use this skill to read or summarize social posts and videos that ordinary page fetching cannot access, including Xiaohongshu, Douyin, TikTok, YouTube, and X links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted links and fetched media are processed by an external digest service.

Mitigation: Avoid private, confidential, sensitive, or access-token-bearing links unless the user explicitly intends that processing.

Risk: A partial digest or speech-recognized transcript may omit or misstate details.

Mitigation: Check reported gaps and identify speech recognition as the source before quoting names or numbers as fact.

## Reference(s):

- [linkdigest on ClawHub](https://clawhub.ai/jackchew7143/skills/linkdigest)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes transcripts, image descriptions, captions, and metadata; optional translations, post breakdowns, and answers to questions.]

## Skill Version(s):

0.0.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
