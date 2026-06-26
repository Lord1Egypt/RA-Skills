# 伪控件识别与修复（下拉框、多选框、单选框、带外框搜索框）

## 1. 适用场景

静态页（index.vue）常使用 **div + 文案 + 图标** 模拟表单控件，没有原生 `<select>`、`<input type="checkbox">`、`<input type="radio">` 或带外框的 `<input type="text">`。改造为 Custom.vue 时若只按「是否有原生标签」判断，会漏掉这些伪控件，导致下拉框、多选框、单选框未替换为 Element UI，或搜索框样式错乱。本文档给出**识别规则**与**修复方法**，并沉淀为通用规则与需求文案，供改造与自检使用。

## 2. 识别规则（通用）

### 2.1 下拉框（el-select）

| 维度 | 说明 |
|------|------|
| **DOM 特征** | 小容器内为「当前选中的一项文案」+ 右侧「下拉/箭头」图标；或「标签 + 可切换的若干项」 |
| **样式特征** | 在 index.css 中该区域多为：固定宽高（如 66×28px）、圆角、边框、与列表项风格一致 |
| **典型文案** | 「鼓点-1」「请选择」「选择 XX」等表示「当前选中值」的短文案 |
| **替换组件** | `el-select` + `el-option`，选项与同页已有列表/配置一致（如 drumList） |
| **数据** | data 中定义选中值，如 `selectedDrumPhonetic: 0`，选项 value 可为 index 或 id |

**识别步骤：**

1. 在 index.vue 中搜索：带「选」、带数字/名称的「当前项」、或带下拉箭头图标的 div 结构。
2. 在 index.css 中确认：该区域是否为小盒子（宽高、圆角、边框）。
3. 若同页有同类列表（如鼓点列表），且该小盒子展示的是「其中一项」，则识别为下拉框并替换为 el-select。
4. **替换时须同时定位并删除**：同页中若有**独立的下拉选项列表**（如浮层、侧边列表、鼓点-1～鼓点-11 等静态列表），须在替换为 el-select 时一并删除该列表 DOM，仅保留 el-select。

### 2.2 多选框（el-checkbox）

| 维度 | 说明 |
|------|------|
| **DOM 特征** | 左侧为「勾选图标容器」（含勾选图或方框图）+ 右侧说明文案；多行结构相同 |
| **样式特征** | 左侧图标区域约 16×16 或类似尺寸；右侧文案为说明性（如「全选所有模块」「当前配置应用于所有页面」） |
| **典型文案** | 「全选」「应用于所有」「勾选」等 |
| **替换组件** | `el-checkbox`，每项一个 v-model 绑定 |
| **数据** | data 中每项一个布尔，如 `checkedAllModules: false`、`applyToAllPages: false` |

**识别步骤：**

1. 在 index.vue 中搜索：带「全选」「应用」「勾选」等语义的文案，或带勾选图标（勾/方框）的 div。
2. 在 index.css 中确认：左侧是否为小方框/图标区域（如 16×16）。
3. 若为「勾/未勾 + 说明文字」且多行结构一致，则识别为多选框并替换为 el-checkbox。

### 2.2.1 纵向模块勾选列（易漏识别）

| 维度 | 说明 |
|------|------|
| **漏识别原因** | 与「2.2 多选框」常见形态不同：**左侧没有紧跟一段「全选」「应用于」类说明文案**；左侧仅为 **16×16（或接近）小方框/切图**，右侧是**模块名称**（如「美式音标」「释义」「例句」「词组」），或同一行 `justify-between` 分列；多行在 **纵向一列对齐**，看起来像「配置项列表」而非表单多选。 |
| **DOM 特征** | 多行结构为：`flex-row` + `justify-between` + **左侧** `image-wrapper`（或 div）内 **单张 png**（勾/空方框）+ **右侧** `span` 为模块标题；或 **左侧一列** 多个 `image-wrapper` **纵向堆叠**（如 `flex-col` + `justify-between`），与右侧 **多行文案**（如「例句」「译文」）**行对行对齐**。 |
| **样式特征** | index.css 中左侧容器多为 **固定宽高约 16×16**、无文案；`thumbnail` 约 13×13、`margin` 约 `2px 0 0 2px`；**不同行可能引用不同 png**（表示选中/未选中态），与「装饰性图标」区分的关键是：**每一行左侧方框与右侧模块名语义成对，且多行形成一列「开关」**。 |
| **与装饰图区别** | 若左侧图标与右侧文案在**业务上表示「是否展示该模块」**（勾选后右侧主内容区对应块显示），即属伪复选框；若仅为列表 bullet 或纯装饰且无勾选语义，则不必改为 el-checkbox。 |
| **替换组件** | 每行（或每个堆叠方框）一个 **`el-checkbox`**，`v-model` 绑定独立布尔；**无组件内文案**时隐藏 `.el-checkbox__label`，右侧模块标题保留为旁侧 `span`。 |
| **联动** | 须在**右侧主内容区**对对应模块根节点使用 **`v-show` / `v-if`** 与勾选布尔联动，避免「已改为 el-checkbox 但内容始终展示」的假动态。 |

**识别步骤（补充）：**

1. 在 index.vue 中搜索：同一区域内 **多行** `image-wrapper_*` + `img` + **模块类文案**（音标、释义、例句、词组、书写等）。
2. 在 index.css 中核对：左侧是否为 **约 16×16** 的方框占位、**无标题文字**。
3. 若多行左侧方框与右侧/邻列模块名**一一对应**，且设计稿为勾选态切换，则按 **2.2.1** 识别为纵向模块多选，不得仅保留静态 `img`。

### 2.2.2 横向工具条 / 分栏首行 / 尾行上的模块勾选（易漏识别）

| 维度 | 说明 |
|------|------|
| **漏识别原因** | 注意力集中在「左侧纵向一列」模块勾选时，易忽略**同一配置区顶部横向 `flex-row`** 里、**模块标题（如英式音标、鼓点音频）左侧**的 `image-wrapper` + **小方框 png**；或忽略底部 **「单词书写」** 等 **尾行** 的「左方框 + 标签 + 右侧预览文案」——这些与 2.2.1 **形态相同**（方框 + 语义标签），只是**排在横向行**而非纵列。 |
| **DOM 特征** | 在 `group_*` / `box_*` 等**横向排列**容器中：**标签 span 之前**为单独的 `image-wrapper` + `img`（常见与纵列勾选**同一张或同一类** `SketchPng…` 资源）；右侧可能紧跟 **IPA 区、el-select、播放图标** 等。尾行常见：`image-text_*` 内左 `image-wrapper` + 右「单词书写：」+ 行末手写体预览词。 |
| **样式特征** | index.css 中该 `image-wrapper` 多为 **16×16（或接近）**、无内联标题；与 `.image-wrapper_22`（纵列美式音标左侧）等**尺寸同级**。若纵列已改为 `el-checkbox` 而横条仍保留 `img`，会出现**同一屏「实心填充勾」与「描边切图」混排**，尺寸与风格不一致（用户可见的「有的识别了有的没有」）。 |
| **替换组件** | 与 2.2.1 相同：每个语义独立的方框一个 **`el-checkbox`**，`v-model` 独立布尔；**无组件内文案**时隐藏 `.el-checkbox__label`。 |
| **联动** | **英式音标行**：勾选应对 **IPA + 喇叭区**（原 `group_12` 一类容器）做 `v-show`。**鼓点音频行**：若方框表示「是否启用鼓点模块」，应对 **el-select 及同组操作图标** 做 `v-show`（或 `v-if`，按是否需卸载组件权衡）。**单词书写行**：对右侧预览词（如 `text_42`）做 `v-show`。 |
| **全选联动** | 「全选所有模块」的 `handleSelectAll` / 批量布尔须**包含**上述横向行、尾行上的布尔，与纵列模块**同一套 keys**，避免出现「全选已勾选但英式/书写行仍为未勾选态」的逻辑错误。 |

