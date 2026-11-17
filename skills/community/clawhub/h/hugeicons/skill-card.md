## Description:

Hugeicons MCP Server是一个基于TypeScript的服务器，提供Hugeicons图标库的集成工具和资源，支持多种平台的图标搜索、获取和使用指南。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to list Hugeicons icons, search icons by name or tag, retrieve platform-specific usage guidance, and get icon glyph information through the configured API service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports mismatched documentation and code for an icon lookup skill.

Mitigation: Review the artifact before installation and confirm the documented icon workflow matches the installed scripts.

Risk: The skill stores the user API key in a local plaintext .env file.

Mitigation: Use only an API key suitable for local plaintext storage, keep the .env file out of source control, and rotate the key if exposure is suspected.

Risk: Tool calls send requests to an external XiaoBenYang service.

Mitigation: Confirm the API service relationship and data handling expectations before using the skill with sensitive queries or credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/hugeicons)
- [XiaoBenYang API key portal](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries of JSON API responses and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided XBY_APIKEY before tool calls can return icon data.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact SKILL.md frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
