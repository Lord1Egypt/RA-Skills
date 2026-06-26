# Pattern 8: Compaction 前记忆提取（Save Before Delete）

## 问题

Claude Code 的 auto-compact 在 context 接近上限时自动触发。压缩会丢弃旧消息，其中可能包含重要的设计决策和发现。

## 原理

利用 Claude Code 的 PreCompact hook，在压缩发生前提取关键信息到磁盘。来自 Claude Code 内部的 `buildExtractAutoOnlyPrompt` 和 `buildExtractCombinedPrompt`——Claude Code 在压缩时并行提取 memory。

## 与 Handoff 文档的区别

| | Handoff 文档 (Pattern 2) | Compaction 提取 (Pattern 8) |
|---|---|---|
| 触发时机 | 阶段结束时（主动） | 压缩触发时（被动） |
| 触发者 | Agent 自行写入 | PreCompact hook 自动注入 |
| 内容控制 | 完全由 agent 决定 | 由 hook prompt 引导 |
| 可靠性 | 依赖 agent 遵守指令 | 系统级保证 |

两者互补：handoff 是计划内的上下文传递，compaction 提取是应急的知识抢救。

## 实现

settings.json 中配置 PreCompact hook：

```json
{
  "hooks": {
    "PreCompact": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "Context 即将被压缩。在压缩前，将以下信息写入 handoff 文档：1) 当前任务的完成状态 2) 已做的关键决策及原因 3) 已排除的方案 4) 已知风险 5) 下一步计划。写入路径：sessions/<session-id>/handoffs/pre-compact.md"
      }]
    }]
  }
}
```

## Claude Code 的 Memory Extraction 机制

Claude Code 内部有两种 extraction prompt builder：

- `buildExtractAutoOnlyPrompt`：只提取 private memory（用户偏好、工作习惯）
- `buildExtractCombinedPrompt`：根据内容敏感性路由到 private 或 team scope

提取发生在压缩的同时（并行），提取结果写入 memdir 的 Markdown 文件。Memory taxonomy 包含 4 种类型：user（个人偏好）、feedback（纠正/表扬）、project（架构/目标）、reference（外部文档/流程）。
