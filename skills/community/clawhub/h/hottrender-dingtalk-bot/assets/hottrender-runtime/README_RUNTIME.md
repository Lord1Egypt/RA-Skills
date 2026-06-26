# HotTrender Basic Crawler Runtime

This runtime is intentionally small. It only supports:

- Four-region daily hotspot trend crawling: `jp`, `us`, `tw`, `kr`
- Custom keyword / vertical hotspot crawling
- Markdown and JSON outputs for local inspection

It does not include DingTalk push, OSS publishing, ActionCard, lp-ads workspace, worker queues, databases, or LLM summaries.

## Install

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Daily Trends

```bash
python scripts/fetch_daily_trends.py --output out/daily_trends.md
```

Default platforms are `google,youtube,x`. `x` uses Trends24 and may not support every region; unsupported regions are reported in the `抓取失败` section instead of being faked.

## Custom Keyword Hotspots

```bash
python scripts/fetch_keyword_hotspots.py \
  --keywords "乙游,短剧,AI男友" \
  --regions jp,us,tw,kr \
  --platforms google,youtube \
  --output out/keyword_hotspots.md
```

## Optional TikTok

TikTok is not a default dependency because it requires Playwright and a usable network/session environment.

```bash
pip install -r requirements-tiktok.txt
python -m playwright install
export TIKTOK_MS_TOKEN=...
python scripts/fetch_daily_trends.py --platforms tiktok --output out/tiktok_trends.md
```

## Offline Test Mode

Set provider `mode: offline` in `configs/providers.yaml` for deterministic local tests without network access.
