---
name: smart-compact
description: "Smart context compaction for OpenClaw agents. 4-phase progressive strategy: Scan, Extract, Check, Compact. Before running /compact, this skill scans tool outputs, extracts valuable information into memory files, and generates a pre-compact checklist — ensuring nothing important is lost during compression. Triggers: smart-compact, 智能压缩, pre-compact, 压缩检查, compact check."
---

# Smart Compact — 智能压缩增强

四阶段渐进式压缩策略，在 /compact 前先把重要信息救出来。

## 什么时候用

- 用户说"智能压缩"、"smart-compact"、"压缩检查"
- 在手动执行 /compact 之前先跑一遍
- 对话上下文快满时，主动触发
- Heartbeat 检测到 context 接近 80% 时自动建议

## 核心理念

传统的上下文压缩是一刀切——整个对话被浓缩成一段摘要，大量细节在过程中丢失。

Smart Compact 采用**四阶段渐进式**策略，在 /compact 之前插入一个"预处理"阶段：

1. **扫描**：识别对话中的大块工具输出和关键信息
2. **提取**：把值得保留的信息写入记忆文件
3. **检查**：生成压缩前检查清单，标记风险项
4. **压缩**：用户确认安全后才执行压缩

核心原则：**先救再压**，宁可多存也不能漏存。

## 执行流程

### Phase 1 — 扫描工具输出

1. 回顾当前对话中所有的工具调用结果
2. 识别**大块输出**（超过 50 行或 2000 字符的工具结果）
3. 对每个大块输出评估：
   - 是否包含**关键信息**（决策、配置、错误信息、地址等）
   - 是否已经被后续对话**引用或总结过**
   - 是否是**重复或冗余**的（如多次 ls、git status）

### Phase 2 — 提取记忆

1. 从工具输出和对话中提取值得持久化的信息：
   - **新发现的事实**：地址、配置值、端点、文件路径
   - **决策和原因**：为什么选了方案 A 而不是 B
   - **错误和解决方案**：踩坑记录
   - **用户偏好**：明确表达的喜好或要求
   - **任务进度**：哪些做完了，哪些还没做

2. 将提取的信息**追加写入** `memory/YYYY-MM-DD.md`
   - 使用 `edit`（追加模式），绝不覆盖已有内容
   - 每条记忆附带简短的来源说明

### Phase 3 — 生成压缩前检查清单

输出一份结构化的检查清单：

```
📋 Smart Compact 检查清单
━━━━━━━━━━━━━━━━━━━━━━

📊 扫描统计：
- 工具调用总数：N 次
- 大块输出（>50行）：N 个
- 已引用/总结过的：N 个
- 可安全压缩的：N 个

💾 已提取到记忆：
- [+] 新事实：简要描述...
- [+] 决策记录：简要描述...
- [+] 错误解决：简要描述...
（共 N 条写入 memory/YYYY-MM-DD.md）

⚠️ 需要注意：
- [!] 某某工具输出包含重要数据但尚未被引用
- [!] 某某配置值只出现在工具输出中

✅ 建议：可以安全执行 /compact
```

### Phase 4 — 执行压缩（可选）

- 如果检查清单显示"✅ 可以安全压缩"，提示用户确认
- 用户确认后，执行 /compact
- 如果有 ⚠️ 警告项，先处理完再压缩

## 规则

### 必须遵守
- **绝不丢弃未被记录的关键信息**：宁可多存也不能漏存
- **追加写入**：只用 edit 追加到 memory 文件，绝不覆盖
- **不自动压缩**：除非用户明确确认，否则只生成检查清单
- **透明**：每一步操作都告知用户

### 信息分类标准
- **必须保存**：重要配置、地址端点、文件路径、错误解决方案
- **建议保存**：决策原因、用户偏好、任务进度
- **可以丢弃**：重复的 ls 输出、已被总结的搜索结果、中间调试过程

## 与 Dream Skill 的配合

Smart Compact 和 Dream 是互补的：
- **Smart Compact**：实时的，在压缩前抢救信息 → 写入日记
- **Dream**：定期的，把日记整合到长期记忆 → 更新 MEMORY.md

推荐工作流：
1. 对话中随时触发 Smart Compact 保护信息
2. 每天凌晨 Dream 整合日记到长期记忆
3. 形成完整的记忆保护链条
