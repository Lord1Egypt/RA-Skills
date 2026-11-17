# 与 self-improving-agent 的兼容说明

## 两者关系

persona-switcher 和 self-improving-agent 共享 `.learnings/` 目录作为学习数据仓库。

## 分工

| 维度 | persona-switcher | self-improving-agent |
|------|-----------------|---------------------|
| 何时触发 | 每次对话后（即时记录） | 定期复盘（深度分析） |
| 记录范围 | 当前会话的改进点 | 跨会话的模式识别 |
| 数据粒度 | 单条学习/错误 | 批量分析、优先级排序 |
| 推广动作 | 直接推广到人格文件 | 推广到 AGENTS.md/SOUL.md |
| Persona 标签 | 写入时标注 | 读取时按标签过滤 |

## 日志格式示例

```markdown
## [LRN-20260702-001] 用户偏好短回答

**Logged**: 2026-07-02T17:00:00+08:00
**Priority**: medium
**Status**: pending
**Area**: behavior

### Summary
用户每次回答超过 5 段就不看了

### Details
三次对话中用户都只读了前两段就回复了

### Suggested Action
控制在 3 段以内，必要信息用 bullet point

### Metadata
- Source: conversation
- Persona: shared    ← 通用改进，所有模式都适用
- Tags: response_length, conciseness

---
```

## 注意事项

1. **不要重复写**：两个 skill 共享同一个 `.learnings/` 目录，不需要各自维护一套
2. **标签即隔离**：通过 `Persona: xxx` 标签区分归属
3. **推广到通用文件的必须标 `Persona: shared`**
4. **self-improving-agent 的 hooks 不需要改动**，它只读写文件，不关心文件来源
