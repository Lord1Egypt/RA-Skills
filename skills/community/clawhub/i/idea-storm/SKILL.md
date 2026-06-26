---
name: idea-storm
version: 1.0.0
description: 工程问题的自动化迭代实验室。给定一个 idea 或工程问题，自动调研方案、设计实现、验证效果、迭代优化，结果存入 Notion。触发词："idea-storm"、"实验一下"、"帮我验证"、"迭代优化"、"idea 验证"。当用户提出一个工程问题并希望自动化地调研→设计→验证→迭代时使用此 skill。
---

# Idea Storm

工程问题的自动化 设计→验证→迭代 闭环。后台运行，不阻塞主会话。

## 运行架构

采用分段 spawn 模式：每个检查点之间的工作在独立子 agent 中运行，状态通过文件传递。

```
主会话                              子 agent (isolated)
  │                                    │
  ├─ 创建 experiment.yaml              │
  ├─ spawn("idea-storm: 调研+设计") ───→ │
  │   (继续聊天)                       ├─ Phase 2: 调研
  │                                    ├─ Phase 3: 方案设计
  │                                    ├─ 更新 experiment.yaml
  │  ◄── announce 方案摘要 ────────────┤  ✅ 检查点1
  │                                    └─ (退出)
  │
  ├─ 用户确认方案
  ├─ spawn("idea-storm: 实现+验证") ───→ │
  │   (继续聊天)                       ├─ 读 experiment.yaml 恢复状态
  │                                    ├─ Phase 4: 实现
  │                                    ├─ Phase 5: 验证
  │                                    ├─ Phase 6: 评估
  │                                    ├─ 更新 experiment.yaml
  │  ◄── announce 迭代结果 ────────────┤  ✅ 检查点2
  │                                    └─ (退出)
  │
  ├─ 用户确认（继续迭代/收敛）
  ├─ spawn("idea-storm: 迭代N") ───→    ...（重复直到收敛）
  │
  ├─ spawn("idea-storm: 收敛报告") ──→  │
  │  ◄── announce 最终报告 ────────────┤  ✅ 检查点3
  └─ 完成
```

### spawn 任务模板

每次 spawn 时，task 中必须包含：
1. 实验状态文件路径：`experiments/<id>/experiment.yaml`
2. 当前要执行的阶段
3. 用户的确认/反馈内容（如有）

示例：
```
sessions_spawn(task="执行 idea-storm 实验。
读取实验状态：experiments/facial-gan-20260213/experiment.yaml
执行阶段：Phase 4-6（实现→验证→评估）
用户反馈：方案OK，用 StyleGAN3 路线
按 idea-storm skill 流程执行，完成后更新 experiment.yaml 并汇报结果。")
```

子 agent 启动后：
1. 读 idea-storm SKILL.md 获取流程指引
2. 读 experiment.yaml 恢复实验状态
3. 执行指定阶段
4. 更新 experiment.yaml + Notion
5. announce 结果摘要

---

## 记忆管理

三层存储，确保状态不丢失：

### 层级 1：热状态 (SESSION-STATE.md)

主会话的 SESSION-STATE.md 记录当前活跃实验的概要：

```yaml
idea_lab:
  active_experiment: "facial-gan-20260213"
  experiment_path: "experiments/facial-gan-20260213/"
  current_phase: "等待用户确认检查点2"
  last_spawn_label: "idea-storm-facial-gan-iter2"
```

### 层级 2：实验工作区

每个实验在 workspace 下有独立目录：

```
experiments/<experiment-id>/
├── experiment.yaml          # 实验完整状态（核心）
├── research/                # 调研资料
│   └── findings.md
├── design/                  # 方案设计
│   └── plan.md
├── src/                     # 实现代码
├── data/                    # 输入数据、参考图等
├── results/                 # 每轮验证结果
│   ├── iter-1/
│   ├── iter-2/
│   └── ...
└── report.md                # 最终报告（本地副本）
```

### 层级 3：Notion 长期记录

