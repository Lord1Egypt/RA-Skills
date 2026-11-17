# Changelog

## 1.1.1 (2026-09-06)

- 改名：`幼儿园英语全套课程` → `幼儿园英语课程体系`（displayName / H1 / summary / README 标题 / references/curriculum.md 标题同步更新）
- 移除与姊妹 Skill 的交叉引用：删除 SKILL.md Overview 中"与 kindergarten-math-course、kindergarten-thinking-course 互补"一句，删除 README.md「姊妹 Skill」整段，CHANGELOG 历史条目的"姊妹 Skill 对齐"措辞相应精简
- 重新提交触发平台 AI 评估

## 1.1.0 (2026-09-06)

按 SkillHub TRACE 五维评测体系（Trust / Reliability / Adaptability / Convention / Effectiveness）做的系统性优化：

- **A 适用性**：新增「对话示例（自然语言触发）」章节，5 组完整多轮对话示例（直接出题 / 零基础定级 / 批改重练 / 开口说英语 / 不触发场景），覆盖从触发到交付再到不触发的完整链路
- **R 可靠性**：新增「错误处理与边界输入」章节，6 类异常情况的处置表（非法等级、题数超范围、目录无权限、答卷照片无法识别、不提供音频、答案同页）+ 4 条边界输入约定，明确"不静默失败、不凭猜测批改"
- **T 可信任度**：新增「安全与国内可用性」声明——零外网、零凭证、最小权限、无数据外传、HTML 转义、中文与字体 fallback、seed 可复现
- **C 规范性**：新增「已知限制与扩展指引」章节，如实声明 emoji 素材差异、无音频、未做移动端适配、口语题无标准答案四项限制，并给出新增题型/扩充词汇/调整版式的扩展路径
- 明确启蒙阶段批改原则：能拼出首音且结构接近即算通过，不因拼写细节判错

## 1.0.2 (2026-09-06)

- 收紧 frontmatter `description`（518 字 → 约 90 字），触发词表保留在正文「触发条件」章节与 `keywords`，符合上架 description 简洁化建议
- 重新提交触发平台 AI 评估

## 1.0.1 (2026-09-06)

- 补齐 frontmatter 发布字段：`category=education`、`platforms`、`author`、`keywords`（上架元数据完整度）
- 重新提交以触发平台 AI 评估

## 1.0.0 (2026-09-06)

- 首次发布：L1-L4 四级体系 + 10 题型插件架构
- A4 可打印练习页生成器（含参考答案页）
- 诊断卷（`--preset diagnostic`）、错题重练（`--review`/`--wrong`）
- 中英双语（`--lang`）、分栏（`--columns`）、姓名预填（`--name`）、seed 可复现
