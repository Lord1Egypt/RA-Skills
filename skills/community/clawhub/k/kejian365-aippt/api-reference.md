# AIPPT Skill — API Reference

Base URL: `https://kejian365.com/api`  
Auth: 鉴权由 `KEJIAN365_AUTH_TOKEN` 环境变量透明注入，脚本自动处理，无需手动传递。

---

## Workflow order

1. **Local model** — generate outline array + material text
2. `GET /aippt/v1/skill/themes` — pick a theme
3. `POST /aippt/v1/skill/task/create` — create record + task (billing deducted here)
4. `GET /aippt/v1/skill/ppt/{ppt_id}/status` — poll until done
5. Handle success / failure

---

## 1. List themes

```
GET /aippt/v1/skill/themes
```

Only returns themes with `theme_type=aippt`, `is_valid=1`, `theme_state=1`.

### Query params

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `page` | int | 1 | Page number |
| `pageSize` | int | 20 | Page size (max 100) |

### Response

```json
{
  "rspCode": "0000",
  "rspDesc": "业务处理成功!",
  "data": {
    "total": 42,
    "list": [
      {
        "theme_id": "649757396252045312",
        "theme_name": "产品介绍",
        "preview_url": "https://oss.../thumb.jpg",
        "style": "商务",
        "scene": "汇报",
        "color": "蓝色",
        "category": "商务",
        "vip_flag": "0",
        "tag": "简约,蓝色"
      }
    ]
  }
}
```

---

## 2. Create task

```
POST /aippt/v1/skill/task/create
Content-Type: application/json; charset=utf-8
```

Creates the PPT record and starts generation in one call.  
**Billing is deducted during this call.** If billing fails the task is NOT created.

### Request body

```json
{
  "topic": "人工智能发展趋势",
  "themeId": "649757396252045312",
  "outline": [
    { "pageNumber": 1, "pageType": "封面", "title": "人工智能发展趋势", "content": "" },
    { "pageNumber": 2, "pageType": "目录", "title": "目录", "content": "1.概述\n2.应用" },
    { "pageNumber": 3, "pageType": "章节", "title": "第一章 概述", "content": "", "chapterNumber": "01" },
    { "pageNumber": 4, "pageType": "内容", "title": "AI定义", "content": "...", "chapterNumber": "01" },
    { "pageNumber": 5, "pageType": "内容", "title": "发展历程", "content": "...", "chapterNumber": "01" },
    { "pageNumber": 6, "pageType": "结束", "title": "谢谢观看", "content": "" }
  ],
  "requirements": "商务风格，适合高管汇报",
  "material": "# 调研资料\n\n## AI发展概述\n人工智能...",
  "themeConfig": {
    "settingPages": "精简",
    "settingLanguage": "中文",
    "settingAudience": "职场员工",
    "contentDepth": "智能生成",
    "illustration": "智能配图",
    "sourceMode": "智能参考"
  },
  "illustrationMode": "standard",
  "generateType": "3"
}
```

> `userId`、`tenantCode`、`deduct` 由网关自动注入，**skill 不需要传递**。

### Request fields

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `topic` | ✅ | string | — | PPT theme / title |
| `themeId` | ✅ | string | — | Template ID from `/skill/themes` |
| `outline` | ✅ | array | — | Page array (see outline rules) |
| `requirements` | | string | `null` | Style / content hint |
| `material` | | string | `null` | Research/summary markdown |
| `themeConfig` | | object | all defaults | Generation config |
| `illustrationMode` | | string | `"standard"` | `"standard"` 普通配图 · `"pro"` 高级配图 |
| `generateType` | | string | `"3"` | `"3"` = AI auto generate |

### `themeConfig` fields

| Field (JSON alias) | Default | Values |
|--------------------|---------|--------|
| `settingPages` | `"智能决策"` | `"智能决策"` · `"精简"` (~10 pages) · `"标准"` (~20 pages) · `"长篇"` (~30 pages) |
| `settingLanguage` | `"中文"` | `"中文"` · `"English"` · any language name |
| `settingAudience` | `"智能决策"` | `"大学生"` · `"职场员工"` · `"专家"` · `"智能决策"` (AI decides) |
| `contentDepth` | `"智能生成"` | `"智能生成"` · `"精简"` · `"标准"` · `"深度"` |
| `illustration` | `"智能配图"` | `"智能配图"` · `"不配图"` |
| `sourceMode` | `"智能参考"` | `"智能参考"` · `"仅用户资料"` |

### Outline page types

