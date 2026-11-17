## Description:

Converts user-provided images into validated, decision-ready action drafts across domains such as events, meal photos, places, products, receipts, documents, and civic issues, with reverse image search support via Yandex and Google.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use Look to turn user-provided images into validated action drafts for events, meals, places, products, receipts, documents, and civic reports. It is intended for image-to-action workflows, not generic OCR, computer vision research, surveillance, or image generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images or image metadata may be uploaded to third-party services for reverse image search.

Mitigation: Require explicit confirmation before public image uploads and disable reverse search where that data sharing is not acceptable.

Risk: The skill declares a silent daily self-update path.

Mitigation: Disable or remove the cron/self-update path, pin a reviewed release, and review updates before deployment.

Risk: The skill has documented false-trigger risk outside image-to-action workflows.

Mitigation: Load it only for user-provided images intended to become action drafts, not for general OCR or image analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/indigokarasu/skills/ocas-look)
- [README](README.md)
- [Skill definition](SKILL.md)
- [Look Core Workflow](references/workflow.md)
- [Look Domain Playbooks](references/domain_playbooks.md)
- [Look Schemas](references/schemas.md)
- [Look Decision Policy](references/decision_policy.md)
- [Reverse Image Search Reference](references/google-image-source-search.md)
- [Credential Files Reference](references/credential-files.md)
- [Self-Update Procedure](references/self_update.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries with structured JSON action drafts, decision records, execution receipts, and journal records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-first workflow; high-risk actions require explicit confirmation before execution.]

## Skill Version(s):

2.3.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
