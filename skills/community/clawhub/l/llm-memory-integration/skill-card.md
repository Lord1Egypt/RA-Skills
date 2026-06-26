## Description: <br>
LLM Memory V9 provides a public framework package that links a user-controlled local private configuration directory through CNB_PRIVATE_WORKSPACE while keeping shared templates separate from private files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xkzs2007](https://clawhub.ai/user/xkzs2007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install default workspace templates and optionally link a local private configuration directory into the skill workspace for custom AGENTS.md, TOOLS.md, memory, and configuration files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The postinstall hook can automatically link or copy private local files from CNB_PRIVATE_WORKSPACE into the skill workspace. <br>
Mitigation: Review the CNB_PRIVATE_WORKSPACE path before installation, use a dedicated minimal directory, and avoid including secrets or broad personal folders. <br>
Risk: Permission metadata may underreport the private local file access performed by the postinstall hook. <br>
Mitigation: Treat install-time linking as a review point and use --no-hooks or unset CNB_PRIVATE_WORKSPACE when private files should not be linked. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xkzs2007/llm-memory-integration) <br>
- [Hooks README](hooks/README.md) <br>
- [Workspace template README](workspace_template/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, configuration, guidance, shell commands] <br>
**Output Format:** [Markdown documentation, workspace template files, and local filesystem link or copy actions during postinstall] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; CNB_PRIVATE_WORKSPACE is optional and controls private file linking.] <br>

## Skill Version(s): <br>
9.0.1 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
