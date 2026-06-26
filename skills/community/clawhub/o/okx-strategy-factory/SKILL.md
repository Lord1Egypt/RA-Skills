---
name: okx-strategy-factory
description: "Agent Team 工厂：协调 5 个 AI Agent（Strategy/Backtest/Infra/Publish/Iteration）完成 OKX OnchainOS 链上交易策略的全生命周期——开发、回测、部署、发布、迭代。支持多策略并行，每个策略独立状态管理。触发词：策略开发、agent team、回测、迭代策略、发布 skill、部署策略。"
license: Apache-2.0
metadata:
  author: SynthThoughts
  version: "2.0.0"
  pattern: "pipeline"
  steps: "5"
---

# OKX Strategy Factory — Agent Team

协调 5 个专家 Agent 完成交易策略全生命周期。Lead 只协调不写代码。

```
Strategy → Backtest → Infra(deploy) → LIVE
              ↑          ↑ (parallel)
              │        Publish → GitHub Release
              │
         Iteration ← (定时/手动复盘)
```

**这是文件夹 Skill**。按需读取 `roles/`、`references/`、`assets/`，不要一次性加载全部。

## Strategy Selection

Lead 启动 Pipeline 时**必须**指定策略名称 `{strategy}`，所有路径和状态按策略隔离。

- **已有策略**: `grid-trading`、`cl-lp-rebalancer`
- **新策略**: 指定新名称即可，自动创建 `Strategy/{strategy}/` 工作空间
- 每个策略拥有独立的 `Strategy/{strategy}/state.json`，互不干扰
- 同一时间可有多个策略处于不同阶段（如 grid-trading 在 LIVE，cl-lp-rebalancer 在 BACKTEST）

## When to Use

- 开发新交易策略 → Lead 指定 `{strategy}` 名称，读 `roles/lead.md`，spawn strategy + backtest
- 回测 → spawn backtest，读 `roles/backtest.md`，指定 `{strategy}`
- 部署到 VPS → spawn infra，读 `roles/infra.md`，指定 `{strategy}`
- 发布为独立 Skill → spawn publish，读 `roles/publish.md`，指定 `{strategy}`
- 迭代/复盘 → spawn iteration，读 `roles/iteration.md`，指定 `{strategy}`
- 全流程 → spawn 全部 teammate，Lead 指定 `{strategy}` 后协调

**示例**:
```
"启动 grid-trading 策略的回测"
"为 cl-lp-rebalancer 执行全流程 Pipeline"
"新建策略 momentum-breakout，从 Step 1 开始"
```

## Pipeline: Execution Steps

**CRITICAL RULE**: Steps MUST execute in order. Do NOT skip steps or proceed past a gate.

### Step 1: Strategy Development

**Load**: `roles/lead.md`（第一跳流程）+ `roles/strategy.md` + `references/api-interfaces.md` + `references/strategy-lessons.md`

**Actions**:
1. Lead 从主窗口讨论中提炼需求，填写 `templates/requirements.md` 模板，写入 `Strategy/{strategy}/requirements.md`
2. Lead 展示需求给用户确认（用户可修正）
3. 确认后 spawn strategy teammate，prompt 指向需求文件
4. Strategy agent 输出到 `Strategy/{strategy}/Script/v{version}/`
5. Lead 验证产出完整性

**Gate** (ALL must pass):
- [ ] `strategy.js` 或 `.ts` 存在，无硬编码参数
- [ ] `config.json` 存在，所有可调参数已外置
- [ ] `risk-profile.json` 存在且字段完整（校验 `references/risk-schema.json`）
- [ ] `README.md` 存在，含收益预期和适用市场条件

### Step 2: Backtest Validation

**Load**: `roles/backtest.md`

**Input**: Step 1 输出的 `Strategy/{strategy}/Script/v{version}/`

**Actions**:
1. Spawn backtest teammate
2. 拉取历史行情数据
3. 运行回测，输出到 `Strategy/{strategy}/Backtest/v{version}/`
4. 执行 Compliance Check：实际指标 vs `risk-profile.json` 声明值

**Gate**:
- [ ] Compliance 全部 PASS + Sharpe > 1.0 + Win Rate > 40% → **PASS**
- [ ] 任一 Compliance FAIL → **FAIL**，退回 Step 1 附失败详情
- [ ] Compliance PASS 但指标 borderline → **CONDITIONAL**，请用户决定

