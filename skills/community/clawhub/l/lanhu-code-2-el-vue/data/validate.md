# ✅ 五、最终验证清单

### 5.1 样式检查（使用浏览器开发者工具对比）

**尺寸检查：**
- [ ] 所有元素高度与源文件完全一致（精确到px）
- [ ] 所有元素宽度计算后与源文件一致（百分比但实际值一致）
- [ ] padding、margin、行高与源文件完全一致

**颜色和字体检查：**
- [ ] 文字颜色、背景颜色、边框颜色完全一致
- [ ] 字体类型、大小、粗细完全一致

**视觉效果检查：**
- [ ] 圆角、阴影、透明度、背景图完全一致

**交互状态检查：**
- [ ] hover、active、focus、disabled、selected等状态样式完全一致

**布局检查：**
- [ ] display、flex/grid、对齐方式、定位与源文件一致

**筛选项折行（适用横向筛选 / el-radio-group）：**
- [ ] 筛选卡与筛选行在选项折行时 **min-height + 自动增高**，无固定 height 导致与下行重叠（见 `filter-row-wrap.md`）

**垂直居中检查：**
- [ ] el-button 文字在按钮内垂直居中（按钮 class 已设 `display: inline-flex; align-items: center; justify-content: center; line-height: 1`）
- [ ] **el-button 选择器未误用**：自定义 class 在按钮根上时，样式为 **`.class.el-button`**（或外层 div + `::v-deep`），**未**使用 **`.class ::v-deep .el-button`** 导致筛选/次要按钮样式丢失（见 `data/el-button-root-and-deep.md`、Skill 6.3.6.1）
- [ ] **el-button 类型与三态**：带底/边的次要按钮**未误用** `type="text"`；主按钮及次要按钮已写全 **:hover / :focus / :active**（及主按钮字色）；并排按钮已处理 **`.el-button + .el-button` 默认间距**；按钮内 **img/span** 已去源稿静态 **margin**（见 `el-button-root-and-deep.md` 2.1～2.3）
- [ ] 列表/步骤 **badge 内数字或文字水平垂直都居中**（badge 容器已设 `display: flex; align-items: center; justify-content: center`，子元素 `text-align: center; margin: 0`）
- [ ] 列表项行内（badge + 文字 + 图标）整体垂直居中（行容器已设 `display: flex; align-items: center`，子元素无垂直 margin）

**下拉框与激活态主题色：**
- [ ] el-select 触发器尺寸、边框、圆角与设计一致；focus/hover 边框色为页面主题色
- [ ] el-select **右侧箭头/后缀**垂直与水平位置与稿一致：根节点**未**误用 `flex`+`space-between`；已同步 **`.el-input__icon` / `.el-select__caret`** 与 **inner 高度**及 **`.el-input__suffix` 的 `right`、`padding-right`**（见 `data/el-select-suffix-alignment.md`、Skill 6.3.7.1）
- [ ] el-select 下拉选项选中/悬停为主题色（已用 `popper-class` + 非 scoped 样式覆盖，非 Element 默认蓝）

**多选框激活态主题色：**
- [ ] el-checkbox 选中/半选时方框背景与边框为页面主题色（已用 ::v-deep 覆盖 .el-checkbox__input.is-checked .el-checkbox__inner 等）
- [ ] el-checkbox 悬停时边框为主题色（.el-checkbox__inner:hover）

### 5.2 功能检查

**循环渲染：**
- [ ] 所有v-for部分正常渲染
- [ ] 数据数量正确
- [ ] 每个循环项有唯一key值
- [ ] 循环内图片使用require引入

**Element UI组件：**
- [ ] 所有组件功能正常（分页、弹窗、输入等）
- [ ] **每个组件都有对应的data定义**：所有组件使用的数据变量都在 `data()` 中定义
- [ ] **每个组件都有对应的方法实现**：所有事件绑定（`@click`、`@change`、`@size-change` 等）都有对应的处理方法
- [ ] **方法命名规范**：所有方法使用 `handle` 前缀 + 事件类型 + 组件功能（如 `handleSizeChange`、`handleDialogClose`）
- [ ] **无原 DOM 残留**：替换为 el-checkbox / el-button 的区域，已删除原有表现同一交互的 DOM（如原 div+img+span），页面上仅保留一套 Element 组件 UI
- [ ] **多选/按钮样式与源稿一致**：el-checkbox、el-button 通过 ::v-deep 覆盖后，尺寸、颜色、图标位置、未选/选中态、按钮圆角与背景与 index 或设计稿一致（详见 `data/element-ui-style.md` 2.9 节）

**交互事件：**
- [ ] 点击、输入、选择/切换事件正常触发
- [ ] **可点击的按钮均已绑定点击方法**：每个可点击的按钮（上传、预览、确定、取消等）都有 `@click="handleXxx"` 且在 methods 中实现了对应的 `handleXxx`
- [ ] **所有事件处理方法已实现**：template中的每个事件绑定都有对应的methods方法
- [ ] **方法可以正常调用**：测试所有事件处理方法，确保无报错

**数据绑定：**
- [ ] 数据绑定（{{ }}、v-bind）正确显示
- [ ] 双向绑定（v-model）正常工作
- [ ] **所有数据变量已定义**：methods中使用的所有数据都在 `data()` 中定义初始值

### 5.3 代码质量检查

**命名规范：**
- [ ] 所有 class 已重命名为规范格式（`sourceName_功能_内容_特征`）
- [ ] **仅使用下划线 `_` 连接**，未使用连字符 `-` 或驼峰
- [ ] **带数字的 class 已全部替换**：class 名称中不包含任何数字（无 `_1`、`_2`、`cell_2`、`option_3`、`theme_option_1` 等；若改造后仍出现含数字的 class，也须替换为 first、second、left、right 等）
- [ ] class 名称具有描述性和语义化（序位用 first、second、left、right 等英文词）

**CSS选择器：**
- [ ] 所有CSS选择器已同步更新
- [ ] 深度选择器（::v-deep）使用正确

**Vue组件结构：**
- [ ] template部分完整且正确
- [ ] script部分完整（data、methods等）
- [ ] style部分使用 `<style scoped>`

**文件检查：**
- [ ] Custom.vue文件路径正确
- [ ] 文件已成功创建
- [ ] 没有语法错误
- [ ] 可以正常编译和运行

---
