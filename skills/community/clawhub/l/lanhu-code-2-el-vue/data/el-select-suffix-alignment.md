# el-select 触发器：右侧箭头/后缀图标对齐（通用）

## 1. 问题现象（识别）

改造为 `el-select` 后出现以下任一情况，须按本节排查：

- 下拉箭头（`.el-select__caret` / `.el-input__icon`）**偏上、偏下或与右边缘间距**与 index.vue 中静态图不一致。
- 箭头与文字**重叠**，或右侧显得**过挤/过空**。
- 仅改了 `.el-input__inner` 的 `height` / `line-height`（如小尺寸 28px、30px），**未改后缀区域**，视觉上箭头仍在「默认 40px 行高」的垂直节奏里，导致错位。

## 2. 根因说明

### 2.1 静态稿布局不可照搬 el-select 根节点

源页面常用 **`display: flex` + `justify-content: space-between`** 实现「左侧文案 + 右侧小箭头图」在同一盒子里。

`el-select` 内部由 **`el-input` + 绝对定位的 `.el-input__suffix`** 承载箭头，**不是**「flex 两端对齐」结构。若把同一套 **`display:flex; justify-content:space-between`** 写在 **`el-select` 根节点**（与自定义 class 合并处），会干扰内部 `el-input` 的块级占位与 suffix 的 `right` / `height:100%` 计算，表现为**后缀水平或垂直偏移**。

**规则**：自定义在 `el-select` 上的外壳样式应优先保持与 Element 一致 **`display: inline-block`（或明确 `block` + 宽度）**，**不要**为复刻静态稿而把 `el-select` 根设成 `flex` + `space-between`。

### 2.2 小高度未同步后缀图标行高

Element UI 2 中 `.el-input__icon` 默认使用 **`line-height: $--input-height`（常为 40px）**。当把 `.el-input__inner` 改为 **28px / 30px** 等时，若后缀图标仍为大行高，会在 **28px 高的输入框**内**垂直不对齐**。

**规则**：修改触发器高度时，须用 `::v-deep` **同步** `.el-input__suffix` 内 `.el-input__icon`、`.el-select__caret` 的 **`line-height`、`height`**（与 `inner` 一致或等价），必要时 **`display: inline-flex; align-items: center; justify-content: center`**，并按稿调整 **`right`**（常见 6px～10px，需对照 index.css 中箭头 `margin-right`）。

### 2.3 `padding-right` 与图标占位

`el-select` 对 `.el-input__inner` 默认有 **`padding-right: 35px`**。若改得过小，文字会与箭头重叠；须保证 **≥ 图标宽度 + 右侧留白**（与稿面一致）。

## 3. 修复步骤（建议顺序）

1. **去掉** `el-select` 根上不当的 **`display:flex` + `justify-content:space-between`**，改为 **`inline-block` + `vertical-align: middle`**（父行是 flex 时便于与筛选行对齐），或仅保留宽度/边框/圆角等外壳样式。
2. **`::v-deep .el-input { display: block; }`**，保证占满自定义宽度。
3. **`::v-deep .el-input__suffix`**：`right` 按稿；可用 **`display:flex; align-items:center; justify-content:center`** 使箭头在后缀槽内居中。
4. **`::v-deep .el-input__icon`**（及必要时 **`.el-select__caret`**）：**`line-height` / `height` 与 `.el-input__inner` 一致**，`font-size` 与稿面箭头大小一致。
5. 校验 **`.el-input__inner` 的 `padding-right`**，避免与箭头重叠。

## 4. 需求文案（可写入任务/验收）

- 筛选区/表单项中的 `el-select` 触发器，**右侧箭头位置与垂直居中**须与 index.css / 设计稿一致。
- **禁止**为复刻静态「左文右图」flex，在 **`el-select` 根节点**使用 **`justify-content: space-between`**（除非同时用外层 `div` 包裹且 flex 仅作用于包裹层，而不作用于 `el-select` 根）。
- 凡调整 **`el-input__inner` 高度**，必须**同步后缀图标**的 **`line-height` / `height` / 后缀 `right` / `padding-right`**，保证不重叠、不漂移。

## 5. 自检清单

- [ ] DevTools 中 `el-select` 根节点**无**不当 `display:flex` + `justify-content:space-between`（除非已确认不影响内部 `el-input`）。
- [ ] `.el-input__suffix` 的 `right` 与稿面右侧留白一致；箭头垂直居中。
- [ ] `.el-input__icon` / `.el-select__caret` 的 `line-height`（或 flex 居中）与 `inner` 高度一致。
- [ ] 选中文案不与箭头重叠；open 状态下箭头旋转后仍不溢出框体。

## 6. 关联规范

- Skill **6.3.7**、**6.3.7.1**
- `element-ui-style.md` 中 el-select / 深度选择器说明
- `data/recognition-and-fix.md` 中下拉框 focus 边框（9.7）
