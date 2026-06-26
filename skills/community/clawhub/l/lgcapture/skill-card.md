## Description: <br>
Automatically fetches Douyin videos from short, standard, or share links by extracting a video ID and downloading through a simulated iPhone browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ly5201314gjx](https://clawhub.ai/user/ly5201314gjx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use lgCapture to download Douyin videos from supported link formats into local MP4 files when they have legitimate access and permission to do so. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled helper script can overwrite a custom output path if an agent is instructed to use one. <br>
Mitigation: Use the documented douyin.py path by default, and only pass a custom output path after choosing a safe, intended location. <br>
Risk: The skill runs a browser and downloads remote content to disk. <br>
Mitigation: Run it in a contained working directory and review links before execution. <br>


## Reference(s): <br>
- [lgCapture on ClawHub](https://clawhub.ai/ly5201314gjx/lgcapture) <br>
- [ly5201314gjx ClawHub profile](https://clawhub.ai/user/ly5201314gjx) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Plain text CLI output with a downloaded MP4 file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs Playwright with Chromium, makes network requests to Douyin, and writes downloaded video content to disk.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
