---
name: label-compliance-audit
description: 智能审核食品包装标签的合规性，支持图片/PDF设计稿；当用户需要审核标签强制性标识、营养标签规范性、声称用语合规性或格式要求时使用
---

# 标签合规审核

## 任务目标
- 本 Skill 用于：食品包装标签的智能合规审核
- 能力包含：识别标签内容、对照GB7718/GB28050标准检查、生成审核报告
- 触发条件：用户上传包装设计稿并要求审核标签合规性

## 前置准备
- 依赖说明：无需外部依赖，使用智能体原生能力
- 非标准文件/文件夹准备：无需额外准备

## 操作步骤
- 标准流程：
  1. 读取设计稿
     - 使用图像识别工具提取标签中的所有文字和图片内容
     - 识别关键信息：品名、配料表、净含量、生产者信息、营养标签、声称用语等
  2. 选择审核模式
     - 模式A：智能体自主审核
       - 基于以下参考标准进行全面审核
       - 生成结构化审核报告
     - 模式B：逐项清单比对
       - 参考 `assets/audit-checklist.md` 中的审核清单
       - 逐项对照并记录审核结果
  3. 执行审核（参考以下文档）
     - 强制性标识完整性：见 [references/gb7718-standard.md](references/gb7718-standard.md)
     - 营养标签规范性：见 [references/gb28050-standard.md](references/gb28050-standard.md)
     - 声称用语合规性：见 [references/claims-guideline.md](references/claims-guideline.md)
     - 格式要求（字体大小、对比度）：见 [references/gb7718-standard.md](references/gb7718-standard.md)
     - 过敏原标识：见 [references/gb7718-standard.md](references/gb7718-standard.md)
  4. 生成审核报告
     - 列出所有不符合项
     - 提供整改建议
     - 标注风险等级（严重/一般/轻微）

- 可选分支：
  - 当设计稿为PDF时：先提取页面内容，再进行图像识别
  - 当需要详细NRV计算：参考GB28050标准中的计算公式逐项验证

## 资源索引
- 领域参考：
  - [references/gb7718-standard.md](references/gb7718-standard.md)（何时读取：审核强制性标识、格式要求、过敏原）
  - [references/gb28050-standard.md](references/gb28050-standard.md)（何时读取：审核营养标签、NRV计算）
  - [references/claims-guideline.md](references/claims-guideline.md)（何时读取：审核声称用语）
- 资产模板：
  - [assets/audit-checklist.md](assets/audit-checklist.md)（用途：逐项清单比对审核）

## 注意事项
- 审核时需全面识别标签中的所有文字信息，包括小字说明
- 营养标签的NRV%需根据GB28050中的计算方法逐项验证
- 声称用语必须满足特定条件才能使用（如"无糖"需≤0.5g/100g）
- 格式要求需关注字体高度（≥1.8mm）和背景对比度
- 过敏原标识需明确标注，采用加粗或特殊字体

## 使用示例

### 示例1：智能体自主审核
- 功能说明：上传设计稿，智能体自动完成全面审核
- 执行方式：智能体读取参考标准，自主判断并生成报告
- 关键要点：
  - 全面识别标签内容
  - 逐项对照标准要求
  - 生成结构化审核报告
- 示例：用户上传饼干包装设计稿，要求审核标签合规性

### 示例2：逐项清单比对
- 功能说明：使用审核清单逐项核对标签内容
- 执行方式：参考 assets/audit-checklist.md 逐项检查
- 关键要点：
  - 按清单顺序逐项确认
  - 记录每一项的审核结果
  - 汇总不符合项
- 示例：用户要求使用清单方式审核饮料标签

### 示例3：营养标签专项审核
- 功能说明：重点审核营养标签的规范性和NRV计算
- 执行方式：重点读取 references/gb28050-standard.md
- 关键要点：
  - 验证能量、蛋白质、脂肪等核心营养素标注
  - 计算并核实NRV%
  - 检查营养声称的合规性
- 示例：用户需要验证酸奶营养标签的NRV%计算准确性
