## Description: <br>
Provides monitoring and alerting for agent abnormal behavior metrics with Prometheus and Grafana support, including P99 latency, error rates, anomaly detection, and custom alert rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to instrument agent behavior, track latency percentiles and error rates, generate Prometheus metrics, create Grafana dashboard configuration, and define alerts for abnormal behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Metric labels or error types can expose sensitive tokens, raw prompts, or personal data if callers pass them into monitoring fields. <br>
Mitigation: Use stable low-cardinality labels and scrub secrets, personal data, and raw prompts before recording metrics. <br>
Risk: The Grafana dashboard example writes a local JSON file and could overwrite or place files in an unintended location if copied without review. <br>
Mitigation: Choose and review the output path before writing dashboard files, especially in shared or automated environments. <br>
Risk: Publisher provenance is unavailable for this release. <br>
Mitigation: Review the source artifact and publisher profile if provenance or supply-chain assurance is required before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-agent-metrics-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, configuration, guidance] <br>
**Output Format:** [JavaScript API objects, Prometheus exposition text, Grafana dashboard JSON, and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Keeps metrics in local in-memory collectors and can export dashboard configuration for external provisioning.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
