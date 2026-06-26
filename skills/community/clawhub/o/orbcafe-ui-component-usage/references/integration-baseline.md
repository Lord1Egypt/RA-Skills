# Integration Baseline

## Required checks

- Import path:
  - `import { ... } from 'orbcafe-ui'`
- Contract path:
  - classify with `skill-routing-map.md`
  - confirm module contract in `module-contracts.md`
- Next.js App Router:
  - unwrap dynamic `params` in Server Page, then pass plain props to Client Component.
- Hydration safety:
  - avoid first-render `Date.now()`, `Math.random()`, direct browser-only branching.
- Tailwind scan path:
  - include `./node_modules/orbcafe-ui/dist/**/*.{js,mjs}`.
- i18n:
  - use `OrbcafeI18nProvider` or `CAppPageLayout.locale`.

## Version-sensitive notes (>= 1.0.6)

- `useStandardReport` default rows-per-page is `20` and includes `-1` (`ALL`).
- `CAppPageLayout` supports `locale`, `localeOptions`, `onLocaleChange`.
- `CTable` includes `quickCreate` config.
- `AgentUI` is exported from package entry and should be consumed via `AgentPanel` / `StdChat` / `CopilotChat`, not internal renderers.
