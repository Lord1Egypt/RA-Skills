# Smoke Test Checklist

Run these commands from repository root after changing scripts.

## 1. Syntax Check

```bash
python -m py_compile scripts/sora_generate_video.py scripts/sora_query_video.py scripts/_config.py scripts/_validators.py scripts/_logger.py
python -m py_compile scripts/veo_generate_video.py scripts/veo_query_video.py scripts/grok_generate_video.py scripts/grok_query_video.py
python -m py_compile scripts/doubao_generate_video.py scripts/doubao_query_video.py scripts/vidu_generate_video.py scripts/vidu_query_video.py
```

## 2. Provider Entry Checks

```bash
python scripts/veo_generate_video.py "smoke test" --raw
python scripts/grok_generate_video.py "smoke test" --raw
python scripts/doubao_generate_video.py "smoke test" --raw
python scripts/vidu_generate_video.py "smoke test" --raw
```

Expected: request reaches gateway; if channel unavailable, provider may return `model_not_found`.

## 3. Query Checks

Use a known task id from generation response:

```bash
python scripts/veo_query_video.py <TASK_ID> --raw
python scripts/grok_query_video.py <TASK_ID> --raw
python scripts/doubao_query_video.py <TASK_ID> --raw
python scripts/vidu_query_video.py <TASK_ID> --raw
```

## 4. Env File Coverage

Ensure `.env` or `.env.example` includes:

- `API_BASE_URL`
- `API_KEY`
- `GEMINI_MODEL`
- `SORA_MODEL`, `SORA_SIZE`, `SORA_SECONDS`
- `VEO_MODEL`, `VEO_SIZE`, `VEO_SECONDS`
- `GROK_MODEL`, `GROK_SIZE`, `GROK_SECONDS`, `GROK_ASPECT_RATIO`
- `DOUBAO_MODEL`, `DOUBAO_SIZE`, `DOUBAO_SECONDS`
- `VIDU_MODEL`, `VIDU_SIZE`, `VIDU_DURATION`, `VIDU_ASPECT_RATIO`
- `LIBTV_ACCESS_KEY`
