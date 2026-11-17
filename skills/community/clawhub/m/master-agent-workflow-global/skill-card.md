## Description:

Master Agent Workflow Global helps OpenClaw users run parallel agent workflows with configurable worker limits, templates, error handling, and migration tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shujianming](https://clawhub.ai/user/shujianming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install a global master-agent workflow, coordinate batch tasks across worker agents, and manage reusable templates, configuration, backups, and migrations across environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and activation scripts can make persistent local changes to OpenClaw configuration, shell startup files, aliases, MAW_HOME, and PATH.

Mitigation: Review the installer before use, run it first in a test environment, back up existing OpenClaw and shell configuration files, and inspect startup files after installation.

Risk: Migration and import flows can write configuration and template files from supplied archives or JSON files.

Mitigation: Import only trusted migration files, inspect imported configuration and templates before applying them, and keep a backup of the target configuration directory.

Risk: Documentation includes a curl-to-bash migration path.

Mitigation: Avoid piping remote scripts directly to a shell; download the installer, verify its source and contents, then execute the reviewed local copy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shujianming/skills/master-agent-workflow-global)
- [Publisher Profile](https://clawhub.ai/user/shujianming)
- [README](artifact/README.md)
- [Skill Documentation](artifact/SKILL.md)
- [Usage Examples](artifact/references/examples.md)
- [Migration Guide](artifact/migration-guide.md)
- [OpenClaw Hook Guide](artifact/hooks/openclaw/HOOK.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain-text agent responses with JSON configuration and shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include generated execution instructions, configuration/template summaries, migration guidance, and local file paths.]

## Skill Version(s):

2.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
