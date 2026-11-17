# Troubleshooting monitors

## Contents
- Status values
- Noisy monitors
- Silent monitors
- Pages that will not load
- Tool errors

## Status values

`list-monitors` and `get-monitor-details` report each monitor's `status` and `failed` (consecutive failed checks; 0 is healthy).

| Status | Meaning | What to do |
|---|---|---|
| `ok`, `unchanged` | Checking normally | Nothing |
| `pending` | The first check has not finished yet | Wait a few minutes, then read it with `get-latest-values` |
| `disabled` | Paused, by the user or a plan limit | `set-monitor-status(monitor_id="...", enabled=true)` if the user wants it back |
| `stock_recorded` | A stock level was saved without an alert | Nothing; alerts follow the Stock Alerts set in PageCrawl |
| `selector_not_found`, `invalid_selector`, `number_not_found` | The tracked element is missing or the selector is broken, usually after a redesign | Diagnose with `test-configuration`, then create a corrected monitor (or `ai_extract`) and offer to delete the old one |
| `blank_page`, `pdf_blank_page`, `empty_file` | The page or file came back empty | Look at `get-screenshot`; if the content needs a click or a wait, add `actions` |
| `timeout`, `unreachable`, `unavailable`, `net_error`, `connection_reset` | The site did not answer in time or at all | PageCrawl retries on the next check; if it persists, check the URL works in a browser |
| `404_page_not_found` | The page is gone | Ask whether the page moved; update the URL with `manage-monitors(action="update", monitor_id="...", url="...")` |
| `401_unauthorized`, `requires_auth`, `login_failed` | The page needs a login, or the saved login failed | The user fixes the login in the PageCrawl app; never ask for the password |
| `403_forbidden`, `429_rate_limit`, any status starting with `blocked` | The site refused or limited the visit | See "Pages that will not load" below |
| `too_many_redirects`, `unexpected_redirect` | The URL redirects somewhere else | Ask whether to monitor the final address instead |
| `ssl_error` | The site's certificate is invalid | Tell the user; the site owner has to fix it |
| `javascript_error` | Custom JavaScript (an action or a tracked element) threw an error | Fix or remove the script |
| `currency_mismatch` | The page showed the price in a different currency than before, so the check was not recorded | Usually the site varied its currency or region; tell the user if it persists |
| `file_too_large`, `pdf_error`, `file_error` | The file could not be processed | Tell the user; a smaller or different file URL may work |
| `relay_offline` | The PageCrawl Relay this monitor uses is offline | The user restarts the Relay machine |

## Noisy monitors

Signs: `get-intelligence` lists the monitor as changing on every check, or the user keeps clearing changes nobody cares about. Fixes, gentlest first:

1. Sharpen `ai_page_focus` so importance scores reflect what matters: `manage-monitors(action="update", monitor_id="...", ai_page_focus="Only plan prices and limits matter; ignore testimonials, dates and counters")`.
2. Read with `min_priority` and set reports to `filter_mode="important"`, so minor changes stay out of the way without being lost.
3. Narrow what is tracked: `content_only` or `reader` instead of the whole page, or one element with a selector. This needs a corrected monitor, because `manage-monitors` cannot change what a monitor tracks.

More: https://pagecrawl.io/help/reduce-false-positives/article/reduce-false-positives-monitoring-website-for-changes

## Silent monitors

A monitor that has never recorded a change may be watching the wrong thing rather than a quiet page. Read what it captures with `get-latest-values`. If the value is empty, a cookie notice, or not what the user meant, diagnose with `test-configuration(url="...", tracking_mode="...", selector="...")` and create a corrected monitor. `test-configuration` fetches the page live and is slow: use it once per question, never in a loop.

## Pages that will not load

Some sites refuse automated visits or limit how often they can be checked. PageCrawl retries on the next scheduled check. If a page keeps failing:

- Confirm the URL works in a normal browser and is not behind a login.
- A lower check frequency helps with rate limits.
- Point the user to https://pagecrawl.io/help/troubleshooting/article/how-to-unblock-a-blocked-page for the options in their account.

Do not try to fetch the page another way to work around the block.

## Tool errors

| Error | What to do |
|---|---|
| A plan limit or quota (monitor count, check allowance, on-demand checks) | Tell the user what the message says. Do not retry or work around it |
| A validation message (missing `selector`, `prompt`, or `workspace_id`) | Fix the arguments and call again |
| Monitor not found | Find it with `list-monitors(search="...")`; it may be in another workspace or disabled (`include_disabled=true`) |
| Several monitors match a URL | Ask the user which one, showing names and what each tracks |
| Authentication required | The connection has expired; see [setup.md](setup.md) |
