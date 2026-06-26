# OurGroceries skill — agent notes

Human-oriented overview lives in **`SKILL.md`**. This file is for **OpenClaw / automation agents** implementing or debugging list changes.

**Versioned handoff:** see **`VERSION`** (semver) and **`RELEASE_NOTES.md`** (full OpenClaw-oriented summary for this release).

## Implementation (do not use PyPI `ourgroceries` for this skill)

- **`lib/ourgroceries/`** is a **vendored** HTTP client (forked from [py-our-groceries](https://github.com/ljmerza/py-our-groceries)), prepended by every script via `sys.path`.
- **`requirements.txt`**: only **`aiohttp`** is required (`pip install -r requirements.txt` in a venv is fine; do not commit `.venv/`).

## API behavior vs the live website

- **`getLists`** is used for list overview (the site no longer uses legacy `getOverview`). Payload must include **`knownLists`** (empty `[]` for a full refresh). The JSON response uses **`lists`**, not `shoppingLists`; scripts accept either key.
- **`auto_category=True` on `add_item_to_list`**: calls **`getItemCategory`** (`itemName`, `note`, `guess: true`, plus `teamId` / `shareId` / `locale`), then **`insertItem`** with the returned **`categoryId`**, matching the web UI. If no category is returned, insert omits `categoryId` (fallback) and logs a warning.
- **`OurGroceries(email, password, locale="en-US")`** — optional third argument for `locale` on API payloads.

## Scripts

| Script | Role |
|--------|------|
| `scripts/add_item.py` | Adds one item; always `auto_category=True` |
| `scripts/get_list.py` | Prints list contents (`-j` JSON) |
| `scripts/remove_item.py` | Removes by name; normalizes `get_list_items` dict shape |
| `scripts/test_connection.py` | Login + list count smoke check |

Credentials: **`OURGROCERIES_EMAIL`** and **`OURGROCERIES_PASSWORD`** (env). Scripts also load optional **`env`** in the skill root (same `KEY=value` lines as shell exports); **`env` is gitignored** — never commit it. Real env vars still win (`setdefault`).

## Debugging in the browser

- **`scripts/devtools_network_monitor.js`**: paste in DevTools (or Snippets); logs POST JSON to `/your-lists`. Chrome may require typing `allow pasting` in the console before paste.

## Workspace-wide agent doc

See **`../../AGENTS.md`** (workspace root) for session rules; the OurGroceries summary is duplicated there under **Skills → OurGroceries**.
