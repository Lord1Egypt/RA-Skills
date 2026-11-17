# Infoseek 凭证工具选型（Tier 2.5）+ KeyManager 归一化管理

> 版本：v1.0.1 ｜ 状态：✅ 已提供 ｜ 对齐全：`scripts/infoseek_pipeline.py::CREDENTIAL_TOOLS` / `request_credential` / `core/key_manager.py`

## 0. KeyManager 归一化 Key 管理（v1.0.1 新增）

所有 API key 统一经 `core/key_manager.py::KeyManager` 读取，替代散落的 `os.environ.get()`：

| 能力 | 说明 |
|------|------|
| 统一入口 | `KeyManager.get(provider)` → str；未注册时退化读 env（向后兼容） |
| 多后端 | Env（默认）→ Dotenv（.env 文件，标准库解析，不覆盖已有 env）→ 会话注册（多 key 池） |
| 状态机 | CONFIGURED → ACTIVE → DEGRADED → CIRCUIT_OPEN → ROTATING → REVOKED |
| 熔断 | 连续失败 3 次 DEGRADED / 5 次 CIRCUIT_OPEN（60s 冷却），成功回注恢复 |
| 多 key 池 | `register()` 同 provider 多 key，least-used 选择（配额余量/失败数最小） |
| 配额感知 | `set_quota(provider, limit)` 用尽自动切换下一 key → env → '' |
| 用量统计 | `stats()` 脱敏输出 + `persist_usage()` 落盘 `~/.infoseek/key_usage.json` |
| 生命周期 | `rotate()` 轮换重排 / `revoke()` 按指纹吊销 |

阈值经 env 覆盖：`INFOSEEK_KEY_FAIL_THRESHOLD`（3）/ `INFOSEEK_KEY_CIRCUIT_THRESHOLD`（5）/ `INFOSEEK_KEY_CIRCUIT_COOLDOWN`（60）/ `INFOSEEK_DOTENV`（.env 路径）。

已接入模块：`llm_router`（6 LLM provider）、`pipeline`（5 搜索引擎）、`mcp_server`/`summarize_adapter`（INFOSEEK_LLM_API_KEY）。


## 1. 定位

4 级降级链中的 **Tier 2.5**：免费工具（Tier1）与浏览器渲染（Tier2）之间，需用户提供凭证才能继续的降级层。

```
Tier 1 静态抓取 → Tier 2 反爬兜底 → [Tier 2.5 凭证辅助] → Tier 3 凭证执行 → Tier 4 多媒体
```

**核心原则：不自动执行、不保存凭证（SESSION_ONLY）** —— `request_credential()` 仅返回操作指引模板，由用户在会话中决定是否提供 key。

## 2. 可选工具清单

| id | 名称 | 成本 | 凭证类型 | 端点 |
|----|------|------|----------|------|
| `firecrawl` | Firecrawl API | 免费层 1000 页/月 | API Key | `https://api.firecrawl.dev/v1/scrape` |
| `jina_reader` | Jina Reader API | 免费层 | API Key | `https://r.jina.ai/http://<url>` |
| `wechat_exporter` | wechat-article-exporter | 免费 | 浏览器扫码 | 本地 docker Web 界面 |

## 3. 降级触发条件（degradation_router 状态机）

| 条件 | 动作 |
|------|------|
| HTTP 404/410 | final（内容不存在） |
| HTTP 403 / Cloudflare 特征 | tier2（反爬拦截） |
| 无标题无正文 | tier2（JS 渲染/SPA） |
| 有标题无正文 | tier2 |
| 标题 + 正文 >100 字 | done（Tier1 成功） |
| 标题 + 正文 <100 字 | tier2（正文过短） |
| Tier2 返回 video/audio/live | tier3（媒体类型） |
| Tier2 正文 >50 字 | done（Tier2 成功） |
| 其余 | tier3 |

## 4. 凭证安全策略

- `credential_policy: SESSION_ONLY` —— 凭证仅存会话内存，不写磁盘
- `request_credential()` 不自动执行任何第三方调用
- 密钥 env 注入：`DEEPSEEK_API_KEY` / `KIMI_API_KEY` 等经 MCP 客户端 env 传入

## 5. 当前实现状态

- `_tier2_execute` / `_tier3_execute` 为函数壳（标注"需选装"），真实浏览器渲染需安装 `playwright`（requirements-extra.txt）
- 凭证工具仅输出指引模板，实际调用由宿主集成方实现
