# Changelog

## 1.0.3 (2026-04-14)

### Fixed
- **隐私合规最终版**：彻底移除所有版本中可能残留的个人身份信息
- SKILL.md 描述优化，明确技能触发条件和依赖关系
- 移除 publish.py 中的硬编码路径引用

### Changed
- 依赖 skill 描述从 `academic-literature-search` 改为 `academic-literature-search (或类似文献检索 skill)`
- 流程步骤优化：合并"多渠道下载"和"科研通求助"步骤，减少冗余

## 1.0.2 (2026-04-14)

### Changed
- **安全合规修复**：在 SKILL.md frontmatter 中声明所有环境变量（env）和权限（permissions）
- 声明权限：browser-cdp、filesystem-read、filesystem-write、cron、subprocess
- 修复 registry metadata 与实际指令不匹配的问题（扫描器报告"declared none vs. many required"）

## 1.0.1 (2026-04-14)

### Changed
- **安全修复**：移除所有硬编码的个人环境信息（微信 userId、文件路径、Unpaywall 邮箱等）
- 新增环境变量配置机制（`LIT_DOWNLOAD_DIR`、`LIT_NOTIFY_CHANNEL`、`LIT_NOTIFY_USER` 等 7 个变量）
- skill.json 新增 `env` 声明，明确列出所有依赖的环境变量
- 文件路径从硬编码改为环境变量 + 自动定位
- 通知机制改为可选：未配置通知渠道时仅在对话中告知结果
- 浏览器 CDP 端口可配置（默认 9334）
- 首次使用时自动检查环境变量并引导配置

## 1.0.0 (2026-04-10)

### Added
- Complete end-to-end literature research workflow
- Academic literature search via academic-literature-search skill (Crossref + Semantic Scholar)
- 10-20 results presentation with 2-3 high-value paper recommendations
- Multi-channel download: Unpaywall → DOI.org → Semantic Scholar PDF → Crossref
- Ablesci.com help posting automation via CDP-connected browser
- Cron-based monitoring (every 30 minutes) for help request responses
- Notification when papers are downloaded
- Progress tracking in literature-progress.md
- Detailed technical notes covering CDP timing issues, Ablesci download mechanism, and common failure modes
