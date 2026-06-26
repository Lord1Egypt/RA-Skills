---
name: pans-deal-coach
description: |
  AI算力销售谈判教练。输入客户异议，输出专业应对话术和策略。
  覆盖价格、竞品、技术、流程、安全等20+常见异议场景。
  触发词：谈判话术, 客户异议, 应对策略, 销售教练, objection handling, deal coaching
---

# pans-deal-coach

AI算力销售谈判教练，帮助销售人员应对客户各种异议。

## 功能

- **异议识别**：自动识别客户异议类型（价格/竞品/技术/流程/安全）
- **话术生成**：提供3种版本的话术（简短/详细/邮件）
- **策略建议**：针对客户类型和销售阶段给出定制化建议
- **场景库**：内置20+常见异议场景

## 使用方法

```bash
# 基本使用
python3 scripts/coach.py --objection "你们比AWS贵30%" --type price --client enterprise

# 指定销售阶段
python3 scripts/coach.py --objection "需要内部审批" --type process --stage negotiation

# 查看所有场景
python3 scripts/coach.py --list

# JSON输出（用于集成）
python3 scripts/coach.py --objection "担心稳定性" --json
```

## 参数说明

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `--objection` | 客户异议内容 | 任意文本 |
| `--type` | 异议类型 | price, competitor, tech, process, security |
| `--client` | 客户背景 | startup, enterprise, gov |
| `--stage` | 销售阶段 | discovery, demo, negotiation, close |
| `--list` | 列出所有场景 | - |
| `--lang` | 输出语言 | zh, en |
| `--json` | JSON格式输出 | - |

## 覆盖场景

### 价格异议
- 价格太贵
- 竞品更便宜
- 没有预算
- 需要内部审批

### 竞品异议
- 竞品功能更强
- 竞品市占率高
- 已有供应商

### 技术异议
- 技术栈不兼容
- 担心稳定性
- 性能不满足
- 迁移成本高

### 流程异议
- 决策周期长
- 需要POC
- 多人决策

### 安全异议
- 数据安全顾虑
- 合同条款问题
- 供应商资质

## 输出内容

1. 🎯 异议分析
2. 💡 应对话术（3个版本）
3. 📊 支持材料建议
4. ⚠️ 注意事项
5. 🚀 下一步行动
