## Description:

腾讯混元生3D API (OpenAI兼容接口) - 基于混元大模型的3D模型生成.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wszhhx](https://clawhub.ai/user/wszhhx)

### License/Terms of Use:


## Use Case:

Developers and technical users use this skill to configure Tencent Hunyuan 3D access and run text-to-3D or image-to-3D generation jobs that save local model artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script requires a Tencent Hunyuan 3D API key and the artifact suggests shell startup file persistence as one configuration option.

Mitigation: Use temporary environment variables or a secret manager, avoid committing or persisting keys unnecessarily, and rotate the key if it may have been exposed.

Risk: Remote API response values may influence local output paths and downloads.

Mitigation: Run the script with an output directory you control, validate returned JobId path components before broad use, and constrain downloads to trusted HTTPS hosts with expected file size and type limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wszhhx/skills/hunyuan-3d)
- [Tencent Hunyuan 3D OpenAI-compatible API documentation](https://cloud.tencent.com/document/product/1804/126189)
- [Tencent Hunyuan 3D submit task API documentation](https://cloud.tencent.com/document/product/1804/123447)
- [Tencent Hunyuan 3D console](https://console.cloud.tencent.com/ai3d)
- [Tencent Hunyuan API key management](https://console.cloud.tencent.com/hunyuan/start)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands and Python script usage examples; generated runs create local JSON metadata and 3D model files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and HUNYUAN_3D_API_KEY; generated model outputs are written under the selected local output directory.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
