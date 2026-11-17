---
name: pinterest-image-finder
description: 搜索 Pinterest 灵感图并提取可直接访问的图片 URL。当用户说"帮我找灵感图""搜Pinterest""找参考图""找灵感照片""search inspiration""find reference photo"时触发。接受关键词，返回图片 URL 列表供下游 textgen 分析使用。
---

# Pinterest 灵感图搜索与提取

接受搜索关键词，通过 tsearch 搜索 Pinterest 页面，再尝试从搜索结果中提取可直接访问的图片 URL。返回的图片 URL 可直接传给 `linkfox-aigc-textgen` 做色彩/构图分析。

## 工作原理（三层提取策略）

1. **搜索**：调用 `/tsearch/search` 接口搜索 `site:pinterest.com <keyword>`，返回 Pinterest 页面列表 + 文本内容
2. **正则提取**：从搜索结果的 `content` 字段中正则匹配所有图片 URL（`jpg/jpeg/png/webp`）
3. **页面抓取**：若正则无命中，用 `urllib` 请求排名靠前的 Pinterest 页面 HTML，从中提取 `i.pinimg.com` 图片地址
4. **降级**：若以上均未提取到图片 URL（Pinterest 返回 401/超时等），返回 Pinterest 页面 URL 列表，由 agent 引导用户手动浏览选图

## 调用方式

```bash
# 方式一：直传 JSON（推荐简单场景）
python scripts/find_inspiration_image.py '{"keyword":"Hanfu aesthetic lifestyle photo","max_results":5}'

# 方式二：stdin（推荐 prompt 含特殊字符时）
python scripts/find_inspiration_image.py --stdin < params.json
```

## 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `keyword` | string | 是 | — | 搜索关键词。脚本自动拼接 `site:pinterest.com` 前缀，无需手动加。建议用英文，描述美学风格 + 场景，如 `"Hanfu aesthetic lifestyle photo"`、`"minimalist product photography warm tone"` |
| `max_results` | int | 否 | `5` | 最多返回的图片/页面 URL 数量 |

### 关键词建议

- 越具体效果越好：`"Hanfu photography cherry blossom portrait"` 优于 `"Hanfu"`
- 包含场景/情绪词：`lifestyle`、`portrait`、`aesthetic`、`photoshoot`、`warm tone`
- 英文搜索结果更丰富
- 可传入 Step 0 商品图分析输出的 `pinterest_keywords` 之一

## 输出

stdout 始终输出可 `json.loads` 的 JSON。完整结果同时落盘到会话目录 `linkfox/<日期>/<session>/data/pinterest-image-finder-<timestamp>.json`。

### 输出字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | `success` / `partial` / `error` |
| `image_urls` | array&lt;string&gt; | 可直接访问的图片 URL（`https://i.pinimg.com/...` 或其他图片域名）。可能为空数组 |
| `page_urls` | array&lt;string&gt; | Pinterest 页面 URL（`https://www.pinterest.com/...`），供用户手动浏览。可能为空数组 |
| `fallback` | bool | `true` = 未能自动提取图片，需用户手动上传；`false` = 已提取到图片 URL |
| `search_keyword` | string | 实际搜索使用的关键词（不含 `site:pinterest.com` 前缀） |
| `message` | string | 仅 `partial` / `error` 时出现，向用户说明原因和下一步操作 |

### 三种状态示例

**success — 成功提取到图片 URL：**

```json
{
  "status": "success",
  "image_urls": [
    "https://i.pinimg.com/originals/ab/cd/ef/abcdef123456.jpg",
    "https://i.pinimg.com/originals/12/34/56/1234567890ab.jpg"
  ],
  "page_urls": [
    "https://www.pinterest.com/ideas/hanfu-photoshoot/123456789"
  ],
  "fallback": false,
  "search_keyword": "Hanfu aesthetic lifestyle photo"
}
```

→ agent 取 `image_urls[0]` 直接传给 `linkfox-aigc-textgen` 的 `imageUrls` 参数

**partial — 只找到页面 URL，需用户手动选图：**

```json
{
  "status": "partial",
  "image_urls": [],
  "page_urls": [
    "https://www.pinterest.com/charlie5772/古",
    "https://www.pinterest.com/ideas/chinese-hanfu-photoshoot/912768365864"
  ],
  "fallback": true,
  "search_keyword": "Hanfu aesthetic lifestyle photo",
  "message": "未能自动提取图片 URL，请手动访问 page_urls 中的链接，选一张图上传"
}
```

→ agent 将 `page_urls` 展示给用户，引导用户点击链接、选图、上传

**error — 搜索无结果：**

```json
{
  "status": "error",
  "image_urls": [],
  "page_urls": [],
  "fallback": true,
  "search_keyword": "xxx",
  "message": "搜索无有效结果"
}
```

→ agent 建议用户换关键词重试，或直接上传自己的灵感图

## agent 集成建议

```
Step 2 路由逻辑：
  调用 pinterest-image-finder
    ├─ status == "success" → 取 image_urls[0] 进入 Step 3
    ├─ status == "partial" → 展示 page_urls，请用户手动选图上传
    └─ status == "error"   → 建议换关键词或直接上传灵感图
```

## 限制

- Pinterest 页面可能返回 401 Unauthorized，此时三层策略退化为降级模式
- tsearch 搜索结果为文本提取，可能不含直接图片链接
- 每次调用消耗 tsearch 6 积分
- 建议配合手动上传使用：自动提取失败时，用户手动选图上传是可靠兜底
