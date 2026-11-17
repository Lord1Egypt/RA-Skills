# API 参考 — 行业雷达 Industry Radar

服务基地址：`http://127.0.0.1:8000`（以启动器实际 `--host/--port` 为准）
认证方式：除 `/api/login`、`/api/sources`、`/api/config` 外，均需请求头 `Authorization: Bearer <token>`。
交互式文档：`http://127.0.0.1:8000/docs`（FastAPI 自动生成）。

## 认证与系统

### POST /api/login

```bash
curl -s -X POST http://127.0.0.1:8000/api/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"demo","password":"demo"}'
```

响应：

```json
{"token": "a1b2c3...", "username": "demo", "user_id": 1}
```

> Token 存于内存，服务重启后失效，需重新登录。

### GET /api/config（无需认证，可当探活用）

```json
{"llm_enabled": false, "mode": "离线规则引擎（可配置 LLM）", "version": "1.1.0"}
```

### GET /api/sources（无需认证）

返回全部内置数据源元数据（14 源）。自定义源不在此列表，见下文「自定义源」。

| id            | 名称            | 语言 |
| ------------- | --------------- | ---- |
| 36kr          | 36氪            | zh   |
| ithome        | IT之家          | zh   |
| tmtpost       | 钛媒体          | zh   |
| leiphone      | 雷锋网          | zh   |
| infoq_cn      | InfoQ 中文      | zh   |
| sspai         | 少数派          | zh   |
| oschina       | 开源中国        | zh   |
| solidot       | Solidot 奇客    | zh   |
| zhihu_daily   | 知乎每日精选    | zh   |
| huxiu         | 虎嗅            | zh   |
| jiqizhixin    | 机器之心        | zh   |
| techcrunch    | TechCrunch      | en   |
| verge         | The Verge       | en   |
| ars           | Ars Technica    | en   |

## 自定义源

自定义源是用户自己录入的 RSS/Atom 地址，按 `user_id` 隔离，只能被本人订阅引用。
总开关 `IR_ALLOW_CUSTOM_SOURCES=0` 时，写操作全部返回 `403`（列表仍可读，`enabled` 为 `false`）。

### GET /api/custom-sources

```json
{"enabled": true,
 "sources": [
   {"id": 7, "user_id": 1, "name": "阮一峰的网络日志",
    "url": "https://www.ruanyifeng.com/blog/atom.xml",
    "enabled": 1, "status": "ok", "fail_count": 0,
    "last_status": "ok", "last_error": null,
    "last_fetch_at": "2026-10-20 22:41:07", "created_at": "...",
    "used_by": 1}
 ],
 "limits": {"max_per_user": 10, "max_per_sub": 5}}
```

| 字段         | 说明                                                             |
| ------------ | ---------------------------------------------------------------- |
| `enabled`    | 全局开关状态；`false` 表示该实例关闭了自定义源能力                |
| `status`     | `ok` 正常 / `disabled` 连续失败被自动停用                        |
| `fail_count` | 连续失败次数，成功一次即清零                                     |
| `last_*`     | 最近一次抓取的时间、结果、错误信息（`last_error` 供排查）        |
| `used_by`    | 被多少个订阅引用，删除前可参考                                   |

### POST /api/custom-sources

```json
{"name": "阮一峰的网络日志", "url": "https://www.ruanyifeng.com/blog/atom.xml"}
```

录入即探活：内部先过 `net_guard.check_url()`，再实抓一次并要求解析到 ≥1 条，否则 `400`。

响应：`{"id": 7, "items": 3, "message": "已添加，首次抓取到 3 条"}`

常见 `400`：名称空/超 60 字符、地址非法或解析不出条目、`text/html` 等非 RSS/Atom、
数量超上限（`自定义源数量已达上限（10 个）`）、地址重复（`该源已存在，无需重复添加`）。

### PUT /api/custom-sources/{cs_id}

Body 字段均可选：`name` / `url` / `enabled`（布尔）。

```json
{"enabled": false}
```

改 `url` 会重新探活，失败则拒绝；把被自动停用的源重新 `enabled=true`
会清零 `fail_count`，给它一次干净的重试机会。响应：`{"message": "更新成功"}`
（改过 URL 时额外带 `items`）。非本人源一律 `404`。

### DELETE /api/custom-sources/{cs_id}

响应：`{"message": "已删除"}`。会先把引用它的订阅里对应的 `cs:<id>` 摘掉，
不会留下指向空源的订阅。

