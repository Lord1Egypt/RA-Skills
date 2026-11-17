## Description:

iFlytek Image Understanding analyzes images and answers questions about their content using the iFlytek Spark Vision WebSocket API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingzhe2020](https://clawhub.ai/user/qingzhe2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to describe JPG, JPEG, and PNG images or ask targeted questions about image content through iFlytek Spark Vision. It supports general description, OCR-style questions, object identification, chart interpretation, model selection, token limits, and optional raw API frame output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a project-local Claude settings file that grants unrelated file-read and packaging command permissions.

Mitigation: Review or remove artifact/.claude/settings.local.json before installing, especially in Claude environments that honor local permission files.

Risk: Images and prompts are sent to iFlytek's remote service for analysis.

Mitigation: Avoid submitting sensitive images or prompts unless that third-party transfer is acceptable for the intended use case.

## Reference(s):

- [iFlytek Image Understanding Service Documentation](https://console.xfyun.cn/services/image)
- [iFlytek Console](https://console.xfyun.cn)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text image answers, optional raw WebSocket JSON frames, and Markdown usage examples with shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IFLY_APP_ID, IFLY_API_KEY, and IFLY_API_SECRET environment variables; accepts .jpg, .jpeg, and .png images up to 4MB with max_tokens from 1 to 8192.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
