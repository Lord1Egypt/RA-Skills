## Description: <br>
Generates a Markdown system operations report with local system, CPU, memory, disk, network, process, and service status details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[viztazeng](https://clawhub.ai/user/viztazeng) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, system administrators, and operations engineers use this skill to collect local diagnostic information for troubleshooting, environment inventory, and routine system health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may contain sensitive local machine details such as hostnames, usernames, IP addresses, disk layout, running processes, and active services. <br>
Mitigation: Review and redact generated reports before sharing them outside the intended operational context. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/viztazeng/my-system-info-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report file with collapsible detail sections and a timestamped filename] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports to the system-tool-results directory and prints the generated report path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
