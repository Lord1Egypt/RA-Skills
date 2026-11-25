# 阶段 4 规程 — Assemble 组装

目标：生成产物 `output/<skill_name>/SKILL.md`——Agent 加载该 skill 的唯一入口。

## frontmatter

```yaml
---
name: <skill_name>        # 必须与产物目录名完全一致，小写字母数字+连字符，≤64 字符
description: <按下方公式生成>
---
```

## description 公式

```
<领域定位一句话：这个 skill 覆盖什么>。Use when <trigger_scenarios（领域配置）>。
Triggers: <description_keywords 按优先级前置排列，逗号分隔>。
Covers <主框架及版本锚定，如 React 19 / Next.js 15>。
```

要求：
- 第三人称；关键词**前置**（加载器靠它们匹配触发）。
- 覆盖 ≥80% 的 `description_keywords`。
- 长度 ≤1024 字符。
- 「Use ONLY when...」收窄措辞仅当领域确实狭窄时使用。

## 正文骨架

```markdown
# <标题>

<一句话定位 + 何时用/不用>

## 知识库索引

| 文件 | 内容 | 何时读 |
|---|---|---|
| kb/laws.md | 全局宪法：跨领域不可违背原则（LAW-N 编号可引用） | **写代码前必读** |
| kb/react-core.md | ... | ... |
（全部 kb 文件，含横切文件；laws.md 置顶）

## 决策树（按问题类型找知识文件）

- 确认什么能做什么不能做 / 红线在哪 → `kb/laws.md`
- 状态管理 / hooks / 重渲染问题 → `kb/react-core.md`
- 路由 / RSC / 缓存 / hydration → `kb/nextjs.md`
- ...（覆盖全部 kb 文件）
- 先查 AI 典型错误再写代码 → `kb/ai-mistakes.md`

## Top 法则（不读 kb 也必须遵守的）

<从 laws.md 提炼 5~8 条最致命 LAW 条款，一句话版 + 编号>

## Top 坑点（不读 kb 也必须知道的）

<从 gotchas 提炼 5~10 条一句话版，高危红线>

## 回答规范

- 回答引用 kb 条目时保留来源标注（[官方文档]/[模型经验]/[推断]/[实战回流]）。
- 生成代码前先核对 `kb/laws.md` 的 LAW 条款与对应领域法则，逐条自检是否违反。
- 不确定时明说不确定，不编造 API；版本敏感结论注明所基于的版本。

## 知识回流

<触发条件：修复了 kb 未覆盖的 bug / 发现 kb 错误过时 / 官方大版本更新。
处理：按 kb-distiller 的 refine 规程向对应 kb 文件追加结构化条目，标注 [实战回流]，更新 version 与 updated。
路径提示：kb-distiller/prompts/refine.md>
```

## 自检

组装完成后核对：
1. frontmatter 可解析，name 与目录一致。
2. description 含全部（或 ≥80%）keywords。
3. 索引表与 kb/ 目录实际文件一一对应，无缺漏。
4. 决策树覆盖全部 kb 文件。
5. 目录内**有且仅有一个** SKILL.md。
