## Description:

Use when scripting or batch-driving a NetBox instance over the REST API - relocating/renaming devices, cables, IP assignment, OOB/primary IP, pre-verify + read-back.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indane](https://clawhub.ai/user/indane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to plan and script NetBox REST API changes such as device relocation, renames, cable cleanup, IP assignment, and post-change verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A NetBox bearer token could be exposed to an unintended URL.

Mitigation: Review or patch the helper before use, keep requests limited to trusted NetBox hosts, and use a narrowly scoped token.

Risk: TLS verification can be disabled for internal or self-signed certificate scenarios.

Mitigation: Keep certificate verification enabled by default and set NETBOX_INSECURE_TLS only in a controlled emergency.

Risk: Batch PATCH or DELETE operations can make broad NetBox inventory changes.

Mitigation: Require explicit confirmation before write batches, pre-verify object identity, and read back changed objects after execution.

## Reference(s):

- [NetBox REST API quick reference](references/netbox-api.md)
- [Batch device operations verified recipe](references/batch-device-operations.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands, API payloads, and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed NetBox API request plans, helper script usage, and read-back verification steps.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
