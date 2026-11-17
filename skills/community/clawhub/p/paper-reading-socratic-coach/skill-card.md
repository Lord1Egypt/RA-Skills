## Description:

Use when the user wants to train independent academic paper reading, scientific thinking, and research methodology through diagnostic questioning, precision reports, and persistent learning-state tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c-narcissus](https://clawhub.ai/user/c-narcissus)

### License/Terms of Use:

MIT-0

## Use Case:

Students, researchers, and research teams use this skill to turn an academic paper into a diagnostic training session. It helps users practice paper-grounded reconstruction, scientific reasoning, methodology critique, and follow-up research thinking through adaptive questions and persistent progress tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save local Markdown notes about paper-reading performance, weaknesses, and session history in the workspace.

Mitigation: Use it only in workspaces where those learning records are appropriate, and review or delete `.paper-reading-coach/` files in shared, synced, or sensitive environments.

Risk: The coaching workflow can quote or paraphrase paper evidence while diagnosing answers, so users may mistake diagnostic feedback for a complete paper substitute.

Mitigation: Keep the workflow focused on paper-grounded questioning and require the learner to reconstruct evidence before moving to critique or frontier questions.

## Reference(s):

- [Skill README](artifact/README.md)
- [Precision Dimensions](artifact/rubrics/precision_dimensions.md)
- [Weakness Taxonomy](artifact/rubrics/weakness_taxonomy.md)
- [Precision Report Template](artifact/templates/precision_report_template.md)
- [Learning State Template](artifact/templates/learning_state_template.md)
- [Session Log Template](artifact/templates/session_log_template.md)
- [ClawHub Skill Page](https://clawhub.ai/c-narcissus/skills/paper-reading-socratic-coach)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown with structured diagnostic reports, question prompts, feedback blocks, and learning-state updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local Markdown learning records and session logs under .paper-reading-coach/ when file-writing tools are available.]

## Skill Version(s):

1.0.0 (source: frontmatter, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
