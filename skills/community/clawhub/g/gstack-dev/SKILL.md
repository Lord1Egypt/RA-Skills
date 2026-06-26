---
name: gstack-dev
description: >
  Gstack式AI工程团队开发模式。基于Y Combinator CEO Garry Tan开源的gstack方法论，
  将单一AI助手转化为虚拟工程团队。适用场景：新项目启动、功能开发、代码重构、Bug修复、
  技术方案评审、部署上线、团队Sprint规划、代码审查、E2E测试。
  触发词：gstack、用gstack模式、工程团队模式、Sprint开发、角色化开发、虚拟团队、
  office-hours、CEO review、QA测试、安全审计、canary发布、Sprint回顾、
  用团队模式开发、多角色协作开发、专业分工开发
version: 1.0.0
author: Based on Garry Tan's gstack (YC CEO), adapted for WorkBuddy
---

# gstack-dev — AI 虚拟工程团队技能

> **核心理念（来自 YC CEO Garry Tan）**：
> 1人 = 20人工程团队。通过**专业化角色 + Sprint流水线 + 安全工具层**，
> 让每次开发都经过完整的企业级工程流程。

---

## 一、架构总览

```
┌─────────────────────────────────────────────────┐
│                  gstack-dev                      │
├──────────┬──────────┬───────────────────────────┤
│ 角色层   │ 流水线层  │ 工具层                     │
│(Roles)   │(Sprint)  │(Tools)                    │
├──────────┼──────────┼───────────────────────────┤
│ /think   │ Phase 1  │ /freeze   编辑锁定        │
│ /plan    │ Phase 2  │ /careful  危险操作警告     │
│ /build   │ Phase 3  │ /guard    锁定+警告       │
│ /review  │ Phase 4  │ /xcheck   多模型交叉验证   │
│ /test    │ Phase 5  │ /browse   真实浏览器验证   │
│ /ship    │ Phase 6  │                            │
│ /reflect │ Phase 7  │                            │
└──────────┴──────────┴───────────────────────────┘
```

---

## 二、7阶段 Sprint 流水线（核心）

### 完整流程图

```
Phase 1: THINK ──→ Phase 2: PLAN ──→ Phase 3: BUILD
     ↓ 需求定义            ↓ 架构设计          ↓ 编码实现
  挑战需求框架         CEO+Eng+Design Review  代码生成
     
Phase 4: REVIEW ──→ Phase 5: TEST ──→ Phase 6: SHIP
     ↓ 生产级审查         ↓ E2E测试           ↓ 部署上线  
  找隐含bug          浏览器真实验证        CI/CD+监控
  
     ↓
Phase 7: REFLECT
     ↓ 回顾改进
  统计+优化建议
```

### 各阶段详解

#### Phase 1: THINK — 需求思考（对应 `/office-hours`）
- **触发**: 用户提出新需求或功能想法
- **角色**: 产品顾问（PM视角）
- **输出**: 经过挑战的需求定义文档
- **核心动作**: 
  - 问 6 个强迫性问题（见 roles/think.md）
  - 不执行，只重新定义问题
  - 产出：需求规格 + 成功指标 + MVP范围

#### Phase 2: PLAN — 方案规划（对应 `/plan-*` 三连审）
- **输入**: Phase 1 的需求定义
- **角色**: CEO Review → Eng Review → Design Review（三轮）
- **输出**: 技术方案 + 架构决策 + 测试计划
- **核心动作**:
  - `/plan-ceo-review`: 重新思考问题，找10星产品
  - `/plan-eng-review`: 锁架构、数据流、边界情况
  - `/plan-design-review`: 每维度0-10分打分

#### Phase 3: BUILD — 构建实现
- **输入**: Phase 2 的技术方案
- **角色**: 工程师（Staff Engineer级别）
- **输出**: 可运行的代码 + 单元测试
- **核心动作**:
  - 按方案逐步实现
  - 每个函数/模块写测试
  - 遵循项目既有代码风格

#### Phase 4: REVIEW — 生产级审查（对应 `/review`）
- **输入**: Phase 3 的代码
- **角色**: 资深工程师（非编写者本人）
- **输出**: Bug清单 + 修复后的代码
- **核心动作**（不做风格检查，专注生产级问题）:
  - 竞态条件检测
  - 资源泄漏检查
  - 边界情况覆盖
  - 错误处理完整性
  - 安全漏洞扫描
  - **简单问题自动修复，复杂问题标 [ASK] 等用户确认**

#### Phase 5: TEST — 端到端测试（对应 `/qa` + `/browse`）
- **输入**: Phase 4 的修复后代码
- **角色**: QA负责人 + 真实浏览器
- **输出**: 测试报告 + 回归测试套件
- **核心动作**:
  - 打开真实浏览器（Chromium）
  - 按测试计划走完主流程
  - 记录控制台错误和网络异常
  - 发现bug → 自动修复 → 写回归测试
  - 重新验证通过

#### Phase 6: SHIP — 发布上线（对应 `/ship` → `/land-and-deploy` → `/canary`）
- **输入**: Phase 5 通过的代码
- **角色**: 发布工程师 + SRE
- **输出**: 已上线且监控中的版本
- **核心动作**:
  - 同步 main，跑全量测试
  - 审计覆盖率（目标 >80%）
  - 推 PR，合并，等 CI
  - 部署，健康检查
  - canary 监控循环

