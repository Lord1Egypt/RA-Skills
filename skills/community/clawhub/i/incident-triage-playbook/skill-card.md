## Description: <br>
Runbook-first incident triage workflow for service outages and high-error alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JiaranI](https://clawhub.ai/user/JiaranI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Incident responders, on-call engineers, and service owners use this skill to gather alert context, assign ownership, keep a concise timeline, and produce checklist and report artifacts during early incident triage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The playbook includes commands that may update owner and timeline state in a local incident-management workflow. <br>
Mitigation: Confirm that the local triage and workflow commands are the intended tools before applying the playbook during a live incident. <br>
Risk: The healthcheck helper prints a different skill name even though ClawScan did not classify it as harmful. <br>
Mitigation: Treat the mismatch as a version-alignment issue and review helper output before relying on it for release or operational checks. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown runbook guidance with command examples and reusable checklist and report templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes templates/checklist.md and templates/report.md; helper scripts only echo version or healthcheck text.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
