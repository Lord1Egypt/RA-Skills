---
name: lanhu-code-2-el-vue
description: "将静态 Vue 页面(index.vue)改造为动态页面(Custom.vue)；执行前必须先应用 ui-ux-max-pro 做 UI/UX 分析；稿源仅限 index.vue、其引用的 CSS 与资源路径，禁止参考仓库内其他文件。Invoke when user wants to transform a static Vue page into a dynamic data-driven page with Element UI components."
---

# lanhu-code-2-el-vue

## 介绍

本 Skill 用于将**静态 HTML 页面改造为 Vue 2 + Element UI 的数据驱动动态页面**，执行时会直接生成 `Custom.vue` 文件。

## 前置 Skill：ui-ux-max-pro

当本 Skill 被触发时，**必须先执行 `ui-ux-max-pro`**，再继续执行当前 Skill：

1. 先读取并遵守 `ui-ux-max-pro` 的 `SKILL.md`。
2. 先完成 `ui-ux-max-pro` 要求的 UI/UX 分析、布局判断、视觉一致性检查与可用性评估。
3. 将 `ui-ux-max-pro` 的结论作为后续静态页改动态页的设计约束，但不得违反本 Skill 的「唯一信息源」限制。
4. 然后再继续执行当前 `lanhu-code-2-el-vue` 的 `index.vue` → `Custom.vue` 改造流程。
5. 若找不到 `ui-ux-max-pro`，必须告知用户并暂停，不得直接开始生成或改写 `Custom.vue`。

## When to Use This Skill

在以下场景触发本 Skill：

- 用户要求「静态改动态」「把 index.vue 改成 Custom.vue」「按改造规范改造页面」
- 将某视图文件夹下的静态页面改为 Vue 2 + Element UI 动态页面
- 需要循环渲染、Element UI 替换、统一 class 命名、像素级还原设计稿

**不适用：** 全新页面从零开发、非 Vue 2/Element UI 技术栈、不涉及「静态→动态」改造。

---

## 执行指令（核心）

当本 Skill 被触发时，**必须按照以下步骤直接执行代码改造，生成 Custom.vue 文件**，而不是仅提供指导文档。

### 唯一信息源（生成 Custom.vue 时必须遵守）

**生成/改写 `Custom.vue` 时，只允许使用以下材料作为页面结构与样式的依据：**

1. **`src/views/${folderName}/index.vue`** 的源码（模板、脚本、内联样式）。
2. **由 index.vue 直接或间接引用的样式文件**（例如 `<style src="./assets/index.css">`、`@import`、`import` 等，按路径相对 `index.vue` 解析；若存在链式 `@import`，仅沿该链读取，不得扩大范围）。
3. **在上述 Vue/CSS 中出现的图片等资源路径**（保留或转换为 `Custom.vue` 所需写法即可；无需读取图片二进制内容作「设计参考」）。

**禁止：**

- **不得**为拼页面而读取、对照或照搬**本仓库其他文件**的内容，包括但不限于：同目录或其他视图下的 `Custom.vue`、`index.vue`（非当前 `${folderName}`）、公共组件源码、`create.md`、**路由配置**、`package.json` 等。
- **不得**以「已有某页的 Custom.vue 写法」为模板生成当前页；每一页只认当前文件夹的 `index.vue` + 其引用 CSS + 资源路径。

**路由配置的例外（仅交付阶段）：** 在 **`Custom.vue` 已写入磁盘之后**，**允许**打开项目路由文件（如 `src/router/index.js`）**仅用于**登记或校验 `index.vue` / `Custom.vue` 的访问路径，使页面可通过 URL 打开。**禁止**把路由里其它页面的 path/name/meta 当作当前页的 UI 稿源或布局依据。详见 **`data/router-sync.md`** 第 5 节。

**说明：** 本 Skill 正文与 `data/` 下的规范文档属于**操作规则**（如何命名、如何用 Element UI 等），不是「页面稿源」。页面稿源仍仅限上述 1～3 项。

### 步骤 1: 获取目标文件夹名称

从用户输入中提取 `${folderName}`（如：kz、shushi 等）。

### 步骤 2: 验证源文件存在性（必须执行）

```javascript
// 必须存在：
必须存在: src/views/${folderName}/index.vue

// 样式文件：以 index.vue 实际引用为准（常见为 ./assets/index.css，若引用多个则均需存在）
// 读取 index.vue 后解析其 style src / @import / import 路径并逐一验证存在

// 目标文件（将被创建或覆盖）：
目标文件: src/views/${folderName}/Custom.vue
```

**⚠️ 重要：** 若 `index.vue` 不存在，或其所引用的样式文件缺失，必须告知用户并停止执行。验证通过后，**仅读取** `index.vue` 与这些被引用的样式文件（及链式 `@import`），不打开其他工程文件。

### 步骤 3: 读取源文件（仅限唯一信息源）

1. 使用 Read 工具读取 `src/views/${folderName}/index.vue`。
2. 根据 `index.vue` 中的引用，**仅**读取其指向的 CSS（及该 CSS 内 `@import` 的下一层样式，若需要完整样式表）。
3. **不要**读取 `package.json`、**路由文件**、其他视图的 `Custom.vue` 等作为**模板/稿源/样式依据**（见上文「唯一信息源」；路由仅在步骤 8 用于登记，见 **`data/router-sync.md`**）。

### 步骤 4: 分析源文件结构

分析内容：
1. **识别页面布局** - 确定是单栏、双栏还是多栏布局
2. **识别重复结构** - 找出需要循环渲染的部分（使用 v-for）
3. **识别交互元素** - 找出按钮、输入框、多选、单选等可替换为 Element UI 的元素（开关保留原生 DOM，不替换为 el-switch）
4. **识别样式特征** - 记录关键样式值（颜色、尺寸、间距）
5. **识别伪控件（必做）** - 源页面常用 div+文案+图标模拟表单控件，须按「6.3.4 伪控件识别与替换」规则识别并替换为 el-select、el-checkbox、el-input；**取色**须按 **点击后展开的下拉面板的形态（图1 / 图2）** 选用 **`el-color-picker-extend`** 或 **`el-color-picker`**（**不以触发区单独判断**；见 **6.3 映射表**、**6.3.11**、**`data/el-color-picker-extend.md` §「颜色选择：触发与下拉的共同结构」**），避免漏改或错用组件。

### 步骤 5: 生成 Custom.vue 文件

**⚠️ 必须使用 Write 工具直接生成文件，而不是返回代码给用户！**

生成的 `Custom.vue` 必须包含以下结构：

```vue
<template>
  <div class="[folderName]_page_container">
    <!-- 改造后的动态页面内容 -->
    <!-- 1. 将重复结构改为 v-for 循环渲染 -->
    <!-- 2. 将原生的 input、button、checkbox、radio 等替换为 Element UI 组件（开关不替换，保留原生结构） -->
    <!-- 3. 保留所有样式，确保像素级一致 -->
  </div>
</template>

<script>
export default {
  name: '[FolderName]Custom',
  data() {
    return {
      // 所有 template 中使用的数据必须在此定义
      // 包括：列表数据、表单数据、状态变量等
    }
  },
  methods: {
    // 所有 @click、@change 等事件处理方法必须在此实现
    // 命名规范：handle + 功能名（如 handleSearch、handleSubmit）
  }
}
</script>

<style scoped>
/* 所有样式必须在此定义，禁止引用外部 index.css */
/* 使用 scoped 避免样式污染 */
/* 对 Element UI 组件使用 ::v-deep 进行样式覆盖 */
</style>
```

### 步骤 6: 改造规范（必须遵守）

#### 6.1 文件操作规范

| 规则 | 说明 |
|------|------|
| ❌ 禁止修改源文件 | `index.vue` 及其引用的样式文件只能读取，绝对不能修改 |
| ✅ 只操作目标文件 | 所有代码只写入 `Custom.vue` |
| ✅ 唯一稿源 | 结构与样式依据仅限当前 `index.vue` + 其引用 CSS + 资源路径；禁止参考其他视图/其他 `Custom.vue`/路由等工程文件生成页面内容 |
| ✅ 使用 scoped 样式 | 所有样式必须在 `<style scoped>` 中定义 |
| ✅ 完整单文件组件 | Custom.vue 必须包含 template、script、style 三部分 |

#### 6.2 命名规范

- Class 名**仅使用下划线 `_` 连接**，**不得包含任何数字**（0-9）
- 序位、顺序用英文词表示（如 `first`、`second`、`left`、`right`）
- 命名公式：`[folderName]_[功能]_[内容]_[特征]`

```
✅ 正确示例：
kz_header_container
kz_list_item
kz_button_primary
kz_math_cell_first

❌ 错误示例：
group_1              // 含数字
kz_cell_2            // 含数字
box-1                // 使用连字符
headerBox            // 使用驼峰
```

#### 6.3 Element UI 替换要求

凡有按钮、多选、单选、输入、分页、弹窗等，须替换为 Element UI 组件。**不替换**：开关保留源页面原生 DOM（如 div + @click、原生 input 等），不使用 `el-switch`。

**替换映射表：**

| 原元素 | Element UI 组件 | 说明 |
|--------|-----------------|------|
| 按钮 | `el-button` | 可点击按钮须绑定 `@click`，并在 methods 中实现对应方法 |
| 多选 | `el-checkbox-group` + `el-checkbox` | |
| 单选 | `el-radio-group` + `el-radio` | 互斥多选一；样式与源页一致，激活态与选中项须为主题色，见「6.3.10 单选框识别与主题色规范」 |
| 输入框（单行） | `el-input` | 带外框的搜索框须同时满足「6.3.1 带外框搜索框样式规范」 |
| 多行文本 | `el-input type="textarea"` | 可配 show-word-limit、maxlength |
| 下拉选择 | `el-select` + `el-option` | |
| 分页 | `el-pagination` | 需定义 currentPage、pageSize、total，实现 size-change、current-change；**替换时必须删除原始分页全部静态内容**（共 xxx 条、静态页码、上下页、条数/页等），仅保留一个 el-pagination，见「6.3.9 分页替换与主题色规范」 |
| 弹窗 | `el-dialog` | 需定义 dialogVisible，实现关闭/确定/取消方法 |
| 日期输入 | `el-date-picker` | |
| 下拉菜单 | `el-dropdown` + `el-dropdown-menu` | 需实现 @command 处理方法 |
| 进度条 | `el-progress` | |
| 评分 | `el-rate` | 星星颜色、评分数值须与源页面一致，见「6.3.2 el-rate 注意事项」 |
| 取色 / 填充（**展开后的下拉**为 **图1**：预设色块矩阵 + Hex/RGB/不透明度 +「最近使用」+ 吸管等；或页内静态整区模拟该形态） | `el-color-picker-extend` | **触发区长什么样不决定选型**，见 **`data/el-color-picker-extend.md`** §「颜色选择：触发与下拉的共同结构」；全局注册见 `main.js` |
| 取色（**展开后的下拉**为 **图2：Element 默认面板**，**SV 面 + 右侧竖向色相条 + 底部 Hex +「清空」「确定」**） | `el-color-picker` | 常见触发器为 **字体颜色**（A+下划线+箭头）→ **透明叠层**；**删除页内重复取色区**见 **6.3.11**；细则见 `data/el-color-picker-extend.md` |

