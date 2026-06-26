# OKX 策略工厂

[English](./README.md)

一个元技能，协调 5 个专业 AI 智能体，完成 OKX OnchainOS 链上交易策略的完整生命周期：开发、回测、部署、发布和迭代。

## 这是什么？

策略工厂是一个 **Agent Team 流水线** —— 不是一个 AI 智能体包揽一切，而是由 Lead 协调者为每个阶段生成专用的专家智能体。每个智能体有严格的输入/输出契约和质量门禁，必须通过才能进入下一阶段。

适合希望用 AI 智能体通过 OKX DEX API 开发、验证、部署并持续优化链上交易策略的开发者。

## 架构

```
用户请求
   │
   ▼
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ Strategy │────▶│ Backtest │────▶│  Infra   │────▶│ Publish  │     │ Iteration│
│  Agent   │     │  Agent   │     │  Agent   │     │  Agent   │     │  Agent   │
│          │     │          │     │          │     │ (并行启动)│     │(上线后)  │
│ 开发策略  │     │ 回测验证  │     │ 部署到VPS │     │ 打包为技能│     │ 复盘优化 │
└──────────┘     └──────────┘     └──────────┘     └──────────┘     └──────────┘
     ▲               │ 失败            │                                  │
     └───────────────┘                 │ 失败 → 自动回滚                   │
     ▲                                                                    │
     └──────────────────── 用户批准优化方案 ──────────────────────────────┘

                    Lead Agent（协调者，不写代码）
```

## 平台兼容性

> **推荐**: Claude Code、Cursor、Gemini CLI —— 支持子智能体/队友生成的 AI 编程 IDE。
>
> **不推荐**: OpenClaw —— OpenClaw 是策略执行运行时，不适合多智能体开发流水线。请在 OpenClaw 上使用独立策略技能（如 `grid-trading`）。

## 安装

**Claude Code**（推荐）:
```bash
npx clawhub install okx-strategy-factory
# 或手动安装:
cp -r okx-strategy-factory ~/.claude/skills/
```

**Cursor**:
```bash
cp -r okx-strategy-factory /path/to/project/.cursor/skills/
```

**Gemini CLI**:
```bash
cp -r okx-strategy-factory /path/to/project/.gemini/skills/
```

## 快速开始

安装后，对你的 AI 智能体说：

```
使用 okx-strategy-factory 技能，为 Base 链上的 ETH/USDC 开发一个网格交易策略。
```

或触发特定阶段：

```
使用 okx-strategy-factory 回测 Strategy/grid-trading/Script/v1.0.0/ 中的网格策略。
```

```
使用 okx-strategy-factory 对正在运行的 ETH 网格策略做迭代复盘 —— 回顾最近 7 天。
```

Lead 智能体会自动协调对应的专家智能体。

## 目录结构

```
okx-strategy-factory/
├── SKILL.md              # 主文档：流水线定义 + 状态机
├── roles/                # 智能体角色定义
│   ├── lead.md           #   协调者 —— 生成智能体、执行门禁
│   ├── strategy.md       #   编写策略代码 + 配置 + 风控档案
│   ├── backtest.md       #   基于历史数据验证策略
│   ├── infra.md          #   通过 SSH 部署到 VPS
│   ├── publish.md        #   将策略打包为跨平台技能
│   └── iteration.md      #   上线后复盘与优化建议
├── templates/            # 结构化模板
│   └── requirements.md   #   策略需求模板（Lead 在 spawn Strategy agent 前填写）
├── references/           # 共享技术参考
│   ├── api-interfaces.md #   适配器接口规范（钱包、DEX、持仓）
│   ├── risk-schema.json  #   risk-profile.json 的 JSON Schema
│   └── strategy-lessons.md # 策略经验库（风控、MTF、成本、陷阱）
├── assets/               # 模板和工具
│   ├── product-skill-template/  # 策略专用打包模板（.tmpl）
│   ├── skill-templates/         # Skill 设计模式模板（pipeline、tool-wrapper 等）
│   └── publish.sh               # Skill 验证与发布脚本
└── hooks/                # 流水线自动化
    ├── task-completed-gate.sh   # 步骤间质量门禁检查
    └── teammate-idle-reassign.sh # 空闲智能体重新分配
```

## 智能体角色

| 角色 | 职责 | 输入 | 输出 |
|------|------|------|------|
| **Lead** | 协调流水线、执行质量门禁、管理状态 | 用户请求 | 生成提示词、更新 state.json |
| **Strategy** | 编写策略逻辑 + 配置 + 风控档案 | `Strategy/{strategy}/requirements.md`（Lead 提炼的结构化需求） | `Strategy/{strategy}/Script/v{ver}/`（strategy.js, config.json, risk-profile.json, README.md） |
| **Backtest** | 基于历史数据验证策略 | 策略脚本目录 | `Strategy/{strategy}/Backtest/v{ver}/`（backtest-report.json, equity-curve.csv） |
| **Infra** | 部署到 VPS（SSH、pm2、健康检查、回滚） | 回测通过的策略版本 | VPS 上运行的进程、VERSION 文件 |
| **Publish** | 将策略打包为跨平台技能 + GitHub 发布 | 回测通过的策略 + 部署确认 | `{strategy}/`（manifest.json, install.sh, SKILL.md） |
| **Iteration** | 分析实盘表现、提出优化建议 | 链上交易记录 + 市场数据 | `Strategy/{strategy}/Iteration/v{ver}-review-{date}.md` |

## 流水线

```
步骤 1: 策略开发
  Lead 从讨论中提炼需求 → 写入 Strategy/{strategy}/requirements.md → 用户确认 → spawn Strategy agent
  门禁: strategy.js + config.json + risk-profile.json + README.md 全部就位
    │
    ▼
步骤 2: 回测验证
  门禁: 合规 PASS + Sharpe > 1.0 + 胜率 > 40%
  失败 → 携带失败详情返回步骤 1
    │
    ▼
步骤 3: 部署到 VPS ────────────────── 步骤 4: 发布为技能（并行启动）
  门禁: pm2 在线 + 30s 内无报错       门禁: manifest.json + install.sh + 适配器
  失败 → 自动回滚到上一版本            GitHub release 等待步骤 3 成功
    │
    ▼
步骤 5: 迭代（上线后，按需触发）
  门禁: 用户确认优化方案
  批准 → 新版本从步骤 1 重新开始（必须重新回测）
```

严格顺序执行，不可跳步。迭代始终触发从步骤 1 的完整重跑。

## 前置条件

- **onchainos CLI** — `npx skills add okx/onchainos-skills`
- **OKX API Key** — 需有 DEX 交易权限
- **OnchainOS Agentic Wallet** — 需启用 TEE 签名
- **Python 3.10+** — 用于回测引擎和交易脚本
- **VPS**（可选） — 用于实盘部署
- **1Password CLI**（可选） — 安全凭证管理（`op`）

## 许可证

Apache-2.0
