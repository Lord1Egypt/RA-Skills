## Description: <br>
Generate captions, descriptions, summaries, and interpretations for images, videos, and documents using Zhipu GLM-V multimodal models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaredforreal](https://clawhub.ai/user/jaredforreal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to caption, summarize, and interpret user-supplied images, videos, and documents through the Zhipu GLM-V API. It is suited for media understanding workflows that need raw model output returned to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted media, media URLs, prompts, and selected local images are sent to Zhipu for processing under the configured API key. <br>
Mitigation: Avoid confidential or regulated material unless Zhipu privacy and retention terms are acceptable for the intended use. <br>
Risk: The skill requires a sensitive ZHIPU_API_KEY credential and may consume quota or incur billing. <br>
Mitigation: Use a dedicated revocable API key where possible, monitor quota or billing, and rotate or revoke the key if exposure is suspected. <br>
Risk: API constraints limit supported formats, sizes, and input mixing, so unsupported requests can fail. <br>
Mitigation: Check inputs against documented image, video, and file limits before running the captioning command. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jaredforreal/glmv-caption) <br>
- [GLM-V Caption homepage](https://github.com/zai-org/GLM-V/tree/main/skills/glmv-caption) <br>
- [Zhipu Chat Completions API documentation](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8) <br>
- [Zhipu API key management](https://bigmodel.cn/usercenter/proj-mgmt/apikeys) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Raw caption text or JSON output from the captioning script, with setup and command examples in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZHIPU_API_KEY; supports image, video, and document inputs with API-specific format, size, and mixing limits.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
