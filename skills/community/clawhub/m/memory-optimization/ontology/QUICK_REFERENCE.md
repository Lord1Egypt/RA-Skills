# Agent Memory Knowledge Graph - Quick Reference Card
# 知识图谱快速参考卡

---

## 🚀 常用命令

### 创建实体
```bash
# 决策
python3 scripts/memory_ontology.py create --type Decision --props '{"title":"标题","rationale":"理由","made_at":"2026-03-12T23:00:00+08:00","impact":"high","confidence":0.9,"status":"final","tags":["#decision"]}'

# 发现
python3 scripts/memory_ontology.py create --type Finding --props '{"title":"标题","content":"内容","discovered_at":"2026-03-12T22:00:00+08:00","type":"process","confidence":"confirmed","tags":["#finding"]}'

# 经验教训
python3 scripts/memory_ontology.py create --type LessonLearned --props '{"title":"标题","lesson":"教训内容","learned_at":"2026-03-12T23:30:00+08:00","mistake_or_success":"best_practice","application":"如何应用","tags":["#lesson"]}'

# 承诺
python3 scripts/memory_ontology.py create --type Commitment --props '{"description":"承诺内容","created_at":"2026-03-12T23:00:00+08:00","due_date":"2026-03-13","priority":"high","status":"pending","committed_to":"rong","tags":["#commitment"]}'
```

### 建立关系
```bash
python3 scripts/memory_ontology.py relate --from find_xxx --rel led_to_decision --to dec_xxx
```

### 查询
```bash
# 按类型查询
python3 scripts/memory_ontology.py query --type Decision

# 按标签查询
python3 scripts/memory_ontology.py query --tags "#memory" "#decision"

# 按状态查询
python3 scripts/memory_ontology.py query --type Commitment --status pending

# 详细输出
python3 scripts/memory_ontology.py query --type Decision --verbose
```

### 获取相关实体
```bash
python3 scripts/memory_ontology.py related --id dec_xxx
```

### 验证
```bash
python3 scripts/memory_ontology.py validate
```

### 统计
```bash
python3 scripts/memory_ontology.py stats
```

---

## 📋 实体类型速查

### Decision (决策)
**必填**: title, rationale, made_at  
**关键**: alternatives_considered, confidence, impact  
**何时用**: 技术选型、架构决策、流程改变

### Finding (发现)
**必填**: title, content, discovered_at, type, confidence  
**关键**: evidence, implications, source  
**何时用**: 问题根因、优化机会、重要洞察

### LessonLearned (经验教训)
**必填**: title, lesson, learned_at, mistake_or_success, application  
**关键**: context, related_findings, related_decisions  
**何时用**: 从错误/成功中学习、最佳实践

### Commitment (承诺)
**必填**: description, source, created_at, committed_to  
**关键**: due_date, priority, status, related_tasks  
**何时用**: 对用户承诺、接收任务

### ContextSnapshot (上下文快照)
**必填**: title, captured_at, content_summary, key_entities  
**关键**: compression_ratio, session_id  
**何时用**: 会话结束、上下文压缩前

---

## 🔗 核心关系

```
Finding ── led_to_decision ── Decision
                                 │
                                 └── decision_created ── Commitment
                                                               │
                                                               └── fulfilled_by ── Task

LessonLearned ── lesson_from ── [Decision, Finding, Task, Project]
```

---

## ✅ 最佳实践

### DO ✅
- 立即记录决策（不要等待！）
- 详细记录 rationale（为什么）
- 建立实体间关系
- 使用标签
- 定期验证

### DON'T ❌
- 不要延迟记录
- 不要只记录"是什么"
- 不要忽略置信度
- 不要让实体孤立
- 不要过度记录

---

## 📁 文件位置

```
ontology/
├── graph.jsonl              # 图谱数据
├── memory-schema.yaml       # Schema 定义
├── entity-templates.md      # 实体模板
├── INTEGRATION.md           # 集成指南
├── IMPLEMENTATION_SUMMARY.md # 实施总结
└── QUICK_REFERENCE.md       # 本文件

scripts/
└── memory_ontology.py       # 管理工具
```

---

## 🎯 工作流

### 记录决策流程
1. 创建 Decision 实体
2. 记录 rationale（最重要！）
3. 列出 alternatives_considered
4. 设置 confidence 和 impact
5. 添加标签
6. 关联相关 Finding/Task

### 记录发现流程
1. 创建 Finding 实体
2. 描述内容和证据
3. 设置 type 和 confidence
4. 说明 implications
5. 如果导致决策，创建 Decision 并关联

### 经验学习流程
1. 创建 LessonLearned 实体
2. 描述 lesson（具体、可操作）
3. 设置 mistake_or_success
4. 说明 application
5. 关联相关 Finding/Decision

---

## 🔍 查询示例

### 查找所有待履行承诺
```bash
python3 scripts/memory_ontology.py query --type Commitment --status pending
```

### 查找某个决策的背景
```bash
python3 scripts/memory_ontology.py get --id dec_xxx --verbose
python3 scripts/memory_ontology.py related --id dec_xxx
```

### 查找所有经验教训
```bash
python3 scripts/memory_ontology.py query --type LessonLearned --verbose
```

### 导出为 Markdown
```bash
python3 scripts/memory_ontology.py export --output memory/kg-export.md
```

---

## 📊 当前状态

**实体总数**: 790+ (see `python3 scripts/memory_dashboard.py --view json` for current count)
**验证状态**: ✅ 通过

---

## 📞 完整文档

- **集成指南**: `ontology/INTEGRATION.md`
- **实体模板**: `ontology/entity-templates.md`
- **实施总结**: `ontology/IMPLEMENTATION_SUMMARY.md`
- **Schema**: `ontology/memory-schema.yaml`

---

*版本：1.0.2 | 最后更新：2026-03-29*
