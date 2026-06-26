---
name: openclaw-doc-sync
description: |
  Post-release documentation sync skill that automatically aligns README/ARCHITECTURE/CONTRIBUTING/CLAUDE.md with actual changes, cleans up TODOs, polishes Changelog tone, and optionally updates version to improve delivery consistency.
  中文：发布后文档同步技能，自动对齐 README/ARCHITECTURE/CONTRIBUTING/CLAUDE.md 与实际变更，清理 TODO，优化 Changelog 语气，并可同步完成版本更新，提升交付一致性。
  日本語：リリース後のドキュメントを同期するスキル。README/ARCHITECTURE/CONTRIBUTING/CLAUDE.mdを実装差分に合わせて更新し、TODOを整理・削除、CHANGELOGの語調を最適化し、必要ならバージョン更新も実施。
  한국어：릴리스 후 문서를 동기화하는 에이전트. README/ARCHITECTURE/CONTRIBUTING/CLAUDE.md를 변경사항과 일치시키고 TODO를 정리, CHANGELOG 톤을 개선하며 필요 시 버전 업데이트까지 수행.
  Español：Sincroniza documentación post-lanzamiento: alinea README, ARCHITECTURE, CONTRIBUTING y CLAUDE.md con el diff real, limpia TODOs, mejora el tono del changelog y opcionalmente actualiza la versión.
---

# ClawLite Doc Sync — 发布后文档更新

你是运行 `/doc-sync` 工作流。这在代码提交后、PR 合并前运行。你的工作：确保项目中的每个文档文件准确、最新，并以友好、用户导向的语气撰写。

你大部分是自动化的。直接做明显的 factual 更新。只为有风险或主观的决定停止。

**只停止：**
- 有风险/可疑的文档更改（叙述、哲学、安全、删除、大型重写）
- VERSION 升级决定（如果还没升级）
- 要添加的新 TODOS 项目
- 跨文档矛盾（叙述性，而非事实性）

**永远不要停止：**
- 清楚来自 diff 的事实性更正
- 向表格/列表添加项目
- 更新路径、数量、版本号
- 修复过时的交叉引用
- CHANGELOG 语气优化（小幅措辞调整）
- 标记 TODOS 完成
- 跨文档事实性不一致（例如版本号不匹配）

---

## 阶段 1：预检与 Diff 分析

1. 检查当前分支。如果在 base 分支上，**中止**："你在 base 分支上。从功能分支运行。"

2. 收集关于更改的上下文：

```bash
git diff <base>...HEAD --stat
git log <base>..HEAD --oneline
git diff <base>...HEAD --name-only
```

3. 发现项目中所有文档文件：

```bash
find . -maxdepth 2 -name "*.md" -not -path "./.git/*" -not -path "./node_modules/*" | sort
```

4. 将更改分类为与文档相关的类别：
   - **新功能** — 新文件、新命令、新 skills、新能力
   - **更改行为** — 修改的服务、更新 API、配置更改
   - **删除功能** — 删除的文件、删除的命令
   - **基础设施** — 构建系统、测试基础设施、CI

输出："分析 N 个文件在 M 次提交中更改。发现 K 个文档文件需要审查。"

---

## 阶段 2：逐文件文档审计

读取每个文档文件并与 diff 交叉引用。使用这些通用启发式方法：

**README.md:**
- 它是否描述了 diff 中可见的所有功能和能力？
- 安装/设置说明是否与更改一致？
- 示例、演示和使用描述是否仍然有效？
- 故障排除步骤是否仍然准确？

**ARCHITECTURE.md:**
- ASCII 图表和组件描述是否与当前代码匹配？
- 设计决策和"为什么"解释是否仍然准确？
- 保守一点 — 只更新被 diff 清楚反驳的内容。架构文档描述不太可能频繁更改的内容。

**CONTRIBUTING.md — 新贡献者烟雾测试：**
- 就像全新的贡献者一样浏览设置说明。
- 列出的命令准确吗？每个步骤都会成功吗？
- 测试层级描述是否与当前测试基础设施匹配？
- 工作流描述（开发设置、贡献者模式等）是否最新？
- 标记任何会失败或让首次贡献者困惑的内容。

**CLAUDE.md / 项目说明：**
- 项目结构部分是否与实际文件树匹配？
- 列出的命令和脚本是否准确？
- 构建/测试说明是否与 package.json 中的匹配？

**任何其他 .md 文件：**
- 读取文件，确定其目的和受众。
- 与 diff 交叉引用，检查它是否与文件所说的矛盾。

对于每个文件，将需要的更新分类为：

- **自动更新** — 清楚由 diff 证明的事实性更正：向表格添加项目、更新文件路径、修复数量、更新项目结构树。
- **询问用户** — 叙述性更改、章节删除、安全模型更改、大型重写（一个章节中超过 ~10 行）、模糊相关性、添加全新章节。

---

## 阶段 3：应用自动更新

使用 Edit 工具直接做所有清楚的事实性更新。

对于每个修改的文件，输出一行摘要描述**具体更改了什么** — 不是"更新了 README.md"而是"README.md: 向 skills 表添加了 /new-skill，将 skill 数量从 9 更新到 10。"

**永远不要自动更新：**
- README 介绍或项目定位
- ARCHITECTURE 哲学或设计理念
- 安全模型描述
- 不要从任何文档中删除整个章节

---

## 阶段 4：询问有风险/可疑的更改

对于阶段 2 中识别的每个有风险或可疑的更新，使用 AskUserQuestion：
- 上下文：项目名称、分支、哪个文档文件、我们正在审查什么
- 具体的文档决定
- `RECOMMENDATION: 选择 [X] 因为 [一行原因]`
- 选项包括 C) 跳过 — 保持原样

在每个答案后立即应用批准的更改。

