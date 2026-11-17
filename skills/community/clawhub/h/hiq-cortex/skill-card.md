## Description:

Find source-backed life-cycle emission factors and published EPDs for material and product footprints, BOM accounting, production-route comparisons, multi-indicator LCIA, CBAM, and EN 15804 work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kirbyingithub](https://clawhub.ai/user/kirbyingithub)

### License/Terms of Use:

MIT-0

## Use Case:

LCA practitioners and product sustainability teams use this skill to find source-backed emission factors and published EPDs, account for bills of materials, compare production routes, and assess multiple LCIA indicators. Results must retain their database, version, system model, geography, and reference unit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer instructions use remote shell scripts, and the security scan was partial because referenced paths were unavailable.

Mitigation: Download the installer into a new directory, verify its published SHA-256 checksum, review the script, and then run it; do not pipe a remote script directly to a shell.

## Reference(s):

- [HiQ Agent Skills](https://github.com/HiQ-AI/agent-skills)
- [Environmental Data CLI](https://github.com/HiQ-AI/environmental-data)
- [HiQ LCA Data](https://www.hiqlcd.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown responses with cited dataset details and inline CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [LCA values include their database, version, system model, geography, and reference unit; the skill does not supply remembered values.]

## Skill Version(s):

1.11.0 (source: frontmatter; matches server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
