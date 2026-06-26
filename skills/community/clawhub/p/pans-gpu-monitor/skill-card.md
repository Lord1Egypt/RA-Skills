## Description: <br>
A GPU monitoring skill for AI compute sales teams that ingests customer GPU usage data, generates usage and efficiency reports, and identifies cost optimization, anomaly, and capacity planning signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashiming](https://clawhub.ai/user/dashiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and customer success teams use this skill to prepare weekly customer GPU usage reviews, surface efficiency and cost issues, and support renewal or upsell conversations with structured reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Imported customer GPU metrics may be written to the default metrics database even when a user chooses another database path. <br>
Mitigation: Review or fix the import path behavior before using real customer data; until then, avoid confidential datasets, back up the default metrics file, and minimize or anonymize customer identifiers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dashiming/pans-gpu-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/dashiming) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate weekly and monthly GPU usage summaries, anomaly alerts, optimization suggestions, and capacity planning guidance from CSV or JSON metrics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