**替换时必须：**
1. **先删除**该区域原有 DOM 结构（含该控件的**全部**相关 DOM，见下方「下拉框」说明）
2. **再写入** Element UI 组件
3. **同时完成** template、data()、methods 三部分（禁止只写 template 不写 methods/data）
4. **用 `::v-deep`** 覆盖 Element UI 默认样式，保持视觉一致
5. **可点击按钮**：页面中所有可点击区域（上传、预览、确定、取消、智能合成等）须在 template 中绑定 `@click="handleXxx"`，并在 methods 中实现 `handleXxx`，命名建议 `handle` + 功能名（如 handleUploadImage、handleDialogConfirm）

**下拉框替换时须删除的 DOM（通用规则）：** 除「当前选中项 + 箭头」的触发区外，若 index.vue 中还有**独立的下拉选项列表**（如浮层、侧边列表、鼓点-1～鼓点-11 等静态列表），须**一并删除**。替换为 `el-select` 后，选项由 el-select 自带的 dropdown 展示，不得保留原静态选项列表 DOM，否则会出现「识别了下拉框但页面上仍有两套选项」的问题。

**6.3.1 带外框的搜索框（el-input）样式规范**

当搜索框被包在带边框、圆角的白底容器内（如「搜索资源标题、ID」「搜索你想要的单词」）时，须满足：

- **外层容器**：固定高度（如 48px）、宽度（如 688px）、圆角、**边框**（须设 `border`，如 `1px solid`）、背景色；`display: flex`、`align-items: center`、`box-sizing: border-box`、`overflow: hidden`，使内部输入框垂直居中且不撑高。**容器在 hover 与 focus-within 时边框须为主题色**（`.xxx_search_wrapper:hover`、`.xxx_search_wrapper:focus-within` 设 `border-color` 为页面主题色），详见 `data/recognition-and-fix.md` 9.8。
- **.el-input-group**：通过 `::v-deep` 对 `.el-input-group` 做样式覆盖：`display: flex`、`flex: 1`、`height: 100%`、`min-width: 0`、`border: none`、`background: transparent`，避免出现双重边框或额外外框。
- **.el-input / .el-input__inner**：`.el-input` 在容器内 `height: 100%`、`flex: 1`；`.el-input__inner` 去掉自带边框（`border: none`）、背景透明、高度略小于容器约 2px（如容器 48px 则 inner 约 46px）、`line-height` 与高度一致、`border-radius` 仅左侧与容器一致（若右侧为 append 按钮则设为 `12px 0 0 12px`）、`box-sizing: border-box`、`padding-left` 为前缀图标留足空间（如 44px），避免双边框与错位。
- **占位符**：`::v-deep .el-input__inner::placeholder` 设置 placeholder 颜色与设计稿一致（如 `rgba(153, 153, 153, 1)`）。
- **前缀图标**：`.el-input__prefix` 使用 `display: flex`、`align-items: center`、`height: 100%`，`left` 与设计一致（如 16px）；自定义 prefix 插槽根节点用 `display: inline-flex`、`align-items: center`，图标尺寸与设计一致（如 16×16px）。
- **命名**：类名使用 `[folderName]_search_wrapper`、`[folderName]_search_input` 等规范命名。同一项目内所有带外框的搜索框均按此规则实现。

**自检**：容器高度与设计一致；容器有 border，**hover 与 focus-within 时边框为主题色**（见 9.8）；无双重边框；`.el-input-group` 已覆盖无边框且 flex 占满；前缀图标与文字垂直对齐；placeholder 颜色正确；无错位或溢出。

**6.3.1.1 placeholder 垂直居中与页面溢出（必做）**

- **placeholder 垂直居中**：`.el-input__inner` 高度与容器一致（或略小 1～2px），`line-height` 与高度一致，上下 padding 为 0；`.el-input`、`.el-input-group` 设 `display: flex`、`align-items: center`，使输入区在容器内垂直居中；必要时对 `::v-deep .el-input__inner::placeholder` 设相同 line-height。
- **输入框/按钮不溢出页面**：页面根容器设 `overflow-x: hidden`；主卡片、Tab 行、底栏、列表区使用 `width: 100%` + `max-width: [设计稿宽度]` + `min-width: 0` + `box-sizing: border-box`；带外框搜索框容器在 flex 中设 `flex: 1`、`min-width: 0`、`max-width: [设计稿宽度]`；底栏中间文案将固定大 `margin-left` 改为 `margin-left: auto`，避免窄屏下溢出。

详见 `data/search-input-and-page-overflow.md`（识别步骤、修复方法、需求文案与自检清单）。

**6.3.2 el-rate 评分组件注意事项**

- 星星颜色：选中/未选中颜色须与源页面一致（打开 index.vue 查看），不可默认用橙色而源页为黄色。
- 评分数值：每个维度显示的实心星数须与源页面一致（如色彩 5 星、构图 5 星、想象力 3 星），不得全部默认 5 星或 3 星。
- 文字样式：「超赞」等评分文字的颜色、大小、位置须与源页面一致，用开发者工具对比。
- 样式覆盖：星星、文字、间距等均通过 `::v-deep` 精确匹配源样式。

**6.3.4 伪控件识别与替换（下拉框、多选框、单选框、搜索框）**

源页面常使用 div + 文案 + 图标模拟表单控件，没有原生 `<select>`、`<input type="checkbox">`、`<input type="radio">` 或带外框的 `<input type="text">`，改造时容易漏识别。须按以下规则识别并替换：

| 控件类型 | 识别特征（index.vue / index.css） | 替换为 | 说明 |
|----------|-----------------------------------|--------|------|
| **下拉框 select** | 小容器内为「当前选中文案 + 右侧下拉箭头图标」、或「标签 + 可切换项」；样式为带边框、圆角的盒子（如 66×28px） | `el-select` + `el-option` | 在 data 中定义选中值（如 selectedXxx），options 与同页列表/配置一致 |
| **多选框 checkbox** | 左侧为勾选图标容器（含勾/未勾图或方框）+ 右侧说明文案（如「全选所有模块」「当前配置应用于所有页面」）；多行结构相同 | `el-checkbox` | 每项对应 data 中一个布尔（如 checkedAllModules、applyToAllPages） |
| **纵向模块勾选列** | **易漏识别**：左侧仅为 **~16×16 方框切图**（`image-wrapper` + `img`），**无**「全选」类长说明；右侧或邻列为**模块名**（音标、释义、例句、词组等）；多行**纵向对齐**成列；或左侧 **flex-col 堆叠多个方框**与右侧多行标题**行对行**对应 | `el-checkbox`（无内联文案时隐藏 `label`）+ 右侧内容区 **`v-show`/`v-if` 联动** | data 中用对象（如 `moduleFlags`）或多项布尔；**禁止**保留静态勾图；样式见 **6.3.4.1** 与 `data/recognition-and-fix.md` **§2.2.1、§3.2.1** |
| **横向工具条 / 尾行模块勾选** | **易漏识别**：在**横向 `flex-row`** 中，**模块标题（如英式音标、鼓点音频）左侧**仍有 **16×16 方框切图**；或底部 **「单词书写」** 等行「左方框 + 标签 + 右侧预览」— 与纵列勾选**同类语义**，只是排在横排/尾行 | `el-checkbox` + 对 IPA 区、鼓点 **el-select** 与图标、书写预览等 **`v-show` 联动** | 须纳入 **「全选所有模块」** 的同一批布尔；**禁止**纵列用组件、横条仍留 png；**尺寸**按 **6.3.4.3** 与 `recognition-and-fix.md` **§2.2.2～§2.2.3、§3.2.2～§3.2.3** |
| **单选框 radio** | 多个选项中仅能选一项（互斥）；圆点/圆圈 + 文案，或 div 模拟的选项组；有「选中」与「未选中」两种视觉状态 | `el-radio-group` + `el-radio` | 在 data 中定义选中值（如 radioValue），样式与源页一致，选中/悬停为主题色，见 6.3.10 |
| **带外框搜索框** | 外层为白底/圆角/边框容器，内为「搜索图标 + 占位文字 + 右侧搜索/按钮」 | `el-input` + prefix/suffix 插槽 | 必须同时满足「6.3.1 带外框搜索框样式规范」 |
| **取色 / 填充面板（图1 形态）** | **展开后的面板**含：标题「填充」等 + **色块格矩阵**、**渐变/透明度滑条**、**#+hex**、**% 不透明**、**RGB 数字格**、**最近使用**等（页内整区或弹层）；触发区可为按钮或小入口 | `el-color-picker-extend` | **`data/el-color-picker-extend.md`** §「颜色选择：触发与下拉的共同结构」、§选型、§产品需求 |
| **取色（图2 形态）** | **展开后**为 **SV 渐变方 + 竖向彩虹色相条 + 底栏 Hex +「清空」「确定」**（Element UI 2 默认取色下拉）；触发区常为 A+下划线+箭头 | `el-color-picker` | **6.3.11**、**`data/el-color-picker-extend.md`** §对照清单、字体颜色触发器 |

**识别步骤（通用）：**
1. 在 index.vue 中搜索：带「选」「勾」「搜索」等语义的文案，或带下拉箭头、勾选图标的 div 结构。
2. 在 index.css 中确认该区域样式：是否有边框、圆角、固定宽高（如 66×28、16×16 勾选区域）。
3. 若符合上表特征，在 Custom.vue 中替换为对应 Element UI 组件，并补全 data、methods。
4. **纵向模块勾选列（补充）**：在配置/预览区搜索**多行**「左列小方框图 + 右列模块标题」；若左列无说明性长文案、仅方框 png，须按上表「纵向模块勾选列」处理，详见 `data/recognition-and-fix.md` **§2.2.1**。
5. **横向工具条 / 尾行（补充）**：除纵列外，扫描配置区**所有横向行**与**底部尾行**：是否存在「**方框切图 + 模块名 + 业务区**」；若 img 与纵列勾选**同资源或同类**，须同样改为 `el-checkbox`，详见 **6.3.4.2**、`data/recognition-and-fix.md` **§2.2.2**。

