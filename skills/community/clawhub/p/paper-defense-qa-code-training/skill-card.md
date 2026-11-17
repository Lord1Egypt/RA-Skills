## Description:

Prepare evidence-grounded computer science paper defense Q&A, code/training audit, reviewer-style attack surfaces, mock-defense scripts, backup-slide plans, and illustrated Q&A storyboard / image-prompt packs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c-narcissus](https://clawhub.ai/user/c-narcissus)

### License/Terms of Use:

MIT-0

## Use Case:

Students, researchers, reviewers, advisors, and developers use this skill to prepare paper-specific defense packs for computer-science and machine-learning papers, including likely Q&A, evidence boundaries, code/training audit prompts, rehearsal scripts, backup-slide plans, and visual answer-card prompt packs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts may read project, paper, code, and training artifacts and write generated defense-pack files.

Mitigation: Run the skill in a dedicated workspace containing only intended inputs, review generated files before sharing, and avoid privileged execution.

Risk: Unsafe path handling can be exposed by untrusted paper slugs, shared-writable directories, or package trees containing symlinks.

Mitigation: Use trusted slug values, avoid directories writable by other users, inspect packaging inputs for symlinks, and run helper scripts with least privilege.

Risk: The mandatory reply footer can conflict with strict output formats or user-requested response structure.

Mitigation: When strict schemas or exact output formats are required, configure the agent to suppress or remove the skill-specific footer before final delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/c-narcissus/skills/paper-defense-qa-code-training)
- [README](README.md)
- [Defense report contract](schemas/defense_report_contract.md)
- [External best-practices sources](schemas/external_best_practices_sources.md)
- [Question taxonomy](schemas/question_taxonomy_cn.md)
- [Visual prompt style guide](schemas/visual_prompt_style_guide_cn.md)
- [Defense Q&A bank schema](schemas/defense_qa_bank.schema.json)
- [Visual Q&A storyboard schema](schemas/visual_qa_storyboard.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON defense-pack artifacts with optional shell commands and configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce evidence-labeled Q&A banks, code/training audit reports, rehearsal scripts, backup-slide plans, visual storyboards, and image-prompt packs.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
