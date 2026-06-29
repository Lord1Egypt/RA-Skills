## Description: <br>
Triage a performance regression from concrete evidence - latency percentiles, error rate, resource and DB metrics, recent deploys - separate symptoms from hypotheses, and recommend one measurement before one fix. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ritual](https://clawhub.ai/user/ritual) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to investigate performance regressions from concrete operational evidence, rank likely causes, choose the first measurement to run, and identify the smallest likely fix with verification criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Performance diagnoses may misattribute a regression when evidence is incomplete. <br>
Mitigation: Review the proposed cause against measurements, logs, and benchmark results before applying remediation steps. <br>
Risk: Optional Ritual Cloud use can add external workspace discovery or team workflows. <br>
Mitigation: Review the npm package and connect Ritual Cloud only when that external context is desired. <br>
Risk: Optional knowledge capture can write a reusable note into the repository. <br>
Mitigation: Approve knowledge-note file writes only when the proposed note is useful and accurately cites the supporting evidence. <br>


## Reference(s): <br>
- [Ritual](https://ritual.work) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with ranked hypotheses, measurement guidance, fix recommendations, optional commands, and verification criteria] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
