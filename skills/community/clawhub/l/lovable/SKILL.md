---
name: clawhub-lovable
description: Helps OpenClaw Clinical Hackathon participants get started quickly building clinical and healthcare apps with Lovable. Use when the user is building a clinical app in Lovable, mentions the hackathon or Lovable, or asks for quick-start guidance for clinical projects (patient intake, dashboards, assessments, PHI-safe patterns).
---

# ClawHub × Lovable — Clinical Hackathon Quick Start

Use this skill when helping participants of the **OpenClaw Clinical Hackathon** build **clinical or healthcare projects** with **Lovable** (full-stack AI app platform). Goal: get from idea to a working clinical MVP fast, with sensible patterns for auth, data, and scope.

## When to apply

- User mentions **OpenClaw Clinical Hackathon**, **Lovable**, or **clinical project**
- User wants to build a **clinical/healthcare app** (intake forms, dashboards, assessments, vitals, etc.)
- User asks for **quick start** or **getting started** with Lovable for clinical use cases

## Quick start (first clinical project in Lovable)

1. **Account and project**
   - Sign up at [lovable.dev](https://lovable.dev) and create a new project.
   - Name it clearly (e.g. “Patient Intake MVP”, “Clinical Dashboard”).

2. **Scope with Plan mode**
   - In Lovable, use **Plan mode** first: describe the clinical goal (e.g. “Patient intake form with consent and basic demographics, then a simple list view”).
   - Get a high-level plan and break the app into **components** (e.g. intake form, list, detail view).

3. **Build by component**
   - Use **Agent mode** to implement one component at a time.
   - Prompt for **that component** (e.g. “Add a patient intake form with fields: name, DOB, consent checkbox, submit”) instead of “build the whole app”.
   - Add **authentication early** if the app will show any user-specific or sensitive data.

4. **Backend and data**
   - Use **Lovable Cloud** (Supabase) for database and auth so you don’t manage servers.
   - Prefer **structured fields** (e.g. demographics, assessments) in the DB from the start; avoid free-text blobs for anything that might be PHI.

5. **Publish**
   - Use Lovable’s deploy/publish flow when the MVP is ready; add a **custom domain** later if needed.

## Clinical project patterns

- **Auth from day one**  
  If the app touches patient or user-specific data, add auth (e.g. Supabase Auth) at the start so you don’t retrofit it later.

- **PHI-safe prompts and logs**  
  Do **not** put real patient names, IDs, or clinical content in prompts or in logs. Use placeholders in prompts (e.g. “patient name field”, “DOB field”) and keep real data only in the database and in the running app.

- **Common clinical UIs**
  - **Intake**: Form with demographics, consent, and optional referral reason.
  - **Assessments**: Step-by-step or single-page forms with scores/results stored in DB.
  - **Dashboards**: Read-only or summary views (e.g. list of patients, vitals summary) with filters and simple charts.

- **Keep scope MVP**  
  One clear workflow (e.g. “intake → list” or “assessment → result”) is enough for the hackathon; add features after the core works.

## Lovable best practices (recap)

- **Plan before prompt**: Use Plan mode to get a component-level plan, then implement in Agent mode.
- **Prompt by component**: One prompt per component or small feature; avoid “build entire app” in one go.
- **Use Knowledge**: Upload design system, brand, or API docs as a Knowledge file so prompts stay consistent.
- **Credits**: Lovable uses credits for generation; smaller, focused prompts use them more efficiently.

## OpenClaw / ClawHub context

- **OpenClaw**: Self-hosted gateway for chat apps (WhatsApp, Telegram, Discord, iMessage, etc.) and AI agents. Useful if participants want to expose a clinical workflow via chat (e.g. “start intake via Telegram”).
- **ClawHub**: [clawhub.com](https://clawhub.com) — skills discovery. Point participants there for more skills (e.g. health assistant, automation) that can complement a Lovable-built clinical UI.

When the user’s goal is **“get something clinical running in Lovable fast”**, lead with the Quick start and Clinical project patterns; add OpenClaw/ClawHub only if they ask about chat channels or existing skills.

## Examples

**User:** “I’m doing the OpenClaw Clinical Hackathon and want to build a patient intake form in Lovable.”  
**Agent:** Walk them through: create project → Plan mode to get “intake form + list” plan → Agent mode to build the form component (fields, validation, submit) → add Supabase table and auth if they need per-user data → then the list view.

**User:** “How do I make sure I don’t leak PHI when building with Lovable?”  
**Agent:** Emphasize: no real patient data in prompts or in Knowledge; use generic field names and placeholders; keep PHI only in the database and in the running app; avoid logging request/response content that could contain PHI.

**User:** “What’s the fastest way to get a clinical dashboard live?”  
**Agent:** Suggest: Plan mode for “dashboard with list + filters + one detail view” → implement one view at a time in Agent mode → use Lovable Cloud (Supabase) for data and auth → publish when the main view works; add charts or extra filters as follow-up.
