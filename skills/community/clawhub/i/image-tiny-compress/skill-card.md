## Description: <br>
Compress PNG, JPEG, and WebP images using TinyPNG/Tinify web endpoints without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aga-j](https://clawhub.ai/user/aga-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and content teams use this skill to reduce image file sizes for PNG, JPEG, and WebP assets in single-file, batch, or directory workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images are uploaded to TinyPNG/Tinify servers for compression, which may expose private or sensitive image content to an external service. <br>
Mitigation: Use the skill only with images approved for external processing, and avoid personal, confidential, or regulated content. <br>
Risk: Overwrite mode can replace original image files. <br>
Mitigation: Keep backups or write compressed images to a separate output directory unless replacement is explicitly intended. <br>
Risk: The skill simulates browser requests to TinyPNG/Tinify web endpoints rather than using the official API, so endpoint behavior, rate limits, or availability may change. <br>
Mitigation: Use moderate request volumes, review failures before retrying, and consider the official TinyPNG API for heavy or automated production workloads. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aga-j/image-tiny-compress) <br>
- [TinyPNG](https://tinypng.com) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, json, guidance] <br>
**Output Format:** [Compressed image files with JSON compression statistics and concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports PNG, JPEG, and WebP files up to 5 MB each, with up to 20 images per batch.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
