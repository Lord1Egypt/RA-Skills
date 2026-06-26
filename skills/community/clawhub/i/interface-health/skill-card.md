## Description: <br>
Interface and link health assessment for Cisco IOS-XE/NX-OS, Juniper JunOS, and Arista EOS, covering error counters, optical power, discards, resets, flaps, and utilization against severity-tiered thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network engineers and operations teams use this skill to diagnose link degradation, packet loss, interface flaps, optical alarms, and utilization issues across Cisco, Juniper, and Arista devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is labeled read-only while including commands that can reset counters or disrupt live interfaces. <br>
Mitigation: Use read-only accounts for diagnosis, preserve counter snapshots, and require human change-control approval before clearing counters, shutting interfaces, or re-enabling ports. <br>


## Reference(s): <br>
- [Interface Health CLI Reference](artifact/references/cli-reference.md) <br>
- [Interface Health Threshold Tables](artifact/references/threshold-tables.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/vahagn-madatyan/interface-health) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with vendor-specific CLI command blocks, threshold tables, decision trees, and a report template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Diagnostic workflow for interface health assessment; no structured machine-readable output is specified.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
