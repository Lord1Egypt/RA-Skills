## Description:

Generate videos from text prompts using Jimeng OpenClaw with asynchronous task handling and configurable model selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangshenghzj888-stack](https://clawhub.ai/user/liangshenghzj888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to submit text-to-video prompts to the Jimeng/Wanjie Ark API from an OpenClaw-style agent workflow, poll for completion, and retrieve a generated video URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads an API key from the user's OpenClaw configuration and sends prompts to an external video-generation service.

Mitigation: Use a dedicated Wanjiedata/Jimeng API key with limited scope or quota, avoid sensitive prompts, and review service terms before deployment.

Risk: Runtime dependency installation and background subprocess execution can make installation and execution harder to control.

Mitigation: Install dependencies through a reviewed, pinned environment and run the skill in an isolated workspace before allowing normal agent use.

Risk: The artifact includes generated log/result files and can open generated video URLs on the host system.

Mitigation: Remove shipped runtime files before release and disable or gate automatic URL opening in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liangshenghzj888-stack/skills/jimeng-openclaw-video-v1-1)
- [Wanjie Ark](https://www.wjark.com)
- [Wanjie Ark OpenClaw development guide](https://docs.wjark.com/maas/scenarios/Development/openclaw.html)
- [Wanjie Ark model center](https://www.wjark.com/center/model)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, code, shell commands, files, guidance]

**Output Format:** [Text status messages and a result file containing SUCCESS|<video URL>, with Markdown documentation and Python usage examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submits one prompt at a time, writes logs and results locally, and may open the generated video URL on the host system.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact manifest lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
