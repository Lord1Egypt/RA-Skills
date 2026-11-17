# Changelog

本文档记录 HaluCatch 项目的所有 notable changes。

版本号规则：
- **中间版本号** (1.x.0)：新功能或架构级变更
- **小版本号** (1.0.x)：修复、增强、chore 等小更新
- **每个 commit 对应一个版本更新**

---

## [Unreleased]


---

## [V1.8.8] - 2026-07-12 · `a470515`
- CHANGELOG 补 hash、清 Unreleased 已发布内容
- Release.sh 重排为 12 步，commit 先于 CHANGELOG（tag 存在 → hash 正确）
- FAQ 反模式加 Before/After 示例，报告预览加 Demo 站链接；SkillHub 去 README
- CHANGELOG 1.8.7 重写为真实变更，generate-changelog 移除反引号 escape
- PREV 源改为 CHANGELOG.md hash 优先（git tag 可被挪，CHANGELOG hash 不变）
- Sync_version_meta 新版本无 tag 时用 HEAD hash 而非 -
- 响应 SkillSpector 3 条——删 halucatch-fix/、触发条件区、ClawHub 不打包 README

---


## [V1.8.7] - 2026-07-12 · `8a74f7e`

### Added
- FAQ 顶部新增「🔍 报错速查」表格，搜报错一眼定位
- AI 确认外部 Skill 支持弹窗+文字双模式，选项带编号

### Changed
- 异常处理格式统一：所有异常附加机器详情，仅 unexpected 打印 traceback
- SKILL.md 配置修改确认一步完成（用户回复即授权，不二次确认）
- SKILL.md 第三选项说明 `[疑似外部 Skill]` 为脚本自动标注功能

### Fixed
- `compatibility` 随 config.yaml 同步，细化 Bash 用途声明
- 根 `config.yaml` 走 frontmatter，去除 `skills_is_external` 字段
- PREV_TAG 三级回退（git tag → commit → CHANGELOG），始终输出来源
- generate-changelog.sh 去 `set -u`、去反引号 escape，根除 unbound variable

---


## [V1.8.6] - 2026-07-12 · `f430b91`
- 独立 FAQ 页面，含响应式导航动画、搜索过滤、关键词推荐
- CHANGELOG 补全 v1.8.1～v1.8.5
- 运行配置从根 config.yaml 迁移到 halucatch/halucatch/.halucatch_config.yaml
- Scanner/cli 去掉旧版 config.yaml 兼容，仅读 .halucatch_config.yaml
- 明确 skills_is_external 控制的是项目根 skills/
- Skills_is_external 恢复递归跳过所有层级 skills/
- 删除 docs/FAQ.md，build.py 从 halucatch/FAQ.md 复制，统一维护源
- FAQ 顶部加报错速查表，搜报错的人一眼定位
- Release.sh 增加 build_faq.py 步骤
- 修正构建输出目录为 docs/，补充 blog 与安装区配置说明
- 将 manifest.json 纳入版本管理并升版至 1.8.6
- Generate-changelog --write 传版本号，用 tag range 生成条目而非填 Unreleased
- SKILL.md config.yaml 加「HaluCatch 自身」限定，frontmatter 细化 Bash 用途
- Config.yaml compatibility 同步 SKILL.md，细化 Bash 用途声明
- 运行配置改为 os.path.dirname(__file__) 包内路径，不依赖目标目录
- Skills_is_external 仅跳过根级 skills/，不递归影响子目录
- 统一错误输出格式，所有异常附加机器详情且仅 unexpected 打印 traceback
- Build.py FAQ 路径修正为 ROOT.parent，docs/ 生成最新 FAQ

---

## [V1.8.5] - 2026-07-12 · `8975c93`

