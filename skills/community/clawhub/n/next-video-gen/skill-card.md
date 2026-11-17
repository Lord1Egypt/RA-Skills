## Description:

Next Video Gen enables AI coding agents to generate images and short videos from text, images, or source videos through Volcengine Ark Seedance models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vennduan](https://clawhub.ai/user/vennduan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill with AI coding agents to generate images and short videos, animate reference images, transform video inputs, and save generated media locally through Volcengine Ark APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled legacy shell script has a URL interpolation flaw when handling untrusted video or audio URLs.

Mitigation: Prefer the Node implementation and avoid running scripts/seedance-gen.sh with untrusted media URLs until the flaw is fixed.

Risk: The authenticated HTTP helper is not restricted to Volcengine Ark hosts.

Mitigation: Restrict authenticated requests to HTTPS Volcengine Ark endpoints before attaching DOUBAO_API_KEY.

Risk: Prompts and media URLs are sent to Volcengine, and generated files are saved locally by default.

Mitigation: Use a scoped API key, avoid sensitive prompts or media URLs, and review the configured local output directory.

## Reference(s):

- [Next Video Gen ClawHub listing](https://clawhub.ai/vennduan/skills/next-video-gen)
- [Next Video Gen repository homepage](https://github.com/vennduan/next-video-gen)
- [API parameter reference](references/api-params.md)
- [Volcengine Ark console](https://console.volcengine.com/ark)
- [Doubao Seedream text-to-image model](https://console.volcengine.com/ark/model_detail?Id=doubao-seedream-5-0-260128)
- [Doubao Seedance 1.5 Pro video model](https://console.volcengine.com/ark/model_detail?Id=doubao-seedance-1-5-pro-251215)
- [Doubao Seedance 2.0 video model](https://console.volcengine.com/ark/model_detail?Id=doubao-seedance-2-0-260128)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Structured status text with local file paths, media specifications, and temporary media URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DOUBAO_API_KEY; generated media is saved locally by default and online links are temporary.]

## Skill Version(s):

1.0.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
