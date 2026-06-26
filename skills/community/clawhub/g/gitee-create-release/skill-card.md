## Description: <br>
Use this skill when the user asks to publish a release, create a release, "create release", "create-release", "tag a release", or generate a changelog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oschina](https://clawhub.ai/user/oschina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release maintainers use this skill to review Gitee release history, summarize merged pull requests, generate a changelog, and create a confirmed release through Gitee MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A release may be created with the wrong repository, version tag, prerelease status, or changelog content. <br>
Mitigation: Verify the owner, repository, version tag, prerelease flag, and generated changelog before confirming release creation. <br>
Risk: The Gitee token used by the MCP server may grant broader repository permissions than needed. <br>
Mitigation: Use a least-privileged Gitee token where possible and install the skill only for intended release management workflows. <br>


## Reference(s): <br>
- [Create Release on ClawHub](https://clawhub.ai/oschina/gitee-create-release) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown changelog text and Gitee MCP release creation requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured Gitee MCP tools and user confirmation before creating a release.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