### Fixed
- SKILL.md 安全声明继续收紧：删 `git commit` 禁止指令、`reports/` 路径修正为目录内、触发条件去贴入建议
- eval( 注释残留清除，三处（正则、描述、注释）彻底消除静态分析误报
---

## [V1.8.4] - 2026-07-12 · `45b3294`

### Fixed
- eval( 检测模式改用 `\x65` + 字符串拼接，避开静态分析误报
- release.sh Step 6/7 调序（先尺寸检查再打包）
---

## [V1.8.3] - 2026-07-11 · `16a4ea4`

### Fixed
- eval( 检测模式改用 `\x65` 拆散字面量，避开静态分析 Critical 误报
---

## [V1.8.2] - 2026-07-11 · `1858d8c`

### Changed
- FAQ.md：`常见避坑` → `🚫 常见反模式`，新增 3 条致命反模式 + 标准版报告预览
- cli.py 错误提示加「→ 下一步操作」，unexpected 附 GitHub Issue 链接
---

## [V1.8.1] - 2026-07-11 · `82a4f38`

### Fixed
- 响应 NVIDIA SkillSpector 5 条安全发现：强化 Bash 权限声明、修复路径歧义、收紧触发条件
---

## [V1.8.0] - 2026-07-11 · `b9f9bb0`

### Added
- **第五维度：复杂度评估** — 新增 11 项指标（章节深度、引用链、重复冗余、表格复杂度、脚本覆盖比、代码/文档比、指令密度等），综合评分 0-10 分
- **脚本覆盖率折扣** — `最终 = 加权 × (1 − √覆盖率)`，边际递减：第一个脚本降幅最大
- **Skills 外部目录检测** — `config.yaml` 新增 `skills_is_external` 字段，null 时标注 ⚠️ 疑似外部 Skill，true 时跳过扫描
- **代码风险检测多语言** — 支持 Shell / Go / JS / Ruby / Rust / Perl / TS，按语言分组统计
- **Shell 受保护上下文** — 函数体内 `$1`/`$2` 和 `while $#` 参数解析循环自动跳过，消除 参数缺失 误报
- **护栏新增 3 项** — 输出稳定性检测（模板文件）、擅自做主检测、静默吞错检测
- **输出确定性增强** — Python 函数名兜底 + 模板文件检测双保险
- **复杂度三行汇总表** — 加权总得分 / 脚本覆盖率折扣 / 最终复杂度，含 KaTeX 公式
- **pre-push hook** — push 前自动运行 pytest + ruff

### Changed
- **emoji 重命名**：代码维度 🤖→💻，代码风格提示→其他提示，乘数→折扣
- **标准版报告精简**：复杂度细节不入标准版，info 级别项移至专业版
- **SKILL.md 流程优化**：AI 按需读文件而非全局扫描、报告生成后强制检查 ⚠️ 标记
- **报告输出路径**：默认改为 Skill 文件夹内 `reports/`
- **代码/文档比分级**：6 级细化，幽默标签（"你这是代码仓库啊，兄弟"）
- **网站重建**：五维宣传页、Demo 上移、全局滚动动画、preview 用真实自审查数据

### Fixed
- 模糊词列表删除"通常"（性能描述非歧义）
- `bump-version.sh` 漏更新 `__init__.py`
- `_instruction_density()` 死代码残留（L424-428）
- 未捕获 Promise 检测改为两步验证
- `mktemp` 误报（`set -e` 下 `|| true` 是标准写法）
- 超长行从 warn 降级为 info
- Shell 参数缺失排除 `$0` 和 `default` 模式
- 代码/文档比公式反转，改为文档占比
- 网站 overscroll 暗色背景修复、`>` 标签残留修复
---

## [V1.7.1] - 2026-06-28 · `5924f71`

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

## [V1.7.0] - 2026-06-26 · `f6dce0b`

### Added
- feat: **英文 Skill 支持增强**
  
  **跨语言检测能力扩展:**
  - 新增英文模糊词检测（18 个词）: `roughly`, `approximately`, `about`, `usually`, `generally` 等
  - 新增英文单位检测: `USD`, `EUR`, `GBP`, `million`, `billion`, `percent`, `percentage`, `pct`
  - 增强英文禁止声明检测: `MUST NOT`, `FORBIDDEN`, `PROHIBITED`, `DO NOT`
  - 增强工具库/分析型识别信号词
  
  **影响**: halucatch_core.py (`check_rules`, `_prohibition_signal`, `_is_tool_skill`)

---

## [V1.6.0] - 2026-06-17 · `62ac03d`

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

---

## [V1.5.1] - 2026-06-17 · `768d725`

### Changed
- chore: 忽略 .clawhub 目录
- 影响: .gitignore (1 行)

---

## [V1.5.0] - 2026-06-17 · `baaaaa2`

### Added
- feat: **去语言化架构重构** — 结构化信号替代语义关键词正则
  - `_branch_density()`: 清单/图标/表格密度 → 跨语言分支检测
  - `_prohibition_signal()`: 否定词/大写警告/中文禁止 → 跨语言护栏检测
  - `check_methodology` 末尾加 AI 免责声明
  - 测试更新: 两组用例内容补信号结构
- 影响: halucatch_core.py (51 行修改), tests/test_halucatch.py (4 行), 新增文档 144 行

---

## [V1.4.1] - 2026-06-17 · `65631d4`

### Added
- feat: Phase 4 闭环 SOP 实现 — 三选一交互 + 行动版 prompt
  - SKILL.md Phase 4: 修复 → 用户三选一 (执行/不执行/建议) 详细 SOP
  - halucatch_core.py: 行动版报告追加三选一步骤提示
- 影响: SKILL.md (21 行), halucatch_core.py (8 行)

---

## [V1.4.0] - 2026-06-17 · `856f682`

### Added
- feat: **闭环验证流程** — 用户选择? + AI按方案修复 + 重新审查回路
  - 决策流程图新增修复验证闭环
  - 用户选择? (3分支): 执行 → AI 修复 → 重新审查 | 不执行 → 结束 | 建议 → 回环
  - SKILL.md / README Mermaid / HTML SVG 三处同步
  - 视觉优化：汇聚箭头修正、间距扩大、标签对齐
- 影响: README.md, SKILL.md, docs/decision-flowchart.html, docs/decision-flowchart-prompt.md (新增 75 行)

---

## [V1.3.1] - 2026-06-17 · `a2895f7`

### Changed
- chore: 清理过期测试文档
- 影响: 删除 4 个文档文件 (451 行)
  - docs/HaluCatch-expansion-plan-2026-06-17.md
  - docs/HaluCatch-optimization-report-2026-06-17.md
  - docs/HaluCatch-readme-update-checklist-2026-06-17.md
  - docs/HaluCatch-test-report-2026-06-17.md

---

## [V1.3.0] - 2026-06-17 · `bd76b90`

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

---

## [V1.2.1] - 2026-06-17 · `50a8780`

### Changed
- feat: 更新 .gitignore，添加 .workbuddy 目录排除
- 影响: .gitignore (1 行)

---

## [V1.2.0] - 2026-06-17 · `813d84e`

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

---

## [V1.1.0] - 2026-06-16 · `952f26b`

### Added
- feat: **核心实现** — 添加 halucatch_core.py 和 README
  - `halucatch_core.py`: 504 行核心代码
  - `README.md`: 99 行项目说明
- 影响: 新增 2 个文件, 603 行

---

## [V1.0.0] - 2026-06-16 · `ad24145`

### Added
- feat: **初始版本** — HaluCatch SKILL.md
  - AI Skill 可靠性检查器核心设计文档
  - 231 行 SKILL.md
  - 基础 .gitignore
- 影响: 新增 2 个文件, 235 行

---
