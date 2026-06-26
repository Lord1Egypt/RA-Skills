## Description: <br>
Compresses PNG, JPEG, and WebP images with TinyPNG/Tinify web endpoints, supporting single files, batches, and directories with retry and rate-limit handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aga-j](https://clawhub.ai/user/aga-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to reduce image file sizes for PNG, JPEG, and WebP assets while preserving near-original visual quality. It is suited to one-off compression, batch jobs, and directory-based optimization when the images are acceptable to upload to TinyPNG/Tinify. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images are uploaded to TinyPNG/Tinify for processing. <br>
Mitigation: Do not use the skill with sensitive, personal, confidential, or proprietary images unless that upload is explicitly approved. <br>
Risk: The skill uses unofficial web endpoints with spoofed browser and IP headers, which may break or violate service expectations for high-volume use. <br>
Mitigation: For production or high-volume workflows, use the provider's official API and terms instead of the web endpoint. <br>
Risk: Overwrite mode can replace original files irreversibly. <br>
Mitigation: Keep backups and use explicit output directories unless overwrite behavior has been reviewed and requested. <br>
Risk: Recursive directory compression can upload more files than intended. <br>
Mitigation: Review the directory scope before using recursive mode and prefer narrow input paths. <br>


## Reference(s): <br>
- [ImageCompress ClawHub release](https://clawhub.ai/aga-j/imgae-compress) <br>
- [TinyPNG](https://tinypng.com) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Text, JSON] <br>
**Output Format:** [Compressed image files with terminal status output and optional JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes PNG, JPEG, and WebP files up to 5 MB each, with up to 20 files per batch and optional recursive directory traversal.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
