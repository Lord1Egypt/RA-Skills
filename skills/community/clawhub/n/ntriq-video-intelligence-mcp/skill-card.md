## Description:

Video analysis: object detection, scene classification, activity recognition, and summarization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to send video URLs to a remote video-intelligence service and receive object detections, scene labels, activity recognition, and narrative summaries. Typical uses include incident review, content moderation triage, and highlight identification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video URLs are sent to an external paid service.

Mitigation: Use only approved video sources and confirm the provider's data handling terms before submitting confidential, regulated, surveillance, or personal footage.

Risk: Each analysis call may incur the stated per-call fee.

Mitigation: Confirm payment authorization and expected usage volume before deploying the skill in automated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ntriq-gh/skills/ntriq-video-intelligence-mcp)
- [Ntriq x402 service homepage](https://x402.ntriq.co.kr)
- [Video Intelligence MCP endpoint](https://x402.ntriq.co.kr/video-intel-mcp)
- [Ntriq service catalog](https://x402.ntriq.co.kr/services)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Text]

**Output Format:** [Structured JSON with timestamped detections, scene labels, activity lists, and summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require payment to the external x402 service; output depends on the submitted video URL and selected analysis tasks.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
