# 列表行高度与对齐：识别与修复（通用规则）

## 1. 适用场景

将静态页（index.vue）改造为 Custom.vue 时，若列表使用 **v-for 渲染**，可能出现以下问题：
- **列表行高度不够**：文字被截掉一部分（如行高 22px 但容器高度 23px，导致底部被裁切）
- **右侧列表对齐问题**：列表项内各列（如课包名、讲次、状态、更新）未按设计稿对齐，右侧元素位置偏移

本文档给出识别规则、修复方法与需求文案，供改造与自检使用。

## 2. 问题成因

| 来源 | 说明 |
|------|------|
| **固定高度限制** | index.css 中列表行设置了固定 `height`（如 `height: 23px`），但行内元素（如文字）的 `line-height` 与 `height` 相同（如 `height: 22px; line-height: 22px`），在 flex 布局下可能导致内容被截断。 |
| **flex 子项收缩** | 列表行使用 `flex-row` 布局，子元素未设置 `flex-shrink: 0` 时，可能被压缩导致宽度不足，影响后续元素对齐。 |
| **宽度未固定** | 列表项内各列（如讲次信息、状态信息）使用 `width: auto` 而非固定宽度，导致在不同内容长度下位置不一致。 |
| **margin 值不精确** | 各列之间的 `margin-left` 值未与设计稿完全一致，导致右侧元素整体偏移。 |

因此：**列表行必须使用 `min-height` 而非固定 `height`，各列需固定宽度并设置 `flex-shrink: 0`，margin 值需精确匹配设计稿。**

## 3. 识别规则（通用）

### 3.1 何时需要做「列表行高度与对齐」修复

满足以下条件时，必须按 4 的修复方法处理：

- 存在**列表**（如课程列表、资源列表等），且使用 **v-for** 循环渲染。
- 列表行有**固定高度**（如 `height: 23px`、`height: 52px`），但行内文字可能被截断。
- 列表行使用 **flex-row** 横向布局，包含多个列（如课包名、讲次、状态、更新）。
- 在浏览器中查看时，发现：
  - 文字底部被裁切（如行高 22px 但容器高度 23px，底部 1px 被截掉）
  - 右侧列（如状态、更新）位置与设计稿不一致，整体向右偏移或左移

### 3.2 识别步骤

1. **定位列表行**：在 Custom.vue 的 template 中找到 `v-for` 渲染的列表行容器（如 `.jingpinke_list_normal_row`、`.jingpinke_list_first_row`）。
2. **检查高度设置**：在样式中查看列表行是否使用固定 `height`（如 `height: 23px`），行内文字是否有 `line-height` 且与容器高度接近。
3. **检查列宽度**：列表行内各列（如讲次信息、状态信息）是否使用 `width: auto` 或未设置固定宽度。
4. **检查 flex 收缩**：列表行使用 `flex-row` 时，各列是否未设置 `flex-shrink: 0`。
5. **对照设计稿**：用浏览器开发者工具测量各列的 `margin-left` 值，与 index.css 中的值对比，确认是否一致。

若「固定高度 + 行内文字可能被截断」或「列宽度不固定 + margin 值不一致」同时存在，则必须按第 4 节修复。

## 4. 修复方法（通用）

### 4.1 列表行高度修复

- **将固定 `height` 改为 `min-height`**：
  - 原写法：`height: 23px;`
  - 修复后：`min-height: 23px; height: 23px;`（保留 `height` 以保持设计尺寸，但用 `min-height` 确保内容不被截断）
- **确保行内元素高度一致**：
  - 行内文字元素（如 `.jingpinke_course_name_normal`）需设置 `min-height: 22px; height: 22px;`，与 `line-height: 22px` 配合，确保文字完整显示。
- **添加 `box-sizing: border-box`**：
  - 列表行容器需设置 `box-sizing: border-box`，确保 padding/border 不撑大容器。

### 4.2 列表行对齐修复

- **固定各列宽度**：
  - 原写法：`.jingpinke_lecture_info_normal { width: auto; }`
  - 修复后：`.jingpinke_lecture_info_normal { width: 134px; }`（从 index.css 中查找对应列的固定宽度，如 `.image-text_4 { width: 134px; }`）
