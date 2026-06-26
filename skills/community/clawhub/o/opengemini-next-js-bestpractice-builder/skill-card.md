## Description: <br>
Builds and documents solo-developer SaaS projects with a fixed Next.js App Router, Tailwind, Prisma 6, Neon PostgreSQL, Clerk, Stripe, and Vercel stack, using FastAPI only when Python workloads require it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hiromps](https://clawhub.ai/user/hiromps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external builders use this skill to define, scaffold, and document a solo SaaS project with a fixed Next.js-centered stack and implementation policies before coding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create project structure, GEMINI.md, docs, and project-level skills that may become local policy for an agent workflow. <br>
Mitigation: Run the scripts in a new or backed-up project directory and review generated GEMINI.md, docs, and skills before relying on them. <br>
Risk: Gemini CLI document generation sends the project brief to Gemini, which could expose sensitive product, customer, or secret information if included. <br>
Mitigation: Do not include secrets, credentials, or sensitive customer data in project briefs passed to Gemini CLI. <br>
Risk: The skill is intentionally opinionated around a fixed Next.js and Gemini SaaS workflow, which may be unsuitable for projects that need a different architecture. <br>
Mitigation: Use it only when the fixed stack and workflow match the project, and verify deployment, database, and integration assumptions before implementation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hiromps/opengemini-next-js-bestpractice-builder) <br>
- [Doc Templates](references/doc-templates.md) <br>
- [Integration Rules](references/integration-rules.md) <br>
- [Project Bootstrap Checklist](references/project-bootstrap-checklist.md) <br>
- [Project Skill Template](references/project-skill-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, shell commands, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local directories, GEMINI.md, docs, project-level skills, Prisma and FastAPI placeholders, and implementation plans.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
