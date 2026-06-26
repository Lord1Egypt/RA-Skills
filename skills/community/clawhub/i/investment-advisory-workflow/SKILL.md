---
name: investment-advisory-workflow
version: 1.2.0
description: "［何时使用］当用户需要投顾服务时；当用户说'最近 XX 怎么看'、'这个事件有什么用'、'帮我看看持仓'、'100 万怎么配置'、'大跌了怎么办'时触发。场景驱动的投顾全流程，融合四专家思维。"
author: 燃冰 & ant
created: 2026-04-24
skill_type: 通用🟡
allowed-tools: [Bash, Read, Write, Exec, WebSearch]
related_skills: [investment-workflow, fund-analyzer-pro, holding-diagnoser, fund-allocator, decision-checklist, companion-script, expression-layer]
tags: [投资顾问，场景驱动，工作流，资产配置，行为金融]
---

# investment-advisory-workflow: 投资顾问工作流 🎯

## 📋 功能描述

帮助用户**系统化执行投顾全流程**。融合林奇 (洞察)/卡尼曼 (行为)/芒格 (逆向)/马利克 (系统) 四位专家思想，覆盖 5 个用户场景。

**适用场景：**
- 市场解读 / 事件分析 / 持仓诊断 / 资产配置 / 行为纠偏

**边界条件：**
- 不替代持牌投顾服务
- 输出为 Markdown 报告，需配合 data_layer / mcp-aktools / qieman-mcp 获取真实数据
- 场景识别依赖用户输入关键词与情绪表达
- **KYC 前置**：资产配置场景（场景 4）必须先收集用户年龄/风险偏好/金额/期限，不直接给配置方案
- **四专家标注**：输出必须包含 [林奇视角]/[卡尼曼视角]/[芒格视角]/[马利克视角] 标注，确保思维融合
- **隐私保护**：检测到敏感信息（身份证/银行卡）必须脱敏，不入库

---

## 🔄 5 个核心场景

| 场景 | 触发词 | 调用步骤 | 输出 |
|------|--------|---------|------|
| 市场解读 | "最近 XX 怎么看？" | market-scan → industry-rank → plain-explain → ljg-card | Markdown + PNG 卡片 |
| 事件分析 | "这个事件有什么用？" | market-scan → industry-rank → multi-view → plain-explain → decision-integrate | Markdown 影响分析 |
| 持仓诊断 | "帮我看看持仓" | data-query → holding-diagnoser → decision-checklist → fund-allocator → report-generator | Markdown 诊断报告 |
| 资产配置 | "100 万怎么配置？" | decision-checklist → fund-allocator → ljg-roundtable → IPS 模板 → report-generator | Markdown 配置方案 |
| 行为纠偏 | "大跌了怎么办？" | market-scan → companion-script → ljg-relationship → problem-mapper → plain-explain | Markdown 纠偏方案 |

详细四专家框架 → `references/four-experts.md`
六阶段能力库 → `references/six-stages.md`
共享 Skill 说明 → `references/shared-skills.md`

---

## ⚠️ 常见错误

**错误 1：混淆投资工作流与投顾工作流**
```
问题：
• 用户问"帮我看看持仓"，却调用投资工作流的 stock-research
• 输出偏重标的分析，忽略用户心理与行为纠偏

解决：
✓ 投顾工作流核心是"帮别人"，侧重 KYC + 行为干预 + 陪伴
✓ 投资工作流核心是"自己投"，侧重标的分析 + 决策验证
✓ 严格匹配场景定义
```

**错误 2：忽略四专家视角融合**
```
问题：
• 输出只有数据，没有行为纠偏或逆向思考
• 像数据报告，不像投顾建议

解决：
✓ 每个场景必须融合至少 2 个专家视角
✓ 标注 [林奇视角]/[卡尼曼视角]/[芒格视角]/[马利克视角]
✓ 输出包含"洞察 + 行为 + 逆向 + 系统"四维结构
```

**错误 3：配置方案硬编码**
```
问题：
• 直接给固定比例，不协商
• 忽略市场观点动态调整

解决：
✓ fund-allocator 必须输出基础配置 + 调整后配置
✓ 生成协商点（风险偏好 vs 配置比例）
✓ 标注调整理由与置信度
```

**错误 4：情绪识别缺失（冷冰冰）**
```
问题：
• 用户说"大跌了，我好慌"，AI 直接给数据报告
• 忽略情绪，导致建议"冷冰冰"，可能引发非理性操作

解决：
✓ 阶段 1 必须检测情绪词（"慌"、"割肉"、"好怕"、"大跌"）
✓ 若检测到情绪，优先调用 companion-script 安抚话术
✓ 原则：先处理情绪，再处理问题
```

**错误 5：KYC 前置不足（无画像不配置）**
```
问题：
• 用户问"100 万怎么配"，AI 直接给比例
• 未收集年龄/风险偏好/期限，配置方案不匹配

解决：
✓ 执行"无 KYC，不配置"原则
✓ 若信息不全，暂停配置流程，先引导用户完成 KYC 问卷
✓ 输出中必须包含"基于您的风险等级为 XX"的声明
```

**错误 6：隐私保护缺失**
```
问题：
• 用户输入身份证号/银行卡号，AI 原样输出或入库
• 数据安全风险

解决：
✓ 立即脱敏：输出时掩码处理（如"6222 **** **** 1234"）
✓ 安全提示：提醒用户"请勿在对话中发送完整身份证号/银行卡号"
✓ 不入库：敏感信息不写入知识库/日志
```

---

## 🧪 使用示例

**输入：**
```
最近消费怎么看？
```

**预期输出：**
- 识别场景：市场解读
- 调用：market-scan → industry-rank → plain-explain → ljg-card
- 输出：Markdown 解读 + PNG 卡片（含四专家视角标注）

**输入：**
```
大跌了，我好慌，要不要割肉？
```

**预期输出：**
- 识别场景：行为纠偏 + 情绪检测
- 调用：market-scan → companion-script（安抚）→ ljg-relationship（行为识别）→ problem-mapper（纠偏）
- 输出：Markdown 安抚话术 + 纠偏方案

**输入：**
```
100 万怎么配置？
```

**预期输出：**
- 识别场景：资产配置
- 调用：decision-checklist（KYC 问卷）→ fund-allocator → ljg-roundtable → IPS 模板 → report-generator
- 输出：Markdown 配置方案 + IPS（若 KYC 不全，先询问）

---

## 🔧 故障排查

| 问题 | 检查项 |
|------|--------|
| 不触发 | description 是否包含触发词？用户输入是否匹配场景？ |
| 数据为空 | data_layer 是否安装？mcp-aktools/qieman-mcp 是否运行？ |
| 输出像投资报告 | 是否混淆投资工作流？检查场景定义与专家视角融合 |
| 配置无协商点 | fund-allocator 是否调用？是否生成协商点？ |
| 缺乏行为纠偏 | 是否调用 companion-script / ljg-relationship？ |
| 情绪未识别 | 是否检测情绪词？是否优先安抚？ |
| KYC 缺失 | 是否执行"无 KYC 不配置"？是否先询问画像？ |
| 隐私泄露 | 是否检测敏感信息？是否脱敏输出？ |

---

## 🔗 相关资源

- 四专家框架：`references/four-experts.md`
- 六阶段能力库：`references/six-stages.md`
- 共享 Skill 文档：`references/shared-skills.md`
- 报告模板：`templates/report-template.md`
- 标准参考：`docs/SKILL-STANDARD-v3.md`
