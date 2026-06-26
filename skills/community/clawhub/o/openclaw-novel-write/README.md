# Novel Write - OpenClaw 小说创作助手

<<<<<<< HEAD
> **版本：0.1.0** | 基于 [novel-writer-skills](https://github.com/wordflowlab/novel-writer-skills) 改编
=======
> **版本：0.1.2** | 基于 [novel-writer-skills](https://github.com/wordflowlab/novel-writer-skills) 改编
>>>>>>> 3a77ccf (chore: 版本更新至0.1.2)

---

## 核心能力

| 能力 | 说明 |
|------|------|
| 七步方法论 | 从宪法到写作的完整创作流程 |
| 六阶段写作 | 预写分析 → 初稿 → 自检 → 润色 → 修订 → 元数据 |
| 伏笔回收检查 | 每章强制检查伏笔是否正常揭晓 |
| 记忆系统 | .learnings/ 记录中途灵感，确保设定不丢失 |
| Mermaid 情节图 | 自动生成人物关系图/战斗图/势力图 |
| 失败记录 | fail-log 持续积累问题，持续优化 |
| 五视角读者反馈 | Target/Casual/Expert/Critic/Editor 五视角评估 |
| 反AI检测 | 内置自然化写作规范，避免AI味 |
| 追踪系统 | 角色状态、情节进度、线索管理 |

---

## 触发命令

**方式一**：直接使用命令
```
/novel init 项目名
/novel constitution
...
```

**方式二**：用中文描述意图（AI 自动识别）

| 命令 | 触发关键词示例 |
|------|--------------|
| `/novel init [项目名]` | "创建新小说项目"、"初始化项目" |
| `/novel constitution` | "制定创作宪法"、"开始写宪法" |
| `/novel specify` | "定义故事规格"、"开始specify" |
| `/novel clarify` | "澄清关键决策"、"clarify" |
| `/novel plan` | "制定创作计划"、"生成章节大纲" |
| `/novel timeline` | "生成时间线"、"创建时间线文档" |
| `/novel track-init` | "初始化追踪系统" |
| `/novel tasks` | "分解任务清单"、"生成写作任务" |
| `/novel write [章节]` | "写第X章"、"开始第一章"、"继续写" |
| `/novel track --check` | "追踪验证"、"检查状态" |
| `/novel analyze` | "质量分析"、"分析章节" |
| `/novel learnings` | "记忆系统"、"记录设定"、"更新记忆" |
| `/novel diagram` | "生成关系图"、"生成战斗图"、"势力图" |
| `/novel fail-log` | "失败记录"、"查看问题" |
| `/novel feedback` | "读者视角反馈"、"生成反馈报告" |

---

## 七步创作流程

### 第一步：初始化项目

```
/novel init 项目名
```

**触发示例**：
```
用户: 帮我创建一个新小说项目，名字叫"都市神医"
```

自动创建项目目录结构和追踪文件。

---

### 第二步：创建宪法 + 风格设置

```
/novel constitution
```

**触发示例**：
```
用户: 我想写一个都市甜宠文，男主是霸总
```

**流程**：
1. 描述你的写作风格偏好
2. AI 分析并推荐预设风格（自然人声/网文爽文/文学质感/古风典雅/极简白描）
3. 确认或修改推荐结果

---

### 第三步：定义故事规格

```
/novel specify
```

**触发示例**：
```
用户: 继续描述故事，男主是豪门总裁，女主是普通上班族
```

**流程**：
1. 自由描述你的故事想法（题材、类型、主角、冲突等）
2. AI 自动分析并加载对应知识库（genres/styles/requirements）
3. 确认或修改分析结果

---

### 第四步：澄清关键决策

```
/novel clarify
```

**触发示例**：
```
用户: 好的，继续下一步
```

**流程**：回答 5 个关键问题，确保创作方向清晰。

---

### 第五步：制定创作计划

```
/novel plan
```

**触发示例**：
```
用户: 开始制定计划
```

生成章节架构、线索分布、伏笔设计、节奏规划。

---

### 第六步：生成时间线

```
/novel timeline
```

**触发示例**：
```
用户: 开始生成时间线
```

**流程**：
1. 从创作计划中提取所有事件
2. 按真实时间顺序排列，生成 `timeline.md`
3. 与创作计划互相校验（关键情节点必须在时间线中，时间线事件必须在计划中能找到）
4. 校验通过后保存

**时间线文档格式**：
```markdown
| 序号 | 时间点 | 事件 | 章节对应 | 重要程度 |
|------|--------|------|---------|---------|
| 001 | 第1年3月 | 主角出生 | 序章 | ⭐⭐⭐ |
| 002 | 第1年7月 | 主角离家 | 第1章 | ⭐⭐⭐ |
```

**校验失败**：
```
❌ 时间线与创作计划不一致
问题类型：[冲突类型]
请修复后再继续。
```

---

### 第七步：初始化追踪系统

```
/novel track-init
```

**触发示例**：
```
用户: 开始分解任务
```

根据计划填充角色状态、关系网络、情节追踪。

---

### 第八步：生成任务清单

```
/novel tasks
```

**触发示例**：
```
用户: 开始分解任务
```

按卷分拆任务，细化到每章节，含字数要求。

**输出结构**：
```
stories/<项目>/
├── tasks.md              # 总纲（索引 + 统计）
├── tasks-volume-1.md    # 第1卷详细任务
├── tasks-volume-2.md    # 第2卷详细任务
└── ...
```

---

### 开始写作

```
/novel write 第1章
```

**触发示例**：
```
用户: 开始写第一章
```

**⚠️ 前置检查（自动执行，强制）**：

| 步骤 | 命令 | 产出文件 | 检查 |
|------|------|---------|------|
| 1 | `/novel init` | 项目目录 | ✅ |
| 2 | `/novel constitution` | `memory/constitution.md` | ✅ |
| 3 | `/novel specify` | `stories/*/specification.md` | ✅ |
| 4 | `/novel clarify` | `stories/*/clarify-answers.md` | ✅ |
| 5 | `/novel plan` | `stories/*/creative-plan.md` | ✅ |
| 6 | `/novel timeline` | `stories/*/timeline.md` | ✅ |
| 7 | `/novel track-init` | `spec/tracking/*.json` | ✅ |
| 8 | `/novel tasks` | `stories/*/tasks.md` + `tasks-volume-*.md` | ✅ |

如果任何检查项未通过，`/novel write` 会报错并提示缺少哪一步。

**写作后强制检查（阻断型）**：
- 每次完成 → `/novel track --check` 追踪验证 + 伏笔回收检查（失败 → 阻断）
- 每 5 章完成 → 提醒用户执行 `/novel analyze`（失败 → 阻断）

---

## 完整对话示例

```
用户: 帮我创建一个新小说项目，名字叫"都市神医"
      → 触发 /novel init
      → AI: 项目已创建，目录结构如下...
      → AI: 请描述你的写作风格偏好

用户: 我想写一个都市甜宠文，男主是霸总
      → 触发 /novel constitution
      → AI 分析推荐：网文爽文 + romance-sweet
      → AI: 推荐风格为"网文爽文"，是否确认？
      
用户: OK确认了
      → 宪法生成完成
      
用户: 继续描述故事，男主是豪门总裁，女主是普通上班族
      → 触发 /novel specify
      → AI 分析：都市言情 × 豪门 + 甜宠
      → AI: 已加载 romance.md + web-novel.md + romance-sweet.md
      → AI: 是否确认以上分析结果？

用户: 没问题
      → 规格文档生成完成
      
用户: 好的，继续下一步
      → 触发 /novel clarify
      → AI 提出5个关键问题
      → 用户逐一回答
      
用户: 开始制定计划
      → 触发 /novel plan
      → AI 生成：章节架构、线索分布、伏笔设计、节奏规划

用户: 生成时间线
      → 触发 /novel timeline
      → AI 生成：时间线文档 + 与计划互相校验
      → 校验通过

用户: 开始初始化追踪系统
      → 触发 /novel track-init
      → AI 初始化追踪系统

用户: 开始分解任务
      → 触发 /novel tasks
      → AI 生成任务清单（tasks.md 总纲 + tasks-volume-*.md 分卷）

用户: 开始写第一章
      → 触发 /novel write
      → ⚠️ 前置检查（前8步）→ 全部通过
      → 📋 阶段1 预写分析（时间点/角色/伏笔/前文摘要）
      → ✏️  阶段2 初稿生成
      → 🔍 阶段3 自检（时间线/伏笔/角色一致性）
      → ✨ 阶段4 文笔润色（反AI检测）
      → 🔎 阶段5 修订（节奏/对话/冗余）
      → 📦 阶段6 元数据输出（更新tracking）
      → 完成后自动 /novel track --check（伏笔回收检查）
      → AI: ✅ 章节写作完成，字数 3,256 字

用户: 继续写第5章
      → 触发 /novel write
      → ⚠️ 前置检查 → 通过
      → AI 开始写作
      → 每5章提醒 → 用户触发 /novel analyze
      → AI: ✅ 质量分析完成
```

---

## 命令一览

| 命令 | 说明 |
|------|------|
| `/novel init [项目名]` | 初始化项目 |
| `/novel constitution` | 创建宪法 + 风格设置 |
| `/novel specify` | 定义故事规格 |
| `/novel clarify` | 澄清关键决策 |
| `/novel plan` | 制定创作计划 |
| `/novel track-init` | 初始化追踪系统 |
| `/novel tasks` | 生成任务清单 |
| `/novel write [章节]` | 执行写作（6阶段流程） |
| `/novel track --check` | 追踪验证 + 伏笔回收检查 |
| `/novel analyze` | 质量分析 |
| `/novel learnings` | 记忆系统 |
| `/novel diagram` | Mermaid 情节图解 |
| `/novel fail-log` | 失败记录 |
| `/novel feedback` | 五视角读者反馈 |

---

## 安装

```bash
clawhub install openclaw-novel-write
```

---

## 致谢

本 Skill 基于 [wordflowlab/novel-writer-skills](https://github.com/wordflowlab/novel-writer-skills) 改编。
