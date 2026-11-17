## Description:

PRD文档生成器（团队版） - 从需求描述一键生成完整PRD文档与HTML交互原型，支持iWiki发布

This skill is ready for commercial/non-commercial use.

## Publisher:

[junko-zhang](https://clawhub.ai/user/junko-zhang)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers and product teams use this skill to turn requirement descriptions into structured PRD documents, interactive HTML prototypes, screenshots, flow maps, and optional iWiki publication workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: iWiki publishing uses an authenticated TAI_PAT_TOKEN with broad document authority.

Mitigation: Use a narrowly scoped, revocable token and avoid storing it in shell startup files.

Risk: Publishing can create, update, or overwrite iWiki content.

Mitigation: Confirm the project directory, parent page ID, document ID, and overwrite mode before upload.

Risk: Generated PRD content and prototypes may contain incomplete or incorrect product guidance.

Mitigation: Review generated documents, screenshots, and flow maps before sharing or publishing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/junko-zhang/skills/prd-generator-team)
- [README](artifact/README.md)
- [Usage guide](artifact/guide.md)
- [TAI PAT token setup](https://tai.it.woa.com/user/pat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documents, HTML prototype files, image assets, flow-map files, shell commands, and iWiki publication guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally package and publish generated PRD content and images to iWiki when the user provides a valid TAI_PAT_TOKEN.]

## Skill Version(s):

4.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
