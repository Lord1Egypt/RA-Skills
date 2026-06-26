---
name: memory-association
description: 记忆联想系统。基于 MEMORY_INDEX.md 实现任务前的上下文联想召回，确保消耗 token 前先关联已有记忆。触发场景：(1) 启动任何新任务前 (2) 分析需求时 (3) 解决问题时 (4) 被问"之前做过什么"时 (5) Session Startup 第7步。避免重复工作，保持上下文连续性。
---

# Memory Association

## 核心原则

**先联想，再行动；先召回，再消耗 token。**

每次接到任务，立即联想：这件事之前做过吗？相关文件在哪？有什么经验教训？

## 联想工作流

### Step 1 — 读取索引

读取 `memory/MEMORY_INDEX.md`，按任务类型匹配联想链：

```
任务类型 → 优先召回文件（见索引§联想链）
```

### Step 2 — 精准召回

用 `memory_get` 拉取关键段落：

```bash
# 格式
memory_get(path="memory/xxx.md", from=行号, lines=20)
```

### Step 3 — 判断

| 判断结果 | 行动 |
|---------|------|
| 有相关记忆 | 引用关键段落，继续任务 |
| 记忆过期/缺失 | 补充写入 `memory/YYYY-MM-DD.md` |
| 发现通用教训 | 更新 `.learnings/LEARNINGS.md` |

### Step 4 — 记录

任务完成后，将关键结论写入当日 memory 文件：

```markdown
---
name: "任务摘要"
description: "一句话描述"
type: project
---

# 任务结果

[关键决策/结论/教训]
```

## 索引结构

完整索引见 `references/MEMORY_INDEX.md`，包含：

- 按项目分类（壹启健康/彩色乐园/入境医疗/科普竞赛）
- 按主题分类（TikTok/医学脚本/OpenClaw配置）
- 按时间分类（早期/密集期/稳定迭代/收尾）
- 关键词索引（踩坑/部署/UI改版等）
- 联想链（任务类型 → 优先召回文件）

## 索引更新时机

当有以下情况时，更新 MEMORY_INDEX.md：

1. 新项目启动 → 添加项目分类条目
2. 新主题出现 → 添加关键词索引
3. 重要教训 → 更新联想链
4. 重大踩坑 → 更新 `.learnings/ERRORS.md`

## 记忆分层

| 层级 | 位置 | 更新频率 | 用途 |
|------|------|---------|------|
| HOT | `MEMORY.md` | 按需 | 核心/长期记忆，200行硬限制 |
| WARM | `memory/YYYY-MM-DD.md` | 每日 | 当日工作日志 |
| COLD | `memory/projects/*.md` | 项目结束时 | 项目档案 |
| ARCHIVE | `memory/.dreams/` | 梦境处理 | 历史会话冷存 |

## 联想示例

**用户**：帮我查一下腾讯云部署的情况

1. 联想链匹配 → "壹启健康开发/部署" → `yiqi-health-project.md`
2. `memory_get` 拉取腾讯云段落
3. 结论：IP 62.234.146.100，版本 4.8.5，在 `2026-04-29.md` 有详细日志

**用户**：彩色乐园音频有问题

1. 联想链匹配 → "彩色乐园迭代" → `colorful-park-project.md`
2. `memory_get` 拉取音频相关段落
3. 结论：音频处理在 `2026-04-20-bgm-cleanup-fix.md`，使用 Mac say + ffmpeg 后处理

## 参考文件

- `references/MEMORY_INDEX.md` — 完整记忆索引
- `references/TASK_ASSOCIATION_EXAMPLES.md` — 联想示例库
