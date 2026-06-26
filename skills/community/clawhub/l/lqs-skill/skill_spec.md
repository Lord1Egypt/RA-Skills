# LQS Skill 实施规范（MVP）

## 1. 目标
输入自由文本需求或 Google Doc 导出的正文文本，先做需求分析，再基于项目现有代码模式自动沉淀模板，最终生成后台默认工件：Model、Controller、View、Migration。

重点：模板来自项目分析，不依赖固定脚手架命令，也不依赖仓库内专用执行器代码。

## 2. MVP 边界
- 支持输入：
  - 纯文本需求
  - Google Doc 导出的正文文本（手动粘贴或外部抓取后粘贴）
- 默认产物：`model,controller,view,migration`
- 默认模块：`Admin`
- 默认控制器基类：`BackendBaseController`
- 默认行为：先预览 diff，确认后写入

## 3. 端到端流程
1) Ingest
- 接收自由文本或“已提取的文档正文”
- 对输入正文做归一化与清洗（标题编号、注释、页眉页脚）

2) Analyze
- 输出需求草案 `RequirementDraft`
- 内容：实体、字段、动作、页面、约束、验收点

3) Mine Patterns
- 从项目现有控制器/视图/模型提取高频模式
- 产出 `ProjectPatternProfile`

4) Build Templates
- 用 `ProjectPatternProfile` 生成模板包 `TemplatePack`
- 模板包括：controller/model/view/migration

5) Resolve Spec
- 将 `RequirementDraft` 映射为 `Spec`
- 补全默认值（模块、前缀、基类、命名）

6) Render Preview
- 使用 `TemplatePack + Spec` 生成候选文件
- 输出 unified diff（dry-run）

7) Confirm & Write
- 用户 approve 后，由外部执行环境或人工确认写入
- 返回变更清单 + 风险提示

## 4. 数据对象

### 4.1 RequirementDraft
- feature_name
- business_goal
- entities[]
- actions[]
- ui_pages[]
- constraints[]
- acceptance[]

### 4.2 ProjectPatternProfile
- controller_patterns
- view_patterns
- response_contract
- naming_rules
- path_rules
- migration_rules

### 4.3 Spec
- module
- entity
- table
- pk
- fields[]
- apis[]
- artifacts[]
- target_paths

## 5. 默认路径规则（后台）
- Controller: `application/modules/Admin/controllers/{Entity}.php`
- Model: `application/models/{Entity}Model.php`
- View: `application/modules/Admin/views/{entity}/index.tpl`
- Migration: `migrations/{timestamp}_{action}_{table}.php`

## 6. 质量门槛
- Parse 准确率：字段与动作不漏主语义
- Diff 可读：新增/修改/覆盖分组
- Migration 合规：必须含 `up()` 与 `down()`
- 安全：不含任何凭证

## 7. 非目标（MVP）
- 不做自动执行 migration
- 不做复杂权限系统自动接入
- 不做跨模块联动代码重写
- 不在仓库内维护专用 Skill 命令执行器
