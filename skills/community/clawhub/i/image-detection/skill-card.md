## Description: <br>
Analyzes images to detect AI generation, extract metadata, identify artifacts, and perform content moderation using local and cloud-based tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raghulpasupathi](https://clawhub.ai/user/raghulpasupathi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content review teams use this skill to choose image detection workflows for AI-generated image checks, metadata review, artifact identification, reverse image search, and moderation. It supports local privacy-focused analysis as well as optional cloud API analysis when that fits the use case. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private, regulated, or sensitive images may be exposed through optional cloud analysis, reverse image search, caching, or retained metadata. <br>
Mitigation: Use the privacy-focused stack for private or regulated images and review each referenced package or service for what content, metadata, hashes, and results are transmitted or stored before enabling external APIs or caching. <br>
Risk: Detection results may be inaccurate or misleading when used as the sole basis for moderation or authenticity decisions. <br>
Mitigation: Treat outputs as decision support and review results before deployment or enforcement. <br>


## Reference(s): <br>
- [Image Detection on ClawHub](https://clawhub.ai/raghulpasupathi/image-detection) <br>
- [Publisher profile](https://clawhub.ai/user/raghulpasupathi) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with npm commands and JSON or JavaScript configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend local-only, high-accuracy, or cloud API stacks depending on privacy and speed requirements.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
