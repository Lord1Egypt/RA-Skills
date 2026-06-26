## Description: <br>
Takes a URL, HTML file path, or raw HTML code and generates a printable image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upwell](https://clawhub.ai/user/upwell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content workflows can use this skill to render a URL, local HTML file, or raw HTML snippet into an image for previews, documentation, review, or printable output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendering user-provided URLs, local files, or HTML can expose external content or local file contents during capture. <br>
Mitigation: Use trusted sources, review the requested input path or URL before execution, and inspect the generated image before relying on it. <br>
Risk: The security evidence reports a clean verdict but still advises review before using workflows that can make real local or authorized remote changes. <br>
Mitigation: Run the skill in an appropriate workspace and review outputs before sharing, publishing, or using them in downstream workflows. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON] <br>
**Output Format:** [JSON metadata with an image file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates PNG, JPEG, or WebP output using the requested viewport width and optional full-page capture.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
