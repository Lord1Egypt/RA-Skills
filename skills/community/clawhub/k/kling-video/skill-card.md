## Description: <br>
Generate, animate, and edit AI videos using Kuaishou's Kling 3.0 and Kling Video O3 through the Atlas Cloud API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xixihhhh](https://clawhub.ai/user/xixihhhh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create short AI video clips, animate images, generate reference-based videos, and edit existing videos with Kling models through Atlas Cloud. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video generation uses a paid Atlas Cloud API and may upload prompts, image URLs, video URLs, or local media. <br>
Mitigation: Use a dedicated API key and review the selected model, duration, input media, and expected cost before running commands. <br>
Risk: Private or regulated media may be sent to Atlas Cloud for generation, editing, or upload workflows. <br>
Mitigation: Avoid uploading sensitive media unless Atlas Cloud's data handling is acceptable for the user's organization and use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xixihhhh/kling-video) <br>
- [Atlas Cloud](https://www.atlascloud.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands and Python script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ATLASCLOUD_API_KEY and may download generated MP4 files to the requested output directory.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
