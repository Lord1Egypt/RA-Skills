# 带外框搜索框 placeholder 垂直居中与页面溢出（通用规则）

## 1. 适用场景

将静态页（index.vue）改造为 Custom.vue 时，若页面内存在**带外框的搜索框**（el-input 置于固定高度白底容器内）或**底部操作栏**（分页 + 文案 + 按钮），容易出现以下问题：

- **placeholder 未垂直居中**：占位文字在容器内偏上或偏下，与设计稿不一致。
- **输入框/按钮溢出页面**：搜索框所在行或底部分页/按钮区域在窄屏或小容器下横向溢出，出现横向滚动条或裁切。

本文档给出**识别规则**、**修复方法**与**需求文案**，供改造与自检使用。

## 2. 识别规则（通用）

### 2.1 placeholder 未垂直居中

| 维度 | 说明 |
|------|------|
| **表现** | 带外框的 el-input 内，placeholder 或输入文字在视觉上偏上/偏下，未在容器高度内居中。 |
| **常见原因** | ① `.el-input__inner` 高度与容器不一致（如容器 32px、inner 30px 且未与容器对齐）；② 仅设了 `line-height` 未与 `height` 一致，或存在上下 padding 导致行高与可视区不匹配；③ `.el-input` / `.el-input-group` 未在容器内垂直居中，导致整块输入区偏上/偏下。 |
| **识别步骤** | 1）在浏览器中查看带外框搜索框，对比设计稿看 placeholder 是否在容器中线。2）用开发者工具检查 `.el-input__inner` 的 height、line-height、padding。3）若容器有固定高度（如 32px），则 inner 高度宜与容器一致或略小 1～2px，且 line-height 与 inner 高度一致、上下无多余 padding。 |

### 2.2 输入框/按钮溢出页面

| 维度 | 说明 |
|------|------|
| **表现** | 搜索框所在行（如 Tab + 搜索框）或底部分页条、操作按钮在视口或父容器宽度不足时向右溢出，出现横向滚动或右侧被裁切。 |
| **常见原因** | ① 主容器、主卡片、Tab 行、底栏等使用**固定宽度**（如 1122px、1074px）且未设 `max-width: 100%`，小屏下超出视口；② 搜索框使用固定 `width: 400px` 且所在行为 flex 时未设 `min-width: 0` / `flex: 1`，无法在空间不足时收缩；③ 底栏内「已选择 xxx」等文案使用大数值 `margin-left`（如 459px）固定撑开，窄屏下与右侧按钮一起溢出。 |
| **识别步骤** | 1）缩小浏览器宽度或在小屏下查看，是否出现横向滚动或右侧内容不可见。2）检查主容器、主卡片、Tab 行、底栏的 width 是否为固定 px。3）检查搜索框容器是否在 flex 子项中且无 `min-width: 0` 或 `max-width: 100%`。4）检查底栏是否用固定 margin-left 撑开中间区域。 |

## 3. 修复方法（通用）

### 3.1 placeholder 垂直居中

- **外层容器**：保持固定高度（如 32px）、`display: flex`、`align-items: center`、`box-sizing: border-box`、`overflow: hidden`。
- **.el-input**：在容器内 `height: 100%`、`flex: 1`、`min-width: 0`；**增加** `display: flex`、`align-items: center`，使内部输入区在容器内垂直居中。
- **.el-input-group**：`display: flex`、`flex: 1`、`height: 100%`、`min-width: 0`；**增加** `align-items: center`。
- **.el-input__inner**：高度与容器一致（如 32px），`line-height` 与高度一致（如 `line-height: 32px`）；**上下 padding 设为 0**（`padding: 0 0 0 44px` 仅保留左侧为前缀图标留空），`box-sizing: border-box`。若容器略高而希望 inner 略矮 1～2px，则 inner 高度设为 30px、line-height: 30px，并保证 .el-input 的 `align-items: center` 使整块在容器内居中。
- **placeholder**：`::v-deep .el-input__inner::placeholder` 设置颜色；若仍偏上/偏下，可对 placeholder 同轴设置 `line-height` 与 `.el-input__inner` 一致（部分浏览器下 placeholder 继承 line-height）。

**自检**：在设计与多分辨率下，placeholder 与输入文字均在容器高度方向居中；无顶底多余空白。

### 3.2 输入框/按钮不溢出页面

- **页面根容器**：`overflow-x: hidden`（或 `overflow: auto`），避免整页横向滚动；宽度使用 `width: 100%` 或 `max-width: 100%`。
- **主卡片/主内容区**：固定宽度改为 `width: 100%` + `max-width: 1122px`（按设计稿取值），`box-sizing: border-box`，保证小屏下不超出视口。
- **Tab 行（含搜索框）**：整行使用 `width: 100%`、`max-width: 1074px`、`min-width: 0`，使 flex 子项可收缩；搜索框**外层容器**设 `flex: 1`、`min-width: 0`、`max-width: 400px`（或设计稿宽度），避免固定 `width: 400px` 在窄屏下撑破。
- **底部分页/操作栏**：整栏使用 `width: 100%`、`max-width: 1122px`、`min-width: 0`、`box-sizing: border-box`；中间「已选择 xxx」等若原为固定 `margin-left: 459px`，改为 `margin-left: auto` + `flex-shrink: 0`，使左侧分页与右侧文案/按钮之间弹性留白且不溢出。
- **列表/网格区**：若为固定宽度，改为 `width: 100%`、`max-width: 1058px`、`min-width: 0`、`box-sizing: border-box`。

**自检**：在 375px、768px、1024px、1440px 等宽度下，无横向滚动；搜索框与底栏按钮完整可见且不溢出父级。

## 4. 需求文案（可直接用于任务/规范）

- **带外框搜索框 placeholder 垂直居中**：改造时，带外框的 el-input 须保证 placeholder 与输入文字在容器高度内**垂直居中**。做法：外层容器固定高度 + flex + align-items: center；`.el-input`、`.el-input-group` 设 `align-items: center`；`.el-input__inner` 高度与容器一致（或略小 1～2px）、line-height 与高度一致、上下 padding 为 0；必要时对 `::placeholder` 设相同 line-height。自检：多分辨率下 placeholder 与文字均居中。
- **输入框与底栏按钮不溢出页面**：改造后，搜索框所在行与底部分页/操作按钮不得在窄屏下**横向溢出**页面或父容器。做法：页面根容器 `overflow-x: hidden`；主卡片、Tab 行、底栏、列表区使用 `width: 100%` + `max-width: [设计稿宽度]` + `min-width: 0` + `box-sizing: border-box`；搜索框容器在 flex 中设 `flex: 1`、`min-width: 0`、`max-width: [设计稿宽度]`；底栏中间文案将固定大 margin-left 改为 `margin-left: auto`。自检：375px～1440px 下无横向滚动，输入框与按钮完整可见。

## 5. 与现有规范的关系

- **6.3.1 带外框搜索框样式规范**（SKILL.md）：本规范在 6.3.1 基础上补充「placeholder 垂直居中」与「搜索框容器不溢出」的识别与修复。
- **样式一致性**（style-consistency.md）：溢出与居中均属视觉与布局一致性，修复后须在验证清单中检查。