**识别步骤（补充）：**

1. 在 index.vue 中除搜索「纵列 `block_*` + `image-wrapper`」外，**额外**扫描配置区 **所有** `flex-row`：是否存在 **「小方框图 + 模块名 span + 业务内容」** 且方框**无长说明文案**。
2. 对比 **img 的 src** 是否与纵列勾选使用**相同或同类**资源；若是，则与纵列**同等对待**，必须改为 `el-checkbox`，不得单独留图。
3. 为每个新增布尔补 **data**、**v-show**、**全选** 逻辑。

### 2.2.3 多选框尺寸分层：槽位（wrapper）与方框视觉（thumbnail）

| 维度 | 说明 |
|------|------|
| **为何容易做错** | 静态稿中勾选多为 **`image-wrapper`（如 16×16）+ `img.thumbnail`（如 13×13，`margin: 2px 0 0 2px`）**。若改造时只扫到 wrapper 或将「16×16」当作 inner 边长，会把 **`el-checkbox__inner` 画得比稿面方框大一圈**，与切图或设计稿不一致。 |
| **槽位** | index.css 中 **`.image-wrapper_*`** 或父级 **`.group_*` / `.box_*`** 的 `width`/`height`，用于与同行文案、图标 **对齐的占位区域**（常见 **16×16**）。对应 **`el-checkbox` 根** 与 **`::v-deep .el-checkbox__input`**：同尺寸，`display: inline-flex; align-items: center; justify-content: center`，使 inner 在槽内居中。 |
| **方框视觉** | **优先**取同结构下 **`.thumbnail_*` 的 `width`/`height`**（即切图在稿面上的绘制尺寸）。若无 `img` 而由 **单层 `image-wrapper` 的 background** 承担方框，则取 **该层** 的 width/height。对应 **`::v-deep .el-checkbox__inner`** 的 width/height，`box-sizing: border-box`。 |
| **勾形** | `::after` 的 `height`/`width`/`left`/`top`/`border-width` 须随 **inner 边长** 成比例调整；`is-checked` 时 `::after` 的 `border-color`（多为白）须单独覆盖。 |

**识别步骤：**

1. 在 index.vue 勾选左侧找 **`image-wrapper_*` + `img[class*="thumbnail"]`** 或等价结构。
2. 在 index.css **同时**打开上述 **wrapper** 与 **thumbnail** 选择器，记录两组 width/height。
3. 若 thumbnail 尺寸小于 wrapper，**inner = thumbnail**；**根/`__input` = wrapper**（或业务上与稿对齐的父级槽位尺寸）。

### 2.3 带外框的搜索框（el-input）

| 维度 | 说明 |
|------|------|
| **DOM 特征** | 外层为白底/圆角/边框容器，内为「搜索图标 + 占位文字（如搜索你想要的单词）+ 右侧搜索按钮/图标」 |
| **样式特征** | 容器固定高度（如 48px）、宽度（如 688px）、圆角（如 12px）、边框；内部为单行输入语义 |
| **替换组件** | `el-input`，使用 prefix/suffix 插槽放图标与按钮 |
| **样式要求** | 必须同时满足 SKILL.md 中「6.3.1 带外框搜索框样式规范」 |

**识别步骤：**

1. 在 index.vue 中搜索：「搜索」、placeholder 类文案、搜索图标 + 文字 + 按钮 的 div 结构。
2. 在 index.css 中确认：是否有「外层容器 + 内层输入区」的样式（高度、圆角、边框）。
3. 若为「带外框的搜索」语义，则替换为 el-input，并严格按 6.3.1 做样式覆盖。

### 2.4 分页（el-pagination）

| 维度 | 说明 |
|------|------|
| **DOM 特征** | 底部或列表下方有「共 xxx 条」、静态页码（1/2/3…）、上一页/下一页图标、以及「xx条/页」等下拉或文案，整体为一组分页条 |
| **样式特征** | 在 index.css 中该区域多为固定高度条（如 60px）、横向排列、有总数、页码块、箭头、条数选择区 |
| **替换组件** | `el-pagination`，使用 `layout="total, prev, pager, next, sizes"` 等，绑定 current-page、page-size、total，实现 current-change、size-change |
| **必须删除的 DOM** | **替换时必须删除整块原始分页静态内容**：包括「共 xxx 条」文案与图标、所有静态页码 div（如 text-wrapper_19/20 等）、上一页/下一页的静态图标或按钮、以及「30条/页」等静态或伪下拉。只保留一个 `el-pagination` 组件，由组件自带展示 total、prev、pager、next、sizes，不得保留两套（静态 + 组件） |

**识别步骤：**

1. 在 index.vue 中搜索：带「共」「条」「页」、数字页码、上一页/下一页图标、每页条数等语义的整块 DOM。
2. 在 index.css 中确认：该块是否为底部分页条（固定高度、横向 flex、含总数与页码）。
3. 若为一组分页功能，则整块替换为单个 `el-pagination`，并**删除该区域内全部静态子节点**。

### 2.5 单选框（el-radio）

| 维度 | 说明 |
|------|------|
| **DOM 特征** | 多个选项中仅能选一项（互斥）；每项为「圆点/圆圈 + 文案」或 div 模拟的选项块；存在「选中」与「未选中」两种视觉状态（如高亮/边框/背景不同） |
| **样式特征** | 在 index.css 中该区域多为圆点或圆形容器（如 14×14、16×16）、与文案横向或纵向排列；选中态常有不同背景色或边框色 |
| **替换组件** | `el-radio-group` + `el-radio`，v-model 绑定一个选中值（字符串或数字），每项 `el-radio` 的 `:label` 为选项值 |
| **样式与主题色** | 替换后须用 `::v-deep` 使尺寸、圆角、边框、字号与源页一致；**选中项与悬停态**须使用页面主题色（非 Element 默认蓝），见下方 3.5 |

**识别步骤：**

1. 在 index.vue 中搜索：多选一互斥的选项组（如「选项 A / 选项 B / 选项 C」仅能选一）、圆点/圆圈 + 文案、或带选中态的 div 组。
2. 在 index.css 中确认：是否有选中态与未选中态样式区分（如 border-color、background）。
3. 若为互斥单选项组，则替换为 `el-radio-group` + `el-radio`，并删除原单选区域全部 DOM。

## 3. 修复方法（通用）

### 3.1 下拉框修复

