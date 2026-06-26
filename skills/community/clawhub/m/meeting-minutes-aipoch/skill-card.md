## Description: <br>
Structures medical meeting transcripts into formal minutes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users can use this skill to turn provided medical, clinical, research, or administrative meeting transcripts into structured minutes. It focuses the workflow on explicit inputs, stated assumptions, action items, decisions, and bounded output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting transcripts and generated minutes may contain sensitive medical, research, or confidential workspace information. <br>
Mitigation: Use the skill only with intended meeting-minutes inputs, keep transcript files within approved workspace controls, and review generated minutes before sharing. <br>
Risk: The scanner notes overly broad routing language, which could lead an agent to apply the skill outside its intended transcript-to-minutes workflow. <br>
Mitigation: Invoke the skill explicitly for meeting-minutes work and stop when required inputs, scope, or acceptance criteria are missing. <br>


## Reference(s): <br>
- [Meeting Minutes References](references/guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Structured Markdown response and JSON object when running scripts/main.py] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a transcript input; meeting_type is optional and defaults to clinical.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
