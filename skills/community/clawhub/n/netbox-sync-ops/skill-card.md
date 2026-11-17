## Description:

Infrastructure inventory automation and utility operations for netbox-proxmox-sync, an idempotent state sync that models Proxmox VE and UniFi into NetBox DCIM/IPAM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddygk](https://clawhub.ai/user/eddygk)

### License/Terms of Use:

MIT-0

## Use Case:

Infrastructure operators, developers, and engineers use this skill to deploy, schedule, troubleshoot, and safely extend NetBox inventory syncs for Proxmox VE, UniFi, and optional iDRAC/Redfish enrichment. It focuses on dry-run review, idempotency checks, reaper gating, and NetBox API issue resolution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide NetBox write and delete workflows through the sync reaper.

Mitigation: Use a least-privilege NetBox token, run --dry-run --report first, keep --no-reap enabled until deletion thresholds are reviewed, and confirm the reaper only targets records owned by the sync.

Risk: Incorrect comparisons or NetBox API modeling can cause repeated updates or HTTP 400 failures.

Mitigation: Follow the bundled gotchas reference for numeric comparisons, object re-fetching, VirtualDisk ownership, interface bridge modeling, and exact interface type strings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eddygk/skills/netbox-sync-ops)
- [netbox-proxmox-sync homepage](https://github.com/eddygk/netbox-proxmox-sync)
- [Extending reference](references/extending.md)
- [Gotchas reference](references/gotchas.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and operational checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires environment-specific NetBox, Proxmox, and optional UniFi or iDRAC credentials before commands are usable.]

## Skill Version(s):

1.0.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
