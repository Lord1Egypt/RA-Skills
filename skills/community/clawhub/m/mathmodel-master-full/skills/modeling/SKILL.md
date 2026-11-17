---
name: modeling
description: 用于全国大学生数学建模竞赛（国赛/CUMCM）任务。适用于阅读赛题、数据预处理与可视化、模型建立、结果可视化、敏感性分析、模型检验、模型创新和最终论文撰写。使用本 skill 时，最终用户交付物必须是一篇完整数学建模论文，而不是分散的中间分析、代码、图表或说明。
---

# 全国大学生数学建模竞赛（国赛/CUMCM）

## 路由器

本 skill 采用两层结构：

- **静态层**：`static/` 保存稳定、短小、每次都会复用的工作姿态、流程和阶段片段。
- **路由层**：本文件与 `manifest.yaml` 负责判断当前任务阶段，并只加载需要的片段。
- **深层参考层**：`references/` 保存更细的写作和建模规则，只在当前阶段需要展开时读取。

不要凭记忆完成国赛/CUMCM 数模任务。每次调用本 skill 时，先读取 `manifest.yaml`，再按路由加载必要文件。

## 加载协议

### 1. 读取 manifest 与核心规则

读取 [manifest.yaml](manifest.yaml)，再读取 `always_load` 中列出的所有文件。它们定义最终交付纪律、八阶段工作流和输出格式。

### 2. 判断当前阶段

根据用户请求和当前材料，判断当前处于哪些阶段：

- `problem-reading`
- `data-preprocessing-visualization`
- `model-construction`
- `result-visualization`
- `sensitivity-analysis`
- `model-validation`
- `model-innovation`
- `paper-writing`

若用户要求完整建模论文，默认按上述顺序全部推进。若用户只要求修改某一部分，只加载该阶段及其直接相关阶段。

### 3. 加载对应片段

读取 `manifest.yaml` 中 stage 对应的 `static/fragments/stage/*.md`。只读取当前需要的片段，不要一次性加载全部 static 文件。

### 4. 按需读取深层参考

当 stage fragment 不足以完成任务时，再按 `references.on_demand` 读取对应 `references/*.md`。例如需要详细读题拆解模板时读取 `references/problem-reading.md`，需要终稿结构时读取 `references/paper-writing.md`。

### 5. 始终收束到完整论文

最终用户交付物必须是一篇完整论文。中间文件、代码、图表、表格和阶段性判断只能服务于论文，不应作为最终交付替代品。

如果关键题目、附件数据或用户边界缺失，先输出一个很短的 alignment block，列出已知信息、关键假设和最多 2-3 个必须确认的问题；不要在错误前提上直接写完整论文。

## 结构意图

- 路由器保持短小，负责触发、判断和加载。
- 静态片段保存稳定工作流，便于版本化修改。
- 深层参考保存较长细则，只有真正需要时进入上下文。
- 新增阶段或改写规则时，优先更新 `static/` 或 `references/`，不要把正文堆回本文件。
