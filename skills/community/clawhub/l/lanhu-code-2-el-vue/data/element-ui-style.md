# Element UI 替换规范、样式覆盖与任务4 强制要求

本文档合并「Element UI 组件替换」的通用规范、样式覆盖方法、各组件替换要求、**任务4 强制要求与修复流程**，执行任务 4 时须全文遵循。

---

## 一、替换总则

### 1.1 目标与原则

- **目标**：将页面中的原生 HTML 元素替换为 Element UI 组件，并保持与源文件**视觉效果一致**、**交互与数据完整**。
- **原则**：每替换一处组件，必须**同时完成** template、data、样式覆盖；禁止只改 template 不补 data/methods。

### 1.2 替换映射表（识别与选型）

执行前先根据源 HTML 识别替换点，按下表选择对应组件：

| 源 HTML 元素 | Element UI 组件 | 识别特征 | 优先级 |
|-------------|----------------|----------|--------|
| 可点击的「按钮」（生成、插入、确定、取消、上传、预览等） | `el-button` | 有明确主操作/次操作的点击区域 | 🔴 高 |
| `<input type="text">` | `el-input` | 单行输入 | 🔴 高 |
| `<input type="textarea">` / 多行文本 | `el-input type="textarea"` | 多行、字数限制 | 🔴 高 |
| `<select>` | `el-select` + `el-option` | 下拉选择 | 🔴 高 |
| 分页结构（页码、上下页、总条数） | `el-pagination` | 页码按钮组 | 🟠 中 |
| 固定定位弹窗 + 遮罩 | `el-dialog` | 弹窗、关闭按钮 | 🟠 中 |
| `<input type="checkbox">` | `el-checkbox` / `el-checkbox-group` | 多选 | 🟡 低 |
| 日期选择控件 | `el-date-picker` | 日期输入 | 🟡 低 |
| 下拉菜单（点击展开项） | `el-dropdown` + `el-dropdown-menu` | 命令菜单 | 🟡 低 |
| 进度条 | `el-progress` | 百分比展示 | 🟡 低 |
| 悬停提示 | `el-tooltip` | 提示文案 | 🟡 低 |

其他可选用组件：`el-slider`、`el-rate`、`el-tag`、`el-badge`、`el-alert` 等，按源页面实际使用情况选用。**不替换**：开关保留源页面原生 DOM，不使用 `el-switch`。单选用 `el-radio-group`/`el-radio` 替换，样式与源页一致，选中/悬停为主题色，见 `data/recognition-and-fix.md`。

### 1.3 通用执行步骤（每处替换均须执行）

1. **识别**：记录被替换处的 HTML 结构、类名与关键样式。
2. **替换**：用对应 Element UI 组件替换，配置好 props（如 `v-model`、`:current-page` 等）并绑定事件。
3. **删除**：删除已被替换的原 HTML 代码，避免重复 DOM。
4. **样式匹配**：在 `<style scoped>` 中用**深度选择器**（见第二节）覆盖组件内部样式，使与设计稿一致。
5. **数据与方法同步（必须）**：
   - 在 `data()` 中定义该组件所需的所有变量（如 `currentPage`、`dialogVisible`、`inputValue` 等）。
   - 在 `methods` 中实现所有已绑定事件的处理函数（如 `handleSizeChange`、`handleDialogClose`、`handleInputChange` 等）。
   - **可点击的按钮**（如「上传」「预览」「确定」「取消」「智能合成」等）必须在 template 上绑定 `@click="handleXxx"`，并在 methods 中实现 `handleXxx`。
6. **验证**：确认样式与源文件一致、交互正常、无报错。

### 1.4 必须遵守的约束

| 约束 | 说明 |
|------|------|
| **禁止只写 template 不写 methods** | 每个 `@click`、`@change`、`@size-change` 等事件都必须有对应方法实现。 |
| **禁止只写 methods 不写 data** | 方法中使用的变量（如 `this.currentPage`、`this.dialogVisible`）必须在 `data()` 中定义初始值。 |
| **方法命名** | 使用 `handle` + 功能/事件，如：`handleSizeChange`、`handleDialogClose`、`handleUploadImage`、`handlePreview`。 |
| **类名** | 组件外层容器使用 `[sourceName]_xxx` 形式（如 `custom_pagination_container`），便于样式作用域与深度覆盖。 |

---

## 二、样式覆盖方法

### 2.1 为什么必须用深度选择器

Element UI 组件内部 DOM 带自带类名（如 `.el-input__inner`），且通常由组件库的样式作用域控制。在单文件组件内使用 `<style scoped>` 时，普通选择器无法穿透到组件内部，因此**必须使用深度选择器**才能覆盖其内部样式。

### 2.2 深度选择器用法

**Vue 2.x 推荐：**

