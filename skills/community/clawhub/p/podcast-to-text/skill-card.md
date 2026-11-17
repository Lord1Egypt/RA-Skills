## Description:

Turn public Xiaoyuzhou or Apple Podcasts episode links into timestamped transcripts, show notes, key points, and episode statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

Listeners and researchers can use this skill to turn a public episode link into a timestamped transcript and concise notes, find supported quotations, or ask a question about the episode. It requires a LinkDigest API key, and some options use additional credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default command may not enforce the promised audio-only processing or pricing.

Mitigation: Confirm processing and pricing behavior before use, and set a request or API-key credit cap; the script supports --max-credits.

Risk: The service says cached digests may be shared with other users.

Mitigation: Submit only public episode links.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jackchew7143/skills/podcast-to-text)
- [LinkDigest platform information](https://linkdigest.dev/platforms?ref=skill-podcast-to-text)
- [LinkDigest privacy policy](https://linkdigest.dev/privacy)
- [LinkDigest MCP](https://linkdigest.dev/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown or JSON with timestamped transcript, show notes, key points, and episode statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include episode Q&A or a translated transcript; these options consume additional credits.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