### Step 3: Local Validate + Deploy to VPS

**Load**: `roles/infra.md`

**Input**: 通过回测的策略版本

**Actions**:
1. Spawn infra teammate
2. **本地验证**: `./deploy.sh {strategy} validate` — 3 tick dry-run，验证启动 + RPC + 钱包
3. 本地验证通过后，`./deploy.sh {strategy} production` — 部署到 VPS
4. 健康检查通过后更新 `VERSION`

**Gate (Local)**:
- [ ] 本地 3 tick dry-run 全部成功
- [ ] onchainos 连接 + 价格/余额查询正常
- [ ] 失败 → 退回 Step 1 修复

**Gate (Production)**:
- [ ] 进程存活（pm2 status → "online"）
- [ ] 启动 10s 内无错误日志
- [ ] 失败 → 自动回滚到上一版本

### Step 4: Publish as Skill

**Load**: `roles/publish.md` + `assets/product-skill-template/`

**Input**: 通过回测的策略 + deploy 成功确认

**Actions**:
1. Spawn publish teammate（可在 Step 3 并行开始抽象）
2. 从 `assets/product-skill-template/` 读取产品 Skill 模板
3. 生成独立 Skill 包到 `{strategy}/`（仓库根目录下，与策略同名）
4. GitHub release 等待 Step 3 成功后执行

**Gate**:
- [ ] `manifest.json` 存在（Single Source of Truth）
- [ ] 三平台 adapter 均已生成（SKILL.md / agents.md / openclaw.yaml）
- [ ] `install.sh` 存在且可执行
- [ ] GitHub tag + release 创建成功

### Step 5: Iteration (Post-LIVE)

**Load**: `roles/iteration.md`

**Input**: 链上交易记录 + 行情数据

**Actions**:
1. Spawn iteration teammate（定时或手动触发）
2. 分析表现、提取因果关系、输出优化方案
3. 输出到 `Strategy/{strategy}/Iteration/v{version}-review-{date}.md`
4. **用户确认后** → 回到 Step 1 生成新版本 → 必须重走 Step 2

**Gate**:
- [ ] 优化方案已输出
- [ ] 用户在聊天中确认 — **绝不自动执行**
- [ ] 新版本回到 Step 1，必须走完整 Pipeline

## State Machine

每个策略独立维护状态，互不影响。

```
DRAFT → BACKTEST → PASSED → LOCAL_VALIDATING → LOCAL_VALIDATED → DEPLOYING → LIVE → ITERATION_REVIEW
                 → FAILED → DRAFT (revision)
                 → CONDITIONAL → (user decides)
LOCAL_VALIDATING → LOCAL_FAILED → DRAFT (fix issues)
DEPLOYING → DEPLOY_FAILED → rollback + DRAFT or retry
ITERATION_REVIEW → APPROVED → DRAFT (new version, must re-backtest)
                 → REJECTED → LIVE (keep current)
```

Track in `Strategy/{strategy}/state.json`。Log every transition: `[STATE] {strategy} v{ver}: {OLD} → {NEW} | {reason}`

## Failure & Rollback

```
IF Step N fails for strategy {strategy}:
  1. Log failure reason to Strategy/{strategy}/state.json
  2. Step 2 fail → 退回 Step 1（Strategy 修订），附失败详情
  3. Step 3 fail → Infra 自动回滚到上一版本
  4. Step 4 fail → 不影响线上运行，可重试 Publish
  5. Step 5 fail → 保持当前版本，通知用户
  6. DO NOT proceed to next step
```

## Anti-Patterns

| Pattern | Problem |
|---|---|
| Lead 自己写代码 | Lead 只协调，代码由 Strategy agent 写 |
| 跳过 Backtest 直接部署 | 包括 Iteration 新版本也必须回测 |
| 自动执行 Iteration 优化 | 必须用户确认 |
| risk-profile.json 缺失 | 直接 reject，不要"帮忙补全" |
| 同时部署两个版本 | 同一策略同一时间只有一个 DEPLOYING |
| 修改已发布版本目录 | 版本不可变，只能创建新版本 |
| 2 次迭代未改善仍继续 | 应建议暂停策略或重新设计 |
| 启动 Pipeline 未指定策略名 | Lead 必须先明确 `{strategy}`，否则拒绝执行 |
