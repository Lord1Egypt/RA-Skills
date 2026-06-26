# Hopola 上架 ClawHub 规划（Plan）

## Summary
- 目标：把现有 `Hopola` 打造成可上架 ClawHub 的高质量 Skill 套件，包含主 Skill、子技能（4 主 + 2 扩展）、打包脚本、展示资产与中英双语文档。
- 能力范围：在现有“检索/生图/上传/报告”基础上，新增“视频生成、3D 模型生成”能力。
- 安全要求：API Key 不落盘、不写入 JSON 默认值，统一采用环境变量读取；发布包中仅保留空模板与校验逻辑。

## Current State Analysis
- 当前已存在目录：`/Users/youpengtu/Hopola-Skills/.trae/skills/Hopola/`
- 现有文件：
  - `SKILL.md`（主技能说明，已接 Gateway）
  - `config.template.json`（含 Gateway 与流程配置）
  - `examples.md`（调用示例）
- 现状缺口：
  - 尚无子技能拆分结构（subskills）
  - 尚无发布脚本（校验/打包）
  - 尚无品牌资产（logo/cover/flow）
  - 尚无面向 ClawHub 的上架说明与发布清单
  - 配置文件需进一步收敛为“默认 key 为空 + 强制环境变量注入”

## Proposed Changes

### 1) 主 Skill 强化
**文件**：`/Users/youpengtu/Hopola-Skills/.trae/skills/Hopola/SKILL.md`  
**改动**：
- 增加“ClawHub 发布版”说明章节（目录规范、调用约定、依赖边界）。
- 明确主编排只做路由与容错，具体能力委派给子技能。
- 增加视频/3D 的调度策略：优先固定工具名，缺失时自动发现。
**原因**：让主 Skill 成为稳定入口，降低后续维护复杂度。

### 2) 配置安全化与能力扩展
**文件**：`/Users/youpengtu/Hopola-Skills/.trae/skills/Hopola/config.template.json`  
**改动**：
- 删除一切默认密钥值，仅保留 `key_env_name` 与空占位字段。
- 新增 `video_generation` 与 `model3d_generation` 配置段。
- 为“固定优先、自动发现回退”增加显式字段：
  - `preferred_tool_name`
  - `fallback_discovery_keywords`
  - `required_args_schema`
- 增加发布前安全校验标识（如 `forbid_plaintext_key`）。
**原因**：满足“用户主动配置 key”的安全诉求，同时支持新增能力。

### 3) 子技能体系（4 主 + 2 扩展）
**目录**：`/Users/youpengtu/Hopola-Skills/.trae/skills/Hopola/subskills/`
**新增文件**：
- `search/SKILL.md`
- `generate-image/SKILL.md`
- `upload/SKILL.md`
- `report/SKILL.md`
- `generate-video/SKILL.md`
- `generate-3d/SKILL.md`
**改动**：
- 每个子技能定义：触发时机、输入输出契约、失败处理、与主技能协同方式。
- 扩展子技能（video/3d）采用“固定工具优先 + 自动发现回退”。
**原因**：增强复用性与可维护性，提升 ClawHub 展示专业度。

### 4) 发布脚本（Python）
**目录**：`/Users/youpengtu/Hopola-Skills/.trae/skills/Hopola/scripts/`
**新增文件**：
- `validate_release.py`：结构完整性、字段合法性、安全项检查（禁止明文 key）
- `build_release_zip.py`：生成发布 zip 与校验摘要
- `check_tools_mapping.py`：检查固定工具名与发现关键词策略是否完备
**原因**：实现发布前自动体检与一键打包，减少人工失误。

### 5) 资产与展示物料
**目录**：`/Users/youpengtu/Hopola-Skills/.trae/skills/Hopola/assets/`
**新增文件**：
- `logo.svg`
- `cover.svg`
- `flow.svg`
**改动**：
- 资产采用可编辑矢量格式，内容围绕“Search → Image/Video/3D → Upload → Report”。
**原因**：提升 ClawHub 页面辨识度与专业感。

### 6) 文档与发布说明（中英双语）
**新增文件**：
- `/Users/youpengtu/Hopola-Skills/.trae/skills/Hopola/README.zh-CN.md`
- `/Users/youpengtu/Hopola-Skills/.trae/skills/Hopola/README.en.md`
- `/Users/youpengtu/Hopola-Skills/.trae/skills/Hopola/RELEASE.md`
- `/Users/youpengtu/Hopola-Skills/.trae/skills/Hopola/examples.md`（补视频/3D 示例）
**改动**：
- README：能力、目录、快速开始、安全配置、故障排查。
- RELEASE：上架前检查清单、zip 内容说明、版本变更说明模板。
**原因**：满足上架可读性与可操作性。

## Assumptions & Decisions
- 决策：发布形态采用“单 Skill + 子技能包”。
- 决策：子技能组织采用“4 主子技能 + 2 扩展子技能（视频/3D）”。
- 决策：脚本采用 Python；发布输出为 zip。
- 决策：文档采用中英双语。
- 决策：API Key 仅通过环境变量提供，默认空值，不写入任何 JSON 与示例命令明文。
- 决策：视频/3D 调用策略采用“固定工具名优先，缺失时自动发现回退”。
- 假设：ClawHub 接受 zip 包上传，且当前目录结构可作为发布根目录。

## Verification Steps
- 结构校验：
  - 子技能目录与 6 个 `SKILL.md` 全部存在。
  - `scripts/`、`assets/`、双语 README 与 `RELEASE.md` 存在。
- 安全校验：
  - `validate_release.py` 通过；扫描结果中无明文 API Key。
  - `config.template.json` 不包含任何默认 key 值。
- 能力校验：
  - 示例覆盖检索、生图、视频、3D、上传、报告六类流程。
  - 固定工具名不可用时，回退发现流程在文档与配置中均有定义。
- 打包校验：
  - `build_release_zip.py` 成功生成 zip。
  - zip 解压后目录完整，关键文档可读，示例可复用。

## 安全设计建议（将在实施中落地）
- 密钥入口唯一化：只认环境变量（如 `OPENCLOW_KEY`），不接受配置文件硬编码。
- 最小暴露原则：日志中脱敏 key，仅显示前后少量字符或完全掩码。
- 发布前阻断：发现明文 key 即打包失败并输出修复建议。
- 示例去敏：文档示例统一使用 `$OPENCLOW_KEY` 占位，不出现真实值。
