## Description:

Use when installing, updating, diagnosing, configuring, fixing, tuning, or setting up anything in OpenClaw, including gateway outages, silent channels, model failover issues, auth errors, agent routing problems, config validation failures, plugin drift after update, and operational tasks involving openclaw.json, the gateway, agents, channels, or the openclaw CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rendrag-git](https://clawhub.ai/user/rendrag-git)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and AI coding assistants use this skill to diagnose, configure, repair, and maintain local OpenClaw installations. It provides operational runbooks for gateway health, channels, plugins, config validation, install/update drift, and safe OpenClaw CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local administration workflows can expose OpenClaw credentials or private session data if an agent reads full config, env, secrets, logs, or workspace contents indiscriminately.

Mitigation: Review before installing in credentialed environments, prefer narrow `openclaw config get <key>` reads, never open secrets or env files, and require approval before reading session or workspace file contents.

Risk: Full-config reads may reveal inline credentials or sensitive routing and provider configuration.

Mitigation: Use targeted config reads whenever possible; when edits are required, back up first, change individual keys, validate with `openclaw config validate`, and avoid batch-writing openclaw.json.

Risk: Gateway restart, stop, service reinstall, deletion, token rotation, or destructive system changes can interrupt service or remove state.

Mitigation: Require explicit user confirmation for restart/write/delete actions, verify the active service manager and process before changes, and rerun health, doctor, channel, plugin, and task checks after each fix.

Risk: Online documentation refreshes or fetches could accidentally carry local logs, config, session text, or secrets to an external service.

Mitigation: Fetch only public OpenClaw documentation URLs, keep local evidence out of web requests, and avoid refreshing live docs during active incidents unless the user approves and the immediate repair is not blocked.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/rendrag-git/skills/openclawadmin)
- [OpenClaw documentation](https://docs.openclaw.ai/)
- [OpenClaw docs index](https://docs.openclaw.ai/llms.txt)
- [Config map](config-map.md)
- [Local install profile](local-install.md)
- [Update failure patterns](update-failure-patterns.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, code]

**Output Format:** [Markdown guidance with inline shell commands, configuration paths, and operational checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local diagnostic command sequences, config-editing steps, risk notes, and follow-up verification checks.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