### POST /api/custom-sources/{cs_id}/test

手动复检，重新走出站校验 + 抓取，并把结果写回健康状态字段（不写入文章库）。

```json
{"ok": true, "items": 3, "error": ""}
```

失败时 HTTP 仍为 200，但 `ok=false`，`error` 给出原因（例如 `不是 RSS/Atom（Content-Type: text/html）`）；
地址已不再允许访问时返回 `400`。

### 在订阅里引用

订阅的 `sources` 数组里写 `"cs:<cs_id>"`：

```json
{"name": "前端 × 开源", "industry_kw": "前端", "tech_kw": "开源",
 "sources": ["36kr", "cs:7"]}
```

- 只能引自己名下且 `enabled=1` 的源，引用别人的 `cs:<id>` 会被静默过滤（不报错，但抓不到内容）
- 单订阅最多引用 5 个自定义源，超出的部分同样被过滤
- 采集时与内置源一起串行抓取，共享同一份超时预算，抓取结果会回写 `last_status` / `last_error`
- 条目在简报里归入「自定义」分类

## 自定义源

自定义源是用户自己录入的 RSS/Atom 地址，按 `user_id` 隔离，只能被本人订阅引用。
总开关 `IR_ALLOW_CUSTOM_SOURCES=0` 时，写操作全部返回 `403`（列表仍可读，`enabled` 为 `false`）。

### GET /api/custom-sources

```json
{"enabled": true,
 "sources": [
   {"id": 7, "user_id": 1, "name": "阮一峰的网络日志",
    "url": "https://www.ruanyifeng.com/blog/atom.xml",
    "enabled": 1, "status": "ok", "fail_count": 0,
    "last_status": "ok", "last_error": null,
    "last_fetch_at": "2026-10-20 22:41:07", "created_at": "...",
    "used_by": 1}
 ],
 "limits": {"max_per_user": 10, "max_per_sub": 5}}
```

| 字段         | 说明                                                             |
| ------------ | ---------------------------------------------------------------- |
| `enabled`    | 全局开关状态；`false` 表示该实例关闭了自定义源能力                |
| `status`     | `ok` 正常 / `disabled` 连续失败被自动停用                        |
| `fail_count` | 连续失败次数，成功一次即清零                                     |
| `last_*`     | 最近一次抓取的时间、结果、错误信息（`last_error` 供排查）        |
| `used_by`    | 被多少个订阅引用，删除前可参考                                   |

### POST /api/custom-sources

```json
{"name": "阮一峰的网络日志", "url": "https://www.ruanyifeng.com/blog/atom.xml"}
```

录入即探活：内部先过 `net_guard.check_url()`，再实抓一次并要求解析到 ≥1 条，否则 `400`。

响应：`{"id": 7, "items": 3, "message": "已添加，首次抓取到 3 条"}`

常见 `400`：名称空/超 60 字符、地址非法或解析不出条目、`text/html` 等非 RSS/Atom、
数量超上限（`自定义源数量已达上限（10 个）`）、地址重复（`该源已存在，无需重复添加`）。

### PUT /api/custom-sources/{cs_id}

Body 字段均可选：`name` / `url` / `enabled`（布尔）。

```json
{"enabled": false}
```

改 `url` 会重新探活，失败则拒绝；把被自动停用的源重新 `enabled=true`
会清零 `fail_count`，给它一次干净的重试机会。响应：`{"message": "更新成功"}`
（改过 URL 时额外带 `items`）。非本人源一律 `404`。

### DELETE /api/custom-sources/{cs_id}

响应：`{"message": "已删除"}`。会先把引用它的订阅里对应的 `cs:<id>` 摘掉，
不会留下指向空源的订阅。

### POST /api/custom-sources/{cs_id}/test

手动复检，重新走出站校验 + 抓取，并把结果写回健康状态字段（不写入文章库）。

```json
{"ok": true, "items": 3, "error": ""}
```

失败时 HTTP 仍为 200，但 `ok=false`，`error` 给出原因（例如 `不是 RSS/Atom（Content-Type: text/html）`）；
地址已不再允许访问时返回 `400`。

### 在订阅里引用

订阅的 `sources` 数组里写 `"cs:<cs_id>"`：

```json
{"name": "前端 × 开源", "industry_kw": "前端", "tech_kw": "开源",
 "sources": ["36kr", "cs:7"]}
```

