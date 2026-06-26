## Description: <br>
Uses GLM-4.6V to analyze images, videos, and documents for multimodal content understanding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TriDefender](https://clawhub.ai/user/TriDefender) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to ask GLM-4.6V for OCR, scene and object analysis, video summarization, key frame analysis, and document or table understanding from a single supplied modality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-supplied input and prompts may be interpolated into a shell-string tool handler. <br>
Mitigation: Use structured argument execution or robust escaping before deployment, and review commands before execution. <br>
Risk: Local files, URLs, and prompts may be uploaded to a third-party GLM/BigModel API using ZHIPU_API_KEY. <br>
Mitigation: Avoid confidential or regulated content unless approved, and add explicit user consent plus upload and retention disclosure for local files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/TriDefender/multimodal) <br>
- [BigModel chat completions API endpoint](https://open.bigmodel.cn/api/paas/v4/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown analysis, with optional streaming CLI output and JSON fallback for raw API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZHIPU_API_KEY; requests use glm-4.6v with a 4096 token response cap and may send files, URLs, and prompts to the BigModel API.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
