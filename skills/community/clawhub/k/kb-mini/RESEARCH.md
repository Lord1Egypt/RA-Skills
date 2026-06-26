# 调研报告 - 参考项目分析

**日期**: 2026-03-22

---

## 一、GitHub/Skill 市场调研结果

### 1.1 ClawHub (Skill 市场)

**网址**: https://clawhub.com / https://clawhub.ai

**现状**:
- 刚上线，skill 数量较少
- 目前没有 knowledge-base 相关 skill
- 是未来发布的主要渠道

### 1.2 awesome-openclaw-skills

**Stars**: 40.6k
**链接**: https://github.com/VoltAgent/awesome-openclaw-skills

**现状**:
- 收录 339+ OpenClaw skills
- 按场景分类整理
- 包含中文版本

### 1.3 obsidian-agent-memory-skills

**Stars**: 27
**链接**: https://github.com/AdamTylerLynch/obsidian-agent-memory-skills

**核心设计**:
```
┌─────────────────────────────────────────────────┐
│ Session Start                                    │
│   Agent reads: TODOs → Project Overview          │
│   (2 files, ~100 lines — minimal token cost)     │
├─────────────────────────────────────────────────┤
│ During Work                                      │
│   Project Overview ──link──→ Component Note      │
│        │                         │               │
│        └──link──→ Pattern   ──link──→ Domain     │
│                    Note             Knowledge     │
│   Agent follows links ON DEMAND                  │
├─────────────────────────────────────────────────┤
│ Session End                                      │
│   Agent writes: Session summary, updates TODOs,  │
│   creates/updates component and pattern notes     │
└─────────────────────────────────────────────────┘
```

**优点**:
- **Proactive behaviors**: 自动 session 方向、结束时的 summary
- **Token 优化**: frontmatter-first scanning, CLI over file reads
- **Bidirectional relationships**: `relate` command with BFS tree walking
- **Graph traversal**: wikilinks 按需导航
- **多 agent 兼容**: Claude Code, Cursor, Cline, Windsurf, Copilot

**缺点**:
- 需要 Obsidian vault（额外依赖）
- 不支持 SQLite FTS5
- 无 RRF 融合检索

### 1.4 openclaw-superpowers

**Stars**: 25
**链接**: https://github.com/ArchieIndian/openclaw-superpowers

**核心设计**:
- **53 个 skills**: 15 核心 + 37 OpenClaw-native + 1 community
- **Self-modifying**: agent 可以自己写新 skill
- **DAG-based memory compaction**: 层级摘要 DAGs
- **SQLite session persistence + FTS5**: 和我们的方案类似！
- **Security guardrails**: 6 层安全防护
- **Runtime verification**: cron registration, state freshness

**关键特性**:
```
persistent-memory-hygiene    - 每日清理
memory-dag-compactor         - 层级 DAG 摘要
memory-integrity-checker     - DAG 完整性验证
session-persistence          - SQLite + FTS5 存储
dag-recall                   - DAG recall
context-assembly-scorer      - 上下文评分
```

**优点**:
- SQLite + FTS5 实现（和我们一致）
- DAG 层级摘要（可借鉴）
- 安全防护机制完善
- 20 个 cron scheduled skills

**缺点**:
- 偏向内存/会话管理，非专门知识库
- 无 RRF 融合检索
- 无明确的 topic_key upsert

### 1.5 para-memory

**Stars**: 4
**链接**: https://github.com/theSamPadilla/para-memory

**核心设计**:
| Folder | What goes here | Example |
|--------|-----------------|---------|
| `projects/` | Active work with goal/end | `migrate-to-v2.md` |
| `areas/` | Ongoing responsibilities | `infrastructure.md` |
| `resources/` | Reference material | `postgres-tuning.md` |
| `archives/` | Completed/inactive | `old-auth-system.md` |
| `memory/` | Daily logs (`YYYY-MM-DD.md`) | `2025-01-15.md` |