- **替换**：删除原「当前文案 + 箭头」的 div 结构，改为 `<el-select v-model="selectedXxx" class="xxx_select">` + `<el-option v-for="..." :label="..." :value="..." />`。
- **必须删除的 DOM**：若源页面除「当前选中项 + 箭头」外还有**独立的下拉选项列表**（如浮层、侧边列表、鼓点-1～鼓点-11 等静态列表），须**一并删除**。el-select 自带的 dropdown 负责展示选项，不得保留原静态选项列表 DOM；否则会出现「识别了下拉框但页面上仍有两套选项」的问题。
- **data**：新增 `selectedXxx`（数字或字符串，与 option 的 value 一致）。
- **样式**：用 `::v-deep .el-input__inner` 设置高度、line-height、border-radius、font-size、border-color，与设计稿一致。**focus/hover 边框色**须为页面主题色（从 index.css 取主色），如 `::v-deep .el-input__inner:focus { border-color: 主题色; }`。
- **激活态主题色**：下拉弹层挂载在 body，须给 el-select 设置 `popper-class="[folderName]_xxx_dropdown_popper"`，在 Custom.vue 中增加**非 scoped** 的 `<style>` 块，用该 class 覆盖 `.popper-class名.el-select-dropdown .el-select-dropdown__item.selected` 与 `.el-select-dropdown__item:hover` 的文字色、背景色为页面主题色/主题浅色，不得使用 Element 默认蓝色。

### 3.2 多选框修复

- **替换**：删除原「勾选图标容器 + 文案」的 div 结构，改为 `<el-checkbox v-model="checkedXxx" class="xxx_checkbox">文案</el-checkbox>`。
- **data**：新增 `checkedXxx: false`（或 true，按设计默认值）。
- **样式**：用 `::v-deep .el-checkbox__label` 设颜色、字号；`::v-deep .el-checkbox__inner` 设宽高、圆角。
- **激活态主题色**：选中/半选时不得使用 Element 默认蓝。须用 `::v-deep .el-checkbox__input.is-checked .el-checkbox__inner`、`::v-deep .el-checkbox__input.is-indeterminate .el-checkbox__inner` 设置 `background-color`、`border-color` 为页面主题色；`::v-deep .el-checkbox__inner:hover` 设置 `border-color` 为主题色。

### 3.2.1 纵向模块勾选列修复

- **删除**：原 **每一行**（或堆叠位）的 `image-wrapper` + `img`（勾/空方框切图），不得保留静态 png 冒充勾选态。
- **替换**：在**原 wrapper 尺寸**位置放入 `<el-checkbox v-model="moduleFlags.xxx" class="[folderName]_module_checkbox" />`；**无内置标签文案**时须 `::v-deep .el-checkbox__label { display: none; width: 0; padding: 0; margin: 0; overflow: hidden; }`，避免挤出布局。
- **data**：使用**对象分组**（如 `moduleFlags: { showUsIpa: true, showMeaning: false, ... }`）或独立布尔，**每个方框一个布尔**，默认值与源稿首屏勾/未勾一致（可对齐不同 png 资源路径或设计说明）。
- **联动**：右侧内容区每个模块根节点增加 `v-show="moduleFlags.xxx"`（或 `v-if` 需收缩高度时）；**例句与译文**若共用一个卡片但左侧为**两个**方框，须**分别**绑定两个布尔，并对卡片内**英文例句块、分隔线、译文块**分别 `v-show`，分隔线仅在两者同时展示时出现。
- **样式**：`::v-deep .el-checkbox__inner` 的宽高须与 index.css 中 **方框视觉层**一致（常为 **`.thumbnail_*` 的 13×13**，而非外层 16×16 wrapper），`border-radius` 与稿一致；未选中边框色多为浅灰；选中为主题色边框 + 勾。槽位与 inner 分层见 **§2.2.3、§3.2.3**。
- **对齐**：父级保留原 `image-wrapper` 的 class 与 flex，内部仅换为 `el-checkbox`；**根/`__input` 对齐槽位（常见 16px）**，**inner 对齐 thumbnail（常见 13px）**，用 flex 在槽内居中 inner。

**需求文案（摘要）**

- 凡预览区/配置区出现**纵向一列**小方框切图，且与**模块名称行**对齐、语义为「是否展示该模块」者，须识别为 **el-checkbox**，禁止保留静态勾图。
- 每个方框须有 **data 布尔**；右侧对应模块须有 **v-show/v-if 联动**。
- 样式须还原 **16×16 级圆角方框**、**未选中灰框 / 选中主题色线框与白底勾**，**悬停与 focus 边框**建议与主题色一致；隐藏 label 不留空白占位。

### 3.2.2 多选框尺寸与全页视觉统一（必做）

**问题现象**：同一配置区内，部分行已改为 `el-checkbox`，部分行仍为 **`image-wrapper` + 切图**，或不同行的 `el-checkbox` 使用了**不同自定义 class** 导致 `::v-deep` 未覆盖全；表现为**勾框大小不一致**、**未选中态一为描边图一为 Element 默认**、**选中态一为实心主题色一为浅色描边**。

**修复方法：**

1. **单一组件类名**：为本页所有「无内联文案的模块勾选」使用**同一**自定义 class（如 `[folderName]_module_checkbox`），禁止纵列用 A 类、横条用 B 类而样式只写了一套。
2. **像素分层（与 §3.2.3 一致）**：**槽位**（多为 `image-wrapper` 16×16）与 **方框视觉**（多为 `thumbnail` 13×13）须分别从 index.css 读取；**根/`__input` 对齐槽位**，**`__inner` 对齐方框视觉**，二者常不相等，**禁止**把槽位尺寸误写到 `__inner` 上。
3. **根与 `__input`**：`display: inline-flex; align-items: center; justify-content: center; margin: 0; line-height: 1`；宽高取 **W_slot × H_slot**（见 §3.2.3）。
4. **inner 盒模型**：`::v-deep .el-checkbox__inner` 的 `width` / `height` 取 **W_box × H_box**（通常来自 **thumbnail**），须 `box-sizing: border-box`；**未选中**边框色对齐稿面。
5. **勾形（::after）**：在 **inner 边长 W_box、H_box** 确定后覆盖 `::v-deep .el-checkbox__inner::after` 的几何量；**选中态**须覆盖 `is-checked .el-checkbox__inner::after` 的 `border-color`（多为白）。
6. **状态齐全**：`is-checked`、`is-indeterminate`、`hover`、`is-focus` 的边框/背景须写全，与 **6.3.8** 主题色一致。

**需求文案（摘要）**

- 同一预览/配置区内，**凡模块开关式勾选**，须**全部**为 `el-checkbox`，**禁止**与静态方框 png 混用。
- **全页共用一套** `[folderName]_module_checkbox`（或等价）样式：**根节点 + `__input` + `__inner` + `__inner::after` + 选中/悬停/focus** 统一；**尺寸以 index.css 分层读取为唯一依据**（槽位 + 方框视觉），保证纵列、横条、尾行**像素级一致**。

### 3.2.3 按 index.css 校准 el-checkbox 像素（wrapper + thumbnail）

**适用**：凡从 **`image-wrapper` + `thumbnail` img** 替换而来的模块勾选（含纵列、横条、尾行、全选行）。

**操作步骤：**

1. **抄数**：在 index.css 记录 **`.image-wrapper_*`**（及参与布局的 margin）的 `width`/`height` 为 **槽位 W_slot × H_slot**；记录 **`.thumbnail_*`** 的 `width`/`height` 为 **W_box × H_box**。若无 thumbnail，则方框视觉层为单层 wrapper 时，**W_box、H_box** 取该层尺寸。
2. **根节点**：`.[folderName]_module_checkbox.el-checkbox` 设 `width: W_slot; height: H_slot; display: inline-flex; align-items: center; justify-content: center; margin: 0; line-height: 1`（若稿面根节点无固定宽高，则至少保证 `__input` 为槽位尺寸）。
3. **`__input`**：`::v-deep .el-checkbox__input` 设 `width: W_slot; height: H_slot; display: inline-flex; align-items: center; justify-content: center; line-height: 1`。
4. **`__inner`**：`::v-deep .el-checkbox__inner` 设 `width: W_box; height: H_box; box-sizing: border-box; border: …; border-radius: …`（与稿一致）。
5. **`::after`**：按 **W_box、H_box** 调整 `height`、`width`、`left`、`top`、`border-width`，使勾在方框内比例合理；**`is-checked .el-checkbox__inner::after`** 设 `border-color`（多为 `#fff` 或 `rgba(255,255,255,1)`）。
6. **父级 cell**：若使用 `.checkbox_cell` 等，其宽高宜与 **槽位**一致（常见 16×16），与 index 中 `group_*`/`image-wrapper` 对齐。

