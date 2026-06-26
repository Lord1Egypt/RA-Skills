## Description: <br>
Generates short videos from text prompts through the Jimeng model for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangshenghzj888-stack](https://clawhub.ai/user/liangshenghzj888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to submit text-to-video prompts to the Wanjie/Jimeng service, poll for completion, and retrieve a generated video URL. <br>

### Deployment Geography for Use: <br>
Global, subject to Wanjie/Jimeng service availability and applicable law. <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads an OpenClaw provider API key and uses it to call the Wanjie/Jimeng service. <br>
Mitigation: Use a dedicated provider key for this service, confirm which key the skill reads, and avoid sensitive prompts. <br>
Risk: Video generation may consume API quota or incur charges. <br>
Mitigation: Confirm Wanjie/Jimeng quota and billing settings before running the skill. <br>
Risk: Prompts, task status, and generated video links may be written to local log and result files. <br>
Mitigation: Avoid sensitive prompts and review or clear local log and result files when needed. <br>
Risk: The skill may install the requests package on first run if it is missing. <br>
Mitigation: Run it in a controlled Python environment and preinstall reviewed dependencies where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liangshenghzj888-stack/jimeng-openclaw-video-v1) <br>
- [Wanjie Ark](https://www.wjark.com) <br>
- [Wanjie MaaS OpenClaw tutorial](https://docs.wjark.com/maas/scenarios/Development/openclaw.html) <br>
- [Wanjie model selection](https://www.wjark.com/center/model) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, files] <br>
**Output Format:** [Plain text status plus a local result file containing SUCCESS|<video URL> when generation succeeds.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs asynchronously, writes local logs and result files, and returns temporary video URLs from the provider.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
