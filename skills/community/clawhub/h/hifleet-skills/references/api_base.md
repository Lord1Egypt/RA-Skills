# API 基址 / API Base URL

本技能内所有 HiFleet API 文档与 Agent 构造请求时，使用占位符 **`{base}`** 表示 API 根地址（**不含**末尾 `/`）。

| 项 | 值 |
|----|-----|
| 默认 `{base}` | `https://api.hifleet.com` |
| 其它部署 | 环境变量 **`HIFLEET_API_BASE`** |
| 完整 URL | `{base}` + 路径，例如 `{base}/position/getcallport/token`、`{base}/pscapi/get` |

`scripts/` 下 Python 脚本统一：

```python
def api_base():
    return (os.environ.get("HIFLEET_API_BASE") or "https://api.hifleet.com").rstrip("/")
```

租船分册 API 根（`…` = `HIFLEET_API_BASE` 或 `https://api.hifleet.com`）：

| 分册 | 默认根 |
|------|--------|
| **`hifleet-schedule/`** 班轮船期 | `…/openclaw/vessel/charter/liner`（`hifleet_liner_api_base` / `HIFLEET_LINER_API_BASE`） |
| **`hifleet-opentonnages/`** 公开船/货盘 | `…/openclaw/vessel/charter`（`vessels/search`、`cargo/search`；同 `hifleet_charter_api_base`） |