- 只能引自己名下且 `enabled=1` 的源，引用别人的 `cs:<id>` 会被静默过滤（不报错，但抓不到内容）
- 单订阅最多引用 5 个自定义源，超出的部分同样被过滤
- 采集时与内置源一起串行抓取，共享同一份超时预算，抓取结果会回写 `last_status` / `last_error`
- 条目在简报里归入「自定义」分类

## 订阅管理

### GET /api/subscriptions

响应（每项含 `briefing_count` 统计）：

```json
{"subscriptions": [
  {"id": 1, "user_id": 1, "name": "新能源汽车 × 固态电池",
   "industry_kw": "新能源汽车,汽车", "tech_kw": "固态电池,电池,续航",
   "extra_kw": "量产,车企", "sources_json": "[\"36kr\",\"zhihu_daily\",\"techcrunch\"]",
   "frequency": "weekly", "style": "curated", "enabled": 1,
   "last_run_at": "2026-10-20 16:19:26", "created_at": "...", "briefing_count": 4}
]}
```

### POST /api/subscriptions

```json
{
  "name": "智能眼镜 × 端侧AI",
  "industry_kw": "智能眼镜,AR眼镜",
  "tech_kw": "端侧AI,大模型",
  "extra_kw": "",
  "sources": ["36kr", "ithome", "jiqizhixin"],
  "frequency": "weekly",
  "style": "curated"
}
```

| 字段          | 必填 | 说明                                                        |
| ------------- | ---- | ----------------------------------------------------------- |
| name          | 是   | 订阅名称                                                    |
| industry_kw   | 是   | 行业词，逗号分隔                                            |
| tech_kw       | 是   | 技术词，逗号分隔                                            |
| extra_kw      | 否   | 附加过滤词                                                  |
| sources       | 否   | 数据源 id 数组（内置源 key 或 `cs:<自定义源 id>`），空则用默认启用源 |
| frequency     | 否   | `weekly`（当前仅此值）                                      |
| style         | 否   | `standard` 标准周报 / `curated` 编辑精选（推荐）            |

响应：`{"id": 2, "message": "创建成功"}`

### PUT /api/subscriptions/{sub_id}

Body 传需要修改的字段（同上，均可选，另支持 `enabled` 0/1）。响应：`{"message": "更新成功"}`

### DELETE /api/subscriptions/{sub_id}

响应：`{"message": "已删除"}`。注意：历史简报 `.md` 文件保留在磁盘。

## 生成与预览

### POST /api/subscriptions/{sub_id}/run

同步执行整条流水线（采集→清洗→去重→打分→聚类→摘要→成稿），约 30–120 秒。
HTTP 客户端超时建议 ≥ 180 秒（curl 加 `--max-time 300`）。

```json
{"briefing_id": 5, "title": "智能眼镜 × 端侧AI 行业周报（第 1 期）",
 "stats": {"collected": 62, "deduped": 41, "kept": 12, "clusters": 4},
 "message": "简报生成完成"}
```

> 只补增量：simhash 去重会跳过已入库文章，短时间内重复 run 新文章很少。

### POST /api/preview

与 run 相同流水线但**不落库**，适合试关键词。Body：

```json
{"industry_kw": "人形机器人", "tech_kw": "具身智能", "extra_kw": "", "sources": ["36kr", "jiqizhixin"]}
```

响应：`{"markdown": "# ...", "stats": {...}}`

## 读取与导出

### GET /api/articles?subscription_id=1&limit=100

返回已入库文章（id/title/url/source_name/published_at/summary/score）。

### GET /api/briefings?subscription_id=1

简报列表（不含 md_path）。

### GET /api/briefings/{briefing_id}

单份简报详情，含完整 `markdown` 字段。

### GET /api/briefings/{briefing_id}/export

以 `text/markdown` 附件形式下载（Content-Disposition: briefing_<id>.md）。

### GET /api/trend?subscription_id=1

每期简报的 stats 时间序列 + 各源文章数分布。

### GET /api/dashboard

```json
{"subscription_count": 4, "briefing_count": 16, "article_count": 512, "llm_enabled": false}
```

## 数据落盘位置

| 数据     | 位置                                             |
| -------- | ------------------------------------------------ |
| SQLite   | `app/data/industry_radar.db`（可用 `IR_DB_PATH` 覆盖） |
| 简报 .md | `app/data/briefings/sub<N>_<日期>_<时间>.md`     |

> 数据库删除后下次启动自动重建；简报 .md 不受影响。
