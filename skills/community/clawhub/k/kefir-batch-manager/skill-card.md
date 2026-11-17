## Description:

Comprehensive kefir batch management system with cycle tracking, intelligent reminders, grain health monitoring, and recipe management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[p-salmon](https://clawhub.ai/user/p-salmon)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage kefir fermentation cycles, calculate ingredient ratios, track grain health, maintain batch records, and consult recipe and troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The described reminder and dashboard capabilities are broader than the lightweight local scripts in the artifact.

Mitigation: Treat the release as a local batch tracker and ratio calculator unless reminder or dashboard workflows are separately verified.

Risk: Local batch records may be written to kefir_batches.json.

Mitigation: Review stored notes and photo paths before sharing the artifact, and avoid recording sensitive personal information.

Risk: Sealed second fermentation and bottle conditioning can create pressure-related handling risk.

Mitigation: Use pressure-rated bottles, monitor carbonation, refrigerate before opening, and open bottles away from the face.

## Reference(s):

- [Recipes Database](references/recipes_database.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/p-salmon/skills/kefir-batch-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON batch records and Python script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local batch data to kefir_batches.json when the bundled tracker script is used.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
