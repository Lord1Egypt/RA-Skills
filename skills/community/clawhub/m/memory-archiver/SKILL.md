---
name: memory-archiver
description: 记忆管理技能 - 三层时间架构 + 自动搜索/提取/会话笔记统一 Hook + 记忆巩固（整合 auto-dream）
version: 10.3.0
author: c32
---

# Memory Archiver Skill - 记忆归档技能

**版本**: 10.3.0 (安全修复：execFile 杜绝命令注入)  
**创建日期**: 2026-03-11  
**更新日期**: 2026-04-14  
**作者**: c32

---

## 📋 技能描述

**二维记忆架构**：时间分层 × 类型标签

- **时间分层**: daily (每天) → weekly (每周) → long-term (长期/MEMORY.md)
- **类型标签**: [episodic] 事件 / [semantic] 知识 / [procedural] 流程
- **存储**: 每日记忆 + 每周记忆 + 长期精选记忆
- **WAL 协议**: Write-Ahead Log，写前日志防数据丢失
- **统一 Hook** (message:received): 自动搜索 + 自动提取 + 会话笔记追踪（整合原 auto-memory-extract + session-notes）

---

## 🎯 功能清单

### 时间分层任务

| 任务 | 频率 | 说明 |
|------|------|------|
| **记忆及时写入** | 10 分钟 | 检查并写入重要信息到 daily 文件 |
| **记忆归档 - Daily 层** | 每天 23:00 | 提炼当天内容到 daily 文件 |
| **记忆总结 - Weekly 层** | 每周日 22:00 | 提炼 weekly 到 MEMORY.md 长期记忆 |

### 记忆巩固（原 auto-dream）

| 任务 | 频率 | 说明 |
|------|------|------|
| **记忆巩固** | 每 6 小时 | 闸门检查(24h/5新会话) → 老化清理 → 数量限制 → 索引更新 → 去重 |
| **老化清理** | 随巩固触发 | 标记并清理超过 30 天的记忆文件 |
| **数量限制** | 随巩固触发 | 每类型最多 50 条，超出清理最旧的 |
| **索引更新** | 随巩固触发 | 重建 MEMORY.md 底部记忆索引 |
| **去重** | 随巩固触发 | MEMORY.md 段落级去重（清理重复/无效内容） |

### 自动搜索 Hook（多维度增强）

| 功能 | 说明 |
|------|------|
| **消息类型检测** | 疑问/修复/规范/特征/配置/命令/技术 |
| **关键词提取** | 自动提取中英文关键词 |
| **维度 1: 关键词搜索** | 在 SESSION-STATE.md 缓存中搜索 |
| **维度 2: 类型标签搜索** | 按 [episodic]/[semantic]/[procedural] 标签搜索 |
| **维度 3: 时间维度搜索** | 今日→昨日→长期记忆，优先最近 |
| **维度 4: 组合搜索** | 多关键词 OR 关系，扩大匹配范围 |
| **上下文注入** | 合并所有维度结果注入 prompt |

### 自动记忆提取

| 功能 | 说明 |
|------|------|
| **记忆分类** | 基于关键词和模式自动分类为 user/feedback/project/reference |
| **自动去重** | MD5 hash + 模糊匹配，防止重复写入 |
| **索引更新** | 自动更新 MEMORY.md 底部记忆索引 |

### 会话笔记追踪

| 功能 | 说明 |
|------|------|
| **自动初始化** | 新会话自动创建笔记 |n| **消息计数** | 每 10 条消息更新一次笔记 |
| **会话归档** | 会话结束自动生成摘要并归档 |

---

## 📂 文件结构

```
skills/memory-archiver/
├── SKILL.md                          # 本文件
├── skill.json                        # 技能元数据
├── _meta.json                        # ClawHub 元数据
├── .clawhub/                         # ClawHub 同步目录
│   └── origin.json                   # 来源信息
├── scripts/
│   ├── install.js                    # 安装脚本（含 hook 自动注册）
│   ├── auto-memory-search.js         # 自动记忆搜索（被 hook 调用）
│   ├── memory-loader.js              # 加载记忆到缓存
│   ├── memory-search.js              # 搜索记忆
│   ├── memory-refresh.js             # 智能刷新缓存
│   ├── memory-dedup.js               # MEMORY.md 段落级去重
│   ├── memory-extract.js             # 从对话提取记忆
│   ├── memory-classify.js            # 关键词分类器
│   ├── memory-dedup-extract.js       # 提取去重（MD5 hash）
│   ├── memory-aging.js               # 记忆老化与数量限制检查
│   ├── dream-consolidate.js          # 记忆巩固主程序（闸门+索引+编排，原 auto-dream）
│   ├── dream-lock.js                 # 文件锁（防止并发巩固）
│   ├── session-tracker.js            # 会话笔记追踪
│   └── README.md                     # 脚本说明文档
├── hooks/                            # Hook 源文件（安装时复制到 workspace/hooks/）
│   ├── handler.js                    # Hook 处理器（事件：message:received）
│   ├── HOOK.md                       # Hook 元数据
│   └── bootstrap-loader/             # 启动加载 Hook
│       ├── handler.js                # Hook 处理器（事件：agent:bootstrap）
│       └── HOOK.md                   # Hook 元数据
└── prompts/                          # 提示词
    └── consolidation.md              # 记忆巩固提示词
```

