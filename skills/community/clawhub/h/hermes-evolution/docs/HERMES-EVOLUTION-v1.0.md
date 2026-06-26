# 爱马仕自动进化版 - 升级文档

> **版本**: Hermes Evolution v1.0  
> **日期**: 2026-04-11  
> **适用**: OpenClaw 所有版本（基于 Node.js）  
> **作者**: 森森  
> **备份位置**: `backups/backup-20260411-hermes-evolution/`

---

## 📋 目录

1. [概述](#概述)
2. [架构设计](#架构设计)
3. [文件清单](#文件清单)
4. [核心模块详解](#核心模块详解)
5. [部署指南](#部署指南)
6. [升级指南](#升级指南)
7. [故障排查](#故障排查)

---

## 概述

### 什么是爱马仕进化版？

爱马仕进化版是森森在 OpenClaw 基础上构建的**智能增强层**，实现了：

- **主动服务**：不等指令，主动自检、预测需求
- **自动进化**：观察工作流，自动创建 Skill
- **用户理解**：角色画像，行为预测
- **性能优化**：FTS 检索、增量存储、Token 控制

### 与原生 OpenClaw 的区别

| 维度 | 原生 OpenClaw | 爱马仕进化版 |
|------|--------------|-------------|
| 响应模式 | 被动等指令 | 主动服务 |
| 记忆系统 | 简单 JSON | Frozen Memory + DAG |
| 学习能力 | 无 | Self-Improving v2 |
| 用户理解 | 无 | Honcho Profiler |
| 检索性能 | O(n) 遍历 | FTS 0.03ms |

---

## 架构设计

### 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        OpenClaw Gateway                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐   │
│   │  Router     │───▶│  Sessions   │───▶│  Skills         │   │
│   └─────────────┘    └─────────────┘    └─────────────────┘   │
│         │                                       │              │
│         ▼                                       ▼              │
│   ┌─────────────────────────────────────────────────────┐     │
│   │                  爱马仕增强层                          │     │
│   │  ┌───────────┐  ┌───────────┐  ┌───────────────┐   │     │
│   │  │PM Router  │  │Task Store │  │Intent Router  │   │     │
│   │  └───────────┘  └───────────┘  └───────────────┘   │     │
│   │  ┌───────────┐  ┌───────────┐  ┌───────────────┐   │     │
│   │  │Self-Imp   │  │Frozen Mem │  │Periodic Nudge │   │     │
│   │  └───────────┘  └───────────┘  └───────────────┘   │     │
│   │  ┌───────────┐  ┌───────────┐  ┌───────────────┐   │     │
│   │  │Honcho     │  │AutoSkill  │  │FTS Indexer    │   │     │
│   │  └───────────┘  └───────────┘  └───────────────┘   │     │
│   │  ┌───────────┐  ┌───────────┐  ┌───────────────┐   │     │
│   │  │TaskDAG    │  │Collab Vis │  │Template Eng   │   │     │
│   │  └───────────┘  └───────────┘  └───────────────┘   │     │
│   └─────────────────────────────────────────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 数据流

```
用户输入 → IntentRouter → PM Router → Agent 分配
                │
                ▼
         Task Store (创建任务)
                │
                ▼
         Task DAG (依赖分析)
                │
                ▼
         Collaboration Scheduler (协作调度)
                │
                ▼
         Self-Improving v2 (学习改进)
                │
                ▼
         Frozen Memory (记忆持久化)
```

---

## 文件清单

### 核心文件（必须保留）

| 文件 | 功能 | 依赖 |
|------|------|------|
| `sensen-pm-router.js` | 路由核心 + Agent Profile | 无 |
| `agent-profiles.js` | Agent 角色定义 | 无 |
| `task-manager.js` | 任务状态机 | 无 |
| `task-store.js` | 任务存储 + 索引 | 无 |
| `task-dag.js` | DAG 依赖管理 | 无 |
| `intent-router.js` | TF-IDF 意图路由 | 无 |
| `sensen-self-improving-v2.js` | 自改进引擎 v2 | corrections/, rules/ |
| `frozen-memory.js` | 冻结记忆 | 无 |
| `patch-store.js` | 增量更新 | corrections/ |
| `enhanced-skill.js` | Skill 增强结构 | 无 |
| `fts-indexer.js` | 全文检索 | 无 |
| `progressive-disclosure.js` | 渐进式加载 | 无 |
| `periodic-nudge.js` | 主动自检引擎 | task-manager, self-improving |
| `auto-skill-generator.js` | 自动创建 Skill | 无 |
| `llm-summarizer.js` | LLM 摘要 | 无 |
| `honcho-profiler.js` | 用户画像 | 无 |
| `sensen-logger.js` | 结构化日志 | 无 |
| `sensen-collaborator.js` | 协作调度器 | 无 |
| `sensen-collab-visualizer.js` | 协作可视化 | collaborator |
| `template-engine.js` | 模板引擎 | 无 |
| `sensen-scheduler.js` | 定时调度 | 无 |
| `sensen-feishu-notifier.js` | 飞书通知 | 无 |
| `sensen-spawner.js` | Agent Spawn | 无 |

### 数据目录

| 目录 | 内容 |
|------|------|
| `tasks/` | 任务 JSON 文件 |
| `corrections/` | 纠正记录 (JSONL) |
| `rules/` | 生成的规则 |
| `schedules/` | 定时任务配置 |
| `collaborations/` | 协作记录 |

### 测试文件

| 文件 | 功能 |
|------|------|
| `test-*.js` | 各模块测试脚本 |

---

## 核心模块详解

### 1. TaskStore (任务存储)

**文件**: `task-store.js`

**功能**: 内存缓存 + 索引加速

**核心 API**:

```javascript
const TaskStore = require('./task-store');

// 创建任务
const task = TaskStore.createTask({
  title: '测试任务',
  assignedTo: 'Marketing',
  priority: 'high'
});

// 更新任务
TaskStore.updateTask(taskId, { status: 'done' });

// 查询（索引加速）
const tasks = TaskStore.queryByStatus('inbox');
const tasks = TaskStore.queryByAssignee('Marketing');

// 统计
const stats = TaskStore.getStats();

// 打印看板
TaskStore.printKanban();
```

**性能**: 查询从 O(n) → O(1)，1000 次查询 < 50ms

---

### 2. IntentRouter (意图路由)

**文件**: `intent-router.js`

**功能**: TF-IDF 置信度计算

**核心 API**:

```javascript
const IntentRouter = require('./intent-router');

// 路由
const result = IntentRouter.route('发布小红书内容');
console.log(result.agent);      // 'Marketing'
console.log(result.confidence); // 0.85

// 添加关键词
IntentRouter.addKeyword('Marketing', ['小红书', '内容', '发布']);

// 排除词
IntentRouter.setExcludedWords(['测试', '调试']);
```

---

### 3. Self-Improving v2 (自改进)

**文件**: `sensen-self-improving-v2.js`

**功能**: 规则权重 + 版本管理 + 有效期

**核心 API**:

```javascript
const SelfImproving = require('./sensen-self-improving-v2');

// 记录纠正
SelfImproving.logCorrection({
  type: SelfImproving.CorrectionType.FORMAT,
  originalText: '太长了',
  correction: '输出简洁'
});

// 获取规则
const rules = SelfImproving.getActiveRules();

// 检查文本是否匹配规则
const result = SelfImproving.matchRule('太长了缩短');
if (result.matched) {
  console.log('匹配规则:', result.rule.description);
}

// 获取统计
const stats = SelfImproving.getStats();
```

---

### 4. FrozenMemory (冻结记忆)

**文件**: `frozen-memory.js`

**功能**: 编辑存入 staging，下次会话生效

**核心 API**:

```javascript
const FrozenMemory = require('./frozen-memory');

// 编辑（存入 staging，当前会话不受影响）
FrozenMemory.stageEdit('memory/2026-04-11.md', '# 新内容');

// 冻结（下次会话生效）
FrozenMemory.freezeMemory('2026-04-11');

// 获取所有记忆（启动时调用）
const memories = FrozenMemory.readAllMemoryForSession();
```

---

### 5. PeriodicNudge (主动自检)

**文件**: `periodic-nudge.js`

**功能**: 主动发现问题，不等纠正

**核心 API**:

```javascript
const { createEngine } = require('./periodic-nudge');

const engine = createEngine({ interval: 60 * 60 * 1000 }); // 1小时

// 启动
engine.start();

// 获取摘要
const summary = engine.getSummary();
console.log(`待处理: ${summary.total} 个`);
console.log(`紧急: ${summary.critical} 个`);

// 获取待处理项
const pending = engine.getPendingNudges();

// 停止
engine.stop();
```

---

### 6. HonchoProfiler (用户画像)

**文件**: `honcho-profiler.js`

**功能**: 用户画像 + 行为预测

**核心 API**:

```javascript
const { HonchoProfiler } = require('./honcho-profiler');

const profiler = new HonchoProfiler();

// 获取/创建画像
const profile = profiler.getProfile('user_001');

// 更新身份
profile.updateIdentity({
  name: '苍苍子森',
  title: 'HR一号位'
});

// 添加目标
profile.addGoal('三年内实现财富自由');

// 记录交互
profiler.recordInteraction('user_001', {
  responseTime: 5000,
  hour: 9,
  intent: '小红书发布'
});

// 预测需求
const predictions = profile.predictNeeds();

// 获取推荐
const recs = profile.getRecommendations();
```

---

### 7. AutoSkillGenerator (自动创建 Skill)

**文件**: `auto-skill-generator.js`

**功能**: 观察工作流，自动创建 Skill

**核心 API**:

```javascript
const { AutoSkillGenerator } = require('./auto-skill-generator');

const generator = new AutoSkillGenerator({ minFrequency: 3 });

// 记录工具调用
generator.recordCall('tavily_search', { query: '小红书热门' }, { success: true });
generator.recordCall('content_writer', { topic: 'HR转型' }, { success: true });
// ... 重复3次后自动创建 Skill

// 获取统计
const stats = generator.getStats();

// 手动触发分析
generator.analyzeNow();
```

---

### 8. FTSIndexer (全文检索)

**文件**: `fts-indexer.js`

**功能**: 反向索引 + TF-IDF

**核心 API**:

```javascript
const { FTSIndexer } = require('./fts-indexer');

const fts = new FTSIndexer();

// 添加文档
fts.addDocument('doc1', '小红书内容运营攻略', { type: 'tutorial' });

// 搜索
const results = fts.search('小红书 运营');
console.log(results[0].score); // 0.85

// 短语搜索
const phrase = fts.searchPhrase('财富自由');

// 保存/加载
fts.save('myindex');
fts.load('myindex');
```

**性能**: 1000 次搜索 < 100ms (0.03ms/次)

---

## 部署指南

### 前提条件

- Node.js 16+
- OpenClaw 已安装并运行
- 飞书 Channel 已配置

### 步骤 1: 备份当前配置

```powershell
# 创建备份目录
$backupDir = "backups/backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')-before-hermes"
New-Item -Path $backupDir -ItemType Directory -Force

# 复制当前 Skills
Copy-Item -Path "skills/sensen-pm-router" -Destination "$backupDir/" -Recurse

# 复制配置文件
Copy-Item -Path "skills/sensen-pm-router/*.js" -Destination "$backupDir/"
```

### 步骤 2: 复制爱马仕文件

```powershell
# 从备份复制所有 .js 文件
$source = "backups/backup-20260411-hermes-evolution"
Copy-Item -Path "$source\*.js" -Destination "skills/sensen-pm-router\" -Force

# 复制目录结构
Copy-Item -Path "$source\tasks" -Destination "skills/sensen-pm-router\" -Recurse -Force
Copy-Item -Path "$source\rules" -Destination "skills/sensen-pm-router\" -Recurse -Force
Copy-Item -Path "$source\corrections" -Destination "skills/sensen-pm-router\" -Recurse -Force
```

### 步骤 3: 验证部署

```powershell
# 运行测试
node "skills/sensen-pm-router/test-task-store.js"
node "skills/sensen-pm-router/test-intent-router.js"
node "skills/sensen-pm-router/test-self-improving-v2.js"
node "skills/sensen-pm-router/test-fts-indexer.js"
node "skills/sensen-pm-router/test-honcho-profiler.js"
```

### 步骤 4: 健康检查

```powershell
# 检查 Gateway 状态
openclaw gateway status

# 检查端口
curl -s http://localhost:18790/health || echo "Port check failed"
```

---

## 升级指南

### 当 OpenClaw 升级时

如果 OpenClaw 发布了新版本，按以下步骤升级：

#### 1. 确认兼容性

```
┌─────────────────────────────────────────────────────────────┐
│  检查项                                                     │
├─────────────────────────────────────────────────────────────┤
│  □ Node.js 版本是否兼容 (需要 16+)                          │
│  □ OpenClaw API 是否有重大变化                              │
│  □ Channel Plugin 接口是否变化                               │
│  □ sessions_spawn 接口是否变化                              │
└─────────────────────────────────────────────────────────────┘
```

#### 2. 执行升级

```powershell
# 1. 备份当前爱马仕配置
$hermesBackup = "backups/hermes-before-openclaw-$(Get-Date -Format 'yyyyMMdd')"
Copy-Item -Path "skills/sensen-pm-router" -Destination $hermesBackup -Recurse

# 2. 升级 OpenClaw
npm update openclaw -g

# 3. 测试基础功能
openclaw gateway status
openclaw skills list

# 4. 运行爱马仕测试
node "skills/sensen-pm-router/test-task-store.js"

# 5. 如果测试失败，查看错误并修复
```

#### 3. 常见兼容性问题

| 问题 | 解决方案 |
|------|----------|
| `sessions_spawn` 接口变化 | 检查 `sensen-spawner.js`，更新调用方式 |
| Channel API 变化 | 检查 `sensen-feishu-notifier.js` |
| Skills 加载路径变化 | 更新 `require` 路径 |
| Cron 格式变化 | 检查 `sensen-scheduler.js` |

#### 4. 快速回滚

```powershell
# 如果升级失败，回滚
Remove-Item -Path "skills/sensen-pm-router" -Recurse -Force
Copy-Item -Path "backups/backup-20260411-hermes-evolution" -Destination "skills/sensen-pm-router" -Recurse
```

---

## 故障排查

### 常见问题

#### 1. TaskStore 查询返回空

```javascript
// 检查索引是否初始化
const store = require('./task-store');
console.log(store.getStats());

// 重新构建索引
store.rebuildIndex();
```

#### 2. IntentRouter 路由错误

```javascript
// 检查关键词
const router = require('./intent-router');
console.log(router.getKeywords());

// 添加缺失的关键词
router.addKeyword('AgentName', ['keyword1', 'keyword2']);
```

#### 3. Self-Improving 不生效

```javascript
// 检查规则文件
const fs = require('fs');
console.log(fs.readdirSync('./rules'));

// 检查 corrections
console.log(fs.readdirSync('./corrections'));
```

#### 4. FTS 搜索慢

```javascript
// 重建索引
const fts = new FTSIndexer();
fts.rebuildIndex();
fts.save('default');
```

### 日志位置

| 类型 | 位置 |
|------|------|
| 爱马仕日志 | `skills/sensen-pm-router/.logs/` |
| 任务日志 | `skills/sensen-pm-router/tasks/` |
| 规则日志 | `skills/sensen-pm-router/rules/` |
| OpenClaw 日志 | `~/.openclaw/logs/` |

### 调试模式

```javascript
// 启用调试日志
const logger = require('./sensen-logger');
logger.setLevel('DEBUG');

// 打印调用栈
logger.error('Error occurred', { stack: new Error().stack });
```

---

## 附录

### A. 文件哈希（用于验证完整性）

```
备份: backup-20260411-hermes-evolution/
文件数: 65
核心模块: 23 个 .js 文件
数据目录: 4 个 (tasks, rules, corrections, schedules)
```

### B. 依赖关系图

```
sensen-pm-router.js
├── agent-profiles.js
├── task-manager.js
│   └── task-store.js
│       └── fts-indexer.js
├── task-dag.js
├── intent-router.js
├── sensen-self-improving-v2.js
│   ├── corrections/
│   └── rules/
├── frozen-memory.js
├── patch-store.js
│   └── corrections/
├── enhanced-skill.js
├── progressive-disclosure.js
├── periodic-nudge.js
│   ├── task-manager.js
│   └── sensen-self-improving-v2.js
├── auto-skill-generator.js
├── llm-summarizer.js
├── honcho-profiler.js
├── sensen-logger.js
├── sensen-collaborator.js
│   └── task-dag.js
├── sensen-collab-visualizer.js
│   └── sensen-collaborator.js
├── template-engine.js
├── sensen-scheduler.js
├── sensen-feishu-notifier.js
└── sensen-spawner.js
```

### C. 测试清单

```powershell
# 运行所有测试
node test-task-store.js
node test-intent-router.js
node test-self-improving-v2.js
node test-frozen-memory.js
node test-patch-store.js
node test-enhanced-skill.js
node test-fts-indexer.js
node test-progressive-disclosure.js
node test-periodic-nudge.js
node test-auto-skill-generator.js
node test-llm-summarizer.js
node test-honcho-profiler.js
node test-logger.js
node test-dag.js
node test-template.js
node test-collaborator.js
node test-collab-visualizer.js
node test-scheduler.js
```

---

## 更新日志

| 日期 | 版本 | 更新内容 |
|------|------|----------|
| 2026-04-11 | v1.0 | 爱马仕进化版初始发布 |

---

*文档生成时间: 2026-04-11 18:40 GMT+8*
*如有问题，请检查备份或联系森森*
