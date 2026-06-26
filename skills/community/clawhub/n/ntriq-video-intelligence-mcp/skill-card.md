## Description: <br>
Video analysis: object detection, scene classification, activity recognition, and summarization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send a video URL to ntriq's external service for object detection, scene classification, activity recognition, and summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends referenced video content to an external ntriq service. <br>
Mitigation: Use only videos you are authorized to share, and avoid confidential, regulated, internal-only, or surveillance footage unless retention and logging practices are acceptable. <br>
Risk: Calls use a paid x402 micropayment endpoint. <br>
Mitigation: Confirm payment authorization, network, and expected per-call cost before invoking the service. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/ntriq-gh/ntriq-video-intelligence-mcp) <br>
- [ntriq x402 homepage](https://x402.ntriq.co.kr) <br>
- [ntriq service catalog](https://x402.ntriq.co.kr/services) <br>
- [Video intelligence endpoint](https://x402.ntriq.co.kr/video-intel-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON analysis results with labels, timestamps, confidence scores, activities, and summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Inputs include a video URL, optional task selection, confidence threshold, and frame sample rate.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
