# 骨架路由 — 关系类型决定图形

> **本文件自足**：画图第一步不是选样式，是回答「这些节点之间到底是什么关系」。关系类型决定骨架家族。选错骨架，后面所有坐标都是白算。

## 两条入口

| 入口 | 什么时候走 | 在哪 |
|---|---|---|
| **关系驱动** | 已经知道要画什么关系，只是不知道怎么画 | 本文件 |
| **文档驱动** | 用户丢来一篇文章/一段材料，说「帮我画图」 | [../structures.md](../structures.md) — 18 种信息结构识别，**同一张表带出骨架映射列** |

两条路汇进同一批骨架文件。

## 第一步：判断关系类型

| 关系 | 判定问句 | 骨架家族 |
|---|---|---|
| **Hierarchy** 层级 / 包含 | A 包含 B？A 是 B 的上级？ | [hierarchy-tree](hierarchy-tree.md) |
| **Sequence** 时序 | A 发生在 B 之后？ | [linear-sequence](linear-sequence.md) |
| **Cycle** 循环 | A 强化 A？流程回到起点？ | [flow-cycle](flow-cycle.md) |
| **Comparison** 对比 | A 与 B 相比？现状 vs 目标？ | [structure-block](structure-block.md) |
| **Matrix** 矩阵 | 两个维度交叉分类？ | [matrix-quadrant](matrix-quadrant.md) |
| **Framework** 框架 | 3 层 / 4 支柱 / 5 维度的结构化模型？ | [structure-block](structure-block.md) |
| **Strategy** 战略 | 愿景 → 战略 → 执行的承接？ | [hierarchy-tree](hierarchy-tree.md) 金字塔壳 |
| **Mapping** 映射 | 两组实体之间的对应？ | [hierarchy-tree](hierarchy-tree.md) 单边树 |
| **Growth** 演进 | 我们在哪，下一步去哪？ | [linear-sequence](linear-sequence.md) 阶梯 |
| **Evidence** 论证 | 主张靠什么证据支撑？ | [evidence](evidence.md) 图尔敏 |
| **Flow** 流量 | X 从哪来，流向哪，带多少量？ | [flow-cycle](flow-cycle.md) 桑基 |
| **Composition** 占比 | 各部分加起来是一个整体？份额各多少？ | [pie](pie.md) |
| **Profile** 画像 | 同一组维度上，对象的得分形状如何？ | [radar](radar.md) |
| **Balance** 平衡 | 单个对象的现状 vs 目标，短板在哪？ | [wheel](wheel.md) |

**关键区分**：节点多且**多对多双向**（A↔B↔C 都相连）时，不要硬塞进中心辐射（Hub & Spoke）——那会丢掉交叉关联，退化成一张关系网。此时用 [network-hub](network-hub.md) 的网络图，或拆成分组矩阵。

## 第二步：骨架 → 具体文件

| 骨架 | 什么时候选它 | 什么时候别选 |
|---|---|---|
| [linear-sequence](linear-sequence.md) | 有明确先后顺序，横向阅读 | 顺序不重要，只是并列 |
| [hierarchy-tree](hierarchy-tree.md) | 严格的从属关系，深度 2–3 层 | 兄弟节点之间还有横向关系（改用 network-hub） |
| [matrix-quadrant](matrix-quadrant.md) | 恰好两个**独立**维度交叉分类 | 维度超过 2 个（改用 structure-block 的对比矩阵） |
| [flow-cycle](flow-cycle.md) | 循环、收敛、带量级的流动 | 单向无分叉的直线流程（改用 linear-sequence） |
| [network-hub](network-hub.md) | 多对多的关系网 / 中心辐射 | 严格的树状从属（用 hierarchy-tree，更清晰） |
| [lanes](lanes.md) | 多个实体在同一时间轴上并行推进 | 只有一条线在走（用 linear-sequence） |
| [structure-block](structure-block.md) | 框架分层、并列模块、对比表格 | 需要表达关系（框和框之间没有关系线） |
| [evidence](evidence.md) | 主张 + 证据 + 推理的论证结构 | 只是罗列事实（用 structure-block） |
| [wave-timeline](wave-timeline.md) | 起伏波浪 + 整体向上推进，过程曲折抵达 | 时间点无波折（用 lanes） |
| [icon-rail](icon-rail.md) | 3–6 项**并列**的属性/方面，水平对齐 | 节点之间有顺序（用 linear-sequence） |
| [card-row](card-row.md) | 3–5 张**图文卡片**水平对齐，每张上半图下半文 | 内容是数字对比（用 structure-block） |
| [pie](pie.md) | 占比构成；1–3 个饼的对比（同分类同色） | 比较绝对值大小（用表格或条形） |
| [radar](radar.md) | 2–3 个对象、5–7 个统一刻度的维度叠比 | 单对象自评找短板（用 wheel） |
| [wheel](wheel.md) | 单对象自评：现状 vs 目标、缺口即优先级 | 多对象叠比（用 radar） |

## 第三步：换叙事外壳

骨架定完之后，再问「这页要什么情绪」——阶梯、金字塔、冰山、漏斗、飞轮等隐喻在**同一副骨架上换壳**，不改变路由。查 [../metaphors.md](../metaphors.md)。

**一页只讲一个隐喻。不要结构叠隐喻。**

## 第四步：定配色

默认用 deck 自己的调色板（[../../style-bootstrap.md](../../style-bootstrap.md)），保证图和正文属于同一份 deck。8 个备选风格见 [../styles/INDEX.md](../styles/INDEX.md)。

## 硬约束

- **单图节点数 ≤ 7** 是黄金法则。超了拆页、聚合，或降级成表格。
- **树的层级 ≤ 3。** 第 4 层开始线索就断了。
- **一页一个 Pattern。** 不要把诊断（问题树）、战略（金字塔）、转型（前后对比）混在一张图里。
- **没匹配就降级。** 找不到合适的关系类型时，用最接近的通用结构（箭头串 / 关系树 / 2×2），不要硬画。

画布、间距、线宽的共同尺度见 [../craft/canvas.md](../craft/canvas.md)。
