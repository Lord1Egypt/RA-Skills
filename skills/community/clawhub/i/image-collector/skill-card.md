## Description: <br>
AI technology daily image collection tool that gathers news images from official sources and supports watermark detection, quality checks, and relevance validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lunadelo](https://clawhub.ai/user/lunadelo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, editors, and developers use this skill to collect and prepare relevant images for AI technology news articles from preferred official or authoritative sources. It helps screen downloaded images for basic watermark, quality, and filename-keyword relevance signals before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound web requests and saves downloaded image files locally. <br>
Mitigation: Use it only in environments where outbound requests and local image storage are acceptable, and restrict allowed domains for controlled deployments. <br>
Risk: Watermark, copyright, and relevance checks are basic signals rather than strong guarantees. <br>
Mitigation: Manually review each selected image before publication and confirm rights, source, and relevance. <br>
Risk: Dependency behavior may change over time. <br>
Mitigation: Pin Pillow and requests versions before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lunadelo/image-collector) <br>
- [README.md](README.md) <br>
- [Skill definition](skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Console status text, command examples, and local image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloaded images are saved locally and may be optimized or rejected based on basic validation checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
