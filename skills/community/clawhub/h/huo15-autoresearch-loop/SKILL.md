---
name: huo15-autoresearch-loop
version: 1.0.2
aliases:
  - 火一五自动迭代
  - 火一五自动循环
  - 自动迭代循环
description: 基于 Karpathy 自主研究循环的 OpenClaw Skill，Modify → Verify → Keep/Discard → Repeat forever
---

# huo15-autoresearch-loop

> 基于 [uditgoenka/autoresearch](https://github.com/uditgoenka/autoresearch)（Karpathy 自主研究循环）的 OpenClaw Skill 实现。

## 触发词

- 自动迭代
- autoresearch
- 跑起来别停
- 自动循环

## 功能

实现 Karpathy 的 **Modify → Verify → Keep/Discard → Repeat forever** 自主研究循环。

## 核心流程

1. 用户说「自动迭代 [目标] [验证命令]」
2. 初始化状态（目标/验证命令/迭代次数/范围）
3. 循环：
   - 修改代码/文件
   - 调用验证命令
   - 成功 → git commit + 记录
   - 失败 → git revert
   - 判断是否继续（迭代次数/收敛检测）
4. 输出摘要

## 使用方式

```
自动迭代 [目标描述] [验证命令]
```

示例：
```
自动迭代 优化性能瓶颈 make test
自动迭代 修复所有lint错误 ./scripts/lint.sh
```

## 配置说明

`config.json` 控制循环行为：

```json
{
  "max_iterations": 50,
  "verify_command": "",
  "scope_globs": ["**/*.py", "**/*.js"],
  "convergence_threshold": 3,
  "commit_each_success": true,
  "revert_on_fail": true
}
```

## 非侵入设计

- 只通过 `exec` 调用脚本
- 不修改 OpenClaw 内核
- 状态持久化在本地文件

## 状态文件

每次迭代的状态保存在 `~/.openclaw/tmp/autoresearch-loop-state.json`：

```json
{
  "goal": "优化性能",
  "verify_command": "make test",
  "iteration": 5,
  "successes": 3,
  "failures": 2,
  "last_success": "2026-04-22T00:30:00Z",
  "history": [...]
}
```

## 停止条件

- 达到 `max_iterations`
- 连续失败超过 `convergence_threshold`
- 用户发送「停止迭代」
- 收敛检测（连续 N 次成功）

## version

1.0.0