| 写法 | 兼容性 | 说明 |
|------|--------|------|
| `::v-deep` | Vue 2.7+ | 推荐，写法统一 |
| `/deep/` | Vue 2.x | 可用 |
| `>>>` | 仅原生 CSS | 在部分预处理器中可能无效，少用 |

**规范写法示例：** 在父容器类下用 `::v-deep` 选中组件内部类，避免污染全局。

```css
.[sourceName]_pagination_container ::v-deep .el-pagination__total { color: #333; }
.[sourceName]_search_input ::v-deep .el-input__inner { height: 40px; border-radius: 4px; }
```

### 2.3 覆盖技巧与注意

- **查找内部类名**：用浏览器开发者工具选中组件 DOM，在 Elements 面板查看实际 class，再用 `::v-deep` + 该类名书写。
- **优先级**：父类 + `::v-deep` + 组件内部类，已具备较高优先级；尽量避免滥用 `!important`。
- **作用范围**：同一选择器会命中当前组件内所有匹配节点，尽量用**父级容器类**限定范围（如 `.custom_pagination_container ::v-deep ...`）。
- **状态完整**：覆盖时考虑 `:hover`、`:focus`、`.active`、`disabled` 等状态，与源文件一致。
- **多选（el-checkbox）**：先判断原样式是否多选框 → 用 el-checkbox 替换并删除原多选框 DOM → 用深度选择器将 el-checkbox 样式覆盖为与原有样式一致。详见 **2.7、2.8 节**。
- **公式栏/表单项（el-input + el-button 同行）**：容器须 flex、align-items: center；删除原有样式；input 与 button 与源稿尺寸/位置一致。详见 **2.4.1 节**。

**选择器优先级（从低到高，见 create.md 2.4.4）：**

```css
/* 低：直接选择器 */
.el-input__inner { }

/* 中：通过父类选择 */
.custom_input ::v-deep .el-input__inner { }

/* 高：更具体的选择器 */
.custom_input ::v-deep .el-input__inner.el-input__inner--focus { }

/* 最高：!important（不推荐，除非必要） */
.custom_input ::v-deep .el-input__inner { height: 40px !important; }
```

**注意事项（create.md 2.4.4）：** 使用 `::v-deep` 后的样式会影响该选择器下所有匹配元素；尽量用具体的父级 class 限制作用范围；避免过度使用 `!important`；测试多种状态（hover、active、focus、disabled）。

### 2.4 搜索框（带外框的 el-input）专项规范

当页面中存在「带外框的搜索框」（如占位符「搜索资源标题、ID」且外层有白底、圆角、边框的容器）时，除通用 el-input 替换与样式覆盖外，须满足：

**适用场景：**
- `el-input` 外层有自定义容器（如 `[sourceName]_search_wrapper`）；
- 或使用 `el-input` 的 `prefix` 插槽放置图标。

**必须满足：**

1. **外层容器**  
   固定宽高（如 288×32px）、圆角、边框、背景色；`display: flex`、`align-items: center`、`box-sizing: border-box`，使内部 `el-input` 垂直居中且不撑高、不溢出。

2. **el-input 与 .el-input__inner**  
   - 通过 `::v-deep` 使 `.el-input` 在容器内 `height: 100%`。  
   - `.el-input__inner`：去掉边框或与容器视觉统一（如 `border: none`）、`background: transparent`、高度略小于容器约 2px（如容器 32px 则 inner 30px）、`line-height` 与高度一致、`border-radius` 与容器一致、`box-sizing: border-box`；若容器已负责边框，inner 不再重复，避免双边框。

3. **占位符**  
   使用 `::v-deep .el-input__inner::placeholder` 设置 placeholder 颜色（如 `rgba(136, 136, 136, 1)`），与设计稿一致。

4. **前缀图标**  
   `.el-input__prefix` 使用 `display: flex`、`align-items: center`、`height: 100%`，图标垂直居中；若为自定义 slot（如图片），插槽根节点使用 `display: inline-flex`、`align-items: center`、`justify-content: center`，尺寸与设计一致（如 13×13px）。

5. **命名与统一**  
   同一项目内带外框的搜索框统一采用上述实现，类名使用 `[sourceName]_search_wrapper`、`[sourceName]_search_input` 等。

**AI 执行时自检（与 create.md 2.4.5 一致）：** 修复或实现搜索框后须确认：容器高度与设计一致；输入框与容器无双重边框；前缀图标与文字垂直对齐；placeholder 颜色正确；在不同浏览器下无错位或溢出。

### 2.4.1 公式栏/表单项中 el-input 与 el-button 同行（通用）

当源稿存在「一行内：输入区（公式/关键词等）+ 右侧按钮（如生成、搜索、确定）」且已替换为 `el-input` + `el-button` 时，须满足以下规则，避免样式错位、高度撑开、原有样式残留。

**适用场景**：
- 源稿为「白底/带边框的容器」内「左侧文字/输入 + 右侧按钮」（如公式栏 386+148 + 生成）；
- 已用 `el-input` 替代左侧文字或输入，用 `el-button` 替代右侧按钮。

