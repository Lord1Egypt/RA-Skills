---
name: jd-review-export
slug: jd-review-export
displayName: 京东商品评价导出 · 一键采集为本地 Markdown 表格
version: 1.0.4
description: 输入京东商品详情页链接，自动打开页面、展开「全部评价」浮层，在虚拟列表里持续下拉采集买家评价，去重后导出为本地 Markdown 表格（用户名/购买标签/日期/SKU/正文/商家回复/有用数），可用 count 控制条数。当用户给出京东商品链接并要求采集/导出该商品的评价、评论、买家评价、口碑数据时使用。
summary: 京东商品评价一键导出为本地 Markdown 表格——用户名、日期、SKU、正文、商家回复、有用数一列不落，选品和差评分析直接用。给一个京东商品链接就能跑：边滚边采自动去重，可指定采集条数。不需要任何 API key 或付费额度，用你 Chrome 里已登录的账号跑。当用户要采集/导出京东商品评价、评论、买家评价、口碑数据时唤起。
license: MIT
---

# jd-review-export

## 功能

输入一个京东商品详情页链接，自动打开商品页、触发「全部评价」浮层，在浮层的虚拟列表里持续下拉捞取评价，
去重后导出为本地 Markdown 表格（列：序号、用户名、购买标签、日期、SKU、正文、商家回复、有用数）。

全程通过浏览器扩展的 Relay HTTP API 操作用户真实 Chrome（复用登录态），不使用 CDP、不调用京东接口。

## 前置条件

1. Chrome 已打开，浏览器扩展（Extension Relay）已启用且 relay 服务运行在 `http://127.0.0.1:3459`。
2. **已在 Chrome 中登录京东**。未登录时京东会强制跳转登录墙，skill 会直接报错并提示登录后重试。
3. 若需要 LLM 子会话（页面状态语义判别），本地 pipeline 服务（端口 3460）需运行中，子会话经它代跑。
   判别在「已知特征串」命中时由代码直接短路，不消耗 token；仅当状态拿不准时才调用子会话，
   子会话不可用时按 `other` 如实上报，不会编造结论。

## 使用方式

```bash
node skill.mjs <input.json>
```

`input.json`：

```json
{
  "productUrl": "https://item.jd.com/100275743932.html",
  "count": 50,
  "output_dir": "/abs/path/to/output",
  "output_files": { "data": "data.md", "result": "res.json" }
}
```

### 入参

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `productUrl` | string | 是 | — | 京东商品详情页链接，形如 `https://item.jd.com/{sku}.html`；纯链接即可，无需 `pcdk` 等加密参数 |
| `count` | number | 否 | 50 | 最多捞取评价条数；达到条数或滚动到底即停 |
| `output_dir` | string | 否 | `/tmp/jd-review-export-output/` | 产出目录；也接受 `outputDir` |
| `output_files` | object | 否 | `{"data":"data.md","result":"res.json"}` | 产出文件名 |

## 输出

写到 `output_dir`：

- **`reviews.md`** — 业务交付物，Markdown 表格，列为 序号 / 用户名 / 购买标签 / 日期 / SKU / 正文 / 商家回复 / 有用数。
  正文内的换行以 `<br>` 表示、`|` 已转义。数据不足时**首行**为 `<!-- partial -->` 并在「说明」里写明原因。
- **`data.md`** — 与 `reviews.md` 内容一致（采集到的数据）。
- **`res.json`** — 精简元信息：`status` / `summary` / `total` / `requested` / `stop_reason` / `error` / `hint` / `timestamp` 等。

stdout 只输出一行 JSON：`{"status":"...","summary":"...","output_dir":"..."}`。

`status` 取值：`success`（达到验收底线）/ `partial`（有数据但不足底线，已标 partial）/ `failed`（无数据或前置条件不满足）。

## 验收底线

- 至少 5 条评价（当 `count` < 5 时按 `count` 计），且每条 用户名 / 日期 / SKU / 正文 四项非空；
  字段不全的条目会被跳过并在 `res.json.skipped_incomplete` 中计数。
- 不足时仍生成 `reviews.md`，首行标注 `<!-- partial -->` 并说明原因（商品评价总量少 / 页面受限中断 / 达到轮次上限）。

## 行为与限制

- **边滚边收集**：评价浮层是虚拟列表，DOM 只渲染视口附近的 3–6 条，历史条目会被回收。
  skill 每轮滚动前先提取当前渲染条目、按 `用户名+日期+正文前20字` 去重累积，最后一次性导出，
  因此**不要**改成「滚到底再一次性提取」。
- **滚动节流**：轮次间隔约 2.2s。实测更快的连续滚动会让商品页返回 403，请勿调小。
- **终止条件**：累计条数 ≥ `count`，或「本轮无新增且滚动高度不再增长」（判定到底），或达到 40 轮安全上限。
- **页面受限 / 登录墙 / 无效链接**：会明确报错并在 `res.json` 的 `error`/`hint` 与 `reviews.md` 中给出中文提示。
  遇到 403 时请等待约 10 分钟后再重试；未登录时请在 Chrome 登录京东后重试。
- 选择器全部使用前缀匹配（`[class*="_rateListContainer_"]`、`[class*="_listItem_"]`）以抗版本改版，
  语义 class（`.jdc-pc-rate-card-nick` 等）用于字段提取。
