## Description:

Reads individual public Xiaohongshu and Douyin posts through LinkDigest to provide summaries, image text, video transcripts, and optional translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents reading a public Xiaohongshu or Douyin post use this skill to understand its caption, image text, or video speech and request an English translation or summary. A limited keyless summary is available; full extraction requires a LinkDigest API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted links or copied share text are sent to LinkDigest, and cached text for a public link may be returned to other users.

Mitigation: Submit only public, non-sensitive links or share text and avoid private content.

Risk: The bundled script may fail when handling responses because some referenced output and error helpers are missing.

Mitigation: Test with a non-sensitive public link before relying on the skill and review results or errors manually.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jackchew7143/skills/linkdigest-xiaohongshu-douyin-reader)
- [LinkDigest documentation](https://linkdigest.dev/docs)
- [LinkDigest privacy](https://linkdigest.dev/privacy)
- [LinkDigest pricing](https://linkdigest.dev/pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown by default; structured JSON on request]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include captions, image text, timestamped transcripts, coverage details, and translations; keyless use returns a limited summary.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