**需求文案（摘要）**

- **`el-checkbox__inner` 不得默认写 16×16**：须先读 **thumbnail（或内层）** 再写 inner。
- **槽位与 inner 不同尺寸时**，必须用 **flex 居中** 将 inner 置于槽内，避免勾框贴顶贴左偏移。

**自检**：在浏览器中与静态 index.vue 同区域叠图或量像素，**inner 外沿与稿面方框外沿误差 ≤1px**。

### 3.3 带外框搜索框修复

- **结构**：外层容器保持固定高度、宽度、圆角、**边框**（须有 `border` 以便 hover/focus 时改色），`display: flex; align-items: center; box-sizing: border-box; overflow: hidden`；内层为 `el-input`，使用 prefix/append 插槽。**容器在 hover 与 focus-within 时边框须为主题色**（见 9.8）。
- **样式（必做）**：
  - **`.el-input-group`**：必须做样式覆盖，避免双重外框。设置 `display: flex; flex: 1; height: 100%; min-width: 0; border: none; background: transparent`。
  - **`.el-input`**：在容器内 `height: 100%; flex: 1; min-width: 0`。
  - **`.el-input__inner`**：去掉边框（`border: none`）、背景透明、**高度略小于容器约 2px**（如容器 48px 则 46px）、`line-height` 与高度一致、`border-radius` 仅左侧与容器一致（若右侧为 append 按钮则设为 `12px 0 0 12px`）、`box-sizing: border-box`、**`padding-left`** 为前缀图标留足空间（如 44px），避免与图标重叠。
  - **`.el-input__inner::placeholder`**：占位符颜色与设计一致（如 `rgba(153, 153, 153, 1)`）。
  - **`.el-input__prefix`**：`display: flex; align-items: center; height: 100%`；`left` 与设计一致（如 16px）；自定义 prefix 根节点用 `display: inline-flex; align-items: center`，避免错位。
- **命名**：类名使用 `[folderName]_search_wrapper`、`[folderName]_search_input` 等。
- **placeholder 垂直居中与页面溢出**：须保证 placeholder 与输入文字在容器内垂直居中，且搜索框/底栏不溢出页面。详见 `search-input-and-page-overflow.md`（识别、修复与需求文案）。

### 3.4 分页修复

- **替换**：删除整块原始分页 DOM（「共 xxx 条」、静态页码、上一页/下一页、条数/页的静态或伪下拉），改为单个 `<el-pagination layout="total, prev, pager, next, sizes" :current-page="..." :page-size="..." :total="..." @current-change="..." @size-change="..." class="[folderName]_pagination" />`。
- **禁止**：不得在 el-pagination 外再保留一份「共 xxx 条」、静态页码、静态上下页或静态条数下拉，否则会出现两套分页内容。
- **data**：定义 `currentPage`、`pageSize`、`total`（或 totalCount），与接口或列表数据一致。
- **样式（必做）**：
  - **总数**：`::v-deep .[folderName]_pagination .el-pagination__total` 设置字体、颜色、行高与设计一致。
  - **上一页/下一页**：`.btn-prev`、`.btn-next` 尺寸、边框、圆角与设计一致；**:hover 态**边框色、**按钮与内部图标的颜色**须为页面主题色（须同时设置 `color` 与 `.el-icon` 的 `color`，见下方 9.5）。
  - **页码**：`.el-pager li` 尺寸、边框与设计一致；**当前页 `.el-pager li.active` 背景色、边框色须为页面主题色**；li:hover 边框/文字色为主题色。
  - **每页条数 sizes**：`.el-pagination__sizes .el-input__inner` 高度、圆角、边框、字号与设计一致；**触发器（el-input）的 focus 与 hover 态边框色须为主题色**（须同时覆盖 `:hover`、`:focus` 及 `.el-input.is-focus .el-input__inner`，见下方 9.7）。sizes 的下拉层挂载在 body，无法单独设置 popper-class，须在 Custom.vue 中增加**非 scoped** 的 `<style>`，对下拉选项的**选中态与悬停态**设置主题色（见下方「分页 sizes 下拉选中/悬停主题色」）。
  - **分页 sizes 下拉选中/悬停主题色**：Element UI 下拉项使用 class `.selected`（选中）、`.hover`（键盘焦点）及伪类 `:hover`。若仅写 `.el-select-dropdown__item.selected` 与 `:hover` 仍被默认样式覆盖，须采用**更高特异性选择器**并**同时覆盖所有状态**：使用 `body .el-select-dropdown li.el-select-dropdown__item` 前缀，覆盖 `.selected`、`.hover`、`:hover` 以及 `.selected:hover`、`.selected.hover`，对 `color` 与 `background-color` 使用 `!important`，使选中项与悬停项均为页面主题色，不得仍为 Element 默认蓝。详见下方 9.4。

### 3.5 单选框修复

- **替换**：删除原单选区域全部 DOM（圆点/圆圈 + 文案或 div 模拟的选项组），改为 `<el-radio-group v-model="radioValue" class="[folderName]_radio_group">` + `<el-radio v-for="..." :label="item.value" :key="item.value">...</el-radio>`；在 data 中定义 `radioValue`（与选项 value 类型一致），在 methods 中实现 `@change`（如 `handleRadioChange`）。
- **样式与源页一致**：用 `::v-deep` 对 `.el-radio__inner`（圆点）、`.el-radio__label` 设置与 index.css/设计稿一致的尺寸、圆角、边框、字号、颜色；布局（横向/纵向、间距）与源页面一致。
- **激活态与选中项主题色**：Element 默认选中为蓝色，须改为**页面主题色**。在 radio 父级 class 下用 `::v-deep` 设置：
  - **选中态**：`父级 ::v-deep .el-radio__input.is-checked .el-radio__inner` 的 `border-color`、`background-color` 为页面主题色；`父级 ::v-deep .el-radio__input.is-checked + .el-radio__label` 的文字色可设为主题色或与设计一致。
  - **悬停态**：`父级 ::v-deep .el-radio__inner:hover` 的 `border-color` 设为主题色。
- **主题色来源**：与 el-select、el-checkbox 一致，从 index.css 或设计稿取主色。
- **筛选项折行**：若筛选为横向多选项（如课程/年级/学期）且需支持换行，须避免筛选卡或各行仍用**固定 `height`** 导致裁切及与下行重叠；须配合 **`min-height`、`gap`、`el-radio-group` 的 `flex:1` + `min-width:0` + `flex-wrap`** 等，详见 `filter-row-wrap.md` 与 SKILL **§6.3.10.1**。

## 4. 自检清单

改造或修复 Custom.vue 后，按以下项自检：

