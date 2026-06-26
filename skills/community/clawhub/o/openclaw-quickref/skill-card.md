## Description: <br>
Provides a quick reference for OpenClaw CLI commands, configuration syntax, and common setup patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxadc](https://clawhub.ai/user/maxadc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to answer OpenClaw command, configuration, environment variable, and setup-reference questions quickly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples include commands that can change configuration, remove plugins, delete sessions, or start daemon services. <br>
Mitigation: Review each command against the current workspace and OpenClaw environment before running it. <br>
Risk: Configuration examples mention API keys and service tokens. <br>
Mitigation: Use environment variables or secret storage, and do not paste real credentials into shared commands or files. <br>
Risk: Plugin installation examples may point to external or local package sources. <br>
Mitigation: Verify plugin source, publisher, and package contents before installation. <br>


## Reference(s): <br>
- [OpenClaw CLI Command Reference](references/cli-reference.md) <br>
- [OpenClaw Configuration Reference](references/config-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/maxadc/openclaw-quickref) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline command and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; no automatic actions are executed by the skill.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter: 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
