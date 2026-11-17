## Description:

Use this skill when the user asks to publish a release, create a release, "create release", "create-release", "tag a release", or generate a changelog. Requires Gitee MCP Server to be configured.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oschina](https://clawhub.ai/user/oschina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release managers use this skill to prepare Gitee releases by checking prior releases, collecting merged pull requests, generating a categorized changelog, and creating the release after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured Gitee MCP Server may let the agent inspect or manage repositories beyond the intended release target.

Mitigation: Configure the Gitee MCP Server only for repositories the agent is intended to manage before installing or using the skill.

Risk: An incorrect changelog, version, or prerelease setting could publish a misleading release.

Mitigation: Review the generated changelog, version number, and release settings before approving release creation.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls, Shell commands]

**Output Format:** [Markdown changelog text, Gitee MCP tool calls, and a release link after publication]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Gitee MCP Server and user confirmation before release creation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
