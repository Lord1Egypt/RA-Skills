## Description: <br>
Diagnoses high CPU conditions in Huawei Cloud DWS clusters by collecting CPU metrics through KooCLI or the DWS Autopilot MCP Server, analyzing customer-side or system-side causes, and producing a standardized diagnosis report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to investigate DWS cluster high CPU alarms, CPU load anomalies, and user-initiated CPU diagnosis requests. It gathers cluster metrics, host data, concurrency information, query details, and process usage before generating a factual HTML diagnosis report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installation references include OBS and obsutil setup that is not needed for DWS CPU diagnosis. <br>
Mitigation: Follow only the DWS, KooCLI, and DWS Autopilot MCP setup steps unless OBS tooling is independently required. <br>
Risk: Credential setup can expose Huawei Cloud AK/SK secrets if entered directly in shell commands or conversation. <br>
Mitigation: Use interactive configuration or protected environment/config files, avoid command-line secrets, and grant only the read-only DWS permissions listed in the IAM policy reference. <br>
Risk: Generated HTML diagnosis reports may contain operational details such as cluster identifiers, users, queries, process names, and timestamps. <br>
Mitigation: Treat generated reports as sensitive operational data and share them only with authorized reviewers. <br>


## Reference(s): <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [DWS Autopilot MCP Server Installation Guide](references/dws-mcp-installation-guide.md) <br>
- [IAM Policies](references/iam-policies.md) <br>
- [Metric Reference](references/metric-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/huaweiclouddev/skills/huawei-cloud-dws-cpu-diag) <br>


## Skill Output: <br>
**Output Type(s):** [text, HTML, shell commands, API calls, configuration guidance] <br>
**Output Format:** [Text summary and complete HTML diagnosis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report is generated from tool-returned data, uses Beijing time for displayed timestamps, and may be saved as dws_cpu_diagnosis_report_{timestamp}.html.] <br>

## Skill Version(s): <br>
0.0.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
