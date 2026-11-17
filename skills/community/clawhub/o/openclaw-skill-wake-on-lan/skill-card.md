## Description:

Wake-on-LAN functionality for macOS - wake devices remotely by MAC address or name.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppopen](https://clawhub.ai/user/ppopen)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to wake, list, add, remove, and check saved Wake-on-LAN devices on a local macOS network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent can send Wake-on-LAN packets to local network devices, including all saved devices when broadcast is used.

Mitigation: Install only when this behavior is intended, review saved devices before broadcast, and use explicit Wake-on-LAN phrasing for wake requests.

Risk: The skill maintains a saved device list with MAC addresses, broadcast addresses, and optional ping IPs under ~/.config/openclaw/wol-devices.json.

Mitigation: Review the device list regularly, remove stale entries, and protect the local config file according to workstation policy.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown guidance with shell command examples and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local JSON device list at ~/.config/openclaw/wol-devices.json and the wakeonlan command.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
