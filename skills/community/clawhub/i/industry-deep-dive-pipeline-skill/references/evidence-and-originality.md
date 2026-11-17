# Evidence and Originality

## Source tiers

| 等级 | 来源 | 用法 |
|---|---|---|
| A | 官方公告、监管原文、财报、论文、产品文档、法院文件、公开演讲原文 | 可支撑高风险事实 |
| B | Reuters、Bloomberg、FT 等高可信二手媒体，或有明确采访对象的专业媒体 | 可交叉确认；缺一手时标注来源边界 |
| C | 行业分析、播客、博客、社区文章 | 用于观点、竞争覆盖和反方；数字需回溯 |
| D | 社交媒体、转载、搜索摘要、截图 | 仅作线索或待核信号 |

## Fact table status

- `confirmed`：一手源确认，或两个独立可靠来源一致。
- `qualified`：事实成立，但需保留来源、时间或 vendor-reported 限定。
- `contested`：存在直接冲突，正文必须呈现边界或不使用。
- `pending`：尚未完成核验，禁止进入终稿。
- `rejected`：已确认错误、过时或与文章无关。

## Fact table minimum fields

| ID | Claim | Type | Status | Original date | Verified at | Source tier | Source URL/path | Allowed wording | Expiry/invalidating signal |
|---|---|---|---|---|---|---|---|---|---|

类型包括：number、date、status、quote、policy、market、causal、interpretation。

## High-risk rules

1. 政策和法律状态明确区分讨论、征求意见、草案、通过、生效和执行案例。
2. 产品状态明确区分 roadmap、private preview、public preview、GA 和 deprecated。
3. 融资区分本轮融资额、累计融资额、估值和交易对价。
4. 厂商性能数字标注 vendor-reported；客户效果标注 customer-reported。
5. 宏观数据保留统计主体、时间、分母和单位。
6. 高时效主题在写作当天或终稿前重新核验。

## Originality review

### Search units

分别搜索：

- 主题与主体。
- 核心判断的同义表达。
- 分析框架与关键区分。
- 标志性标题和记忆句。
- 直接反方和历史反例。
- 中文、英文及主题相关语言。

### Competition categories

| 类型 | 判断 |
|---|---|
| news coverage | 事实已报道，不代表分析撞车 |
| profile/financing story | 公司与人物叙事充分，不能再以介绍为主线 |
| same topic, different thesis | 可写，但需明确增量 |
| same thesis, different evidence | 空间有限，需更强框架或新证据 |
| same thesis and structure | 高撞车风险，换角度或放弃 |

### Allowed conclusions

- “现有覆盖主要集中在 X，本文增量位于 Y。”
- “该判断已有公开讨论，本文补充了 Z 证据或边界。”
- “未检索到将 A、B、C 组合为同一框架的中文深度分析；结论受当前检索范围限制。”

### Forbidden shortcuts

- 只搜一个关键词就断言“中文无人写”。
- 把标题不同当作观点不同。
- 把用户首次提出当作首创。
- 用“有媒体报道”替代文章和论证的逐项比较。
- 忽略直接反方，再用单向证据证明结论。

## Stop conditions

- 核心判断和论证结构均已被充分覆盖。
- 差异化依赖无法核实或明显错误的事实。
- 唯一增量是更夸张的标题。
- 主题高风险且缺少可靠来源。

停止后输出：放弃、并入其他文章、缩为短观察、等待新证据或更换角度。