- [ ] **下拉框**：所有「当前选中一项 + 箭头」的伪下拉已替换为 el-select；**已删除源页面中独立的下拉选项列表 DOM**（浮层、侧边列表等），仅保留 el-select；data 中有对应选中值；选项与同页列表一致；样式与设计一致；**el-select 触发器（el-input）的 focus 与 hover 边框**已为主题色（见 9.7）。
- [ ] **多选框**：所有「勾选图标 + 说明文案」的伪多选已替换为 el-checkbox；data 中有对应布尔；标签与勾选框样式与设计一致；**选中/悬停态为主题色**（已用 ::v-deep 覆盖 is-checked、is-indeterminate、hover）。
- [ ] **纵向模块勾选列**：左侧约 16×16 方框列 + 模块名（无「全选」类长文案）已按 **2.2.1 / 3.2.1** 改为 el-checkbox；已删除方框 png；**moduleFlags（或等价）与右侧 v-show 联动**；无 label 时已隐藏 `.el-checkbox__label`。
- [ ] **横向工具条 / 尾行模块勾选**：配置区顶部横排（英式音标、鼓点音频等）及底部「单词书写」等行，左侧方框已按 **2.2.2** 改为 el-checkbox，**无静态勾图残留**；对应内容区（IPA、鼓点控件、书写预览等）已 **v-show** 联动；**全选所有模块** 已包含上述布尔（见 **2.2.2**）。
- [ ] **多选框尺寸统一**：全页模块勾选共用同一自定义 class 与同一套 `::v-deep`（含根节点、`__input`、`__inner`、`__inner::after`、选中勾线色），与 index.css 方框尺寸一致，无「有的行大、有的小、有的像切图有的像组件」混排（见 **3.2.2**）。
- [ ] **多选 inner 与槽位**：已从 index.css 区分 **wrapper 槽位** 与 **thumbnail 方框视觉**；`__inner` 为方框视觉尺寸，`__input`/根为槽位并居中 inner，已按 **§3.2.3** 校准 `::after`，非笼统 16×16 inner。
- [ ] **带外框搜索框**：容器高度/宽度/圆角与设计一致，**容器有 border**；**容器在 hover 与 focus-within 时边框为主题色**（见 9.8）；已对 .el-input-group 做无边框、透明背景、flex 占满的样式覆盖；无双重边框；el-input__inner 高度略小于容器、无边框、背景透明、padding-left 为前缀留足空间；placeholder 颜色正确；前缀图标与文字垂直对齐；无错位或溢出。
- [ ] **分页**：**已删除原始分页全部静态内容**（共 xxx 条、静态页码、上下页、条数/页伪下拉），仅保留一个 el-pagination；total、prev、pager、next、sizes 的样式与设计一致；**sizes 的 el-select 触发器** focus 与 hover 时边框已为主题色（见 9.7）；**上一页/下一页** 已设 padding:0、inline-flex、居中，默认态与 hover 态图标颜色正确（见 9.6），hover 时边框与 .el-icon 均为主题色（见 9.5）；**sizes 下拉**选中项与悬停项已通过非 scoped 样式设为主题色，若未生效已用双重 class 或 body 前缀及 !important（见 9.4）。
- [ ] **单选框**：互斥单选项组已替换为 el-radio-group + el-radio；尺寸、布局、文字与源页一致；**选中项与悬停态圆点/边框为主题色**，已用 ::v-deep 覆盖，非 Element 默认蓝。
- [ ] **筛选折行**：横向筛选在折行时筛选区高度随内容增高，无行间重叠（见 `filter-row-wrap.md`）。

## 5. 按钮与列表内文字垂直居中（识别与修复）

### 5.1 识别

改造后若出现以下情况，即需按 5.2 修复：

- **el-button**：按钮有固定高度，文字或「图标+文字」明显偏上/偏下或偏左/偏右；或**默认态与激活态（hover/active/focus/内容切换后）切换时内容发生错位**，未始终保持水平垂直居中。
- **按钮激活态/替换态**：按钮在状态切换后由其他 DOM（如 div）展示（如「导入」→「已导入」），该 DOM 内文字或图标未在容器内水平垂直居中。
- **列表/步骤 badge**：圆形或方形容器（如步骤 1、2、3 的圆圈或序号块）内数字/序号未在容器内垂直居中。
- **列表项**：整行有固定高度（如 48px），左侧 badge、中间文字、右侧图标未整体在行内垂直居中。

### 5.2 修复方法（通用）

- **el-button（默认与所有状态均居中）**：
  - 在按钮的自定义 class 上通过 `::v-deep` 为**默认态及 :hover、:active、:focus** 统一设置：`display: inline-flex; align-items: center; justify-content: center; line-height: 1;`，保证状态切换时内容始终水平垂直居中。
  - 按钮内文案（如 `span`）须：`text-align: center; margin: 0;`（或仅保留对称的左右 margin，如仅 `margin-left` 作与图标的间距），避免单侧 margin 导致水平偏位；建议同时设 `display: inline-flex; align-items: center;` 使多行或图标+文字整体居中。
- **按钮激活态/替换态**：若状态切换后由非 el-button 的容器（如 div）展示内容，该容器须使用 `display: flex; align-items: center; justify-content: center;`（或 `inline-flex`），内部文案与图标使用 `text-align: center; margin: 0;` 或 `display: inline-flex; align-items: center; justify-content: center;`，确保与默认态一致地水平垂直居中。
- **badge 内文字**：badge 容器增加 `display: flex; align-items: center; justify-content: center;`；内部文字或数字 **水平垂直都居中**：`text-align: center; margin: 0;`，不保留左右 margin。
- **列表项内文字与子元素**：列表行容器使用 `display: flex; align-items: center;`；行内所有子元素（badge、文字、图标）去掉垂直 margin（`margin-top`/`margin-bottom` 设为 0），只保留水平 margin，由 flex 负责垂直居中。

### 5.3 自检

- [ ] 所有 el-button 在**默认态与 hover/active/focus 态**下，内容（文字或图标+文字）均在按钮内**水平垂直居中**；状态切换后无错位。
- [ ] 若按钮存在「激活态/替换态」（如由 div 展示另一套内容），该态内容也在容器内**水平垂直居中**。
- [ ] 所有 badge（步骤序号、列表序号等）内数字/文字在 badge 内**水平垂直都居中**（text-align: center; margin: 0）。
- [ ] 所有列表项行内（badge + 文字 + 图标）整体垂直居中。
- [ ] 所有 el-select 触发器 focus/hover 边框色为页面主题色；下拉选项选中/悬停为主题色（popper-class + 非 scoped 样式）。
- [ ] 所有 el-checkbox 选中/半选时方框背景与边框为主题色，悬停时边框为主题色。
- [ ] **下拉框激活主题色**：所有下拉（含分页 sizes）的选中项与悬停项均为页面主题色，已用非 scoped 样式覆盖，必要时 !important（见 9.1）。
- [ ] **按钮文字水平垂直都居中**：所有按钮内文字（含 div+背景图+文字）均居中，文字节点无单侧 margin 导致偏位（见 9.2）。
- [ ] **搜索框不溢出**：带外框搜索框容器 max-width: 100%、min-width: 0，所在行 min-width: 0、overflow: hidden（见 9.3）。

---

## 6. 需求文案（可直接用于任务/规范）

以下可作为「静态改动态」任务或规范中的需求描述：

