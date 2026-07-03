## Description: <br>
Diagnoses high memory, memory alarm, and OOM scenarios in Huawei Cloud DWS clusters by collecting metrics through KooCLI or the DWS Autopilot MCP Server and producing a standardized diagnosis report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database operators, and support engineers use this skill to investigate Huawei Cloud DWS cluster high-memory alarms, OOM events, and user-initiated memory diagnostics. It gathers read-only cluster, host, metric, session, user, and SQL evidence to distinguish customer-side and system-side root causes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect Huawei Cloud DWS cluster metrics, active sessions, users, and SQL text. <br>
Mitigation: Use least-privilege read-only IAM permissions and run it only on clusters whose diagnostic data may be exposed to the agent. <br>
Risk: Credential handling for KooCLI or the MCP Server can expose AK/SK values if entered in commands or conversation. <br>
Mitigation: Use interactive or environment-based secret entry, avoid command-line AK/SK arguments, and never paste secrets into the chat. <br>
Risk: Generated HTML diagnosis reports may contain sensitive operational data, including SQL text and user/session details. <br>
Mitigation: Review reports before sharing them and delete local report files when they are no longer needed. <br>
Risk: The skill relies on downloaded local Huawei tooling and an optional MCP Server. <br>
Mitigation: Verify downloaded tooling and MCP configuration before granting access to cloud diagnostics. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/huaweiclouddev/skills/huawei-cloud-dws-dymem-diag) <br>
- [CLI Installation Guide - Huawei Cloud DWS Memory Diagnosis](references/cli-installation-guide.md) <br>
- [DWS Autopilot MCP Server](references/dws-mcp-installation-guide.md) <br>
- [IAM Policies - DWS Memory High Diagnosis](references/iam-policies.md) <br>
- [Metric Reference - DWS Memory High Diagnosis](references/metric-reference.md) <br>
- [Memory Background Knowledge - DWS Memory High Diagnosis](references/memory-background.md) <br>
- [Output Format - DWS Memory High Diagnosis](references/output-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, HTML, shell commands, configuration, guidance] <br>
**Output Format:** [HTML diagnosis report plus concise text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a timestamped dws_mem_diagnosis_report HTML file in the workspace when diagnosis runs.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
