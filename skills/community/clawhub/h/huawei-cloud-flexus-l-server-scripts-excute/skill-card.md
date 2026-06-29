## Description: <br>
Based on Huawei Cloud COC (Cloud Operations Center) APIs for script management and remote execution, this skill supports creating Shell, Python, and Bat scripts and batch execution on target host instances via UniAgent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations engineers use this skill to create, list, execute, and query Huawei Cloud COC scripts for Flexus L instances. It is suited to batch operations, deployment, health checks, log collection, and emergency operational response where remote execution is intentionally authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables high-impact cloud script execution, including root-level execution on target instances. <br>
Mitigation: Use a dedicated least-privilege Huawei Cloud identity, verify target instance IDs and script UUIDs manually, and require out-of-band confirmation before production or root-level execution. <br>
Risk: Credential handling through chat or command-line arguments can expose AK, SK, or security token values. <br>
Mitigation: Prefer environment variables or a managed secrets mechanism, avoid placing real credentials in conversation or command history, use temporary credentials where possible, and rotate keys regularly. <br>
Risk: Weak scoping of regions, instances, or permissions can cause scripts to run against unintended infrastructure. <br>
Mitigation: Constrain IAM permissions to the documented COC actions, limit allowed regions and instances operationally, and test scripts on a single non-production instance before batch execution. <br>


## Reference(s): <br>
- [IAM Policy Configuration](references/iam-policies.md) <br>
- [Project Dependencies Configuration](scripts/pyproject.toml) <br>
- [Huawei Cloud COC SDK package](https://pypi.org/project/huaweicloudsdkcoc/) <br>
- [ClawHub skill page](https://clawhub.ai/huaweiclouddev/huawei-cloud-flexus-l-server-scripts-excute) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Huawei Cloud COC credentials and may return script IDs, execution task IDs, status text, and error details.] <br>

## Skill Version(s): <br>
0.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
