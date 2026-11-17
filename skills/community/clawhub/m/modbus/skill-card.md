## Description:

A Modbus-labeled CLI helper for recording, listing, searching, exporting, and checking local task entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill as a CLI-style local record manager for Modbus-labeled tasks such as adding, listing, searching, exporting, and checking status. Security evidence says it does not perform real Modbus communication and should not be relied on for industrial device state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the Modbus-labeled status output for industrial device state.

Mitigation: Use it only as a local note/config record manager and verify real device state with appropriate Modbus tooling.

Risk: Untrusted config keys or values may be written through an unsafe config update path.

Mitigation: Avoid untrusted config input and review changes to files under ~/.modbus or MODBUS_DIR before use.

## Reference(s):

- [ClawHub Modbus skill page](https://clawhub.ai/ckchzh/skills/modbus)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands and local JSONL or CSV file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or mutate files under ~/.modbus or the directory named by MODBUS_DIR.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
