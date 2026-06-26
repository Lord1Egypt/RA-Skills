---
name: memory-system
description: 完整记忆系统 - 四类记忆分类 + AutoDream自动整合 + MiniMax LLM驱动 + Feedback双向记录
---

# Memory System 🧠

> 完整记忆系统 - 四类记忆分类 + AutoDream 自动整合 + MiniMax LLM 驱动 + Feedback 双向记录

**版本**: 2.0.0 | **作者**: 团宝 (openclaw)

---

## 核心特性

| 特性 | 说明 |
|------|------|
| 📁 **文件系统存储** | 纯 Markdown，无数据库，可直接编辑 |
| 🔍 **语义搜索** | Ollama 向量搜索 + 关键词降级 |
| ⚡ **自动加载** | 会话启动时自动读取相关记忆 |
| 📝 **四类记忆** | User / Feedback / Project / Reference |
| 🔄 **Feedback 双向** | 纠正 (negative) + 确认 (positive) |
| 🌙 **AutoDream** | 定时自动整合，MiniMax LLM 驱动 |
| 💾 **智能 Flush** | 上下文接近阈值时自动保存 |

---

## AutoDream：自动记忆整合

### 工作原理

```
定时触发 (每天 22:00) 或 手动触发
           ↓
扫描所有记忆文件 + 会话历史
           ↓
调用 MiniMax LLM 分析
           ↓
自动执行整合：
  - 新增遗漏的记忆
  - 删除过时的记忆
  - 更新 MEMORY.md 索引
           ↓
通知用户整合结果
```

### 触发条件

| 条件 | 默认值 | 说明 |
|------|--------|------|
| 时间间隔 | ≥ 24 小时 | 距离上次整合的时间 |
| 新会话数 | ≥ 3 个 | 新增的会话数 |

### 整合能力

- ✅ 扫描现有记忆文件
- ✅ 识别过时信息
- ✅ 合并重复记忆
- ✅ 更新 MEMORY.md 索引
- ✅ 使用绝对日期
- ✅ 四类记忆分类

---

## 四类记忆分类

### 1. User（用户）记忆
**作用域**: 私密  
**用途**: 了解用户角色、偏好、知识背景

```markdown
## user/李明.md
- 民盟上海市委宣传部副部长
- 技术背景：AI、编程
- 偏好：简洁回复，中文为主
```

### 2. Feedback（反馈）记忆 ⭐
**作用域**: 私密 / 团队  
**用途**: 记录用户的纠正和确认

```markdown
## feedback/开发规范.md
### 集成测试必须用真实数据库
**Type:** negative
**Why:** 上季度mock测试通过但生产迁移失败
**How to apply:** 禁止在集成测试中 mock 数据库层
**Date:** 2026-03-15

### 单PR优于多个小PR
**Type:** positive
**Why:** 拆分反而造成不必要的开销
**How to apply:** 重构类需求优先合并为大PR
**Date:** 2026-03-20
```

### 3. Project（项目）记忆
**作用域**: 团队  
**用途**: 项目进展、目标、决策

```markdown
## project/民盟宣传系统.md
- 阶段：二期开发
- 目标：6月底前完成
- 当前：AI播客监控系统
```

### 4. Reference（引用）记忆
**作用域**: 团队  
**用途**: 外部系统入口

```markdown
## reference/工具入口.md
- Bug追踪：Linear 项目 "MINMENG"
- 文档：Confluence /minmeng-space
```

---

## 安装

```bash
clawhub install memory-system
```

---

## 工具列表

### memory_search
语义搜索记忆

```json
{
  "query": "用户对代码规范的偏好",
  "type": "feedback",
  "topK": 5
}
```

### memory_write
写入记忆（写入后自动检查是否触发 AutoDream）

```json
{
  "file": "feedback/dev-rules.md",
  "content": "### 集成测试...\n**Type:** negative...",
  "type": "feedback",
  "mode": "append"
}
```

### memory_flush
手动触发持久化

```json
{ "force": true }
```

### memory_dream
执行 AutoDream 整合

```json
{ "force": false }
```
- `force: false` - 检查条件，满足后执行
- `force: true` - 强制立即执行

### memory_dream_status
查看整合状态

```json
{}
```

返回：
```json
{
  "enabled": true,
  "lastDream": "2026-03-30T22:00:00Z",
  "hoursSince": 21.5,
  "sessionsSinceLast": 5,
  "totalMemoryFiles": 32,
  "nextTrigger": "已达时间条件"
}
```

---

## 配置

```json
{
  "skills": {
    "memory-system": {
      "memoryDir": "~/.openclaw/workspace/memory",
      "flushMode": "safeguard",
      "softThresholdTokens": 300000,
      "vectorEnabled": true,
      "embeddingModel": "nomic-embed-text",
      "autoDream": {
        "enabled": true,
        "minHours": 24,
        "minSessions": 3,
        "apiKey": "env:MINIMAX_CODING_API_KEY"
      }
    }
  }
}
```

---

## 目录结构

```
memory/
├── MEMORY.md                    # 索引文件
├── .auto-dream-state.json      # 整合状态
├── user/                       # 用户记忆
│   └── [用户ID].md
├── feedback/                   # 反馈记忆
│   ├── positive/             # 正面确认
│   └── negative/             # 纠正指导
├── project/                   # 项目记忆
│   └── [项目名].md
├── reference/                 # 引用记忆
│   └── external.md
└── sessions/                  # 会话历史
    └── [日期].json
```

---

## 与 HEARTBEAT 集成

AutoDream 与 OpenClaw HEARTBEAT 深度集成：

```markdown
## 🌙 AutoDream 记忆整合 (每天 22:00)
- 自动检查触发条件
- 静默执行，无变化时通知
- 手动触发：说"执行记忆整合"
```

---

## 最佳实践

### 保存时机

| 类型 | 保存时机 | 示例 |
|------|---------|------|
| User | 了解用户信息 | "我是数据科学家" |
| Feedback | 用户纠正/确认 | "不要那样做" / "perfect" |
| Project | 了解项目动态 | "在做X项目" |
| Reference | 发现外部资源 | "bug在Linear跟踪" |

### 格式规范

```markdown
### [标题]
**Type:** negative | positive
**Why:** [原因]
**How to apply:** [何时应用]
**Date:** YYYY-MM-DD
```

### 索引规范

- 每条索引 <= 150 字符
- 使用绝对日期
- 按 user / feedback / project / reference 分类

---

## 技术架构

```
memory-system (v2.0.0)
├── src/
│   ├── index.ts          # 入口 + 工具注册
│   ├── search.ts         # 向量/关键词搜索
│   ├── write.ts          # 写入 + 触发检查
│   ├── get.ts            # 读取
│   ├── flush.ts          # 内存持久化
│   ├── autoLoad.ts       # 自动加载
│   ├── embed.ts          # 向量嵌入
│   └── autoDream.ts      # AutoDream LLM整合
└── HEARTBEAT.md          # 定时触发集成
```

---

**版本**: 2.0.0 | **更新**: AutoDream 与记忆系统深度整合
