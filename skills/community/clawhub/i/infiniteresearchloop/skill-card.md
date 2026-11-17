## Description:

Guides an agent through structured research, verification, debugging, Hidden NO detection, and budgeted refinement to produce stable, context-aware answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satoshinclaude](https://clawhub.ai/user/satoshinclaude)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when a task needs deeper research, contradiction checking, uncertainty handling, and controlled refinement before a final answer is delivered.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package advertises a research skill, but the primary runtime SKILL.md describes a broadly triggered skill-creation workflow.

Mitigation: Correct the package so the manifest and SKILL.md describe the same purpose before deployment.

Risk: The runtime trigger can redirect broad modification requests into skill creation or skill updates.

Mitigation: Limit activation to explicit skill-creation or skill-update requests.

Risk: The documented memory layer can preserve reusable lessons and validated insights, which may be inappropriate for sensitive or instruction-like content.

Mitigation: Require clear consent for memory storage and exclude sensitive or instruction-like content.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/satoshinclaude/skills/infiniteresearchloop)
- [Infinite Research + Hidden NO](artifact/Infinite Research + Hidden NO.md)
- [Infinite Research + Hidden NO Skill](artifact/Infinite Research + Hidden NO Skill.md)
- [Budget Management](artifact/budget_management.md)
- [Hidden NO Examples](artifact/hidden_no_examples.md)
- [Master Loop Checklist](artifact/master_loop_checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style response with Result, Key Findings, Remaining Uncertainty, Confidence, Hidden NO Status, and TLDR sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses bounded internal research, debug, refinement, and speculative-assumption loops.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