---

## 阶段 5：CHANGELOG 语气优化

**关键 — 永远不要覆盖 CHANGELOG 条目。**

此步骤优化语气。它不会重写、替换或重新生成 CHANGELOG 内容。

**规则：**
1. 首先读取整个 CHANGELOG.md。了解已经存在的内容。
2. 只修改现有条目中的措辞。永不删除、重新排序或替换条目。
3. 永远不从零重新生成 CHANGELOG 条目。条目由 `/ship` 根据实际 diff 和提交历史编写。它是真相来源。你在优化散文，不是重写历史。
4. 如果条目看起来错误或不完整，使用 AskUserQuestion — 不要静默修复。
5. 使用 Edit 工具和精确的 `old_string` 匹配 — 永远不要使用 Write 覆盖 CHANGELOG.md。

**如果此分支中 CHANGELOG 未修改：** 跳过此步骤。

**如果此分支中 CHANGELOG 已修改**，审查条目的语气：

- **销售测试：** 用户阅读每个要点会想"哦不错，我想试试那个"吗？如果不是，重写措辞（不是内容）。
- 以用户现在能**做的**领先 — 不是实现细节。
- "你现在可以..."不是"重构了..."
- 标记并重写任何像提交消息一样读的条目。
- 内部/贡献者更改属于单独的"### For contributors"小节。
- 自动修复小的语气调整。如果重写会改变含义，使用 AskUserQuestion。

---

## 阶段 6：跨文档一致性与可发现性检查

在逐个审计每个文件后，进行跨文档一致性检查：

1. README 的功能/能力列表是否与 CLAUDE.md 描述的匹配？
2. ARCHITECTURE 的组件列表是否与 CONTRIBUTING 的项目结构描述匹配？
3. CHANGELOG 的最新版本是否与 VERSION 文件匹配？
4. **可发现性：** 每个文档文件是否可从 README.md 或 CLAUDE.md 到达？如果 ARCHITECTURE.md 存在但 README 和 CLAUDE.md 都不链接到它，标记它。每个文档应该从两个入口文件之一可发现。
5. 标记文档之间的任何矛盾。自动修复清楚的事实性不一致（例如版本不匹配）。对叙述性矛盾使用 AskUserQuestion。

---

## 阶段 7：TODOS.md 清理

1. **尚未标记的已完成项目：** 将 open TODO 项目与 diff 交叉引用。如果 TODO 清楚由此分支的更改完成，将其移至 Completed 部分，格式为 `**Completed:** vX.Y.Z.W (YYYY-MM-DD)`。保守一点 — 只标记 diff 中有清楚证据的项目。

2. **需要描述更新的项目：** 如果 TODO 引用的文件或组件被显著更改，其描述可能过时。使用 AskUserQuestion 确认 TODO 是否应该更新、完成或保持原样。

3. **新的延迟工作：** 检查 diff 中的 `TODO`、`FIXME`、`HACK` 和 `XXX` 注释。对于每个代表有意义的延迟工作的（不是微不足道的内联注释），使用 AskUserQuestion 询问是否应该捕获到 TODOS.md。

---

## 阶段 8：VERSION 升级问题

**关键 — 永远不要不询问就升级 VERSION。**

1. **如果 VERSION 不存在：** 静默跳过。

2. 检查此分支上 VERSION 是否已经修改：

```bash
git diff <base>...HEAD -- VERSION
```

3. **如果 VERSION 未升级：** 使用 AskUserQuestion：
   - RECOMMENDATION: 选择 C（跳过）因为纯文档更改很少需要版本升级
   - A) 升级 PATCH (X.Y.Z+1) — 如果文档更改与代码更改一起发布
   - B) 升级 MINOR (X.Y+1.0) — 如果这是重要的独立发布
   - C) 跳过 — 不需要版本升级

4. **如果 VERSION 已经升级：** 不要静默跳过。相反，检查升级是否仍然覆盖此分支的更改范围：
   a. 读取当前 VERSION 的 CHANGELOG 条目。它描述了什么功能？
   b. 读取完整 diff。是否有未在当前 VERSION 的 CHANGELOG 条目中提及的重大更改（新功能、新 skills、新命令、主要重构）？
   c. **如果 CHANGELOG 条目涵盖一切：** 跳过 — 输出 "VERSION: 已经升级到 vX.Y.Z，涵盖所有更改。"
   d. **如果有重大未覆盖更改：** 使用 AskUserQuestion 解释当前版本涵盖什么 vs 什么是新的，并询问：
      - RECOMMENDATION: 选择 A 因为新更改值得自己的版本
      - A) 升级到下一个 patch (X.Y.Z+1) — 给新更改自己的版本
      - B) 保持当前版本 — 将新更改添加到现有 CHANGELOG 条目
      - C) 跳过 — 保持原样，稍后处理

---

## 阶段 9：提交与输出

**首先空检查：** 运行 `git status`。如果之前的阶段没有修改任何文档文件，输出"所有文档都是最新的。"然后退出而不提交。

**提交：**

1. 按名称暂存修改的文档文件（永远不要 `git add -A` 或 `git add .`）。
2. 创建单个提交：

```bash
git add README.md ARCHITECTURE.md CONTRIBUTING.md CLAUDE.md CHANGELOG.md TODOS.md
git commit -m "docs: sync documentation with shipped changes"
```

3. 输出总结：
   - 修改了哪些文件
   - 每个文件的具体更改
   - 任何需要用户注意的后续步骤

---

## 完成状态

- **DONE** — 所有文档已同步，提交已创建
- **DONE_WITH_CONCERNS** — 完成但有用户应该知道的问题
- **BLOCKED** — 无法继续，说明阻塞了什么
- **NEEDS_CONTEXT** — 缺少继续所需的上下文
