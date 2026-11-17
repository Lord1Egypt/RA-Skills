## Description:

Build and document a solo-developer SaaS project using a fixed Next.js, Tailwind, Prisma, and Neon PostgreSQL stack, with FastAPI only for Python-required workloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hiromps](https://clawhub.ai/user/hiromps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and solo founders use this skill to plan, scaffold, and document SaaS projects with a prescribed Next.js App Router stack. It helps produce project guidance, docs, scaffold structure, and integration plans before implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scripts can overwrite project guidance, documentation, and project-level skill files.

Mitigation: Run the skill in a new or version-controlled project, review diffs before keeping generated files, and keep backups when applying it to an existing project.

Risk: The project brief may be sent to Gemini CLI during documentation generation.

Mitigation: Remove secrets, credentials, customer data, and other sensitive information from the brief before running generation commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hiromps/skills/opengemini-next-js-bestpractice-builder)
- [Doc Templates](references/doc-templates.md)
- [Integration Rules](references/integration-rules.md)
- [Project Bootstrap Checklist](references/project-bootstrap-checklist.md)
- [Project Skill Template](references/project-skill-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, shell scripts, directory scaffolds, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use Gemini CLI to generate project documentation from a project brief; scripts can create or overwrite project guidance and documentation in the target project.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
