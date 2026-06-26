## Description: <br>
Windows PC health-check skill that inspects CPU, memory, disk, network, processes, drivers, devices, startup entries, listening ports, security updates, and recent system events, then generates a structured Markdown or JSON report with risk levels and suggested actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolfzb](https://clawhub.ai/user/coolfzb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and support engineers use this skill to run quick or full Windows PC diagnostics and receive a structured health report with warnings, errors, and practical remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs broad local diagnostics that may reveal process lists, network ports, startup entries, drivers, devices, update posture, and recent system events. <br>
Mitigation: Use explicit diagnostic commands, review generated reports before sharing them, and keep saved reports in private storage. <br>
Risk: Saved health reports may persist sensitive system details beyond the interactive session. <br>
Mitigation: Save reports only to intended paths, restrict access to the saved files, and delete reports when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coolfzb/pc-health-check) <br>
- [Publisher profile](https://clawhub.ai/user/coolfzb) <br>
- [README](artifact/README.md) <br>
- [CHANGELOG](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Guidance, Files] <br>
**Output Format:** [Structured JSON or Markdown health report with risk levels, summary tables, and suggested actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can be generated in quick or full mode and may be saved to a local file when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and changelog report 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
