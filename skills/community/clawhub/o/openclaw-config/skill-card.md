## Description: <br>
Edit and validate OpenClaw Gateway config (openclaw.json / JSON5). Use when adding/changing config keys (gateway.*, agents.*, models.*, channels.*, tools.*, skills.*, plugins.*, $include) or diagnosing openclaw doctor/config validation errors, to avoid schema mismatches that prevent the Gateway from starting or weaken security policies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caopulan](https://clawhub.ai/user/caopulan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to edit OpenClaw Gateway configuration with a schema-first workflow, validate changes, and troubleshoot doctor or config validation errors before the Gateway is restarted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect config keys, types, or broad file replacement can prevent OpenClaw Gateway startup or unintentionally change security behavior. <br>
Mitigation: Prefer targeted config set, unset, or patch edits, review proposed changes, keep backups, and run openclaw doctor after changes. <br>
Risk: Long-lived tokens or API keys may be placed directly in openclaw.json while configuring channels or tools. <br>
Mitigation: Prefer environment variables or credential files for secrets and avoid committing tokens in configuration files. <br>
Risk: Automatic repair commands can write to config or state files without a clear review step. <br>
Mitigation: Require explicit user consent before running write-capable repair commands such as openclaw doctor --fix or --yes. <br>


## Reference(s): <br>
- [OpenClaw Config Field Index](references/openclaw-config-fields.md) <br>
- [OpenClaw Config Schema Sources](references/schema-sources.md) <br>
- [Openclaw Config on ClawHub](https://clawhub.ai/caopulan/openclaw-config) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON5 configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May suggest targeted OpenClaw config edits, validation commands, and troubleshooting steps for user review.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
