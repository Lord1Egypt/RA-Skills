# API 录制指南（`api_call`）

录制器支持 **`api_call`** 步骤：通过 **httpx** 发起 **GET/POST** 等请求，响应可选保存到桌面。字段说明见 [**SKILL.zh-CN.md**](../SKILL.zh-CN.md) 中「单步录制协议」表格的 **`api_call`** 行；组合流程见典型场景 1。

---

## `api_call` 做什么

在录制会话里增加一步：**向指定 URL 发 HTTP 请求**（与当前浏览器页面无关），可选把返回内容写到桌面文件（`save_response_to`）。

---

## 密钥写入策略

在 `record-step` JSON 的 `params` 或 `headers` 中，用占位符 **`__ENV:环境变量名__`**；同时在同一步骤带上 **`"env": {"变量名": "真实密钥"}`** 字段：

```json
{
  "action": "api_call",
  ...,
  "params": {"apikey": "__ENV:ALPHAVANTAGE_API_KEY__", ...},
  "env": {"ALPHAVANTAGE_API_KEY": "你的真实密钥"}
}
```

代码生成器检测到 `env` 字段后，会把真实密钥**直接写入生成脚本**——回放时**无需 `export`**，脚本可直接运行。

若不提供 `env`，则生成 `os.environ.get("变量名", "")`，运行前需手动 `export 变量名=…`。

**占位符小结：** 用 **`__ENV:变量名__`** + **`"env"` 字段**同时使用 → 密钥写入脚本，无需额外 `export`。

---

## Alpha Vantage 日线示例（对应案例 §3）

文档：[TIME_SERIES_DAILY](https://www.alphavantage.co/documentation/#daily)。`record-step` 典型写法：

- `base_url` + `params`（含 `function`、`symbol`、`outputsize` 等）
- `apikey` 填 `"__ENV:ALPHAVANTAGE_API_KEY__"`
- `env` 填真实密钥
- `save_response_to` 填输出文件名

---

## 混合流程：行情 + 新闻页 + 本地简报

同一录制任务可：
1. 通过 `api_call` 拉行情 JSON 落盘
2. 浏览器打开新闻页
3. `extract_text` 写入同一简报文件名（追加规则见 [SKILL.zh-CN.md 典型场景 1](../SKILL.zh-CN.md)）

**给非技术用户看的任务提示词**见 [README.zh-CN.md — 案例 §3](../README.zh-CN.md#api-quotes-news-brief-zh)。

---

## 说明与边界

- **合规**：请遵守各网站服务条款与使用政策；本仓库不鼓励绕过风控或在禁止场景下抓取数据。
- **强风控站点（如 LinkedIn）**：即便支持自动登录或会话复用，仍可能遇到 **2FA、设备验证、验证码、风控拦截**，需要**人工介入**。
