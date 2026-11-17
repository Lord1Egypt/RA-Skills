# structures — 内容层：这份内容该画什么图

> **本文件自足**：当用户丢来一篇文章、一段材料、一次会议记录，说「帮我画图」时，先在这里判断**画几张、每张画什么**。判断完直接进 [skeletons/INDEX.md](skeletons/INDEX.md) 或 [metaphors.md](metaphors.md) 出图。

## 两种入口的区别

| 入口 | 场景 | 起点 |
|---|---|---|
| **本文件（文档驱动）** | 有一堆内容，不知道能画什么 | 扫一遍下面的表，找出内容里存在哪几种结构 |
| [skeletons/INDEX.md](skeletons/INDEX.md)（关系驱动） | 已经知道要画什么关系，只是不知道用什么图形 | 直接问「这些节点之间是什么关系」 |

两条路最后都进同一批骨架文件。

## 18 种信息结构

**提取要点**这一列是重点——它规定了在 `key_elements` 和 `relationships` 里**必须提取到什么**，不是泛泛列「要素1、要素2」。按要点组织信息，画出来才有价值。

| # | 结构类型 | 特征 | 提取要点（必须提取到） | → 骨架 |
|---|---|---|---|---|
| 1 | **network** 关系网络 | 「影响」「相互作用」多对多 | 节点名称、连接方向、关系类型（因果/影响/依赖） | [network-hub](skeletons/network-hub.md) |
| 2 | **hierarchy** 层次结构 | 「由…组成」「下设」 | 层级数、每层节点名称、从属关系 | [hierarchy-tree](skeletons/hierarchy-tree.md) 分层 |
| 3 | **concept-decomposition** 概念拆解 | 「该理论包含…」框架拆解 | 核心概念、子概念、概念间的解释/组成关系 | [hierarchy-tree](skeletons/hierarchy-tree.md) 关系树 |
| 4 | **stakeholder** 利益相关方 | 多方参与、影响力/利益分析 | 各方名称、权力/影响力大小、利益方向、立场 | [structure-block](skeletons/structure-block.md) 对比矩阵<br>*或* [matrix-quadrant](skeletons/matrix-quadrant.md) 权力×利益 |
| 5 | **argument** 论证结构 | 主张+证据+推理、「因为…所以」 | claim、grounds、warrant、backing、qualifier、rebuttal | [evidence](skeletons/evidence.md) 图尔敏 |
| 6 | **debate** 正反对立 | 「支持者认为…反对者则…」 | 争议焦点、正方论点+论据、反方论点+论据 | [structure-block](skeletons/structure-block.md) 对比矩阵 |
| 7 | **semantic-opposition** 语义对立 | 二元对立、「既不是A也不是B」 | 对立两极、矛盾项（非A/非B）、蕴含关系 | [structure-block](skeletons/structure-block.md) 对比矩阵 |
| 8 | **cycle** 循环过程 | 「周而复始」反馈回路 | 各阶段名称、阶段间转化机制、回路方向 | [flow-cycle](skeletons/flow-cycle.md) 环形 |
| 9 | **flow** 流量分配 | 「X% 流向了…」价值链 | 源节点、目标节点、**流量数值**、阶段划分 | [flow-cycle](skeletons/flow-cycle.md) 桑基 |
| 10 | **timeline** 时间序列 | 年份、日期、「从…到…」 | 时间点/时期、各时间点的事件、因果承接 | [linear-sequence](skeletons/linear-sequence.md) 箭头串 |
| 11 | **parallel-evolution** 并行演变 | 「与此同时…」多领域同步 | 并行实体名称、共享时间轴、各实体在各时间点分别发生了什么 | [lanes](skeletons/lanes.md) 泳道 |
| 12 | **multi-dimensional** 多维评估 | 「在X方面优秀，但Y方面不足」 | 评估维度名称、各维度的评价/得分、评估对象 | [structure-block](skeletons/structure-block.md) 对比矩阵 |
| 13 | **two-dimensional** 二维定位 | 「高X低Y」策略矩阵 | **两个维度名称及极性**、各元素在两维度上的定位 | [matrix-quadrant](skeletons/matrix-quadrant.md) 2×2 |
| 14 | **landscape** 领域全景 | 「主要分为…」生态概览 | 分类维度、各区域/流派名称、代表性实体 | [structure-block](skeletons/structure-block.md) 便当格 |
| 15 | **geographic** 地理分布 | 多地区数据对比 | 地区名称、各地区数据/特征、地区间关系 | [structure-block](skeletons/structure-block.md) 便当格<br>*见下方降级说明* |
| 16 | **composition** 占比构成 | 「X% 是…」份额、构成 | 分类名称、各自百分比（**合计 100%**）、对比的时点/对象 | [pie](skeletons/pie.md) 饼图 |
| 17 | **profile** 多维画像 | 「在 X 个维度上分别是…」 | 维度名称（5–7 个）、统一满分刻度、各对象各维度得分 | [radar](skeletons/radar.md) 雷达图 |
| 18 | **balance** 平衡自评 | 「现状离目标还差…」找短板 | 维度（6–10 个）、现状分、目标分（**同一把尺**） | [wheel](skeletons/wheel.md) 平衡轮 |

