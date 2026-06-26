## Description: <br>
Fast local image search using macOS Spotlight or fd. Search images by name, date, location, or metadata. Use when users need to find images on their local machine quickly without manual browsing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaomenghuan](https://clawhub.ai/user/zhaomenghuan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to find local image files quickly by filename, date, location metadata, or image type without manual folder browsing. It is especially relevant for macOS workflows that can use Spotlight metadata, with fd and find as filename-search fallbacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches can reveal local image file paths and GPS-tagged photo metadata. <br>
Mitigation: Use narrow search directories where possible and review returned paths before sharing or further processing results. <br>
Risk: copy_results.sh can copy selected photos into a destination that may be shared or cloud-synced. <br>
Mitigation: Review the result list and destination folder before copying, and avoid copying sensitive photos unless intended. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhaomenghuan/local-image-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include local image paths and image metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
