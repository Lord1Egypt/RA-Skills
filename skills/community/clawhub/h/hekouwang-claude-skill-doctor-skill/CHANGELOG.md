# Changelog

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.1.0] - 2026-06-24

接入外部安全扫描、消化业界 skill 写作最佳实践，扩展体检维度。

### Added
- **工作流新增步骤 2b · 深度安全扫描（可选）**：叠加 [NVIDIA SkillSpector](https://github.com/NVIDIA/skillspector)，
  覆盖提示注入 / 数据外泄 / 隐藏指令 / 供应链 / 过度授权 / MCP 越权等 68 类模式，
  补 `check.py` #0 密钥正则之外的深度安全维。含实战铁律：**只扫逻辑文件、别扫 assets**
  （直接扫会把字体/图片二进制当代码，刷出几十条假 `TM1 Tool Parameter Abuse`）；
  低可信度（<30%）`Hidden Instructions` 多是中文/零宽字符误报，人工复核。
- **评分维度 #8 触发方式匹配（model vs user invoked）**：只靠人手敲名字触发的 skill
  应设 `disable-model-invocation: true`，省掉每轮 `description` 的 context load。
- **`references/skill-writing-vocab.md`**：消化 mattpocock/skills 的 *writing-great-skills*，
  把"好 skill"的判据沉淀成可命名的诊断词汇——两种载荷（context/cognitive load）、
  信息阶梯、branch 拆分测试、完成判据（防 premature completion）、no-op 测试、
  sediment/sprawl/duplication 失败模式、leading word。出报告时用这些词点破问题。

### Changed
- **#10a 锐化为 no-op 测试**：判据明确为「这段相对模型默认行为改变了什么？没有就删」，
  比原先"别替模型补它已经会的"更可操作。

## [1.0.2] - 2026-06-22

实战体检三个品牌 skill 时暴露的机检缺陷修复（dogfooding）：

### Fixed
- **#7 allowed-tools 兼容逗号字符串**：原先只认 YAML 列表（`- a` / `[a,b]`），
  把官方 frontmatter 标准的逗号字符串写法（`allowed-tools: Bash, Read, Write`）
  误判为「未声明」。现在两种写法都解析、非空即 PASS。

## [1.0.1] - 2026-06-21

实战体检 14 个 skill 时暴露的两个机检缺陷修复（dogfooding）：

### Fixed
- **glob 指针不再误报死链**：`reference/deck-engine-*.html` 这类通配符指针，
  现在用 `glob` 解析、能匹配到真实文件就算存在；`{a,b}` brace 简写跳过不误报。
  （原正则在 `*` 处截断成 `reference/deck-engine-`，当字面路径判死。）
- **指针 / 教学词行号还原为文件绝对行号**：原先报的是正文相对行号（少算了
  frontmatter 行数），定位会偏。`parse_frontmatter` 现返回 `body_offset` 补正。

## [1.0.0] - 2026-06-21

首个版本。给 Agent Skill（SKILL.md）做体检的零依赖检查器。

### 检查项（12 项加权）
- **安全**：SKILL.md 及捆绑文件无硬编码密钥（命中即 FAIL，资损级）。
- **触发**：frontmatter 必填合法（name/description）；description 含「何时用」且 ≤1024 字符。
- **减法**：SKILL.md ≤500 行；长内容下沉 references/（渐进披露）；大段脚本外置 scripts/。
- **可移植**：无硬编码 `/Users/`、`/home/` 绝对路径。
- **取舍**：别替模型补它已会的（教学冗余检测）；allowed-tools 最小化；配套 README/CHANGELOG。

### 特性
- 零依赖（Python3 标准库），文本 + `--json` 双输出，退出码随 FAIL。
- 按重要度加权评分（触发/减法核心项 1.5，标准项 1.0，加内容项 0.6），A/B/C/D 分档。
- 极简零依赖 frontmatter 解析（块标量 / 行内 list / 缩进 list）。
- 密钥扫描双档豁免：指纹型用窄填充表、赋值型用宽占位表，避免误杀真 key。
- 报告口吻与署名沿用「会勇禾口王的AI笔记」品牌人设。