**必须满足**：

1. **删除原有样式**  
   删除 Custom.vue 中针对**已被替换掉的 DOM** 的样式规则（如原 `.xxx_formula_label`、`.xxx_btn_generate_wrap`、`.xxx_btn_generate_text` 等仅作用于已删除 span/div 的 class），避免无用样式残留。替换后只保留「容器 + el-input + el-button」对应样式。

2. **容器布局**  
   该行容器（如 `.[sourceName]_formula_row`）须显式设置：  
   `display: flex; flex-direction: row; align-items: center; box-sizing: border-box;`  
   以及源稿的宽高、margin、背景、边框、圆角，使内部 `el-input` 与 `el-button` 同行且垂直居中，不撑高、不溢出。

3. **el-input 与 .el-input__inner**  
   - 通过 `::v-deep` 使 `.el-input` 高度与源稿一致（如 `height: 28px`），不撑开容器。  
   - `.el-input__inner`：与源稿一致——通常 `border: none`、`background: transparent`、`height`/`line-height` 与容器内一行高度一致、`font-size`/`color` 与源稿一致、`padding` 适中；若源稿无边框，inner 不出现单独边框。  
   - `.el-input__inner::placeholder`：占位符颜色与设计稿一致（如 `rgba(136, 136, 136, 1)`）。

4. **el-button**  
   用深度选择器或直接类名限定在该行内：宽高、圆角、背景色、字体大小、颜色与源稿一致；`flex: 0 0 auto` 避免被压缩；hover/focus 态与源稿一致。**右侧按钮的 margin**：若容器为固定宽度（如 776px），**禁止**使用过大的固定 `margin-left`（如 627px）导致「输入区宽度 + 按钮 margin-left + 按钮宽度 + 按钮 margin-right」大于容器宽度、按钮溢出不可见；应使用 **`margin: 0 12px 0 auto`**（或 `margin-left: auto`）使按钮贴右且不溢出，视觉上仍为「左输入、右按钮」。

5. **防止挤压**  
   若该行仅两子元素（input + button），可为 input 与 button 均设 `flex: 0 0 auto`，避免在窄屏或 flex 布局下被压缩变形；宽度或由源稿 margin 控制，或设固定 width。

6. **防止按钮溢出（必须检查）**  
   - **识别**：容器有固定宽度时，若按钮使用从源稿复制的「大数值 margin-left」（如 627px），先核算：`输入左 margin + 输入宽度 + 按钮 margin-left + 按钮宽度 + 按钮右 margin` 是否 ≤ 容器宽度；若大于则按钮会溢出、不显示。  
   - **修复**：将按钮的 `margin-left` 改为 **`auto`**（如 `margin: 0 12px 0 auto`），在 flex 布局下按钮自动贴右，不溢出；右侧留白与源稿「按钮在右」一致。

**自检**：容器高度与源稿一致且未被撑高；输入框无多余边框、与容器视觉融合；**按钮在容器内可见、未溢出**；按钮尺寸与位置与源稿一致（右对齐）；无「原有样式未删除」的冗余规则；同行、垂直居中、无错位。

### 2.7 多选框替换逻辑（通用流程）

多选框（可勾选/可取消、布尔开关或多项勾选）的替换须按以下顺序执行，并保证替换后仅保留一套多选 UI、视觉与源稿一致。

**步骤一：判断原样式是否显示多选框**

- 查看源文件（index.vue / 设计稿）：该区域是否为「可勾选/可取消」的交互（如「隐藏过程」「进位信息」「显示小数」等开关，或从多个选项中勾选多项）。
- 若**是**多选框语义（布尔开关用单个 `el-checkbox`，多选列表用 `el-checkbox-group`），则适用对应组件替换。若为**多选一互斥**单选项组，须替换为 `el-radio-group` + `el-radio`，样式与源页一致、选中/悬停为主题色。若为开关（toggle），保留源页面原生 DOM，不替换为 el-switch。

**步骤二：用 el-checkbox 替换并删除原有多选框 DOM**

- 用 `el-checkbox` 或 `el-checkbox-group` + `el-checkbox` 替换该区域，在 `data()` 中定义绑定变量（如 `hideProcess`、`carryInfo` 或 `checkboxList`），在 `methods` 中实现 `@change` 处理（如 `handleCheckboxChange`）。
- **必须删除**原有表现多选/勾选的 DOM（如多个 `div` + `@click`、或 `input type="checkbox"`、或自定义样式的勾选块），避免页面上同时存在「原样式多选框」与「el-checkbox」两套可操作区域。替换完成后，该区域只保留一套 `el-checkbox` / `el-checkbox-group`。

**步骤三：将 el-checkbox 样式覆盖为与原有样式一致**

