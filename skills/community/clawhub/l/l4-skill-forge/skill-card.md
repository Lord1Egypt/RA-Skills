## Description:

Designs and produces publishable L4 Agent Skills for creating skills from scratch, refactoring existing skills, performing security reviews, and establishing evaluation and release workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reffwu](https://clawhub.ai/user/reffwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to design, scaffold, review, evaluate, and package Agent Skills to a production-oriented L4 standard. It is especially suited for users who need structured onboarding, safety gates, templates, checklists, and evaluation cases for reusable skill releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or modified skills may include incorrect, incomplete, or organization-inappropriate guidance.

Mitigation: Review generated skill files, templates, checklists, and eval cases before publishing or using them in team workflows.

Risk: The skill can guide an agent through file creation or modification and includes optional local Node.js helper scripts.

Mitigation: Inspect proposed file changes and script commands before execution, especially when working in production or shared repositories.

Risk: High-impact actions such as deletion, deployment, external sending, or production data writes could cause harm if confirmation gates are removed.

Mitigation: Preserve explicit approval gates for high-impact actions and run the bundled release checklist before release.

Risk: Most bundled guidance is written in Chinese, which may lead to misunderstandings for reviewers who do not read Chinese.

Mitigation: Use a qualified reviewer or translation workflow before relying on the skill in non-Chinese-speaking teams.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/reffwu/skills/l4-skill-forge)
- [L4 Standard](references/l4-standard.md)
- [Onboarding Zero to One](references/onboarding-zero-to-one.md)
- [Behavioral Testing](references/behavioral-testing.md)
- [CSO Guide](references/cso-guide.md)
- [Benchmark vs Official](references/benchmark-vs-official.md)
- [Skill Blueprint Template](assets/templates/skill-blueprint.md)
- [Release Checklist](assets/checklists/release-checklist.md)
- [Eval Cases](assets/evals/eval-cases.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated skill files, templates, checklists, eval cases, and optional JSON score reports from local helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Most guidance and bundled templates are written in Chinese; helper scripts are local Node.js commands for scaffolding and scoring skill directories.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
