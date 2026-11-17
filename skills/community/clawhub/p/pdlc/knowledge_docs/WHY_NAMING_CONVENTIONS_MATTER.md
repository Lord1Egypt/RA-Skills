# Why Naming Conventions Matter

**Purpose:** Explains why consistent naming across files, variables, modules, and APIs prevents the cognitive overhead that slows development — and why automated enforcement is the only way to maintain consistency at scale.

---

## The Practice

Naming conventions mean agreeing on a single, consistent pattern for how things are named in code: files (kebab-case, PascalCase), variables (camelCase), classes (PascalCase), APIs (plural nouns, versioned paths), modules (feature-based, domain-based). One pattern per category, documented, enforced.

---

## What Happens When You Skip It

1. **The "which one is right?" confusion.** `UserService.ts`, `user-service.ts`, `userService.ts`, and `user_service.ts` all exist in the same project. New developers can't infer the pattern. They guess — and add a fifth variant.

2. **The search failure.** Developer needs the user authentication handler. Searches for `auth`. Finds nothing — because it's named `loginManager`. Searches for `user`. Finds 30 files with inconsistent naming. 10 minutes lost finding what should be instant.

3. **The meaning drift.** `handler`, `controller`, `manager`, `service` are used interchangeably. Does `UserManager` manage user lifecycle or manage the user list? Does `OrderHandler` handle HTTP requests or handle business logic? Without conventions, names lie.

4. **The merge conflict factory.** Developer A creates `src/components/UserProfile.tsx`. Developer B creates `src/components/user-profile.tsx`. Both are valid by their own mental model. Git sees two different files. Reviews waste time on naming debates instead of logic discussions.

5. **The API inconsistency.** `/api/users` (plural), `/api/Order` (singular, capitalized), `/api/get-products` (verb prefix), `/api/v2/inventory_items` (snake_case). Every endpoint follows a different pattern. Consumers can't predict URLs — they must memorize each one.

---

## Real-World Impact

| Dimension | Impact |
|-----------|--------|
| Cost | Developers spend 5-10% of their time on name-related friction (searching, guessing, resolving conflicts). On a team of 8, that's 20-40 hours per month of pure waste. |
| Timeline | Naming debates in code review add 15-30 minutes per PR when conventions aren't established. Automated enforcement eliminates the debate entirely. |
| Quality | Inconsistent naming correlates with inconsistent architecture — teams that don't enforce names often don't enforce boundaries either. Naming is the canary. |
| Team | "You named it wrong" feedback feels personal without a documented convention. "The naming hook caught this" feels objective. Conventions depersonalize code style discussions. |
| Risk | API naming inconsistency creates documentation gaps, confuses consumers, and makes automated tooling (SDK generation, API testing) harder to implement. |

---

## How the AI-* Family Prevents This

| Package | Feature | Prevention Mechanism |
|---------|---------|---------------------|
| **AI-DWG** | `naming-conventions.md` steering | Generates a naming conventions steering file derived from the chosen tech stack — specific patterns for the project's language and framework. |
| **AI-GCE** | NAME-* enforcement rules | Derives naming rules from the steering file. Hooks fire in real-time when files, classes, or APIs violate the convention. |
| **AI-GCE** | Tier 1 inclusion | Naming enforcement is a Tier 1 (foundational) rule — active from day one. Basic enough that no one objects, impactful enough to prevent drift. |
| **AI-ADLC** | API naming in Stage 10 | API architecture stage defines URL structure, resource naming, and versioning pattern. Conventions are locked at design time. |
| **AI-DWG** | Folder structure generation | Generated folder names follow the convention. Physical structure establishes the pattern by example. |

---

## Severity: Medium

Naming inconsistency doesn't cause outages or security breaches. It causes chronic cognitive friction — the kind that's too small to report but too persistent to ignore. Over months, it compounds into significant productivity drag and makes codebases feel hostile to navigate.

---

## Related Documents

| Document | Location |
|----------|----------|
| How DWG Generation Engine Works | `knowledge_docs/HOW_DWG_GENERATION_ENGINE_WORKS.md` |
| How GCE Derivation Pipeline Works | `knowledge_docs/HOW_GCE_DERIVATION_PIPELINE_WORKS.md` |
| How to Adopt Governance on a Project | `knowledge_docs/HOW_TO_ADOPT_GOVERNANCE_ON_A_PROJECT.md` |
| Why API Contract First Matters | `knowledge_docs/WHY_API_CONTRACT_FIRST_MATTERS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
