# Tracking modes and monitor settings

## Contents
- Choose a tracking mode
- Several values on one page
- Selectors
- Actions before the capture
- Pages behind a login
- Prices and stock
- Files
- Notifications and saved defaults
- Values that cannot be crawled
- Errors you may see

## Choose a tracking mode

`add-page-monitor` takes one `tracking_mode`. Leave it out when unsure: the whole page text works for most pages, and files are detected from the URL.

| `tracking_mode` | Watches | Good for |
|---|---|---|
| `fullpage` (default) | All visible text | Landing pages, documentation, dashboards |
| `content_only` | The main content, without navigation, header, footer and sidebars | Busy pages where boilerplate would cause noise |
| `reader` | The main article text | Terms of service, privacy policies, legal pages, news, blog posts |
| `feed` | Repeating items, each tracked as added, removed or changed | Job boards, product listings, release lists, search results |
| `price` | The price, plus availability by default | Product pages |
| `specific_text` | The text of one element (needs `selector`) | A status line, a headline, one section |
| `specific_number` | A number in one element (needs `selector`) | A count, a rate, a score |
| `ai_extract` | Whatever a plain-language `prompt` describes | Values that are easier to describe than to select |
| `json_path` | One value in a JSON response (needs a JSONPath in `selector`) | APIs and data endpoints |
| `seo` | Title, meta description, canonical URL, robots tag, H1, social tags | SEO changes on your own or competitors' pages |
| `http_status` | The HTTP response code | Whether a URL is up, gone or redirected |
| `leaderboard` | Ranked rows (`selector` optional) | Rankings, charts, leaderboards |
| `pdf_extract` | The text of a PDF | PDFs, though leaving `tracking_mode` out detects them too |

For `ai_extract`, ask for one value and its format, for example `prompt="Return ONLY the next launch date as YYYY-MM-DD"`. A prompt that returns a single clean value gives clean history and charts.

Examples:

- `add-page-monitor(url="https://example.com/pricing", tracking_mode="content_only", ai_page_focus="Plan prices and limits; ignore testimonials")`
- `add-page-monitor(url="https://example.com/careers", tracking_mode="feed", frequency=1440)`
- `add-page-monitor(url="https://api.example.com/status.json", tracking_mode="json_path", selector="$.status.indicator")`

## Several values on one page

Pass `elements` instead of `tracking_mode` to track several values on one monitor, each with its own history and chart. Element `type` is one of `fullpage`, `text`, `price`, `number`, `stock`, `html`, `javascript`, `file_hash`, `pdf`, `ai_extract`.

- `selector` is required for `text`, `price`, `number`, `html` and `javascript`, and optional for `stock`.
- `label` is required for every `ai_extract` element and whenever a type appears twice, so the values can be told apart.
- `prompt` is required for `ai_extract`.

Example: `add-page-monitor(url="...", elements=[{"type": "price", "selector": ".price"}, {"type": "ai_extract", "label": "Shipping date", "prompt": "Return ONLY the shipping date as YYYY-MM-DD"}])`

## Selectors

`selector` takes CSS or XPath. Prefer stable attributes (IDs, `data-*` attributes) over generated class names. If the user cannot point at the element, `ai_extract` with a prompt usually works without one. Help for finding a selector: https://pagecrawl.io/help/tutorials/article/find-xpath-css-selector-in-chrome

## Actions before the capture

`actions` runs steps before the capture, in order: `remove_cookies_v2`, `remove_overlays`, `remove_element`, `remove_text`, `display_hidden`, `click`, `click_button`, `type`, `select`, `hover`, `submit_form`, `wait`, `wait_text`, `wait_element`, `scroll_to_bottom`, `javascript`.

- Monitors get cookie banner and overlay removal by default. Passing `actions` replaces that default, so include `{"type": "remove_cookies_v2"}` and `{"type": "remove_overlays"}` again if they are still wanted.
- `wait` takes 1 to 10 seconds in `value`. `javascript` takes up to 1500 characters.
- The plan limits how many wait steps a monitor can use.

More: https://pagecrawl.io/help/features/article/perform-actions

## Pages behind a login

Never ask for the password. Call `list-authentications` for the workspace and pass the matching `auth_id` to `add-page-monitor`. If none exists, tell the user to add the login in the PageCrawl app first (https://pagecrawl.io/help/features/article/can-i-track-password-protected-websites), then create the monitor.

## Prices and stock

- `tracking_mode="price"` tracks availability too (`track_availability` defaults to true).
- `track_stock=true` also saves how many units the page says are left. Every stock change is kept in the history, and an alert is sent only when a Stock Alert the user set in PageCrawl is reached. A check that only recorded a stock level has the status `stock_recorded`.
- To compare one product across shops, create one monitor per shop and read them together with `get-latest-values(monitor_ids=[...])`.

## Files

PDF, Word, Excel, CSV and other file URLs are detected when `tracking_mode` is left out. Other binary files are tracked by checksum, so any change to the file is detected.

## Notifications and saved defaults

- `notifications` chooses channels from `mail`, `slack`, `discord`, `telegram`, `teams`. By default PageCrawl uses email plus the channels already connected in the workspace. A channel must be connected in the PageCrawl app before it can deliver.
- `update-monitor-defaults` saves the workspace's defaults for new monitors (frequency, notifications, screenshots, `ai_page_focus`). Explicit arguments on `add-page-monitor` override them.
- `template_id` applies a template's shared settings. List templates with `list-templates`.

## Values that cannot be crawled

For internal metrics, values behind an API, or data the user already has, create a push data source with `create-data-source` and send values with `record-data`. See [automation.md](automation.md).

## Errors you may see

| Message or result | What to do |
|---|---|
| A mode needs a `selector` or `prompt` | Add it, or choose another mode |
| The frequency is below what the plan allows | Use the minimum the error names, or tell the user |
| Created but disabled because the monitor limit was reached | Tell the user the monitor exists but is paused, and why |
| A batch reports `skipped` | That URL already has a monitor; nothing was created for it |
| A single URL response includes a warning about an existing monitor | A second monitor was created for the same URL; offer to delete one |
