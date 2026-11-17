---
name: githubcard
description: Create embeddable GitHub profile and repository card images with the ghcard CLI, design custom card layouts, and add them to README files. Use when the user wants a GitHub stats card, a profile card, a repo card or banner, a social preview image for a repository, or to put such a card in a README or profile README (github.com/<user>/<user>). Also covers listing, deleting, and checking quota for GitHubCard cards.
---

# GitHubCard cards with `ghcard`

`ghcard` turns a GitHub username or `owner/repo` into a published card image
with stable SVG/PNG links and ready-made Markdown/HTML embeds. Card images
show live GitHub data, so a card never needs regenerating to stay current.

## Before you start

1. Check the CLI is installed: `ghcard --version` (this skill is written for
   0.1.0 or later). If it is missing and Node.js 20+ is available, run it
   through npx without installing: replace `ghcard` with `npx -y @ghcardhq/ghcard` in
   every command below. Suggest `npm install -g @ghcardhq/ghcard` to the user if they
   will use it again; do not install global packages without asking.
2. Check auth: `ghcard auth status --json`.
   - Exit code 3 / `NO_API_KEY` or `UNAUTHORIZED`: the user needs a key from
     https://githubcard.com/dashboard. Ask them to run
     `ghcard auth login` themselves, or to set `GHCARD_API_KEY`.
     Never ask the user to paste the key into the chat, and never echo,
     log, or write a key into a file in the repository.
   - Listing templates/palettes works without a key.

Always pass `--json` and read stdout as one JSON document:
`{"ok": true, "data": ...}` or
`{"ok": false, "error": {"code", "message", "retryable", "hint"}}`.

## Main flows

**Card for a profile or repo** (the common case):

```bash
ghcard create octocat --json
ghcard create octocat/hello-world --json
```

Use `data.urls.svg` / `data.urls.png` for links and `data.embed.markdown`
for a README. `data.created` is `false` when the identical card already
existed, which is expected and fine.

**Add it to a README** (inserts after the first heading, or replaces the
existing `<!-- ghcard:<subject> -->` block on later runs):

```bash
ghcard create octocat --readme README.md --json
```

For a GitHub *profile* README the file lives in the repo named after the
user (`<user>/<user>/README.md`). Show the user the diff before
committing; do not commit or push unless they ask.

**Choose a look** only if the user cares about style:

```bash
ghcard templates --scope profile --free --json   # or --scope repo
ghcard templates --scope profile --free --widget streak --json   # must contain these widgets
ghcard palettes --json
ghcard create octocat --template pro-terminal --palette sage --json
```

Each template lists its `widgets`. `--palette` takes only preset ids; for
any other background colour, font, size, or widget changes, use a custom
layout (below). When several templates qualify, start from the one whose
size and widgets need the fewest edits.

Template scope must match the subject: profile templates for a user,
repo templates for `owner/repo` (templates with scope `all` fit both).
Prefer templates with `"pro": false` unless the user has Pro
(`ghcard usage --json` → `data.tier`).

**Custom layout** when the user wants specific widgets, colours, fonts,
or sizes that no template has:

```bash
ghcard components --json                                 # widget types
ghcard design init social --subject octocat -o design.json --json   # template as JSON (free, no quota)
# edit design.json: artboard (width, height, background.color, style.*) and layers[]
ghcard create octocat --design design.json --dry-run --json   # free check: ids, Pro features, layout
ghcard create octocat --design design.json --json            # publish it
```

Always `--dry-run` an edited design first: it catches every request error
without creating a card or using quota, and `data.warnings` lists layers
that reach outside the artboard (they would be clipped). Fix warnings
before publishing. When you darken or lighten the background a lot, also
set `artboard.style.textColor` / `secondaryTextColor` so text stays readable.

Prefer a template that already has exactly the widgets the user wants
(`--widget` to filter, then check each candidate's `widgets` for ones to
avoid); edit layers only when no template fits.

Editing rules (`ghcard design --help` has the full list):
- Layers are absolutely positioned (`x`, `y`, `width`, `height`).
  Removing one leaves its space empty; widen or move neighbours to fill it.
- Keep each layer's `id` unique and its `type` from `ghcard components`.
  `layer` is only stacking order; gaps are fine.
- The subject inside the file is ignored; the `create` argument decides
  whose data is shown. `showWatermark` is decided by the server.
