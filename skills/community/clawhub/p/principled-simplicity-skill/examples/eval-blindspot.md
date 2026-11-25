# Example: Eval Blindspot

## 输入

> 我改了 prompt，感觉现在回答稳多了。

## 失败模式

Eval Blindspot

## 如果没有 Guardrail

团队会把“感觉变好”当成修复完成：

- 没有保存原始 badcase
- 没有回放旧样本
- 没有负例
- 没有边界样本
- 没有记录这次修改想改善什么指标

这会让系统进入不可审计状态。每次 prompt 改动都像重新掷骰子。

## 更好的下一步

建立最小 eval：

- 5 个应该通过的正例
- 5 个之前失败的回归例
- 5 个应该拒绝或降级处理的负例
- 2 个边界例

每次修改必须说明：

```text
Expected improvement:
Expected non-regression:
Known trade-off:
Replay command or manual checklist:
```

没有 eval 的修复，只能叫实验，不能叫完成。
