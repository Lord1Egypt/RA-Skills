## 1.3.0 (2026-06-11)

### 新增

- **inject 模式**：`scripts/component_inject.py` — 向现有 .tex 增量插入组件，自动拆分导言区/正文，支持 lualatex/xelatex/pdflatex 引擎检测和语法转换
- **convert 模式**：`scripts/convert.py` — pdfLaTeX → LuaLaTeX 全文档转换，原文件不动，输出新文件 + 转换报告
- **语义路由**：`scripts/workflow_router.py` — 分析用户输入自动匹配 4 条流程线，含语义验证钩子 + 文件大小钩子
- **流程守卫**：`scripts/workflow_state.py` — 四流程线步骤依赖检查，跳过则拦截，状态持久化；所有流程线末尾强制 validate + report；line2/line3 首步强制 backup
- **结构化报告**：`scripts/workflow_report.py` — 按流程线生成 Markdown 表格报告
- **写入守卫**：`scripts/write_guard.py` — AST 扫描直接 `open() 'w'` / `os.remove()` 等违规写入
- **引擎路径智能查找**：`find_engine()` 支持注册表 + 系统/用户安装路径 + TeX Live 年份扫描 + `where/which` + 安装指引（含清华大学/阿里云镜像链接）

### 修复

- **extract.py fancyhdr 死循环**：`j = i` 导致内层循环立即 break 而外层 i 不推进，改为 `j = i + 1`
- **个人隐私信息清理**：body.txt 中 `\author{思淼}` 替换为 `__AUTHOR__` 占位符；文档中 sm001 路径泛化；联系方式移除
- **safe_delete() 统一删除接口**：`template.py` 的 `os.remove()`/`unlink()` 迁移到 `safe_delete()`
- **异常处理覆盖率**：`convert.py`、`workflow_state.py` 增加文件读写 try/except
- **产出物路径合规**：`.function-test_blueprint.json` 等迁至 `.standardization/latex-modular/data/`
- **skill-standardization 备份格式统一**：`skill_audit/__init__.py` 备份从 `shutil.copytree()` 改为 `shutil.make_archive(zip)`

### 变更

- 引擎策略从「不推荐 pdflatex」改为「inject 模式支持 pdflatex 动态转换」
- 4 条流程线确立：新建文档 / 改造（三分支） / 增量编辑 / 组件复用闭环

---

## 1.2.4 (2026-06-02)

### 修复

- **组件库目录树同步**：SKILL.md 组件库目录树从 .tex 更新为 .txt，删除不存在的幻影条目，仅保留磁盘上实际存在的 11 个文件
- **组件表路径修复**：references/component-spec.md 组件表中 standard-table 改为 table-style

---

## 1.2.3 (2026-06-02)---

# 版本更新记录

## 1.2.2 (2026-06-01)

### 修复

- 所有 `.tex` 组件文件改为 `.txt` 扩展名，适应平台文件类型限制
- 更新 manifest 路径和脚本中对应的文件引用

## 1.2.1 (2026-06-01)

### 修复

- 组件目录从 `components/` 迁移至 `scripts/components/`，满足平台文件类型要求

## 1.2.0 (2026-06-01)

### 新增

- **模板库系统**：新增 `scripts/templates/` 目录，模板定义为 JSON 格式，包含 body_template、styles、sample_sections 等字段
- **template.py 新增参数**：`--template` 按名加载模板、`--list-templates` 列出模板、`--show-template` 查看详情、`--search` 搜索、`--save-as` 保存自定义模板、`--content` 注入正文、`--save-description` 模板描述
- **内置模板**：article(论文) / report(报告) 两种预设模板，`--type` 旧版参数自动映射到模板库
- **`--type` 完全兼容**：旧版参数使用方式不变，内部自动加载模板库

### 修复

- template.py 旧版 `--no-sample` 骨架降级路径修复

## 1.1.0 (2026-06-01)

### 新增功能

- **template 模式实现**：新增 `scripts/template.py`，支持 article/report 两种文档类型
  - 根据文档类型自动生成结构完整的示例正文
  - 展示所有组件的使用方法（mylist、timu、seeref 等）
  - 支持 `--no-sample` 只输出骨架
  - 支持 `--output-mode tex|pdf` 选择输出形式
  - 支持 `--skip-validation` 跳过编译验证
  - 验证为默认核心步骤（不再是可选项）

### 修复

- **标准化改造**：补齐 `_meta.json`、frontmatter `trigger`/`data_dir` 字段，修复 H1 版本号

## 1.0.1 (2026-06-01)

### 修复

- **manifest.json 格式统一**：dict 改 list，与 compose.py / component_manager.py 兼容
- **extract.py/extract_simple.py 路径前缀修复**：删除 components/ 前缀，防止路径翻倍
- **compose.py 引擎查找**：新增 find_engine() 和 --engine 参数，不再硬编码 lualatex
- **compose.py dict 兼容**：导入时自动将 dict-format 转为 list 格式
- **compose.py 组件内嵌宏包不吞内容**：非纯宏包组件提取 usepackage 行后保留剩余内容
- **compose.py 宏包去重增强**：规范化去重，捕获多余空格等变体
- **manifest.json 补 body 组件**：使正文能正确拼入最终文档
- **refactor.py manifest 输出**：从 dict 改为 list 格式
- **refactor.py input 相对路径**：自动计算组件目录相对输出文档的路径
- **清理冗余文件**：删除 build_manual.py 应急脚本

## 1.0.0 (2026-05-27)

### 初始版本

- 创建 `latex-modular` 技能（基于用户提供的荣事达食材净化机技术方案 LaTeX 代码）
- 实现 5 种工作模式：extract / compose / refactor / validate / template
- 创建核心 Python 脚本（位于 `scripts/`）
- 创建 `references/` 渐进式加载文档
- 提取用户 LaTeX 代码中的组件（23 类组件）
- 确认系统已安装 lualatex（`/c/Program Files/MiKTeX/miktex/bin/x64/lualatex`）
- 确认 managed Python 3.13.12 可用

### 已知问题

- [ ] `extract.py` 的组件分类规则（`CLASSIFY_RULES`）为启发式，可能漏提或误提
- [ ] `compose.py` 的宏包顺序（`PACKAGE_ORDER`）可能不适合所有文档
- [ ] `validate.py` 的错误解析（`ERROR_PATTERNS`）可能漏报或误报
- [ ] `refactor.py` 的模块分类规则（`MODULE_RULES`）为启发式，可能不完全准确
- [ ] 暂未实现 GUI 或 Web 界面（当前为命令行工具）
- [ ] 图片路径中的中文可能在某些系统上报错（建议用英文路径）

### 下一步计划

- [ ] 编写完整功能测试（覆盖 extract/compose/refactor/validate 四种模式）
- [ ] 验证生成的 LaTeX 代码能否无错误编译
- [ ] 增加更多预设模板（如：论文模板、报告模板、提案模板）
- [ ] 支持更多 LaTeX 引擎（pdflatex、platex 等）
- [ ] 增加 CI/CD 集成示例（GitHub Actions、GitLab CI 等）
- [ ] 编写用户手册（PDF + 在线文档）
