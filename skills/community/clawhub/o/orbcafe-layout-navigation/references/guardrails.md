# Layout Guardrails

## i18n constraints

- Use `OrbcafeI18nProvider` at app root or `locale` on `CAppPageLayout`.
- Keep business identifiers stable and localize labels only.

## Next.js constraints

- In App Router, unwrap `params` in Server Page before passing to Client Component.
- Avoid first-render mismatch from pathname-only highlights or browser-only values.

## User menu constraints

- If using default menu, wire `onUserSetting` and `onUserLogout`.
- If using `userMenuItems`, ensure all actions are provided and consistent with auth policy.

## Motion constraints

- Prefer `CPageTransition` variants using transform/opacity and durations around 160-260ms.
- Respect reduced-motion behavior; avoid adding forced animations on top.
