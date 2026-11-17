# 周度反思（第六步详细说明）

> 仅周五执行。合并原「每日反思 Nevo v2」cron 的全部能力。
> 路径以 OpenClaw 为主，Claude Code 环境下脚本自动降级。

## 6a. 错误扫描

回顾本周全部日记（`memory/YYYY-MM-DD.md`，从上周六到本周五），提取：

- **重复错误**：同一 Pattern-Key 在本周出现 ≥2 次
- **新错误**：首次出现的错误记录到 `.learnings/ERRORS.md`
- **已修复验证**：上周提出的修复方案，本周是否还复发？复发→升级优先级

输出格式：
```
### 本周错误扫描（YYYY-MM-DD 周五）
- 🔴 重复错误 N 条（列出 Pattern-Key + 出现次数）
- 🟡 新错误 N 条（已录入 ERRORS.md）
- ✅ 已验证修复 N 条
```

## 6b. 生成 Narrative

写入 `memory/narratives/YYYY-MM-DD.md`，按 (WHERE×WHY) 病理键结构化（v3.0）：

```markdown
# Week Narrative — YYYY-MM-DD

## 本周关键事件
按时间线列出重要决策和操作

## 病理矩阵（WHERE × WHY）
| WHERE | WHY | 条目数 | Pattern-Key | 严重度 |
|-------|-----|--------|-------------|--------|
| mcp_call | token_expired | 3 | mcp.token_expired | high |
| file_write | timing_race | 1 | file.race | medium |

## 意图 → 决策 → 结果
每个关键事件的因果链

## 教训
从错误和成功中提炼的认知

## 原子事实
本周新获得的确定性知识点（可直接引用）
```

## 6c. 规则提议

从重复错误中提炼行为规则：

- **触发条件**：同一错误模式出现 ≥2 次（本周内或跨周累计）
- **规则格式**：
  ```
  #### 规则提议 [类型]-NNN: 规则名称
  - **触发**：什么情况下执行
  - **执行**：具体做什么
  - **验证**：怎么确认规则生效
  - **来源**：ERR-XXXXXXXX-XXX × N 次
  - **病理键**：WHERE=xxx, WHY=xxx
  ```
- **类型**：`BEHAV`（行为）、`OPS`（运维）、`TOOL`（工具）、`FLOW`（流程）
- **提议后**：写入当周 Narrative 文件，待木老师确认后提升到 MEMORY.md

## 反思通知

反思完成后在进化摘要中追加反思结果：
```
📊 本周反思：
- 错误扫描：重复 N / 新增 N / 已修 N
- Narrative：已写入 memory/narratives/YYYY-MM-DD.md
- 规则提议：N 条（简述）
```

## 6d. MEMORY.md 蒸馏

目标：保持 `MEMORY.md` ≤ 80 行，确保长期记忆精炼有效。

步骤：
1. 读取本周日记，识别值得沉淀到 MEMORY.md 的新决策/偏好/教训
2. 追加新条目到 MEMORY.md 对应分区
3. 检查是否超过 80 行：
   - 超过 → 识别已过时/被覆盖的旧条目，移入 `## 已归档` 区域（不直接删除）
   - 未超 → 跳过
4. 用户画像、重要决策、硬规则优先保留，细节性记忆优先归档

## 6e. 归档旧日志

目标：保持 `memory/` 和 `memory/narratives/` 目录整洁。

步骤：
1. 扫描 `memory/YYYY-MM-DD.md` 和 `memory/narratives/YYYY-*.md` 文件
2. 找出日期超过 30 天的
3. 移动到 `memory/archive/`（目录不存在则创建）
4. 保留原文件名，不删除、不合并内容
5. 输出归档数量

```
🗜️ 记忆蒸馏：
- MEMORY.md：当前 X 行（新增 N 条 / 归档 N 条）
- 旧日志归档：N 个文件移至 archive/
```

## 6f. 评分+衰减淘汰（v3.0 替代行数硬截断）

目标：用评分+衰减淘汰替代粗暴的行数截断，保留高价值条目，淘汰低分老旧条目。

### 执行顺序