**6.3.4.1 纵向模块勾选列（无内联文案的 el-checkbox）**

- **结构**：保留原 `image-wrapper` 父级 class 与布局，内部替换为 `el-checkbox`；模块标题仍为旁侧 `span`，**不要**把标题塞进 `el-checkbox` 默认插槽（除非稿面即为一体标签）。
- **隐藏 label**：`::v-deep .el-checkbox__label { display: none; width: 0; padding: 0; margin: 0; overflow: hidden; }`，避免 Element 为空白 label 留出间距导致与稿面不齐。
- **尺寸与视觉**：`::v-deep .el-checkbox__inner` 的宽高须与 index.css 中**负责方框视觉的一层**一致（见 **6.3.4.3**）；`border-radius` 与稿一致；未选中边框浅灰，选中为**白底 + 主题色边框与勾**（与稿一致即可）；`hover`、`is-focus` 边框建议主题色，与 **6.3.8** 一致。
- **联动**：每个布尔对应右侧一块内容 `v-show`；双勾（例句/译文）对应同一卡片内**两个**内容区的分别显示与中隔线条件显示。
- **禁止**：保留原方框 png 冒充勾选态；仅改「全选」行而漏改纵向模块列。

**6.3.4.2 横向工具条 / 尾行上的模块勾选与尺寸统一**

- **识别**：在**顶部横向配置行**（如英式音标、鼓点音频）或**底部尾行**（如单词书写）中，**模块标题 span 之前**的 `image-wrapper` + 小 png，若与左侧纵列模块勾选**尺寸同级（约 16×16）**且语义为「是否展示该段能力」，即属模块勾选，**不得**仅替换纵列而保留此处静态图。
- **替换**：删除切图，在原 wrapper 内放入与纵列**同一 class** 的 `el-checkbox`（如 `[folderName]_module_checkbox`），保证全页共用**同一套** `::v-deep` 规则。
- **联动**：英式音标应对 **IPA + 播放图标所在行** `v-show`；鼓点音频若左侧方框表示模块总开关，应对 **el-select 及同组图标** `v-show`；单词书写应对**右侧预览词** `v-show`。
- **全选**：`handleSelectAll` / 同步 `selectAll` 的 keys 须**包含**上述布尔，与纵列模块字段**合并为一套**，避免逻辑分裂。
- **尺寸与勾形（与 6.3.8 配合）**：全页无文案模块勾选须 **class 统一**；覆盖 **`.el-checkbox` 根**、**`.el-checkbox__input`**、**`.el-checkbox__inner`**、**`.el-checkbox__inner::after`** 及选中态勾线色；**inner 像素须按 6.3.4.3 从 index.css 读取**，禁止默认臆断为 16×16。详见 `data/recognition-and-fix.md` **§3.2.2、§3.2.3**。

**需求文案（摘要）**

- 配置区内**凡「左方框 + 模块名」式开关**，无论出现在**纵列、横条还是尾行**，均须 `el-checkbox`，禁止 png 与组件混用。
- **同一自定义 class + 完整深度样式（含 ::after）**；**方框边长以 index.css 实测为准（常为外层槽位 16px + 内层切图 13px）**，「全选」须覆盖横条与尾行布尔。

**6.3.4.3 多选框原始尺寸识别（wrapper / thumbnail 分层，必做）**

稿面常见结构为：**外层 `image-wrapper_*`（或 `group_*` / `box_*`）提供 16×16 对齐槽位**，内层 **`thumbnail_*` 的 `img` 为 13×13** 且带 `margin: 2px 0 0 2px`——**可见方框的物理像素往往等于 thumbnail 的 width/height，而非外层 wrapper 的 width/height**。若将 `el-checkbox__inner` 一律写成 16×16，会较稿面**偏大**，与仍使用切图的行或设计稿对比时产生偏差。

**识别步骤（须自 index.css / 稿源读取，禁止猜默认）：**

1. 在 index.vue 中定位该勾选左侧的 **`image-wrapper_*` + `img.thumbnail_*`**（或仅带 background 的 `image-wrapper_*`，其自身 width/height 即方框视觉尺寸）。
2. 在 index.css 中同时打开 **`.image-wrapper_*`** 与 **`.thumbnail_*`**（若存在）：
   - **槽位尺寸**：wrapper 的 `width`、`height`（及 `margin-top` 等），用于 **`el-checkbox` 根或 `.el-checkbox__input` 的占位与 flex 居中**（常见 **16×16**）。
   - **方框视觉尺寸**：**优先**取 **`.thumbnail_*` 的 `width`/`height`**；若无 thumbnail 而 wrapper 本身即为切图区（如 13×13 的 background 盒），则取 **该层** 的 width/height。此数值用于 **`::v-deep .el-checkbox__inner` 的 width/height**（本页示例为 **13×13**）。
3. 将 **`el-checkbox` 根** 设为 `display: inline-flex; align-items: center; justify-content: center`，**宽高等于槽位**（如 16px），**`__input`** 同槽位并 flex 居中，**`__inner`** 为步骤 2 的方框视觉尺寸（如 13px），`box-sizing: border-box`。
4. **`::after` 勾形**：在 inner 边长确定后，按比例微调 `height`、`width`、`left`、`top`、`border-width`，并在 **`is-checked .el-checkbox__inner::after`** 上设 `border-color`（多为白），使勾与稿面比例接近。

**禁止**：未打开 index.css 即写死 **16×16 inner**；或仅看 wrapper 忽略 **thumbnail** 导致 inner 过大。

**需求文案（摘要）**

- 替换伪多选前须**从当前页 index.css 读出槽位与方框两层尺寸**；**inner 对齐方框视觉层（多为 thumbnail）**，**根/`__input` 对齐槽位（多为 wrapper）** 并居中 inner。
- 勾形 **::after** 须随 inner 边长缩放，并做选中态勾线色覆盖。

详见 `data/recognition-and-fix.md` **§3.2.3**。

**下拉框替换时必须删除的 DOM（通用规则）：** 除「当前选中项 + 箭头」的触发区外，若 index.vue 中还有**独立的下拉选项列表**（如浮层、侧边列表、鼓点-1～鼓点-11 等静态列表），须**一并删除**。替换为 `el-select` 后，选项由 el-select 自带的 dropdown 展示，不得保留原静态选项列表 DOM。

**修复已有 Custom.vue 时：**
- 若发现「看起来像下拉/多选/搜索但仍是 div+img+span」：按上表替换，并补全绑定与样式覆盖。
- 若已用 el-select 但页面上仍保留原静态选项列表：删除该静态列表 DOM 及与之相关的 data/methods（如仅用于该列表的 handleXxx）。
- 搜索框样式异常：按「6.3.1」逐项检查容器高度、`.el-input-group` 无边框与 flex、el-input__inner 高度与无边框、padding-left、placeholder、prefix 对齐等。

详见 `data/recognition-and-fix.md`。

**6.3.5 Element UI 样式覆盖方法**

- **深度选择器**：scoped 无法直接修改组件内部样式，须用深度选择器。Vue 2 推荐 `::v-deep`，兼容写法 `/deep/`。
- **写法示例**：给组件加父级 class（如 `custom_search_input`），再写 `父级class ::v-deep .el-input__inner { ... }`，避免影响其他页面。
- **查找 class**：用开发者工具选中组件 DOM，在 Elements 面板查看内部 class（如 `.el-input__inner`、`.el-pager li`），再用 `::v-deep` 覆盖。
- **优先级**：优先用「父级 class + ::v-deep + 组件 class」提高特异性；尽量避免 `!important`；需覆盖多种状态时写全 `:hover`、`:focus`、`.active` 等。
- **输入框示例**：`父级 ::v-deep .el-input__inner` 设置 height、border、border-radius、padding、font-size；`::v-deep .el-input__inner:focus` 设 focus 边框色；`::v-deep .el-input__inner::placeholder` 设占位符颜色。
- **分页示例**：`父级 ::v-deep .el-pagination__total` 设总数样式；`::v-deep .el-pager li`、`::v-deep .el-pager li.active` 设页码与选中态；`::v-deep .btn-prev, ::v-deep .btn-next` 设上下页按钮。
- **下拉框示例**：小尺寸 select 用 `父级 ::v-deep .el-input__inner` 设 height、line-height、border-radius、font-size、border-color 与设计一致；`::v-deep .el-input__inner:focus`、`::v-deep .el-input.is-focus .el-input__inner` 设 focus 边框色为页面主题色。下拉选项选中/悬停须用 `popper-class` + 非 scoped 样式覆盖为主题色，见「6.3.7 下拉框样式与激活态主题色规范」。
- **多选框示例**：`父级 ::v-deep .el-checkbox__label` 设颜色、字号；`::v-deep .el-checkbox__inner` 的宽高取 **方框视觉层**（常为 thumbnail，见 **6.3.4.3**），圆角与设计一致。**选中/悬停/焦点须为主题色**：`::v-deep .el-checkbox__input.is-checked .el-checkbox__inner`、`::v-deep .el-checkbox__input.is-indeterminate .el-checkbox__inner` 的 background-color、border-color 设为主题色；`::v-deep .el-checkbox__inner:hover`、`::v-deep .el-checkbox__input.is-focus .el-checkbox__inner` 的 border-color 设为主题色，见「6.3.8」「6.3.8.1」。
- **单选框示例**：`父级 ::v-deep .el-radio__inner` 设尺寸、圆角、边框与设计一致；**选中/悬停/焦点须为主题色**：`::v-deep .el-radio__input.is-checked .el-radio__inner` 的 border-color、background-color 设为主题色；`::v-deep .el-radio__inner:hover`、`::v-deep .el-radio__input.is-focus .el-radio__inner` 的 border-color 设为主题色；并覆盖 **`.el-radio:focus:not(.is-focus):not(:active):not(.is-disabled) .el-radio__inner` 的 `box-shadow`**，见「6.3.10」「6.3.8.1」。

**6.3.6 按钮与列表内文字垂直居中规范**

