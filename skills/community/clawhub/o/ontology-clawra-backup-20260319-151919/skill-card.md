## Description: <br>
Provides a structured ontology and rule-based reasoning framework for agent analysis, including confidence labels, user confirmation steps, and local ontology updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-xiaochen](https://clawhub.ai/user/wu-xiaochen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide agent reasoning through ontology lookup, rule matching, explicit assumptions, and user-confirmed local knowledge updates. The bundled rules focus on structured selection and safety checks for gas regulation boxes and household combustible gas detectors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may persist local notes about decisions, preferences, or reasoning records. <br>
Mitigation: Require the agent to preview proposed memory writes and obtain explicit approval before writing anything to local ontology storage. <br>
Risk: The evidence flags inconsistent instructions about local-only behavior and private reasoning records. <br>
Mitigation: Keep network-backed search or external sharing disabled unless the user explicitly approves a specific external action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-xiaochen/ontology-clawra-backup-20260319-151919) <br>
- [Publisher profile](https://clawhub.ai/user/wu-xiaochen) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [laws.yaml](artifact/laws.yaml) <br>
- [rules.yaml](artifact/rules.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown or plain text guidance with structured rule references and confidence labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local ontology changes only after explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
