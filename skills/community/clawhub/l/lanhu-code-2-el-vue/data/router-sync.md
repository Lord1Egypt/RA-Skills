# 路由登记与校验（Custom.vue 交付后）

本文档与 SKILL 正文「步骤 3 / 唯一信息源」配合使用：**生成页面结构与样式时仍以 `index.vue` + 其 CSS 为唯一稿源**；路由文件**仅**在 `Custom.vue` 落地后用于**可访问性登记**，不得作为 UI 稿源。

---

## 1. 问题识别

### 1.1 典型现象

- 已在 `src/views/${folderName}/` 下生成或更新 `Custom.vue`，浏览器访问预期地址时出现 **404**、**空白**或 **仍打开旧页**。
- 项目使用 Vue Router（常见为 `src/router/index.js`），其它视图（如 `gushi`、`yingyu`、`danci`）存在 **`/xxx` + `/xxx-custom` 双路由** 模式，但新建文件夹未同步。

### 1.2 识别步骤

1. 确认目标目录存在：`src/views/${folderName}/index.vue`（静态稿）与 `src/views/${folderName}/Custom.vue`（动态稿，若已改造）。
2. 打开路由入口文件（本仓库为 `src/router/index.js`，其它项目可能是 `router.ts` / 模块化 `routes` 文件）。
3. 全文搜索 **`folderName`**（如 `shushi`）、**`Custom.vue`** 路径片段 **`views/${folderName}/`**。
4. 对照仓库内**已有同类约定**：
   - 若存在「静态 `index` + 动态 `Custom`」两条路径（例如 `/gushi` 与 `/gushi-custom`），则新页面应**沿用同一命名与结构**。
5. 若仅有 `index` 无 `Custom` 路由：判定为 **Custom 页不可达**；若 `import` 路径错误或 `component` 未指向 `Custom.vue`：判定为 **配置错误**。

---

## 2. 修复方法

### 2.1 标准修复（与本仓库约定一致时）

1. 在路由文件顶部增加 **静态页** 与 **动态页** 的 `import`（路径与项目别名/相对路径保持一致）：

```javascript
import shushi from '../views/shushi/index.vue'
import shushiCustom from '../views/shushi/Custom.vue'
```

2. 在 `routes` 数组中追加两条路由（`path` / `name` 与现有页面风格一致，常用 **kebab-case 路径** + **camelCase name**）：

```javascript
{
  path: '/shushi',
  name: 'shushi',
  component: shushi,
},
{
  path: '/shushi-custom',
  name: 'shushiCustom',
  component: shushiCustom,
},
```

3. 保存后本地启动应用，依次访问 **`/shushi`**、**`/shushi-custom`**，确认组件加载无控制台报错。

### 2.2 模块化路由项目

- 若路由按模块拆分，将上述 `import` 与 `route` 对象写入**负责业务视图**的模块，并确保该模块被汇总进根 `routes`。

### 2.3 history 模式与部署

- 使用 `mode: 'history'` 时，生产环境需服务器 **fallback 到 `index.html`**；若仅开发环境 404，仍先排除「未注册路由」再查部署配置。

---

## 3. 需求文案（摘要）

- **每新增或正式交付一个视图的 `Custom.vue`**，须在路由中提供**可达路径**，与项目中同类页面（静态 `index` / 动态 `Custom`）**命名与成对关系一致**。
- **`import` 路径**须指向真实文件，**`component` 字段**须与 `import` 变量一致，避免拼写错误或未使用的 `import`。
- **不得**用路由里其它页面的 meta/path 作为当前页 **UI 稿源**；路由变更**不改变** lanhu-code-2-el-vue 对 `Custom.vue` 内容与样式的唯一信息源要求。

---

## 4. 自检清单

- [ ] 路由文件中可搜到 `${folderName}`（或与用户约定目录名一致的路径片段）。
- [ ] 存在指向 `../views/${folderName}/index.vue` 的路由（若项目约定保留静态预览）。
- [ ] 存在指向 `../views/${folderName}/Custom.vue` 的路由（改造页应对应 `-custom` 或项目统一后缀）。
- [ ] `path`、`name` 与仓库内已有路由风格一致，无重复 `name` / 重复 `path`。
- [ ] 浏览器访问新路径无 404，控制台无组件解析失败报错。

---

## 5. 与 SKILL「唯一信息源」的关系

| 阶段 | 能否读取路由文件 | 用途 |
|------|------------------|------|
| 编写 `Custom.vue` 的 template / style / 数据稿 | **否**（不作为稿源） | — |
| `Custom.vue` 写入完成后的交付步骤 | **是** | 仅登记、校验 `import` 与 `routes`，保证可访问性 |
