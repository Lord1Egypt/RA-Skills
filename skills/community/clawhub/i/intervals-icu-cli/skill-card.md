## Description:

Use this skill when an installed `intervals` CLI should be used to query Intervals.icu, inspect activities, create scheduled workout events, create workout library items, or write wellness data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonaswide](https://clawhub.ai/user/jonaswide)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to choose safe `intervals` CLI commands for Intervals.icu reads and requested writes, including activity queries, scheduled workout events, reusable workout items, and wellness data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install a mutable `latest` CLI release from an upstream third-party GitHub publisher.

Mitigation: Install only after trusting the upstream publisher, and prefer a pinned, checksum-verified CLI release.

Risk: The CLI can access authenticated Intervals.icu fitness data.

Mitigation: Use an appropriate Intervals.icu credential and confirm the user is comfortable granting CLI access before use.

Risk: Requested write actions can create or change events, workout library items, or wellness data.

Mitigation: Review mutations before execution and prefer a read command after each write to verify the resulting data.

## Reference(s):

- [Skill page](https://clawhub.ai/jonaswide/skills/intervals-icu-cli)
- [Intervals CLI homepage](https://github.com/jonaswide/intervals-cli)
- [Query guidance](references/queries.md)
- [Write patterns](references/writes.md)
- [Install intervals CLI (macOS arm64)](https://github.com/jonaswide/intervals-cli/releases/latest/download/intervals_darwin_arm64.tar.gz)
- [Install intervals CLI (macOS amd64)](https://github.com/jonaswide/intervals-cli/releases/latest/download/intervals_darwin_amd64.tar.gz)
- [Install intervals CLI (Linux arm64)](https://github.com/jonaswide/intervals-cli/releases/latest/download/intervals_linux_arm64.tar.gz)
- [Install intervals CLI (Linux amd64)](https://github.com/jonaswide/intervals-cli/releases/latest/download/intervals_linux_amd64.tar.gz)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON payloads]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers JSON-formatted CLI output, absolute dates, stdin or temporary files for complex writes, and read-after-write verification.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