- **下拉框**：页面中所有「当前选中一项 + 下拉箭头」的展示区，须识别为下拉选择，并替换为 `el-select` + `el-option`，选项与页面已有数据一致，选中态与 data 双向绑定。**替换时必须删除源页面中独立的下拉选项列表 DOM**（如浮层、侧边列表等），仅保留 el-select。**样式与主题色**：触发器尺寸、边框、圆角与设计一致；focus/hover 边框色须为页面主题色；下拉选项选中/悬停须用 `popper-class` + 非 scoped 样式覆盖为主题色，不得使用 Element 默认蓝。
- **多选框**：页面中所有「勾选图标 + 说明文案」且可勾选/取消的项，须识别为多选框，并替换为 `el-checkbox`，每项在 data 中有对应布尔变量。**激活态主题色**：选中/半选时方框背景与边框须为页面主题色，悬停时边框为主题色，须用 ::v-deep 覆盖，不得使用 Element 默认蓝色。
- **带外框搜索框**：所有「白底/圆角/边框容器 + 搜索图标 + 占位文字 + 搜索按钮」的搜索区，须替换为 `el-input`，并满足带外框搜索框样式规范：容器定高定宽、**容器有 border**；对 `.el-input-group` 做无边框、透明背景、flex 占满的样式覆盖；内层 `.el-input__inner` 无重复边框、高度略小于容器、`padding-left` 为前缀图标留足空间；占位符与前缀图标样式与设计一致；**容器在 hover 与 focus-within 时边框须为主题色**（见 9.8）；无错位或溢出。
- **el-input focus 与 hover 边框主题色**：所有 **el-input** 在 focus 与 hover 时，**可见边框**须为页面主题色。带外框的搜索框：外层容器须设 `border`，并设 `.xxx_search_wrapper:hover`、`.xxx_search_wrapper:focus-within` 的 `border-color` 为主题色；独立 el-input：须覆盖 `.el-input__inner:hover`、`.el-input__inner:focus`、`.el-input.is-focus .el-input__inner` 的 `border-color`。自检：hover 与 focus 时边框均为主题色（见 9.8）。

- **el-button 默认与激活态内容水平垂直居中**：所有 el-button 须通过自定义 class 在**默认态及 :hover、:active、:focus** 统一设置 `display: inline-flex; align-items: center; justify-content: center; line-height: 1;`，使内容（文字或图标+文字）在按钮内**始终水平垂直居中**，状态切换时不得错位。按钮内文案须 `text-align: center; margin: 0;`（或仅对称 margin），避免单侧 margin 导致水平偏位。若状态切换后由其他 DOM（如 div）展示（如「导入」→「已导入」），该容器也须 `display: flex; align-items: center; justify-content: center;`，内容水平垂直居中与默认态一致。
- **按钮与列表内文字垂直居中**：列表/步骤中的 **badge 内文字须水平垂直都居中**：badge 容器 `display: flex; align-items: center; justify-content: center;`，内部文字 `text-align: center; margin: 0;`。列表项行须使用 `display: flex; align-items: center;`，行内子元素去掉垂直 margin，由 flex 实现垂直居中。
- **下拉框样式与激活态主题色**：el-select 触发器 focus/hover 边框色须为页面主题色（从 index.css/设计稿取）；下拉选项选中/悬停须用 `popper-class` + 非 scoped 样式覆盖为主题色，与当前页面主题一致，不得使用 Element 默认蓝色。
- **多选框激活态主题色**：el-checkbox 选中/半选时 `.el-checkbox__inner` 的 background-color、border-color 须为页面主题色，悬停时 border-color 须为主题色，用 ::v-deep 覆盖，不得使用 Element 默认蓝色。
- **分页（el-pagination）**：页面底部分页条须识别为分页，**整块替换为单个 el-pagination**，并**删除该区域内全部原始静态内容**（「共 xxx 条」、静态页码、上一页/下一页、条数/页的静态或伪下拉），不得保留两套。需定义 currentPage、pageSize、total 及 current-change、size-change。**样式与主题色**：total、prev、pager、next、sizes 的尺寸与设计一致；当前页（.el-pager li.active）、上一页/下一页与 sizes 触发器的 focus/hover 须使用页面主题色；**每页条数 sizes 的下拉**挂载在 body 且无法单独设 popper-class，须在页面内增加非 scoped 样式，对下拉选项的**选中态（.selected）、键盘焦点态（.hover）、悬停态（:hover）及选中+悬停**同时覆盖，使用 `body .el-select-dropdown li.el-select-dropdown__item` 等更高特异性选择器并对 color、background-color 使用 !important，使下拉选中项与悬停项与页面主题一致，不得仍为 Element 默认蓝（见 9.4）。
- **下拉框激活主题色（必生效）**：所有下拉（含页内 el-select、分页 sizes）的选中项与悬停项须为页面主题色。页内 el-select 用 popper-class + 非 scoped 覆盖；挂载在 body 的下拉用非 scoped 全局覆盖，若被覆盖则对 color/background-color 使用 !important。自检：点击下拉后选中项与悬停项均为主题色。
- **按钮文字水平垂直都居中**：所有按钮（含 div+背景图+文字）内文字须**水平与垂直都居中**。按钮容器 `display: inline-flex; align-items: center; justify-content: center;`；文字节点 `display: inline-flex; align-items: center; justify-content: center; width: 100%; margin: 0; text-align: center; line-height: 1;`，禁止单侧 margin 导致偏位。自检：按钮内文字在默认态与 hover/点击态均居中。
- **搜索框不溢出**：带外框搜索框容器须设 `max-width: 100%; min-width: 0;`（必要时 flex-shrink: 1）；所在行须设 `min-width: 0; overflow: hidden;`（必要时 max-width: 100%），确保窄屏或与 tabs 同排时不溢出父级。自检：缩小视口或增加左侧内容后，搜索框不撑出、不横向溢出。
- **单选框（el-radio）**：页面中所有「多选一」互斥选项组（含原生 `<input type="radio">` 或 div+文案/圆点模拟的单选）须识别为单选框，并替换为 `el-radio-group` + `el-radio`，v-model 绑定一个选中值，实现 @change。**样式与源页一致**：圆点尺寸、圆角、边框、字号、布局与 index.css/设计稿一致。**激活态与选中项主题色**：选中态 `.el-radio__input.is-checked .el-radio__inner` 的 border-color、background-color 须为页面主题色；悬停态 `.el-radio__inner:hover` 的 border-color 须为主题色；须用 ::v-deep 覆盖，不得使用 Element 默认蓝色。
- **分页 sizes 下拉选中/悬停主题色（必生效）**：分页「每页条数」sizes 的下拉挂载在 body，选中项与悬停项须为页面主题色。须在 Custom.vue 中增加非 scoped 样式，使用 `body .el-select-dropdown .el-select-dropdown__item` 等选择器，**同时覆盖** `.selected`、`.hover`、`:hover` 及 `.selected:hover`、`.selected.hover`，对 color、background-color 使用 !important；**若 hover 仍不生效**，须使用**双重 class** 提高特异性（如 `.el-select-dropdown .el-select-dropdown__item.el-select-dropdown__item:hover`）。自检：打开 sizes 下拉后选中项与悬停项均为主题色（见 9.4）。
- **分页上一页/下一页图标 hover 主题色**：分页「上一页」「下一页」按钮在 hover 时，除边框色为主题色外，**箭头图标**也须为主题色。须在分页父级 class 下用 ::v-deep 为 `.btn-prev:hover`、`.btn-next:hover` 设置 `color`，并为 `.btn-prev:hover .el-icon`、`.btn-next:hover .el-icon` 设置 `color` 为主题色，不得仅改边框而图标仍为默认色。自检：悬停上一页/下一页时边框与图标均为主题色（见 9.5）。
- **分页按钮样式（上一页/下一页）**：分页「上一页」「下一页」须**布局正确、图标居中**。须对 `.btn-prev`、`.btn-next` 设 `padding: 0`、`display: inline-flex`、`align-items: center`、`justify-content: center`，并设默认态 `color`；对 `.btn-prev .el-icon`、`.btn-next .el-icon` 设 `color: inherit`，避免图标偏位或默认色错误。自检：按钮内图标居中、默认态与 hover 态颜色与设计一致（见 9.6）。
- **el-select 触发器 focus 与 hover 边框主题色**：所有 el-select（含分页 sizes）内部的 **el-input 触发器**在 **focus** 与 **hover** 时边框须为页面主题色。须用 `::v-deep` 同时覆盖 `.el-input__inner:hover`、`.el-input__inner:focus` 及 `.el-input.is-focus .el-input__inner` 的 `border-color`，不得仅改其一或漏写 `.is-focus`。自检：触发器 hover 与 focus 时边框均为主题色（见 9.7）。