### 两个降级说明

- **geographic**：本模块没有地图骨架。需要真实地理时用 [subway-map](styles/subway-map.md) 的简化拓扑表达相对位置和连接；只需要「哪些地区、各自什么特征」时用便当格平铺，不要硬画没有地理底图的假地图。
- **debate / semantic-opposition / stakeholder**：对比矩阵是 fallback。如果正反双方各有 3 个以上论点，矩阵会挤——改用 [hierarchy-tree](skeletons/hierarchy-tree.md) 左右镜像的双树。

## 识别流程

1. **通读材料**，理解主题、章节结构、信息密度
2. **逐条扫上表**，标记材料里出现了哪几种结构（通常 3–6 种）
3. **按提取要点逐项过一遍材料**，确认信息是否充分
   - 信息充分 → 进第 4 步
   - 信息不足（比如 flow 结构但材料里没有具体数值）→ **不画**。桑基和漏斗没有数字就是装饰
4. **给每种结构配骨架**（用上表的映射列）
5. **给每张图定一个叙事隐喻**（见 [metaphors.md](metaphors.md)）
6. **默认用 deck 调色板**（见 [styles/INDEX.md](styles/INDEX.md)）

## 数量控制

**一份材料出 3–5 张图通常就够了。** 质量优先于数量。

超过 5 种结构时，按「和主题的相关度」排序，只留最贴题的那几个。

## 两条纪律

**不要编造。** 所有识别出的结构必须基于材料内容。材料里没说的数字、没说到的关系，不要补。「合理推断」在图上会被当成事实读。

**信息不充分就不画。** 三个常见的「不该画」：

| 情况 | 为什么不该画 |
|---|---|
| flow 结构但没有具体数值 | 桑基的宽度就是数据，没数据就没有图 |
| two-dimensional 但两个维度不独立 | 象限退化成一条对角带，四个象限有两个永远空着 |
| multi-dimensional 但只列了维度没给评价 | 对比矩阵全是空格，读者会以为是漏了 |
| composition 但没有具体份额 / profile·balance 但没有评分 | 饼图的弧长、雷达的半径就是数据——没有数值只能画成等分，那是编造 |

## 提取优先级

按「可视化增值」排序，优先画**图表比纯文字更有效**的结构：

```
高增值：flow（有量级）· composition（有份额）· two-dimensional（空间定位）
        · parallel-evolution（并行对比）· cycle（回路）· hierarchy（拆解）
中增值：network · argument · multi-dimensional · stakeholder · profile · balance
低增值：landscape（容易退化成列表）· timeline（容易退化成项目符号）
```

低增值不是不能画，而是**要额外设计**才能拉开差距：timeline 加上并行泳道或里程碑强调；landscape 用便当格的视觉权重做主次区分。
