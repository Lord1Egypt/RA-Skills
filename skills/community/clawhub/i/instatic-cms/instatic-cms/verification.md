# Verification

Evidence bar for claiming anything about an Instatic instance. Text and measurements only; no screenshots into the model.

## Liveness
- Container reports healthy; `GET /health` answers; `/admin` returns 200; `/admin/api/cms/setup/status` returns JSON.

## Data and publish
- After a schema write (table create/patch), read it back: `GET /data/tables/:id` or `GET /data/_meta` (response nests under `meta`) and confirm kind, stored fields, and the computed routable/versioned flags; create responses omit computed flags.
- After a row publish, fetch the page HTML from the site origin and grep for the changed content.
- After a site publish, confirm the response carries `publishedPages:n` and a matching `/audit` event exists.
- Static-deploy tests: fetch a published loop-bearing page and count `instatic-hole` occurrences; zero on the whole set is the precondition for claiming a pure static host can serve it.
- On any 401 `step_up_required`: open POST /auth/step-up {password}, retry once. A second failure means stop and read /auth/activity; do not loop, the lockout counter is real.

## UI flows
- Headless-render admin pages and check text content and DOM geometry (scrollWidth vs clientWidth for clipping, expected panel strings). A benign pre-login 401 on the session probe is normal.
- Interactive product decisions belong to the operator: his own hands on his own device/browser are the acceptance gate. An HTTP 200 never marks a workflow done.

## Style propagation
- Change a token, then confirm the computed style on at least one page that was not the edited one, after publish.
