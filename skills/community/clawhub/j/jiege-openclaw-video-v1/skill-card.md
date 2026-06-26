## Description: <br>
Jiege OpenClaw Video lets OpenClaw users trigger a background Veo video-generation job from a natural-language chat prompt and open the returned result link when the job completes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangshenghzj888-stack](https://clawhub.ai/user/liangshenghzj888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to submit short video prompts from chat, generate videos through a configured third-party model provider, and receive the result link in the browser. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the video prompt and a local OpenClaw API key to WanjieData. <br>
Mitigation: Use a dedicated limited-scope API key where possible and avoid sensitive prompt content. <br>
Risk: Completion may automatically open a browser page returned by the remote service. <br>
Mitigation: Run only in an environment where opening returned links is acceptable and inspect unexpected pages before interacting with them. <br>
Risk: A background Python worker and lock file can leave future generation requests blocked after interruption. <br>
Mitigation: Check the local log and remove stale lock files before retrying a blocked task. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liangshenghzj888-stack/jiege-openclaw-video-v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, files] <br>
**Output Format:** [Chat status text with background video generation and browser-opened result link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local log and lock files while a background worker processes the request.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
