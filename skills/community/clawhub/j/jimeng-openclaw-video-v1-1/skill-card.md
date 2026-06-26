## Description: <br>
Generates short videos from text prompts using the Wanjie/Jimeng service for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangshenghzj888-stack](https://clawhub.ai/user/liangshenghzj888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to submit text prompts to the Wanjie/Jimeng video generation API, poll asynchronous jobs, and retrieve generated video links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw API-key configuration and sends prompts to an external Wanjie/Jimeng endpoint. <br>
Mitigation: Use a scoped API key, review the configured provider before running, and avoid submitting sensitive prompts. <br>
Risk: The skill can install the requests package automatically and launch a detached Python worker. <br>
Mitigation: Review the code before installation, run it in a controlled environment, and pin or preinstall dependencies when reproducibility is required. <br>
Risk: Prompts, task status, and generated video links are written to plaintext local log and result files. <br>
Mitigation: Treat generated logs and result files as sensitive artifacts and delete or protect them according to local data-handling requirements. <br>
Risk: Returned video links may be opened automatically by the local system. <br>
Mitigation: Disable or modify automatic URL opening if manual review of generated links is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liangshenghzj888-stack/jimeng-openclaw-video-v1-1) <br>
- [Wanjie Ark](https://www.wjark.com) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Wanjie OpenClaw development guide](https://docs.wjark.com/maas/scenarios/Development/openclaw.html) <br>
- [Wanjie model selection](https://www.wjark.com/center/model) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Code, Files, API Calls] <br>
**Output Format:** [Markdown guidance, Python entry points, plaintext logs, and SUCCESS-prefixed video URL result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenClaw API key configuration, submits prompts to the Wanjie/Jimeng service, and writes local log/result files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
