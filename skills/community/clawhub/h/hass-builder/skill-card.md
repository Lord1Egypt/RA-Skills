## Description:

A skill to build and manage Home Assistant configurations with the Home Assistant Builder (`hab`) CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ha](https://clawhub.ai/user/ha)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, operators, and Home Assistant administrators use this skill to inspect, create, update, delete, operate, and troubleshoot Home Assistant resources from a terminal. It emphasizes read-first workflows, JSON parsing, preview steps, confirmation for risky mutations, and verification commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper downloads and executes a mutable latest GitHub release binary without integrity verification while using HAB_TOKEN and HAB_URL credentials.

Mitigation: Use only in trusted environments, prefer a pinned and checksum-verified hab release for sensitive deployments, and confirm that credential exposure to the downloaded CLI is acceptable.

Risk: Home Assistant operations can change or delete resources, restart systems, affect connectivity, or alter hardware behavior.

Mitigation: Start with read-only inventory, use --plan or --dry-run when available, obtain explicit user confirmation for risky mutations, avoid convenience use of --force, and run verification commands after changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ha/skills/hass-builder)
- [Publisher Profile](https://clawhub.ai/user/ha)
- [Home Assistant Build CLI](https://github.com/balloob/home-assistant-build-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON-field inspection guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may produce JSON envelopes or NDJSON event streams when executed through the hab CLI.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