- **设置 `flex-shrink: 0`**：
  - 列表行内各列（如课包名、讲次信息、状态信息、更新信息）需设置 `flex-shrink: 0`，防止在 flex 布局中被压缩。
- **精确匹配 margin 值**：
  - 从 index.css 中查找各列的 `margin-left` 值（如 `.image-text_4 { margin: 1px 0 0 366px; }`），在 Custom.vue 中完全一致地设置。
- **设置 `min-width: 0` 与 `overflow`**：
  - 对于可能溢出的文本列（如课包名），设置 `max-width`、`overflow: hidden`、`text-overflow: ellipsis`，但**不影响列容器的固定宽度**（列容器仍用固定 `width`，内部文本用 `max-width` 约束）。

### 4.3 特殊行处理

- **第一行/特殊行**：若第一行有特殊样式（如灰色背景、更大的高度），同样需将 `height` 改为 `min-height`，并确保各列宽度与 margin 精确匹配。
- **第二行/高亮行**：若第二行有高亮背景（如蓝色半透明），需确保行高与各列对齐与普通行一致。

### 4.4 自检清单

- [ ] 所有列表行（普通行、第一行、第二行等）已使用 `min-height` 而非仅 `height`，且行内元素设置了 `min-height`。
- [ ] 列表行内各列（课包名、讲次信息、状态信息、更新信息）已设置**固定宽度**（从 index.css 中查找），不再使用 `width: auto`。
- [ ] 列表行内各列已设置 `flex-shrink: 0`，防止在 flex 布局中被压缩。
- [ ] 各列的 `margin-left` 值与 index.css 中的值**完全一致**（误差不超过 1px）。
- [ ] 在浏览器中查看，文字完整显示（无底部截断），右侧列（状态、更新）位置与设计稿一致。

## 5. 需求文案（可直接用于任务/规范）

以下可作为「静态改动态」任务或规范中的需求描述：

- **列表行高度与对齐**：凡使用 v-for 渲染的列表，其列表行（普通行、第一行、第二行等）必须满足：
  1. **高度**：使用 `min-height` 而非仅固定 `height`，确保行内文字（`line-height` 与 `height` 一致）不被截断；行内元素需设置 `min-height` 与 `height` 一致。
  2. **对齐**：列表行内各列（如课包名、讲次、状态、更新）需设置**固定宽度**（从 index.css 中查找，如 `.image-text_4 { width: 134px; }`），并设置 `flex-shrink: 0` 防止压缩；各列的 `margin-left` 值需与 index.css 中的值**完全一致**（误差不超过 1px）。
  3. **溢出处理**：列内文本（如课包名）可用 `max-width` + `overflow: hidden` + `text-overflow: ellipsis` 防止溢出，但列容器本身需保持固定宽度。
- **自检**：改造完成后，在浏览器中查看列表，确认文字完整显示（无底部截断），右侧列位置与设计稿一致；用开发者工具测量各列宽度与 margin 值，与 index.css 对比确认一致。

## 6. 与现有规范的关系

- **列表项内容溢出**（list-item-overflow.md）：本文档关注**列表行整体高度与各列对齐**，list-item-overflow.md 关注**列表项内动态文本的溢出防护**。两者需同时满足：
  - 列表行高度：用 `min-height` 确保内容不被截断（本文档）
  - 列表项内文本：用 `max-width` 防止文本溢出容器（list-item-overflow.md）
- **样式匹配标准**（style-match-standard.md）：在「完整匹配」列表项时，除尺寸、颜色、字体等与设计一致外，**列表行高度与对齐必须按本文档处理**，不能为追求「与设计稿数值一致」而保留会导致文字截断的固定高度或列宽度不固定。
- **循环渲染规范**（render.md）：v-for 列表的数据与 DOM 结构按 render 规范来；**样式**上若存在列表行高度与对齐问题，则同时满足本文档的要求。

## 7. 示例对比

### 修复前（问题代码）

