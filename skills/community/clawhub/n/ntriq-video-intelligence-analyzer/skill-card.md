## Description: <br>
AI-powered multimodal analysis for user-provided image and video URLs, returning structured tags, scene descriptions, mood analysis, virality scores, and content classifications in up to 15 languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content, marketing, and media teams use this skill to analyze user-provided images and videos for tagging, scene summaries, mood, content safety, and social performance signals before publishing or organizing assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media URLs submitted for analysis are sent to an external service. <br>
Mitigation: Avoid submitting private or sensitive media URLs unless the user is comfortable sharing them with the provider. <br>
Risk: The skill uses x402 USDC micropayments and may incur a per-call charge. <br>
Mitigation: Confirm the user intends to make a paid request before invoking the paid endpoint. <br>


## Reference(s): <br>
- [Ntriq x402 homepage](https://x402.ntriq.co.kr) <br>
- [Ntriq service catalog](https://x402.ntriq.co.kr/services) <br>
- [ClawHub skill page](https://clawhub.ai/ntriq-gh/ntriq-video-intelligence-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Structured JSON or concise natural-language analysis describing tags, scenes, mood, virality, and content safety.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports optional analysis categories, output language selection, and audience context for virality scoring.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
