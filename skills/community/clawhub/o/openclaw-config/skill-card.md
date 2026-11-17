## Description:

Helps agents edit and validate OpenClaw Gateway JSON5 configuration while avoiding schema mismatches that can break startup or weaken security policies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caopulan](https://clawhub.ai/user/caopulan)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect, edit, and validate OpenClaw Gateway configuration for gateway, channel, model, tool, skill, plugin, and include settings before applying changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent OpenClaw Gateway configuration changes can affect auth, remote access, plugins, skills, or tool-execution behavior.

Mitigation: Review proposed config changes before applying them, validate with openclaw doctor, and require explicit consent for commands that write or automatically fix config and state files.

Risk: Long-lived secrets or API keys could be placed directly in openclaw.json.

Mitigation: Prefer environment variables or credential files, keep config permissions restrictive, and avoid committing tokens or API keys.

## Reference(s):

- [OpenClaw Config Field Index](references/openclaw-config-fields.md)
- [OpenClaw Config Schema Sources](references/schema-sources.md)
- [OpenClaw Config on ClawHub](https://clawhub.ai/caopulan/skills/openclaw-config)
- [OpenClaw source repository for schema lookup](https://github.com/openclaw/openclaw.git)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON5 examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent OpenClaw configuration edits and validation commands for user review.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