结构化实验报告，按时间和分类组织。详见 [Notion 页面结构](#notion-实验页面结构)。

### experiment.yaml 规范

实验的完整状态文件，子 agent 靠它恢复上下文：

```yaml
id: "facial-gan-20260213"
title: "用 GAN 生成面部微表情"
created: "2026-02-13T12:00:00+08:00"
status: "running"  # running | paused | completed | abandoned

# 当前进度
phase: "Phase 5: 验证"
iteration: 2
max_iterations: 5

# 问题定义
problem:
  description: "需要生成逼真的面部微表情动画"
  constraints: "实时渲染，延迟<50ms"

# 验证配置
validation:
  mode: "B"  # A=图片对比 B=指标优化 C=功能验证 D=自定义
  description: "优化 FID score"
  threshold: 50
  current_best: 67.3

# 检查点记录
checkpoints:
  - phase: 3
    time: "2026-02-13T13:00:00+08:00"
    status: "approved"
    user_feedback: "方案确认，用 StyleGAN3"
  - phase: 6
    iteration: 1
    time: "2026-02-13T14:30:00+08:00"
    status: "continue"
    user_feedback: "FID 67.3，继续优化学习率"

# 迭代历史
iterations:
  - round: 1
    changes: "初始实现，lr=0.001"
    result: "FID 67.3"
    decision: "继续，调整学习率"
  - round: 2
    changes: "lr=0.0003, 增加数据增强"
    result: "pending"

# Notion
notion_page_id: "xxx-xxx-xxx"
```

---

## 核心流程

### Phase 1: 问题定义（主会话执行）

用户输入工程问题或 idea。提取并确认：

1. **问题描述**：要解决什么
2. **成功标准**：怎样算解决了
3. **约束条件**：技术栈、资源限制
4. **验证方式**：见 [验证模式](#验证模式)

如果用户没有明确给出以上信息，主动询问（不要一次问太多）。

确认后：
1. 创建实验目录 `experiments/<id>/`
2. 写入 `experiment.yaml`
3. 创建 Notion 实验页面
4. 更新 SESSION-STATE.md
5. spawn 子 agent 执行 Phase 2-3

### Phase 2: 调研（子 agent）

偏向工程化搜索，优先级：

1. GitHub 开源项目和实现
2. 技术博客、Stack Overflow、工程实践
3. 产品文档、API 文档
4. 论文（仅在工程资料不足时补充）

工具：`web_search` + `web_fetch`

输出：
- `research/findings.md`：调研结果
- 更新 experiment.yaml
- 更新 Notion「调研记录」

### Phase 3: 方案设计（子 agent）

基于调研设计技术方案：
- 整体架构
- 关键技术选型
- 实现步骤
- 预期效果

输出：
- `design/plan.md`：方案详情
- 更新 experiment.yaml（phase → "等待检查点1"）
- 更新 Notion「方案设计」
- announce 方案摘要给主会话

### ✅ 检查点 1：方案确认（主会话）

用户确认后，主会话 spawn 新子 agent 执行 Phase 4-6。

### Phase 4: 实现（子 agent）

按方案执行。可能包括：编写代码、配置环境、生成资源、调用 API。

输出：
- `src/` 下的实现代码
- 更新 Notion「实验日志」

### Phase 5: 验证（子 agent）

按 experiment.yaml 中定义的验证方式执行。详见 [验证模式](#验证模式)。

输出：
- `results/iter-N/`：本轮验证数据
- 更新 Notion「验证结果」

### Phase 6: 评估与迭代决策（子 agent）

根据验证结果判断：

| 情况 | 动作 |
|------|------|
| 达标 | 标记收敛，announce 结果 |
| 接近达标，参数可调 | 自动迭代参数，回到 Phase 4（不超过 max_iterations） |
| 方向有问题 | announce 建议换方案 |

更新 experiment.yaml 后 announce 结果给主会话。

### ✅ 检查点 2：迭代确认（主会话）

汇报内容：
- 本轮做了什么
- 效果数据/截图
- 下一步建议

用户确认后 spawn 下一轮或进入收敛。

### Phase 7: 收敛报告（子 agent）

生成最终报告：
- `report.md`：本地完整报告
- 更新 Notion 最终报告区块
- announce 报告摘要

### ✅ 检查点 3：最终确认（主会话）

---

## 验证模式

由用户在 Phase 1 定义。

### 模式 A：图片对比

用户提供参考图 + 输入集。Agent 生成输出，与参考图对比。

- 工具：`scripts/compare_images.py`（SSIM / 像素差异）或 `image` 工具（视觉分析）
- 达标标准由用户定义

### 模式 B：指标优化

用户定义评测函数或指标，Agent 优化实现以提升指标。

- 用户提供评测脚本或指标定义
- 每轮记录指标变化
- 达到阈值即收敛

### 模式 C：功能验证

用户定义测试用例或验收标准，Agent 逐项验证。

### 模式 D：自定义

用户描述验证方式，Agent 按描述执行。

---

## Notion 实验页面结构

每次启动实验时创建新页面。配置见 `references/notion-setup.md`。

```
📋 [实验标题] - [日期]
├── 问题定义
├── 调研记录
├── 方案设计
├── 实验日志（按迭代轮次）
├── 验证结果（按迭代轮次）
└── 最终报告
```

---

## 工具使用

| 阶段 | 工具 |
|------|------|
| 调研 | `web_search`, `web_fetch` |
| 实现 | Claude Code（首选）, `exec`, `write`, `edit` |
| 图片验证 | `image`, `scripts/compare_images.py` |
| 指标验证 | `exec`（运行评测脚本） |
| Notion | Notion API via `exec` |
| 后台运行 | `sessions_spawn` |
| 状态传递 | `experiment.yaml` 文件 |
| 通知用户 | announce（子 agent 自动） |

---

## Claude Code 集成

Phase 4（实现）阶段，优先使用 Claude Code 在 Docker 沙盒中完成编码任务。

### Docker 沙盒架构

每个实验在独立的 Docker 容器中运行 Claude Code，与宿主机隔离：

```
宿主机                              Docker 容器 (idea-storm-sandbox)
├── openclaw.json ──(env注入)────→  ANTHROPIC_AUTH_TOKEN / BASE_URL
├── experiments/<id>/ ──(volume)──→ /workspace
│                                   ├── 非 root 用户 (coder)
│                                   ├── Claude Code CLI + --dangerously-skip-permissions
│                                   ├── Python3 / Node.js / Git
│                                   └── 代码写在 /workspace，自动持久化
```

优势：
- 完全隔离，不污染宿主机环境
- 非 root 用户可用 `--dangerously-skip-permissions` 自动跳过权限
- API 配置从 `openclaw.json` 动态注入，换中转改一处即可
- 容器用完即删，干净无残留

### 镜像构建

使用预构建的 `idea-storm-sandbox` 镜像。Dockerfile 位于 `scripts/Dockerfile`：

```dockerfile
FROM node:22-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN npm install -g @anthropic-ai/claude-code
RUN useradd -m -s /bin/bash coder
RUN mkdir -p /home/coder/.openclaw /workspace && chown -R coder:coder /workspace /home/coder
USER coder
WORKDIR /workspace
CMD ["bash"]
```

构建：`docker build -t idea-storm-sandbox -f scripts/Dockerfile .`

### 调用方式

从 `openclaw.json` 动态提取 API 配置，注入容器环境变量：

```bash
# 提取 API 配置
API_KEY=$(python3 -c "import json; print(json.load(open('/root/.openclaw/openclaw.json'))['models']['providers']['cc']['apiKey'])")
BASE_URL=$(python3 -c "import json; print(json.load(open('/root/.openclaw/openclaw.json'))['models']['providers']['cc']['baseUrl'])")

# 运行 Claude Code（单次任务）
docker run --rm -t \
  -e ANTHROPIC_AUTH_TOKEN="$API_KEY" \
  -e ANTHROPIC_BASE_URL="$BASE_URL" \
  -v experiments/<id>:/workspace \
  idea-storm-sandbox \
  bash -c 'cd /workspace && git init -q 2>/dev/null; claude --print --dangerously-skip-permissions "<prompt>"'
```

### 在子 agent 中使用

子 agent 执行 Phase 4 时，通过 `exec` + `pty:true` 调用：

```
exec(
  command="API_KEY=$(python3 -c \"import json; print(json.load(open('/root/.openclaw/openclaw.json'))['models']['providers']['cc']['apiKey'])\") && BASE_URL=$(python3 -c \"import json; print(json.load(open('/root/.openclaw/openclaw.json'))['models']['providers']['cc']['baseUrl'])\") && docker run --rm -t -e ANTHROPIC_AUTH_TOKEN=$API_KEY -e ANTHROPIC_BASE_URL=$BASE_URL -v /root/.openclaw/workspace/experiments/<id>:/workspace idea-storm-sandbox bash -c 'cd /workspace && git init -q 2>/dev/null; claude --print --dangerously-skip-permissions \"<prompt>\"'",
  pty=true,
  timeout=300
)
```

也可以使用辅助脚本 `scripts/run-sandbox.sh` 简化调用（见下方）。

### Prompt 构造原则

给 Claude Code 的 prompt 应包含：
1. **目标**：要实现什么功能
2. **上下文**：当前项目结构、技术栈、已有代码
3. **约束**：文件路径、命名规范、依赖限制
4. **验证**：实现后如何验证（测试命令等）

示例：
```
基于 design/plan.md 中的方案，在当前目录实现面部微表情生成模块。
技术栈：Python 3.11 + PyTorch + StyleGAN3
要求：
1. 实现 FacialExpressionGenerator 类
2. 支持 6 种基本表情
3. 推理延迟 < 50ms
4. 写好单元测试
完成后运行 pytest 确认测试通过。
```

### 迭代模式（Ralph Loop）

多轮迭代优化时，循环调用容器中的 Claude Code：

1. 将任务写入实验目录的 `PROMPT.md`
2. 循环调用 Docker 容器，每轮读取 PROMPT.md
3. 通过文件（experiment.yaml）传递迭代状态
4. 检查完成标记决定是否继续

```bash
# 单轮实现（在容器中）
scripts/run-sandbox.sh <experiment-id> "$(cat experiments/<id>/PROMPT.md)"

# 宿主机验证结果
cd experiments/<id> && python3 -m pytest

# 如果失败，更新 PROMPT.md 加入错误信息，再跑一轮
```

### 何时用 Docker 沙盒 vs 宿主机直接执行

| 场景 | 推荐 |
|------|------|
| 创建项目脚手架、多文件编辑 | Docker 沙盒 (Claude Code) |
| 复杂代码重构 | Docker 沙盒 (Claude Code) |
| 安装未知依赖、运行不信任代码 | Docker 沙盒 |
| 简单文件写入、小修改 | 宿主机 OpenClaw `write`/`edit` |
| 运行已验证的命令 | 宿主机 OpenClaw `exec` |
| 需要读取实验状态做决策 | 宿主机 OpenClaw（子 agent 自身） |
