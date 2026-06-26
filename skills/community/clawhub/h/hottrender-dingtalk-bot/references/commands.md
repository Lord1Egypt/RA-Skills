# Command Reference

Resolve the runtime first:

```bash
cd "$HOTTRENDER_APP_DIR"
PYTHON="${HOTTRENDER_PYTHON:-python}"
```

If there is no local runtime yet, install the bundled runtime from the Skill directory:

```bash
python assets/install_hottrender_runtime.py --target ./HotTrenderRuntime
export HOTTRENDER_APP_DIR="$PWD/HotTrenderRuntime"
cd "$HOTTRENDER_APP_DIR"
PYTHON="${HOTTRENDER_PYTHON:-python}"
```

Use the virtualenv when present:

```bash
export HOTTRENDER_PYTHON="$HOTTRENDER_APP_DIR/.venv/bin/python"
PYTHON="$HOTTRENDER_PYTHON"
```

## Four-Region Daily Trends

Default regions are `jp,us,tw,kr`; default platforms are `google,youtube,x`.

```bash
"$PYTHON" scripts/fetch_daily_trends.py --output out/daily_trends.md
```

Specify platforms:

```bash
"$PYTHON" scripts/fetch_daily_trends.py \
  --regions jp,us,tw,kr \
  --platforms google,youtube,x \
  --limit 10 \
  --output out/daily_trends.md
```

JSON-only output:

```bash
"$PYTHON" scripts/fetch_daily_trends.py --output out/daily_trends.json
```

## Custom Keyword Hotspots

Default platforms are `google,youtube`.

```bash
"$PYTHON" scripts/fetch_keyword_hotspots.py \
  --keywords "乙游,短剧,AI男友" \
  --regions jp,us,tw,kr \
  --platforms google,youtube \
  --limit 10 \
  --output out/keyword_hotspots.md
```

Single keyword:

```bash
"$PYTHON" scripts/fetch_keyword_hotspots.py --keywords "恋爱" --output out/romance.md
```

## Offline Mode

For deterministic local validation, temporarily set providers to `mode: offline` in `configs/providers.yaml`, then run:

```bash
"$PYTHON" -m pytest tests/test_basic_crawler.py -q
"$PYTHON" scripts/fetch_daily_trends.py --output out/offline_daily.md
```

## Optional TikTok

TikTok is not installed by default:

```bash
pip install -r requirements-tiktok.txt
python -m playwright install
export TIKTOK_MS_TOKEN=...
"$PYTHON" scripts/fetch_daily_trends.py --platforms tiktok --output out/tiktok_trends.md
```

If TikTok fails, keep the explicit error in the report. Do not replace it with fake data.
