# llm-wiki

> 把 LLM 变成你的专属知识库管理员——不是问答，是编译。

基于 [Andrej Karpathy 的 LLM Wiki 理念](https://x.com/karpathy/status/1793562750870294638)构建的 Claude Skill。让 LLM 把你读过的一切编译成持久增长的结构化知识库，而不是每次查询都从零推导。

---

## 核心理念

**RAG vs Wiki 的本质区别：**

| | RAG | LLM Wiki |
|---|---|---|
| 工作方式 | 每次查询重新检索推导 | 编译一次，持续积累 |
| 知识状态 | 无状态 | 有状态，持续复利 |
| 矛盾处理 | 静默混合 | 显式标注，保留两方 |
| 交叉引用 | 无 | 自动维护 wikilink |

原始资料是不可变的真相来源，LLM 负责编译——摘要、交叉引用、标注矛盾、综合洞见。你负责提供资料和提问，LLM 负责其余一切。

---

## 目录结构

```
your-wiki-project/
├── schema.md       ← Wiki 结构规则（LLM 的"宪法"）
├── purpose.md      ← 项目目标与范围
├── raw/            ← 原始资料（只读，永不修改）
│   ├── article1.md
│   └── notes.pdf
└── wiki/           ← LLM 编写并维护的知识页面
    ├── index.md
    ├── log.md
    ├── overview.md
    ├── concepts/
    ├── entities/
    ├── sources/
    └── synthesis/
```

---

## 四种操作模式

### 🏗️ INIT — 初始化

首次建立知识库。回答几个问题后，自动生成 `schema.md`、`purpose.md`、`wiki/index.md`、`wiki/log.md`、`wiki/overview.md`。

支持五种预设场景，各有专属子目录结构：

| 场景 | 适用 | 专属目录 |
|------|------|---------|
| 🔬 研究调研 | 论文、田野调查 | methodology / findings / thesis |
| 📚 阅读积累 | 读书笔记、书评 | characters / themes / chapters |
| 🌱 个人成长 | 习惯、目标、反思 | goals / habits / reflections |
| 💼 商业/团队 | 会议、决策、项目 | meetings / decisions / projects |
| 📄 通用 | 什么都行 | — |

### 📥 INGEST — 摄入

把新资料"编译"进 wiki。LLM 会：
1. 先告知你将更新哪些页面、是否发现矛盾
2. 新建或整合 wiki 页面（不覆盖，整合）
3. 保留原始数字、百分比、故事线、贡献者原话
4. 维护双向 `[[Wikilink]]`
5. 汇报变更摘要

一次摄入通常涉及 5–15 个 wiki 页面。

### 🔍 QUERY — 查询

基于 wiki 回答问题。LLM 先读 `index.md` 定位页面，再读相关页面作答，引用原始数据和案例。好的分析可选择保存为新 wiki 页面。

### 🩺 LINT — 健康检查

扫描 wiki 健康状态，报告：
- 孤立页面（无入链）
- 缺失页面（被引用但不存在）
- 矛盾内容
- 未索引页面
- 缺失 frontmatter

所有发现先展示，用户确认后再处理。

---

## 安装

**前置依赖：** `/obsidian` skill（用于写入 Obsidian Vault）

### Claude.ai / ClawhHub

1. 下载 `llm-wiki.skill`
2. 在 Claude.ai 设置 → Skills 中安装
3. 确保已安装 `/obsidian` skill
4. 对话中说"初始化我的 wiki"即可开始

### 手动安装

```
your-skills/
└── llm-wiki/
    ├── SKILL.md
    └── references/
        ├── templates.md
        └── ingest-logic.md
```

---

## 使用示例

```
用户：帮我初始化一个研究调研 wiki，主题是"大语言模型推理能力"

Claude：好的，请回答以下几个问题：
        1. 使用场景：A 研究调研 ✓
        2. 主题领域：大语言模型推理能力
        ...

用户：把这篇论文加进 wiki → [附上 paper.pdf]

Claude：读完了，发现以下内容：
        - 新实体：Chain-of-Thought（需新建页面）
        - 更新页面：scaling-laws.md（有新数据）
        - ⚠️ 矛盾：与 wei-2022 在 few-shot 结论上不一致
        确认后开始写入？

用户：wiki 里关于 few-shot 的内容有哪些？

Claude：根据 index.md，相关页面有 3 个……（引用原始数据作答）
        要把这个分析保存为 wiki 页面吗？
```

---

## 设计原则

- **原始资料永不修改**：`raw/` 是只读的真相来源
- **矛盾优于干净**：发现冲突就标注，不擅自裁决
- **编译前先告知**：摄入前汇报计划，摄入后汇报变更
- **Obsidian 兼容**：wikilink 只在正文 `## Related` section 中使用，不放 YAML frontmatter
- **语言跟随资料**：中文资料生成中文页面，英文资料生成英文页面

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `SKILL.md` | Skill 主体，定义四种操作模式 |
| `references/templates.md` | 五种场景的 schema + purpose 完整模板 |
| `references/ingest-logic.md` | 摄入两步流程（分析→生成）详解，供高级定制 |

---

## 致谢

理念来源：[Andrej Karpathy — "LLMs as a new kind of memory"](https://x.com/karpathy/status/1793562750870294638)
