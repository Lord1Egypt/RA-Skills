## Description: <br>
MiVisionForgeSVOR helps agents run a CLI workflow for stable video object removal using SVOR-backed segmentation and erasure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangfei1204](https://clawhub.ai/user/wangfei1204) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video workflow operators use this skill to segment objects in short videos, review target object IDs, and run object removal through the disclosed Xiaomi Tools SVOR service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected videos and derived masks are sent to the disclosed Xiaomi Tools SVOR endpoint for processing. <br>
Mitigation: Use non-sensitive test videos first and avoid private, identifiable, regulated, or confidential content unless the service's data-handling terms are acceptable. <br>
Risk: SVOR_API_KEY authenticates requests to the remote service. <br>
Mitigation: Protect SVOR_API_KEY like a password and avoid exposing it in shared environments, logs, or version control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangfei1204/mi-visionforge-svor) <br>
- [Xiaomi SVOR reference repository](https://github.com/xiaomi-research/svor) <br>
- [Xiaomi Tools SVOR endpoint](https://mipixgen-pre.ai.mioffice.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline CLI commands and generated video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, ffmpeg, and SVOR_API_KEY; uploads selected videos and derived masks to the disclosed remote SVOR service.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
