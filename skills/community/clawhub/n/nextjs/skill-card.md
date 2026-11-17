## Description:

Builds Next.js apps with App Router, including server components, caching, Server Actions, authentication, deployment, routing, and data-fetching guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, debug, harden, and deploy Next.js App Router applications. It helps with common routing, rendering, caching, authentication, Server Actions, and deployment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store local Next.js project context under ~/Clawic/data/nextjs/.

Mitigation: Review what the agent writes to local memory and avoid storing secrets or sensitive project details there.

Risk: Authentication setup guidance includes a beta NextAuth/Auth.js dependency path.

Mitigation: Pin and review authentication package versions before applying generated install or setup commands.

Risk: Middleware-only authorization can leave protected data paths exposed.

Mitigation: Enforce authorization in Server Actions, route handlers, and data-access functions, not only in middleware.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/nextjs)
- [Clawic NextJS skill page](https://clawic.com/skills/nextjs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local project memory under ~/Clawic/data/nextjs/ when used by an agent.]

## Skill Version(s):

1.1.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
