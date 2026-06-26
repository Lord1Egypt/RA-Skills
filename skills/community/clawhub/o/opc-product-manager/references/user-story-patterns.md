# User Story Patterns

> Patterns for writing agent-executable user stories with measurable acceptance criteria.
> Load with `read_file("references/user-story-patterns.md")` during Phase 2 (Spec Generation).

---

## Story Format

```
As [role], I want [specific action], so that [measurable benefit].
```

**Rules:**
- Role = who is doing this (user, admin, visitor, API consumer)
- Action = specific verb + object ("create a task", "upload a file"), not vague ("manage things")
- Benefit = why this matters, ideally measurable ("I can track my progress", "I don't lose data")

---

## Acceptance Criteria Format

Each story needs 3-5 acceptance criteria in Given/When/Then format:

```
Given [context/precondition],
When [action the user takes],
Then [expected result].
```

**Good criteria are:**
- Testable — you can write a test for it
- Specific — no "works correctly" or "is fast"
- Observable — the result is visible to the user or measurable by the system

---

## Good vs Bad Examples

### Bad Stories

| Story | Problem |
|-------|---------|
| "As a user, I want to manage my account" | Vague action — "manage" could mean anything |
| "As a user, I want a fast experience" | Not a user story — it's a quality attribute |
| "As a developer, I want to use Redis for caching" | Implementation detail, not user need |
| "As a user, I want to create, edit, delete, share, and archive tasks" | Compound — split into individual stories |
| "As a user, I want a beautiful dashboard" | Subjective — not testable |

### Good Stories

| Story | Why it works |
|-------|-------------|
| "As a user, I want to create a task with a title and due date, so I can track what I need to do." | Specific action, clear fields, clear benefit |
| "As a user, I want to mark a task as complete, so I can see my progress." | Single action, observable result |
| "As an API consumer, I want to fetch tasks filtered by status, so I can display them in my frontend." | Clear technical context, specific filter capability |
| "As a visitor, I want to sign up with my email, so I can start using the app." | Clear entry point, specific auth method |

---

## Priority Framework

| Priority | Definition | Rule |
|----------|-----------|------|
| **P0 (MVP)** | Without this, the product doesn't work. Core value delivery. | Must ship in V1. |
| **P1 (Soon after)** | Users will ask for this within a week. Expected functionality. | Ship in V1.1 or V2. |
| **P2 (Nice-to-have)** | Would make the product better, but not essential. Delight features. | Defer until validated. |

**Guideline for solo founders:**
- V1 should have 3-5 P0 stories maximum
- If you have more than 7 total stories for V1, you're building too much
- Every P1/P2 story should include: "Defer because: [reason it's not P0]"

---

## Common Story Patterns by Feature

### Authentication

```
P0: As a visitor, I want to sign up with email and password, so I can create an account.
    - Given I'm on the sign-up page, When I submit a valid email and password (8+ chars), Then my account is created and I'm logged in.
    - Given I submit an email that's already registered, When I try to sign up, Then I see an error message.

P0: As a user, I want to log in with my email and password, so I can access my data.
    - Given I have an account, When I submit correct credentials, Then I'm redirected to the dashboard.
    - Given I submit wrong credentials, When I try to log in, Then I see "Invalid email or password."

P1: As a user, I want to reset my password via email, so I can regain access if I forget it.
P2: As a user, I want to log in with Google, so I can sign up faster.
```

### CRUD (Core Entity)

```
P0: As a user, I want to create a [entity] with [key fields], so I can [core benefit].
    - Given I'm logged in, When I fill in [fields] and submit, Then the [entity] appears in my list.
    - Given I leave a required field empty, When I submit, Then I see a validation error.

P0: As a user, I want to see a list of my [entities], so I can browse and select one.
    - Given I have [entities], When I open the list page, Then I see all my [entities] sorted by [default sort].
    - Given I have no [entities], When I open the list page, Then I see an empty state with a "Create" button.

P0: As a user, I want to edit a [entity], so I can fix mistakes or update information.
P1: As a user, I want to delete a [entity], so I can remove things I no longer need.
P2: As a user, I want to search/filter [entities] by [field], so I can find specific ones quickly.
```

### Data Display

```
P0: As a user, I want to view the detail page of a [entity], so I can see all its information.
P1: As a user, I want to sort my list by [field], so I can find what I need.
P1: As a user, I want to export my data as CSV, so I can use it in spreadsheets.
P2: As a user, I want a dashboard with summary stats, so I can see my activity at a glance.
```

### Notifications

```
P2: As a user, I want to receive an email when [event], so I don't miss important updates.
    Note: For V1, log events to console or show in-app. Email in V2.
```

### Billing/Payments

```
P1: As a user, I want to subscribe to a paid plan, so I can access premium features.
    Note: For V1, consider manual invoicing (opc-invoice-manager) instead of Stripe integration.
P2: As a user, I want to manage my subscription (upgrade/downgrade/cancel).
```

---

## Anti-Patterns to Avoid

1. **Compound stories** — "I want to create, edit, and delete tasks" → Split into 3 stories
2. **Implementation stories** — "Add a Redis cache" → Not a user need. Why do you need caching?
3. **Vague acceptance criteria** — "Works correctly" → How? What does "correctly" mean?
4. **Admin-first thinking** — Don't build an admin dashboard for V1. Use your database GUI.
5. **Premature features** — "Search with fuzzy matching" → For V1, a simple text search or filter is enough
6. **Copy-paste stories** — Don't write stories that could apply to any product. Every story should be specific to YOUR product.

---

*Reference for opc-product-manager.*
