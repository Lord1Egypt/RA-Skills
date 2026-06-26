## Description: <br>
OnlyBaby analyzes contraction and baby log JSON files to summarize labour timing, feeding, and diaper patterns with safety-oriented verdicts and care-seeking caveats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jacklandrin](https://clawhub.ai/user/jacklandrin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Caregivers or birth partners use this skill to turn contraction logs and newborn feeding and diaper logs into a scannable status report. It helps organize observations for monitoring and discussion with a midwife, OB, paediatrician, or emergency services when concerns arise. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pregnancy and newborn health summaries can be mistaken for diagnosis or reassurance. <br>
Mitigation: Use the output as an informational log summary only, and contact a midwife, OB, paediatrician, or emergency services for worrying symptoms, uncertainty, or urgent concerns. <br>
Risk: The skill needs access to contraction and baby log JSON files that may contain sensitive family health information. <br>
Mitigation: Share only the specific files needed for the summary and review the generated report before storing or forwarding it. <br>


## Reference(s): <br>
- [Data Schemas and Health/Safety Thresholds](references/schemas-and-thresholds.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with headings, bullets, verdicts, supporting statistics, and a medical-advice caveat] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summarizes user-provided local JSON logs; does not diagnose medical conditions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