改造后若出现「按钮文字、列表 badge 数字、列表项文字」未垂直居中，或**按钮在默认态与激活态（hover/active/focus/内容切换）下内容错位**，须按以下方式修复并作为通用规则遵守：

| 场景 | 识别特征 | 修复方法 |
|------|----------|----------|
| **el-button 默认与激活态** | 按钮有固定高度，文字或图标+文字偏上/偏下/偏左/偏右；或**切换状态（hover/active/focus 或内容从「导入」变为「已导入」等）后内容错位** | 在按钮的自定义 class 上通过 `::v-deep` 为**默认态及 :hover、:active、:focus** 统一设置 `display: inline-flex; align-items: center; justify-content: center; line-height: 1;`；按钮内文案（span 等）设 `text-align: center; margin: 0;`（或仅对称 margin），保证**默认与激活态内容均水平垂直居中，切换状态时保持居中** |
| **按钮激活态/替换态 DOM** | 状态切换后由非 button 的容器（如 div）展示内容，该容器内文字或图标未水平垂直居中 | 该容器使用 `display: flex; align-items: center; justify-content: center;`（或 `inline-flex`），内部文案与图标用 `text-align: center; margin: 0;` 或 flex 居中，与默认态一致 |
| **列表/步骤 badge 内文字** | 圆形或方形容器内为数字/序号，须**水平垂直都居中** | badge 容器使用 `display: flex; align-items: center; justify-content: center;`；内部文字 `text-align: center; margin: 0;`，不保留左右 margin，实现水平垂直都居中 |
| **列表项内文字** | 列表行有固定高度（如 48px），左侧 badge、中间文字、右侧图标未整体垂直居中 | 列表行容器使用 `display: flex; align-items: center;`；所有子元素（badge、文字、图标）去掉垂直方向 margin（`margin-top`/`margin-bottom` 置为 0），由 flex 的 `align-items: center` 负责垂直居中 |

**自检**：el-button 在默认态与 hover/active/focus 及内容切换后，内容均在按钮内**水平垂直居中**；若有激活态/替换态容器，其内容也水平垂直居中；badge 内文字水平垂直都居中；列表项行内整体垂直居中。若源稿用 margin 实现视觉居中，改造时优先改为 flex 居中并去掉子元素垂直 margin。

**6.3.6.1 el-button 根节点 class 与深度选择器（必做，易错）**

当**源稿容器 class**写在 `<el-button class="[同一容器 class]">` 上时，组件根节点即为 `button.el-button.[容器class]`，**不存在**「容器在内、.el-button 在子级」的 DOM。**禁止**用「`.容器class ::v-deep .el-button`」为该按钮写样式——该选择器只匹配**后代**中的 `.el-button`，会导致**整段样式不生效**，页面仍呈现 Element 默认按钮（错误常见于筛选区「重置」「查询」等）。

| 环节 | 要求 |
|------|------|
| **识别** | DevTools 查看按钮根节点：若自定义 class 与 `el-button` 在同一 `<button>` 上，即属「class 在根节点」。 |
| **修复** | **方案 A**：用「`.容器class.el-button`」及 **`:hover`、`:focus`、`:active`** 写全尺寸、padding、min-width、背景、边框、字色（必要时 `!important`）。**慎用 `type="text"`**：`el-button--text` 强制透明底/边且三态常回退透明，与稿面「小框+描边/浅底」冲突时须改**默认 type（省略）**或 `plain` 再覆盖。`type="primary"` 须覆盖 **默认与三态**及字色。**方案 B**：外层再包 `div`，class 在 `div` 上，则用「父级 `::v-deep` .el-button」。 |
| **子节点** | 按钮内 **img / span** 若沿用源稿 class，常带**静态 flex 用的 margin**（如 `margin: 8px 0 0 16px`），须在按钮内 **`margin: 0`**，布局交给根上 **flex + `align-items` + `justify-content`**（如主按钮图标+文案 `space-between`），与 **6.3.6** 一致。 |
| **并排间距** | 主题 **`.el-button + .el-button { margin-left: 10px }`** 会叠加稿面间距；须在父行取消或改写，再只用各按钮自身 `margin-left` 控制。 |
| **主按钮** | `type="primary"` 时须用「`.自定义class.el-button--primary`」等覆盖 **hover / focus / active** 背景、边框、**字色**，避免状态切换露默认样式。 |

**需求文案（摘要）**：凡将可点击区改为 `el-button` 且把原稿容器 class 合并到按钮根上者，样式选择器必须与 DOM 一致；禁止误用「父级 `::v-deep` .el-button」；**带底/边的次要按钮勿用 `type="text"`**；并排按钮须处理默认 **10px** 相邻间距；子级 **img/span** 须去源稿 margin。

**自检**：样式表含 `.容器class.el-button`（或外层 `::v-deep`）；**默认与 hover、focus、active** 与源稿一致；无不当 `type="text"`；并排无多余 10px；子级无破坏 flex 的 margin。

详见 `data/el-button-root-and-deep.md`（识别步骤、两种修复方案、需求全文、自检清单）。

**6.3.7 下拉框样式与激活态主题色规范**

- **触发器样式**：el-select 的 `.el-input__inner` 须用 `::v-deep` 设置与设计稿一致的 height、line-height、border-radius、font-size、border-color（默认态）；**focus 与 hover 态**的边框色须使用**当前页面主题色**（从 index.css 或设计稿中取主色），不得使用 Element 默认蓝色。须**同时**覆盖：`.el-input__inner:hover`、`.el-input__inner:focus`、`.el-input.is-focus .el-input__inner` 的 `border-color`（Element 在 focus 时给 .el-input 加 .is-focus，漏写则 focus 边框可能仍为默认色）。详见 `data/recognition-and-fix.md` 9.7。
- **下拉选项激活态**：下拉弹层挂载在 body，scoped 无法覆盖。须给 el-select 设置 `popper-class="[folderName]_xxx_dropdown_popper"`，在 Custom.vue 中增加**非 scoped** 的 `<style>` 块，用该 class 覆盖：
  - `.popper-class名.el-select-dropdown .el-select-dropdown__item.selected`：文字色、背景色为主题色/主题浅色（与设计一致）；
  - `.popper-class名.el-select-dropdown .el-select-dropdown__item:hover`：悬停态文字色、背景色为主题色/主题浅色。
- **主题色来源**：从源页面 index.css 或设计稿中提取主色（如高亮边框、选中项背景、主按钮背景），统一用于 el-select 的 focus 边框、下拉选项 selected/hover，以及列表中选中项边框/文字色等，保证激活态与当前主题一致。

**自检**：el-select 触发器尺寸与设计一致；**focus 与 hover** 时边框色均为主题色（见 9.7）；下拉选项选中/悬停为主题色，非 Element 默认蓝。

**6.3.7.1 el-select 右侧箭头/后缀对齐（必做，易错）**

静态稿常用 **`flex` + `justify-content: space-between`** 做「左文案 + 右箭头图」。改为 `el-select` 后，箭头在 **`.el-input__suffix`（绝对定位）** 内，**不得**把同一套 **`display:flex; justify-content:space-between`** 加在 **`el-select` 根节点**（与自定义 class 合并处），否则会干扰内部 `el-input` 布局，表现为**右侧图标水平/垂直偏移**。

另：仅把 **`.el-input__inner`** 改为小高度（如 28px）时，Element 默认 **`.el-input__icon` 的 `line-height` 仍按大输入框（如 40px）**，箭头会**上下不齐**；须用 `::v-deep` 将 **`.el-input__icon` / `.el-select__caret` 的 `line-height`、`height`** 与 inner 对齐，并设置 **`.el-input__suffix` 的 `right`**（对照 index.css 箭头距右缘）、校验 **`padding-right`** 避免文字与箭头重叠。

**需求文案（摘要）**：`el-select` 触发器右侧箭头位置、垂直居中与右内边距须与稿一致；禁止为复刻静态 flex 在 `el-select` 根上使用 `space-between`；改小触发器高度必须同步后缀图标行高/高度与 suffix 定位。

**自检**：根节点无不当 flex+space-between；suffix `right`、icon `line-height`/`height` 与 inner 一致；文案与箭头不重叠。

详见 `data/el-select-suffix-alignment.md`（识别、根因、修复步骤、需求全文、自检清单）。

**6.3.8 多选框激活态主题色规范**

- **选中态**：el-checkbox 默认选中为 Element 蓝色，须用**页面主题色**覆盖。在 checkbox 的自定义 class 下用 `::v-deep` 设置：
  - `父级 ::v-deep .el-checkbox__input.is-checked .el-checkbox__inner`、`父级 ::v-deep .el-checkbox__input.is-indeterminate .el-checkbox__inner`：`background-color`、`border-color` 为页面主题色（与 6.3.7 主题色来源一致）。
- **悬停态**：`父级 ::v-deep .el-checkbox__inner:hover` 的 `border-color` 设为主题色，与设计一致。
- **焦点态（必做）**：见 **6.3.8.1**；仅写 `is-checked` / `:hover` 时，键盘聚焦或点击后仍可能露出 **Element 默认主色蓝**。
- **主题色**：与 el-select、列表选中项等统一，从 index.css/设计稿取主色（如 `rgba(255, 106, 106, 1)`）；**多主色稿面**下须与**该控件所在区块**一致，见 **6.3.8.1**。

**自检**：多选框选中/半选时方框背景与边框为主题色；悬停时边框为主题色；**焦点态（is-focus）** 边框为主题色，非 Element 默认蓝。详见 **6.3.8.1**。

**6.3.8.1 单选/多选主题色：稿面取色、焦点态与 Element 残留蓝（必做）**

**问题识别**

1. **只覆盖了选中与 hover，仍见「蓝框」**：Element UI 2 在 **`.el-checkbox__input.is-focus .el-checkbox__inner`**、**`.el-radio__input.is-focus .el-radio__inner`** 上使用 `$--checkbox-input-border-color-hover` / `$--radio-input-border-color-hover`（即 **Element 主题主色**，常为 `#409EFF`），与 Custom.vue 里为「稿面主题色」设置的 `is-checked` / `:hover` **不是同一套规则**，表现为：点击或 Tab 聚焦后**边框仍蓝**。
2. **单选独有：焦点环为蓝**：**`.el-radio:focus:not(.is-focus):not(:active):not(.is-disabled) .el-radio__inner`** 带 **`box-shadow: 0 0 2px 2px $--radio-input-border-color-hover`**，未覆盖时整圈仍为默认蓝。
3. **主题色选错（多主色页面）**：同一 `index.css` 中常并存 **导航/Tab 高亮蓝**（如 `rgba(0, 116, 252, 1)`）与 **主按钮/设置区/勾选切图色**（如 `rgba(4, 180, 182, 1)`）。将前者套到**设置面板内**的 `el-checkbox` / `el-radio` 会导致与**静态勾选 PNG、邻近竖条（`section_*`）、主按钮**不一致。

