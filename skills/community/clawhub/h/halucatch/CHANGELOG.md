# Changelog

本文档记录 HaluCatch 项目的所有 notable changes。

版本号规则：
- **中间版本号** (1.x.0)：新功能或架构级变更
- **小版本号** (1.0.x)：修复、增强、chore 等小更新
- **每个 commit 对应一个版本更新**

---

## [Unreleased]


### Fixed

- Add actionable fix guidance to all error messages
- Raise file size thresholds to reasonable levels (.py 500, .md 800)

---

## [V1.7.1] - 2026-06-28

### Fixed
- **高优先级代码修复**
  - `except:` → `except Exception:`（防吞系统级异常）
  - `score / total` → `score / max(total, 1)`（3处，防除零崩溃）
  - `check_code_risks` 字符串/注释误扫描 → 预处理移除字面量后再正则匹配
- **中优先级文档修复**
  - 报告文件名含版本号，冲突时自动加序号（`-1`、`-2`...）
  - SKILL.md 新增"数据要求"章节（时效性 + 前提假设）
  - 移除 `ToolCard.md` 认知污染，规范化为 `SKILL.md`
- **低优先级架构重构**
  - 1191 行 `halucatch_core.py` 拆分为 11 个模块，单文件 ≤270 行
  - 新增 `halucatch/` 包：`config`, `scanner`, `classifier`, `evaluators/`, `reporter`, `cli`
  - 保留 `halucatch_core.py` 向后兼容入口

### Added
- **版本号自动提取**：从 `_meta.json` / `meta.json` / 任意 `.md` frontmatter
- **无 SKILL.md 替代机制**：启发式匹配（frontmatter 优先 + 文件大小），报告规范性问题后继续工作
- **无 .md 文件严格拒绝**：直接报错，拒绝非标准 Skill 目录
- **测试覆盖**：新增 3 个扫描测试，总计 24 个测试全部通过

### Changed
- `build-skillhub.sh` / `check-file-size.sh` / `release.yml` / `manifest.json` 适配新包结构

---

## [V1.7.0] - 2026-06-26

### Added
- feat: **英文 Skill 支持增强**
  
  **跨语言检测能力扩展:**
  - 新增英文模糊词检测（18 个词）: `roughly`, `approximately`, `about`, `usually`, `generally` 等
  - 新增英文单位检测: `USD`, `EUR`, `GBP`, `million`, `billion`, `percent`, `percentage`, `pct`
  - 增强英文禁止声明检测: `MUST NOT`, `FORBIDDEN`, `PROHIBITED`, `DO NOT`
  - 增强工具库/分析型识别信号词
  
  **影响**: halucatch_core.py (`check_rules`, `_prohibition_signal`, `_is_tool_skill`)
  - 提交: `待提交`

---

## [V1.6.0] - 2026-06-17

### Added
- feat: **数据驱动型护栏分层** — 工具库 vs 分析型双档评分
  
  **护栏分层架构重构:**
  - `check_guardrails` 集成 `_is_tool_skill()` 分支
  - **工具库型**: total=5, 跳过置信度/数据来源/时效性检查
  - **分析型**: total=8, 全查
  - **方法论**: total=5, 保持不变
  
  **测试增强:**
  - 新增 `test_guardrails_tool_type` 测试用例
  - 21/21 通过，xlsx/pptx 3/5, neodata 7/8
  
- 影响: halucatch_core.py (52 行修改), tests/test_halucatch.py (18 行新增)
- 提交: `f445999`

---

## [V1.5.1] - 2026-06-17

### Changed
- chore: 忽略 .clawhub 目录
- 影响: .gitignore (1 行)
- 提交: `768d725`

---

## [V1.5.0] - 2026-06-17

### Added
- feat: **去语言化架构重构** — 结构化信号替代语义关键词正则
  - `_branch_density()`: 清单/图标/表格密度 → 跨语言分支检测
  - `_prohibition_signal()`: 否定词/大写警告/中文禁止 → 跨语言护栏检测
  - `check_methodology` 末尾加 AI 免责声明
  - 测试更新: 两组用例内容补信号结构