- `artboard.background.color` is a full CSS background: a hex colour, or a
  gradient/pattern such as `radial-gradient(...) 0 0 / 22px 22px #0d1117`.
  Replacing it with a hex removes the template's texture; to keep the
  texture, change only the trailing base colour.
- Any plain solid colour (`"#14213d"`) is free; gradients and patterns
  are free only when they are a free preset, a `ghcard palettes` palette,
  or a free template's own background. On Free, the editor's Pro
  fonts and background presets fail with `PRO_FEATURE`; fonts and
  backgrounds that free templates already use are fine.

To change an existing card: `ghcard design get <card-id> -o design.json`,
edit, and publish again (this creates a new card; the old link keeps
working until deleted). Keep each layer's `id` unique and its `type` from
`ghcard components`. `ghcard open <card-id> --print` gives the web editor
link if the user would rather drag things around themselves.

**Download the image** instead of linking it:
`ghcard create octocat --format png --output card.png --json`.

Flags combine in one call (one quota unit): `--design`, `--format`,
`--output`, `--readme`. `--format` decides which link is printed and which
image `--output` saves; `--readme` always embeds the live SVG link. So a
PNG file *and* a README card is one call:
`--format png --output card.png --readme README.md`.

Links: share `data.urls` (live: they re-render with current GitHub data).
`data.snapshotUrls` are frozen images of the moment the card was created;
use them only when the user asks for an image that never changes.

**Manage cards:** `ghcard list --json`, `ghcard usage --json`.
`ghcard delete <id> --yes --json` breaks every place the card is
embedded, so confirm with the user first.

## Handling errors

Branch on `error.code` (or the exit code), and use `error.hint`:

| Code / exit | What to do |
| --- | --- |
| `UNKNOWN_TEMPLATE`, `TEMPLATE_SCOPE_MISMATCH` (2) | List templates for the right scope and pick a valid id |
| `UNKNOWN_PALETTE` (2) | List palettes, or drop `--palette` |
| `INVALID_REQUEST` (2) | Fix the argument named in `error.details.field` |
| `PRO_TEMPLATE` (1) | Pick a free template, or tell the user it needs Pro |
| `PRO_FEATURE` (1) | The design uses a Pro font/background (`error.details.features` lists each `path`); swap them for free ones or tell the user |
| `INVALID_DESIGN` (2) | Fix the design as `error.message` says; re-start from `ghcard design init` if unsure |
| `SUBJECT_NOT_FOUND` (4) | Check spelling; private repositories are not supported |
| `NO_API_KEY`, `UNAUTHORIZED` (3) | See "Before you start" |
| `QUOTA_EXCEEDED` (5) | Stop. Tell the user the daily quota resets at 00:00 UTC (`error.details.resetAt`) |
| `GITHUB_DATA_NOT_READY`, `GITHUB_CAPACITY` (6) | Wait `error.details.retryAfterSeconds` (or ~30s) and repeat the identical command; at most 5 attempts in total |
| `CARD_GENERATION_IN_PROGRESS`, `NETWORK_ERROR` (6) | A first card can take minutes to render. Wait ~30s and repeat the identical command; it resumes the same card. At most 5 attempts in total |
| `CARD_GENERATION_FAILED` (6) | A server-side rendering failure, not your request (a `--dry-run` that passes proves the request is fine). Repeat at most 2 more times, then stop and report it |

Failed calls are refunded (`ghcard usage` shows the same `used` before and
after), so repeating the identical command never costs extra quota. When
you stop, tell the user which step failed and the last `error.message`.
`error.hint` gives the same rule for each code.

## Things to avoid

- Calling `ghcard create` repeatedly to "refresh" a card: each call costs
  quota and the link already shows live data.
- Hand-building `githubcard.com` URLs: use the links the CLI returns.
- Passing `--no-watermark` on a Free account: the server keeps the
  watermark anyway; mention that removing it is a Pro feature.

## MCP alternative

If GitHubCard MCP tools are available (`create_card`, `validate_card`,
`list_templates`, `list_palettes`, `list_components`, `get_template_design`,
`get_card_design`, `list_cards`, `delete_card`, `get_usage`), they do the
same things and return the same error codes; use whichever is available.
This plugin adds the hosted server at `https://githubcard.com/mcp`. Its tools
cannot edit files, so insert `embed.markdown` into the README yourself, or
use `ghcard create ... --readme`.
