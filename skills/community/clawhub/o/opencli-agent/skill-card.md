## Description:

OpenCLI Agent helps an agent turn natural-language requests into opencli commands for browser-backed website, social media, content, download, desktop app, and local CLI automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengmengkaizmk](https://clawhub.ai/user/zhengmengkaizmk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check OpenCLI setup, map requests to supported opencli commands, run read or write actions across web services, and summarize command results or remediation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act through logged-in browser sessions, including social account actions.

Mitigation: Use a dedicated Chrome profile, avoid primary logged-in sessions, and require manual approval before any post, delete, follow, block, or message action.

Risk: The skill may install unpinned npm packages, browser extensions, plugins, or external CLI tools.

Mitigation: Pin and verify the npm package and extension source, and require manual approval before package, plugin, or tool installation.

Risk: The skill can control local applications and execute local CLI commands.

Mitigation: Require manual approval before local CLI execution and keep each command scoped to the user's requested task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhengmengkaizmk/skills/opencli-agent)
- [OpenCLI Command Reference](references/command_reference.md)
- [OpenCLI extension releases](https://github.com/jackwener/opencli/releases)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and optional structured command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request JSON, YAML, Markdown, CSV, or table output from opencli when supported.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
