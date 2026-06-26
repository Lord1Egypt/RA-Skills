# Discovery Interview: Question Bank

Use this bank to select the 5 to 8 most relevant questions for each
engagement. Never ask all of them. Read the user's initial input first,
extract whatever context you can, then pick questions that fill the
remaining gaps.

Group your selected questions by theme when presenting them to the user.

---

## Category 1: Problem and Users

Ask at least one from this category. Always.

- **What specific problem does this solve?** Ask the user to describe
  the pain point in concrete terms, not as a missing feature. "Users
  can't do X" is weaker than "Users currently spend 40 minutes doing X
  manually, which causes Y errors per week."

- **Who is the primary user?** Get specifics: role, technical literacy,
  frequency of use, environment (mobile, desktop, API consumer). If
  there are multiple user types, ask which one the MVP targets.

- **What does the user do today without this?** The current workaround
  reveals constraints and expectations. If they use spreadsheets, they
  expect tabular UX. If they use Slack commands, they expect a CLI-like
  interface.

- **What does success look like?** Push for measurable outcomes, not
  vibes. "Reduce X by Y%", "Enable Z without manual intervention",
  "Process N items in under M seconds."

Ask when: User provides only a solution ("build me an app that does X")
without stating the underlying problem.

---

## Category 2: Solution Shape

Ask 1 to 2 from here. Skip if the user already described the solution
in detail.

- **What are the 3 to 5 core features of the MVP?** Force prioritization.
  If they list more than 5, ask which they would cut if they had to ship
  in half the time.

- **What is explicitly out of scope for v1?** This prevents agents from
  gold-plating. Get concrete exclusions: "No multi-tenant support",
  "No mobile app", "No real-time sync."

- **Are there existing products or features that serve as reference?**
  Competitors, internal tools, open-source projects. "Like X but with Y"
  is useful signal.

- **What are the primary user flows?** Ask for the happy path first,
  then the top 2 to 3 error/edge cases they care about.

Ask when: User provides a vague idea ("I want a dashboard for X") or
the scope feels unbounded.

---

## Category 3: Technical Context

Ask 2 to 3 from here. Critical for agent-executable PRDs.

- **What is the target stack?** Language, framework, runtime, package
  manager. If there is an existing repo, ask for its path or a brief
  description of its structure (monorepo, microservices, monolith).

- **What database or storage does this use?** Existing DB, new DB, file
  storage, third-party API, localStorage. If existing, ask for the ORM
  or query pattern (Prisma, Drizzle, raw SQL, Mongoose).

- **What authentication/authorization is in place or needed?** Existing
  auth provider (Clerk, Auth0, Supabase Auth, custom JWT)? Role-based
  access? API keys? If none, say so explicitly.

- **What external services or APIs does this integrate with?** Payment
  providers, email services, search, analytics, third-party data sources.
  Ask for existing API clients or SDKs already in the codebase.

- **Are there existing patterns or conventions the agent must follow?**
  CLAUDE.md, AGENTS.md, .cursorrules, linting config, testing framework,
  commit message conventions, branching strategy.

- **What are the deployment targets?** Vercel, AWS, self-hosted, Docker,
  edge functions. Staging environment? CI/CD pipeline in place?

Ask when: Always for greenfield projects. For existing codebases, ask
only what you cannot infer from the repo description.

---

## Category 4: Constraints and Non-Functional Requirements

Ask 1 to 2 from here. Agents ignore NFRs unless they are explicit.

- **Performance requirements?** Response time targets, concurrent users,
  data volume. "The dashboard must load in under 2 seconds with 10K
  rows" is actionable. "It should be fast" is not.

- **Security or compliance constraints?** SOC2, GDPR, HIPAA, PCI. Data
  residency requirements. Encryption at rest or in transit mandates.

- **Accessibility requirements?** WCAG level, screen reader support,
  keyboard navigation, contrast requirements.

- **What must NOT break?** Existing features, APIs consumed by other
  services, data integrity constraints. This is the most underrated
  question. Agents will confidently refactor code that other services
  depend on.

- **Budget or time constraints?** If the user has a hard deadline,
  the PRD scope must fit. If they have a token budget for agent usage,
  the PRD should be phased to allow incremental delivery.

Ask when: The project involves production systems, user data, or
external consumers.

---

## Category 5: Delivery Preferences

Ask 1 from here if not already clear.

- **What companion files do you need?** Just the PRD? Also CLAUDE.md?
  TASKS.md with a task breakdown? PLANNING.md with architecture notes?

- **What format works best for your workflow?** Single Markdown file?
  Separate files per phase? JSON for machine consumption?

- **Is this for a specific agent tool?** Claude Code, Cursor, Codex,
  Gemini CLI, Windsurf? The PRD structure remains the same, but the
  companion file (CLAUDE.md vs AGENTS.md vs .cursorrules) differs.

Ask when: First time working with this user, or when the user has not
specified their toolchain.

---

## Processing User Responses

After the user answers:

1. Summarize what you understood in 3 to 5 bullet points. Let them
   confirm or correct.
2. Identify remaining gaps. If critical gaps exist (no stack specified,
   no success criteria), ask up to 3 follow-up questions.
3. If non-critical gaps remain, state your assumptions explicitly and
   mark them with `[ASSUMPTION]` in the PRD.
4. Proceed to Stage 2.
