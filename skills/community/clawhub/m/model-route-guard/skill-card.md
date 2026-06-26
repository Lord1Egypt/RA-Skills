## Description: <br>
Diagnose and fix model routing conflicts. Ensure primary model uses correct provider endpoint without duplicate overrides. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dalomeve](https://clawhub.ai/user/Dalomeve) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to audit Bailian model routing, align provider endpoint configuration, remove conflicting agent overrides, and verify model calls after gateway restarts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The repair workflow can permanently modify OpenClaw routing configuration and delete an agent models.json override. <br>
Mitigation: Back up both OpenClaw configuration files before applying fixes and manually confirm whether deleting the agent override would remove intentional routing. <br>
Risk: Using the wrong provider endpoint can keep model calls routed to an incorrect or unsupported service. <br>
Mitigation: Confirm that coding.dashscope.aliyuncs.com is the correct endpoint for the account and region before writing it to configuration. <br>


## Reference(s): <br>
- [Model Route Guard on ClawHub](https://clawhub.ai/Dalomeve/model-route-guard) <br>
- [Privacy Checklist](references/privacy-checklist.md) <br>
- [DashScope Coding Endpoint](https://coding.dashscope.aliyuncs.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes audit, repair, verification, and privacy checklist guidance for local OpenClaw configuration files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
