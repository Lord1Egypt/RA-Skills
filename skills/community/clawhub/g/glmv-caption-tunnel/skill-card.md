## Description:

Generates captions and descriptions for images, videos, and documents using Zhipu GLM-V multimodal models, with support for URLs, local paths, image base64, and optional structured JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tridefender](https://clawhub.ai/user/tridefender)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to caption, summarize, compare, or interpret images, videos, and documents through the Zhipu GLM-V API. It can return plain captions or structured JSON when response_format and a system prompt are provided.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local video and document paths may be exposed through a public quick tunnel, and security evidence reports weak scoping and misleading safety assurances.

Mitigation: Avoid confidential files, directories, source trees, credentials, or regulated data; prefer remote URLs already intended for sharing, validate regular files only, bind to localhost, add per-file random tokens, verify dependencies, and require explicit consent before creating a public tunnel.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tridefender/skills/glmv-caption-tunnel)
- [GLM-V Caption Homepage](https://github.com/zai-org/GLM-V/tree/main/skills/glmv-caption)
- [Zhipu Chat Completions API Docs](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8)
- [Zhipu API Keys](https://bigmodel.cn/usercenter/proj-mgmt/apikeys)
- [Cloudflare cloudflared Downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)
- [cloudflared](https://github.com/cloudflare/cloudflared)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON response containing success, caption, usage, warning, or error fields; streaming mode can print caption text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save result JSON to a file; optional JSON-mode output is available through response_format and a system prompt.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
