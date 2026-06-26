# NotebookLM Skill Factory

> 将领域知识转化为 Claude Code 技能 —— NotebookLM 研究 → 结构化 SKILL.md 生成 → 自动验证流水线。

[English](README.md)

## 解决了什么问题

手写 SKILL.md 很痛苦：研究耗几小时，容易幻觉，迭代更慢。这个技能编排了一条 4 阶段流水线，把 NotebookLM 的「基于来源回答」能力和 Claude Code 的执行能力结合起来：

```
用户意图 → NotebookLM 来源摄入 → SKILL.md 提取 → 验证 → 测试 & 迭代
```

## 为什么这套方法有效

- **几乎不幻觉** —— NotebookLM 只基于你给的来源回答，不会自己编造
- **几分钟出活** —— 以前花一下午，现在几分钟出一个可用版本
- **结构化输出** —— 自动生成带正确 YAML frontmatter 的 SKILL.md
- **内建迭代闭环** —— 测试失败自动回灌 NotebookLM 修正

## 快速开始

### 前置条件

```bash
# 一次性设置
notebooklm login        # 浏览器弹出 Google OAuth 授权
```

### 用法

```
/帮我做一个高转化落地页文案的 skill
```

技能会自动：
1. 询问你提供来源材料（PDF、文章 URL、YouTube 链接）
2. 创建专用 NotebookLM notebook 并索引来源
3. 提取完整、通过验证的 SKILL.md
4. 测试并在需要时迭代优化

## 手动安装

```bash
# 复制到 skills 目录
cp -r notebooklm-skill-factory ~/.claude/skills/
```

或通过 ClawHub 安装：

```bash
clawhub install notebooklm-skill-factory
```

## 文件结构

```
├── SKILL.md                              # 技能主定义
├── scripts/
│   └── parse-skill-output.py             # 解析 NotebookLM JSON → SKILL.md
└── references/
    └── skill-extraction-prompt.md         # 提词模板
```

## 依赖

- [NotebookLM CLI](https://github.com/UseClawPro/notebooklm) — `notebooklm` 命令
- Python 3.10+（仅标准库，无需 pip 安装）
- Claude Code，需安装 `skill-creator` 和 `skill-vetter` 技能

## 工作原理

### 四阶段流水线

| 阶段 | 做什么 | 核心命令 |
|------|--------|---------|
| **1. 摄入** | 创建 notebook、添加来源、等待索引 | `notebooklm create` / `source add` / `source wait` |
| **2. 提取** | 用提词模板从来源提取结构化 SKILL.md | `notebooklm ask` → `parse-skill-output.py` |
| **3. 验证** | 写入 skills 目录、调 skill-creator 和 skill-vetter 审查 | `Skill(skill-creator)` / `Skill(skill-vetter)` |
| **4. 迭代** | 真实用例测试，失败反馈回灌 NotebookLM | `notebooklm ask` (修正) → 重写 → 再测 |

### 与已有技能的关系

- **`notebooklm`**：提供 NB CLI 能力（被本技能调用）
- **`skill-creator`**：提供 SKILL.md 验证（被本技能在阶段 3 调用）
- **`skill-vetter`**：提供安全审查（被本技能在阶段 3 调用）
- **本技能**：编排以上三者，串成完整自动化流水线

## 来源质量建议

- 一个 notebook 专注一个 skill，一个主题
- 3-10 个高质量来源 > 20 个杂乱的来源
- 官方文档 > 博客文章 > YouTube 转录
- 如果 skill 涉及多个不相关领域，分别创建 notebook
- 生成后务必人工过一遍 —— 人永远是最终把关者

## License

MIT — 详见 [LICENSE](LICENSE)
