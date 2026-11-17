# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.3.0] - 2026-07-07

### Added

- add universal installers for AI agent skill distribution ([17e55df](https://github.com/CripterHack/ig-downloader-skill/commit/17e55df))

## [2.2.3] - 2026-07-07

### Other

- replace USERNAME placeholders with cripterhack ([1fc2c51](https://github.com/CripterHack/ig-downloader-skill/commit/1fc2c51))

## [2.2.2] - 2026-07-07

### Added

- **setup:** add Playwright-based interactive setup with Chromium ([94bfc53](https://github.com/CripterHack/ig-downloader-skill/commit/94bfc53))
- **config:** add Chrome cookie extraction, config management, and interactive setup ([cbac97f](https://github.com/CripterHack/ig-downloader-skill/commit/cbac97f))
- add SKILL.md for Claude/OpenCoder agent integration ([724f72d](https://github.com/CripterHack/ig-downloader-skill/commit/724f72d))
- add Instagram downloader CLI script v1.1.0 ([c81ecbb](https://github.com/CripterHack/ig-downloader-skill/commit/c81ecbb))

### Fixed

- **release:** specify remote branch for git push in workflow_run context ([78f11ff](https://github.com/CripterHack/ig-downloader-skill/commit/78f11ff))
- replace deprecated setuptools.backends._legacy with setuptools.build_meta ([0f47ced](https://github.com/CripterHack/ig-downloader-skill/commit/0f47ced))
- **docs:** update script docstring to v2.2, remove broken login mode promotion, add warning ([0f68646](https://github.com/CripterHack/ig-downloader-skill/commit/0f68646))
- **cli:** add -u short alias for --username flag ([d6ee6ae](https://github.com/CripterHack/ig-downloader-skill/commit/d6ee6ae))

### Other

- **project:** enforce global-only opencode and add auto-release workflow ([9482284](https://github.com/CripterHack/ig-downloader-skill/commit/9482284))
- add GitHub Actions workflow — pytest matrix (3.10-3.12), CLI verification, import check ([d816ab1](https://github.com/CripterHack/ig-downloader-skill/commit/d816ab1))
- **readme:** add Mermaid data flow and Playwright sequence diagrams ([2cd27ea](https://github.com/CripterHack/ig-downloader-skill/commit/2cd27ea))
- **agents:** replace ASCII decision tree with Mermaid flowchart ([7cd2253](https://github.com/CripterHack/ig-downloader-skill/commit/7cd2253))
- **skill:** replace ASCII architecture with Mermaid diagrams (modes, sessionid flow, setup chain) ([7f4d72e](https://github.com/CripterHack/ig-downloader-skill/commit/7f4d72e))
- **readme:** update README.md to v2.2 — remove login references, add broken login warning, promote Playwright ([9afa78c](https://github.com/CripterHack/ig-downloader-skill/commit/9afa78c))
- **skill:** update SKILL.md to v2.2 — remove login mode, promote sessionid + Playwright setup ([97cf4c9](https://github.com/CripterHack/ig-downloader-skill/commit/97cf4c9))
- bump pyproject.toml to v2.2.0, add playwright dependency ([cb85b59](https://github.com/CripterHack/ig-downloader-skill/commit/cb85b59))
- **agents:** add AGENTS.md with mode selection logic, decision tree, and agent instructions ([88f3793](https://github.com/CripterHack/ig-downloader-skill/commit/88f3793))
- **changelog:** add v2.2.0 entry for Playwright interactive setup ([857fd1c](https://github.com/CripterHack/ig-downloader-skill/commit/857fd1c))
- **readme:** update README.md to v2.1 — login mode, authentication docs, updated FAQ ([a160c42](https://github.com/CripterHack/ig-downloader-skill/commit/a160c42))
- **skill:** update SKILL.md to v2.1 — login mode with 2FA, challenge handling, saved sessions, 4-mode architecture ([af6e105](https://github.com/CripterHack/ig-downloader-skill/commit/af6e105))
- **changelog:** add v2.0.0 entry — sessionid mode, setup wizard, config management, Chrome cookie extraction ([e352843](https://github.com/CripterHack/ig-downloader-skill/commit/e352843))
- **readme:** rewrite README.md for v2.0 — sessionid quick-start, three-mode comparison, setup wizard, cookie extraction guide ([b0ada50](https://github.com/CripterHack/ig-downloader-skill/commit/b0ada50))
- **skill:** rewrite SKILL.md for v2.0 — sessionid mode, setup wizard, three-mode architecture, config management ([4e91ce8](https://github.com/CripterHack/ig-downloader-skill/commit/4e91ce8))
- **script:** update docstring for v2.0 three-mode architecture (sessionid, Apify, setup) ([19129ee](https://github.com/CripterHack/ig-downloader-skill/commit/19129ee))
- remove backup files, add to .gitignore ([5e26048](https://github.com/CripterHack/ig-downloader-skill/commit/5e26048))
- add unit tests for parser, normalizer, and filter logic ([5c1991f](https://github.com/CripterHack/ig-downloader-skill/commit/5c1991f))
- add GitHub issue and PR templates ([c704928](https://github.com/CripterHack/ig-downloader-skill/commit/c704928))
- add CHANGELOG.md with version history ([2c1b84c](https://github.com/CripterHack/ig-downloader-skill/commit/2c1b84c))
- add CONTRIBUTING.md with contribution guidelines ([ce29675](https://github.com/CripterHack/ig-downloader-skill/commit/ce29675))
- add comprehensive README with architecture, usage, and troubleshooting ([04a8196](https://github.com/CripterHack/ig-downloader-skill/commit/04a8196))
- add pyproject.toml and requirements.txt ([6035e89](https://github.com/CripterHack/ig-downloader-skill/commit/6035e89))
- add LICENSE (GPLv2) and .gitignore ([0509221](https://github.com/CripterHack/ig-downloader-skill/commit/0509221))

## [2.2.1] - 2026-07-07

### Fixed
- **CI failing on `pip install -e .`** — `setuptools.backends._legacy:_Backend` removed in modern setuptools.
  Changed to `setuptools.build_meta` (stable backend, works with pip 26.x).

## [2.2.0] - 2026-07-07

### Added
- **Playwright browser setup** — new `try_playwright_setup()` function as primary setup path
- Launches clean Chromium (no Chrome profile dependency), waits for user login,
  extracts `sessionid` directly via Playwright's `context.cookies()` API
- **Triple fallback chain** in `--setup`: Playwright → Chrome extraction → manual paste
- `playwright>=1.48.0` added to `requirements.txt`

### Changed
- Version bumped to 2.2.0
- Interactive setup (`--setup`) now uses Playwright by default (resilient, cross-platform)
- Legacy Chrome cookie extraction kept as second fallback
- Manual sessionid paste added as third fallback

### Fixed
- Chrome cookie extraction was unreliable due to file locking, profile detection, DB format
  changes (Chrome 127+ moved to `Network/Cookies`). Playwright bypasses all of these.

## [2.1.0] - 2026-07-07

### Added
- **Login mode** (`--login`) — full username/password login via instagrapi
- **2FA support** (`--totp CODE`) — two-factor authentication for login
- **Challenge handling** — SMS/email verification codes auto-prompted during login
- **Session persistence** — `~/.ig-downloader/settings.json` saved after login, auto-reused
- **Private profile access** — download from any profile the authenticated user follows
- `--password PASS` flag (omit to prompt securely via `getpass`)
- `download_from_session()` pipeline — fetches ALL user media via `user_medias()`
- `load_or_login_client()` — priority: saved settings > sessionid > full login
- Smart mode detection: auto-routes to login/session/Apify based on available credentials

### Changed
- Version bumped to 2.1.0
- `main()` now supports 4 operation modes (Login, Sessionid, Apify, Setup)
- Authentication falls back gracefully: saved session → sessionid → login → Apify
- `--sessionid` flag still works alongside new `--login` mode

## [2.0.0] - 2026-07-07

### Added
- **Sessionid mode** — instagrapi login via browser cookie (no password, no 2FA)
- **Setup wizard** (`--setup`) — opens browser, polls for login, saves cookie to config
- **Config management** — `~/.ig-downloader/config.json`, auto-detected on each run
- **Chrome cookie extraction** — DPAPI + AES-GCM decryption for automatic sessionid retrieval
- Three-way source priority: `--sessionid` flag > `SESSIONID` env var > config file > Chrome cookies
- `--username` / `-u` flag for target Instagram handle
- `--version` flag
- Full carousel extraction via `media_info()` for ALL posts (no GQL cutoff)

### Changed
- Script auto-detects mode: sessionid (config) → setup → Apify legacy → help
- `instagrapi` is now a hard dependency for sessionid mode
- Output folder structure uses `post_info.txt` with `relation: own_post` field
- `--profile` flag renamed to `-u`/`--username`

### Removed
- `--no-instagrapi` flag (no longer needed — instagrapi is always available in sessionid mode)

## [1.1.0] - 2026-07-07

### Added
- Hybrid carousel extraction via `instagrapi` GQL (no login, no cookies)
- `--no-instagrapi` flag to disable GQL enhancement
- `InstagrapiHelper` class: lazy-init `Client`, `get_carousel_images()`, `download_url()` via `public.get()` to bypass CDN 403
- GQL stats tracking (hits/misses) in download summary
- Full carousel downloads — all images, not just thumbnail

### Changed
- Carousel processing: try GQL first (20s timeout), fallback to Apify thumbnail on failure
- Download method: use `instagrapi`'s browser-like client for CDN URLs from `fbcdn.net`
- `requirements.txt` now includes `instagrapi>=2.0.0`

### Fixed
- `fbcdn.net` CDN URLs returning 403 with plain `requests` — now use `instagrapi` `public.get()` which has proper browser headers

## [1.0.0] - 2026-07-06

### Added
- Initial release
- Apify-based Instagram media downloader
- Two input modes: `--dataset` (Apify API) and `--toon-file` (MCP export)
- Filters: `--date-start/--end`, `--type`, `--own-only`, `--mentions-only`
- Output organization: `YYYY-MM-DD/shortcode/` with `post_info.txt`
- Flat output mode: `--flat`
- Reel download (MP4) + thumbnail
- Carousel/photo download (single thumbnail JPG per post)
- Retry logic for failed downloads
- SSL verification toggle (`--no-verify`)
