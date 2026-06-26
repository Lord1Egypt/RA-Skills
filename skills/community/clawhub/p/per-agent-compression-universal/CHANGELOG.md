# Changelog

All notable changes to this skill will be documented in this file.

**[skip to first Chinese section](#chinese-1-3-4)** | 请往下翻页查看各版本的中文说明

---

## [1.4.0] - 2026-03-20 (Delivery Flexibility & Resilience)

### Added
- **Interactive installer with delivery prompts**: `install.sh` now accepts `--channel`, `--to`, `--account` arguments to configure task announcement destination. If no arguments provided and running in an interactive terminal, installer prompts for these values.
- **Automatic retry with exponential backoff**: Task execution now includes retry logic for transient failures (network issues, API rate limits, temporary model errors). Up to 3 attempts with delays 2s, 4s, 8s. Permanent errors are logged and skipped.
- **Enhanced failure reporting**: If any notes fail extraction after all retries, the summary announcement includes a failure count, providing visibility into issues.
- **Per-agent execution (security hardening)**: Changed `--agent "main"` to `--agent "$agent_id"` so each cron task runs under its respective agent (hrbp, parenting, decoration, etc.), achieving true isolation and minimizing privileges.
- **Explicit binary dependencies**: `skill.json` now declares `"binaries": ["openclaw", "jq"]` to reflect actual installer requirements.

### Technical Details
- Delivery configuration is embedded in the task message and applied to the cron job's announce delivery parameters.
- Retry logic is part of the execution plan in MSG_FULL; agents will automatically retry failed note processing.
- State tracking remains unchanged; failures do not block subsequent notes.
- Per-agent execution eliminates the previous central-executor model; each task operates only on its own workspace, reducing blast radius and aligning with the `workspace-isolation` capability.
- The `jq` binary is required for parsing `openclaw agents list --json` during agent discovery.

---

<a name="chinese-1-4-0"></a>( Chinese )
### 新增（Added）
- **交互式安装器**：`install.sh` 现在接受 `--channel`、`--to`、`--account` 参数来配置任务公告的目标通道和接收者。如果未提供参数且运行在交互式终端中，安装程序会提示输入这些值。
- **自动重试机制**：任务执行现在包含针对 transient 失败（网络问题、API 速率限制、临时模型错误）的重试逻辑。最多 3 次尝试，延迟分别为 2s、4s、8s（指数退避）。永久性错误将被记录并跳过。
- **增强的失败报告**：如果任何笔记在所有重试后仍失败，摘要公告将包含失败计数，提供问题可见性。
- **Per-agent 执行（安全加固）**：将 `--agent "main"` 改为 `--agent "$agent_id"`，使每个 cron 任务在对应代理（hrbp、parenting、decoration 等）上下文中运行，实现真正隔离并最小化权限。
- **显式二进制依赖声明**：`skill.json` 新增 `"binaries": ["openclaw", "jq"]`，反映实际安装器依赖。

### 技术细节（Technical Details）
- 交付配置嵌入任务消息中，并应用于 cron 作业的 announce 投递参数。
- 重试逻辑是 MSG_FULL 执行计划的一部分；代理将自动重试失败的笔记处理。
- 状态跟踪保持不变；失败不会阻塞后续笔记。
- Per-agent 执行消除了之前的中央执行器模型；每个任务仅操作自身 workspace，缩小爆炸半径，并与 `workspace-isolation` 能力保持一致。
- `jq` 二进制是代理发现阶段解析 `openclaw agents list --json` 所必需的。

---

## [1.3.4] - 2026-03-19 (Critical Bug Fix: STATE_FILE Variable & Task Reliability)

### Fixed
- **STATE_FILE variable case sensitivity**: Changed `STATE_FILE={workspace}` to `{WORKSPACE}` (uppercase) to match OpenClaw's case-sensitive environment variable substitution. This bug prevented state file creation, causing tasks to hang at step 2 and eventually timeout.
- **Task reliability**: Fixed issue where tasks appeared `running` but never actually executed due to incorrect path resolution and Gateway state caching.
- **Installation script**: Updated `install.sh` to generate correct `{WORKSPACE}` variable in both short and full messages.

### Changed
- `install.sh`: All task messages now use `{WORKSPACE}` (uppercase) consistently for `DAILY_NOTES_DIR`, `PROCESSED_DIR`, and `STATE_FILE`.
- All existing tasks should be updated manually or by re-running `./install.sh` to apply the fix.

### Impact
- Tasks per_agent_compression_* now successfully create `.compression_state.json` and execute all steps.
- Verified with per_agent_compression_hrbp: completed in ~9 minutes, processed 3 old notes, moved files to `processed/`, and compressed content into target files.
- No more silent hangs at step 2.

### Recommended Actions
1. **Re-run install script**: `./install.sh` to update all existing tasks with corrected variable.
2. **Monitor** next scheduled runs (starting 2026-03-21) to confirm all 5 tasks complete successfully.
3. **Optional**: Increase timeout to 6000s for larger workspaces (already applied in previous manual fixes).

### Enhanced
- **Extraction framework expansion**: Added **User Traits & Self-Profile** category to capture personality traits, communication preferences, learning style, values, interests, strengths/weaknesses, and self-descriptions.
- **USER.md format update**: Extraction now explicitly includes User Traits prominently in the `## Personal Info / Preferences` section.
- **Comprehensiveness**: Extraction categories increased from 10 to 11, ensuring user characteristics are systematically preserved alongside decisions, constraints, principles, todos, metrics, people, context, problems, preferences, and references.

### Impact
- Agents will now solidify a more holistic profile of the user, including self-perceived traits and communication style.
- This addresses the observation that extracted content was too sparse; the enhanced framework captures more nuanced user information.
- All tasks (hrbp, parenting, decoration, memory_master, main) updated to include new category in their execution plan.

### Note
Existing installations should re-run `./install.sh` to apply the enhanced extraction framework to their tasks.

---

## [1.3.3] - 2026-03-18 (Message Length Fix)

### Fixed
- **CLI message truncation**: `openclaw cron add --message` was truncating long execution plans to ~500 chars, losing critical steps
- **Implementation**: Changed install script to use two-step approach:
  1. `add` with concise message (~400 chars)
  2. Immediately `edit` to enrich with full execution plan (~1700 chars) using job UUID
- **Reliability**: All per-agent compression tasks now receive complete instruction set regardless of CLI limits

### Changed
- `install.sh`: Introduced `MSG_SHORT` and `MSG_FULL`, added post-add `edit` enrichment with proper job ID lookup
- All `per_agent_compression_*` tasks: Message length now >1700 chars with full 10-step execution plan

### Note
This fix ensures tasks have all necessary details to run correctly. No functional changes to compression logic. Existing installations should re-run `./install.sh` to upgrade tasks.

<a name="chinese-1-3-3"></a>( Chinese )
### 已修复（Fixed）
- **CLI 消息截断**：`openclaw cron add --message` 截断长执行计划至约 500 字符，丢失关键步骤
- **解决方案**：改用两步法：
  1. `add` 使用精简消息（约 400 字符）
  2. 立即 `edit` 富化为完整执行计划（约 1700 字符），使用 job UUID 获取
- **可靠性**：所有 per-agent 压缩任务现在接收完整指令集，不受 CLI 限制影响

### 变更（Changed）
- `install.sh`：引入 `MSG_SHORT` 和 `MSG_FULL`，在 add 后添加 edit 富化步骤，使用正确的 job ID 查找
- 所有 `per_agent_compression_*` 任务：消息长度 >1700 字符，包含完整 10 步骤执行计划

### 备注（Note）
此修复确保任务拥有运行所需的所有详细信息。压缩逻辑无功能变更。现有安装应重新运行 `./install.sh` 以升级任务。

---

## [1.3.2] - 2026-03-18 (Critical Privacy Remediation)

### Security
- **Removed specific references from public documentation**: Purged all mentions of user-specific configuration values (including recipient identifiers and model names) from CHANGELOG to prevent information leakage
- **Generalized security disclosure**: Revised version history to describe remediation in abstract terms without revealing sensitive details
- **Privacy-first documentation**: Ensured all public-facing documents avoid exposing any user data, even in historical context

### Changed
- CHANGELOG.md: Reworded v1.3.0 security entry to remove specific leak details while preserving accountability
- All documentation: Adopted conservative language for security disclosures

### Note
This patch addresses a documentation-level information exposure. No functional changes. users should upgrade to ensure public distributions contain no residual sensitive information.

<a name="chinese-1-3-2"></a>( Chinese )
### 安全（Security）
- **从公开文档中移除具体引用**：从 CHANGELOG 中清除所有提及用户特定配置值（包括接收者标识和模型名称）的内容，以防止信息泄露
- **泛化安全披露**：修订版本历史，以抽象方式描述修复措施，不透露敏感细节
- **隐私优先文档**：确保所有对外文档避免暴露任何用户数据，即使在历史上下文中也如此

### 变更（Changed）
- CHANGELOG.md：重新措辞 v1.3.0 安全条目，移除具体泄露细节，同时保留问责
- 所有文档：采用保守的语言进行安全披露

### 备注（Note）
此补丁修复文档级信息暴露问题。无功能变更。用户应升级以确保公开分发版本不包含任何残留敏感信息。

---

## [1.3.1] - 2026-03-18 (Version Unification)

### Changed
- Unified version numbers across local, GitHub, and ClawHub to 1.3.1
- Consolidated all prior documentation refinements into single version

### Note
This release contains no functional changes. It is a version synchronization point. All features are as in v1.3.0.

<a name="chinese-1-3-1"></a>( Chinese )
### 变更（Changed）
- 统一本地、GitHub 和 ClawHub 的版本号为 1.3.1
- 将所有先前的文档改进合并为单一版本

### 备注（Note）
此版本不包含任何功能变更。这是版本同步点。所有功能与 v1.3.0 相同。

---

## [1.3.0] - 2026-03-18 (Security & Privacy Hardening)

### Security
- **Credential hygiene**: Removed hardcoded user-specific configuration values from install script and documentation
- **Privacy hardening**: Installer now infers environment-specific parameters automatically, avoiding any personal data exposure
- **Model agnostic**: No longer embeds fixed model references in the package
- **Public distribution safe**: Skill can be safely published without leaking any user identifiers

### Changed
- `install.sh`: Stripped all explicit `--model`, `--channel`, `--to`, and `--best-effort-deliver` arguments; now relies on OpenClaw's runtime inference
- `README.md`: Revised task creation instructions to emphasize automatic parameter inference
- Documentation: Generalized all examples to avoid exposing personal configuration details

### Note
This is a critical privacy update. All users should upgrade to remove any residual personal data from prior installations.

<a name="chinese-1-3-0"></a>( Chinese )
### 安全（Security）
- **凭据卫生**：从安装脚本和文档中移除硬编码的用户特定配置值
- **隐私强化**：安装程序现在自动推断环境特定参数，避免任何个人数据暴露
- **模型无关**：不再在包中嵌入固定模型引用
- **公开分发安全**：技能可以安全发布，不会泄露任何用户标识符

### 变更（Changed）
- `install.sh`：剥离所有显式的 `--model`、`--channel`、`--to` 和 `--best-effort-deliver` 参数；现在依赖 OpenClaw 的运行时推断
- `README.md`：修订任务创建说明，强调自动参数推断
- 文档：泛化所有示例，避免暴露个人配置细节

### 备注（Note）
这是关键隐私更新。所有用户应升级以移除先前安装中残留的任何个人数据。

---

## [1.2.6] - 2026-03-18 (Version Unification)

### Changed
- Unified all version numbers across local, GitHub, and ClawHub to 1.2.6
- Consolidated all prior documentation refinements into single version

### Note
This release contains no functional changes. It is a version synchronization point. All features are as in v1.2.2.

( Chinese )
### 变更（Changed）
- 统一本地、GitHub 和 ClawHub 的所有版本号为 1.2.6
- 将所有先前文档改进合并为单一版本

### 备注（Note）
此版本不包含任何功能变更。这是版本同步点。所有功能与 v1.2.2 相同。

---

## [1.2.5] - 2026-03-18 (Documentation Cleanup)

### Changed
- Removed intermediate version entries (1.2.3, 1.2.4) from CHANGELOG to avoid confusion
- Kept only essential version history (1.2.2 as final feature release)

### Fixed
- Ensured CHANGELOG structure follows rule: newest at top, oldest at bottom
- Verified bilingual separation across all documents

### Note
No functional changes. Documentation only.

( Chinese )
### 变更（Changed）
- 从 CHANGELOG 中移除中间版本条目（1.2.3、1.2.4）以避免混淆
- 仅保留必要版本历史（1.2.2 作为最终功能版本）

### 已修复（Fixed）
- 确保 CHANGELOG 结构符合规则：最新版本在顶部，最旧在底部
- 验证所有文档的双语分离

### 备注（Note）
无功能变更。仅文档整理。

---

## [1.2.4] - 2026-03-18 (Documentation Fix)

### Added
- Separated English and Chinese documentation correctly (CHANGELOG now has distinct sections)
- Version & release protocol added to AGENTS.md

### Changed
- CHANGELOG ordering: newest versions at top, oldest at bottom
- Documentation structure: clear English-first then Chinese-after-separator

### Fixed
- Fixed duplicate/incorrect version entries in CHANGELOG
- Ensured bilingual consistency across README and CHANGELOG

### Note
No functional changes. Documentation refinement only.

( Chinese )
### 已添加（Added）
- 正确分离英文和中文文档（CHANGELOG 现在有独立章节）
- 版本与发布协议已加入 AGENTS.md

### 变更（Changed）
- CHANGELOG 排序：最新版本在顶部，最旧在底部
- 文档结构：清晰的英文优先、后跟中文的分隔格式

### 已修复（Fixed）
- 修复 CHANGELOG 中重复/不正确的版本条目
- 确保 README 和 CHANGELOG 的双语一致性

### 备注（Note）
无功能变更。仅文档优化。

---

## [1.2.3] - 2026-03-18 (Documentation Update)

### Added
- Separated English and Chinese documentation in README and CHANGELOG for improved readability
- "Please scroll down for Chinese" notice at the top of each document
- Comprehensive version & release protocol added to AGENTS.md

### Changed
- Documentation structure: English content first, then full Chinese translation after separator
- README and CHANGELOG now fully bilingual with clear section separation

### Fixed
- None (documentation only)

### Note
This version was an intermediate documentation update. All changes are non-functional.

( Chinese )
### 已添加（Added）
- 在 README 和 CHANGELOG 中分离英文和中文文档以提高可读性
- 每个文档顶部添加"请往下翻页查看中文说明"提示
- 综合版本与发布协议已加入 AGENTS.md

### 变更（Changed）
- 文档结构：英文内容在前，分隔符后为完整中文翻译
- README 和 CHANGELOG 现为完全双语，章节清晰分离

### 已修复（Fixed）
- 无（仅文档）

### 备注（Note）
此为中间文档更新版本。所有更改均不影响功能。

---

## [1.2.2] - 2026-03-18 (Final Feature Release)

### Added
- State persistence & checkpoint resilience - Each agent task maintains `.compression_state.json` to resume from interruptions
- Deduplication - Checks target files before appending to avoid duplicate entries from same daily note
- Remaining notes reporting - Summary includes count of old notes still pending for future runs
- Enhanced error handling - Individual note failures don't stop the entire task; errors logged and continue
- Moved-file marking - Processed notes moved to `memory/processed/` directory for clear separation
- Domain-specific extraction guidelines - Each task includes DOMAIN_CONTEXT to tailor extraction (general, HR/work, parenting, renovation)
- Pre-check validation - Script verifies agents list, workspace existence, and memory directory before registration
- Auto-discovery of all agents via `openclaw agents list --json`
- Staggered weekly scheduling (Sundays, 30-minute intervals starting 03:00)
- Workspace isolation - each agent compresses its own memory files
- Basic extraction of preferences, decisions, and personal information
- Markdown date headers for all appended entries
- Summary notifications via DingTalk connector
- Uninstall script to remove all `per_agent_compression_*` tasks
- Comprehensive README with troubleshooting guide

### Changed
- Task naming - Changed from `peragent_compression_` to `per_agent_compression_` for better readability
- Timeout increased - From 300s to 1200s to accommodate larger note sets
- Message payload enriched - Detailed execution plan with specific file paths, state structure, and date header format (`### [YYYY-MM-DD]`)
- Delivery mode - Uses `--best-effort-deliver` to ensure notifications are attempted even if partial failures occur

### Fixed
- State file path - Now properly defined as `{workspace}/memory/.compression_state.json`
- Processed directory - Explicitly created as `{workspace}/memory/processed/`
- Target sections - Clear append locations: USER.md (`## Personal Info / Preferences`), IDENTITY.md (`## Notes`), SOUL.md (`## Principles`/`## Boundaries`), MEMORY.md (`## Key Learnings`)

### Documentation Improvements (Continuous)
- **Bilingual documentation**: README and CHANGELOG fully separated into English (first) and Chinese (after separator) sections for readability
- **Scroll notice**: "请往下翻页查看中文说明" at the top of each document
- **Version & release protocol**: Added to AGENTS.md to enforce proper changelog ordering and release workflow
- **CHANGELOG structure**: Newest versions at top, oldest at bottom; clear separation between English and Chinese entries

### Known Issues
- CLI message length limit: `openclaw cron add --message` truncates messages > ~1KB. Workaround: use concise template. For fully detailed instructions, manually edit the task post-install using `openclaw cron edit --message`.
- No per-agent install filter: Skill auto-discovers all agents; cannot limit to a single agent via flag. To test one agent, either edit `install.sh` or manually create that agent's task after uninstall.
- Requires `self-improve-agent` for full automation (optional).
- Memory/processed/ directory must be writable (standard permissions suffice).
- No dry-run mode for testing (future enhancement).
- No performance optimizations (caching, indexing) - acceptable for typical workloads.

### Tested
- ✅ Fresh install on clean system (no pre-existing per-agent tasks)
- ✅ Reinstall over existing tasks (skips duplicates)
- ✅ Uninstall removes all skill-created tasks
- ✅ Task payload includes all expected fields (state file, processed dir, domain context)
- ✅ Gateway logs show no errors during installation
- ✅ Daily notes (2026-03-18) recorded full session for future compression
- ✅ Documentation rendering validated in Markdown viewers
- ✅ Bilingual separation and links verified

( Chinese )
### 已添加（Added）
- 状态持久化与检查点恢复 - 每个代理任务维护 `.compression_state.json` 以从中断处恢复
- 去重 - 在追加前检查目标文件，避免同一每日笔记产生重复条目
- 剩余笔记报告 - 摘要中包含待处理旧笔记数量，用于未来运行参考
- 增强错误处理 - 单个笔记失败不会停止整个任务；错误会被记录并继续
- 移动文件标记 - 已处理笔记移至 `memory/processed/` 目录以便清晰分离
- 领域特定提取指南 - 每个任务包含 DOMAIN_CONTEXT 以定制提取逻辑（通用、HR工作、育儿、装修）
- 预检查验证 - 脚本在注册前验证代理列表、工作区存在性和内存目录
- 自动发现所有代理 - 通过 `openclaw agents list --json`
- 交错每周调度 - 周日开始，30分钟间隔（03:00起）
- 工作区隔离 - 每个代理仅压缩自己的内存文件
- 基础提取功能 - 提取偏好、决策和个人信息
- Markdown 日期标题 - 所有追加条目均带日期头
- 摘要通知 - 通过钉钉连接器发送
- 卸载脚本 - 可移除所有 `per_agent_compression_*` 任务
- 综合 README - 包含故障排除指南

### 已变更（Changed）
- 任务命名 - 从 `peragent_compression_` 改为 `per_agent_compression_` 以提高可读性
- 超时增加 - 从 300s 增至 1200s 以适应更大笔记集
- 消息载荷增强 - 详细执行计划包含具体文件路径、状态结构和日期头格式（`### [YYYY-MM-DD]`）
- 交付模式 - 使用 `--best-effort-deliver` 确保即使部分失败也尝试发送通知

### 已修复（Fixed）
- 状态文件路径 - 正确定义为 `{workspace}/memory/.compression_state.json`
- 已处理目录 - 明确创建为 `{workspace}/memory/processed/`
- 目标章节 - 明确追加位置：USER.md（`## Personal Info / Preferences`）、IDENTITY.md（`## Notes`）、SOUL.md（`## Principles`/`## Boundaries`）、MEMORY.md（`## Key Learnings`）

### 文档改进（持续）
- **双语文档**：README 和 CHANGELOG 完全分为英文（前）和中文（后）章节以提高可读性
- **滚动提示**：每个文档顶部有"请往下翻页查看中文说明"
- **版本与发布协议**：已加入 AGENTS.md 以强制执行正确的 changelog 排序和发布工作流
- **CHANGELOG 结构**：最新版本在顶部，最旧在底部；英文与中文条目之间清晰分隔

### 已知问题（Known Issues）
- CLI 消息长度限制：`openclaw cron add --message` 会截断超过 ~1KB 的消息。变通方案：使用简洁模板。如需完整详细指令，可在安装后手动编辑任务：`openclaw cron edit --message`。
- 无单代理安装过滤器：技能自动发现所有代理；无法通过标志限制代理。如需限制，可修改 `install.sh` 或卸载后手动创建特定代理任务。
- 需要 `self-improve-agent` 以实现全自动（可选）。
- memory/processed/ 目录必须可写（标准权限即可）。
- 无空运行测试模式（未来增强）。

### 测试（Tested）
- ✅ 全新安装（无预存 per-agent 任务）
- ✅ 覆盖重装（跳过重复项）
- ✅ 卸载可移除所有技能创建的任务
- ✅ 任务载荷包含所有预期字段（状态文件、处理目录、领域上下文）
- ✅ 安装过程网关心跳无错误
- ✅ 每日笔记（2026-03-18）记录了完整会话供未来压缩测试
- ✅ 文档渲染在 Markdown 查看器中验证通过
- ✅ 双语分离和链接验证完成

---

## Upgrade Notes

### From 1.1.0 to 1.2.2
1. Run `./uninstall.sh` to remove old tasks
2. Replace skill directory with v1.2.2
3. Run `./install.sh` to register tasks
4. Existing `.compression_state.json` files will be preserved (backward compatible)

### From 1.2.2 to 1.3.0 (Security Fix)
This is a critical security update that removes user-specific configuration exposures. Replace all skill files with v1.3.0+ and re-run `./install.sh` to recreate tasks with safe defaults.

### Fresh Install
Simply run `./install.sh` after placing the skill in `/root/.openclaw/workspace/skills/`.

( Chinese )
### 从 1.1.0 升级至 1.2.2
1. 运行 `./uninstall.sh` 移除旧任务
2. 替换技能目录为 v1.2.2
3. 运行 `./install.sh` 注册任务
4. 现有 `.compression_state.json` 文件将被保留（向后兼容）

### 从 1.2.2 升级至 1.3.0（安全修复）
这是关键安全更新，移除了用户特定配置暴露问题。替换所有技能文件为 v1.3.0+ 并重新运行 `./install.sh` 以使用安全默认值重新创建任务。

### 全新安装
将技能放入 `/root/.openclaw/workspace/skills/` 后直接运行 `./install.sh`。

---

## Version Comparison

| Feature | 1.1.0 | 1.2.2 | 1.2.3-1.2.6 | 1.3.0+ |
|---------|-------|-------|-------------|-------|
| Auto-discovery | ✅ | ✅ | ✅ | ✅ |
| State persistence | ❌ | ✅ | ✅ | ✅ |
| Deduplication | ❌ | ✅ | ✅ | ✅ |
| Domain filtering | ❌ | ✅ | ✅ | ✅ |
| Moved-file marking | ❌ | ✅ | ✅ | ✅ |
| Bilingual docs | ❌ | ✅ | ✅ | ✅ |
| Test artifacts | ❌ | ✅ | ✅ | ✅ |
| Production readiness label | ❌ | ✅ | ✅ | ✅ |
| CLI length workaround | ❌ | ✅ | ✅ | ✅ |
| No hardcoded credentials | ❌ | ❌ | ❌ | ✅ |

### 功能对比

| 功能 | 1.1.0 | 1.2.2 | 1.2.3-1.2.6 | 1.3.0+ |
|---------|-------|-------|-------------|-------|
| 自动发现 | ✅ | ✅ | ✅ | ✅ |
| 状态持久化 | ❌ | ✅ | ✅ | ✅ |
| 去重 | ❌ | ✅ | ✅ | ✅ |
| 领域过滤 | ❌ | ✅ | ✅ | ✅ |
| 移动文件标记 | ❌ | ✅ | ✅ | ✅ |
| 双语文档 | ❌ | ✅ | ✅ | ✅ |
| 测试产物 | ❌ | ✅ | ✅ | ✅ |
| 生产就绪标签 | ❌ | ✅ | ✅ | ✅ |
| CLI 长度变通 | ❌ | ✅ | ✅ | ✅ |
| 无硬编码凭据 | ❌ | ❌ | ❌ | ✅ |

---