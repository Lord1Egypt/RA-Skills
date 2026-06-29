## Description: <br>
Helps agents evaluate KPI and incentive systems for Goodhart's Law risks by identifying proxy gaps, gaming vectors, failure mechanisms, and countermeasures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to test whether a metric, KPI, ranking, audit, or algorithmic objective is likely to distort behavior. It guides the agent to name the underlying goal, predict gaming vectors, classify the Goodhart mechanism, and propose multi-metric, audit, rotation, and retirement controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Historical examples and citations may be stale, incomplete, or contested if used for factual or high-stakes decisions. <br>
Mitigation: Verify cited cases and sources before relying on them for legal, policy, financial, medical, or other high-stakes decisions. <br>
Risk: Metric design recommendations can affect incentives, evaluations, and resource allocation. <br>
Mitigation: Have accountable domain owners review proposed metrics, audits, thresholds, and retirement criteria before deployment. <br>


## Reference(s): <br>
- [Sources - goodharts-law](references/sources.md) <br>
- [Method in Action: Goodhart 1975 (M3) and Strathern 1997 (RAE)](examples/goodhart-1975-m3-and-strathern-1997-rae.md) <br>
- [ClawHub skill page](https://clawhub.ai/deciqai/skills/goodharts-law) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown decision framework with structured fields and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Goodhart-robust metric design analysis; does not run code or modify systems.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