**修复方法（在控件父级自定义 class 下 `::v-deep`，与已写的 checked/hover 同色）**

| 状态 | el-checkbox | el-radio |
|------|-------------|----------|
| 焦点（键盘/点击后 input 带 `.is-focus`） | `父级 ::v-deep .el-checkbox__input.is-focus .el-checkbox__inner { border-color: [稿面主题色]; }` | `父级 ::v-deep .el-radio__input.is-focus .el-radio__inner { border-color: [稿面主题色]; }` |
| 单选：原生 focus 环 | — | `父级.el-radio:focus:not(.is-focus):not(:active):not(.is-disabled) ::v-deep .el-radio__inner { box-shadow: 0 0 2px 2px [稿面主题色半透明]; }`（或与稿一致改为 `none`） |

**稿面主题色怎么取（须自当前页 index.css，禁止抄其它页 Custom）**

1. 定位**该控件在 index.vue 中对应的静态结构**（原勾选/单选切图、或同一块卡片内的主按钮、标题竖条 `background-color`）。
2. 在 **index.css** 中查 **`.thumbnail_*` / `.image-wrapper_*` 背景**、**同区主按钮**、**`section_*` 装饰条** 的 `background-color` / `border-color`，取与**交互控件**一致的那一支作为主色。
3. **同一页**内 `el-pagination`、列表 Tab 若用蓝 A，设置区勾选若用青 B，则 **checkbox/radio 须用 B**，不得统一成 A。

**需求文案（摘要）**

- 替换 `el-checkbox` / `el-radio` 后，**选中、悬停、焦点（`.is-focus`）及单选 `box-shadow` 焦点环**须全部使用**该区块稿面主题色**，不得残留 Element 默认蓝。
- **主题色**须从**当前文件夹** `index.vue` + `index.css` **就近**提取；多主色时**表单控件与静态勾选/主按钮同色**，不得误用仅用于列表或 Tab 的色值。

**自检**：DevTools 选中 `.el-checkbox__input` / `.el-radio__input`，手动切换 `:focus`、查看是否带 `.is-focus`，确认 **inner 边框与（单选）box-shadow** 均为稿面色；与 index 静态区主色对比一致。

详见 `data/radio-checkbox-theme-and-focus.md`（识别步骤、选择器对照、需求全文）。

**6.3.9 分页（el-pagination）替换与主题色规范**

- **替换时必须删除的 DOM**：分页区域整块替换为单个 `el-pagination` 时，**须删除该区域内全部原始静态内容**，包括「共 xxx 条」文案与图标、所有静态页码块（如 1、2、3…）、上一页/下一页的静态图标或按钮、「xx条/页」的静态或伪下拉。不得在 el-pagination 外再保留一份上述内容，否则会出现两套分页。
- **layout**：使用 `layout="total, prev, pager, next, sizes"`，由组件自带展示总数、上下页、页码、每页条数。
- **样式**：用 `::v-deep` 对 `.el-pagination__total`、`.btn-prev`/`.btn-next`、`.el-pager li`、`.el-pagination__sizes .el-input__inner` 设置与设计一致的尺寸、边框、圆角、字号。**上一页/下一页按钮**须设 `padding: 0`、`display: inline-flex`、`align-items: center`、`justify-content: center` 使图标居中，并设默认态 `color`，内部 `.el-icon` 设 `color: inherit`（见 recognition-and-fix 9.6）。
- **激活态/主题色**：**当前页** `.el-pager li.active` 的背景色、边框色须为页面主题色；**上一页/下一页** hover 态须**同时**设边框色与**图标色**为主题色（须为 `.btn-prev:hover`、`.btn-next:hover` 设 `color`，并为 `.btn-prev:hover .el-icon`、`.btn-next:hover .el-icon` 设 `color`，见 9.5）；**页码** `.el-pager li:hover` 边框/文字色为主题色；**每页条数 sizes** 的 el-select 触发器（.el-input）须在 **focus 与 hover** 时边框均为主题色（须同时覆盖 `.el-input__inner:hover`、`.el-input__inner:focus`、`.el-input.is-focus .el-input__inner`，见 9.7）。
- **sizes 下拉主题色**：el-pagination 内部的「每页条数」为 el-select，其下拉层挂载在 body 且无法单独设置 popper-class。须在 Custom.vue 中增加**非 scoped** 的 `<style>`，**同时覆盖**选中态（`.selected`）、键盘焦点态（`.hover`）、悬停态（`:hover`）及选中+悬停（`.selected:hover`、`.selected.hover`），对 `color`、`background-color` 使用 `!important`；**若 hover 仍不生效**须使用**双重 class** 提高特异性（如 `.el-select-dropdown .el-select-dropdown__item.el-select-dropdown__item:hover`）或 `body .el-select-dropdown .el-select-dropdown__item`，使 sizes 下拉的**选中项与悬停项**与页面主题一致。详见 `data/recognition-and-fix.md` 第 3.4、9.4 节。

**自检**：已删除原始分页全部静态内容，仅保留一个 el-pagination；**上一页/下一页** 按钮图标居中、默认态与 hover 态颜色正确（见 9.6、9.5）；**sizes 的 el-select 触发器** focus 与 hover 时边框均为主题色（见 9.7）；当前页、**sizes 下拉选中/悬停**均为主题色（见 9.4）。

**6.3.10 单选框（el-radio）识别与主题色规范**

- **识别**：源页面存在「多选一」互斥选择（如多个选项中仅能选一项），包括原生 `<input type="radio">` 或 div + 文案/图标模拟的单选区域，须替换为 `el-radio-group` + `el-radio`。
- **替换**：删除原单选区域全部 DOM，改为 `<el-radio-group v-model="radioValue" class="[folderName]_radio_group">` + `<el-radio v-for="..." :label="..." :key="...">...</el-radio>`；在 data 中定义选中值（如 `radioValue`），在 methods 中实现 `@change` 处理（如 `handleRadioChange`）。
- **样式与源页一致**：用 `::v-deep` 对 `.el-radio__inner`、`.el-radio__label` 等设置与 index.css/设计稿一致的尺寸、圆角、边框、字号、颜色；整体布局（横向/纵向、间距）与源页面一致。
- **激活态与选中项主题色**：Element 默认选中为蓝色，须改为**页面主题色**。在单选框父级 class 下用 `::v-deep` 设置：
  - **选中态**：`父级 ::v-deep .el-radio__input.is-checked .el-radio__inner` 的 `border-color`、`background-color` 为页面主题色（与 6.3.7/6.3.8 主题色来源一致）；`父级 ::v-deep .el-radio__input.is-checked + .el-radio__label` 的文字色可设为主题色或与设计一致。
  - **悬停态**：`父级 ::v-deep .el-radio__inner:hover` 的 `border-color` 设为主题色。
  - **焦点态与焦点环（必做）**：见 **6.3.8.1**（`.is-focus` 边框 + `.el-radio:focus:not(...)` 的 `box-shadow`）。
- **主题色来源**：从 index.css 或设计稿中取主色（如选中项背景、主按钮背景），与 el-select、el-checkbox 等统一；**多主色稿面**下与设置区静态控件一致，见 **6.3.8.1**。

**自检**：单选项已替换为 el-radio-group + el-radio；尺寸、布局、文字与源页一致；选中项与悬停态圆点/边框为主题色；**焦点态与 focus 环**为主题色，非 Element 默认蓝（见 **6.3.8.1**）。

**6.3.10.1 筛选项折行与高度自适应（必做，适用时）**

将横向筛选改为 `el-radio-group` 后，若在较窄宽度或选项较多时**允许折行**，须避免**固定高度裁切**与**行间重叠**。

| 环节 | 要求 |
|------|------|
| **筛选外层卡片** | 勿用固定 `height` 锁死整张筛选卡；改为 **`min-height: [设计稿高度]` + `height: auto`**，并设 **`padding-bottom`**，使多行选项撑开卡片。 |
| **筛选行（标签 + 选项组）** | 行容器 **`flex-wrap: wrap`**，**`align-items: flex-start`**（或 `align-content: flex-start`），**`gap`** 控制换行后的纵向/横向间距；行宽在 **`max-width` 与面板一致**下可用 **`width: 100%`** 覆盖稿中过窄的固定 `width`。 |
| **左侧标签** | **`flex-shrink: 0`**；**`height: auto` + `min-height: [原行高]`**，与选项首行对齐，避免固定 `height` 与折行冲突。 |
| **`el-radio-group`** | **`flex: 1`、`min-width: 0`、`flex-wrap: wrap`**，**`row-gap` / `column-gap`** 统一选项间距；**减少纯 `margin-left` 链**，避免换行后首列/次行边距错乱。 |
| **`.el-radio` / `__label`** | 使用 **`min-height`** 对齐设计行高，**`height: auto`**；必要时 **`padding`** + **`line-height`**，避免文字与背景 pill 上下被裁切。 |
| **名称行（标签 + 搜索）** | 若与筛选区上下相邻，该行勿用固定 **`height`** 压过折行后的筛选区；改为 **`min-height` + `height: auto`**，必要时 **`flex-wrap` + `gap`**。 |

**识别要点**：在 `Custom.vue` 的 scoped 样式中搜索筛选相关容器的 **`height:`**；若筛选行已 `flex-wrap: wrap` 仍重叠，优先查外层卡片与子行是否仍为固定高度、选项组是否缺 **`min-width: 0`**、间距是否仅依赖 **`margin-left`**。

**自检**：缩小视口或增加选项后，筛选区**自动增高**，**无与下一行筛选或列表重叠**；选项多行时间距清晰；设计宽度下单行布局仍与稿面基本一致。

详见 `data/filter-row-wrap.md`（识别步骤、修复细则、需求文案、自检清单）。

> **取色组件选型（摘要）**：颜色选择均由 **触发区 + 下拉面板** 组成；**以下拉面板的版式** 判断图1 / 图2，**不以触发区**（色块、A 字条等）单独判断。**图1**（预设矩阵类「填充」面板等）→ **`el-color-picker-extend`**；**图2**（Element 默认取色下拉：SV + 竖色相条 + 清空/确定）→ **`el-color-picker`**。替换后须 **删除** 原静态或重复的取色 DOM，避免两套 UI 并存。识别清单、需求文案与错配修复见 **`data/el-color-picker-extend.md`** §「颜色选择：触发与下拉的共同结构」、§「图1 / 图2 对照与识别清单」、§「常见错配与修复」。

