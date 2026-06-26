## Description: <br>
Image-to-video generation on RunComfy that turns still images into short video clips via the RunComfy Model API and routes general, lip-sync, or multi-modal requests to the appropriate endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn a still image plus a motion prompt into a short RunComfy-hosted video, including general animation, lip-sync, and multi-modal reference workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image, video, audio, or prompt content may be sent to RunComfy for hosted generation. <br>
Mitigation: Confirm the user wants RunComfy image-to-video generation and avoid private media, voice clips, videos, or confidential prompts unless RunComfy's data handling is acceptable. <br>
Risk: Ambiguous media requests could route user-provided content to a third-party service. <br>
Mitigation: Clarify user intent before running the skill and only submit media that is appropriate for third-party processing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kalvinrv/image-to-video-runcomfy) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy CLI introduction](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=image-to-video-runcomfy) <br>
- [RunComfy image-to-video models](https://www.runcomfy.com/models?utm_source=clawhub&utm_medium=skill&utm_campaign=image-to-video-runcomfy) <br>
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=image-to-video-runcomfy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown with inline bash commands and JSON request bodies; RunComfy downloads generated video files to the requested output directory.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the runcomfy CLI and RunComfy authentication via RUNCOMFY_TOKEN or local RunComfy config.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
