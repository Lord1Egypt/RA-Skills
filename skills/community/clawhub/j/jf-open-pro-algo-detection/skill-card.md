## Description:

Guides agents through selecting JFTech Open Platform AI detection algorithms, calling approved image-analysis workflows for local images, image URLs, or camera snapshots, and producing structured detection reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to choose from supported JFTech image-detection algorithms for safety, security, retail, vehicle, environment, and camera-quality workflows. It helps configure credentials, validate access, run algorithm calls, and summarize detections for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill submits images, device serial numbers, detection outputs, and API-authenticated requests to JFTech services.

Mitigation: Treat images, serial numbers, callback results, and credentials as sensitive; use HTTPS endpoints and avoid sharing generated result files or source images without review.

Risk: Credentials are stored in a local config.json file generated at runtime.

Mitigation: Keep config.json out of repositories, backups, exported skill packages, and support bundles; rotate credentials if the skill directory is shared.

Risk: The camera-snapshot path can install a separate remote capture skill.

Mitigation: Install the dependency only from a trusted JFTech source and pin or verify the downloaded version before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jftech/skills/jf-open-pro-algo-detection)
- [Algorithm reference](reference.md)
- [Algorithm metadata](algorithms.json)
- [JFTech Open Platform API endpoint](https://api.jftechws.com)
- [JFTech capture skill on ClawHub](https://clawhub.ai/jftech/jf-open-pro-capture)
- [JFTech capture skill source](https://gitee.com/jftek/jftech-open-skills/tree/main/jf-open-pro-capture)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON detection summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create result JSON files and local evidence images when a local source image and Pillow are available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