- 在 `<style scoped>` 中用**深度选择器**（见下方「识别与修复」）覆盖 `el-checkbox` 内部样式，使**当前 el-checkbox 的视觉效果与替换前的原有样式一模一样**（布局、尺寸、图标、未选中态、选中态、间距等）。
- 验收：与源稿或 index 页面对比，勾选块尺寸、图标有无与位置、选中/未选中视觉效果一致，且页面上无重复的多选 UI。

---

### 2.8 多选框（el-checkbox）识别与样式修复（通用）

**常见问题**：替换为 `el-checkbox` / `el-checkbox-group` 后，仅改文字颜色或简单隐藏方框，未按源稿还原**布局、尺寸、图标、选中态**，或未删除原多选框 DOM 导致两套多选并存，与设计不一致。

**识别（对照源文件/设计稿）**：

1. **是否多选框**：该区域是否为「可勾选/可取消」的布尔或多项勾选（见 2.7 步骤一）；文案常为「隐藏 xxx」「显示 xxx」「是否 xxx」等。
2. **布局与尺寸**：每个选项的宽度、高度、间距；整组与上下文的 margin；若为「图标 + 文字」结构，记录图标尺寸与对齐方式。
3. **图标/装饰**：若源稿中每个选项有**图标**（如小图标在文字左侧），须在 `el-checkbox` 的默认插槽或 label 内保留相同结构，并用 CSS 还原图标（background 或 img、尺寸、对齐）。
4. **选中态与未选中态**：未选中时的文字/图标颜色、选中时的文字/图标颜色与背景；若源稿有边框、背景等选中样式，须用 `::v-deep .el-checkbox__input.is-checked` 或 `.el-checkbox.is-checked` 等覆盖实现。

**修复方法（通用）**：

1. **删除原多选框 DOM**：确认该区域仅保留 `el-checkbox` / `el-checkbox-group`，已无原 div/input 等多选框结构。
2. 用**深度选择器**限定在多选容器（如 `.[sourceName]_checkbox_group`）内：按需隐藏或重写 `.el-checkbox__input`（如 `display: none` 或尺寸/边框与源稿一致）。
3. `::v-deep .el-checkbox__label`：设置与源稿一致的 `display`、宽高、`padding`、字体与颜色；若 label 内包含自定义图标，为图标单独设类并写背景/尺寸。
4. 选中态：`::v-deep .el-checkbox__input.is-checked + .el-checkbox__label` 及 `::v-deep .el-checkbox.is-checked` 等，设置与源稿一致的颜色、背景或边框。
5. 验证：与源稿或 index 页面对比，勾选块尺寸、图标有无与位置、选中/未选中视觉效果一致；且仅有一套多选 UI。

**禁止**：只改文字颜色或简单隐藏方框而忽略源稿中的图标、选项宽度或选中态细节；或保留原多选框 DOM 导致与 el-checkbox 双套并存。

---

#### 2.8.1 多选框「图标+文字」结构专项规范（⭐新增）

**⚠️ 问题背景：**
源稿中的多选框常表现为「图标 + 文字」组合（如勾选图标在左，文字在右），而非 Element UI 默认的「方框 + 文字」样式。替换时若简单使用 `el-checkbox` 的默认插槽写文字，会导致：
1. 默认方框与源稿图标并存，出现两套勾选 UI
2. 文字位置与源稿不一致

**❌ 错误示例：**
```vue
<!-- 源稿结构：div > img(图标) + span(文字) -->
<!-- 错误做法：保留原 DOM，再叠加 el-checkbox -->
<div class="custom_option_item">
  <img class="custom_option_icon" src="xxx.png" />
  <el-checkbox v-model="hideProcess">隐藏过程</el-checkbox>
</div>

<style>
/* 结果：图标 + el-checkbox 默认方框 + 文字，三套 UI 并存 */
</style>
```

**✅ 正确做法：**
```vue
<!-- 正确做法：删除原 DOM，el-checkbox 的 label 内放「图标+文字」 -->
<el-checkbox v-model="hideProcess" class="custom_checkbox">
  <img class="custom_checkbox_icon" src="xxx.png" />
  <span class="custom_checkbox_text">隐藏过程</span>
</el-checkbox>

<style scoped>
/* 隐藏默认方框，自定义 label 布局 */
.custom_checkbox ::v-deep .el-checkbox__input {
  display: none;
}

.custom_checkbox ::v-deep .el-checkbox__label {
  display: flex;
  align-items: center;
  padding: 0;
}

.custom_checkbox_icon {
  width: 16px;
  height: 16px;
}

.custom_checkbox_text {
  font-size: 14px;
  color: rgba(85, 85, 85, 1);
  margin-left: 8px;
}
</style>
```

**识别步骤：**
1. 检查源稿多选框是否为「图标 + 文字」结构（非默认方框样式）
2. 记录图标尺寸、图标与文字间距、文字样式
3. 确认是「自定义图标样式」而非「原生 checkbox」

