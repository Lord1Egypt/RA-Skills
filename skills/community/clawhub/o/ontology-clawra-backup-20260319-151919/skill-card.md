## Description:

Ontology Clawra Backup 20260319 151919 provides a Chinese-language ontology and rule-based reasoning workflow for structured knowledge-graph analysis, confidence labeling, and guarded local memory updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-xiaochen](https://clawhub.ai/user/wu-xiaochen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers can use this skill to guide Chinese-language ontology-backed reasoning when they need documented assumptions, confidence labels, and optional local ontology updates after confirmation. The bundled ontology examples focus on gas regulator box selection and household combustible gas detector selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tries to control all reasoning tasks, which can over-constrain unrelated work.

Mitigation: Use it only for workflows that explicitly need this Chinese-language ontology method, and keep normal task instructions in control for unrelated work.

Risk: The skill can persist conclusions into local ontology memory with unclear consent boundaries.

Mitigation: Keep automatic learning disabled and require an explicit preview plus user confirmation before each write.

Risk: Private reasoning records or ordinary conversations could be captured if the skill is used too broadly.

Mitigation: Do not automatically record ordinary conversations, and do not sync private reasoning records to GitHub, ClawHub, or other external services.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wu-xiaochen/skills/ontology-clawra-backup-20260319-151919)
- [SKILL.md](artifact/SKILL.md)
- [Laws Ontology Data](artifact/laws.yaml)
- [Rules Ontology Data](artifact/rules.yaml)
- [Detector Laws Ontology Data](artifact/laws_detector.yaml)
- [Detector Rules Ontology Data](artifact/rules_detector.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with confidence labels, structured reasoning steps, YAML examples, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local ontology-memory writes only after preview and explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
