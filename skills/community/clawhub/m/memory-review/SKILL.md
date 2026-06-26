---
name: memory-review
version: 1.1.0
description: 知识沉淀自动化技能。扫描近期日记，识别可沉淀知识，自动写入知识库。触发时机：cron 定时任务或手动调用。使用方法：加载 skill 后读取 references/spec.md 获取详细规范。
---

# Memory Review

扫描近期日记，生成知识沉淀提案，并自动执行沉淀。

## 核心流程

1. 读取 references/spec.md 获取详细规范
2. 读取 AGENTS.md/MEMORY.md 获取投递配置
3. 增量扫描近期日记（md5 比对）
4. 识别 5 类可沉淀知识
5. 自动写入知识库
6. 生成报告并投递

## 敏感信息

**投递配置（如飞书群ID）存储在 AGENTS.md 或 MEMORY.md 中**，skill 里使用占位符。

读取方式：
- 读取 `MEMORY.md`（如果存在）
- 读取 `AGENTS.md` 中的配置

## 输出

- 报告位置：`memory/daily/YYYY-MM-DD-memory-review.md`
- 知识库：`memory/knowledge/fw-*.md`
- 执行日志：`data/exec-logs/memory-review/YYYY-MM-DD.md`

## 触发时机

- cron 定时任务（建议每 2 天）
- 用户明确要求时
- 每次会话结束前（可选）

## 自动沉淀规则

| 优先级 | 条件 | 行为 |
|--------|------|------|
| 高 | 错误/教训类 | 自动写入 post-mortems.md |
| 中 | 技术知识类 | 自动写入 knowledge/fw-*.md |
| 低 | 配置/偏好类 | 写入 TOOLS.md 或 AGENTS.md |

## 沉淀文件命名规范

```
fw-{主题}.md
- fw = "from work" 工作产出
- 主题：用英文或中文拼音
```
