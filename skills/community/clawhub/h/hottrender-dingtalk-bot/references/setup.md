# Setup And Portability

This skill includes a minimal, sanitized HotTrender crawler runtime. It is designed for users who only need to inspect:

- Four-region daily hotspot trends: `jp`, `us`, `tw`, `kr`
- Vertical/custom-keyword hotspots, such as `乙游`, `短剧`, `AI男友`, or any user-provided keyword

It intentionally excludes DingTalk push, OSS publishing, ActionCard pages, lp-ads workspace, worker queues, databases, and LLM summaries.

## Install Bundled Runtime

From the installed skill directory:

```bash
python assets/install_hottrender_runtime.py --target ./HotTrenderRuntime
export HOTTRENDER_APP_DIR="$PWD/HotTrenderRuntime"
cd "$HOTTRENDER_APP_DIR"
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m pytest tests/test_basic_crawler.py -q
```

The installer copies `assets/hottrender-runtime/`, creates `out`, and copies `.env.example` to `.env`.

## Default Dependencies

The basic runtime defaults to lightweight dependencies:

- `requests`
- `beautifulsoup4`
- `PyYAML`
- `pytest`

TikTok is optional because it requires Playwright and a usable TikTok session/network environment:

```bash
pip install -r requirements-tiktok.txt
python -m playwright install
export TIKTOK_MS_TOKEN=...
```

## Provider Config

Provider settings live in:

```text
configs/providers.yaml
```

Use `mode: offline` for deterministic local tests without network access. Use `mode: real` for live crawling.

## What This Runtime Can Do

Daily four-region trends:

```bash
python scripts/fetch_daily_trends.py --output out/daily_trends.md
```

Custom keyword hotspots:

```bash
python scripts/fetch_keyword_hotspots.py --keywords "乙游,短剧,AI男友" --output out/keyword_hotspots.md
```

Both commands write Markdown for human reading and a sibling JSON file for raw records.
