## Description: <br>
OpenCLI Agent helps an agent translate natural-language requests into opencli commands for web-service automation across social media, content discovery, downloads, desktop apps, and local CLI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhengmengkaizmk](https://clawhub.ai/user/zhengmengkaizmk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to have an agent plan and run opencli commands for supported websites, online services, desktop applications, and registered local CLI tools. It is intended for workflows such as reading feeds, searching content, posting, replying, downloading media, and checking the OpenCLI setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to act through logged-in web accounts, including posting, deleting, following, blocking, messaging, or downloading content. <br>
Mitigation: Use a dedicated low-risk browser profile or test accounts, and require manual confirmation before any account-changing, public, destructive, messaging, or download action. <br>
Risk: OpenCLI plugin and external CLI workflows can expand the agent's local execution surface and may install or invoke additional tools. <br>
Mitigation: Verify OpenCLI, extension, plugin, and CLI sources before use, and avoid plugin installation, auto-install, or external CLI proxy features unless explicitly needed. <br>
Risk: The workflow depends on Chrome session state and a browser extension, so commands may operate with the permissions of the signed-in user. <br>
Mitigation: Run the setup check first, keep Chrome profiles scoped to the task, and review command targets and outputs before relying on results. <br>


## Reference(s): <br>
- [OpenCLI Command Reference](references/command_reference.md) <br>
- [OpenCLI Extension Releases](https://github.com/jackwener/opencli/releases) <br>
- [Skill Page](https://clawhub.ai/zhengmengkaizmk/opencli-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional structured command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request JSON, YAML, Markdown, CSV, or table output from opencli when a command supports formatted results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
