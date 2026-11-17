---
name: gzh-comment-export
slug: gzh-comment-export
displayName: 公众号留言/评论批量导出 · WeChat Comment Export — 读者留言存为本地 Markdown 归档
version: 1.0.3
summary: 把自己公众号后台的读者留言/评论批量导出为本地 Markdown——官方后台「留言管理」按文章分组全量读取、作者/内容/时间/地区完整字段、纯本地运行、全程只读。由 webclaw3 驱动（复用你已登录的 Chrome，无需填任何 token/cookie）。
license: MIT
description: 把自己公众号后台的读者留言/评论批量导出为本地 Markdown——官方后台「留言管理」按文章分组全量读取、作者/内容/时间/地区完整字段、纯本地运行、全程只读。由 webclaw3 驱动（复用你已登录的 Chrome，无需填任何 token/cookie）。触发场景：想把公众号后台的留言、读者评论批量存下来做归档/精选整理/读者反馈分析时使用（只支持自己的公众号，后台登录的那个号）。
---

# 公众号留言导出（gzh-comment-export）

把自己公众号后台收到的读者留言批量导出成本地文件，按文章分组，用于留言归档、精选整理、读者反馈分析。

路径：登录公众号后台 → 「互动管理 → 留言」官方留言管理页 → 按文章分组读取留言列表 → 逐篇提取 → 存本地。

**边界**：只做自己的公众号（后台登录的那个号，无需指定账号）；**全程只读**——屏蔽 / 删除 / 置顶 / 加入黑名单 / 回复等管理按钮一律不碰；不做任何外部抓取（别人文章的评论不在后台，也没有入口）。

## 前置依赖（强制）

**必须安装浏览器自动化通道，否则无法运行。**

本 skill 靠它打开你已登录的 Chrome 里的公众号后台，自身不 import 任何外部模块，只通过本地 relay 的 HTTP API（`http://127.0.0.1:3459`）驱动浏览器。

组成：
- Chrome 扩展 **wc3-chrome**（在 `chrome://extensions` 里确认已启用）
- 本地 relay 服务，监听 `127.0.0.1:3459`

安装：见该浏览器通道仓库的 README（一条命令装好）。装好后运行其 doctor 自检脚本完成通道检查，或直接：

```bash
curl -s http://127.0.0.1:3459/api/status
```

返回里 `extensionConnected: true` 即通道就绪。**同时在 Chrome 里登录 mp.weixin.qq.com 公众号后台**（登录态决定导出哪个号）。

## 使用方式

```bash
node skill.mjs <input.json>
```

`input.json`：

```json
{ "output_dir": "/abs/path/to/out" }
```

| 字段 | 必填 | 默认 | 说明 |
| --- | --- | --- | --- |
| `output_dir` | 否 | 当前工作目录下的 `gzh-comment-export/` | 导出目录（也兼容 `outputDir`）。目录不存在会自动创建 |
| `output_files.data` | 否 | `comments.md` | 留言明细文件名 |
| `output_files.result` | 否 | `index.json` | 统计文件名 |

无需传账号——导出对象就是后台当前登录的那个号。

## 输出格式

`<output_dir>/comments.md` — 按文章分组，每篇文章一节（标题 + 发表时间 + 留言表格）：

```markdown
# 公众号留言导出

> 账号：<昵称>
> 导出时间：2026-09-26 18:26:00
> 数据来源：公众号后台「互动管理 → 留言」（只读）
> 文章总数：18　留言总数：1

---

## 2025 武功山：高山草甸、星空露营，2天1夜最全清单、新手轻松登顶

- 发表时间：2025-09-07 14:08
- 留言数：1

| 作者 | 留言内容 | 留言时间 | 地区 |
| --- | --- | --- | --- |
| 张锋₁₅₉₂₀₂₀₅₃₈₃ | 国庆山上都是人[表情] | 2025-09-08 13:32:17 | 广东 |
```

`<output_dir>/index.json` — 统计与元信息（不含留言正文）：

```json
{
  "account": "石建AI一个人公司",
  "exportTime": "2026-09-26 18:26:00",
  "totalArticles": 18,
  "totalComments": 1,
  "partial": false,
  "partialReason": "",
  "listArticleTotal": 18,
  "failedArticles": 0,
  "stopReason": "end",
  "articles": [
    { "title": "2025 武功山：…", "articleTime": "2025-09-07 14:08", "commentCount": 1 }
  ]
}
```

每条留言字段：`author`（作者昵称）、`content`（留言内容）、`time`（留言时间）、`region`（地区，页面没有则空）、`article`（所属文章标题，在 `comments.md` 里体现为所属小节）。

stdout 只输出一行 JSON 摘要：`{ status, summary, output_dir }`。

## 行为约定

- **翻页到底**：文章列表的「下一页」消失或不可点才结束；右栏留言列表若自身分页也会一并翻到底。
- **0 条留言的文章**照常记录 `commentCount: 0`，不算失败。
- **partial**：有文章读取失败、翻页达到上限、或实际读取篇数少于列表总数时，`index.json` 标 `partial: true` 并在 `partialReason` 说明原因。
- **只读**：全程只做「左栏文章切换」和「分页点击」两类操作。
- **不臆造**：页面给的是相对时间（如「昨天 14:39」）就原样记录，不推算成绝对日期；微信表情无 alt 信息，以 `[表情]` 占位，不猜具体表情；字段缺失留空。

## 常见问题

**报「本地 relay 未响应」** — 浏览器自动化通道没装或没启动。装好后运行其 doctor 自检，或 `curl -s http://127.0.0.1:3459/api/status` 确认通道已起。

**报「relay 已就绪但浏览器侧没连上」** — ① 确认 Chrome 扩展 wc3-chrome 已启用（`chrome://extensions`）；② 在 Chrome 里登录 mp.weixin.qq.com 公众号后台；③ 重跑通道 doctor 自检看 advice。

**报「读不到登录 token」** — 后台登录态失效。在 Chrome 里重新登录公众号后台（确认后台首页能正常打开），再重跑。

**`partial: true` 且 `failedArticles > 0`** — 少量文章读取失败（常见于扩展瞬时断开）。本 skill 对瞬时错误已自动重试；仍失败的可直接重跑，已成功的部分不会受影响。
