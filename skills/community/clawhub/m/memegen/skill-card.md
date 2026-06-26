## Description: <br>
Generate meme images through memegen.link URLs, with guidance for selecting templates, formatting captions, and optionally using custom or trending image sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[artemiopadilla](https://clawhub.ai/user/artemiopadilla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to help an AI agent choose meme templates, create caption text, construct meme image URLs, and download or deliver generated meme images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meme captions, search terms, and custom background image URLs may be sent to third-party services. <br>
Mitigation: Avoid sensitive text in generated meme URLs and use third-party integrations only when the user accepts that data sharing. <br>
Risk: Optional Reddit and Giphy workflows use third-party credentials and can download files locally. <br>
Mitigation: Skip or isolate those optional scripts unless needed, review scripts before execution, and avoid using a personal Reddit password. <br>
Risk: Automatic humor or cultural targeting can produce inappropriate or unwanted content. <br>
Mitigation: Prefer explicit humor, audience, and regional settings, and review generated captions before sharing. <br>


## Reference(s): <br>
- [Memegen Skill README](README.md) <br>
- [memegen.link API Reference](references/api.md) <br>
- [Template Index](references/template-index.md) <br>
- [Complete Template Guide](references/templates-complete.md) <br>
- [Trending Template Sources](references/templates-trending.md) <br>
- [Humor Profiles](humor-profiles.md) <br>
- [memegen.link API](https://api.memegen.link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with meme URLs, shell commands, and optional code snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce URLs or local image download commands; optional scripts can write meme image files under temporary paths.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