- 影响: halucatch_core.py (51 行修改), tests/test_halucatch.py (4 行), 新增文档 144 行
- 提交: `baaaaa2`

---

## [V1.4.1] - 2026-06-17

### Added
- feat: Phase 4 闭环 SOP 实现 — 三选一交互 + 行动版 prompt
  - SKILL.md Phase 4: 修复 → 用户三选一 (执行/不执行/建议) 详细 SOP
  - halucatch_core.py: 行动版报告追加三选一步骤提示
- 影响: SKILL.md (21 行), halucatch_core.py (8 行)
- 提交: `65631d4`

---

## [V1.4.0] - 2026-06-17

### Added
- feat: **闭环验证流程** — 用户选择? + AI按方案修复 + 重新审查回路
  - 决策流程图新增修复验证闭环
  - 用户选择? (3分支): 执行 → AI 修复 → 重新审查 | 不执行 → 结束 | 建议 → 回环
  - SKILL.md / README Mermaid / HTML SVG 三处同步
  - 视觉优化：汇聚箭头修正、间距扩大、标签对齐
- 影响: README.md, SKILL.md, docs/decision-flowchart.html, docs/decision-flowchart-prompt.md (新增 75 行)
- 提交: `856f682`

---

## [V1.3.1] - 2026-06-17

### Changed
- chore: 清理过期测试文档
- 影响: 删除 4 个文档文件 (451 行)
  - docs/HaluCatch-expansion-plan-2026-06-17.md
  - docs/HaluCatch-optimization-report-2026-06-17.md
  - docs/HaluCatch-readme-update-checklist-2026-06-17.md
  - docs/HaluCatch-test-report-2026-06-17.md
- 提交: `a2895f7`

---

## [V1.3.0] - 2026-06-17

### Added
- feat: **代码风险去金融化 + 边界测试 + 护栏分层**
  
  **代码风险检测增强:**
  - 移除写死变量名的 3 个 pattern（p_pool/p_val, math.exp, store_weeks）
  - 新增 4 个通用 pattern：浮点(任意==0.0), 除零(return 除法), 路径拼接, 静默覆盖, 超时缺失
  - 模式库从 5 个扩展到 7 个
  
  **扫描功能改进:**
  - `scan_folder` 改为 `os.walk` 递归扫描，支持子目录 .py
  - 文件清单加 `rel_path` 字段（精确路径匹配）
  - 返回值加 `py_count` / `max_py_lines`（避免拼接行数虚高）
  
  **护栏分层:**
  - `check_guardrails` 按 `skill_type` 分层：methodology 跳过 3 项无用检查
  - 默认输出到 `HaluCatch/reports/`，不污染目标 Skill 目录
  
  **测试增强:**
  - 16 → 20 用例，新增 4 个边界测试（空目录/只有SKILL.md/只有.py/深层嵌套）
  - 全部通过
  
  **文档同步:**
  - README 三维→四维、用例更新、护栏分层说明、测试章节
  - docs/ 补充专家出具的 4 份报告
- 影响: halucatch_core.py, tests/test_halucatch.py, README.md, SKILL.md, 新增 5 个文档
- 提交: `bd76b90`

---

## [V1.2.1] - 2026-06-17

### Changed
- feat: 更新 .gitignore，添加 .workbuddy 目录排除
- 影响: .gitignore (1 行)
- 提交: `50a8780`

---

## [V1.2.0] - 2026-06-17

