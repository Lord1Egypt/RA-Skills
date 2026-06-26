## Description: <br>
Scores logistics suppliers and Cainiao station operators, assigns risk levels, diagnoses key issues, and recommends follow-up actions from operational metrics and compliance records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Internal control, supplier management, and operations teams use this skill to turn supplier or station KPI data, complaint history, and violation records into a structured risk scoring report for review and follow-up. <br>

### Deployment Geography for Use: <br>
China-focused Cainiao logistics and station operations <br>

## Known Risks and Mitigations: <br>
Risk: Users may paste raw sensitive business or customer details while providing complaint records, KPI reports, or case narratives. <br>
Mitigation: Use aggregated metrics, redact customer identifiers and narratives, and avoid leaked records, contact details, addresses, credentials, or confidential complaint files unless an approved handling process exists. <br>
Risk: The score can be misleading when inputs are incomplete, self-reported, or conflict with platform data. <br>
Mitigation: Treat the score as an aid to human review, label missing data as gaps, prefer platform data over self-reported data, and manually review one-vote veto cases before action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nic-yuan/inter-control-02-risk-scoring) <br>
- [Continuation reference](references/continuation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown risk scoring report with score tables, issue diagnosis, recommendations, warnings, and review cadence.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask up to five clarifying data questions before scoring; marks missing inputs as data gaps.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.7.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
