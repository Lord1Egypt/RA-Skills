# Changelog

本文件记录 code-reviewer skill 的版本变更（自 v1.3.0 起维护；更早版本见 git 历史提交）。

## [1.3.1] - 2026-08-07

### Changed
- 发布至 ClawHub（slug: `pro-code-reviewer`，owner: timeaground）

## [1.3.0] - 2026-08-07

### Added
- Frontmatter 新增 `version`、`requires`、`resource_manifest` 声明（消除隐式依赖，声明网络域白名单 github.com / gitlab.com）
- 新增 `## When to use this`（触发条件集中章节）
- 新增 `## 交付物 (Output)`（输出规范独立章节，替代原 `### 7. Output`）
- 新增 `## 不适用场景` 与 `## Tips` 章节
- Workflow Step 2 新增 PR fetch 失败降级路径（重试一次 → 提示重试或转本地审查）
- 新增 `eval/evals.json`（21 条 Layer 2 行为测试用例：POS/NEG/PQ/SEC/ADV）

### Changed
- `description` 精简至 200 字符内（核心触发词保留，扩展触发词移入 When to use this）
- `references/review-android.md`、`references/review-ios.md` 报告模板占位符 `xxx` → `<branch>`

## [1.2.0]
- PR/CI Layer 1：支持通过 URL 远程审查 PR（git: c6dabbf）

## [1.1.0]
- 三遍审查（Pass A/B/C）、review-general 升级、skill-vetter 集成（git: db8c9cf）
