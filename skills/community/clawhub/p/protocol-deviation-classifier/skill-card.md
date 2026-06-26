## Description: <br>
Classifies clinical trial protocol deviation descriptions as major, minor, or critical by assessing subject safety, data integrity, and scientific validity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ewankeynes](https://clawhub.ai/user/ewankeynes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical trial quality, regulatory, and development teams use this skill to classify protocol deviation events, generate rationale and recommended actions, and prepare deviation reports for qualified QA review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clinical trial deviation classifications may be mistaken for final regulatory or QA determinations. <br>
Mitigation: Use outputs as decision support and require qualified clinical QA or regulatory staff to review and confirm classifications. <br>
Risk: Input or output files may include patient, subject, or site identifiers. <br>
Mitigation: Avoid unnecessary identifiers in inputs and handle local files according to applicable clinical data handling procedures. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ewankeynes/protocol-deviation-classifier) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ewankeynes) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON results, markdown-style reports, Python API snippets, and CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces decision-support classifications with confidence scores, rationale, regulatory basis, recommended actions, and batch report data.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