**6.3.11 `el-color-picker`（图2）与页内静态「填充」删除；`el-color-picker-extend`（图1）集成注意（必做，适用时）**

| 环节 | 要求 |
|------|------|
| **通用规则** | **触发与下拉**：点击后展开的区域才是选型依据；图1、图2 的 **触发区都可以是「颜色选择按钮」类控件**，区别仅在 **展开内容** 是稿面定制填充面板还是 Element 默认面板。详见 **`data/el-color-picker-extend.md`** §「颜色选择：触发与下拉的共同结构」。 |
| **识别（稿面）** | **图2**：若展开 look 为 **SV 大方块 + 右侧竖向色相条 + 底栏 Hex +「清空」「确定」** → **`el-color-picker`**；常见 **触发** 为「字体颜色」行 **小框：A + 下划色条 + 箭头**（静态多为 A + png + 绝对定位色条）→ 用 **透明叠层** 盖住触发区。**图1**：展开为 **标题「填充」+ 色块矩阵 + 滑条 + #hex + % + RGB +「最近使用」** 等（页内整区或弹层）→ **`el-color-picker-extend`**，并 **删除** 原静态切图/伪输入整段 DOM。 |
| **触发器样式** | 需与稿一致时：用 **A**（与 index.css 字号/字色一致）+ **横向色条**（`background-color` 绑定 `v-model` 当前色，透明时用 `transparent`）+ **右侧三角**（CSS border 或 8×8 内联图）。**勿**假设 Element UI 2.x 提供 `#trigger` 插槽（**无**）。 |
| **实现图2（`el-color-picker`）** | **透明触发区覆盖**：外层 `position: relative`，底层为 **可见** 自定义面（`pointer-events: none`），上层 **`el-color-picker` 绝对定位铺满**，对 **`::v-deep .el-color-picker__trigger`** 设 **宽高 100%、无边框、`opacity: 0`**，保证点击落在官方触发器上；**勿**对根节点 `.el-color-picker` 整体 `opacity: 0`，否则 **下拉面板** 会被一并隐藏。`popper-class` 仍用于挂载到 body 的下拉样式。 |
| **实现图1（`el-color-picker-extend`）** | 在页面中放置 **`<el-color-picker-extend v-model="fillColorRgba" recent-storage-key="..." />`**（工程内全局注册），**删除** 原页内填充区全部静态节点；父容器若在 index.css 中 **固定高度**，须改为 **`height: auto`**（或加修饰 class 覆盖），见 **`data/el-color-picker-extend.md`**。 |
| **删除页内块** | 已用 **`el-color-picker-extend`** 或 **`el-color-picker`** 承担取色后，须 **删除** index 稿中 **整块** 原「填充」模拟区（多图色矩阵、独立渐变条图、#hex、RGB 行、静态「最近使用」色块行等），**禁止**在页面内再保留一套取色 UI；扩展组件内置「最近使用」时不得与静态切图并存。 |
| **多行相同控件** | 多条「字体颜色」行共用同一 **`v-model`** 即可；每行一个 `el-color-picker`（透明覆盖）或仅一行有 picker（另一行只读展示）按稿面二选一，避免重复逻辑分叉。 |

**需求文案（摘要）**

- **图2 字体颜色**：**A + 随当前色变化的下划线 + 下拉示意**，用透明 `el-color-picker` 覆盖点击；**不得**整页 `opacity: 0` 包住取色组件。
- **图1 填充区**：用 `el-color-picker-extend` 后：**删除** 原静态「填充」**页内大面板**（色格/滑条图、拼出来的 hex/rgb/最近使用等），不重复保留模拟弹层。

**自检**：工具条视觉与 index 一致；点击能打开官方取色下拉；下拉内操作正常；页面无第二套静态取色/最近使用切图。

详见 **`data/el-color-picker-extend.md`** **§「字体颜色触发器（Element UI 2）」**。

#### 6.4 循环渲染规范

将重复的结构改为 `v-for` 循环：

```vue
<!-- ❌ 改造前（静态重复） -->
<div class="item">内容1</div>
<div class="item">内容2</div>
<div class="item">内容3</div>

<!-- ✅ 改造后（动态循环） -->
<div 
  v-for="(item, index) in itemList" 
  :key="item.id" 
  :class="['item', getItemClass(index)]"
>
  {{ item.content }}
</div>
```

#### 6.5 图片路径处理规范（⭐重要）

**⚠️ 路径基准：** `Custom.vue` 与 `index.vue` 同目录，位于视图文件夹根（如 `src/views/shushi/`），图片实际在 `src/views/${folderName}/assets/img/`。所有路径均相对于 **Custom.vue 所在目录** 解析。

| 场景 | 正确做法 | 错误做法 |
|------|---------|---------|
| **Template 中的 &lt;img&gt; 标签** | `:src="require('./assets/img/xxx.png')"` 或 data 中 `require('./assets/img/xxx.png')` | `:src="require('./img/xxx.png')"` |
| **Custom.vue 内 &lt;style&gt; 中的 background-image** | `url(./assets/img/xxx.png)` | `url(./img/xxx.png)` |
| **data() 中定义的图片路径** | `img: require('./assets/img/xxx.png')` | `img: require('./img/xxx.png')` |

**为什么 Custom.vue 里 CSS 必须用 `./assets/img/`？**
- 源文件 `assets/index.css` 在 `assets/` 下，其中 `url(./img/xxx)` 是相对于 **assets 目录** 的，指向 `assets/img/`，在 index.css 中正确。
- 样式内联到 **Custom.vue** 后，构建时相对路径的基准是 **Custom.vue 所在目录**（视图文件夹根），`./img/` 会解析到不存在的 `视图文件夹/img/`，导致图片 404。
- 因此写入 Custom.vue 的 CSS 中必须使用 `url(./assets/img/xxx.png)`，才能正确指向 `视图文件夹/assets/img/`。

**识别与修复（通用流程）：**

1. **识别（以稿源 CSS 为准）**
   - 在 `${folderName}/assets/index.css`（及其链式 `@import`）中搜索：
     - `url(./img/`、`url("./img/`、`url('./img/`（含单/双引号与无引号）
     - `background:` / `background-image:`（定位所有背景图声明，包含 sprite/mergeImage）
   - 在 `index.vue` 中搜索：`src="./assets/img/`、`src='./assets/img/`、`:src=`（定位所有 <img> 引用）

2. **写入 Custom.vue 时的规则（必须执行）**
   - **Template / data()**：图片路径统一为 `require('./assets/img/文件名')`。
   - **<style scoped>**：从 index.css 拷贝过来的背景图路径，凡 `url(./img/xxx)` 一律改为 `url(./assets/img/xxx)`。

3. **修复已有 Custom.vue（问题排查顺序）**
   - **背景区域图片样式异常 / 背景图不显示**：
     1) 在 Custom.vue 的 `<style scoped>` 中搜索 `url(./img/`，若存在则全局替换为 `url(./assets/img/`。
     2) 检查是否误写成 `url(@/...)` 或 `url(/...)`（本 Skill 禁止），统一改为 `url(./assets/img/...)`。
     3) 检查迁移时是否丢了 `background` 的关键子属性：`background-repeat`、`background-position`、`background-size`（如源为 `background: url(...) 100% no-repeat; background-size: 100% 100%;`），必须完整迁移，否则会表现为「背景拉伸不对/不铺满/位置偏移」。
   - **<img> 不显示**：检查是否为 `require('./assets/img/xxx')`，勿用 `require('./img/xxx')`。

**修复自检清单：**
- [ ] Custom.vue 的 style 中：不存在 `url(./img/...)`，所有背景图均为 `url(./assets/img/...)`
- [ ] Custom.vue 的 template/data 中：不存在 `require('./img/...)`，所有图片均为 `require('./assets/img/...)`
- [ ] 对每个背景块核对：`background` 四要素（image / repeat / position / size）与 index.css 一致

#### 6.6 数据与方法同步生成

**❌ 禁止分步执行：**
```vue
<!-- 错误：只写 template，不写 data 和 methods -->
<template>
  <el-input v-model="inputValue" @change="handleChange" />
</template>
<script>
export default {
  // data 和 methods 稍后补充
}
</script>
```

**✅ 必须同步完成：**
```vue
<template>
  <el-input v-model="inputValue" @change="handleChange" />
</template>
<script>
export default {
  data() {
    return {
      inputValue: ''  // ✅ template 中使用的数据必须定义
    }
  },
  methods: {
    handleChange() {  // ✅ template 中的事件必须实现
      // 处理逻辑
    }
  }
}
</script>
```

#### 6.7 样式匹配标准（按元素重要性）

改造后视觉效果须与源文件一致，按元素类型采用不同匹配级别：

| 标准 | 适用场景 | 必须匹配的属性 |
|------|----------|----------------|
| **完整匹配** | 列表项、卡片、主容器 | 盒模型 + 尺寸 + 布局 + 文字 + 边框 + 视觉效果 + 交互状态 |
| **简化匹配** | 筛选项、按钮、标签 | 尺寸 + 布局 + 文字 + 边框 + 视觉效果 + 交互状态 |
| **文字匹配** | 标题、描述文本 | font-family、font-size、color、font-weight、line-height |
| **尺寸匹配** | 图片、图标 | width、height、border、border-radius、box-shadow |

**布局与验证**：PC 端流式布局用 `width: 100%`、百分比宽度，优先 Flex/Grid；尺寸、颜色、字体、间距等用浏览器开发者工具对比 Computed 样式，误差不超过 1px，颜色精确到 rgba。若样式不一致，检查选择器优先级、是否需 `::v-deep` 覆盖、是否有冲突样式。

#### 6.8 列表项内容溢出规范（v-for 列表必做）

凡用 **v-for** 渲染的列表/卡片，其项内**由数据驱动的文本**（标题、作者、描述等）不得沿用 index.css 中该文本的**固定 width/height**，否则长文案会溢出。须按 `data/list-item-overflow.md` 执行：