**修复步骤：**
1. **删除原 DOM**：删除 `div` + `img` + `span` 的原结构
2. **el-checkbox 包裹内容**：将「图标 + 文字」放入 `el-checkbox` 的默认插槽
3. **隐藏默认方框**：`::v-deep .el-checkbox__input { display: none; }`
4. **设置 label 布局**：`::v-deep .el-checkbox__label` 设为 `display: flex; align-items: center;`
5. **还原图标文字样式**：按源稿设置图标尺寸、文字颜色、间距

**自检清单：**
- [ ] 原 DOM 已完全删除，无残留 div/img/span
- [ ] 默认方框已隐藏（`display: none`）
- [ ] 图标尺寸与源稿一致
- [ ] 文字颜色、字号与源稿一致
- [ ] 图标与文字间距与源稿一致
- [ ] 仅有一套多选 UI，无方框+图标并存

---

### 2.9 一次性生成成功要点（多选/按钮）

为保证**多选框、单选框、按钮**在替换时一次性生成成功、样式与源稿一致，且不残留原 DOM，须按以下规则执行。单选用 el-radio-group + el-radio 替换；开关不替换，保留源稿原生 DOM。

#### 2.9.1 识别阶段（任务1 必须输出）

| 步骤 | 内容 | 输出 |
|------|------|------|
| 识别多选 | 源稿中「可勾选/可取消」的布尔项（如 隐藏过程、进位信息、显示小数） | 列出每个选项的**原 DOM 结构**（如 `div.image-text_15` + `img` + `span`）、尺寸、图标、未选/选中态文字颜色 |
| 识别按钮 | 源稿中所有可点击按钮（生成、插入、确定、取消等） | 列出每个按钮的**原 DOM**（如 `div.text-wrapper_13` + `span`）、宽高、圆角、背景色、字体大小、margin |

**禁止**：分析报告只写「替换为 el-checkbox/el-button」而不记录原 DOM 与源稿样式；否则替换时易遗漏删除原 DOM 或漏写深度样式。

#### 2.9.2 替换阶段：先删后写、只保留一套 UI

| 组件 | 正确做法 | 禁止做法 |
|------|----------|----------|
| **多选框** | **先删除**整块原有多选 DOM（如 `div.image-text_15`、其中的 `img`、`span`），**再**写入一个 `<el-checkbox v-model="xxx">`；用 slot 或 label 内放「图标+文字」还原源稿布局；用 `::v-deep` 隐藏 `.el-checkbox__input` 并设置 `.el-checkbox__label` 的 display/宽高/颜色与源稿一致 | 保留原 `div` + `img` + `span`，再在旁边加 `el-checkbox`，导致页面上两套可点击区域 |
| **按钮** | **先删除**原按钮 DOM，**再**写入 `<el-button @click="handleXxx">`；选择器与 DOM 一致（**`.容器class.el-button`** 及 **`:hover`/`:focus`/`:active`**，禁止 **`.容器class ::v-deep .el-button`** 当 class 在根上）。**勿用 `type="text"`** 还原稿面「带底/描边」的次要按钮（`el-button--text` 强制透明底且三态易回退）。并排按钮须处理主题 **`.el-button + .el-button { margin-left:10px }`**。按钮内 **img/span** 须去源稿静态 **margin**，主按钮用 flex **`justify-content`** 控制图标与文案。详见 **`data/el-button-root-and-deep.md`**。 | 同上；或用 `type="text"` 导致 hover 露透明底；或忽略相邻 10px、子级 margin 导致错位 |

#### 2.9.3 样式覆盖清单（必须一次写完）

**多选框（el-checkbox）**  
- [ ] `::v-deep .el-checkbox__input`：隐藏（`display: none`）或按源稿重写方框样式  
- [ ] `::v-deep .el-checkbox__label`：与源稿一致的 `display`（如 flex）、宽高、`padding-left: 0`、字体大小、颜色；若为「图标+文字」，label 内图标与文字间距与源稿一致  
- [ ] `::v-deep .el-checkbox.is-checked .el-checkbox__label`：选中态文字/背景与源稿一致  
- [ ] 若有多项，每项之间的 margin（如第二项 `margin-top: 8px`）与源稿一致  

**按钮（el-button）**  
- [ ] **选择器与 DOM 一致**：自定义 class 在**按钮根节点**上时，用 **`.自定义class.el-button`**（及 `:hover`、`:focus`、`.el-button--primary` 等）写宽、高、圆角、背景、边框、字色、`min-width`/`padding`；**禁止**对该按钮使用 **`.自定义class ::v-deep .el-button`**（无效）。class 在**外层 div**上时，可用 **父级 + `::v-deep` .el-button**。详见 **`data/el-button-root-and-deep.md`**。  
- [ ] hover、focus、active 与源稿一致；`type="text"` / `type="primary"` 时须覆盖修饰类默认值。  
- [ ] 按钮内文案 `span` 清除源稿中为静态块写的错位 `margin-top`/固定 `height`，与 Skill **6.3.6** 居中一致。  
- [ ] 若在固定宽度容器内右侧按钮：使用 `margin: 0 12px 0 auto` 或 `margin-left: auto`，禁止过大固定 `margin-left` 导致溢出  

