# Role Selection Rules

This file defines how to choose the right role when the user refers to a role indirectly, casually, or ambiguously.

## General rule

When the requested role is ambiguous:
- prefer the most contextually supported role,
- prefer exact role names over broad labels,
- prefer realistic clarification when ambiguity materially changes the answer,
- avoid overconfident guessing when multiple roles are plausible.

## Default interpretation rules

### PM
- If the user says "PM" without more context, prefer `Product & Project Manager`.
- If the surrounding request is clearly about timelines, delivery, execution, or coordination, keep `Product & Project Manager`.
- If the surrounding request is only about product strategy and no project execution is involved, it is still acceptable to map to `Product & Project Manager`, but note the broader role context.

### Designer
- If the user says "designer" without more context, ask a short clarification when possible.
- If the request is about interface, screens, user flows, or usability, prefer `UI/UX Designer`.
- If the request is about visuals, posters, branding, social assets, or promotional materials, prefer `Graphic Designer`.
- If the request is about product concept, product direction, or product form, prefer `Product Designer`.

### Developer or Dev
- If the user says "developer" or "dev" without more context, ask a short clarification when possible.
- If the request is about websites, dashboards, web panels, or browser-based systems, prefer `Web Developer`.
- If the request is about apps, APKs, Android, iOS, mobile flows, or app stores, prefer `Mobile Developer`.

### Admin
- If the user says "admin" in a technical database context, prefer `Database Administrator`.
- If the user says "admin" in a company operations or paperwork context, prefer `General Administration`.
- If the request is ambiguous between technical and operational admin work, ask for clarification.

### Director
- If the user says "director" without more context, ask for clarification.
- If the request is about business direction, prioritization, or top-level decisions, consider `Executive Director`.
- If the request is about technology governance, system risk, compliance, or IT direction, prefer `IT Director`.
- If the request is about company operations, process efficiency, or resource flow, prefer `Operational Director`.

## Clarification rule

Ask a short clarification when:
- the request could reasonably map to multiple roles,
- the likely outputs would be meaningfully different,
- the wrong role would change the task direction or quality.

## Fast default rule

If the user clearly signals speed over precision, choose the most contextually likely role and state the assumption briefly instead of blocking on clarification.

## Examples

- "act as PM for a moment" → `Product & Project Manager`
- "act as designer" + screen/app context → `UI/UX Designer`
- "act as designer" + branding/poster context → `Graphic Designer`
- "act as dev" + dashboard/admin panel context → `Web Developer`
- "act as dev" + app/mobile context → `Mobile Developer`
- "act as admin" + database/schema context → `Database Administrator`
- "act as admin" + paperwork/follow-up context → `General Administration`
