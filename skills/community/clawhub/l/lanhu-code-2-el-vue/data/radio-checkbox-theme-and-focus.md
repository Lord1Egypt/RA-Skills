# 单选（el-radio）与多选（el-checkbox）主题色、焦点态与多主色稿面

本文档配合 **SKILL.md §6.3.8、§6.3.8.1、§6.3.10** 使用：说明为何仅覆盖 `is-checked` / `:hover` 仍会出现「激活态仍是蓝」、如何从 **当前页** `index.css` 取色，以及须补充的 **CSS 选择器清单**。

---

## 1. 现象与根因

### 1.1 现象

- 已将 `background-color`、`border-color` 写在 **`.el-checkbox__input.is-checked .el-checkbox__inner`** / **`.el-radio__input.is-checked .el-radio__inner`** 上，但点击或 Tab 后，控件边缘仍呈 **Element 默认主色（#409EFF 一类）**。
- 单选外圈有时出现 **浅色光晕**，颜色仍为蓝，与稿面主色不一致。

### 1.2 根因（Element UI 2）

- **多选**：`checkbox.scss` 中 **`.el-checkbox__input.is-focus .el-checkbox__inner`** 单独设置 `border-color: $--checkbox-input-border-color-hover`（通常即主色蓝），**优先级与 checked 分离**；仅写 `is-checked` 不能消除 focus 边框色差异（依焦点顺序可能仍见蓝）。
- **单选**：
  - **`.el-radio__input.is-focus .el-radio__inner`** 同样使用 hover 变量作边框色；
  - **`radio.scss`** 中 **`.el-radio:focus:not(.is-focus):not(:active):not(.is-disabled) .el-radio__inner`** 使用 **`box-shadow: 0 0 2px 2px $--radio-input-border-color-hover`**，未覆盖时焦点环恒为默认主色。

### 1.3 多主色稿面（易混色）

同一 `index.css` 中可能同时存在：

- **列表 / Tab / 导航高亮**：如 `rgba(0, 116, 252, 1)`；
- **设置区主按钮、勾选切图、装饰竖条**：如 `rgba(4, 180, 182, 1)`。

**规则**：`el-checkbox` / `el-radio` 所在区块若与「主按钮 / 静态勾选图」为同一视觉系统，**须用该支颜色**覆盖全部状态，**不得**仅因「全站主色」或习惯选用 Tab 蓝。

---

## 2. 识别步骤

1. 在 **index.vue** 中找到该控件对应的**静态结构**（原 `thumbnail_*` / `image-wrapper_*` 勾选图、单选圆点图）。
2. 在 **index.css** 中查：
   - 同区 **`.thumbnail_*` / `.image-wrapper_*`** 的 `background`（切图主色倾向）；
   - **同卡片内主按钮**、**`section_*` 小竖条**等的 `background-color` / `border-color`。
3. 在浏览器 **DevTools** 中选中 `.el-checkbox__input` 或 `.el-radio__input`，查看是否带 class **`.is-focus`**；对单选再查看 **`.el-radio`** 根节点在 `:focus` 时子节点 **`.el-radio__inner`** 的 **computed `box-shadow`**。

---

## 3. 修复方法（选择器清单）

设 `[THEME]` 为步骤 2 得到的稿面主题色（如 `rgba(4, 180, 182, 1)`），`[父级]` 为包在组件外的自定义 class（与 `::v-deep` 联用）。

### 3.1 多选 el-checkbox

```css
[父级] ::v-deep .el-checkbox__input.is-checked .el-checkbox__inner,
[父级] ::v-deep .el-checkbox__input.is-indeterminate .el-checkbox__inner {
  background-color: [THEME];
  border-color: [THEME];
}
[父级] ::v-deep .el-checkbox__inner:hover {
  border-color: [THEME];
}
[父级] ::v-deep .el-checkbox__input.is-focus .el-checkbox__inner {
  border-color: [THEME];
}
```

### 3.2 单选 el-radio

```css
[父级] ::v-deep .el-radio__input.is-checked .el-radio__inner {
  border-color: [THEME];
  background-color: [THEME];
}
[父级] ::v-deep .el-radio__inner:hover {
  border-color: [THEME];
}
[父级] ::v-deep .el-radio__input.is-focus .el-radio__inner {
  border-color: [THEME];
}
/* 与 Element 一致结构：焦点环用稿面主色半透明，或按稿改为 none */
[父级].el-radio:focus:not(.is-focus):not(:active):not(.is-disabled) ::v-deep .el-radio__inner {
  box-shadow: 0 0 2px 2px rgba(4, 180, 182, 0.35); /* 示例：与 [THEME] 同色相、透明度按稿调整 */
}
```

**注意**：若自定义 class 写在 `<el-radio class="[父级]">` 上，则 `[父级]` 与 `.el-radio` 在同一节点，选择器写为 **`[父级].el-radio:focus...`**（见 SKILL §6.3.6.1 根节点 class 规则）。

---

## 4. 需求文案（交付/评审用）

- 静态页改为 `el-checkbox` / `el-radio` 后，**选中、悬停、键盘/鼠标焦点**下的边框与（单选）**焦点环**须与 **当前页 index 稿面**一致，**不得**残留 Element 默认主色蓝。
- **主题色**必须从 **本视图** `index.vue` 与 **其引用的 index.css** 中，按**控件所在区块**与静态勾选/主按钮**就近**提取；同一页存在多种强调色时，**表单控件与对应区块静态稿一致**，不得误用其它区域的色值。

---

## 5. 自检清单

- [ ] `is-checked`、`is-indeterminate`、`hover`、`is-focus` 均已覆盖，颜色为稿面 `[THEME]`。
- [ ] 单选已覆盖 **`box-shadow` 焦点环**（或明确与产品确认取消阴影）。
- [ ] 与 index 中同区主按钮、勾选 PNG、装饰条颜色**目视一致**。
- [ ] 未从其它文件夹的 `Custom.vue` 或全局习惯色「猜」主题色。
