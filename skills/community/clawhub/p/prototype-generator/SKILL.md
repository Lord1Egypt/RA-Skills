---
name: prototype-generator
description: Generates admin/list prototypes from requirements. Supports mountListPage-style frameworks (e.g. kfk-mock-ui), standalone HTML, or project-specific setups. Use when user wants to create a prototype, generate prototype from requirements, add list pages, or says "根据需求生成原型" / "自动生成一套原型" / "创建原型".
---

# 通用原型自动生成

根据用户输入的需求，自动生成后台列表原型。支持多种输出模式，适配不同项目结构。

## 触发条件

- 用户要求「根据需求生成原型」「自动生成一套原型」「创建原型」
- 用户描述业务场景并希望得到可运行的原型页面
- 用户要求新增列表页或管理页面

## 第一步：检测项目上下文

生成前先扫描项目，确定输出模式：

| 检测到 | 输出模式 | 说明 |
|--------|----------|------|
| `kfk-mock-ui.js` 或 `KFK.mountListPage` | **列表框架模式** | 生成 menu.js、view_*.html，在现有 mock-ui 中加假数据分支 |
| `kfk-admin.css` 或上层 UI 库目录 | **子项目模式** | 同上，资源路径为 `../父目录/` |
| 无上述依赖 | **独立模式** | 生成自包含的 HTML（内联样式+脚本），无外部依赖 |

若用户明确指定（如「用现有框架」「独立页面」「纯 HTML」），优先按指定执行。

## 第二步：解析需求

从用户描述中提取或推断：

| 项 | 说明 | 缺失时默认 |
|----|------|-----------|
| 项目/模块名称 | 品牌或模块名 | 询问或取首句关键词 |
| 目标目录 | 输出位置 | 项目根或同名子目录 |
| 菜单分组 | 按业务域分组 | 如「核心业务」「基础数据」「系统配置」 |
| 页面列表 | 每页：标题、表格列、查询条件、行操作 | 从需求逐条对应 |

**字段推断规则：**
- 名称/标题/编码类 → 模糊查询 `mode: 'like'`
- 是/否、状态、枚举 → 下拉 `type: 'select'`，`options: [{value:'',label:'全部'},...]`
- 年月/日期 → `type: 'month'` 或 placeholder `如 2025-10`
- 枚举选项从需求或示例中抽取

## 第三步：生成文件（按模式）

### 列表框架模式（存在 kfk-mock-ui 或类似 mountListPage 框架）

1. **menu.js**：`{ group, items: [{ id, title, href }] }`，id 用 kebab-case
2. **view_xxx.html**：引用 css/js，调用 `mountListPage(app, config)`（如 KFK.mountListPage）
3. **mock-ui.js**：新增 `generateXxxRow`，在 `generateRows` 中加分支
4. **sql/*.sql**（可选）：与业务字段对应的建表语句

**资源路径约定**：若项目中有上层 UI 库目录（如父级原型目录），用 `../父目录/css/`、`../父目录/js/`；否则用项目内 `./css/`、`./js/`。

### 独立模式（无框架依赖）

生成单页 HTML，包含：
- 查询表单（根据 queryFields）
- 数据表格（根据 columns）
- 简单分页
- 行操作按钮（查看/编辑/删除等）
- 内联样式与脚本，可直接用浏览器打开

结构：query-form + data-table + pager，内联 CSS 与脚本。详见 [references/standalone-template.md](references/standalone-template.md)。

### 多页独立模式

当有多个列表页且用户需要菜单导航时，可生成：
- `index.html`：左侧菜单 + iframe 展示
- `view_xxx.html`：各列表页（独立 HTML）
- `menu.js` 或内联菜单数据

## 第四步：校验清单

- [ ] menu item 的 id 与 pageId / 页面标识一致
- [ ] columns 的 key 与假数据对象 key 一致
- [ ] 下拉类 queryFields 使用 `type: 'select'` 和 `options`
- [ ] 独立模式下样式、脚本可正常运行

## 配置模板（列表框架模式）

### queryFields

```javascript
{ key: 'name', label: '名称', placeholder: '请输入', mode: 'like' }
{ key: 'status', label: '状态', type: 'select', mode: 'eq', options: [
  { value: '', label: '全部' }, { value: '是', label: '是' }, { value: '否', label: '否' }
]}
{ key: 'summaryMonth', label: '月份', type: 'month', mode: 'eq' }
```

### columns

```javascript
{ key: 'serialNo', title: '序号' }
{ key: 'code', title: '编码', mono: true }
{ key: 'name', title: '名称', align: 'left', required: true }
{ key: 'remark', title: '备注', align: 'left' }
{ key: 'createTime', title: '创建时间', mono: true }
```

### rowActions + onRowAction

```javascript
rowActions: [
  { act: 'view', label: '查看' },
  { act: 'edit', label: '编辑' },
  { act: 'delete', label: '删除', danger: true }
]
```

## 需求示例

| 用户输入 | 产出 |
|----------|------|
| 「做一个供应商管理，名称、主体、备注」 | 1 页供应商列表，3 列 + remark/createTime |
| 「发票池按销方、购方、是否推送查询」 | queryFields：销方/购方/是否推送（下拉） |
| 「列表要有报废、重置按钮」 | rowActions 增加自定义操作，onRowAction 实现逻辑 |
| 「独立原型，不要依赖」 | 单 HTML 文件，内联样式和脚本 |

## 可选引用

项目中若有以下规则，可一并遵循：
- `.cursor/rules/prototype-menu.mdc`：菜单与列表页结构
- 项目中若有列表页 config、CRUD 约定规则，可一并遵循

## 参考

- 独立模式详细模板：[references/standalone-template.md](references/standalone-template.md)