#### 2.9.4 验收（任务4 完成后必查）

- [ ] **无原 DOM 残留**：该区域仅保留 Element 组件，已无原 div/span/img 等表现同一交互的 DOM  
- [ ] **仅一套 UI**：页面上不会同时出现「原样式多选框 + el-checkbox」「原按钮 + el-button」  
- [ ] **样式与源稿一致**：用开发者工具对比，尺寸、颜色、图标位置、未选/选中态与 index 或设计稿一致  

---

## 三、按组件细分的规范与示例

### 3.1 分页 (el-pagination)

**识别**：页码按钮、上一页/下一页、总条数、每页条数选择。

**数据与事件**：
- `data()` 中必须定义：`currentPage`、`pageSize`、`total`。
- 必须实现：`handleSizeChange`（每页条数变化）、`handleCurrentChange`（当前页变化）；换页时可将 `currentPage` 置 1 并调列表加载逻辑。

**样式**：外层包一层容器（如 `[sourceName]_pagination_container`），用 `::v-deep` 覆盖 `.el-pagination`、`.el-pagination__total`、`.el-pager li`、`.btn-prev`/`.btn-next` 等，使尺寸、颜色、间距与源文件一致。

**验收**：组件配置正确、原分页 HTML 已删除、样式一致、分页与数据加载正常。

### 3.2 弹窗 (el-dialog)

**识别**：固定定位、遮罩、标题栏、关闭按钮、底部按钮（确定/取消等）。

**数据与事件**：
- `data()` 中必须定义：`dialogVisible`（或与 `:visible.sync` 对应的变量）。
- 必须实现：`handleDialogClose`、`handleDialogCancel`、`handleDialogConfirm`；若有「打开弹窗」按钮，需实现如 `handleOpenDialog` 并置 `dialogVisible = true`。

**验收**：打开/关闭/确定/取消行为正确，标题与内容区样式与源文件一致（可通过深度选择器覆盖 `.el-dialog` 相关类）。

### 3.3 输入框 (el-input)

**识别**：`<input>`、单行/多行、带字数限制的文本框。若为**带外框的搜索框**，须同时满足 **2.4 节**。

**数据与事件**：
- `data()` 中定义与 `v-model` 对应的变量（如 `inputValue`、`textValue`）。
- 按需实现 `handleInputChange`、`handleInputBlur`、`handleTextareaChange` 等。

**样式**：用 `::v-deep .el-input__inner` 覆盖高度、边框、圆角、padding、placeholder；多行时注意 `.el-textarea__inner`。

**验收**：输入与源文件视觉一致；带外框搜索框符合 2.4；双向绑定与事件正常。

### 3.4 其他常用组件（简要）

- **el-select**：`data` 中 `selectedValue`、`selectOptions`；`handleSelectChange`。样式除 **`.el-input__inner`** 外，须处理 **右侧箭头**：**禁止**在 **`el-select` 根节点**使用 **`display:flex` + `justify-content:space-between`** 复刻静态「左文右图」（会破坏内部 `el-input` 与 **`.el-input__suffix`**）；根节点宜用 **`inline-block` + `vertical-align:middle`**（或外层 `div` 承担 flex）。小高度触发器须 **`::v-deep` 同步** **`.el-input__suffix` 的 `right`**、**`.el-input__icon` / `.el-select__caret` 的 `line-height`/`height`** 与 inner 一致，并校验 **`padding-right`**。详见 **`data/el-select-suffix-alignment.md`**、Skill **6.3.7.1**。
- **el-dropdown**：`@command` 绑定 `handleDropdownCommand(command)`，按 command 分支处理。
- **el-progress**：`data` 中 `progressPercentage`；按需提供 `updateProgress` 等方法。
- **el-date-picker**：`data` 中 `selectedDate`；`handleDateChange`。
- **el-tooltip**：多数仅需 `content`/`placement`，动态文案可用 `:content="tooltipContent"`。
- **el-checkbox-group**：`data` 中 `checkboxList`（数组）；`handleCheckboxChange`。

以上组件替换时均须：**template 绑定 + data 定义 + methods 实现** 一次完成，并用深度选择器做样式匹配。

### 3.5 评分 (el-rate) 特殊注意

**原则**：完全以原始页面为准，不臆造默认值。

- **颜色**：对照源页星星的选中/未选中颜色（黄、橙、金等），通过 `colors`、`void-color` 等 props 或深度选择器覆盖到一致。
- **数值**：每个维度显示几颗实心星必须与源页面一致（如色彩 5、构图 5、想象力 3），不要统一默认 5 星或 3 星。
- **文字**：「超赞」等评语的字号、颜色、位置与源文件一致，用开发者工具对比。
- **样式**：星星、文字、间距均通过 `::v-deep` 精确覆盖。

