## Description: <br>
Turns topics, long-form text, reports, notes, or explanatory material into Chinese visual image-generation prompts, then optionally renders images with DashScope Qwen image models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yeyitech](https://clawhub.ai/user/yeyitech) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to convert topics, articles, reports, meeting notes, or document excerpts into Chinese infographic prompts and optionally rendered image files. It is suited to information graphics, story-comic long images, document-to-image workflows, and style-controlled visual summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text, reports, meeting notes, and optional style files may be sent to DashScope under the user's API key. <br>
Mitigation: Avoid confidential or regulated documents unless approved, and use dry-run or prompt-output mode to review the generated prompt before image rendering. <br>
Risk: Generated prompts or images may simplify, omit, or misrepresent source material. <br>
Mitigation: Review the inferred prompt and final image for factual accuracy, readability, and appropriate use before publication. <br>
Risk: The workflow requires a DashScope API key and external API availability. <br>
Mitigation: Configure DASHSCOPE_API_KEY only in trusted environments and expect generation to fail when the key, network, or upstream service is unavailable. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/yeyitech/infographic-image) <br>
- [DashScope API endpoint](https://dashscope.aliyuncs.com) <br>
- [Infographic meta-prompt](references/meta-prompt.md) <br>
- [Comic story meta-prompt](references/meta-prompts-comic-story.md) <br>
- [Frosted whiteboard meta-prompt](references/meta-prompts-frosted-whiteboard.md) <br>
- [Spatial gallery meta-prompt](references/meta-prompts-spatial-gallery.md) <br>
- [Style presets](references/styles/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands, configuration] <br>
**Output Format:** [Console text, optional JSON prompt file, and optional downloaded image file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses DashScope text and image API calls; dry-run mode emits prompts without rendering an image.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
