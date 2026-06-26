## Description: <br>
Supports text-to-video and image-to-video generation through giggle.pro, including start/end frame inputs, model selection, aspect ratio, duration, and resolution options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patches429](https://clawhub.ai/user/patches429) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit text-to-video or image-to-video jobs to giggle.pro, then query task status and receive generated video links. It is suited for creating short AI videos from prompts, reference images, and selected generation parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference image URLs, asset IDs, base64 image data, generated videos, and API usage are sent to giggle.pro. <br>
Mitigation: Avoid submitting private or sensitive media, use a revocable API key where possible, and install only if the user trusts giggle.pro with these inputs and outputs. <br>
Risk: Task IDs and generated video links may expose previous generation jobs or signed media URLs. <br>
Mitigation: Clear saved task IDs when old jobs should not be remembered, and avoid sharing signed video URLs beyond the intended audience. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/patches429/giggle-generation-video) <br>
- [Giggle API Service](https://giggle.pro/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON task responses, status messages, and signed video links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, requests, and GIGGLE_API_KEY; submitted generation jobs return task IDs for later status queries.] <br>

## Skill Version(s): <br>
0.0.10 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
