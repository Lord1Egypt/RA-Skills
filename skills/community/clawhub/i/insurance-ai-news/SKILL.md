---
name: insurance-ai-news
version: 1.1.1
description: 全球保险业AI动态早报。搜索13板块覆盖的全球保险公司AI进展，按Zara Zhang格式（中英双语+The Takeaway+原文链接）整理成早报推送并同步飞书文档。每天08:30自动执行。板块：9国/地区 + 投资 + 监管 + 重点公司 + AI人才。
---

# 全球保险业AI动态早报

## 触发条件

- 用户明确要求"保险业AI早报"、"保险AI动态"
- 定时触发：每天早上 08:30（通过cron机制）
- 用户要求查看过往早报

---

## ⚠️ 格式规范（强制执行！）

**学习 Zara Zhang 的 AI Builders Digest 格式**：

### 每条新闻必须包含（完整结构）

```markdown
**{公司名（英文）}：{标题（英文）}**
**{公司名（中文）}：{标题（中文）}**

Published: {YYYY-MM-DD}
发布日期：{YYYY-MM-DD}

The Takeaway: {核心观点（英文，1-2句）}
核心观点：{核心观点（中文翻译）}

{正文段落（英文，2-3句关键信息）}
{正文段落（中文翻译）}

🔗 {原文URL}
```

### 禁止事项

- ❌ **禁止多条新闻混在一起**：每条新闻必须独立，不能把多家公司放在同一个标题下
- ❌ **禁止没有原文链接**：每条新闻必须有 🔗 + URL
- ❌ **禁止没有 The Takeaway**：每条必须有核心观点摘要
- ❌ **禁止只有标题双语**：正文也要中英文对照
- ❌ **禁止中文重复两遍**：英文在前，中文在后，必须对照

---

## 执行流程（强制顺序）

### 1. 搜索全球保险公司AI动态

**搜索工具**：
- 优先 `mcporter call 'exa.web_search_exa'`
- 备用 `web_search`

**搜索策略**：
```
# 每个区域至少搜索一次
"insurance AI news Singapore 2026"
"insurance AI news Hong Kong 2026"
"中国保险AI 太保 平安 2026"
"insurance AI Malaysia 2026"
"insurance AI Indonesia 2026"
"insurance AI North America 2026"
"insurance AI Europe 2026"
"insurance AI Africa 2026"
"insurance AI Latin America 2026"
"insurtech AI startup funding investment 2026"
"AI regulation insurance financial services 2026"
```

### 2. 时效性规则

**标注发布日期**：每条新闻必须标注发布日期

**区分两类新闻**：
- 📌 **最新动态**：24小时内发布
- 📎 **近期进展**：过去一周内发布

**如实告知**：
- 如无当天新闻，明确说明"无当日发布新闻"
- 禁止把历史新闻包装成"最新"

### 3. 分类结构（12板块，固定顺序）

```markdown
## 🇸🇬 新加坡 | Singapore
...

## 🇭🇰 香港 | Hong Kong
...

## 🇨🇳 中国 | China
...

## 🇲🇾 马来西亚 | Malaysia
...

## 🇮🇩 印度尼西亚 | Indonesia
...

## 🇺🇸 北美 | North America
...

## 🇪🇺 欧洲 | Europe
...

## 🌍 非洲 | Africa
...

## 🌎 拉美 | Latin America
...

## 💰 全球AI投资动态 | Global AI Investment
...

## 📜 全球AI监管动态 | Global AI Regulation
...

## 🎯 重点监控公司 | Key Companies to Watch
...
```

### 💰 全球AI投资动态板块

**覆盖内容**：
- AI和Insurtech创业公司融资情况（轮次、金额、投资方、用途）
- 全球AI投资、收购新闻
- 保险业AI投资和收购动作

### 📜 全球AI监管动态板块

**覆盖内容**：
- AI监管政策发布与更新
- 金融/保险行业AI合规要求
- 监管机构执法与处罚
- 行业自律与标准制定