**常见错误（与 create.md 4.5 一致）：** 所有评分维度都默认设为 5 星或 3 星（忽略源页面实际显示）；星星颜色与源稿不符（如源稿为黄色却用橙色）；未使用深度选择器导致样式无法覆盖；评分文字（如「超赞」）的字号、颜色、位置未与源文件一致。

---

## 四、任务4 强制要求与修复流程

### 4.1 为什么必须按规范做 Element UI 替换

| 要求来源 | 说明 |
|----------|------|
| **任务4 目标** | `data/tasks.md`：将**原生 HTML 元素**替换为 **Element UI 组件**，保持视觉效果一致 |
| **本文档** | 第一至三节：替换总则、映射表、深度选择器、各组件规范 |
| **一致性** | 使用组件库可统一交互、无障碍与维护成本；禁止整页仅用 div+@click 而不用任何 Element 组件 |

**结论：** 凡存在与「映射表」中对应的原生元素或交互（按钮、多选、单选、输入、分页、弹窗等），**必须**用对应 Element UI 组件实现，不得以「可保留 div」为由全部保留原生写法。单选用 el-radio 替换；开关不替换，保留原生 DOM。

### 4.2 常见错误（禁止做法）

| 错误做法 | 说明 | 正确做法 |
|----------|------|----------|
| **整页无 Element 组件** | 所有可点击处均为 `<div @click>`、无 `el-button`/`el-checkbox` 等 | 按映射表识别：按钮→el-button，多选/勾选→el-checkbox，单选→el-radio-group+el-radio，并替换（开关保留原生） |
| **分析报告写「可保留 div」就不替换** | 以单页分析结论替代通用规范，不再做任务4 | 以 `data/tasks.md` 与本文档为准；分析报告仅可标注「无 input/select/分页/弹窗」等，**不能**豁免按钮/单选/复选等已有对应组件的替换（单选用 el-radio 替换） |
| **只写 template 不写样式** | 用了 el-button/el-checkbox 但未用 `::v-deep` 覆盖样式，导致与设计稿不一致 | 每处替换须在 `<style scoped>` 中用**深度选择器**覆盖组件内部样式，直至与源文件像素级一致 |
| **只写 template 不补 data/methods** | 组件用了 `v-model` 或 `@change` 但未在 data/methods 中定义 | 替换时**同步**完成：template 用组件并绑定、data 定义变量、methods 实现事件处理 |

### 4.3 识别：哪些必须用 Element UI 替换

**必须替换的（有明确映射）**：见本文档 **1.2 替换映射表**。包括可点击按钮→el-button、多选/勾选→el-checkbox、input→el-input、select→el-select、分页→el-pagination、弹窗→el-dialog、日期→el-date-picker 等。

**不替换（保留原生 DOM）**：开关不使用 el-switch，保留源页面原有结构（如 div+@click、原生 input 等）。单选用 el-radio-group + el-radio 替换，见 recognition-and-fix.md。

**可选或保持自定义的：**

- 纯展示（无表单、无点击）的静态区域：无需替换。

**识别步骤：**

1. 通读源页面：找出所有「可点击」「可输入」「可选择」的 DOM（button、div/span 充当按钮、input、select、自定义单选/复选等）。
2. 对每一项查**替换映射表**（本文档 1.2、`data/tasks.md` 任务1 步骤3）：有对应组件则必须替换。
3. 在任务1 分析报告中明确列出 `elementComponents`，并标注每处「原元素 → Element 组件」；不得写「可保留 div」替代「替换为 el-button」等结论。

#### 4.3.1 多选框与输入框的识别（易遗漏）

**多选框（el-checkbox / el-checkbox-group）**

- **识别特征**：页面中存在「可勾选/可取消」的项，且为**布尔状态**（开/关、显示/隐藏、是否启用某功能）。常见表现：文案为「隐藏 xxx」「显示 xxx」「是否 xxx」「启用 xxx」等；设计上为「图标 + 文字」或「小方框 + 文字」的可点击区域；源实现可能是 `<div @click="toggleX">` 或多个相似 div。
- **易漏原因**：源 HTML 未使用 `<input type="checkbox">`，而是用 div+点击切换，容易被误判为「自定义 UI 可保留」。
- **正确做法**：凡「布尔开关/勾选」语义，**必须**用 `el-checkbox`（单个）或 `el-checkbox-group`（多选列表），用 `v-model` 绑定布尔或数组，并用 `::v-deep` 匹配原视觉（含图标、文字、选中态）。替换时须先判断原样式是否多选框 → 替换后删除原多选框 DOM → 将 el-checkbox 样式覆盖为与原有样式一致，详见本文档 **2.7、2.8 节**。

**输入框（el-input）**

