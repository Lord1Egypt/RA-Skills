## Description: <br>
Runs controlled end-to-end workload pressure tests on Huawei Cloud CCE using k6 traffic generation, ELB and AOM observability, elasticity evaluation, and bilingual report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud platform engineers use this skill to plan, preview, run, and report controlled load tests for Huawei Cloud CCE workloads. It helps validate traffic paths, latency, success rate, pod resource usage, and elasticity behavior during approved test windows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad Huawei Cloud and Kubernetes authority. <br>
Mitigation: Install only in a controlled operator environment with least-privilege Huawei Cloud and Kubernetes credentials, human approval, and audit logging. <br>
Risk: Credentials, cluster inventory, logs, and raw outputs may contain sensitive operational data. <br>
Mitigation: Treat outputs as sensitive, avoid raw exports unless needed, and never expose or persist AK/SK values. <br>
Risk: Traffic generation, ELB creation, Service or Ingress changes, and scaling can affect live workloads or incur cost. <br>
Mitigation: Preview mutating actions first, require explicit approval with confirm=true, start with low traffic, and use approved test windows for production paths. <br>
Risk: Exposing cluster APIs or changing replicas can create operational or availability impact. <br>
Mitigation: Review any action that exposes cluster APIs or changes replicas, keep rollback steps available, and stop increasing traffic when latency, success rate, or resource waterlines degrade. <br>


## Reference(s): <br>
- [Pressure-Test Workflow](references/workflow.md) <br>
- [Pressure-Test Risk Rules](references/risk-rules.md) <br>
- [Pressure-Test Output Schema](references/output-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON action results, Markdown and HTML reports, SVG curves, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual reports and optional observability artifacts when output paths are provided.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
