---
name: moneybigA
description: >
  moneybigA — A股/港股/美股机构级多框架股票分析 Skill。
  专为主动交易者和研究者设计：筹码分布+主力控盘、智能资金概念(SMC)订单块/公允价值缺口/流动性清扫、
  威科夫吸筹/派发六阶段、波浪理论浪级判断、MACD背离、量价关系；
  基本面层：杜邦三因子、DCF内在价值、PEG/EV-EBITDA估值、波特五力行业竞争；
  量化层：Alpha101多因子评分体系（动量/价值/成长/质量/资金流）。
  自动搜集实时数据，输出带综合评分仪表盘的交互式 HTML 报告，
  含分级买卖信号（HIGH/MEDIUM/LOW 置信度）、风险等级触发条件、止损参考与目标价。
  Trigger on：股票分析、筹码分布、买卖信号、主力控盘、短线机会、上证指数、基本面分析、
  财务分析、估值分析、财报综合分析、行业分析、技术分析、量化选股、波浪理论、威科夫、
  SMC、Order Block、Alpha因子、stock analysis、chip distribution、buy signal、
  sell signal、fundamental analysis、valuation、DCF、financial report analysis。
keywords:
  - 股票分析
  - 筹码分布
  - 主力控盘
  - 买卖信号
  - 短线机会
  - 上证指数
  - 技术分析
  - 基本面分析
  - 财务分析
  - 估值分析
  - 财报分析
  - 行业分析
  - 量化选股
  - Alpha因子
  - 波浪理论
  - 威科夫
  - 威科夫吸筹
  - 威科夫派发
  - SMC
  - 智能资金
  - Order Block
  - Fair Value Gap
  - 流动性清扫
  - MACD背离
  - 量价分析
  - 杜邦分析
  - DCF估值
  - PE PB ROE
  - 竞争分析
  - 行业景气
  - stock analysis
  - chip distribution
  - buy signal
  - sell signal
  - fundamental analysis
  - valuation
  - financial report
  - sector analysis
  - smart money
  - wyckoff
  - elliott wave
metadata:
  openclaw:
    runtime:
      node: ">=18"
---

# 股票金融分析 (Stock Financial Analysis)

> 机构级多框架分析引擎 — 技术面 × 基本面 × 量化因子 × 智能资金追踪

---

## Purpose & Capability

moneybigA 是面向**主动交易者、量化研究者和价值投资者**的机构级股票分析 Skill。

**核心能力：**

| 维度 | 能力 |
|------|------|
| 技术面 | 筹码分布+主力控盘、威科夫六阶段、SMC（订单块/FVG/流动性清扫）、波浪理论、MACD背离、量价综合 |
| 基本面 | 杜邦三因子、现金流质量验证、财务预警、DCF内在价值+安全边际、PEG/EV-EBITDA、波特五力 |
| 量化因子 | Alpha101体系（动量/价值/成长/质量/资金流）综合评分 |
| 信号系统 | 综合评分（0-100）、分级买卖信号、置信度（HIGH/MEDIUM/LOW）、风险等级 |
| 输出 | 交互式单文件 HTML 仪表盘，含多模块卡片、圆形评分仪表、量化因子热力图 |

**不做的事：**
- 不执行真实交易或下单操作
- 不提供实时 Level2 盘口数据
- 不保证分析结果的投资收益，所有输出不构成投资建议
- 不回测历史交易策略

---

## Instruction Scope

**在 scope 内（会处理）：**
- "分析一下 000001 的筹码分布和主力控盘"
- "帮我看看茅台的基本面，值不值得买"
- "上证指数现在处于什么位置，有没有短线机会"
- "解读这份财务报告，综合给出买卖建议"
- "这只股票的威科夫阶段在哪里？有没有 SMC 订单块"
- "帮我做个行业竞争分析，用波特五力"
- "AAPL 的 DCF 估值和 PE 历史分位分别在哪"

**不在 scope 内（不处理）：**
- 直接下单或执行交易（无券商 API 接入）
- 内幕消息或非公开信息查询
- 提供具体仓位比例或资金管理方案
- 期货、期权复杂衍生品定价

