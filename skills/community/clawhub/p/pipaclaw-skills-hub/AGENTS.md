# Repository Rules

This repository is the public release boundary for `pipaclaw-skills-hub`.

## Scope

- Keep only publishable skill packages in this repo.
- Each public skill package may contain only:
  - `SKILL.md`
  - `agents/`
  - `references/`
  - optional lightweight public helper scripts such as `scripts/*.sh`
  - optional public assets that are safe to release

## Do Not Add

- backend services
- backend implementation code
- local test harnesses
- generated artifacts
- customer data
- private prompts
- reverse-engineered platform material
- `node_modules`, build output, or temporary files

## Product Rule

- Social account operations are exposed through one public skill only: `social-account-ops`.
- Do not reintroduce separate public packages for diagnosis, planning, writing, or retro.
- If the social ops workflow becomes more complex, keep the complexity inside the single skill or its references.

## Editing Rule

- Treat `skills/README.md` as the GitHub repository homepage.
- Keep `SKILL.md` concise and move detailed playbooks into `references/`.
- Keep helper scripts thin transport wrappers only. Do not move backend logic into this repo.
- Preserve public-safe wording and avoid leaking implementation details from private backends.