```css
/* 列表行：固定高度，可能导致文字被截断 */
.jingpinke_list_normal_row {
  width: 1085px;
  height: 23px;  /* ❌ 固定高度，文字可能被截断 */
  margin: 14px 0 0 20px;
  align-items: center;
}

/* 讲次信息：宽度不固定，导致对齐问题 */
.jingpinke_lecture_info_normal {
  width: auto;  /* ❌ 宽度不固定 */
  height: 22px;
  margin: 1px 0 0 366px;
}

/* 课包名：未设置 min-height */
.jingpinke_course_name_normal {
  max-width: 206px;
  height: 22px;  /* ❌ 未设置 min-height */
  line-height: 22px;
}
```

### 修复后（正确代码）

```css
/* 列表行：使用 min-height 确保内容不被截断 */
.jingpinke_list_normal_row {
  width: 1085px;
  min-height: 23px;  /* ✅ 使用 min-height */
  height: 23px;
  margin: 14px 0 0 20px;
  align-items: center;
  flex-wrap: nowrap;
  min-width: 0;
  box-sizing: border-box;  /* ✅ 添加 box-sizing */
}

/* 讲次信息：固定宽度，防止压缩 */
.jingpinke_lecture_info_normal {
  width: 134px;  /* ✅ 固定宽度（从 index.css 查找） */
  min-height: 22px;
  height: 22px;
  margin: 1px 0 0 366px;
  align-items: center;
  flex-shrink: 0;  /* ✅ 防止压缩 */
}

/* 课包名：设置 min-height 确保文字完整显示 */
.jingpinke_course_name_normal {
  max-width: 206px;
  min-height: 22px;  /* ✅ 添加 min-height */
  height: 22px;
  line-height: 22px;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-shrink: 0;  /* ✅ 防止压缩 */
}
```

---

## 8. 多 rowKind / 表格形列表：统一行高与列槽对齐（通用）

### 8.1 适用场景

同一 `v-for` 区域内存在**多种行模板**（如 `lead` 首行灰底课包、`nested` 高亮槽、`normal` 双列、`right_only` / `right_end` 续讲无左列），且静态稿里各 `group_*` 的 **height、margin-top、margin-left** 不一致时，容易出现：

| 现象 | 典型成因 |
|------|----------|
| **行高忽高忽低** | 部分行 `height: 23px`，部分 `52px`，未统一到同一最小行高 |
| **同一列纵向对不齐** | 讲次/状态/更新依赖「子元素 margin-top」凑垂直位置，行高一变即错位 |
| **续讲行整体右飘** | 用「整行 `margin-left: 592px`」代替列网格，与普通行「左 20px + 课包文案宽度可变」不在同一套水平基准上 |
| **项间距不统一** | 仅某类行使用「相邻兄弟 `margin-top: 29px`」，其它行依赖设计稿零散外边距 |

### 8.2 识别步骤

1. 在 Custom.vue 中列出所有 `rowKind`（或等价的 `v-if` / `template` 分支）。
2. 对比各分支**根行容器**的 `height` / `min-height`、**首列起始位置**（是否均为 `margin-left: 20px` 或均为相对同一父级）。
3. 用开发者工具竖线对齐：**讲次列左缘**在 `normal` 与 `right_only` 是否重合；**状态、更新**是否与表头或首行参考线一致。
4. 检查行内文字是否仍用 **`margin-top: 14px`、`16px`** 等做垂直偏移；若父级已 `align-items: center` 且行高统一，应可改为 **0**。

满足「多 rowKind + 列应对齐」而发现上述任一现象，须按 8.3 修复。

### 8.3 修复方法（通用）

1. **统一行高节奏**  
   - 取静态稿中**最高行**（常见为带灰底/高亮槽的 `52px`）作为 **`min-height` 基准**。  
   - 外层 **`.[folder]_list_item`**（或等价 v-for 根）设：`min-height` = 该基准、`display: flex`、`align-items: center`、`box-sizing: border-box`。  
   - 各 rowKind 内层行容器共用类名（如 **`[folder]_list_row_track`**）：`min-height` 与基准一致、`height: auto`、`align-items: center`、`flex-wrap: nowrap`。

