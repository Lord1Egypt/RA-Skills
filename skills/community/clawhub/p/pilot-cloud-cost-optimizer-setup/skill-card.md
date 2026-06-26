## Description: <br>
Deploy a cloud cost optimization pipeline with four collaborating agents for scanning resources, analyzing spend, applying approved optimizations, and reporting savings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, FinOps engineers, and cloud operations teams use this skill to set up a distributed pipeline that scans cloud resources, analyzes cost anomalies, routes optimization recommendations, and sends reports through Slack, email, or webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill wires agents that may exchange sensitive cloud-cost and utilization data. <br>
Mitigation: Use test or tightly scoped cloud accounts first, verify peer hostnames before handshakes, and review data retention for Slack, email, and webhook destinations. <br>
Risk: Optimization workflows may trigger resource shutdown, resize, purchase, or scheduling actions without enough documented approval and rollback controls. <br>
Mitigation: Require human approval for cloud-resource changes, inspect dependent Pilot skills, pin versions where possible, and document rollback steps before enabling automated actions. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub skill listing](https://clawhub.ai/teoslayer/pilot-cloud-cost-optimizer-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands and JSON manifest templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces role-specific setup steps for scanner, analyzer, optimizer, and reporter agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter version is 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
