## Description:

Build a second brain that AI can understand and maintain through decision logging, periodic reviews, routing rules, task tracking, execution monitoring, decision follow-up, and memory distillation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daowuu](https://clawhub.ai/user/daowuu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, knowledge workers, professionals, and teams use this skill to set up and maintain a personal operating system for decisions, tasks, reviews, routing, and reusable knowledge with help from an AI collaborator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an AI collaborator to continuously read and update a personal knowledge base, which can expose private context or create unwanted changes.

Mitigation: Confine the AI to a dedicated personal-os workspace, avoid secrets and highly sensitive personal data, and require diffs or confirmation before writes.

Risk: Periodic maintenance or review generation with broad filesystem access could update files outside the intended workspace.

Mitigation: Do not enable cron-style maintenance with broad filesystem access; keep automated reviews scoped to the personal-os directory.

Risk: The release security verdict is suspicious because approval, privacy, and rollback safeguards are not clearly defined in the artifact.

Mitigation: Use version control or backups and review generated changes before accepting them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daowuu/skills/personal-os-framework)
- [Project Homepage](https://clawhub.ai)
- [README](artifact/README.md)
- [Overview](artifact/docs/overview.md)
- [Setup Guide](artifact/docs/setup.md)
- [AI Collaboration Prompts](artifact/docs/prompts.md)
- [Templates](artifact/template_docs/README.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration, Text]

**Output Format:** [Markdown guidance, templates, and reusable prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; expected outputs include personal-os file structures, decision logs, reviews, routing notes, task updates, and knowledge-entry templates.]

## Skill Version(s):

0.3.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
