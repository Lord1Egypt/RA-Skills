# OpenClaw vs Codex Skill Creator

> 记录了打包的 Codex skill-creator（`/app/skills/skill-creator/`）与新的 OpenClaw 原生 skill-creator 之间的差异。在创建新的 OpenClaw 技能或移植现有 Codex 技能时，请参考此文档。

## 架构差异

| | Codex（CLI 编码代理） | OpenClaw（多代理） |
|---|---|---|
| 执行 | 单个 CLI 会话 | 主代理 + sub-agent（spawn/fork） |
| 上下文 | 所有上下文存在于会话内 | sub-agent 以**空**上下文启动 |
| 技能加载 | description → body → scripts（顺序） | description（始终） → body（触发时） → references（按需） |
| 技能存储 | 单一位置 | workspace（重启间保持）vs bundled（更新时重置） |
| 提示注入 | 不需要（单一上下文） | **必需**（显式注入到 sub-agent） |
| 打包 | `package_skill.py` 创建 `.skill` 文件 | 不需要打包 — 直接识别文件夹结构 |

## 5 个关键差异

### 1. Sub-Agent 上下文注入

**Codex**：所有工作在一个会话中进行，上下文共享是自然的。

**OpenClaw**：当你 spawn 一个 sub-agent 时，它的上下文是**空的**。主代理必须将 Phase 0 中收集的信息显式注入到 sub-agent 的提示中。

Codex 技能没有这个概念。在 OpenClaw 中，这是最重要的模式。

```
Codex:   "总结这段文本" → OK（上下文已存在）
OpenClaw: "总结这段文本" → FAIL（sub-agent 没有上下文）

OpenClaw 正确方法：
"这段文本是《OOO 用户手册》的第 1-5 节。
完整文档共 5 个部分 27 个小节。此片段涵盖'新设计方法'。
请保留以下内容：[类比]、[引文]、[案例研究]..."
```

### 2. Style Guide 优先

**Codex**："简洁是关键" — 专注于节省上下文窗口。假设代理已经足够聪明。

**OpenClaw**：没有 Style Guide，sub-agent 会变成"文本压缩器"。**判断标准**是必需的。

Codex 技能专注于格式（结构、长度），但 OpenClaw 技能还必须包含判断标准（保留什么、使用什么语气、从什么角度）。

### 3. Phase 0（分析阶段）必需

**Codex**：代理在工作中自然进行分析。

**OpenClaw**：需要主代理在 Phase 0 中分析，然后将结果注入 sub-agent 提示的流水线。

没有 Phase 0 时：
- 每个片段独立处理（整体流程丢失）
- 片段间出现重复内容
- 作者的声音（类比、引文）被丢弃

### 4. 顺序流水线

**Codex**：可以并行生成多个输出，代理自然合并。

**OpenClaw**：复杂输出应从简单到复杂顺序展开。

示例：摘要深度 1x + 5x
- Codex：可以并行生成（代理合并）
- OpenClaw：1x → 5x 顺序（1x 结构作为 5x 的骨架）

### 5. 不需要打包

**Codex**：`package_skill.py` 创建 `.skill` 文件（本质上是 zip）用于分发。

**OpenClaw**：直接识别文件夹结构。技能只需要 `SKILL.md` 就能工作。

不需要打包脚本、验证脚本或 init 脚本。

## 移植清单：Codex 技能 → OpenClaw 技能

将 Codex 技能移植到 OpenClaw 时：

- [ ] **检查是否需要 sub-agent** — 如果技能进行分块或并行处理，确认 Phase 0 + 上下文注入模式是否存在
- [ ] **Style Guide 是否存在？** — 如果没有，请添加。仅靠格式规范不足以让 sub-agent 产生高质量输出
- [ ] **添加 Phase 0** — 工作开始前是否有分析阶段？
- [ ] **带有 `[ ]` 占位符的提示模板** — 确认占位符被 Phase 0 结果填充
- [ ] **合并指令** — 明确防止多片段输出的简单拼接
- [ ] **移除 `package_skill.py` 引用** — OpenClaw 中不需要
- [ ] **移除 `init_skill.py` 引用** — OpenClaw 中不需要
- [ ] **description 中包含触发关键词** — 同时包含英文和本地化关键词
- [ ] **将"使用时机"从 body 移到 description** — OpenClaw 只在触发后才加载 body

## 从 Codex 保留的模式

以下是在两种环境中都能良好工作的优秀模式：

1. **Progressive Disclosure** — 保持 SKILL.md 在 500 行以下，将细节移到 references/
2. **"简洁是关键"原则** — 不要重新解释代理已经知道的内容
3. **自由度调整** — 根据任务的脆弱性（高/中/低）调整具体程度
4. **单层引用深度** — 不要在 references/ 内引用其他 references/
5. **使用后改进** — 使用技能，观察失败，修复，重复
