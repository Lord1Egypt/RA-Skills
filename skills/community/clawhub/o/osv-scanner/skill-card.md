## Description:

Scans Node.js/NPM, Python, and Linux package inventories for known vulnerabilities using the Google OSV API and reports related CVEs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moenassi](https://clawhub.ai/user/moenassi)

### License/Terms of Use:


## Use Case:

Developers and system maintainers use this skill to check project dependencies or host package inventories for known vulnerabilities before release, maintenance, or remediation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package names and versions may be sent to OSV during scans, including installed OS package inventories in os mode.

Mitigation: Run the scanner only where sharing package inventory with OSV is acceptable, and avoid os mode on sensitive hosts.

Risk: The scanner can execute local package-discovery commands when run in os mode.

Mitigation: Install and run it in a dedicated virtual environment, avoid root or administrator execution, and review the scan mode before use on production systems.

Risk: Dependency and report-template hygiene issues may affect reliable report generation.

Mitigation: Prefer pinned dependency versions and verify the XLSX template before relying on generated reports.

## Reference(s):

- [ClawHub OSV Scanner release](https://clawhub.ai/moenassi/skills/osv-scanner)
- [OSV API query endpoint](https://api.osv.dev/v1/query)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands, terminal vulnerability output, and optional XLSX report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries OSV with package names and versions; XLSX report generation depends on a valid local template file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
