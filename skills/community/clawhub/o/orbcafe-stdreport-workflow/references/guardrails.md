# StdReport Guardrails

## Public API constraints

- Import from `orbcafe-ui` package entry only.
- Do not import private files under `src/components/...` from consumer apps.

## Behavior constraints

- `useStandardReport` defaults (>= 1.0.6):
  - `initialRowsPerPage = 20`
  - `rowsPerPageOptions = [20, 50, 100, -1]`
  - `-1` means ALL
- Changing rows-per-page resets page index to `0`.
- If backend cannot accept `limit = -1`, map it explicitly in `fetchData`.

## Persistence constraints

- Layout/variant persistence relies on `id/appId/tableKey`.
- Without those IDs, saved states can collide across pages.
- `serviceUrl` unavailable should fallback to local storage paths.

## i18n constraints

- Wrap pages with `OrbcafeI18nProvider` or parent `CAppPageLayout.locale`.
- Keep filter `value` machine-stable and localize labels only.
