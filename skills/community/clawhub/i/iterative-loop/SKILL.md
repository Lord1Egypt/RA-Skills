# iterative-loop

迭代循环控制器 — 借鉴 Claude Code Ralph Wiggum 的 Stop Hook 自引用循环模式，通过状态文件 + 循环控制器实现可控的迭代执行。

## 概述

Ralph Wiggum 通过 Stop Hook 检测 `<promise>` 标签，如果承诺未完成则阻止停止并喂回 prompt。本 skill 用状态文件和循环控制器实现类似效果，支持最大迭代次数、完成条件检测、状态持久化和渐进式改进。

## 迭代模式

### fixed（固定次数）
执行指定次数后停止，不做完成条件判断。
```
loop-controller.py init --mode fixed --max 5
```

### max（最大次数 + 完成条件）
最多执行 N 次，满足完成条件时提前退出。
```
loop-controller.py init --mode max --max 10 --condition "regex:BUILD SUCCESS"
```

### adaptive（自适应）
根据每轮改进幅度动态决定是否继续。连续 N 轮无改进则停止。
```
loop-controller.py init --mode adaptive --max 20 --patience 3
```

## 工作流

### 1. 初始化循环

```bash
python scripts/loop-controller.py init \
  --name "refactor-module" \
  --mode max \
  --max 10 \
  --condition "regex:All tests passed"
```

输出状态文件 `loop-state.json`：
```json
{
  "name": "refactor-module",
  "mode": "max",
  "max_iterations": 10,
  "current_iteration": 0,
  "completion_check": {
    "type": "regex",
    "pattern": "All tests passed"
  },
  "history": [],
  "artifacts": [],
  "status": "running"
}
```

### 2. 执行迭代循环

每轮迭代的标准流程：

```
for iteration in range(max_iterations):
    1. 检查状态 → loop-controller.py check
    2. 执行任务 → 运行实际工作（编码/测试/修复等）
    3. 评估结果 → 检查完成条件
    4. 更新状态 → loop-controller.py update --result ...
    5. 如果完成 → loop-controller.py complete
```

### 3. 与 sessions_spawn 集成

长任务迭代应 spawn 子代理执行每轮：

```
主代理：初始化循环 → loop-controller.py init
  ↓
循环开始：
  → sessions_spawn（子代理执行一轮迭代）
  → 子代理完成后报告结果
  → loop-controller.py update --result <结果>
  → loop-controller.py check（是否继续）
  ↓
循环结束：loop-controller.py complete
```

### 4. 完成条件检测

支持三种检测方式：

**正则匹配**：检查输出是否匹配指定模式
```
--condition "regex:BUILD SUCCESS|All tests passed"
```

**文件检测**：检查文件是否存在或内容变化
```
--condition "file:output/result.txt"
--condition "file-changed:src/main.py"
```

**LLM 判断**：由 LLM 评估当前结果是否满足要求
```
--condition "llm:代码质量达到可发布标准"
```

## 状态文件格式

```json
{
  "name": "任务名称",
  "mode": "fixed|max|adaptive",
  "max_iterations": 10,
  "current_iteration": 3,
  "completion_check": {
    "type": "regex|file|file-changed|llm",
    "pattern": "检测模式"
  },
  "history": [
    {
      "iteration": 1,
      "timestamp": "2026-06-26T22:00:00",
      "result": "pass|fail|partial",
      "summary": "本轮做了什么",
      "metrics": {}
    }
  ],
  "artifacts": ["产出文件列表"],
  "status": "running|completed|failed|cancelled",
  "metadata": {}
}
```

## 命令参考

| 命令 | 说明 | 关键参数 |
|------|------|----------|
| `init` | 初始化循环 | `--name --mode --max --condition` |
| `check` | 检查是否应继续 | `--state <path>` |
| `update` | 更新迭代结果 | `--state <path> --result --summary` |
| `complete` | 标记循环完成 | `--state <path> --reason` |

## 使用示例

### 代码重构迭代

```bash
# 初始化
python scripts/loop-controller.py init --name "refactor" --mode max --max 5 --condition "regex:coverage.*90%"

# 每轮迭代
python scripts/loop-controller.py check --state loop-state.json
# → 执行重构...
python scripts/loop-controller.py update --state loop-state.json --result pass --summary "提取了3个函数"

# 完成
python scripts/loop-controller.py complete --state loop-state.json --reason "覆盖率达到92%"
```

### 测试修复迭代

```bash
python scripts/loop-controller.py init --name "fix-tests" --mode adaptive --max 15 --patience 3

# 每轮：运行测试 → 修复失败 → 记录结果
# 连续3轮无进展时自动停止
```

## 注意事项

- 状态文件默认保存在工作目录的 `loop-state.json`
- adaptive 模式的 patience 默认为 3（连续3轮无改进则停止）
- 每轮迭代应产生可观测的改进，避免空转
- 循环结束后状态文件保留完整历史，供复盘使用
