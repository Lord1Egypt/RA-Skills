## Description: <br>
Get all CI/CD flows from Open-C3 platform. Returns the complete list of flows in the system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijinfeng2011](https://clawhub.ai/user/lijinfeng2011) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to inventory CI/CD flows configured in an Open-C3 deployment, including flow counts, service tree grouping, and source addresses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Open-C3 app name and app key that can list CI/CD flows. <br>
Mitigation: Keep config.env private, restrict file permissions, and use a read-only or least-privilege app key when available. <br>
Risk: The generated flow inventory can expose sensitive infrastructure and pipeline metadata. <br>
Mitigation: Run the skill only against trusted Open-C3 instances and treat the output as sensitive operational information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lijinfeng2011/openc3-flow) <br>
- [Publisher profile](https://clawhub.ai/user/lijinfeng2011) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown table with summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, Open-C3 URL, app name, and app key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
