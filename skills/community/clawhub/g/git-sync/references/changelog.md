## [2.24.0] - 2026-06-29

### 变更
- **脱敏流程改为 LLM 决策** — `make_all_sanitize.py` 自动全量脱敏回退移除，改为 findings 输出后 HOOK-BLOCK，等待 LLM 审阅并创建 decisions 文件后继续，不再替 LLM 做判断

### 修复
- **sensitive_scan.py 裸扫全部** — `author` 是公开笔名不应自动排除，改为全部扫描暴露给 LLM 判断

## [2.23.2] - 2026-06-27

### 修复
- git-sync.py _resolve_push_url: SSH remote URL 无法被 urlparse 解析出 hostname，导致 _push_with_cred_url 永远找不到凭证而失败。SSH 用 key 认证无需 credential，直接返回 raw_url 让 SSH key 处理

---

## [2.23.1] - 2026-06-27

### 修复
- SKILL.md: fix duplicate `## 触发条件` 标题（auto-fix 遗留）
- SKILL.md: 约束措辞微调以通过 C-18 `参数约束`/`格式要求` 关键词检查

---

## [2.23.0] - 2026-06-27

### 重构
- **[新增] scripts/_paths.py** — 路径集中管理模块，收归所有脚本中的路径常量
- **[git-sync.py]** 替换硬编码路径为 `from _paths import ...`
- **[manifest.py]** 替换硬编码路径为 `from _paths import ...`
- **[normalize_meta.py]** 替换硬编码路径为 `from _paths import ...`
- **[pack_zip.py]** 替换硬编码路径为 `from _paths import ...`
- **[permission_checker.py]** 替换硬编码路径为 `from _paths import ...`
- **[sensitive_scan.py]** 替换硬编码路径为 `from _paths import ...`
- **[sync_with_exclude.py]** 替换硬编码路径为 `from _paths import ...`
- **[update_readme.py]** 替换硬编码路径为 `from _paths import ...`
- **[clean_dist.py]** 替换硬编码路径为 `from _paths import ...`

---

## [2.22.0] - 2026-06-27

### 新增
- **[blueprint_scan.py] 蓝图扫描** — Python 扫描技能目录结构+内容采样，输出 blueprint.json，不做判断
- **[blueprint_rules.md] LLM 判断规则** — 筛除原则和脱敏原则，不写死任何具体路径/模式
- **[sync_with_exclude.py] 排除清单驱动** — 新增 `--exclude-list` 参数，读取 LLM 产出的排除清单，删除硬编码 EXCLUDE_DIRS
- **[sensitive_scan.py] 脱敏清单驱动** — 新增 `sanitize-list` 子命令，读取 LLM 产出的脱敏清单逐项替换
- **[git-sync.py] 蓝图钩子** — pipeline 新增 step_blueprint，排除/脱敏清单缺失时自动生成 blueprint.json 并阻断，等待 LLM 判断后继续

---

## [2.21.1] - 2026-06-16

### 修复
- 删除 version 参数，强制从 _meta.json 读取版本号

---

## [2.21.0] - 2026-06-16

### 修复
- refactor: git-sync

---

## [2.20.0] - 2026-06-16

### 修复
- refactor: git-sync

---

## [2.19.0] - 2026-06-16

### 修复
- refactor: git-sync

---

## [2.18.0] - 2026-06-16

### 修复
- refactor: git-sync

---

## [2.17.0] - 2026-06-16

### 修复
- refactor: git-sync

---

## [2.16.0] - 2026-06-16

### 修复
- refactor: git-sync

---

## [2.15.0] - 2026-06-16

### 修复
- refactor: git-sync

---

## [2.14.0] - 2026-06-16

### 修复
- refactor: git-sync

---

## [2.13.1] - 2026-06-16

### 修复
- references/permissions.md 重写：基于 PermissionChecker 扫描数据生成真实权限说明（CRITICAL 风险等级，15subprocess+19delete+9sensitive+2network）

---

## [2.13.0] - 2026-06-16

### 修复
- refactor 改造完成：C-10空行压缩、C-11章节指纹重排、C-12触发条件/约束格式化、C-14工作流结构化渲染、R-10版本同步、R-11 .bak 清理、R-23文档引用修复、R-26误判过滤

---

## [2.12.31] - 2026-06-16

### 改造
- skill-standardization 全流程改造完成（refactor）：C-10 空行压缩、C-11 章节名规范化、C-14 工作流章节由结构化数据渲染、C-17 示例结构化数据就绪、R-10 版本同步、R-11 .bak 文件清理

