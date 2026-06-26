## Description: <br>
Build a concise incident dossier from operational logs, audits, JSON/JSONL files, and state snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neo1307](https://clawhub.ai/user/neo1307) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and incident responders use this skill to turn operational evidence into a structured incident report with a summary, blast radius, timeline, hypotheses, recovery status, and recommended next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper reads local evidence files selected by the user. <br>
Mitigation: Provide only the evidence files intended for analysis and avoid including unrelated sensitive material. <br>
Risk: The helper writes or overwrites the specified Markdown output path. <br>
Mitigation: Choose a non-critical output path and review the target path before running the command. <br>
Risk: Generated dossiers may include local file paths and operational details. <br>
Mitigation: Review and redact the dossier before sharing it outside the response team. <br>


## Reference(s): <br>
- [Incident Dossier on ClawHub](https://clawhub.ai/neo1307/incident-dossier) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown incident dossier with a concise timeline and evidence-based recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or overwrite a user-specified Markdown output file when the helper script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
