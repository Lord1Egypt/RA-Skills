## Description: <br>
Reviews Prometheus instrumentation in Go code for proper metric types, labels, and patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code reviewers use this skill to review Go services that use prometheus/client_golang metrics, with attention to metric semantics, label cardinality, naming, histogram buckets, registration lifecycle, and /metrics exposure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review comments could be misleading if Prometheus findings are made without checking the concrete files, labels, and metric registration lifecycle. <br>
Mitigation: Require findings to cite the reviewed file or symbol, explain the failed label cardinality or registration gate, and tie the concern to observed code before acting on the recommendation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown review guidance with checklist items and Go code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; it does not run commands or access external services.] <br>

## Skill Version(s): <br>
2.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