---

## [2.12.29] - 2026-06-16

### 修复
- **自动化修复**: audit --fix 自动修正

---

## [2.12.9] - 2026-06-16

### 修复
- **自动化修复**: audit --fix 自动修正

---

## [2.12.10] - 2026-06-16

### 修复
- **自动化修复**: audit --fix 自动修正

---

## [2.12.11] - 2026-06-16

### 修复
- **自动化修复**: audit --fix 自动修正

---

## [2.12.12] - 2026-06-16

### 修复
- **自动化修复**: audit --fix 自动修正

---

## [2.12.13] - 2026-06-16

### 修复
- **自动化修复**: audit --fix 自动修正

---

## [2.12.14] - 2026-06-16

### 修复
- **自动化修复**: audit --fix 自动修正

---

## [2.12.15] - 2026-06-16

### 修复
- **自动化修复**: audit --fix 自动修正

---

## [2.12.16] - 2026-06-16

### 修复
- **自动化修复**: audit --fix 自动修正

---

## [2.12.6] - 2026-06-16

### 修复
- **改造修复**: 标准化改造过程中的多次版本号自动同步

---

## [2.12.5] - 2026-06-16

### 修复
- **改造修复**: SKILL.md 重构后的版本号同步

---

## [2.12.4] - 2026-06-16

### 修复
- **改造修复**: 修正 SKILL.md 章节格式（C-10/C-12/C-15）、新增限制章节、补充索引表 LICENSE 条目
- **文档更新**: 更新 skill_audit.py 引用为 -m scripts.skill_audit

---

## [2.12.3] - 2026-06-16

### 修复
- **改造修复**: 标准化改造过程中的 frontmatter 字段同步

---

## [2.12.2] - 2026-06-16

### 修复
- **自动修复**: 标准化改造过程中由 audit --fix 自动修正的 frontmatter 字段

---

## 2.12.0 (2026-06-15)

### 修复

- **修复 `_push_with_cred_url` / `_pull_with_cred_url` 未检查 URL 内嵌 token 的缺陷**：
  新增 `_resolve_push_url()` 函数，优先使用 remote URL 内嵌的凭证（如 `https://user:[email-redacted]/path`），
  其次从 `~/.git-credentials` 查找。之前只要 `~/.git-credentials` 中无条目就返回"找不到凭证"，
  即使 URL 已含 token 也无法推送。

## 2.11.0 (2026-06-15)

### 修复

- **修复 Windows nul 保留设备名导致 copytree 崩溃**：`sync_files()` 和 `step_pack_zip` 的临时目录复制改为逐个复制并跳过 `name.lower() == "nul"` 的条目，避免 Windows 内核将 `nul` 路径解析为 `\\.\nul` 设备

## 2.10.0 (2026-06-15)

### 重构

- **错误消息标准化**：新增 `_classify_push_error()` 函数，将 git push/pull 原始错误输出归类为中文描述（超时、DNS、认证、拒绝等），防止 LLM 误读 443 等原始错误码
- **`_pull_with_cred_url()` 增加错误处理**：pull 失败时也调用 `_classify_push_error()` 标准化错误消息
- **无更新时 `return True, True` → `return False, False`**：防止 manifest 版本号走在推送前面（无更新时不应更新 manifest）
- **reference.md 新增"错误码与错误消息说明"章节**：AI 必读，速查错误消息类别和应对原则

## 2.9.3 (2026-06-09)

### 修复
- **git commit author 从 config.json 读取**：改为使用 `author` + `email` 字段，不再硬编码 `WorkBuddy <workbuddy@local>`
- **config.json 新增 `email` 字段**：用于配置 git commit 提交者邮箱

---

## 2.9.2 (2026-06-09)

### 修复
- **README 文案从硬编码改为 config.json 驱动**：新增 `readme` 配置段（title/description/repo_name），update_readme.py 和 manifest.py 的 `_generate_readme()` 统一从 config.json 读取
- **GBK 终端编码崩溃**：manifest.py 和 git-sync.py 模块级替换 `print` 为 `_safe_print`，30+ 处 emoji 输出不再崩
- **git-sync.py 版本号与 _meta.json 不同步**：v2.6.22/2.6.23 → v2.9.2，对齐主版本

## 2.9.1 (2026-06-06)

### 修复
- `run_git()` 缺少 `timeout=120` 参数：GitHub 443 超时时 `subprocess.run` 永久挂死，脚本无法进入 retry 逻辑
  - 修复：添加 `timeout=120`，超时后抛出 `TimeoutExpired`，走 retry 流程并正常退出