- **列表项根节点**：设 `overflow: hidden`、`box-sizing: border-box`；若项内有固定宽高的内容区（如 first-inner），也设 `overflow: hidden`、`min-width: 0`。
- **动态文本节点**：将固定 `width`/`height` 改为 **max-width**（按内容区可用宽度取值），保留 `overflow-wrap: break-word`，并加 `overflow: hidden`、必要时 `min-width: 0`（flex 子项）。不得为「与设计稿数值一致」保留会导致溢出的固定宽度。

详见 `data/list-item-overflow.md`（识别步骤、修复方法、需求文案、自检清单）。

#### 6.9 文字竖排与横排识别（必做）

改造时须根据 index.css 与设计稿**识别列表/卡片内标题、作者等为竖排还是横排**，避免将竖版做成横版。识别规则见 `data/text-direction-vertical-horizontal.md`：

- **竖排**：index.css 中该文本为**窄宽高瘦**（width 约 14px～24px、height 明显大于 width、line-height 与 width 接近），或设计语义为古诗词/传统竖版 → 在 Custom.vue 中为该节点设 `writing-mode: vertical-rl`（或 vertical-lr）、`text-orientation: upright`、**display: inline-block**（若为 span），并设与设计一致的 width、max-height、line-height、overflow: hidden。竖排下的**复合文案**（如「朝代·作者」）若设计为单列，须用单段拼接，**不得用 `<br>`**（否则竖排会变多列），见 data/text-direction-vertical-horizontal.md 4.2。
- **横排**：无上述特征或为常规 UI 文案 → 不设 writing-mode，按横排布局处理。

详见 `data/text-direction-vertical-horizontal.md`（识别步骤、修复方法、需求文案、自检清单）。

#### 6.10 列表样式（单行不换行）（必做）

凡用 **v-for** 渲染且设计上为**单行横向排布**的列表/卡片项（如左装饰 + 内容 + 标题 + 作者 + 右装饰等），列表项根节点若为 flex 横向布局，须设 **flex-wrap: nowrap**，不得使用 flex-wrap: wrap，避免项内换行导致错位。列表项根节点须同时设 **overflow: hidden**、**box-sizing: border-box**（与 6.8 一致）。详见 `data/list-style.md`（识别步骤、修复方法、需求文案、自检清单）。

#### 6.11 列表行高度与对齐规范（必做）

凡用 **v-for** 渲染的列表，其列表行（普通行、第一行、第二行等）必须满足以下要求，避免文字被截断和右侧列对齐问题：

- **高度修复**：列表行使用 `min-height` 而非仅固定 `height`（如 `min-height: 23px; height: 23px;`），确保行内文字（`line-height` 与 `height` 一致）不被截断；行内元素需设置 `min-height` 与 `height` 一致（如 `min-height: 22px; height: 22px;`）。
- **对齐修复**：列表行内各列（如课包名、讲次信息、状态信息、更新信息）需设置**固定宽度**（从 index.css 中查找对应列的宽度，如 `.image-text_4 { width: 134px; }`），并设置 `flex-shrink: 0` 防止在 flex 布局中被压缩；各列的 `margin-left` 值需与 index.css 中的值**完全一致**（误差不超过 1px）。
- **溢出处理**：列内文本（如课包名）可用 `max-width` + `overflow: hidden` + `text-overflow: ellipsis` 防止溢出，但列容器本身需保持固定宽度。
- **多 rowKind 统一行高与列槽（表格形列表必做）**：若同一列表存在多种 `rowKind`（首行灰底、高亮行、普通双列、续讲无左列等），须 **(1)** 以静态稿**最高行**为统一 `min-height` 基准，列表项外层与内层行轨道共用 `align-items: center`；**(2)** 设**固定宽度课包列槽**（宽度 = index.css 首行课包区宽度），`normal` 与续讲行均经该槽对齐，续讲行用**空槽占位**，禁止单独使用超大整行 `margin-left` 顶替列槽；**(3)** 讲次列紧贴槽右缘用**统一间距**（如 20px），项间距仅用 **`.list_item + .list_item`**（或统一 padding），禁止「仅某类行」的相邻兄弟外边距分叉；**(4)** 行内子元素垂直对齐以 flex 为主，`margin-top` 置 0（绝对定位结构除外）。

详见 `data/list-row-height-alignment.md`（含第 8 节：多 rowKind 统一行高与列槽对齐；识别步骤、修复方法、需求文案、自检清单）。

#### 6.12 双列列表左右数据源独立（必做，适用时）

若列表在语义上为**左列 + 右列**（如课包 + 讲次/状态/更新），且存在**续讲等行左侧无单元格**或两侧数据将来来自不同接口，须：

- 使用 **`packageList`（左）与 `lectureList`（右）等两套独立 `data`**，不得以单一合并对象为唯一数据源；`v-for` 通常以**右侧（明细）列表**为主循环，左侧用 **`packageList[index]`** 对齐。
- 左侧无内容行：左列数据用 **`title: null`（或等价）**，并设 **`rowKind`**（如 `right_only`、`right_only_compact`）走**独立 template + 独立样式类**，margin/width **对照 index.css 中单独 group**，禁止用空字符串 + 普通双列行凑合。

详见 `data/list-dual-column-independent.md`（识别步骤、修复方法、需求文案、自检清单）。

### 步骤 7: 验证生成的代码

生成 `Custom.vue` 后，必须进行以下验证：

#### 7.1 样式检查
- [ ] 尺寸与源文件一致（误差不超过 1px）
- [ ] 颜色完全一致（rgba 值相同）
- [ ] 字体、间距完全一致
- [ ] 视觉效果与源文件 100% 匹配
- [ ] 带外框的搜索框：容器高度与设计一致，**容器有 border，hover 与 focus-within 时边框为主题色**（见 9.8），无双重边框，前缀图标与文字垂直对齐，**placeholder 与输入文字垂直居中**，placeholder 颜色正确，无错位或溢出；容器设 max-width、min-width: 0，所在行设 min-width: 0，不溢出父级（见 6.3.1、6.3.1.1、data/search-input-and-page-overflow.md）
- [ ] **页面不横向溢出**：主卡片/底栏/搜索框所在行使用 width:100%+max-width+min-width:0；底栏中间文案用 margin-left:auto；无横向滚动（见 6.3.1.1、data/search-input-and-page-overflow.md）
- [ ] **垂直居中**：el-button 及 div+背景图+文字按钮内文字均**水平与垂直都居中**，文字节点 width: 100%、margin: 0、display: inline-flex + align/justify center，无单侧 margin 导致偏位；列表/步骤 badge 内文字水平垂直都居中；列表项内文字与图标均在容器内垂直居中（见 6.3.6、recognition-and-fix 9.2）
- [ ] **el-button 与深度选择器**：自定义 class 在按钮根上时，已用 `.class.el-button` 或外层包裹 + `::v-deep`，**未**误用「`.class ::v-deep .el-button`」导致重置/查询等样式不生效（见 6.3.6.1、`data/el-button-root-and-deep.md`）
- [ ] **el-button 类型与三态**：带底/边次要按钮**未误用** `type="text"`；已写全 **:hover / :focus / :active**；并排已处理 **`.el-button + .el-button`**；子 **img/span** 无源稿静态 margin（见 `data/el-button-root-and-deep.md` 2.1～2.3）
- [ ] **下拉框与激活态主题色**：el-select 触发器 **focus 与 hover** 边框色均为主题色（须覆盖 :hover、:focus、.el-input.is-focus .el-input__inner，见 9.7），下拉选项选中/悬停为主题色；分页 sizes 等挂载 body 的下拉须用非 scoped 样式覆盖选中/悬停为主题色，未生效时用 !important（见 6.3.7、recognition-and-fix 9.1、9.7）
- [ ] **el-select 右侧箭头对齐**：未在 `el-select` 根上误用 `flex`+`space-between`；小高度触发器已同步 `.el-input__suffix` / `.el-input__icon`（`.el-select__caret`）与 `padding-right`（见 6.3.7.1、`data/el-select-suffix-alignment.md`）
- [ ] **多选框激活态主题色**：el-checkbox 选中/半选/悬停为主题色（见 6.3.8）
- [ ] **纵向模块勾选列**：配置/预览区左列 16×16 方框列已改为 el-checkbox，已删方框切图；`moduleFlags`（或等价）与右侧 `v-show` 联动；无内联文案时已隐藏 `.el-checkbox__label`（见 6.3.4.1、`recognition-and-fix.md` §2.2.1、§3.2.1）
- [ ] **横向工具条 / 尾行勾选**：英式音标、鼓点音频、单词书写等横排/尾行左侧方框已改为 el-checkbox，无静态图残留；IPA 区、鼓点控件、书写预览等已 `v-show` 联动；「全选所有模块」已包含上述布尔（见 6.3.4.2、`recognition-and-fix.md` §2.2.2）
- [ ] **多选框尺寸全页统一**：模块勾选共用同一 class 与同一套 `::v-deep`（根、`__input`、`__inner`、`__inner::after`、选中勾线色），与 index.css 方框一致，无混排（见 6.3.4.2、`recognition-and-fix.md` §3.2.2）
- [ ] **多选框 inner 与槽位分层**：已从 index.css 核对 **wrapper 槽位** 与 **thumbnail（或内层 wrapper）方框视觉** 宽高；`el-checkbox__inner` 与方框视觉层一致，`__input`/根与槽位一致并居中 inner，非笼统 16×16 inner（见 **6.3.4.3**、`recognition-and-fix.md` §3.2.3）
- [ ] **单选框**：已替换为 el-radio-group + el-radio；样式与源页一致；选中项与悬停态为主题色（见 6.3.10）
- [ ] **筛选折行**：筛选项可折行时，筛选卡片与各筛选行使用 **min-height + 自动增高**，**gap** 控制间距，**el-radio-group** 具备 **flex:1、min-width:0、flex-wrap**，无行间/与列表重叠（见 6.3.10.1、data/filter-row-wrap.md）
- [ ] **分页**：已删除原始分页全部静态内容，仅保留一个 el-pagination；**sizes 的 el-select 触发器** focus 与 hover 时边框均为主题色（见 9.7）；**上一页/下一页** 已设 padding:0、inline-flex、居中及默认态 color（见 9.6），hover 时边框与 .el-icon 均为主题色（见 9.5）；**sizes 下拉**选中/悬停均为主题色，未生效时已用双重 class 或 body 前缀及 !important（见 6.3.9、recognition-and-fix 9.4、9.5、9.6、9.7）
- [ ] **列表项内容不溢出**：v-for 列表项根节点已设 overflow: hidden、box-sizing: border-box；动态文本已用 max-width + overflow-wrap + overflow: hidden，无固定 width/height 导致溢出（见 6.8、data/list-item-overflow.md）
- [ ] **列表行高度与对齐**：v-for 列表行（普通行、第一行、第二行等）已使用 min-height 而非仅固定 height，行内元素已设 min-height 确保文字不被截断；各列（如课包名、讲次、状态、更新）已设置固定宽度（从 index.css 查找）、flex-shrink: 0，各列 margin-left 值与 index.css 完全一致（误差不超过 1px）；在浏览器中确认文字完整显示、右侧列位置与设计稿一致（见 data/list-row-height-alignment.md）
- [ ] **多 rowKind 统一行高与列槽**：若存在多种 rowKind，列表项已统一 min-height 与行轨道 align-items:center；已设课包列槽 W_package，续讲行为空槽而非整行超大 margin-left；讲次列起点统一；项间距无「仅某类行」分叉（见 data/list-row-height-alignment.md 第 8 节）
- [ ] **双列列表左右独立**：若为左列+右列表格形列表，已使用两套独立数据源（如 packageList + lectureList），续讲/无左列行已用 rowKind 与独立布局类，未用单对象合并左右字段或空 courseName + 普通行冒充（见 6.12、data/list-dual-column-independent.md）
- [ ] **文字竖排/横排与设计一致**：已根据 index.css「窄宽高瘦」与设计语义识别竖排；竖排节点已设 writing-mode、text-orientation: upright、display: inline-block（若为 span）及 width/max-height/overflow；竖排复合文案（如朝代·作者）未用 `<br>`，作者区无塌陷错位（见 6.9、data/text-direction-vertical-horizontal.md）
- [ ] **列表项单行不换行**：单行设计的 v-for 列表项根节点已设 flex-wrap: nowrap、overflow: hidden、box-sizing: border-box，项内无换行错位（见 6.10、data/list-style.md）

