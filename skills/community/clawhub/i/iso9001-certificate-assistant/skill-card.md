## Description:

ISO 9001:2015 Quality Management System Certification Assistant - Parse client documents, perform gap analysis, and auto-generate compliant documents (Chinese/English bilingual)

This skill is ready for commercial/non-commercial use.

## Publisher:

[kooui](https://clawhub.ai/user/kooui)

### License/Terms of Use:

MIT-0

## Use Case:

External consultants, quality teams, and implementation staff use this skill to parse ISO 9001-related Word documents, analyze gaps against ISO 9001:2015 expectations, and generate bilingual quality management system document drafts for technical service companies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The document-generation workflow can overwrite arbitrary writable files if an unsafe output path is supplied.

Mitigation: Review before installing in environments with important writable files, write outputs to a dedicated folder, avoid absolute or traversal paths, and confirm files are not being overwritten.

Risk: Uploaded quality management documents may contain confidential company data or personal information.

Mitigation: Use the skill only on intended documents and redact unnecessary confidential or personal information before processing.

## Reference(s):

- [ISO 9001 Framework Data](artifact/knowledge/iso9001_framework.json)
- [Generic QMS Templates](artifact/knowledge/generic_templates.json)
- [ClawHub Skill Page](https://clawhub.ai/kooui/skills/iso9001-certificate-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON analysis outputs, and generated document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write parsed document structures, gap reports, and generated QMS document drafts to user-specified paths.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact body lists 2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
