## Description: <br>
Convert GitHub repositories into RedNote (小红书) style technical articles, including project intros, reviews, tutorials, tool lists, release notes, and optional cover images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caoyachao](https://clawhub.ai/user/caoyachao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical content creators use this skill to turn GitHub repository data into Chinese RedNote-ready technical posts for project promotion, reviews, tutorials, curated lists, and release notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a GitHub token for API access. <br>
Mitigation: Use a fine-grained read-only token and avoid granting write or organization-wide permissions. <br>
Risk: Repository data and generated outputs may be stored locally through output files and the GitHub API cache. <br>
Mitigation: Use public repositories where possible, run with --no-cache for sensitive repositories, and review local output paths before sharing files. <br>
Risk: Generated articles may omit context or overstate a project's value. <br>
Mitigation: Review generated articles before publishing and verify claims against the source repository. <br>
Risk: Optional clipboard and image features depend on local Python packages. <br>
Mitigation: Install optional packages in a virtual environment and review generated image files before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caoyachao/github-to-rednote) <br>
- [README](README.md) <br>
- [RedNote Article Prompts](references/prompts.md) <br>
- [RedNote Style Guide](references/rednote-style.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Images] <br>
**Output Format:** [RedNote-style Chinese Markdown/text article with optional PNG or SVG cover image file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write articles to stdout or a file, copy output to the clipboard, cache GitHub API responses locally, and generate a cover image when an output path is provided.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