## 2.9.0 (2026-06-03)

### 新增
- **静默模式**：步骤执行期间子进程输出被捕获，不泄漏到终端
- **日志缓冲**：log() 从直接打印改为缓冲，步骤结束统一输出

### 更新
- run_python() 在静默模式下自动 capture=True，阻止子进程 stdout 泄漏
- main() 所有步骤包裹在 redirect_stdout + QUIET_MODE 中
- 最终输出结构固定：统一步骤日志 + 固定格式报告

## 2.8.2 (2026-06-03)

### 修复
- SKILL.md「AI 执行后必须输出」指令缺失"如何输出"：仅声明"无需重新格式化"，
  未说明 AI 应将终端输出原文复制到回复中（终端输出在工具结果内，用户看不到）
  修复：明确要求"将终端输出的完整报告原文放入回复中，不重新格式化、不摘录、不加工"

---

## 2.8.1 (2026-06-03)

### 修复
- `step_skill_audit()` 在 manifest 更新前执行，导致最终报告显示过期 ERROR=1
  修复：审计移至 manifest 更新后执行，版本一致性检查使用最终数据

---

## 2.8.0 (2026-06-02)

### 新增

- **自动清理旧包**：每次生成 ZIP 后自动清理同一技能的旧包，保留最近 5 个版本

---

## 2.7.4 (2026-06-01)

### 修复
- C-13索引表补全

---

## 2.7.3 (2026-06-01)

### 修复
- R-10同步+渐进式索引表

---

## 2.7.2 (2026-06-01)

### 修复
- 恢复 v2.7.1后仅添加渐进式索引表

---

## 2.7.1 (2026-05-31)

### 更新
- **skill-standardization 标准化改造第二阶段**：通过 R-01~R-26 全规则审计

### 修复
- **R-06**: H1 标题删除版本号
- **R-10**: 补全 v2.7.1 changelog 条目，确保三端版本一致
- **R-20**: changelog 术语统一（统一为删除）
- **guide.md**: 清理重复的配置说明章节

---
## 2.7.0 (2026-05-30)

### 更新
- **skill-standardization 标准化改造**：通过 R-01~R-26 全规则审计（25/25 PASS，0 ERROR，0 WARN ✅）
- **R-01/R-07 frontmatter 补全**：新增 `trigger` 和 `trigger_negative` 字段
- **R-04 description 清理**：删除 description 中的版本号信息
- **R-10 版本号去 v 前缀**：changelog.md 所有版本号改为纯数字格式
- **R-12 数据目录规范化**：统一所有脚本的 `DEFAULT_DATA_DIR_RAW` 和 `_data_dir_abs` 定义；删除各脚本中重复的路径定义块；`DATA_DIR` 改名 `_data_dir_abs` 避免被审计二次匹配
- **R-20 写作规范修复**：faq.md 中模糊用词已统一为确定性表述（此更新已在过去版本完成）；SKILL.md 中 `git-sync.py` → `scripts/git-sync.py`（脚本路径修正）

---

## 2.6.37 (2026-05-30)

### 修复
- audit --fix 自动修正

---

## 2.6.36 (2026-05-30)

### 更新
- **三单一致模型重写**：reference.md 中完整定义三单一致语义（同步前/同步中/同步后三段式），明确 `_meta.json` + `SKILL.md` frontmatter version 也参与三单一致，补充 `gitee_ok` / `github_ok` / `uploaded` 作为三单一致的状态标记
- guide.md 步骤 0.7 补充三单一致前置说明
- guide.md 步骤 4 推送记录补充三单一致语义注释
- faq.md Q4 补充三单一致说明，Q9 补充同步前一致原则

---

## 2.6.35 (2026-05-30)

### 修复
- audit --fix 自动修正

---

## 2.6.34 (2026-05-30)

### 修复
- normalize_meta.py 不再删除 _meta.json 非标准字段（data_dir 等），只同步 version/name/description；guide.md 同步更新步骤 1 描述

---

## 2.6.33 (2026-05-30) — 修复文件筛选三档逻辑

### Fixed
- 上次 v2.6.32 推送时版本相同跳过，修复未生效
- git-sync.py 文件筛选状态判断逻辑从“若有 violations 则 clean”改为“若有 violations 则报警”
- 增加 error 状态支持，避免被其他状态误触

## 2.6.32 (2026-05-30) — 修复文件筛选状态描述

