---
name: military-news-collector
description: 军事新闻聚合与重要性排序工具。当用户询问军事领域最新动态时触发，如："今天有什么军事新闻？""最近有什么军事冲突？""全球军事局势如何？"。覆盖：地区冲突、武器装备、军事演习、国防政策、地缘政治、战争动态。输出中文摘要列表，按重要性排序，附带原文链接。
---

# Military News Collector

收集、聚合并按重要性排序全球军事领域新闻。

## 核心原则

**不要只搜"military news today"。** 泛搜索返回的是 SEO 聚合页和趋势预测文章，会系统性遗漏区域性冲突、装备更新、战略动向等重要信息。必须用多维度、分层搜索策略。

## 工作流程

### 1. 多维度分层搜索（最少 8 次，建议 10-12 次）

按以下 **6 个维度** 依次执行搜索，每个维度至少 1 次：

#### 维度 A：周报/Newsletter 聚合（最优先 🔑）

这是信息密度最高的来源，一篇文章可覆盖 10+ 条新闻。

```
搜索词：
- "defense weekly" OR "military weekly" [当前月份年份]
- "security roundup" [当前月份年份]
- "war update" OR "conflict update" [当前月份]
- site:substack.com defense OR military [当前月份]
```

发现周报后，用 web_fetch 获取全文，从中提取所有新闻线索。

#### 维度 B：地区冲突与战争动态（关键维度 🔑）

捕捉正在进行的冲突和战争动态，这类信息泛搜索几乎无法触达。

```
搜索词：
- "Ukraine war update" OR "Gaza conflict" [当前月份]
- "Middle East conflict" OR "tensions" [当前月份]
- "border clash" OR "military clash" [当前月份]
- "ceasefire" OR "peace talks" [当前月份]
- "war news" site:reuters.com OR site:apnews.com
```

#### 维度 C：武器装备与军事技术

```
搜索词：
- "military aircraft" OR "fighter jet" new [当前月份]
- "warship" OR "submarine" launch OR commissioned [当前月份]
- "missile test" OR "drone" military [当前月份]
- "defense contract" OR "arms deal" [当前月份年份]
- "军事装备" OR "武器" 新型 [当前月份]
```

#### 维度 D：军事演习与部署

```
搜索词：
- "military exercise" OR "war games" [当前月份年份]
- "NATO exercise" OR "joint military drill" [当前月份]
- "troop deployment" OR "military buildup" [当前月份]
- "aircraft carrier" deployment [当前月份]
- "军演" OR "演习" [当前月份]
```

#### 维度 E：国防政策与战略

```
搜索词：
- "defense budget" OR "military spending" [当前月份年份]
- "NATO summit" OR "defense policy" [当前月份]
- "military alliance" OR "security pact" [当前月份]
- "nuclear weapons" OR "arms control" [当前月份]
- "国防预算" OR "军事战略" [当前月份]
```

#### 维度 F：地缘政治与地区安全

```
搜索词：
- "Taiwan Strait" OR "South China Sea" tensions [当前月份]
- "Korean Peninsula" OR "North Korea" missile [当前月份]
- "Iran" OR "Israel" military [当前月份]
- "Russia" OR "China" military [当前月份]
- "台海" OR "南海" 局势 [当前月份]
```

### 2. 交叉验证与补漏

初轮搜索完成后，检查是否有遗漏：

- 如果 Newsletter 中提到了某个事件但初轮搜索未覆盖 → 对该事件专项搜索
- 如果同一事件被 3+ 个不同来源提及 → 大概率是热点，深入搜索获取更多细节
- 如果中文媒体和英文媒体的热点完全不同 → 两边都要覆盖

### 3. 搜索关键词设计原则（反模式清单）

| ❌ 不要这样搜 | ✅ 应该这样搜 | 原因 |
|---|---|---|
| "military news today February 2026" | "defense weekly roundup February 2026" | 前者返回聚合页，后者返回策划内容 |
| "military news today" | "Ukraine war update" + "military exercise" 分开搜 | 泛搜无法覆盖具体冲突 |
| "defense breaking news" | 按维度分类搜索 | 过于宽泛，返回噪音 |
| 搜索词中加具体年月日 | 用 "this week" "today" "latest" | 日期反而会偏向预测/展望文章 |
| 只搜 3 次就开始写 | 至少 8 次，覆盖 6 个维度 | 3 次搜索覆盖率不到 30% |

### 4. 重要性综合判断

基于以下信号评估每条新闻重要性（1-5 星）：

| 信号 | 权重 | 说明 |
|------|------|------|
| 多家权威媒体报道同一事件 | ⭐⭐⭐ 高 | 3+ 来源 = 确认重大事件 |
| 涉及人员伤亡或领土变更 | ⭐⭐⭐ 高 | 实际冲突升级 |
| 大国直接参与或表态 | ⭐⭐⭐ 高 | 美/中/俄/欧盟等 |
| 武器系统首次亮相或实战 | ⭐⭐ 中 | 军事技术里程碑 |
| 战略格局变化 | ⭐⭐ 中 | 联盟变化、基地部署等 |
| 经济/能源安全影响 | ⭐⭐ 中 | 航运、能源通道等 |
| 时效性（越新越重要） | ⭐ 中低 | 辅助排序 |

### 5. 输出格式

按重要性降序排列，输出 **15-25 条**新闻：

```
## 🔥 军事新闻速递（YYYY-MM-DD）

### ⭐⭐⭐⭐⭐ 最高重要性

1. **[新闻标题]**
   > 一句话摘要（不超过 50 字）
   > 🔗 [来源名称](URL)

### ⭐⭐⭐⭐ 高重要性

2. ...

### ⭐⭐⭐ 中等重要性

...

### ⭐⭐ 一般重要性

...

### ⭐ 低重要性

...

---
📊 本次共收集 XX 条新闻 | 搜索 XX 次 | 覆盖维度：A/B/C/D/E/F | 更新时间：HH:MM
```

### 6. 去重与合并

- 同一事件被多家报道时，合并为一条，选择最权威/详细的来源
- 在摘要中注明"多家媒体报道"以体现重要性
- 持续发展的冲突（如俄乌战争、巴以冲突）按日期区分不同阶段的进展

## 推荐新闻源

详见 [references/sources.md](references/sources.md)。

## 注意事项

- 优先使用 HTTPS 链接
- 遇到付费墙/无法访问的内容，标注"需订阅"
- 保持客观，不对新闻内容做主观评价，尤其是避免选边站队
- 搜索不足 8 次不要开始输出
- 如果某个维度搜索结果为空，换关键词再搜一次
- 特别注意区分事实报道与观点分析，优先呈现事实
