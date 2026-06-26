# Scope Assessment

> Complexity scoring and MVP cutting rules for solo builders.
> Load with `read_file("references/scope-assessment.md")` during Phase 3 (Scope Assessment) and Scope Check mode.

---

## Complexity Scoring

Score each factor and sum for total complexity (1-10 scale).

| Factor | 0 points | 1 point | 2 points | 3 points |
|--------|----------|---------|----------|----------|
| **Entity count** | — | 1-3 entities | 4-6 entities | 7+ entities |
| **Auth complexity** | No auth needed | Basic auth (email/password) | Roles/permissions (admin + user) | — |
| **External integrations** | None | 1-2 APIs | 3+ APIs | — |
| **Real-time features** | None | Present (websockets, SSE) | — | — |
| **Payment processing** | None | — | Payment integration (Stripe, etc.) | — |

**Maximum score: 10** (3 + 2 + 2 + 1 + 2)

---

## Grade Bands

| Score | Grade | Timeline Estimate | Guidance |
|-------|-------|-------------------|----------|
| **1-3** | Weekend project | 1-2 days | Ship it. Don't overthink. |
| **4-6** | Week project | 3-7 days of focused work | Solid scope for a solo MVP. Sweet spot. |
| **7-8** | Multi-week | 2-4 weeks | Needs phased delivery. Consider cutting. |
| **9-10** | Complex | 4+ weeks | Strongly consider simplifying before building. |

---

## Cut Rules — What to Remove First

When complexity is too high, cut in this order (first items are easiest to defer):

| Priority | Cut This | Replace With |
|----------|----------|-------------|
| 1 | Admin dashboard | Use database GUI (Supabase dashboard, pgAdmin, SQLite browser) |
| 2 | Email notifications | Log to console in V1, add emails in V2 |
| 3 | Role-based permissions | Single user type for V1 (everyone is "user") |
| 4 | Search and filtering | Basic list sorted by date, add search in V2 |
| 5 | Analytics/reporting dashboard | Use external tool (Plausible, PostHog, simple SQL queries) |
| 6 | Social auth (Google, GitHub) | Email/password or magic link only for V1 |
| 7 | File upload | URL input or text paste for V1, file upload in V2 |
| 8 | Real-time updates | Polling or manual refresh for V1 |
| 9 | Mobile app | Responsive web first, native app only when web is validated |
| 10 | Payment processing | Manual invoicing (use opc-invoice-manager!) or "contact me" for V1 |

---

## "Is This a Weekend Project?" Checklist

Answer yes/no to each. If 4+ are "yes", it's a weekend project:

- [ ] Can it work with 3 or fewer database tables/entities?
- [ ] Does it need only basic auth (or no auth)?
- [ ] Does it have zero external API integrations?
- [ ] Is the core feature a single CRUD flow?
- [ ] Can it work without real-time features?

---

## Scope Creep Detection

These patterns signal the spec is growing beyond MVP. Flag them:

| Pattern | Signal | Action |
|---------|--------|--------|
| "Also, it should..." | Feature bolting | Ask: "Is this P0 or P1?" |
| "We need an admin panel" | Admin-first thinking | Defer. Use DB GUI for V1. |
| "Users should be able to customize..." | Premature configurability | Ship with sensible defaults. Add customization in V2. |
| "What about mobile?" | Platform creep | Responsive web first. Mobile app is a separate product. |
| "Can it integrate with [5 tools]?" | Integration overload | Pick the ONE most critical integration for V1. |
| "We need user roles" | Permission creep | Single user type for V1. Add roles when you have actual admins. |
| "Add social sharing" | Vanity feature | No user asked for this yet. Defer. |
| "Support multiple languages" | i18n creep | Ship in one language. Translate when you have users in other markets. |
| "We need a notification system" | Notification creep | In-app only for V1. Email/push in V2. |
| "Add an audit log" | Compliance creep | Only if required by regulation. Otherwise defer. |

---

## Scope Reduction Script

When asked to scope down, use this process:

1. **List all user stories** with their priority (P0/P1/P2)
2. **Remove all P2 stories** — they're never in V1
3. **Move P1 stories to V2** — explicitly write "Deferred to V2: [story]"
4. **Challenge each remaining P0 story**: "If we didn't build this, would the product still deliver its core value?"
5. **Re-score complexity** with the trimmed story list
6. **Output the delta**: "Reduced from [X] stories to [Y]. Complexity: [old] → [new]."

---

## Solo-Buildability Verdict

After scoring, output one of:

- **"Solo-buildable: weekend project"** (1-3) — Build it this weekend. Ship on Sunday.
- **"Solo-buildable: week project"** (4-6) — Block a week, focus, ship.
- **"Solo-buildable with phasing"** (7-8) — Build V1 this week (P0 only), V2 next week.
- **"Consider simplifying"** (9-10) — Too complex for one person in one sprint. Cut scope or find help.

---

*Reference for opc-product-manager.*
