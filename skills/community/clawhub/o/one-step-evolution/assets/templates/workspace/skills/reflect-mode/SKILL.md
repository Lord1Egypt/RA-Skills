---
name: reflect-mode
description: 用于复盘近期 daily log、项目进展、成功与失败，把有效经验提升为长期记忆、工作流或新 skill。
---

# Reflect Mode

## 目标

让系统持续变强，而不是只持续工作。

## 读取范围

- 最近 1 到 3 天的 `memory/YYYY-MM-DD.md`
- 活跃项目的 `PROGRESS.md`
- 活跃项目的 `EXECUTION_PLAN.md`
- 相关 `memory/topics/*.md`

## 反思流程

1. 提取近期事实
2. 识别重复成功模式
3. 识别失败、卡点和无效指令
4. 判断哪些内容应进入：
   - `memory/topics/*.md`
   - `MEMORY.md`
   - `skills/*`
   - 项目文件
5. 清理不再有效的提示和结构

## 输出格式

```text
Reflect
近期有效模式：
近期失败模式：
建议沉淀：
建议删除：
下一轮优化重点：
```

## 规则

- 不写空洞总结
- 不把 daily log 原样搬进 `MEMORY.md`
- 只有稳定经验才进入长期层
- 真正无效的内容要删，不要只追加