- **识别特征**：页面中存在**可由用户编辑的文本**，用于输入公式、关键词、姓名、数量等。常见表现：设计上为可编辑区域（白底、边框、占位符等），或静态稿中展示为「示例文字」但业务上需用户输入；源实现可能是 `<span>{{ value }}</span>` 仅展示，但产品需求为「用户可修改该值」。
- **易漏原因**：源静态稿只有 `<span>` 展示默认值，未出现 `<input>` 标签，分析时未结合业务判断「此处应为可输入」而漏识别。
- **正确做法**：凡「用户需编辑的文本」语义，**必须**用 `el-input`（单行或 `type="textarea"`），用 `v-model` 绑定变量，占位符用 `placeholder`，并用 `::v-deep` 匹配原样式。

**任务1 分析报告中的必填项**：在 `elementComponents` 中**显式列出**「多选框」与「输入框」的识别结果，例如：公式栏 → el-input、隐藏过程/进位信息 → el-checkbox（或 el-checkbox-group），不得以「无标准 input/checkbox」为由省略。

### 4.4 修复方法（通用流程）

**步骤 1：列出替换清单**  
根据「识别」结果，列出：位置描述、原 HTML/交互、拟用 Element 组件、所需 data 与 events。示例：生成按钮 → `el-button`，data 无新增，events：`@click="handleGenerate"`。

**步骤 2：替换 template**  
删除或注释掉被替换的原 HTML。插入对应 Element 组件，写好 `v-model`、`@click`、`@change` 等绑定；组件外层包一层容器并加 `class="[sourceName]_xxx_container"` 便于样式限定。

**步骤 3：补全 data 与 methods**  
在 `data()` 中定义组件所需变量（如 `dialogVisible`、`currentPage`、`carryPosition` 等）。在 `methods` 中实现已绑定事件（如 `handleGenerate`、`handleCarryPosition`）；方法命名使用 `handle` + 功能/事件名。

**步骤 4：样式匹配（深度选择器）**  
在 `<style scoped>` 中，用**父容器类 + `::v-deep`** 选中组件内部类（如 `.el-button`、`.el-checkbox__label`、`.el-input__inner`），覆盖为与源文件一致的尺寸、颜色、圆角、间距、字体等。覆盖时兼顾默认态、选中态、hover 等，保证与设计稿一致。

**步骤 5：验证**  
在浏览器中对比改造前后：样式一致、点击/选择行为正确、无控制台报错、表单项与 data 同步正确。

### 4.5 与现有文档的对应关系

| 文档 | 相关内容 |
|------|----------|
| 本文档 | 替换总则、映射表、深度选择器、搜索框与各组件规范；任务4 强制要求、常见错误、识别与修复流程；单选用 el-radio 替换见 recognition-and-fix.md |
| `data/tasks.md` 任务4 | Element UI 替换的通用步骤、各组件示例、验证标准 |
| `data/execution-flow.md` | 组件与方法同步生成、可点击按钮须绑定方法 |

执行任务4 时须同时满足上述文档；本文档提供**替换规范与强制要求的完整依据与操作流程**。

---

## 五、验证要点（Element UI 替换部分）

- 所有替换点均已用正确组件替换，且原 HTML 已删除。
- 每个组件的 `v-model` / 绑定变量均在 `data()` 中定义。
- 每个组件绑定的事件（`@click`、`@change`、`@size-change` 等）均在 `methods` 中有实现。
- 所有可点击按钮均有 `@click="handleXxx"` 且已实现对应方法。
- 样式通过 `::v-deep` 覆盖，与源文件在尺寸、颜色、圆角、状态上一致；带外框搜索框符合 2.4。
- 无控制台报错，交互与数据流正常。

---

## 六、UI/UX 与可访问性（与 ui-ux-pro-max 对齐）

在满足与源稿像素级一致的前提下，交付前可对照以下规则，避免常见不专业表现（详见 ui-ux-pro-max Skill）：

| 类别 | 规则 | 建议做法 |
|------|------|----------|
| **图标与视觉** | 不用 emoji 作 UI 图标 | 使用 SVG 或 Element UI / Heroicons / Lucide 等图标 |
| **交互与光标** | 可点击元素有明确反馈 | 为可点击卡片/按钮添加 `cursor-pointer`；hover 时提供颜色/阴影等视觉反馈 |
| **动效** | 避免布局错位 | hover 时慎用 `transform: scale()`，以免撑开布局；优先使用颜色、透明度、阴影过渡 |
| **对比度** | 亮色模式可读性 | 正文文字避免过浅（如不用 slate-400 作正文）；玻璃/透明卡片在亮色下需足够不透明度（如 `bg-white/80`） |
| **焦点与键盘** | 可访问性 | 表单与按钮的 `:focus` 状态可见，便于键盘导航 |

以上为补充性要求；**改造任务的首要目标仍是与 create.md 及源文件视觉效果、交互逻辑一致**。
