# Setup — NextJS

Read this when no `~/Clawic/data/nextjs/memory.md` exists. Its job is to establish project context and write the initial memory file.

## Operating stance

Apply the Core Rules from `SKILL.md`. Prefer inferring context from the codebase over asking; ask only when a decision genuinely depends on the answer.

## Establish context

Infer as much as possible from the project before asking anything:

- **Version and router** — read `package.json` for the `next` version; check for `app/` vs `pages/`.
- **Stack** — TypeScript, ORM (Prisma/Drizzle), auth library, styling — read the dependencies and config files.
- **Deployment target** — look for `vercel.json`, `Dockerfile`, or `output` in `next.config.*`.

Record what you cannot infer as `Configuration` variables (see `SKILL.md`) with their defaults, and update them when the user states a preference. Do not interrogate the user for units, schedule, goals, or conventions up front — capture preferences as they surface during real work.

## What to save

Write to `~/Clawic/data/nextjs/memory.md`:

- Next.js version and router type
- Key dependencies (Prisma, Auth.js, etc.)
- Deployment target
- Any `Configuration` variables the user has set away from their defaults
- Explicit conventions the user has stated
- How proactive the user wants you to be (default: flag caching/boundary/performance issues; adjust on request)

For project-specific patterns, use `~/Clawic/data/nextjs/projects/{name}.md`.

## When done

Once the stack and integration preferences are recorded in memory, setup is complete. Remaining preferences accrue through ongoing work.
