## [3.2.0] - 2026-06-26

### 修复
- refactor: hug-html

---

## [3.1.0] - 2026-06-26

### 修复
- refactor: hug-html

---

## 3.0.4 (2026-06-02) -- skill-standardization 改造

### Changed
- R-10: SKILL.md frontmatter tags 和 description 与 _meta.json 同步一致
- R-04: description 删除版本号（_meta.json 和 SKILL.md 均去除）
- R-20: changelog.md 术语统一（删除→删除）
- **R-17**: SKILL.md 缩减至 181 行，非标章节按 body.json 三层规则处理:
   - 四层架构（细化）→ 渐进式: references/architecture.md
   - 能力边界 → 重命名: 限制
   - 错误处理说明 → 合并: 核心能力第14项
   - 附录 → 合并: 核心能力 ### 渐进式文件索引

---

## 3.0.3 (2026-05-31)

### 修复
- **R-01/R-07**: frontmatter 补全 trigger 和 trigger_negative 字段
- **R-04**: description 删除版本号
- **R-06**: 补回缺失的 H1 标题
- **R-10**: changelog 版本号去 v 前缀
- **R-18/R-19**: SKILL.md 补充 antipatterns/faq 引用

---

## 3.0.2 (2026-05-30)

### 修复
- audit --fix 自动修正

---

## 3.0.1 (2026-05-30)

### 修复
- audit --fix 自动修正

---

## 3.0.0 (2026-05-30) — 组件式架构重构

### 重大更新（MAJOR）
- **架构重构**：从预置复合模块模板改为原子组件+声明式组合
  - 删除 14 个固定复合模块，替换为 8 种原子组件（text/image/icon/qrcode/table/divider/spacer/group）
  - 新增 3 级约束系统（fill/fit/clip），递归作用于骨架→模块→组件
  - 新增声明式组合逻辑：方向(row/column)、比例(ratios)、对齐(align/cross_align)
  - 新增  组件引擎， 支持新旧两种 Spec 格式

### Changed
- module_assembler.py 完全重写为组件引擎
- grid_builder.py build_cell_html() 支持 components 字段
- references/module-library.md 重写为组件系统文档
- SKILL.md 四层架构、核心能力、快速开始全面更新

---
## 2.1.4 (2026-05-30)

### 修复
- audit --fix 自动修正

---

## 2.1.3 (2026-05-30) — R-12 合规完善

### Changed
- 所有脚本补充 DEFAULT_DATA_DIR_RAW + DATA_DIR R-12 定义
- _meta.json 补充 data_dir 字段
- 运行 fix_missing_data_dir 一键修复，R-12 审计通过


# Changelog — hug-html



## 2.1.2 (2026-05-30) — skill-standardization 改造 + R-12 脚本补全

### Changed
- 版本号 v2.1.1 → v2.1.2（SKILL.md + _meta.json + 脚本版本字符串三端统一）
- SKILL.md frontmatter 补全 description 字段
- SKILL.md 缩减至 ≤230 行（删除冗余空白行和 H1 标题）
- 尾部版本声明更新为 2.1.2
- 删除 references/faq-q4-fixed.md 遗留文件
- template_generator.py / visual_editor.py / content_filler.py: 补充 DEFAULT_DATA_DIR_RAW + DATA_DIR R-12 定义
- gen_calendar_spec.py: 补充 DEFAULT_DATA_DIR_RAW + DATA_DIR，保留 TEMPLATES_DIR 指向内置模板
- _meta.json: 补充 data_dir 字段

### Fixed
- SKILL.md 版本号与 _meta.json 不一致问题
- 4 个脚本缺少 R-12 合规的数据目录变量声明

## 2.1.1 (2026-05-29) — skill-standardization 合规修正

### Changed
- 版本号 v2.1.0 → v2.1.1（`skill-standardization update --fix` 自动 bump）
- `_meta.json` 补充 `data_dir` 字段，通过 R-12 检查
- `scripts/grid_builder.py`：补充 `DEFAULT_DATA_DIR_RAW` R-12 数据目录字面量声明
- `scripts/gen_test_grids.py`：补充 `DEFAULT_DATA_DIR_RAW` R-12 字面量
- `scripts/module_assembler.py`：补充 `DEFAULT_DATA_DIR_RAW` R-12 字面量

## 2.1.0 (2026-05-29) — 全面中文异常处理 + 能力边界定义

### Added
- 所有脚本集成中文错误处理机制：`show_error()` 函数统一输出 `❌ [错误类型] 说明 + 💡 修复建议`
- `safe_read_json()` / `safe_write_text()` 安全文件操作工具，文件不存在/JSON格式错误/编码异常均有中文指引
- `--debug` 参数支持（grid_builder.py / template_generator.py / visual_editor.py），加参数显示完整堆栈
- SKILL.md 新增「能力边界」章节：✅ 支持场景 / ❌ 不支持场景 / ⚠️ 边界情况，明确回答"这个需求支不支持"
- SKILL.md 新增「错误排查」快速入门表格+「错误处理说明」章节
- SKILL.md 触发场景补充多个复杂需求触发示例
- faq.md 新增 Q11-Q17：错误码对照表、文件找不到修复、布局错乱排查、编辑器无响应、模板固化使用、能力边界判断

