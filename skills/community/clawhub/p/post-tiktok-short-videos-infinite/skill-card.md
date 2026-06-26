## Description: <br>
在抖音创作者平台协助上传短视频、填写标题简介、设置封面、合集、权限和 AI 声明，并将视频暂存为草稿。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[infiniteask](https://clawhub.ai/user/infiniteask) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and operators use this skill to prepare Douyin Creator Platform video drafts through an agent-assisted browser workflow. It uploads the selected video, fills metadata, sets cover and collection options, applies permissions, adds an AI-content declaration, and leaves the result for manual review before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is advertised as publishing Douyin videos, but the documented workflow saves the upload as a draft instead of completing public publishing. <br>
Mitigation: Treat the generated draft as a staging result and manually review the draft, title, tags, cover, permissions, collection, and AI declaration before publishing. <br>
Risk: The workflow automates browser actions and local file-dialog input for a user-selected video path. <br>
Mitigation: Provide only the intended video file path and run the workflow in the intended Douyin account session. <br>


## Reference(s): <br>
- [Douyin Creator upload page](https://creator.douyin.com/creator-micro/content/upload) <br>
- [ClawHub skill page](https://clawhub.ai/infiniteask/post-tiktok-short-videos-infinite) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with browser-operation steps and inline Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided video path, Douyin account context, title, description, tags, collection, cover choice, and final manual review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