1. **评委偏差审计**（先行，验证淘汰机制可信度）
   ```bash
   python3 scripts/bias_audit.py
   ```
   - 审计未通过 → 停止淘汰操作，报告木老师需校准阈值
   - 审计通过 → 继续下一步

2. **运行淘汰评分**（脚本自动检测环境，无需指定路径）
   ```bash
   # 默认处理 LEARNINGS.md（自动检测 OpenClaw/Claude Code 路径）
   python3 scripts/eviction_score.py
   # 如需单独处理 ERRORS.md
   python3 scripts/eviction_score.py .learnings/ERRORS.md
   ```

3. **按脚本建议执行归档**
   - 脚本输出按 effective_score 排序的条目列表，标注"保留/归档"
   - Agent 按建议执行归档操作（read → write 覆写）

4. **归档操作**
   - promoted → 移至 `.learnings/archive/promoted-YYYY.md`
   - resolved+旧 → 移至 `.learnings/archive/resolved-YYYY.md`
   - dormant → 移至 `.learnings/archive/dormant-YYYY.md`
   - errors resolved → 移至 `.learnings/archive/errors-resolved-YYYY.md`

### 淘汰公式

```
effective_score = VFM × 0.5^(days_since_last_seen / 30)
```

| 状态 | 条件 | 处理 |
|------|------|------|
| promoted | 状态=promoted | 移出至永久记忆 |
| resolved+旧 | 状态=resolved 且 >30天 | 移至 archive |
| 高复现豁免 | Recurrence≥2 | **保留**（不论分数和年龄） |
| 仅1次+旧 | Recurrence=1 且 >14天 | 标记 dormant |
| 低分+旧 | effective<25 且 >14天 | 移至 archive |
| 正常 | effective≥25 或 <14天 | 保留 |

> 被检索命中（grep 匹配到）时，Agent 更新 Last-Seen → 衰减重置

### 通知格式

```
🪶 淘汰评分：
- LEARNINGS: X条 → 保留N / 归档N / 当前行数X
- ERRORS: X条 → 保留N / 归档N / 当前行数X
- 偏差审计: PASS
- 评分公式: effective = VFM × 0.5^(age/30), 阈值=25, 半衰期=30天
```

---

## 6g. 条目聚类扫描 + 主动Skill合成（v3.0）

目标：识别可合成新 Skill 的条目群，从被动等待 See Also 关联变为主动发现能力聚类并生成 Skill 草案。

### 执行步骤

1. **扫描本周条目** — 读取 LEARNINGS.md 全部活跃条目的领域+摘要+WHERE+WHY+标签
2. **语义聚类** — 按领域和病理类型(WHERE×WHY)自动分组：
   - 同一领域的条目归为一组
   - 同一病理键（WHERE=mcp_call, WHY=token_expired）的条目归为一组
   - 解决同一类问题的条目归为一组
3. **筛选有效聚类** — 每个聚类≥3条 → 值得进一步评估；<3条 → 跳过
4. **生成 Skill 草案** — 对有效聚类输出（不再只是建议，而是草案）：
   ```
   🔍 Skill 提取草案：
   - 聚类名：XX能力
   - 关联条目：LRN-001, LRN-002, ERR-003
   - 病理键：WHERE=mcp_call, WHY=token_expired
   - 建议 Skill 名：mu-xxx
   - Skill 草案骨架：
     ---
     name: mu-xxx
     description: "一句话描述"
     ---
     # mu-xxx · 能力描述
     ## 触发词
     ## 执行步骤
     ## 脚本（如有）
   - 理由：N条条目均指向同一能力缺口
   ```
5. **联动检查** — 检查聚类中是否有 candidate 状态的条目（未通过VFM验算的规则），若同一聚类的多条 candidate 互相印证 → 提升其置信度
6. **报告木老师确认** — 列出所有草案，木老师确认后才走 mu-dev-workflow 创建

### 通知格式

```
🔬 条目聚类扫描 + Skill合成：
- 扫描条目：N 条
- 发现聚类：N 个（≥3条）
- Skill 草案：N 份（详见摘要）
- candidate联动：N 条 candidate 升级为 promoted
```
