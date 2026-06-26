## Description: <br>
Predict depletion time of critical lab reagents based on historical usage frequency, and automatically generate purchase alerts when stock falls below safety thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Lab staff, researchers, and operations teams use this skill to track reagent stock, estimate depletion dates from usage records, and generate purchase or safety-stock alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that the code does not enforce the workspace path limits promised by the documentation. <br>
Mitigation: Use the default data path, avoid custom paths, and do not rely on documented workspace-only path protection until the publisher adds real path validation. <br>
Risk: Sparse usage history can make depletion predictions unreliable. <br>
Mitigation: Treat LOW_CONFIDENCE predictions as advisory and collect additional usage records before relying on purchase timing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/lab-inventory-predictor) <br>
- [Publisher Profile](https://clawhub.ai/user/aipoch-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, CSV, shell commands, guidance] <br>
**Output Format:** [Structured Markdown responses with optional JSON or CSV inventory reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local lab inventory data and reports assumptions, limits, risks, and next checks when relevant.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
