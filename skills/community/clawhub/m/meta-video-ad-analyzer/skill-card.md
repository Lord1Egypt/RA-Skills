## Description: <br>
Extract and analyze content from video ads using Gemini Vision AI, including frame extraction, OCR text detection, audio transcription, scene analysis, and thumbnails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fortytwode](https://clawhub.ai/user/fortytwode) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and marketing teams use this skill to inspect video or image ad creatives, extract visible and spoken content, and generate scene-by-scene analysis for review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media content and extracted audio, text, frames, or thumbnails may include sensitive or proprietary ad material. <br>
Mitigation: Analyze only media you are allowed to send to Google cloud services and use a dedicated least-privilege Google service account. <br>
Risk: Generated thumbnails may expose reviewed creative assets if served from shared or public storage. <br>
Mitigation: Keep generated thumbnails out of public access, or require authenticated serving and unique filenames in shared deployments. <br>
Risk: OCR, transcription, and vision summaries can be incomplete or incorrect. <br>
Mitigation: Treat extracted timelines and summaries as review aids and verify important claims against the source media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fortytwode/meta-video-ad-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Python ExtractedVideoContent object with transcript text, text timeline, scene timeline, thumbnail URL, and setup guidance in Markdown examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Video and image analysis can depend on local ffmpeg or ffprobe, EasyOCR, Google Cloud Speech, Vertex AI, and the configured Gemini model.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
