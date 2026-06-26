## Description: <br>
A skill to build and manage Home Assistant configurations using the Home Assistant Builder (hab) CLI for inspection, creation, updates, deletion, operations, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ha](https://clawhub.ai/user/ha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and Home Assistant administrators use this skill to generate safe hab CLI workflows for Home Assistant resources, dashboards, automations, backups, operations, and ESPHome tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hab CLI can perform powerful Home Assistant operations using HAB_TOKEN and HAB_URL, including deletes, restarts, backup restore/delete, network changes, and ESPHome hardware actions. <br>
Mitigation: Use least-privileged tokens, start with read-only or preview commands, review the exact command, and require explicit user confirmation before risky mutations. <br>
Risk: The wrapper script downloads the hab binary from the upstream GitHub latest release before executing it. <br>
Mitigation: Install only when the upstream Home Assistant Builder releases are trusted and the environment can safely run downloaded CLI binaries. <br>


## Reference(s): <br>
- [Home Assistant Build CLI](https://github.com/balloob/home-assistant-build-cli) <br>
- [ClawHub skill page](https://clawhub.ai/ha/hass-builder) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with ordered shell commands, JSON field guidance, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts agents to prefer JSON output, preview mutations with --plan or --dry-run when supported, and include verification commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
