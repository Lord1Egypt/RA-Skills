# pmtools

Feishu OKR skill for OpenClaw/agents.

## Environment variables

- `FEISHU_APP_ID`: Feishu app id (recommended).
- `FEISHU_APP_SECRET`: Feishu app secret (recommended).
- `FEISHU_ACCESS_TOKEN`: Optional override token used for API calls.
- `FEISHU_TENANT_ACCESS_TOKEN`: Optional override tenant token (used by `reviews-query`).
- `FEISHU_OPEN_API_BASE_URL`: Override OpenAPI base URL for auth; default is `https://open.feishu.cn/open-apis`.
- `FEISHU_OKR_BASE_URL`: Override base URL for testing; default is `https://open.feishu.cn/open-apis/okr/v1`.

## Run tests

From repo root:

```bash
python3 -m unittest discover -s skills/pm_tools/tests -v
```
