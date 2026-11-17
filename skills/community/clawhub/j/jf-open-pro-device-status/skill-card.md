## Description:

Checks whether JFTech devices are online, supporting single-device and batch status queries with online/offline state, wake state, and optional table or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to query JFTech Open Platform device status for one device or many devices after configuring account credentials and device tokens.

### Deployment Geography for Use:

China Mainland, Asia, Europe, and North America

## Known Risks and Mitigations:

Risk: Device tokens and signed account metadata can be sent to a hostname supplied through JF_ENDPOINT.

Mitigation: Restrict JF_ENDPOINT to the documented JFTech API hosts and prevent untrusted users, CI inputs, wrappers, or generated configs from setting it.

Risk: Device tokens, UUIDs, app keys, app secrets, signatures, and WAN IPs are sensitive operational data.

Mitigation: Keep credentials and device identifiers out of logs and shared outputs, and avoid table output when WAN IP disclosure is not needed.

## Reference(s):

- [JFTech Open Platform documentation](https://docs.jftech.com)
- [ClawHub skill page](https://clawhub.ai/jftech/skills/jf-open-pro-device-status)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration]

**Output Format:** [Plain text, table text, or JSON responses; Markdown usage guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JF_UUID, JF_APP_KEY, JF_APP_SECRET, and device tokens; batch queries are processed in groups of up to 500 devices.]

## Skill Version(s):

1.0.1 (source: server release metadata; bundled skill metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
