## Description: <br>
Repo Explorer helps an agent inspect Gitee repositories through a configured Gitee MCP server and produce concise repository overview reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oschina](https://clawhub.ai/user/oschina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and reviewers use this skill to get oriented in a Gitee repository, inspect its structure and key documentation, and generate a focused overview report. It can also support targeted investigation of areas such as authentication, database access, configuration, or core modules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured Gitee account may allow repository files, including private repository content, to be read into the assistant context. <br>
Mitigation: Use a trusted Gitee MCP server and account, and only ask the skill to inspect private or sensitive repositories when that disclosure is intended. <br>
Risk: The skill can optionally use a local mcporter binary when present. <br>
Mitigation: Verify any optional mcporter binary independently before relying on it for repository access. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/oschina/gitee-repo-explorer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown repository overview report with optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Gitee MCP server plus repository owner and name; accepts an optional area of interest for deeper exploration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
