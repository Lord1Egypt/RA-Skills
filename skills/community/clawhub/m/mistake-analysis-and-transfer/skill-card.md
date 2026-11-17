## Description:

Supports students in organizing mistake records from problem screenshots, test photos, or pasted text by identifying the subject and problem type, analyzing the root cause of the mistake, breaking down the relevant knowledge points, giving consolidation advice, and optionally saving, updating, searching, and reviewing entries in a local mistake notebook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caroljiang150-ai](https://clawhub.ai/user/caroljiang150-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and study assistants use this skill to turn real incorrect answers into structured Chinese mistake records with evidence-based root-cause analysis, core knowledge-point review, and actionable self-check advice. When the user explicitly requests it, the skill can manage a local mistake notebook for saving, updating, listing, showing, and localizing saved entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved mistake records may include private schoolwork, answers, and analysis that persist in the configured local notebook directory.

Mitigation: Install and use the skill only when local mistake-notebook persistence is desired, choose an appropriate workspace or notebook directory, and delete saved entries when they are no longer needed.

Risk: The skill may write notebook files and update the local notebook index when the user explicitly asks to save or update mistakes.

Mitigation: Review the notebook root reported after save, update, or query operations and avoid using shared directories for sensitive student work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caroljiang150-ai/skills/mistake-analysis-and-transfer)
- [Publisher profile](https://clawhub.ai/user/caroljiang150-ai)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance, Shell commands, Files, Configuration]

**Output Format:** [Chinese Markdown mistake records, JSON-backed notebook entries, and local file-management command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Markdown files, an index.jsonl file, and a workspace notebook root only when the user requests notebook operations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