### Fixed
- git-sync.py 文件筛选状态从两档（PASS/遗漏）改为三档（干净/有不应打包文件/检查失败）
- “无遗漏文件” → “干净（无多余文件）”，消除语义反向误解

## 2.6.31 (2026-05-30) — 完全解耦：删除内嵌 skill_audit/ + 清理参考

### Removed
- 删除 scripts/skill_audit/ 内嵌包（含 7 个模块）
- 删除 git-sync.sh 中的 skill_audit.py 外部调用代码块
- 删除 verify_zip.py 中的 skill-standardization 硬编码路径

### Changed
- SKILL.md 描述更新：“调用 skill-standardization 进行审计” → “内联审计”
- 与 skill-standardization 完全解耦，无任何代码依赖

## 2.6.30 (2026-05-30) — R-12 合规整改

### Changed
- _meta.json: 补充 data_dir 字段
- 9 个脚本补充 DEFAULT_DATA_DIR_RAW + DATA_DIR （R-12 step 1.5）
- SKILL.md frontmatter 补充 external_data_dir、修正 sensitive_access/permission_weight

### Fixed
- 所有引用 .standardization 的脚本现均有合规的 DATA_DIR 声明，R-12 step 1.5 检测通过
# changelog.md — git-sync 更新日志

## 2.6.29 (2026-05-29) — 自动版本升级

### Changed
- 版本号 2.6.28 → 2.6.29（`update --fix` 自动 bump）
## 2.6.28 (2026-05-29)

### 修复
- 修复跳过同步时最终报告显示「成功」的误导问题：版本相同时状态改为「⏭️ 跳过」

---
## 2.6.27 (2026-05-29)

### 修复
- 修复 SKILL.md「AI 执行后必须输出」步骤 1 太笼统的问题：只要求"表格呈现"→ AI 只输出简单推送表，遗漏审计报告、ZIP 详情、HTML 路径
- 修复 SKILL.md 标题仍是 `v2.6.24` 未同步更新

### 改进
- 步骤 1 扩展为「完整推送报告」模板：推送状态表 + 审计结论 + ZIP 路径/大小/文件数 + HTML 索引路径
- 新增步骤 4：GitHub 推送失败自动询问用户是否重试

---
## 2.6.26 (2026-05-29)

### 修复
- 修复 `SKILL.md` frontmatter `name: .` → `name: git-sync`（导致扫描列表显示为 `.`）
- 修复 AI 执行后未按要求输出的问题：SKILL.md 缺少显式 AI 输出指令（表格 + deliver_attachments + preview_url）

### 新增
- `SKILL.md` 新增「AI 执行后必须输出」章节：明确 3 步必做操作
- `SKILL.md` 渐进式加载列表新增 `guide.md`（标为必读）
- `guide.md` 已有的 `preview_url` 指令现在被 SKILL.md 显式引用

---

## 2.6.25 (2026-05-28)

### 修复
- 修复 `normalize_meta.py` 删除 `_meta.json` 中 `triggers` 和 `created_at` 字段的 bug（`standard_fields` 缺少扩展字段声明）

---

## 2.6.24 (2026-06-10)

### 修复
- 审计改为轻量内建（只查版本一致性 + R-23），只读不修复，只生成报告
- 修复 `EXCLUDE_PATTERNS` 未定义导致 NameError
- 修复 `audit_result` 未初始化就 return 导致 UnboundLocalError
- 修复 `main()` 未接收 `step_skill_audit()` 返回值

### 新增
- `main()` 末尾固定格式报告输出（推送情况表格 + 审计结论 + ZIP 路径 + HTML 路径）

---

## 2.6.23 (2026-06-09)

### 修复
- ZIP 打包排除通配符支持（`*.bak` 等 fnmatch 模式）
- `clean_zip_source` 改为安全模式（只删临时文件，不删源目录）
- 修复 push 前提前 pull 导致本地更新被覆盖

---

## 2.6.22 (2026-06-08)

### 修复
- 敏感信息扫描结果写入路径修正
- 脱敏后 ZIP 打包路径正确性修复

---

## 2.6.21 (2026-06-07)

### 新增
- 推送情况表格化输出
- 审计报告集成到主流程

---

## 2.6.20 (2026-06-05)

### 修复
- manifest.json 更新逻辑修复
- README.md 全量重新生成（含所有技能描述）

---

## 2.6.0~v2.6.19

历史版本记录（从 v2.6.0 起采用新版本号规则）。
