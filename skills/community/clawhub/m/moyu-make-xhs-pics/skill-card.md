## Description: <br>
Converts Markdown articles into Xiaohongshu-style cover, illustration, and decoration images using DashScope or MiniMax with selectable styles and layouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulforcoding](https://clawhub.ai/user/paulforcoding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and developers use this skill to turn a local Markdown article into a cover image, illustration, and supporting decoration images for Xiaohongshu-style posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Article-derived prompts may be sent to MiniMax or DashScope. <br>
Mitigation: Use only content approved for external processing, and avoid confidential drafts, personal data, or proprietary documents unless that processing is approved. <br>
Risk: Generated files and Python dependencies may need local hygiene review. <br>
Mitigation: Pin and audit dependencies where possible, and clean generated files from temporary locations after use. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/paulforcoding/make-xhs-pics) <br>
- [baoyu-skills prompt reference](https://github.com/JimLiu/baoyu-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Code] <br>
**Output Format:** [Generated image files with Python result objects and CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Markdown article and provider API keys; generated images are returned as local file paths.] <br>

## Skill Version(s): <br>
v1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
