## Description:

Scan and map devices on the local network, including IP addresses, hostnames, vendors, device types, first-seen and last-seen times, friendly labels, and searchable device inventory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wrentheai](https://clawhub.ai/user/wrentheai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, IT staff, and home or office network operators use this skill to discover devices on a local network, find device IP addresses, label known devices, and investigate new or unknown devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Active network scanning can be inappropriate on work, shared, or unauthorized networks.

Mitigation: Use the skill only on networks where scanning is permitted, limit scans to the intended local subnet, and avoid deep or watch mode unless explicitly needed.

Risk: MAC vendor lookup can send device MAC addresses to a third-party service.

Mitigation: Review policy before use and disable or remove online vendor lookup when MAC addresses should remain local.

Risk: The skill retains a local inventory of discovered devices.

Mitigation: Review the stored device database and cache location, protect local access to those files, and remove retained inventory when it is no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wrentheai/skills/netmap)
- [MAC Vendors API](https://api.macvendors.com)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and JSON output when exporting the device database]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist a local device inventory and vendor lookup cache under the user's home configuration directory.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
