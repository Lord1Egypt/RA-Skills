## Description:

LQS Skill is a prompt-, schema-, and template-driven artifact generator for the LQS codebase that guides manual generation of RequirementDraft, Spec, RenderPlan, Preview Diff, and ChangeReport outputs without automatically executing code, migrations, or document fetches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fantasy0102](https://clawhub.ai/user/fantasy0102)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn free-text requirements or manually supplied document text into reviewed LQS Admin module artifacts. It supports human-in-the-loop CRUD scaffolding by producing structured requirements, specs, render plans, dry-run diffs, and approved change reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated PHP, SQL migration, and template changes could be written with under-scoped authority.

Mitigation: Require explicit per-file approval, review generated content before writing, and keep dry-run diff preview as the default review step.

Risk: Generated target paths could escape intended project locations.

Mitigation: Allow only canonical in-repository paths and reject absolute paths or parent-directory traversal before any write.

Risk: Migration output may contain incorrect rollback behavior or unsafe schema assumptions.

Mitigation: Review migration up and down behavior manually and do not execute migrations automatically.

Risk: Session-derived patterns could become trusted project context without adequate review.

Mitigation: Require maintainer review before persisting new patterns or treating inferred project context as reusable evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fantasy0102/skills/lqs-skill)
- [Publisher profile](https://clawhub.ai/user/fantasy0102)
- [Quickstart](artifact/quickstart.md)
- [Implementation specification](artifact/skill_spec.md)
- [Implementation runbook](artifact/implementation_runbook.md)
- [MVP delivery checklist](artifact/mvp_delivery_checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [JSON, Markdown guidance, generated source text, and unified diff previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for dry-run review first; file writes require explicit approval and should remain limited to canonical in-repository paths.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter says 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