### 🎯 重点监控公司板块（强制！每期必有）

**必须出现的6家公司（固定顺序）**：

| 序号 | 公司 | 英文名 |
|------|------|--------|
| 1 | 保诚 | Prudential PLC |
| 2 | 中国平安 | Ping An |
| 3 | 苏黎世保险集团 | Zurich Insurance Group |
| 4 | 宏利 | Manulife |
| 5 | 富卫 | FWD |
| 6 | 友邦 | AIA |

**规则**：
- 每家公司必须在结构上留出位置
- 如果前面区域已提到 → 写"与上述{板块名}内容相同，详见上文"
- 如果有新内容 → 正常写入新闻
- 绝不能因为"已提到"就删除这家公司的板块位置

---

### 👥 AI人才动态板块（强制！每期必有）

**覆盖内容**：
- 保险公司AI高管任命与离职
- AI/数据/技术部门负责人变动
- 首席AI官、首席数据官、AI总监任命
- AI团队重要招聘与人才流动

**格式**：
每条人才动态独立，包含职位、公司、背景、任命时间

---

## 📊 行业趋势 | Industry Trends

---

## 4. 飞书文档同步（强制）

**⚠️ 飞书API限制**：`create` 的 `content` 参数只设置标题，正文必须用 `append`

**正确方法（强制执行）**：
```python
# 第1步：创建文档（只设标题）
doc = feishu_doc(action="create", title="全球保险业AI动态早报 {日期}")

# 第2步：追加正文（必须！）
feishu_doc(action="append", doc_token=doc["doc_token"], content="完整正文")

# 第3步：验证
result = feishu_doc(action="read", doc_token=doc["doc_token"])
assert result["block_count"] > 1, "文档只有标题，正文未写入！"
```

**常见错误**：
- ❌ 用 `write` 重写整个文档（会覆盖为空）
- ❌ 只调用 `create` 不调用 `append`（只有标题）
- ❌ 不验证 `block_count`（无法发现正文丢失）

---

## 输出格式（完整模板）

```markdown
📰 **全球保险业AI动态早报 | Global Insurance AI Brief**
**{日期} {星期}**

---

## 🇸🇬 新加坡 | Singapore
{新闻列表}

## 🇭🇰 香港 | Hong Kong
{新闻列表}

## 🇨🇳 中国 | China
{新闻列表}

## 🇲🇾 马来西亚 | Malaysia
{新闻列表}

## 🇮🇩 印度尼西亚 | Indonesia
{新闻列表}

## 🇺🇸 北美 | North America
{新闻列表}

## 🇪🇺 欧洲 | Europe
{新闻列表}

## 🌍 非洲 | Africa
{新闻列表}

## 🌎 拉美 | Latin America
{新闻列表}

## 💰 全球AI投资动态 | Global AI Investment
{融资/收购新闻}

## 📜 全球AI监管动态 | Global AI Regulation
{监管/合规新闻}

## 🎯 重点监控公司 | Key Companies to Watch
{6家重点公司：Prudential, Ping An, Zurich, Manulife, FWD, AIA}

## 👥 AI人才动态 | AI Talent Movement
{AI高管任命与离职}

---

**完整报告**：{飞书文档URL}

_生成时间：{时间} | 熊教小神熊_
```

---

## 常见问题

**Q: 搜索结果没有URL怎么办？**
A: 宁可不放这条新闻，也不能没有链接。真实性是底线。

**Q: 同一区域多家公司有新闻？**
A: 每家公司独立一条，用分隔线 `---` 分开。

**Q: 没有英文内容？**
A: 先用中文写，再翻译成英文。The Takeaway 必须双语。

**Q: 某个板块没有新闻？**
A: 写"本期暂无新动态"，不能省略板块。

---

_版本：1.0.0_
_发布日期：2026-05-16_
_参考格式：Zara Zhang AI Builders Digest_