### Added
- refactor: **P0-P3 全面修复** — 角色声明/三层调用/四维评估骨架/测试
  
  **P0 修复:**
  - SKILL.md 添加 AI 角色声明
  - 三层调用分工表
  - 执行决策流程图
  
  **P1 修复:**
  - 修复 `check_foundation` skip/warn 混淆
  - 修复 `methodology` 自洽逻辑
  - 修复 `report info` 隐藏
  
  **P2 实现:**
  - 实现 `check_rules()` (6项) 骨架函数
  - 实现 `check_guardrails()` (8项) 骨架函数
  
  **P3 测试:**
  - 新增 `tests/` (16 用例)
  - 新增 `docs/` (流程图) 目录
  - 补充 .gitignore
- 影响: 7 个文件变更, 731 行新增, 30 行删除
- 提交: `813d84e`

---

## [V1.1.0] - 2026-06-16

### Added
- feat: **核心实现** — 添加 halucatch_core.py 和 README
  - `halucatch_core.py`: 504 行核心代码
  - `README.md`: 99 行项目说明
- 影响: 新增 2 个文件, 603 行
- 提交: `952f26b`

---

## [V1.0.0] - 2026-06-16

### Added
- feat: **初始版本** — HaluCatch SKILL.md
  - AI Skill 可靠性检查器核心设计文档
  - 231 行 SKILL.md
  - 基础 .gitignore
- 影响: 新增 2 个文件, 235 行
- 提交: `ad24145`

---

## 版本统计

| 版本 | 发布日期 | 提交哈希 | 类型 | 影响范围 | 说明 |
|------|----------|----------|------|----------|------|
| V1.6.0 | 2026-06-17 | `f445999` | feat | 核心代码 + 测试 (60行) | 数据驱动型护栏分层 |
| V1.5.1 | 2026-06-17 | `768d725` | chore | .gitignore (1行) | 忽略 .clawhub 目录 |
| V1.5.0 | 2026-06-17 | `baaaaa2` | feat | 核心代码 + 测试 | 去语言化架构 |
| V1.4.1 | 2026-06-17 | `65631d4` | feat | SKILL.md + 核心 | Phase 4 闭环 SOP |
| V1.4.0 | 2026-06-17 | `856f682` | feat | 文档 + 流程图 | 闭环验证流程 |
| V1.3.1 | 2026-06-17 | `a2895f7` | chore | 删除 4 个文档 | 清理过期测试文档 |
| V1.3.0 | 2026-06-17 | `bd76b90` | feat | 核心 + 测试 + 文档 | 代码风险检测增强 |
| V1.2.1 | 2026-06-17 | `50a8780` | feat | .gitignore (1行) | 更新 gitignore |
| V1.2.0 | 2026-06-17 | `813d84e` | refactor | 7 个文件, 731 行 | P0-P3 全面修复 |
| V1.1.0 | 2026-06-16 | `952f26b` | feat | 2 个文件, 603 行 | 核心实现 |
| V1.0.0 | 2026-06-16 | `ad24145` | feat | 2 个文件, 235 行 | 初始版本 |

**总计：12 个版本（11 次提交）**

---

## 分类统计

### 按提交类型
- **feat**: 8 次 (73%)
- **refactor**: 1 次 (9%)
- **chore**: 2 次 (18%)

### 按版本号规则
- **中间版本更新** (1.x.0): 7 次 (功能级更新)
  - V1.1.0: 核心实现
  - V1.2.0: 架构重构
  - V1.3.0: 代码风险检测
  - V1.4.0: 闭环验证
  - V1.5.0: 去语言化
  - V1.6.0: 数据驱动型护栏分层
  
- **小版本更新** (1.0.x): 4 次 (修复/增强/chore)
  - V1.2.1: gitignore 更新
  - V1.3.1: 清理文档
  - V1.4.1: SOP 实现
  - V1.5.1: 忽略目录

### 代码变更统计
- **总代码行数**: 235 + 603 + 731 + ... ≈ 2000+ 行
- **平均每次提交**: ~200 行
- **最大单次变更**: V1.2.0 (731 行新增)

---

**生成时间**: 2026-06-17  
**生成方式**: 基于 `git log` + `git diff-tree` 分析实际代码变更
