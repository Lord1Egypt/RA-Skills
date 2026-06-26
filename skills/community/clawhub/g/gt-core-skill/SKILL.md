---
name: gumtree-skills
description: |
  Use this skill when the user needs to work with Gumtree in a real Chrome browser session.
  It runs the local Python CLI and Chrome extension bridge to:
  - check login state
  - log in or out
  - search listings
  - read home recommendations, favourites, detail pages, and messages
  - favourite a listing
  - start the post-ad category flow
---

# Gumtree Skills

Use this skill only for Gumtree tasks that must run in a real browser via this repository's bridge.

## When To Use

- The user wants to inspect Gumtree content from a live browser session instead of plain HTTP scraping.
- The user wants to check login state, log in, log out, search listings, open favourites, read a detail page, send a Gumtree message, or start the post-ad flow.
- The user already has or can provide a Gumtree listing URL, keyword, login credentials, message text, or post-ad keyword.

## What This Skill Does

- Runs Gumtree actions through `uv run python scripts/cli.py ...`.
- Uses a local WebSocket bridge server plus the Chrome extension in `extension/`.
- Returns structured JSON from the CLI and should preserve key result fields in the final answer.

## Hard Boundaries

- Do not use unofficial alternate Gumtree automation projects or invent nonexistent Gumtree APIs.
- Do not run commands with system `python` or a random virtualenv; use `uv run`.
- Do not claim support for features outside the implemented commands.
- Current scope stops at category selection for `post-ad`; filling and submitting the final ad form is not implemented.

## Setup And Environment

Work from the directory that contains `SKILL.md`, `pyproject.toml`, `uv.lock`, `scripts/`, and `extension/`.

Prerequisites:

- Python 3.11+
- `uv`
- Google Chrome

First-time setup:

1. Run `uv sync`.
2. Open `chrome://extensions/`.
3. Enable Developer Mode.
4. Load the unpacked extension from `extension/`.
5. Confirm `Gumtree Bridge` is enabled.

Runtime notes:

- The CLI automatically checks and starts the local bridge server if needed.
- If the extension is not connected, the CLI may open Chrome and wait for the extension bridge.
- If you see `No module named 'websockets'`, run from this project directory and use `uv run` after `uv sync`.

## Command Routing

Use these commands exactly from the project root:

- Check login: `uv run python scripts/cli.py check-login`
- Login: `uv run python scripts/cli.py login --username "<email>" --password "<password>"`
- Logout: `uv run python scripts/cli.py logout`
- Search: `uv run python scripts/cli.py search --keyword "<keyword>"`
- Home recommendations: `uv run python scripts/cli.py home-recommend`
- Favourites: `uv run python scripts/cli.py favourites`
- Detail page: `uv run python scripts/cli.py detail --url "<detail-url>"`
- Favourite detail page: `uv run python scripts/cli.py detail-favourite --url "<detail-url>"`
- Messages: `uv run python scripts/cli.py messages`
- Detail message flow: `uv run python scripts/cli.py detail-message --url "<detail-url>"`
- Post ad category flow: `uv run python scripts/cli.py post-ad --keyword "<keyword>"`

Installed entrypoint variants are also valid:

- `uv run gumtree-skills ...`

## Search And Filter Rules

For `search`, add optional flags only when the user asks for filtering or sorting:

- `--limit <N>`
- `--search-location <location>`
- `--search-category <category>`
- `--sort relevance|date|price_lowest_first|price_highest_first|distance`
- `--distance <N>`
- `--min-price <N>`
- `--max-price <N>`
- `--condition as_good_as_new|good|new|fair` and repeat when needed
- `--seller-type trade|private` and repeat when needed
- `--mobile-storage-capacity <value>`
- `--common-for-sale-colour <value>`
- `--mobile-model-apple <value>`

Preserve Gumtree's default search behavior unless the user asks to constrain it.

## Feature-Specific Notes

### Login State

- `check-login` should treat page-embedded JS data as the primary source of truth.
- `__GUMTREE_ANALYTICS_CONFIG__`, `initialDataLayer`, `gumtreeDataLayer`, `legacy.loggedIn`, and `window.clientData` are stronger signals than DOM text.
- DOM labels such as `Manage my Ads`, `My Orders`, `Favourites`, `My Alerts`, `My Details`, `Login`, and `Sign up` are only fallbacks.

### Authentication

- `login` uses the page login modal, switches to email login, then submits the email and password.
- Credential arguments appear in shell history; avoid unnecessary repetition in summaries.
- `logout` uses the user menu and submits `logout-form`.

### Favourites

- `favourites` opens `https://www.gumtree.com/my-account/favourites`.
- The extractor prefers `window.clientData.favouriteAds.adverts`.
- If the user is not logged in, Gumtree may redirect to login or return empty results.

### Detail Favourite

- `detail-favourite` requires a logged-in session.
- It checks favourite state before and after clicking and may return flags such as `already_favourited` or `just_favourited`.

### Messages

- `messages` opens `https://www.gumtree.com/manage/messages`.
- Add `--conversation-id "<id>"` to target a specific conversation.
- Add `--message "<text>"` to send a message in the current or selected conversation.
- `detail-message` first enters messaging from the listing detail page, then reads or sends messages.
- `messages` and `detail-message` both require a logged-in session.

### Post Ad

- `post-ad` calls Gumtree's category suggestion API with the provided keyword.
- With only `--keyword`, it returns suggested categories for user confirmation.
- Add `--category-name "<name>"` for fuzzy name matching.
- Add `--category-index <index>` to pick a suggestion directly.
- After category selection it navigates to `/postad/create?categoryId=<id>`.

## Response Handling

- The CLI prints JSON and exits with `0` on success or `2` on failure.
- Keep the JSON structure intact when possible and summarize only the most important fields.
- If a command fails, report the CLI error instead of fabricating results.

## Known Limitations

- No session import mode.
- No official Gumtree API mode.
- No favourite sync or general favourite management beyond `detail-favourite`.
- `post-ad` stops after category selection and redirect.
- All content extraction depends on the live browser DOM and embedded page data, so site changes may require script updates.
