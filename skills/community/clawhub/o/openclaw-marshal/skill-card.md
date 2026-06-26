## Description: <br>
Defines security policies for agent workspaces, audits installed skills against command, network, data-handling, and workspace hygiene rules, and generates compliance reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtlasPA](https://clawhub.ai/user/AtlasPA) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and workspace administrators use this skill to define local security policy, review installed agent skills for compliance gaps, and produce audit-ready status or report output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports under-documented enforcement commands that can rename installed skills or replace policy files. <br>
Mitigation: Use audit, check, report, and status for read-focused review; run enforce, protect, quarantine, or templates only after backing up the workspace and confirming the intended changes. <br>
Risk: Policy initialization and template application can create or overwrite .marshal-policy.json. <br>
Mitigation: Review the active policy before and after applying templates, and keep a recoverable copy of prior workspace policy. <br>


## Reference(s): <br>
- [OpenClaw Marshal ClawHub page](https://clawhub.ai/AtlasPA/openclaw-marshal) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with JSON policy files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Python 3 and can create or update workspace policy files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
