# WebFetch 失败站点记录

以下网站在使用 WebFetch 抓取时无法获取有效内容。根据失败类型，采取不同降级策略：仅用 WebSearch 摘要，或使用 agent-browser 浏览器抓取。

> 最后测试时间：2026-04

## 超时（Timeout）— 仅用 WebSearch 摘要

| 站点 | URL 示例 | 失败原因 |
|------|----------|----------|
| lignea.co.jp | https://lignea.co.jp/ryokushaka/ | WebFetch 超时（>60s），2026-04 复测仍超时 |
| sonymusic.co.jp | https://www.sonymusic.co.jp/artist/ryokusyaka/info/581667 | WebFetch 超时（>60s）。注：同域名 `/live/` 路径属于 JS 渲染类型，见下方 agent-browser 一节 |

> 超时类站点不建议用 agent-browser（大概率加载也极慢），优先用 WebSearch 摘要。

## HTTP 错误 — 仅用 WebSearch 摘要

| 站点 | URL 示例 | 失败原因 |
|------|----------|----------|
| reissuerecords.net | https://reissuerecords.net/ | HTTP 403 Forbidden，服务器拒绝访问 |

> HTTP 403/5xx 类错误通常与 User-Agent 或 IP 限制有关，agent-browser 可能同样被拒绝，不建议尝试。

## JS 渲染站点 — 可用 agent-browser 🟢

以下站点 WebFetch 只能获取空壳 HTML，但 agent-browser 可以完整渲染 JS 内容。**当 WebSearch 摘要信息不足时，应使用 agent-browser 抓取。**

| 站点 | URL 示例 | WebFetch 表现 | agent-browser 抓取方式 |
|------|----------|---------------|----------------------|
| ryokushaka.com | https://www.ryokushaka.com/live/ | 仅导航栏和 banner | `open` → `wait 3000` → `snapshot -i` |
| ryokushaka.com | https://www.ryokushaka.com/news/archive/?581667 | 同上 | 同上 |
| sonymusic.co.jp | https://www.sonymusic.co.jp/artist/ryokusyaka/live/ | 仅导航链接 | `open` → `wait 3000` → `snapshot -i`（日程可能需要点击展开） |
| ticket.kenshiyonezu.jp | https://ticket.kenshiyonezu.jp/pages/2026_detail | 无演出信息 | `open` → `wait 3000` → `snapshot -i` |

**agent-browser 抓取模板：**
```bash
agent-browser open {URL}
agent-browser wait 3000
agent-browser snapshot -i
# 如需翻页或展开更多内容：
# agent-browser click @eN && agent-browser wait 1000 && agent-browser snapshot -i
agent-browser close
```

## 部分可用（需注意）

| 站点 | URL 示例 | 说明 |
|------|----------|------|
| livefans.jp | https://www.livefans.jp/groups/265804 | 此前返回 504，2026-04 复测部分页面已恢复（团体页面可用 WebFetch），但艺人详情页（/artists/）仍只返回导航链接 — 可尝试 agent-browser |

## 降级策略总览

```
信息需求
  ├─ WebSearch 摘要足够？ → 直接提取，无需访问站点
  ├─ 需要补充详情？
  │   ├─ 目标是可靠站点？ → WebFetch（rockinon.com、natalie.mu 等）
  │   ├─ 目标是 JS 渲染站点？ → agent-browser（见上方 🟢 标记）
  │   └─ 目标是超时/403 站点？ → 放弃，仅用 WebSearch 摘要
  └─ 所有手段都无数据？ → 标记该艺人"暂无公开巡演信息"
```

**可靠的 WebFetch 站点：** rockinon.com、natalie.mu、fashion-press.net、tower.jp、news.yahoo.co.jp、backnumber.info
