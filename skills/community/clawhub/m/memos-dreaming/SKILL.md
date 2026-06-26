# SKILL.md — MemOS Dreaming: Autonomous Memory Consolidation

> 每日凌晨自动运行的记忆蒸馏系统。融合 MemOS SQLite 和每日日志两个信号源，类 Dreaming 六维评分，只提炼真正有价值的记忆写入 MEMORY.md。

---

## 🗂 工作原理

```
每日凌晨 3:00 (cron)
     │
     ├── Source 1: MemOS SQLite
     │   ├── skills 表: quality_score ≥ 0.5 的活跃 skill
     │   └── tasks 表: skill_status = 'promoted' 的任务
     │
     ├── Source 2: 每日记忆日志
     │   └── memory/YYYY-MM-DD.md
     │       提取 ## Decisions / ## Lessons Learned / ## Projects
     │
     └── 双源合并 → 六维评分 → 阈值筛选
              ↓
          DREAMS.md 审查草稿（供人工检查）
              ↓
          写入 MEMORY.md（每日上限 5 条）
```

---

## 📊 六维评分体系（Dreaming 启发）

| 维度 | 权重 | 信号源 |
|---|---|---|
| Relevance（相关性） | 30% | MemOS quality_score（0-10 → 归一化） |
| Frequency（频率） | 24% | skill merge_count / task 引用次数 |
| Query Diversity（查询多样性） | 15% | 跨不同 session/文件的分布 |
| Recency（近因） | 15% | 更新时间，半衰期 30 天 |
| Consolidation（巩固） | 10% | 多日重复出现的条目 |
| Conceptual Richness（概念密度） | 6% | topic tag 数量和长度 |

---

## 🚀 使用方式

### Dry Run（查看本周候选，不写入）
```bash
python3 ~/.openclaw/workspace/skills/memos-dreaming/scripts/memos_dreaming.py
```

### Apply（执行蒸馏，写入 MEMORY.md）
```bash
python3 ~/.openclaw/workspace/skills/memos-dreaming/scripts/memos_dreaming.py --apply
```

### 调整参数
```bash
# 更激进（降低阈值）
python3 ~/.openclaw/workspace/skills/memos-dreaming/scripts/memos_dreaming.py --apply --min-score 0.50

# 更多条（每日上限）
python3 ~/.openclaw/workspace/skills/memos-dreaming/scripts/memos_dreaming.py --apply --limit 10
```

---

## 📁 输出文件

| 文件 | 位置 | 说明 |
|---|---|---|
| DREAMS.md | workspace/ | 审查草稿，每次运行覆盖，包含所有候选条目和评分🆕=新候选 |
| AUDIT.md | workspace/ | 每周审计报告，含去重/过期/噪声发现和修复建议 |
| MEMORY.md | workspace/ | 长期记忆，正式写入位置 |
| promoted.jsonl | workspace/.memos-dreaming/ | 已promote条目的去重索引 |
| audits/ | workspace/.memos-dreaming/audits/ | 审计自动备份目录 |

---

## ⏰ Cron 配置

**每日 Dreaming（凌晨 3:00 北京时间）**
- 自动执行双源蒸馏 + 写入 MEMORY.md
- Cron ID: `2f918133-520a-43f7-b725-21630d33007c`

**每周审计（周六 10:00 北京时间）**
- 扫描 MEMORY.md：重复条目、过期内容、噪声清理
- Cron ID: `606eead7-9345-45dc-88a7-b88b54b7b901`
- 审计报告输出到 `workspace/AUDIT.md`
- `--apply` 模式自动清理高置信度噪声（自动备份）

**验证 cron 是否配置**:
```bash
openclaw cron list | grep -i dreaming
```

**手动触发 Dreaming（不写入）**:
```bash
cd ~/.openclaw/workspace/skills/memos-dreaming/scripts && python3 memos_dreaming.py
```

**手动触发审计**:
```bash
cd ~/.openclaw/workspace/skills/memos-dreaming/scripts && python3 memos_dreaming_audit.py
```

---

## ⚙️ 阈值调节参考

| Min Score | 预期效果 |
|---|---|
| 0.70（默认） | 严格，只promote高质量条目 |
| 0.60 | 适中 |
| 0.50 | 激进，更多条目进入MEMORY.md |
| 0.40 | 宽松，可能产生噪声 |

---

## 🔧 故障排查

**DREAMS.md 为空？**
→ 系统判定没有条目达到阈值，说明近期记忆质量不足（正常现象）

**MemOS candidates: 0？**
→ 检查 MemOS SQLite 路径是否正确：`~/.openclaw/memos-local/memos.db`

**已promote条目重复进入？**
→ promoted.jsonl 已去重，正常情况下不会重复

---

## 🧠 架构设计原则

1. **双源并行**: MemOS Skills/Tasks + 每日日志，两个信号互相补充
2. **评分先于写入**: 先六维评分，再阈值筛选，最后才写入
3. **DREAMS.md 审查**: 每次运行生成可读草稿，人工可追溯决策
4. **去重保护**: promoted.jsonl 防止同一条目重复写入
5. **每日上限**: 最多5条/天，防止MEMORY.md膨胀

---

## 📌 与官方 Dreaming 的区别

| | 官方 Dreaming | MemOS Dreaming |
|---|---|---|
| 信号源 | 每日日志 + recall traces | MemOS Skills/Tasks + 每日日志 |
| 触发机制 | memory-core 插件 | 自定义 Python cron |
| 评分体系 | 六维（相同权重） | 六维（相同权重） |
| 输出位置 | MEMORY.md | MEMORY.md + DREAMS.md |
| 可控性 | 插件内部 | 完全透明可调 |

---

Skill ID: `memos-dreaming`
Version: 1.0.0
Owner: agent:main