---

## 7. 列表项内容溢出（识别与修复）

凡用 **v-for** 渲染的列表/卡片，若项内存在**由数据驱动的文本**（标题、作者、描述等），且 index.css 中对应文本带有**固定 width/height**，改造后易发生**内容溢出**。识别与修复方法、需求文案及自检清单见 **`data/list-item-overflow.md`**。要点：列表项根节点设 `overflow: hidden`、`box-sizing: border-box`；动态文本用 **max-width** 替代固定 width、并设 `overflow-wrap: break-word`、`overflow: hidden`，不得保留会导致溢出的固定宽度。

---

## 8. 文字竖排与横排（识别与修复）

设计稿中列表/卡片内的**标题、作者**等常为**竖版排列**（竖排）；若未识别而按横排实现，版式会与设计不符。识别规则：在 index.css 中若该文本为**窄宽高瘦**（width 约 14px～24px、height 明显大于 width、line-height 与 width 接近），或设计语义为古诗词/传统竖版，则视为竖排。竖排须在 Custom.vue 中设 `writing-mode: vertical-rl`（或 vertical-lr）、`text-orientation: upright` 及 width、max-height、overflow。详见 **`data/text-direction-vertical-horizontal.md`**。

---

## 9. 下拉框激活主题色、按钮文字居中、搜索框溢出（常见漏改与修复）

### 9.1 下拉框激活样式未改成主题色

**识别**：页内存在 el-select（含分页的「每页条数」sizes 下拉）或其它下拉，但**选中项 / 悬停项**仍为 Element 默认蓝色，未使用页面主题色。

**修复**：
- **页内 el-select**：给 el-select 设置 `popper-class="[folderName]_xxx_dropdown_popper"`，在 Custom.vue 中增加**非 scoped** 的 `<style>`，用该 class 覆盖：
  - `.popper-class名.el-select-dropdown .el-select-dropdown__item.selected`、`.popper-class名.el-select-dropdown .el-select-dropdown__item:hover` 的 color、background-color 为页面主题色/主题浅色。
- **分页 sizes 等挂载在 body、无法单独设 popper-class 的下拉**：在 Custom.vue 中增加**非 scoped** 的 `<style>`，对 `.el-select-dropdown .el-select-dropdown__item.selected`、`.el-select-dropdown .el-select-dropdown__item:hover`（及 `.selected.hover`、`.selected:hover` 等组合）设置主题色；若被其它样式覆盖，可对 color、background-color 使用 **!important**，确保激活/悬停态为主题色。

### 9.2 按钮文字未水平垂直都居中

**识别**：按钮（含用 div+背景图+文字实现的「取消」「插入」等）内文字明显偏上/偏下/偏左/偏右，或仅垂直居中但水平未居中。

**修复**：
- **容器**：按钮根节点设 `display: inline-flex; align-items: center; justify-content: center;`，并设固定宽高（如 72px×32px）。
- **文字节点**：文字所在 span/div 设 `display: inline-flex; align-items: center; justify-content: center; width: 100%; margin: 0; text-align: center; line-height: 1;`，**不得**使用单侧 margin（如仅 `margin-left`）导致水平偏位。若为「背景图 + 文字」结构，背景图用 `position: absolute` 脱流，文字节点为唯一在流子元素并占满容器，由 flex 实现水平垂直都居中。

### 9.3 搜索框长度溢出

**识别**：带外框的搜索框（el-input 放在固定宽高的白底圆角容器内）在窄屏或与其它横向内容（如 tabs、筛选项）同排时，**搜索容器或输入区超出父级**，出现横向溢出或挤压。

**修复**：
- **搜索容器**：在保持设计稿宽度（如 400px）的前提下，增加 `max-width: 100%; min-width: 0;`，必要时 `flex-shrink: 1`，使在父级变窄时可收缩而不溢出。
- **父级行**：搜索框所在行（如 tabs + 搜索的 flex 行）设 `min-width: 0; overflow: hidden;`，必要时 `max-width: 100%`，避免子项把行撑开导致整行溢出。
- 保证容器内 el-input 仍通过 `flex: 1; min-width: 0` 占满剩余空间，且无双重边框、无内容溢出（见 6.3.1）。

### 9.4 分页 sizes 下拉选中/悬停未改为主题色

**识别**：el-pagination 的「每页条数」sizes 为内部 el-select，其下拉层挂载在 body。打开 sizes 下拉后，**选中项（当前每页条数）或悬停项**仍为 Element 默认蓝色（#409EFF 等），未使用页面主题色。

**原因**：非 scoped 样式中仅写了 `.el-select-dropdown__item.selected` 与 `:hover` 时，可能被 Element 默认样式或加载顺序覆盖。Element UI 下拉项还使用 class `.hover` 表示键盘焦点，需一并覆盖。

**修复**：
- 在 Custom.vue 中增加**非 scoped** 的 `<style>` 块。
- 使用**更高特异性**选择器，确保覆盖 Element 默认样式：
  - 以 `body .el-select-dropdown` 为前缀，直接覆盖 `.el-select-dropdown__item`（下拉根节点可能为 `.el-select-dropdown` 或位于 `.el-popper` 内）。
  - **若 hover 仍不生效**：使用**双重 class** 提高特异性，如 `.el-select-dropdown .el-select-dropdown__item.el-select-dropdown__item:hover`（重复类名使特异性高于 Element 单类选择器）。
- **同时覆盖**以下状态，对 `color` 与 `background-color` 均设为主题色（或主题浅色），并加 `!important`：
  - 选中项：`.el-select-dropdown__item.selected`
  - 键盘焦点项：`.el-select-dropdown__item.hover`
  - 悬停项：`.el-select-dropdown__item:hover`
  - 选中项被悬停：`.el-select-dropdown__item.selected:hover`、`.el-select-dropdown__item.selected.hover`
- 示例（主题色以页面实际为准）；若未生效可再增加一组带双重 class 的选择器：
  ```css
  body .el-select-dropdown .el-select-dropdown__item.selected,
  body .el-select-dropdown .el-select-dropdown__item.hover,
  body .el-select-dropdown .el-select-dropdown__item:hover,
  body .el-select-dropdown .el-select-dropdown__item.selected:hover,
  body .el-select-dropdown .el-select-dropdown__item.selected.hover,
  .el-select-dropdown .el-select-dropdown__item.el-select-dropdown__item.selected,
  .el-select-dropdown .el-select-dropdown__item.el-select-dropdown__item.hover,
  .el-select-dropdown .el-select-dropdown__item.el-select-dropdown__item:hover,
  .el-select-dropdown .el-select-dropdown__item.el-select-dropdown__item.selected:hover,
  .el-select-dropdown .el-select-dropdown__item.el-select-dropdown__item.selected.hover {
    color: <页面主题色> !important;
    background-color: <主题浅色或半透明> !important;
  }
  ```