### Changed
- `grid_builder.py`: main() 包裹 try/except，所有文件读取/写入改用安全函数
- `template_generator.py`: 重写为 try/except + 中文错误，引入 grid_builder 的 show_error/safe_read_json/safe_write_text
- `visual_editor.py`: 重写为 try/except + 中文错误，模板不存在/读取失败均有中文指引
- `content_filler.py`: 重写为 try/except + 中文错误，文件读取/JSON解析/填充字段校验均有中文提示
- `SKILL.md` frontmatter 版本号 v2.0.4 → v2.1.0

## 2.0.1 (2026-05-29) — 完整交互 + 审计 + 标准化

### Added
- `scripts/grid_builder.py` — 核心网格引擎：N×M 网格布局、单元格合并（rowspan/colspan）
- 两层级模块体系：Base（63 个 CSS 原语）+ Composite（14 个可复用 HTML 组件）
- 内置 7 个方案模板：harmony-app、harmony-dual、calendar-dashboard(交互版)、promo、3x3-merge、4x2-app-card、3x3-mixed-styles
- 泛化三个用户模板：harmony-app，harmony-dual，calendar-dashboard
- `calendar-dashboard` 完整交互版：5×3 网格、年份控制、周末规则勾选、假日区间 CRUD、补班管理、周历视图、总工日统计
- `grid_builder.py` 支持 `scripts` 字段注入自定义 JS，支持 `file` 字段引用外部 JSON 模板
- `scripts/gen_calendar_spec.py` — 交互日历模板生成器
- `scripts/gen_test_grids.py` — 测试 Grid Spec / 模块 JSON 生成工具
- 图片编辑：点击输入 URL + 拖放文件替换（`editable-img` 类），所有复合模块图片均支持
- 编辑器字体控制：字体家族（8种）、字重（100-900）、字号（9-48px）、字色拾色器
- 5 种样式预设：business / academic / festive / mourning / tech，`style_preset` 字段一键切换
- 生成后审计 `audit_html()`：检查 DOCTYPE、标签平衡、网格越界、单元格重叠、backdrop-filter 裁剪、背景异常
- 生成说明 `print_generation_guide()`：每次生成强制输出编辑方法、创作模式、可用资源、审计说明
- 方案模板固化 `--save-as <名>`：将任意 Grid Spec 保存为用户模板，自动版本管理
- `--export-interfaces`：导出完整接口定义 JSON（Grid Spec schema + 63 base + 14 composite + 5 presets）
- `scripts/templates/` 目录：内置文件型模板跟随技能安装（不丢失）
- body 背景智能选择：玻璃卡用 `#000`，普通卡用 card bg 或 `#eef2f7`

### Changed
- `scripts/module_assembler.py` — 重写为 grid-aware（接受 grid spec 而非扁平模块列表）
- `scripts/template_generator.py` — 重写，删除 `gen_body_*` 硬编码，使用 grid 框架，支持用户模板
- `scripts/visual_editor.py` — 增强为网格感知编辑器 + 字体/字重/字号/字色独立控制 + 拖放图片
- `scripts/content_filler.py` — 更新为 v2 接口
- 所有复合模块图标从 `<div>` 改为 `<img>` 可点击换图
- 通用化模板内容：删除具体来源（刻在石头上/灯球色盘），改用通用占位符
- header-entity/header-dual/qr-card/qr-dual/text-img-right 所有图片均加 `editable-img` 类
- CSS cell style 去重：style dict 直接替换默认 bg/padding，不再叠加
- 编辑器工具栏全面升级：B/I/U + 字体 + 字重 + 字号 + 拾色器 + 背景色 + 透明度
- 数据库目录移至 `.standardization/hug-html/data/`，遵循 R-11/R-22 规范
- `SKILL.md` — 四层架构定义（骨架结构/骨架样式/模块结构+样式/基础样式）
- `references/guide.md` — 完整重写为 v2 网格架构教程
- `references/module-library.md` — 完整重写为两层级模块说明
- 版本号 `1.0.1` → `2.0.1`

### Fixed
- Grid Spec `cells` 位置统一：`grid.cells[...]` 为标准存储位置，兼容顶层 `cells`
- 单元格 CSS 生成逻辑修正（style dict 重叠问题）
- body 背景硬编码 `#000` 修复：根据模板类型智能选择
- `backdrop-filter` 从 DEFAULT_CARD_STYLE 泄露到普通模板（导致内容裁剪）修复
- 日历 JS 缺失 `<script>` 包裹导致不执行修复
- GBK 编码兼容：所有 print 输出兼容 Windows 终端
- 标签平衡检查改用正则精确匹配，排除 script/style 内容，消除假阳性
- R-20 写作规范修复：guide.md 中英文混排空格
- R-11/R-22 数据目录合规：`data/` → `.standardization/hug-html/data/`
