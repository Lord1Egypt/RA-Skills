# {{PROJECT_NAME}} — Functional Specifications

> **For:** Product/UX reference and developer onboarding (user-flow contract)
> **Repo:** {{REPO_URL}}
> **Production:** {{PRODUCTION_URL}}

This is the user-flow contract — the document that describes what the system does from a user's perspective. It captures intended behavior, edge cases, and the rules that govern features. It's the answer to "what should this product DO?"

This file stays in sync with the implementation as part of finishing a feature (see CLAUDE.md "Housekeeping protocol"). When a feature ships or changes, update both [`docs/features/<name>.md`](docs/features/) (operational reference) and the matching section here (user-flow contract). The recap workflow prompts for both.

---

## Table of Contents

1. [Authentication & User Management](#1-authentication--user-management)
2. [Subscription & Payment](#2-subscription--payment)
3. [Core Features](#3-core-features)
4. [User Flows](#4-user-flows)
5. [Admin & Internal Tools](#5-admin--internal-tools)
6. [Notifications](#6-notifications)
7. [Edge Cases & Error States](#7-edge-cases--error-states)
8. [UI Consistency Standards](#8-ui-consistency-standards)

---

## 1. Authentication & User Management

<add-when-implemented>
- Signup flow (entry point, fields, validation, post-signup state)
- Login flow
- Password reset flow
- Email verification (if applicable)
- Session management
- Account states (active, disabled, deleted)
- Role hierarchy
</add-when-implemented>

Detailed auth implementation: [`docs/architecture/auth.md`](docs/architecture/auth.md)

## 2. Subscription & Payment

<add-when-implemented>
- Pricing tiers
- Trial mechanics
- Upgrade / downgrade / cancel flows
- Payment failure handling
- Refund policy
</add-when-implemented>

Detailed billing implementation: [`docs/features/billing.md`](docs/features/billing.md) (if applicable)

## 3. Core Features

<add-when-implemented>
For each major feature, document:
- Entry point (which route, which UI element)
- Inputs and validation rules
- Behavior step-by-step
- Output / success state
- Linked operational doc: `docs/features/<name>.md`
</add-when-implemented>

## 4. User Flows

<add-when-implemented>
End-to-end flows that span multiple features:
- Onboarding flow
- First-time-user flow
- Most common task flow
- Account recovery flow
</add-when-implemented>

## 5. Admin & Internal Tools

<add-when-implemented>
- Admin dashboard structure
- Permission boundaries (admin vs super-admin)
- Audit logging
- Common admin tasks
</add-when-implemented>

## 6. Notifications

<add-when-implemented>
- Email triggers (transactional)
- In-app notifications
- Push notifications (if applicable)
- Notification preferences
</add-when-implemented>

## 7. Edge Cases & Error States

<add-when-implemented>
- Empty states (no data yet)
- Loading states
- Network failure
- Permission denied
- Rate limiting
- Account disabled
</add-when-implemented>

## 8. UI Consistency Standards

<add-when-implemented>
- Design system / component library
- Theming (light/dark, brand colors)
- Typography
- Accessibility minimums
- Responsive breakpoints
</add-when-implemented>

Detailed UI implementation: [`docs/features/ui.md`](docs/features/ui.md)
