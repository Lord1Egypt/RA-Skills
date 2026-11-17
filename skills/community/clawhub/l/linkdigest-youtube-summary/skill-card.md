## Description:

Summarizes YouTube videos with timestamped transcripts, key points, on-screen text, and optional translations through LinkDigest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn YouTube links into video summaries, timestamped transcripts, on-screen text, and optional Chinese translations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted links or share text are sent to LinkDigest, and text results may be cached by link.

Mitigation: Submit only content you are comfortable sharing with LinkDigest; avoid private or sensitive links.

Risk: Full transcripts and optional translations may consume paid API credits.

Mitigation: Set --max-credits before processing a video and check reported credit usage.

Risk: The inspected client may fail to show results because its response-handling functions are undefined.

Mitigation: Test a free or low-cost request before relying on the client.

Risk: Model-generated transcripts can misstate names or numbers, and long translations may be incomplete.

Mitigation: Verify important details against the video and disclose any reported coverage limits.

## Reference(s):

- [LinkDigest documentation](https://linkdigest.dev/zh/docs)
- [LinkDigest API keys](https://linkdigest.dev/app/keys)
- [ClawHub skill listing](https://clawhub.ai/jackchew7143/skills/linkdigest-youtube-summary)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown by default; JSON on request]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include timestamps, on-screen text, translation, coverage, and credit usage.]

## Skill Version(s):

1.2.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