**自检**：点击分页「每页条数」打开下拉，当前选中项与鼠标悬停项均显示为主题色（文字与背景），无 Element 默认蓝。

### 9.5 分页上一页/下一页图标 hover 未改为主题色

**识别**：el-pagination 的「上一页」「下一页」按钮在鼠标悬停时，**边框**已为主题色，但**箭头图标**仍为默认灰色或 Element 蓝，未变为页面主题色。

**原因**：仅对 `.btn-prev:hover`、`.btn-next:hover` 设置了 `border-color`，未设置 `color`。Element UI 的箭头为按钮内的 `.el-icon`，图标颜色继承自按钮的 `color`；若未显式设置 hover 时的 `color`，图标可能仍为默认色。

**修复**：
- 在分页父级 class（如 `[folderName]_pagination`）下用 `::v-deep` 同时设置：
  - **按钮 hover**：`.btn-prev:hover`、`.btn-next:hover` 的 `border-color` 与 `color` 均为页面主题色。
  - **图标 hover**：`.btn-prev:hover .el-icon`、`.btn-next:hover .el-icon` 的 `color` 为页面主题色（若按钮已设 `color` 且图标能继承，可省略；若未生效则必须显式写图标选择器）。
- 示例（主题色以页面实际为准）：
  ```css
  .xxx_pagination ::v-deep .btn-prev:hover,
  .xxx_pagination ::v-deep .btn-next:hover {
    border-color: <页面主题色>;
    color: <页面主题色>;
  }
  .xxx_pagination ::v-deep .btn-prev:hover .el-icon,
  .xxx_pagination ::v-deep .btn-next:hover .el-icon {
    color: <页面主题色>;
  }
  ```

**自检**：鼠标悬停「上一页」「下一页」时，边框与箭头图标均显示为主题色。

### 9.6 分页按钮样式问题（上一页/下一页布局与默认态）

**识别**：分页「上一页」「下一页」按钮出现以下任一情况：图标偏左/偏右或未垂直居中、按钮区域明显偏大或留白过多、默认态图标颜色与设计不一致。

**原因**：Element 默认对 `.btn-prev`、`.btn-next` 设置了 `padding-right: 12px` / `padding-left: 12px`，仅改边框和背景时未重置 `padding` 与布局，导致图标不居中；未显式设置默认 `color` 时图标可能使用全局默认色。

**修复**：
- 在分页父级 class 下用 `::v-deep` 对 `.btn-prev`、`.btn-next` 设置：
  - **布局**：`padding: 0`；`display: inline-flex`；`align-items: center`；`justify-content: center`，使内部图标在按钮内水平垂直居中。
  - **默认态**：`color` 与设计一致（如 `rgba(85, 85, 85, 1)`），保证未 hover 时图标颜色正确。
- 对内部图标统一继承按钮颜色：`.btn-prev .el-icon`、`.btn-next .el-icon` 设置 `color: inherit`，则默认态与 hover 态（按钮设 `color` 后）图标自动一致。
- 示例：
  ```css
  .xxx_pagination ::v-deep .btn-prev,
  .xxx_pagination ::v-deep .btn-next {
    padding: 0;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: <默认文字色>;
  }
  .xxx_pagination ::v-deep .btn-prev .el-icon,
  .xxx_pagination ::v-deep .btn-next .el-icon {
    color: inherit;
  }
  ```

**自检**：上一页/下一页按钮内图标居中、默认态与 hover 态颜色与设计一致，无多余留白或错位。

### 9.7 el-select 下 el-input 的 focus 与 hover 边框未改为主题色

**识别**：页面中 el-select 的**触发器**（内部的 el-input）在 **focus（点击展开下拉）** 或 **hover（鼠标悬停）** 时，边框仍为 Element 默认色（灰或蓝），未变为页面主题色。

**原因**：仅设置了触发器默认态边框或只写了 `:focus` 未写 `:hover`，或未覆盖 Element 在 focus 时给 `.el-input` 添加的 `.is-focus` 类对应的样式。

**修复**：
- 在 el-select 的父级 class（如分页用 `[folderName]_pagination`，页内其他 select 用各自父级 class）下用 `::v-deep` **同时**覆盖：
  - **hover**：`.el-select .el-input .el-input__inner:hover` 的 `border-color` 为页面主题色。
  - **focus**：`.el-select .el-input .el-input__inner:focus` 的 `border-color` 为页面主题色。
  - **focus 态（Element 用 .is-focus 标记）**：`.el-select .el-input.is-focus .el-input__inner` 的 `border-color` 为页面主题色。
- 分页 sizes 的 select 触发器示例：
  ```css
  .xxx_pagination ::v-deep .el-pagination__sizes .el-input .el-input__inner:hover,
  .xxx_pagination ::v-deep .el-pagination__sizes .el-input .el-input__inner:focus,
  .xxx_pagination ::v-deep .el-pagination__sizes .el-input.is-focus .el-input__inner {
    border-color: <页面主题色>;
  }
  ```
- 页内其他 el-select 示例：
  ```css
  .xxx_select_wrapper ::v-deep .el-input__inner:hover,
  .xxx_select_wrapper ::v-deep .el-input__inner:focus,
  .xxx_select_wrapper ::v-deep .el-input.is-focus .el-input__inner {
    border-color: <页面主题色>;
  }
  ```

**自检**：el-select 触发器在 hover 与 focus（展开下拉）时边框均为主题色，无默认蓝或灰。

### 9.8 el-input 在 focus 与 hover 时边框未改为主题色

**识别**：页面中的 **el-input**（含带外框的搜索框内的输入、独立输入框）在 **focus** 或 **hover** 时，**可见边框**仍为默认灰或 Element 蓝，未变为页面主题色。

**场景与原因**：
- **带外框的搜索框**：边框在外层容器上，内层 `.el-input__inner` 已设 `border: none`。若未对容器设置 **:hover** 与 **:focus-within** 的 `border-color`，则悬停或聚焦时容器边框不会变主题色。
- **独立 el-input**（自身有边框）：若未覆盖 `.el-input__inner:hover`、`.el-input__inner:focus` 及 `.el-input.is-focus .el-input__inner` 的 `border-color`，则 focus/hover 时仍为默认色。

**修复**：
- **带外框的搜索框**：外层容器须有 `border`（如 `1px solid rgba(226,226,226,1)`），并增加：
  ```css
  .xxx_search_wrapper:hover,
  .xxx_search_wrapper:focus-within {
    border-color: <页面主题色>;
  }
  ```
- **独立 el-input**（或需单独强调触发器边框的输入）：在父级 class 下用 `::v-deep` 覆盖：
  ```css
  .xxx_wrapper ::v-deep .el-input__inner:hover,
  .xxx_wrapper ::v-deep .el-input__inner:focus,
  .xxx_wrapper ::v-deep .el-input.is-focus .el-input__inner {
    border-color: <页面主题色>;
  }
  ```

**自检**：所有 el-input 在 hover 与 focus 时，可见边框（容器或输入框自身）均为主题色。
