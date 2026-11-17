## Description:

Generates short videos from text prompts using the Jimeng model through the Wanjiedata/OpenClaw workflow, with asynchronous task handling and result URL persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangshenghzj888-stack](https://clawhub.ai/user/liangshenghzj888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to submit text-to-video prompts to Jimeng and retrieve the generated video URL. It is suited for agent workflows that need asynchronous video generation from prompt text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send a locally configured OpenClaw API credential and user prompts to an external Wanjiedata service.

Mitigation: Use a dedicated Wanjiedata/OpenClaw credential with limited quota and avoid submitting sensitive or confidential prompts.

Risk: Prompts and generated video URLs may be written to local log and result files.

Mitigation: Run the skill in a workspace where local logs are acceptable, and remove generated logs or result files when they are no longer needed.

Risk: The skill may automatically install Python dependencies and start a detached background worker.

Mitigation: Review before installing and run only in environments where automatic pip installs and background worker processes are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liangshenghzj888-stack/skills/jimeng-openclaw-video-v1)
- [Wanjie Ark](https://www.wjark.com)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Wanjie Ark OpenClaw tutorial](https://docs.wjark.com/maas/scenarios/Development/openclaw.html)
- [Wanjie Ark model selection](https://www.wjark.com/center/model)

## Skill Output:

**Output Type(s):** [Text, Files, API Calls]

**Output Format:** [Plain text status messages and a result file containing SUCCESS|<video URL>]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submits one prompt at a time, polls asynchronously, and writes local logs and generated video URLs.]

## Skill Version(s):

1.0.0 (source: manifest.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