**优点**:
- PARA 方法论成熟
- 生命周期管理（active → archived）
- 每日 memory 日志

**缺点**:
- 无全文检索
- 无 SQLite 存储
- 偏向文件组织，非检索系统

---

## 二、可借鉴的设计

### 2.1 obsidian-agent-memory-skills 的借鉴点

1. **Proactive session orientation**
   - Session 开始时自动读取 TODOs + 项目概览
   - 最小化 token 消耗

2. **End-of-session summary**
   - Session 结束时自动写 summary
   - 更新 TODOs

3. **Bidirectional relationships**
   - `depends-on` / `depended-on-by`
   - `extends` / `extended-by`
   - BFS 树遍历

4. **Token 优化策略**
   - frontmatter-first scanning
   - CLI over file reads
   - scoped navigation

### 2.2 openclaw-superpowers 的借鉴点

1. **DAG-based memory compaction**
   - d0 leaf → d3+ durable 层级
   - depth-aware prompts

2. **Session persistence with FTS5**
   - SQLite + FTS5 实现
   - 可直接参考

3. **Integrity checker**
   - DAG orphans 检测
   - circular refs 检测
   - token inflation 检测

4. **Runtime verification**
   - cron registration 检查
   - state freshness 检查

### 2.3 para-memory 的借鉴点

1. **Lifecycle management**
   - active → archived 状态转换
   - 定期归档旧内容

2. **Daily memory log**
   - YYYY-MM-DD.md 日志
   - 便于时间追溯

---

## 三、我们的方案优化建议

### 3.1 借鉴 Proactive Session Orientation

**现状**: 只有 before_agent_start hook 触发 recall

**优化**: 借鉴 obsidian 的设计，session 开始时只读关键文件：
- 只读 L0 摘要层（< 200 tokens）
- 最多读 2 个文件
- 减少 token 消耗

### 3.2 借鉴 End-of-Session Summary

**现状**: after_turn hook 只做 capture

**优化**: 添加 session 结束检测：
- 检测 "done" / "wrapping up" 等关键词
- 自动写 session summary
- 更新相关 topic_key

### 3.3 借鉴 DAG-based Memory Compaction

**现状**: 只有简单的 access_level 分层

**优化**: 引入 DAG 结构：
- 叶子节点 = 原始内容
- 中间节点 = 摘要
- 根节点 = 高层次洞察
- 支持 expand/collapse

### 3.4 借鉴 Lifecycle Management

**现状**: 无生命周期管理

**优化**: 添加状态转换：
- active → stale → archived
- 自动归档 365 天前的 L0 记录
- 定期清理

### 3.5 借鉴 Token Optimization

**现状**: 加载层级粗粒度

**优化**: 借鉴 frontmatter-first scanning：
- 只加载 frontmatter 获取摘要
- 按需加载完整内容
- 使用 CLI 替代直接文件读取

---

## 四、结论

### 4.1 需要避免的

- **不要过度复杂化**: obsidian 的 bidirectional relationships 可能过度设计
- **不要引入过多依赖**: obsidian 需要额外安装
- **不要偏离核心**: 保持"怎么存、怎么取"的定位

### 4.2 应该采纳的

1. **SQLite + FTS5**: openclaw-superpowers 验证可行
2. **Proactive recall**: session 开始时自动检索
3. **DAG 摘要**: 层级化的记忆压缩
4. **Lifecycle management**: 定期归档和清理
5. **Token 优化**: frontmatter-first + 按需加载

### 4.3 保持我们的优势

- **RRF 融合检索**: 多个策略的结果融合
- **Topic_key upsert**: 同一主题的内容合并
- **共享 KB 模式**: 多 agent 共享知识库
- **Hook 自动触发**: before_agent_start + after_turn

---

## 五、下一步

- [ ] 详细分析每个借鉴点的实现细节
- [ ] 制定优化方案
- [ ] 更新 SPEC.md
