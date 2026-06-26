## Description: <br>
Generates structured PRD documents, interactive HTML prototypes, screenshots, flow maps, and optional iWiki publishing guidance from product requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junko-zhang](https://clawhub.ai/user/junko-zhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers and product teams use this skill to turn requirement descriptions or existing notes into PRDs, clickable prototypes, screenshots, and iWiki-ready publication packages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing can upload local PRD content and screenshots to iWiki using the user's token. <br>
Mitigation: Review PRD text and images for confidential content before publishing, and use a least-privilege iWiki personal access token. <br>
Risk: Cover-style publishing can overwrite an existing iWiki page when explicitly requested. <br>
Mitigation: Use the default non-cover mode or dry-run checks unless an overwrite is intended. <br>
Risk: Optional workspace helper scripts may read or write local project files while generating prototypes, screenshots, and publishing packages. <br>
Mitigation: Run the skill only in trusted workspaces and review generated or modified files before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/junko-zhang/prd-generator-team) <br>
- [TAI personal token setup](https://tai.it.woa.com/user/pat) <br>
- [README](README.md) <br>
- [User guide](guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with generated PRD files, HTML prototype assets, screenshots, flow-map images, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write workspace PRD artifacts and may publish selected PRD content and images to iWiki when the user provides a token and requests publication.] <br>

## Skill Version(s): <br>
4.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