### 安装后的工作区文件

```
~/.openclaw/workspace/
├── MEMORY.md                         # 长期精选记忆
├── hooks/
│   └── memory-archiver-hook/           # Hook（由 install.js 自动部署）
│       ├── handler.js
│       └── HOOK.md
└── memory/
    ├── daily/                        # 每日记忆
    ├── weekly/                       # 每周记忆
    ├── auto/                         # 自动分类记忆 (user/feedback/project/reference)
    ├── .dream-state.json             # 巩固状态（自动维护）
    └── .dream.lock                   # 巩固文件锁
```

---

## 🔧 安装

### 方法 1: 通过 ClawHub 安装（推荐 ⭐）

```bash
clawhub install memory-archiver
```

安装后**自动执行**：
1. 创建 `memory/daily/` 和 `memory/weekly/` 目录
2. 部署 hook 到 `workspace/hooks/memory-archiver-hook/`
3. 执行 `openclaw hooks install --link` 注册 hook
4. 自动添加 3 个 cron 任务
5. 提示重启 gateway

### 方法 2: 本地技能目录（开发调试）

如果技能已在 `~/.openclaw/workspace/skills/memory-archiver/`：

```
node ~/.openclaw/workspace/skills/memory-archiver/scripts/install.js
```

### 验证安装

```
openclaw hooks list
# 应看到 memory-archiver-hook (✓ ready)

openclaw cron list
# 应看到 3 个记忆相关任务
```

---

## 📝 记忆写入规范

### 三类记忆标签

| 标签 | 说明 | 例子 |
|------|------|------|
| `[episodic]` | 事件/经历 | "用户今天完成了模板重设计" |
| `[semantic]` | 知识/事实 | "用户喜欢 Tailwind CSS" |
| `[procedural]` | 流程/方法 | "部署步骤：1. 构建 2. 上传 3. 重启" |

### 记录原则

**✅ 应该记录**:
- 关键决策和教训
- 新发现的有价值内容
- 技术栈使用经验
- 工作习惯调整
- 用户偏好

**❌ 不应该记录**:
- ❌ **重复的上下文** — 已有记录的内容不再重复
- ❌ **毫无意义的日常** — 无事发生就不记
- ❌ **重复的任务进度提示** — 避免刷屏
- ❌ **私密细节** — 保护隐私
- ❌ **短期易变想法** — 临时念头不持久

**核心判断**: 这条信息在未来回顾时是否有价值？

---

## 🔍 记忆搜索

### 自动加载（OpenClaw 启动时）

每次 OpenClaw 启动时，通过 `agent:bootstrap` Hook 自动加载记忆到缓存，无需手动触发。

加载内容：今日 + 昨日 + 最近 3 天 daily + MEMORY.md + 最近 weekly

### 交互式搜索

```
node ~/.openclaw/workspace/skills/memory-archiver/scripts/memory-search.js "搜索内容"
```

**在对话中使用**：
- 直接提问，Hook 会自动检测并搜索相关记忆

### 使用 grep 搜索

```bash
# 搜索所有记忆文件
grep -ri "CSS" ~/.openclaw/workspace/memory/

# 带上下文显示
grep -riC 3 "CSS" ~/.openclaw/workspace/memory/daily/*.md
```

---

## 📊 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| **10.1** | 2026-04-14 | **全部 .sh 转为 .js**: install/memory-search/memory-loader/memory-refresh/memory-dedup/dream-lock 全部纯 JS |
| **10.0** | 2026-04-14 | **整合 auto-memory-extract + session-notes**: 统一 Hook (message:received) 包含搜索/提取/会话笔记三模块 |
| **9.0** | 2026-04-14 | **完全整合 auto-dream**: dream-consolidate.js(闸门+索引+编排)、dream-lock.js(文件锁)、prompts/consolidation.md 全部迁入，auto-dream 技能移除 |
| **8.0** | 2026-04-13 | **整合 auto-dream 去重功能**: memory-dedup.js 现在负责 MEMORY.md 段落去重，auto-dream 仅负责触发 |
| **7.0** | 2026-03-23 | **Hook 安装自动化**: `skill.json` 添加 `postinstall` 脚本，`clawhub install` 自动部署 hook + cron |
| 6.0 | 2026-03-20 | 整合 Auto Memory Search Hook: 将独立 Hook 合并到技能内 |
| 5.0 | 2026-03-20 | **三层精简架构**: 移除 monthly/yearly 层，保留 daily/weekly/long-term |
| 4.0 | 2026-03-20 | **精简版**: 移除向量搜索依赖，简化架构 |
| 3.0 | 2026-03-19 | 向量增强版：整合 Qdrant + Transformers.js |
| 2.0 | 2026-03-19 | 五层时间架构 (hourly/daily/weekly/monthly/yearly) |
| 1.0 | 2026-03-11 | 初始版本 |

---

## 🛠️ 维护命令

```bash
# 检查记忆文件总量
du -sh ~/.openclaw/workspace/memory/

# 查看每日记忆文件
ls -lh ~/.openclaw/workspace/memory/daily/

# 搜索记忆内容
grep -ri "CSS" ~/.openclaw/workspace/memory/
```

---

*文档最后更新：2026-04-14*
