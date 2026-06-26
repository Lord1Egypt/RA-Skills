## Description: <br>
Huo15 OpenClaw Enhance is an OpenClaw plugin that adds non-invasive agent-harness enhancements such as memory support, task and workflow tools, status views, file sharing, upload handling, configuration diagnostics, and skill recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this plugin to extend OpenClaw with non-invasive productivity, memory, workflow, file-transfer, diagnostics, and safety-observation features while keeping overlapping behavior delegated to OpenClaw itself. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin enables broad always-on memory, prompt-hook, local scanning, task-dispatch, and file-transfer behavior beyond the narrow upload-loop fix described in the release summary. <br>
Mitigation: Review the enabled modules before deployment and disable unneeded features such as bridge dispatch, session bridge, native memory surfacing, file sharing or upload, configuration diagnostics, hook profiling, workflows, and lifecycle memory capture. <br>
Risk: Setup and LaunchAgent scripts can create persistent instruction-file changes or scheduled execution. <br>
Mitigation: Do not run setup or scheduled follow-up scripts unless the operator has reviewed the changes and accepted persistent local effects. <br>
Risk: Memory export and upload or share links can expose sensitive local data paths or generated files. <br>
Mitigation: Treat memory exports and file links as sensitive, limit sharing to intended recipients, and revoke or expire links when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhaobod1/skills/huo15-openclaw-enhance) <br>
- [Publisher Profile](https://clawhub.ai/user/zhaobod1) <br>
- [Project Homepage](https://cnb.cool/huo15/ai/huo15-openclaw-enhance) <br>
- [README](README.md) <br>
- [Architecture](docs/architecture.md) <br>
- [Non-invasive Enhancement ADR](docs/decisions/0001-non-invasive-enhancement.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and structured tool responses with file paths, shell commands, JSON-like configuration, and human-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local file-share or upload links, memory and task records, diagnostic findings, and commands for an OpenClaw user to review before execution.] <br>

## Skill Version(s): <br>
6.7.21 (source: server release evidence and package.json; changelog released 2026-06-26) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
