# LLM Wiki 生命周期手册

## 1. 目标

LLM Wiki 不是“让模型随手写 Markdown”，而是一条可重复的知识编译流水线。它将外部来源保存为不可变证据，将可修改的 Wiki 页面视为编译产物，并让查询、反馈和更新重新进入流水线。

```text
Blueprint → Scaffold → Ingest → Compile → Audit → Query
                    ↑                    ↓          ↓
                    └──── Refresh ← Promote ← Feedback
                                      ↓
                                Deprecate/Archive
```

## 2. 状态模型

| 对象 | 状态 | 含义 | 允许的下一步 |
|------|------|------|--------------|
| 来源 | `candidate` | 尚未验证可访问性与价值 | ingest / reject |
| 来源 | `ingested` | 原文与元数据已保存 | compile / supersede |
| 来源 | `superseded` | 有新版但旧版仍保留 | archive-reference |
| 页面 | `draft` | 结构和证据尚不完整 | review / compile |
| 页面 | `active` | 可供查询的当前知识 | refresh / disputed / deprecated |
| 页面 | `disputed` | 来源之间存在未裁决冲突 | review / active |
| 页面 | `stale` | 超过新鲜度阈值或上游变化 | refresh / deprecated |
| 页面 | `deprecated` | 不再作为当前答案依据 | archive |
| 审计项 | `open` | 人类反馈或自动问题待处理 | accept / reject / defer |
| 审计项 | `resolved` | 结论和证据已记录 | reopen |

状态必须显式写入 frontmatter 或审计记录，不能仅存在于聊天上下文。

## 3. 操作契约

### Blueprint

输入是受众、范围、非目标、代表性问题和数据边界。输出是 `WIKI.md`、配置与最小页面分类。没有至少 10 个真实问题，不进入 Scaffold。

### Scaffold

只新增目录和模板，不覆盖既有内容：

```bash
python3 scripts/scaffold_wiki.py ./target --title "Runtime Wiki" --strict
```

### Ingest

每个来源形成“原文 + 元数据”。先判断增量：

```text
新主题？            → New
修正/扩展旧知识？   → Update
与当前结论冲突？    → Disputed
没有实质增量？      → No material change
```

只有前三类进入编译队列；无增量来源可记录拒绝理由，但不必复制全文。

### Compile

按概念边界聚合多个来源。先定位精确证据，再写结论；最后更新交叉链接和索引。共享页面与索引串行写入，避免并行 Agent 相互覆盖。

### Audit

机械门禁检查结构、链接、来源、新鲜度和索引；判断性审查检查事实表达、冲突处理与范围一致性。

```bash
python3 scripts/build_manifest.py ./target --strict
python3 scripts/audit_wiki.py ./target --max-age-days 180 --strict
```

### Query

依次读取索引、全文命中和相邻页面。答案将内容标为“Wiki 明示”“基于证据推断”或“未知”。查询输出默认进 `outputs/queries/`，不是 Wiki 正文。

### Promote

查询结果同时满足以下条件才晋升：可重复使用、跨越至少两个页面或来源、存在稳定证据、能明确归入页面类型。一次性答复和强时效内容不晋升。

### Refresh / Deprecate

来源更新后，先根据 Manifest 找受影响页面，再重新编译。旧页面应标记 `deprecated` 并给出替代页，不能删除历史上下文。

## 4. 事务与并发

| 工作 | 是否可并行 | 原因 |
|------|------------|------|
| 下载互不相关来源 | 是 | 目标文件独立 |
| 生成不同来源摘要 | 是 | 页面互不覆盖时安全 |
| 修改同一概念页 | 否 | 会产生语义和文本冲突 |
| 更新全局索引/Manifest | 否 | 共享状态必须串行 |
| 查询不同问题 | 是 | 输出隔离 |
| 处理同一审计项 | 否 | 必须只有一个最终裁决 |

每次批处理以“一组来源成功落盘 + 所有受影响页面通过审计”为事务边界。失败时保留原始来源，回滚未通过门禁的 Wiki 页面，不伪造完成状态。

## 5. 恢复策略

- 摄取失败：记录 URL、时间与错误；不创建空来源文件。
- 编译中断：从 Manifest 和变更列表恢复，不依赖模型记忆。
- 索引冲突：重新从页面生成 Manifest，再人工合并导航文案。
- 来源消失：保留已授权的归档与哈希，标记可访问性变化。
- 审计失败：问题留在 `audit/open/`；不得通过删除检查项“修复”。

## 6. 操作日志

每次运行在 `log/YYYY-MM-DD.md` 记录：操作者、输入来源、受影响页面、审计结果、未决冲突和回滚点。日志写决策，不复制整份 Diff。

## 7. 完成检查表

- [ ] Wiki 宪章定义了范围、受众、非目标和成功问题
- [ ] 原始来源与知识页面物理分层
- [ ] 每个可查询页面有显式状态、日期、责任人和来源
- [ ] 共享索引与概念页没有并行写入竞争
- [ ] 查询结果只有满足晋升契约才进入 Wiki
- [ ] 刷新、弃用、反馈和失败都有可追踪记录
- [ ] Manifest 与审计门禁在发布前通过

## 相关子技能（L3）

本手册的「Wiki 生命周期」操作契约覆盖以下子技能，运行时按阶段调取对应子技能：

- [wiki-blueprint](../skills/wiki-blueprint/SKILL.md) — Blueprint 阶段（§3 ### Blueprint）。
- [wiki-source-ingestion](../skills/wiki-source-ingestion/SKILL.md) — Ingest 阶段（§3 ### Ingest）。
- [wiki-knowledge-compilation](../skills/wiki-knowledge-compilation/SKILL.md) — Compile / Promote 阶段（§3 ### Compile / Promote）。
- [wiki-quality-audit](../skills/wiki-quality-audit/SKILL.md) — Audit 阶段（§3 ### Audit）。
- [wiki-grounded-query](../skills/wiki-grounded-query/SKILL.md) — Query 阶段（§3 ### Query）。
- [wiki-maintenance](../skills/wiki-maintenance/SKILL.md) — Refresh / Deprecate 阶段（§3 ### Refresh / Deprecate）。
