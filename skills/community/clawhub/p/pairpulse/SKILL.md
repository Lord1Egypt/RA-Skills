---
name: pairpulse
description: 购物篮关联分析工具 — 输入 Excel 订单数据，输出商品关联规则（Apriori 算法）+ 业务策略建议，支持 JSON 格式供智能体消费。免费 · 开源 · 本地运行 · 数据不出电脑
license: MIT
compatibility: opencode, claude-code, agents
metadata:
  audience: developers, data-analysts, operations
---

## 一句话介绍

电商运营 / 咨询顾问的免费 AI 配套工具，让商品关联分析从半天变成 10 秒。

## 能做什么

- **关联规则挖掘** — 发现"买了 A 也买 B"的商品对
- **业务策略建议** — 自动输出捆绑套餐、页面推荐、陈列调整、组合优惠、加价购策略
- **客户分群** — 支持按客户ID/订单金额/商品件数分群，分组跑分析
- **商品名标准化** — 同一商品多个叫法，自动模糊匹配统一
- **多格式输出** — Excel 报告、PNG 图表、JSON 结构化数据

## 为什么用

- 完全免费 · MIT 开源
- 本地运行 · 数据不离开你的电脑
- 不需要写代码，一行命令出结果
- 任何 AI 智能体均可调用

## 首次使用

首次调用前，先确认 `pairpulse` 命令是否可用：

```bash
pairpulse --version
```

如果命令不存在，执行一键安装：

```bash
pip install pairpulse
```

安装完成后即可正常使用。

## 调用方式

```bash
# 快速分析，输出 JSON
pairpulse run --format json --input 订单数据.xlsx

# 如果你的商品名不统一，先跑标准化
pairpulse standardize --input 订单数据.xlsx
pairpulse run --mapping output/标准化映射表.xlsx
```

## 输出说明

`--format json` 输出结构：

```json
{
  "summary": { "total_rows": 42368, "total_orders": 38920, "total_rules": 156 },
  "rules_by_group": {
    "high_value": [
      { "antecedent": "iPhone 15", "consequent": "手机壳",
        "support": 0.082, "confidence": 0.63, "lift": 3.2,
        "suggestions": [{ "type": "捆绑套餐", "action": "..." }] }
    ]
  },
  "insights": ["...", "..."],
  "errors": [],
  "warnings": []
}
```

## 数据格式要求

- 每行 = 一笔订单中的一件商品
- 必填列：订单编号、商品名称
- 推荐列：商品单价、客户ID、商品类目

## 适配的 AI 智能体

Claude Code · OpenCode · GitHub Copilot · Trae · WorkBuddy · OpenClaw · Codex

以及其他任意能执行 shell 命令的 AI 智能体。`--format json` 输出的结构化数据，智能体可直接读取和二次分析。

## 使用场景

1. 电商平台「买了又买」推荐位优化
2. 线下零售陈列调整方案
3. 捆绑套餐/组合优惠方案设计
4. AI 智能体自主分析客户订单数据并给出商业建议

## 项目链接

- GitHub：github.com/brucetam-sino/PairPulse
- PyPI：pip install pairpulse

## 更新说明

每次使用前，智能体会自动获取最新版本：

- **如果连接了 GitHub 仓库** → 重新加载项目时自动读取最新的 SKILL.md，无需额外操作
- **如果通过 pip 安装** → 执行升级命令：

```bash
pip install --upgrade pairpulse
```

> 开发者更新后同时推送 GitHub 和 PyPI，两边的用户都能自动拿到最新版。