#### 7.2 功能检查
- [ ] 循环渲染正常工作
- [ ] Element UI 组件正常显示和交互
- [ ] **取色 / 填充**：已按稿面 **图1 / 图2** 选用 **`el-color-picker-extend`** 或 **`el-color-picker`**（见 **`data/el-color-picker-extend.md`** §选型），并已 **删除** 原静态/重复取色 DOM；图2「字体颜色」工具条已按 **6.3.11** 做 A+下划线+箭头；按该文档 **自检** 与 **集成注意**（如父级 `height: auto`）逐项核对
- [ ] 每个组件使用的数据均在 data() 中定义，每个事件绑定（@click、@change、@size-change 等）均在 methods 中实现
- [ ] 所有可点击按钮均已绑定 @click 并实现对应 handleXxx 方法
- [ ] 所有点击事件有响应，数据绑定正确

#### 7.3 代码质量检查
- [ ] Class 命名符合规范（无数字、无连字符、无驼峰）
- [ ] 所有数据在 data() 中定义
- [ ] 所有方法在 methods 中实现
- [ ] 没有未使用的变量
- [ ] 没有 console.log（除非必要）

**搜索框样式异常时**：按 6.3.1 带外框搜索框规范检查——外层容器 flex + align-items: center + box-sizing: border-box；el-input 高度 100%；el-input__inner 高度略小于容器、无重复边框、背景透明、border-radius 与容器一致；placeholder 用 ::v-deep .el-input__inner::placeholder 设置；el-input__prefix 与自定义图标垂直居中。

#### 7.4 路由登记检查（交付必做）

- [ ] 已在路由文件中为 `src/views/${folderName}/` 补充与项目约定一致的访问路径（常见：**静态** `index.vue` 与 **动态** `Custom.vue` 各一条，如 `/shushi` 与 `/shushi-custom`）。
- [ ] `import` 路径指向真实文件，`component` 与变量一致，无重复 `path` / `name`。
- [ ] 本地访问新路径无 404，控制台无组件加载错误。

识别步骤、修复模板、需求文案与自检全文见 **`data/router-sync.md`**。

### 步骤 8: 路由登记与校验（`Custom.vue` 写入完成后）

在 **`Custom.vue` 生成或更新已落盘** 之后执行（可与步骤 7 并行收尾，但须在交付前完成）：

1. **读取**项目路由入口（本仓库为 `src/router/index.js`）。
2. **搜索** `${folderName}` 与 `views/${folderName}/Custom.vue`；对照仓库内已有视图（如 `gushi`、`yingyu`）的 **静态 + 动态** 成对路由约定。
3. **缺失则补全**：`import` 两个组件（`index.vue`、`Custom.vue`），在 `routes` 中追加 `path` / `name` / `component`，风格与现有条目一致。
4. **自检**：浏览器打开新 path，确认页面渲染且无报错。

**禁止**：根据路由反推当前页 UI；不得省略本步骤导致 `Custom.vue` 仅存在于磁盘却无法访问。

---

## data/ 文档索引

详细规范说明请参考 `data/` 目录下的文档：

| 分类 | 文件 | 主要内容 |
|------|------|----------|
| 项目配置 | `data/project-config.md` | 文件路径、技术栈、改造目标、改造前后示例 |
| 核心规范 | `data/style-consistency.md` | 样式一致性、响应式布局、验证方法 |
| 核心规范 | `data/class-naming.md` | CSS 类命名规范 + Class 重命名强制要求 |
| 核心规范 | `data/render.md` | 循环渲染、v-for、图片路径、常见错误 |
| 核心规范 | `data/element-ui-style.md` | Element UI 替换规范、样式覆盖与深度选择器 |
| 核心规范 | `data/style-match-standard.md` | 按元素重要性的样式匹配标准 |
| 执行流程 | `data/execution-flow.md` | 执行前准备、开发原则、组件同步生成、验证流程 |
| 任务清单 | `data/tasks.md` | 任务 1～5 的步骤与验收标准 |
| 验证与验收 | `data/validate.md` | 最终验证清单：样式 / 功能 / 代码质量检查 |
| 常见问题 | `data/faq-solutions.md` | 样式、循环、图片、布局、交互等常见问题及解决方案 |
| 识别与修复 | `data/recognition-and-fix.md` | 下拉框、多选框、**纵向模块勾选列（§2.2.1、§3.2.1）**、**横向/尾行（§2.2.2）**、**多选尺寸统一（§3.2.2）**、**多选尺寸读取 wrapper/thumbnail（§3.2.3）**、**单选框**（含折行见 `filter-row-wrap.md`）、带外框搜索框、**分页**、**背景区域图片样式 / 背景图不显示**的识别与修复；按钮与列表内文字垂直居中的识别与修复（含自检清单） |
| 识别与修复 | `data/search-input-and-page-overflow.md` | **带外框搜索框 placeholder 垂直居中**与**输入框/底栏按钮不溢出页面**的识别、修复与需求文案 |
| 识别与修复 | `data/list-item-overflow.md` | **列表项内容溢出**：v-for 列表内动态文本的识别、修复（max-width/overflow）、需求文案与自检 |
| 识别与修复 | `data/list-row-height-alignment.md` | **列表行高度与对齐** + **多 rowKind 统一行高与列槽**：min-height、固定列宽、flex-shrink；表格形多行类型列表的统一行高、课包列槽、续讲空槽、项间距与 flex 垂直居中；需求文案与自检（含第 8 节） |
| 识别与修复 | `data/list-dual-column-independent.md` | **双列列表左右独立**：左列+右列数据源分离、续讲无左列行 rowKind 与独立布局、禁止单对象硬合并与空字段冒充 |
| 识别与修复 | `data/text-direction-vertical-horizontal.md` | **文字竖排与横排**：根据 index.css 窄宽高瘦与设计语义识别竖排/横排，修复（writing-mode）、需求文案与自检 |
| 识别与修复 | `data/list-style.md` | **列表样式（单行不换行）**：v-for 列表项为单行横向排布时 flex-wrap: nowrap、overflow/box-sizing，识别、修复与自检 |
| 识别与修复 | `data/filter-row-wrap.md` | **筛选项折行与高度自适应**：筛选卡/筛选行固定 height 裁切、el-radio-group 换行间距、gap 替代 margin 链；需求文案与自检 |
| 识别与修复 | `data/el-button-root-and-deep.md` | **el-button**：根 class 与 `::v-deep`；勿用 `type="text"` 冒充带框次要按钮；相邻 10px；子 img/span 去 margin；三态与 primary 字色 |
| 识别与修复 | `data/el-select-suffix-alignment.md` | **el-select 后缀箭头**：禁止根节点 flex+space-between；小高度须同步 icon line-height、suffix right、padding-right |
| 识别与修复 | `data/el-color-picker-extend.md` | **触发与下拉共同结构**、**图1 / 图2 对照清单**、选型/错配修复、**需求文案（评审可粘贴）**、`el-color-picker-extend` 与 `el-color-picker` 细则、字体颜色触发器、Props/事件、自检；与 6.3 / 6.3.4 / 6.3.11 交叉引用 |
| 交付与工程 | `data/router-sync.md` | **路由登记**：`Custom.vue` 交付后登记 `index`/`Custom` 路由；识别 404/未 import、与稿源关系、自检清单 |
| 关键要求 | `data/requirements.md` | 文件操作、执行原则、代码规范、数据与方法完整性 |
| 流程总结 | `data/workflow-summary.md` | 完整开发流程、检查点、快速参考流程图 |

---

## 执行完成后

1. **报告执行结果**：告知用户 `Custom.vue` 文件已生成，并说明主要改造内容
2. **列出修改清单**：说明完成了哪些改造（循环渲染、Element UI 替换等）
3. **路由**：说明是否已按 **`data/router-sync.md`** 检查/更新路由，并给出可访问的 path（如 `/shushi-custom`）；若用户环境路由文件路径不同，注明需自行同步
4. **打印模型信息**：在回复最后打印本次执行所使用的 AI 模型名称与版本信息

---

## 快速参考：执行流程图

```
用户触发 Skill
    ↓
提取 folderName
    ↓
验证源文件存在（index.vue + index.vue 所引用的 CSS）
    ↓
读取源文件（仅上述文件，不读其他工程文件）
    ↓
分析页面结构（布局、重复结构、交互元素）
    ↓
生成 Custom.vue（Write 工具直接写入文件）
    ↓
验证代码质量（含 7.4 路由登记）
    ↓
登记/校验路由（步骤 8，见 data/router-sync.md）
    ↓
报告执行结果 + 可访问 path + 打印模型信息
```
