## Description: <br>
Runs a lightweight operational and security health check for an OpenClaw deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[X-RayLuan](https://clawhub.ai/user/X-RayLuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect OpenClaw runtime health, gateway reachability, listener exposure, configuration hygiene, browser attach surfaces, and recent runtime errors before wider rollout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The healthcheck output may expose local paths, listener details, status output, or recent log snippets. <br>
Mitigation: Review and redact the generated JSON before sharing it outside the intended operator group. <br>
Risk: A PASS verdict is only a lightweight operational signal and does not prove the deployment is secure. <br>
Mitigation: Use the result as a triage input and perform separate host, network, firewall, secret, backup, and threat-model reviews for internet-exposed systems. <br>
Risk: The script reads local OpenClaw configuration and logs from the machine where it runs. <br>
Mitigation: Install and run it only on the OpenClaw machine or workspace that the operator intends to inspect. <br>


## Reference(s): <br>
- [OpenClaw Healthcheck Checklist](references/checklist.md) <br>
- [ClawHub skill page](https://clawhub.ai/X-RayLuan/openclaw-healthcheck) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [JSON healthcheck report with findings, recommendations, evidence, score, and verdict.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local paths, listener details, status output, and recent log snippets that should be reviewed before sharing.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
