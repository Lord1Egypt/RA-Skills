## Description: <br>
Cloud-powered image compression and resize for JPG, PNG, WebP, and HEIC images using Pixmind's API and Tencent Cloud COS imageMogr2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuyunzhishang](https://clawhub.ai/user/fuyunzhishang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and content operators use this skill to compress, resize, convert, and batch-process images for websites, social sharing, email, thumbnails, and archival workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads user-selected images to Pixmind/Tencent Cloud for processing. <br>
Mitigation: Use it only for images acceptable to send to that provider and avoid confidential, regulated, or sensitive personal material unless provider terms and policy allow it. <br>
Risk: The skill requires a Pixmind API key. <br>
Mitigation: Use a dedicated, revocable key through PIXMIND_API_KEY and rotate it if exposed. <br>
Risk: Recursive batch processing can upload more files than intended. <br>
Mitigation: Review folder scope before running batch commands with recursive processing. <br>


## Reference(s): <br>
- [Pixmind](https://www.pixmind.io) <br>
- [Pixmind API Keys](https://www.pixmind.io/api-keys) <br>
- [Tencent Cloud COS imageMogr2](https://cloud.tencent.com/document/product/460/36540) <br>
- [ClawHub Skill Page](https://clawhub.ai/fuyunzhishang/pixmind-image-compress) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create compressed image files in a local output directory when the generated command is executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
