## Description: <br>
Analyze Huawei Cloud CCE capacity trends, forecast resource bottlenecks, simulate elasticity policies, generate charts and reports, compare recurring history records, and recommend HPA or node autoscaler optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations engineers use this skill to assess Huawei Cloud CCE cluster capacity, identify bottleneck risk, simulate scaling policy changes, and produce capacity planning reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The shipped dispatcher exposes broader cloud and Kubernetes operations than the capacity-forecasting description suggests. <br>
Mitigation: Review the full dispatcher surface before installation and treat the skill as a broad cloud operations tool, not only a capacity forecaster. <br>
Risk: The skill requires sensitive Huawei Cloud credentials and can access operational data. <br>
Mitigation: Use least-privilege, temporary credentials where possible and avoid production credentials unless the credential, kubeconfig, log, audit, and infrastructure-change exposure is acceptable. <br>
Risk: Some artifact-described operations can change HPA or nodepool configuration when explicitly confirmed. <br>
Mitigation: Preview changes first, require explicit approval for confirmed operations, and prepare rollback and validation steps before applying changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pintudeyudi/huawei-cloud-cce-capacity-trend-forecaster) <br>
- [Workflow](references/workflow.md) <br>
- [Simulation Rules](references/simulation-rules.md) <br>
- [Output Schema](references/output-schema.md) <br>
- [Huawei Cloud API Explorer](https://support.huaweiicloud.com/apiexplorer/index.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell command examples and generated JSON, Markdown, HTML, and SVG report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce capacity summaries, curve charts, history records, HPA previews, and node autoscaler recommendations.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