#### Phase 7: REFLECT — 回顾反思（对应 `/retro`）
- **输入**: 全程数据和结果
- **角色**: 工程经理
- **输出**: 改进报告 + 下次Sprint优化点
- **核心动作**:
  - 统计各阶段耗时
  - 哪些地方卡住了？为什么？
  - 产出可复用的经验
  - 更新项目知识库

---

## 三、使用方式

### 方式一：全自动 Sprint（推荐）

用户说"用gstack模式做XXX"，自动跑完全部7个阶段。

**示例**:
- "用gstack模式给IPO项目加支付功能"
- "gstack sprint: 重构前端搜索页"
- "用团队模式修这个bug: XXX"

**流程**:
1. 自动识别任务类型和复杂度
2. 判断需要的阶段（简单bug可能跳过Think/Plan）
3. 按顺序执行每个阶段
4. 每个阶段完成后汇报进度
5. 全部完成后生成 Reflect 报告

### 方式二：单阶段调用

用户明确指定某个阶段：

| 命令 | 作用 | 示例 |
|------|------|------|
| `/think` 或 "office-hours" | 需求咨询 | "帮我 think 一下这个功能" |
| `/plan` | 方案规划（三连审）| "plan一下登录模块" |
| `/review` | 代码审查 | "review 这段代码" |
| `/test` | E2E测试 | "test 一下首页" |
| `/ship` | 部署上线 | "ship 这个PR" |
| `/reflect` | Sprint回顾 | "做个 retro" |

### 方式三：工具层单独调用

| 命令 | 作用 |
|------|------|
| `/freeze <path>` | 锁定编辑范围，只允许修改指定目录 |
| `/careful` | 开启危险操作警告模式 |
| `/guard` | freeze + careful 同时开启 |
| `/unfreeze` | 解除锁定 |
| `/xcheck` | 用另一个模型交叉验证当前方案 |
| `/browse <url>` | 打开真实浏览器验证页面 |

---

## 四、不可妥协的核心原则（来自 gstack 原版）

> ⚠️ 以下原则在任何项目中都不可违反：

1. **绝不编造数据** — 不知道就说不知道，不编造API返回值、不编造测试结果
2. **绝不使用过时信息** — 先确认当前状态再行动（进程是否在跑、文件是否存在）
3. **绝不跳过 Think Aloud** — 复杂操作前必须说明思路和假设
4. **绝不在没调查的情况下修复 bug** — 先根因分析（`/investigate`），再动手修
5. **绝不在重要决策上跳过用户确认** — 删数据、改生产配置、force-push 等

---

## 五、快速开始

### 第一次使用

```
用户: 用gstack模式帮我把IPO项目的入库脚本部署到ECS
```

系统自动执行：
1. **THINK**: 确认入库脚本的用途、依赖、风险点
2. **PLAN**: 制定部署步骤、回滚方案
3. **BUILD**: 准备部署命令和环境检查
4. **REVIEW**: 审查命令安全性（有没有rm -rf之类的危险操作）
5. **TEST**: 在ECS上试跑 dry-run 模式
6. **SHIP**: 正式部署并验证
7. **REFLECT**: 记录部署经验和耗时

---

## 六、角色 Prompt 文件索引

| 文件 | 对应角色/Sprint阶段 |
|------|-------------------|
| `roles/think.md` | Phase 1: 产品顾问 / Office Hours |
| `roles/plan-ceo.md` | Phase 2a: CEO/创始人 Review |
| `roles/plan-eng.md` | Phase 2b: 工程经理 Review |
| `roles/plan-design.md` | Phase 2c: 设计师 Review |
| `roles/build.md` | Phase 3: Staff Engineer 构建 |
| `roles/review.md` | Phase 4: 资深工程师 Review |
| `roles/test.md` | Phase 5: QA负责人 测试 |
| `roles/ship.md` | Phase 6: 发布工程师 + SRE |
| `roles/reflect.md` | Phase 7: 工程经理 回顾 |
| `tools/freeze.md` | 编辑锁定规则 |
| `tools/careful.md` | 危险操作警告 |
| `tools/xcheck.md` | 多模型交叉验证 |

---

## 七、与原始 gstack 的差异（适配说明）

| 原始 gstack (Claude Code) | 本适配版 (WorkBuddy) |
|--------------------------|---------------------|
| 基于 Claude Code Slash Command | 基于 WorkBuddy Skill + Task Agent |
| 固定用 Claude 模型 | 支持多模型切换（Kimi/Qwen/DeepSeek/GLM）|
| `/browse` 用内置 Chromium | 用 ClawBrowser skill 或 preview_url |
| `/codex` 用 OpenAI Codex | `/xcheck` 用已配置的其他国产模型 |
| 单机单用户 | 支持多Agent并行（Task team mode）|
| 无持久化记忆 | 结合 Working Memory 跨会话积累经验 |

---

*基于 [Garry Tan's gstack](https://github.com/garrytan/gstack) 开源项目适配*
