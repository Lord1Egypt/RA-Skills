## Description: <br>
Low Altitude Guardian is an advisory emergency decision engine for low-altitude unmanned devices that classifies UAV and eVTOL crisis scenarios and drafts response recommendations using a P0-P4 loss-priority model and weighted scoring. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[aaalenwow](https://clawhub.ai/user/aaalenwow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and safety reviewers use this skill for offline analysis, training, and drafting advisory procedures for low-altitude drone, eVTOL, delivery vehicle, and robotic-device incidents. It supports scenario classification, response-plan comparison, incident reporting, knowledge-base management, and fleet analytics, but does not replace certified flight safety systems or licensed operator decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides flight-emergency procedure recommendations and includes autonomous-action language that could be mistaken for operational control guidance. <br>
Mitigation: Use only for offline analysis, training, or drafting procedures, and require certified safety engineering plus explicit human approval before any operational use. <br>
Risk: Persistent .guardian data and learned templates can preserve incident details or propagate unreviewed procedural changes. <br>
Mitigation: Review stored .guardian data, generated reports, and learned template changes before reuse, sharing, or deployment. <br>
Risk: Security evidence marks the release suspicious because advice-only safety claims are mixed with autonomous flight-procedure content. <br>
Mitigation: Do not connect outputs to live drones, eVTOLs, autopilots, dispatch systems, or automated emergency workflows without independent review controls. <br>


## Reference(s): <br>
- [Crisis Taxonomy](artifact/references/crisis_taxonomy.md) <br>
- [Decision Priority Matrix](artifact/references/decision_priority_matrix.md) <br>
- [ClawHub Release Page](https://clawhub.ai/aaalenwow/low-altitude-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON decision structures, generated report files, configuration templates, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory only; outputs must not be connected to live drones, eVTOLs, autopilots, dispatch systems, or automated emergency workflows without certified safety engineering and explicit human approval gates.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and SKILL.md openclaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
