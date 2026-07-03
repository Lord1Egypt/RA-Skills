# Memory 文件结构规范

本 Skill 的核心存储单元是 `memory-{npc_id}.md`,一个文件搞定一个画像的所有内容。

## 文件总体结构

```
─────────────────────────────────
| YAML Frontmatter (画像结构化数据)
─────────────────────────────────
| # 画像综述 (人类可读)
| ## 决策风格综述
| ## 高频反应模式
| ## 沟通偏好
| ## 雷区清单
─────────────────────────────────
| ---
| # 语料库 (按时间倒序追加)
| ## C-20260520-001 ...
| ## C-20260418-003 ...
| ## C-20250312-001 ...
─────────────────────────────────
```

## Frontmatter 字段定义

```yaml
---
# === 标识字段 ===
npc_id: L001              # 永不变,代号
relation: direct_superior    # 关系类型枚举
created: 2025-09-12
updated: 2026-05-20

# === 累积统计 ===
evidence_count: 47           # 累计语料条数
confidence: high             # 自动计算: <10=low, 10-30=medium, >30=high

# === 决策偏好量化 (0-1 区间) ===
decision_axes:
  data_vs_intuition: 0.72    # 0=纯直觉, 1=纯数据
  short_vs_long_term: 0.40
  risk_appetite: 0.30
  innovation_vs_execution: 0.65
  top_down_vs_bottom_up: null  # null=证据不足

# === 沟通风格 ===
communication_style:
  prefers_bluf: true
  ideal_doc_length: one-pager  # one-pager|short-deck|detailed-doc|verbal-only
  tolerates_uncertainty: false
  interrupt_frequency: high    # low|medium|high
  feedback_style: direct       # direct|sandwich|written|silent

# === 高频质询点 ===
frequent_challenges:
  - theme: ROI测算依据
    weight: 0.85
    evidence: [C-20250312-001, C-20250418-003]
  - theme: 竞品对标
    weight: 0.72
    evidence: [C-20250205-007]

# === 雷区清单 ===
redlines:
  - 避免"大概""可能"等模糊词
  - 汇报不超过3页
  - 不接受口头承诺

# === 偏好模式 ===
preferred_patterns:
  - 数字+对比+建议三段式
  - 结论先行

# === 每个 axis 的证据数(用于置信度) ===
evidence_by_axis:
  data_vs_intuition: 18
  short_vs_long_term: 8
  risk_appetite: 12
  innovation_vs_execution: 6
  top_down_vs_bottom_up: 2
---
```

## 正文画像区

人类可读的画像综述,4 个固定小节:

```markdown
# L001 画像综述

## 决策风格综述
[2-3 段文字描述]

## 高频反应模式
- 听到 X → 大概率反应 Y
- ...

## 沟通偏好
- BLUF 结构
- ...

## 雷区清单
[复述 frontmatter.redlines,展开解释]
```

## 语料库区块

每条语料一个 `## C-{date}-{seq}` 二级标题,**按时间倒序**(新的在上)。

```markdown
---

# 语料库

## C-20260520-003 · 周会上的方案讨论

- date: 2026-05-20
- scene: 周会
- channel: 会议
- attribution: direct
- weight: 1.0
- tags: [质询-数据来源, 风格-直接]

**场景背景**: 产品同学汇报 Q2 新增用户数据时...

**内容**:
> "你说的 30% 增长,样本是哪几天的?
>  如果只看上周,可能是节假日效应。"

**抽取信号**:
- challenges_raised: 数据样本量 (intensity: high)
- style_signals: prefers_bluf=true
- preferences_expressed: data_vs_intuition direction=1 strength=0.8

**我的判断**: 他对短期数据敏感度高,要拿出周-月-季三个维度的对比才能让他相信趋势。

---

## C-20260418-003 · 邮件回复

[同样结构]

---

## C-20250312-001 · Q1业务复盘会

[同样结构]
```

## 关键约束

1. **代号一致性**: 文件名是 `memory-L001.md`,frontmatter 的 `npc_id` 也是 `L001`,正文中所有提到这个人的地方都用 `L001`。**绝不允许出现真名**。

2. **语料 ID 格式**: `C-YYYYMMDD-NNN` 三位序号。同一天多条按 001/002/003 递增。

3. **倒序排列**: 新语料插入到"# 语料库"之后的第一条位置,不要 append 到末尾。这样最近的内容在视觉上最靠前。

4. **删除策略**: 删除某条语料时,**注释掉而非真删**:
   ```markdown
   <!-- DELETED 2026-05-21
   ## C-20260418-003 · 旧标题
   ...原内容...
   -->
   ```
   这样历史可追溯,误删可恢复。

5. **文件大小**: 单个 memory 文件建议 < 5MB(约 5000 条语料)。超过后用 `scripts/archive_memory.py` 归档旧语料到 `memory-{npc_id}-archive-{year}.md`。

6. **行尾**: 统一使用 LF(不要 CRLF),避免跨平台 diff 混乱。

## 给开发者的 Tips

- 解析时优先用 `python-frontmatter` 库读 frontmatter,正文按 `^## C-\d{8}-\d{3}` 切分
- 写入时**永远先读完整文件→修改→整体写回**,避免增量写入导致格式错乱
- 任何修改前用 `cp memory-L001.md memory-L001.md.bak` 备份,出错可回滚
