## Description:

AI-powered multimodal analysis for images and videos that returns structured tags, scene descriptions, mood analysis, virality scores, and content classification across 15 languages from user-provided media URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze image or video URLs for content tagging, scene summaries, mood signals, virality scoring, and content-safety classification before publishing or organizing media assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted media URLs are processed by ntriq's external service.

Mitigation: Avoid submitting private, confidential, or access-controlled media URLs unless the user has approved sharing those references with the service.

Risk: Each API call may involve a disclosed USDC micropayment.

Mitigation: Confirm payment expectations and call volume before invoking the endpoint.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ntriq-gh/skills/ntriq-video-intelligence-analyzer)
- [Ntriq Homepage](https://x402.ntriq.co.kr)
- [Ntriq Service Catalog](https://x402.ntriq.co.kr/services)
- [Video Intelligence API Endpoint](https://x402.ntriq.co.kr/video-intel)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell/API call snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include tags, scenes, mood, virality score, virality factors, content safety, and language; calls use user-provided media URLs.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
