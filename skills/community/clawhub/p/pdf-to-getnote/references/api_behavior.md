# GetNotes API 关键行为发现（2026-04-01 实测）

## img_text 类型行为

### 行为：每张图 = 独立笔记
传入 `image_urls: [url1, url2, ..., urlN]`（N>1）时，API **为每张图片创建一个独立笔记**，返回 N 个独立 task_id。

**实测证据：**
- 请求传入 10 个 URL，返回 `created_count: 10`，`tasks: [task_id_1, ..., task_id_10]`
- 每个 task_id 对应不同的 note_id
- 无法创建"多图单笔记"

### 行为：content 字段被忽略
传入 `img_text` 的 `content` 字段（AI 摘要），处理完成后查询笔记详情：
- `title`: 空
- `content`: 空
- `attachments`: 只有图片，无任何文字内容

**结论：img_text 完全不支持保留传入的 content。**

### 唯一可行方案：plain_text + Markdown 内嵌

| 方案 | content | 图片 | 附件 | 结论 |
|------|---------|------|------|------|
| img_text 多图 | ❌ 被覆盖 | ✅ | ❌ | 每张图独立笔记 |
| img_text 单图 | ❌ 被覆盖 | ✅ | ❌ | 不保留AI摘要 |
| plain_text | ✅ 保留 | ✅ Markdown嵌入 | ❌ | **推荐** |

---

## 图片上传行为

### 每次只返回 1 个 token
请求 `?count=9` 时，API 只返回 1 个 token，不是 9 个。必须循环调用。

### OSS 字段顺序必须严格
`key → OSSAccessKeyId → policy → signature → callback → Content-Type → file`
顺序错误会导致签名验证失败。

### 支持的 MIME 类型
只支持：`jpg`, `png`, `jpeg`, `gif`, `webp`
不支持：`pdf`, `bmp`, `tiff` 等

---

## 笔记创建行为

### plain_text：同步返回
`POST /note/save` 返回 `{"id": 1905910102880868768, ...}`，note_id 直接可用，无需轮询。

### img_text：异步，返回 task_id
返回 `{"tasks": [{"task_id": "...", "image_url": "..."}]}`，需要轮询 `/note/task/progress`。

---

## 附件行为

### attachments[] 不支持 API 上传
查 `/note/detail` 的 `attachments[]` 显示的是 img_text 由系统生成的图片 OCR 结果，无法通过 API 原生上传 PDF 作为附件。

---

## 结论总结

**目标："1条笔记 = AI摘要 + PDF附件" 在当前 API 版本下无法实现。**

**最优替代：**
- 创建 1 条 `plain_text` 笔记
- AI 摘要放在 `content`
- PDF 每页图片以 `![](url)` 内嵌
- 用户在笔记中往下滑动查看所有页面图
