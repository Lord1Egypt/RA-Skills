# OPC 赛事收录 API 完整对接文档

> 可直接复制给其他 AI 使用。

---

## 1. 接口信息

- **方法**：`POST`
- **路径**：`/api/events/ingest`
- **生产域名**：`https://mrkjai.com`
- **Content-Type**：`application/json; charset=utf-8`
- **鉴权 Header**：`X-API-Key: opc_user_<40 位 hex>`
- **返回**：HTTP 状态码永远 200，业务成功/失败看 body 的 `ok` 和 `code` 字段

> Key 在 OPC 站点「我的 → 个人集成（API Key）」页生成和重置。

---

## 2. 请求体字段

### 必填字段

| 字段 | 类型 | 限制 | 说明 |
|---|---|---|---|
| `title` | string | 1–120 字符 | 赛事名称 |
| `summary` | string | 1–300 字符 | 一句话描述 |
| `type` | enum | 见下表 | 赛事类型 |
| `region` | enum | 见下表 | 地区 |
| `organizer` | string | 1–100 字符 | 主办方 |
| `publishedAt` | string | ISO 8601 | 赛事发布/开始时间 |
| `deadlineAt` | string | ISO 8601 | 报名截止时间，**必须晚于 publishedAt** |
| `externalUrl` | string | 合法 URL | 赛事详情页 URL，**全站唯一**（已存在则幂等返回） |

### 选填字段

| 字段 | 类型 | 限制 | 说明 |
|---|---|---|---|
| `tags` | string[] | 最多 8 个 | 标签 |

### 枚举值

**type**：

| 值 | 中文 |
|---|---|
| `startup` | 创业大赛 |
| `hackathon` | 黑客松 |
| `design` | 设计比赛 |
| `academic` | 学术竞赛 |
| `summit` | 行业峰会 |

**region**：

| 值 | 中文 |
|---|---|
| `online` | 线上 |
| `beijing` | 北京 |
| `shanghai` | 上海 |
| `hangzhou` | 杭州 |
| `shenzhen` | 深圳 |
| `national` | 全国 |
| `overseas` | 海外 |

---

## 3. 调用示例

```bash
curl -s -X POST 'https://mrkjai.com/api/events/ingest' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: opc_user_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' \
  -d '{
    "title": "2025 春季 AI 黑客松",
    "summary": "48 小时极限编程挑战，主题为多模态大模型应用，冠军奖金 10 万元。",
    "type": "hackathon",
    "region": "shanghai",
    "organizer": "XYZ 科技",
    "publishedAt": "2025-04-01T10:00:00+08:00",
    "deadlineAt": "2025-04-15T23:59:59+08:00",
    "externalUrl": "https://example.com/hackathon-2025-spring",
    "tags": ["AI", "多模态", "编程挑战"]
  }'
```

---

## 4. 响应

### 成功创建

```json
{
  "ok": true,
  "code": "created",
  "data": {
    "id": "uuid-xxx",
    "slug": "2025-chun-ji-ai-hei-ke-song-abc12345",
    "title": "2025 春季 AI 黑客松",
    "externalUrl": "https://example.com/hackathon-2025-spring",
    "createdBy": "user-uuid",
    "isNew": true
  }
}
```

### 已存在（幂等）

```json
{
  "ok": true,
  "code": "exists",
  "data": {
    "id": "uuid-xxx",
    "isNew": false
  }
}
```

---

## 5. 错误码

| code | 含义 | 排查 |
|---|---|---|
| `unauthenticated` | 缺 X-API-Key | 加 header |
| `invalid_key` | Key 格式错或不存在 | 检查 Key（`opc_user_` + 40 hex） |
| `key_revoked` | Key 已被撤销 | 去「个人集成」页重置 |
| `bad_json` | 请求体不是合法 JSON | 检查格式 |
| `validation_error` | 字段校验失败 | 看 `field` 和 `error` |
| `internal_error` | 服务器异常 | 稍后重试 |

---

## 6. 给提取信息 AI 的工作流

### 输入
- 赛事详情页 URL
- 用户的 X-API-Key

### 步骤

1. **抓取页面**：fetch(url) → 解析 HTML
2. **字段映射**：

| 抓取内容 | API 字段 | 推断规则 |
|----------|---------|---------|
| 页面 h1 / title | title | 去后缀、清空白 |
| meta description / 首个 p | summary | 截断到 300 字符 |
| 主办方/承办方 | organizer | 截断到 100 字符 |
| 比赛开始时间 | publishedAt | 转 ISO 8601；找不到用当前时间 |
| 报名截止 | deadlineAt | 转 ISO 8601；找不到用 publishedAt + 30 天 |
| 详情页 URL | externalUrl | 原样传 |
| 关键词 | tags | 取前 8 个 |

3. **type 推断**：
   - 含"黑客松/hackathon" → hackathon
   - 含"创业/路演/startup" → startup
   - 含"设计/UI/UX" → design
   - 含"数学/学术/ACM" → academic
   - 含"峰会/summit/大会" → summit
   - 默认 → hackathon

4. **region 推断**：
   - 含"线上/online" → online
   - 含"北京/上海/杭州/深圳" → 对应城市
   - 含"全国" → national
   - 含"海外/overseas" → overseas
   - 默认 → online

5. **deadlineAt 兜底**：抓不到时传 publishedAt + 30 天，summary 注明"长期有效"

6. **提交**：POST `/api/events/ingest`
   - `code: "created"` 或 `"exists"` → 成功
   - `code: "validation_error"` → 看 field 修正后重试一次
   - `code: "invalid_key"` / `"key_revoked"` → 让用户重新生成 Key
   - `code: "internal_error"` → 重试 1 次

7. **不要做的事**：
   - 不猜测/伪造 title 或 organizer
   - 不重复提交同一 URL
   - 不把 publishedAt 设为未来时间