**凭证缺失时的行为：**
本 Skill 无需任何 API 凭证。所有数据通过 WebSearch 公开渠道搜集。若数据无法获取，会明确告知并基于可用信息完成分析。

---

## Credentials

本 Skill 无需任何 API 密钥、token 或账号凭证。

| 操作 | 凭证 | 范围 |
|------|------|------|
| 数据搜集 | 无 | 通过 WebSearch 访问公开信息 |
| 分析计算 | 无 | 本地 LLM 推理 |
| HTML 输出 | 无 | 生成单文件 artifact |

**不会读取或写入：** 任何本地文件、环境变量、系统配置。

---

## Persistence & Privilege

**写入路径：** 无。本 Skill 仅在对话上下文中运行，不向任何本地路径写入文件。

| 路径 | 内容 | 触发条件 |
|------|------|---------|
| 无 | — | — |

**不写入的内容：**
- 不写入任何本地文件或目录
- 不修改系统配置或 shell 环境
- 不持久化用户数据或分析历史
- 不注册 cron 或后台进程

**卸载方法：**
```bash
rm -rf ~/.claude/skills/moneybigA
```

---

## Install Mechanism

### 从 clawHub 安装（推荐）

```bash
clawhub install moneybigA
```

### 手动安装

```bash
cp -r /path/to/moneybigA ~/.claude/skills/moneybigA/
```

### 验证安装

```bash
ls ~/.claude/skills/moneybigA/
# 应看到：SKILL.md  _meta.json  package.json  .clawhub/
```

### 环境变量

本 Skill 无需配置任何环境变量，开箱即用。

### 使用方法

安装后直接在 Claude Code 中输入分析请求即可自动触发：

```
/moneybigA 分析 000001
/moneybigA 帮我看一下茅台的基本面
```

---

## 分析框架

### 技术面矩阵

- **筹码分布**：获利盘比例、筹码集中度、主力成本区、穿透率 → 主力控盘判断
- **威科夫方法**：吸筹六阶段（Spring→SOS→主升浪）/ 派发六阶段（UTAD→SOW→下跌）
- **SMC 智能资金**：订单块（Order Block）/ 公允价值缺口（FVG）/ 流动性清扫
- **波浪理论**：大中小三级浪判断，3浪确认买点，5浪末+背离提示顶部
- **MACD背离**：顶/底背离识别，量价背离（出货/吸筹）

### 基本面矩阵

- **杜邦分析**：ROE = 净利润率 × 资产周转率 × 权益乘数，来源质量判断
- **财务健康**：现金流质量（OCF/净利润）、FCF、负债率、利息覆盖率、财务雷区
- **DCF估值**：5年FCF预测 + 永续增长 + WACC折现，安全边际 ≥30% 为显著低估
- **相对估值**：PE历史分位、PEG（<1低估）、EV/EBITDA跨行业比较
- **波特五力**：竞争强度、进入壁垒、替代品、供应商/客户议价能力

### 量化因子（Alpha101体系）

动量 / 价值（EP/BP）/ 成长（营收增速/ROE趋势）/ 质量（现金流/毛利率稳定性）/ 资金流（大单净流入/北向/融资余额）

### 信号系统

| 信号 | 分数 | 标志 |
|------|------|------|
| 强烈买入 | ≥75 | 多框架共振，置信度 HIGH |
| 温和买入 | 60-75 | 2+ 技术信号一致，置信度 MEDIUM |
| 观望 | 40-60 | 信号混沌，等待方向 |
| 减仓 | <40 | 风险信号触发，置信度 MEDIUM |
| 强烈卖出 | 基本面恶化或派发Phase C/D | 置信度 HIGH |

### HTML 输出

单文件交互式仪表盘，深色金融风格（#0d1117 背景），包含：
股票信息头 / 技术面分析卡 / 基本面评分卡 / 量化因子热力图 / 综合评分圆形仪表（0-100）/ 操作建议与止损目标价 / 风险免责声明

---

> **免责声明**：本分析基于公开信息，仅供参考和学习研究，**不构成任何投资建议**。股市有风险，投资需谨慎。