2. **统一课包列槽（列对齐核心）**  
   - 从 index.css 读取**首行左侧课包区域宽度**（如 `.box_2 { width: 572px; }`），记为 **`W_package`**。  
   - 对所有含「左列课包文案」的行：用 **`[folder]_col_package_slot`** 包裹课包标题，`width` / `flex: 0 0 W_package`、`min-width: 0`，内部文案 `max-width: 100%` + 省略号。  
   - 对 **`right_only` / `right_end`**：在讲次前放置 **同宽空槽**（`aria-hidden="true"` 或等价），**禁止**再用「整行超大 `margin-left`」模拟缩进。

3. **统一讲次列起点**  
   - 课包槽右侧与讲次块之间，使用**固定小间距**（如 **`margin-left: 20px`**，与首行 `.image-text_1` 等与左列间距一致），讲次块宽度仍按 index.css 分 variant 设置。  
   - 删除依赖「课包文案宽度变化」而改变的 **`margin-left: 366px` / `285px`** 等整段平移（改由槽宽吸收差异）。

4. **统一项间距**  
   - 使用 **`.[folder]_list_item + .[folder]_list_item { margin-top: … }`**（或统一 `padding`）控制行距，**删除**「仅 `.normal_row ~ .normal_row`」等分叉选择器，避免 rhythm 不一致。

5. **垂直居中**  
   - 行容器 `align-items: center` 后，将子节点 **`margin-top` / `margin-bottom`** 置 **0**（特殊绝对定位结构除外），圆点、图标用 **flex 对齐**而非 `margin-top: 7px` 硬凑。

6. **防压缩**  
   - 讲次、状态、更新等列容器保持 **`flex-shrink: 0`** 与文首 4.2 节固定宽度策略一致。

### 8.4 需求文案（可直接用于任务/规范）

- **列表项统一行高**：凡同一列表内存在多种 `rowKind` 行模板，所有 **v-for 列表项外层**须使用**同一 `min-height` 基准**（取静态稿最高行），内层行轨道类须 **`align-items: center`**，**禁止**混用 `23px` / `52px` 等互不一致且仅靠子元素 `margin-top` 对齐的做法。  
- **列槽对齐**：若设计为「左列课包 + 右区讲次/状态/更新」，须设**固定宽度课包列槽**（宽度 = index.css 首行课包区宽度），`normal` 与 **续讲行（无课包文案）** 共用该槽；续讲行使用**空槽占位**，**禁止**单独使用超大整行 `margin-left` 代替列槽。  
- **讲次列起点一致**：讲次块紧贴课包槽右侧，使用**统一间距**（如 20px），不得因课包标题长短改用不同的「整段 `margin-left`」作为讲次起点。  
- **项间距统一**：行与行间距仅通过 **列表项相邻选择器**或统一 `padding` 控制，**禁止**仅对某一 `rowKind` 子集使用额外兄弟外边距。  
- **自检**：在浏览器中竖线比对「讲次 / 状态 / 更新」列是否纵向对齐；各列表项高度视觉一致；无仅靠 `margin-top` 拼凑的垂直对齐。

### 8.5 自检清单（补充）

- [ ] 所有 `rowKind` 行轨道 **`min-height` 与列表项基准一致**，且 `align-items: center`。  
- [ ] 已设 **`W_package` 课包列槽**，`normal` 与 `right_only` / `right_end` 均对齐到同一左栏边界。  
- [ ] 已移除续讲行「整行 **`margin-left: 592px`**」类写法，改为 **空槽 + 统一左内边距/间距**。  
- [ ] 列表项间距仅由 **`.list_item + .list_item`**（或统一 padding）控制，无「仅 normal 相邻 +29px」等分叉。  
- [ ] 行内子元素 **`margin-top` 为 0**（绝对定位块除外），圆点/图标参与 flex 居中。

### 8.6 与双列独立数据源的关系

- **`list-dual-column-independent.md`** 规定 `packageList` + `lectureList` 与 `rowKind` 数据拆分；**本节**规定这些行在 **CSS 上**共用**列槽与行高节奏**。二者同时满足：数据独立、视觉列对齐。

