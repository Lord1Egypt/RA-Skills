# Website Management Playbook for Kadence Sites

Use this execution playbook when operating as `rilvo-website-developer`.

## 1) Intake checklist

- Objective (build, redesign, template update, bugfix)
- Scope (pages/templates/site-wide)
- Environment (staging or production)
- Feature tier (Free-only vs Free+Pro confirmed)
- Risk level (safe visual change vs structural template impact)

## 2) Build workflow

1. Confirm capability tier using matrix.
2. Define affected templates and blocks.
3. Implement with Kadence-native controls first.
4. Keep content/presentation split clean.
5. Validate responsive behavior + readability.

## 3) Content workflow integration

For page/post content operations:
- Use `wordpress-content-rest-api` for content CRUD and status control.
- Use this Kadence skill for layout/design-system decisions.

Recommended sequence:
1. Update structure/template in editor/theme settings.
2. Update content via REST when needed (draft-first).
3. Re-open rendered page and verify design tokens/render quality.

## 4) QA gates

- No Pro-only feature in Free-only sites.
- No rogue hardcoded colors/spacing unless requested.
- Header/nav/footer coherent across breakpoints.
- Typography hierarchy intact.
- Main templates render correctly on representative pages.

## 5) Delivery format

When reporting completion, include:
- What changed
- Where it changed (template/page/global)
- Whether implementation is Free-safe or Pro-enhanced
- Any optional Pro upgrades not applied
- Follow-up recommendations (max 3)

## 6) Guardrails

- Do not edit plugin/theme PHP unless explicitly approved.
- Do not perform destructive bulk updates without explicit approval.
- Prefer reversible, editor-level changes.
- Flag uncertainty rather than guessing feature availability.