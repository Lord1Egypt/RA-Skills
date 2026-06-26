## Description: <br>
Create and monitor NotebookLM Studio content, including Audio Overview, Video Overview, Infographics, and Slides, via notebooklm-mcp-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skywalker-lili](https://clawhub.ai/user/skywalker-lili) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create NotebookLM Studio outputs from selected notebooks, optionally triggered by upstream skills with prefilled parameters. It supports generating or downloading audio, video, infographic, and slide artifacts while monitoring completion in the background. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload local files to NotebookLM. <br>
Mitigation: Confirm the exact local file path, notebook name, content type, and output destination before upload. <br>
Risk: Triggered mode may start background work with less per-run user control. <br>
Mitigation: Use triggered execution only with trusted upstream skills and verify prefilled parameters before deployment. <br>
Risk: The skill can send completion notifications through the Discord/OpenClaw messaging path. <br>
Mitigation: Use it only in trusted messaging contexts and confirm the notification target before background runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skywalker-lili/jclaw-notebooklm-content-creation) <br>
- [Publisher profile](https://clawhub.ai/user/skywalker-lili) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON task metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create background polling task files and downloaded NotebookLM artifacts.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
