# 各平台赛事抓取方式

## 1. Kaggle Competitions

- **URL**：https://www.kaggle.com/competitions
- **抓取方式**：WebSearch 搜索 `Kaggle competitions 2026`
- **关键字段**：Competition Name / Deadline / Prize / Type（Featured/Research/Getting Started）
- **备注**：Kaggle 有官方 API，但需要 Kaggle 账号 token

---

## 2. Devpost Hackathons

- **URL**：https://devpost.com/hackathons
- **抓取方式**：WebSearch 搜索 `Devpost hackathon 2026 open`
- **关键字段**：Hackathon Name / Submission Deadline / Prizes / Online/In-person
- **备注**：Devpost 页面是 JS 渲染，直接 WebFetch 可能不完整，建议用 WebSearch 搜索近期赛事

---

## 3. OpenCSG OPC 挑战赛

- **URL**：https://www.opencsg.com
- **抓取方式**：WebSearch 搜索 `OPC 独立先锋挑战赛 2026` 或 `OpenCSG OPC 赛事`
- **关键字段**：赛区 / 报名时间 / 决赛时间 / WAIC 链接

---

## 4. 小红书独立开发大赛

- **URL**：搜索 `小红书 独立开发大赛 2026`
- **抓取方式**：WebSearch + 小红书站内搜索
- **关键字段**：赛道 / 奖金 / 报名截止 / 作品提交截止

---

## 5. Product Hunt Indie Hackers Awards

- **URL**：https://www.producthunt.com/products/indie-hackers/awards
- **抓取方式**：WebSearch 搜索 `Product Hunt Indie Hackers Awards 2026`
- **关键字段**：Award Category / Deadline / Winner Prize

---

## 6. HICOOL / 国内创业大赛

- **URL**：https://www.hicool.com/
- **抓取方式**：WebSearch 搜索 `HICOOL 2026 开发者挑战赛`
- **关键字段**：赛道 / 报名截止 / 决赛地点 / 奖金池

---

## 通用抓取策略

1. **优先用 WebSearch**：搜索 `{平台名} {赛事类型} {当前年份}`，获取最新赛事列表
2. **补充用 WebFetch**：对搜索结果中的具体赛事页面，用 WebFetch 抓取详情
3. **去重用赛事名称**：与本地记录比对，只报告新增赛事
4. **输出格式**：见 `templates.md`
