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

租船分册（`hifleet-mytonnages/`）中 **`{base}`** 另表示**模块 API 根**（非仅主机）：路由 A 默认 `…/openclaw/vessel/charter`，路由 B 默认 `…/openclaw/vessel/charter/liner`（`…` = `HIFLEET_API_BASE` 或 `https://api.hifleet.com`）。可分别用 `hifleet_charter_api_base` / `hifleet_liner_api_base`（或 `HIFLEET_CHARTER_API_BASE` / `HIFLEET_LINER_API_BASE`）覆盖。