| `pageType` | Required | Count | Notes |
|------------|----------|-------|-------|
| `封面` | ✅ | exactly 1 | Always pageNumber 1 |
| `结束` | ✅ | exactly 1 | Always the last page |
| `内容` | ✅ | ≥ 1 | Needs `chapterNumber` if preceded by a `章节` |
| `目录` | optional | 0–1 | Recommended when total pages ≥ 6 |
| `章节` | optional | any | Group dividers; set `chapterNumber` ("01","02"…) |

`pageNumber` starts at 1, sequential, no gaps.

### Success response

```json
{
  "rspCode": "0000",
  "rspDesc": "PPT生成任务创建成功",
  "data": {
    "task_id": "ec1ef7eb-5ab4-4a0b-a12b-257d59decea3",
    "ppt_id": "654236411731582976",
    "topic": "人工智能发展趋势",
    "page_count": 6,
    "execution_status": "started",
    "billing_info": {
      "enabled": true,
      "success": true,
      "amount": 600,
      "page_count": 6,
      "per_page_cost": 100
    },
    "created_time": "2026-04-09T10:00:00"
  }
}
```

Save `data.ppt_id` for status polling.

### Billing error response

When the user has insufficient balance, the API returns a non-`0000` code and does **not** start the task:

```json
{
  "rspCode": "1001",
  "rspDesc": "余额不足，请充值后重试",
  "data": {
    "billing_info": {
      "enabled": true,
      "success": false,
      "amount": 600,
      "raw_response": { ... }
    }
  }
}
```

Detection: `rspCode != "0000"` **AND** `data.billing_info` exists **AND** `data.billing_info.success == false`.

On billing failure: tell the user the `rspDesc`, do not auto-retry.

---

## 3. Poll status

```
GET /aippt/v1/skill/ppt/{ppt_id}/status
```

Poll every 3–5 seconds.

### Response

```json
{
  "rspCode": "0000",
  "data": {
    "ppt_id": "654236411731582976",
    "status": "running",
    "task_status": 0,
    "progress": {
      "total": 6,
      "completed": 3,
      "failed": 0,
      "percentage": 50.0
    },
    "variables": {
      "页面列表": [
        { "url": "https://chatfiles.../page_1.json", "file_id": "file_001" },
        { "url": "https://chatfiles.../page_2.json", "file_id": "file_002" },
        null,
        null,
        null,
        null
      ]
    }
  }
}
```

### Status values

| `status` | Meaning | Next action |
|----------|---------|-------------|
| `pending` | Queued, not started yet | Keep polling |
| `running` | Pages generating in parallel | Keep polling |
| `completed` | All pages done | Process result |
| `failed` | Generation error | Report error |
| `cancelled` | Manually cancelled | Stop |

`null` in `页面列表` means that page is still being generated — this is normal during `running`.

### Completed response

```json
{
  "data": {
    "status": "completed",
    "progress": { "total": 6, "completed": 6, "percentage": 100.0 },
    "variables": {
      "页面列表": [
        { "url": "https://chatfiles.../page_1.json", "file_id": "file_001" },
        { "url": "https://chatfiles.../page_2.json", "file_id": "file_002" },
        { "url": "https://chatfiles.../page_3.json", "file_id": "file_003" },
        { "url": "https://chatfiles.../page_4.json", "file_id": "file_004" },
        { "url": "https://chatfiles.../page_5.json", "file_id": "file_005" },
        { "url": "https://chatfiles.../page_6.json", "file_id": "file_006" }
      ]
    }
  }
}
```

### Failed response

```json
{
  "data": {
    "status": "failed",
    "error": "模板HTML下载失败",
    "steps": [
      { "stepId": "generate_pages", "status": "failed", "error": "Connection timeout" }
    ]
  }
}
```

---

## Error reference

| Scenario | `rspCode` | Example `rspDesc` | Recommended action |
|----------|-----------|-------------------|--------------------|
| Success | `0000` | — | Continue |
| Billing failed | non-`0000` | `余额不足，请充值后重试` | Tell user, do NOT retry |
| Template missing | `8888` | `未找到模板` | Try a different `themeId` |
| Outline empty | `8888` | `大纲不能为空` | Rebuild outline (must have 封面+内容+结束) |
| `themeId` missing | `8888` | `主题ID不能为空` | Provide `themeId` |
| Auth invalid | `401` | `非法请求` | Check `KEJIAN365_AUTH_TOKEN` env var |
| PPT not found | `8888` | `PPT不存在` | Internal error; retry |
| Network / system | `8888` | `系统异常` | Retry once after a short delay |
