## Description: <br>
Enhance images and videos using HitPaw's AI enhancement API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hitpawdev](https://clawhub.ai/user/hitpawdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to call HitPaw's enhancement API for image upscaling, face recovery, denoising, video restoration, and result download workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends provided image or video URLs and the HitPaw API key to HitPaw's API for third-party processing. <br>
Mitigation: Use only media that is appropriate for third-party processing, review HitPaw's terms for sensitive or regulated content, and protect the HITPAW_API_KEY as a sensitive credential. <br>
Risk: API usage may consume HitPaw credits or coins. <br>
Mitigation: Check account balance and expected processing cost before submitting large images, long videos, or batch jobs. <br>
Risk: The video CLI may fail because the release evidence notes packaging or conflict-marker issues. <br>
Mitigation: Validate the installed video command on a small, non-sensitive test file before relying on it for production video workflows. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/hitpawdev/hitpaw-image-enhancer) <br>
- [HitPaw Image API Introduction](https://developer.hitpaw.com/image/Introduction) <br>
- [HitPaw Image Models](https://developer.hitpaw.com/image/available-models) <br>
- [HitPaw Image API Reference](https://developer.hitpaw.com/image/API-reference) <br>
- [HitPaw Video API Introduction](https://developer.hitpaw.com/video/Introduction) <br>
- [HitPaw Video Models](https://developer.hitpaw.com/video/available-models) <br>
- [HitPaw Video API Reference](https://developer.hitpaw.com/video/API-reference) <br>
- [HitPaw OSS Pre-sign PUT API](https://developer.hitpaw.com/common/oss-presign-put-api) <br>
- [HitPaw Playground](https://playground.hitpaw.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, files] <br>
**Output Format:** [Markdown guidance with CLI commands and downloaded media files from API jobs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HITPAW_API_KEY and publicly accessible input media URLs; reports API job status and coin consumption.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
