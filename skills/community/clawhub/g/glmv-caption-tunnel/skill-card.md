## Description: <br>
Generate captions, summaries, and structured descriptions for images, videos, and documents using Zhipu GLM-V multimodal models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tridefender](https://clawhub.ai/user/tridefender) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to caption, summarize, compare, or interpret media and document inputs, including local files that need temporary URL access for the GLM-V API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local videos and documents can be automatically exposed through a temporary public Cloudflare URL without a strong per-use consent gate. <br>
Mitigation: Use only files approved for this exposure path, avoid confidential or regulated content, and add explicit per-file consent before processing sensitive local files. <br>
Risk: Selected media and prompts are sent to Zhipu/BigModel for multimodal processing. <br>
Mitigation: Submit only content approved for third-party API processing and keep ZHIPU_API_KEY scoped and stored outside committed files. <br>


## Reference(s): <br>
- [GLM-V Caption Source Homepage](https://github.com/zai-org/GLM-V/tree/main/skills/glmv-caption) <br>
- [BigModel Chat Completions API Docs](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8) <br>
- [Cloudflare cloudflared Downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) <br>
- [cloudflared GitHub Repository](https://github.com/cloudflare/cloudflared) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [CLI output as JSON or plain caption text, with optional saved JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZHIPU_API_KEY; local videos and documents require cloudflared and may be temporarily exposed through a public tunnel.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
