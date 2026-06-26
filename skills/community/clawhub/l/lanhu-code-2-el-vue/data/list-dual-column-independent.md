# 双列列表（左/右独立数据源）：识别与修复（通用规则）

## 1. 适用场景

将静态页（index.vue）改造为 Custom.vue 时，若主内容区为**表格形双列布局**（常见命名：**左侧课包/资源列** + **右侧讲次/明细列**），设计稿在 DOM 上往往按「行」平铺，但业务上两列数据来源不同（接口不同、长度不同、或续讲行左侧无单元格）。

若改造时把左右字段**捏成单条对象**（如 `{ courseName, lectureName, status }`）并用**一个 `v-for` 驱动整行**，会导致：

- 左侧与右侧无法独立对接真实接口或独立增删；
- 「续讲」等行左侧无内容时，用空字符串 `''` 冒充左侧字段，语义混乱；
- 右侧独占行（仅讲次/状态/更新）仍走「普通整行」模板，**沿用左侧 margin**，与设计稿（整块右移、独立 group）不一致，出现**对齐错误**。

本文档规定：**识别左/右两列语义后，使用两个独立列表（或两套独立数据结构），模板仅通过行下标或显式行类型对齐；续讲/无左列行使用独立 `rowKind` 与独立布局类。**

## 2. 问题成因

| 来源 | 说明 |
|------|------|
| **单对象合并** | 将课包名、讲次、状态、更新写在同一 `item` 上，左右字段强耦合。 |
| **空字符串占位** | 左侧无内容时用 `courseName: ''`，仍走带左侧列的 flex 行，占位或 margin 与设计稿「无左列」不一致。 |
| **忽略设计稿分组** | 设计稿中续讲行常为单独 `group_*`（仅右侧、整体 `margin-left` 较大），与「普通行」不是同一 flex 结构，不能共用同一模板分支。 |

## 3. 识别规则（通用）

### 3.1 何时需要「左右独立列表」

满足以下**任一**即应按第 4 节处理：

- 表头或语义上明确分为**两列**（如「课包」与「讲次/状态/更新」），且产品说明两侧数据来自不同模块或接口。
- 存在**部分行左侧无内容**（续讲、合并单元格视觉），而右侧仍有完整列。
- index.vue 中同一列表区域内，部分行 DOM 结构明显不同（如有左有右 vs 仅右侧一组 `group_17` / `group_18` 类行）。

### 3.2 识别步骤

1. 在 index.vue 中查看列表区域：是否可拆成「左列文案/灰底块」+「右列图标+讲次+状态+更新」。
2. 逐行对比：是否存在**无左侧节点**的行（仅右侧 `flex-row` 且整体缩进）。
3. 在 index.css 中查看这些行的 `margin`、`width`：无左列行是否与「普通行」同一套 margin（通常不是）。
4. 若计划用 v-for 动态化：判断左右是否应**独立请求/独立维护**；若是，禁止用单一扁平对象长期承载两侧业务字段。

## 4. 修复方法（通用）

### 4.1 数据结构

- **`packageList`（或 `leftColumnList`）**：仅描述左侧列；字段示例 `{ id, title }`，**`title` 可为 `null`** 表示该行无左侧展示（续讲行仍保留占位项以便与右侧行下标对齐，或改用显式 `rowIndex` 映射，二选一但要文档化）。
- **`lectureList`（或 `rightColumnList`）**：仅描述右侧列；字段包含讲次文案、图标、状态、更新人等；增加 **`rowKind`**（或等价枚举）区分行模板。
- **对齐方式**：以 **`lectureList`（或较长一侧）为主循环** `v-for="(rightRow, index) in lectureList"`，左侧取 `packageList[index]`；**禁止**在业务层把左右强制塞进一个「大对象」作为唯一数据源（若需提交可再写 computed 合并）。

### 4.2 模板与 rowKind

- `rowKind: 'lead'`：首行特殊样式（如左侧灰底槽 + 竖线）。
- `rowKind: 'nested'`：次行特殊样式（如右侧高亮槽）。
- `rowKind: 'normal'`：左右齐全的标准行。
- `rowKind: 'right_only'` / `'right_only_compact'`：仅右侧列；**单独一块 template + 独立 class**，margin/width **对照 index.css 对应 group**，不得复用「带左侧 margin 的普通行」布局。

### 4.3 样式

- 无左列行：从 index.css 复制对应 `group_*` 的 `width`、`margin-left`、`margin-top`、`margin-bottom`，写到 Custom.vue 的独立类名中（遵守 folder 命名规范）。
- 普通行仍遵守 `list-row-height-alignment.md`、`list-item-overflow.md` 等规范。

### 4.4 自检清单

- [ ] `data()` 中存在**两套**独立列表（或独立结构），未用单一对象同时承载左右业务字段作为唯一源。
- [ ] `v-for` 主循环语义清晰（通常以右侧/明细列为驱动），左侧通过 `packageList[index]` 访问。
- [ ] 续讲或仅右侧行使用独立 `rowKind` 与独立布局类，**未**用空标题 + 普通行凑合。
- [ ] 仅右侧行的 `margin`/`width` 与 index.css 中对应行一致（误差 ≤1px）。
- [ ] `packageList.length` 与 `lectureList.length` 一致或映射关系在注释/computed 中写清，避免越界。

## 5. 需求文案（可直接用于任务/规范）

- **双列列表数据源分离**：若页面为「左侧课包（或资源）列 + 右侧讲次/状态/更新列」，Custom.vue 须使用**两个相互独立**的列表数据源（如 `packageList` 与 `lectureList`），不得以单一合并对象作为唯一数据源。行与行的对齐通过**相同行下标**或显式 `rowKind` 实现。
- **续讲与无左列行**：对设计稿中左侧无单元格的行，左侧数据使用 `title: null`（或等价）并采用**独立**模板分支与样式类（对照 index.css 中单独 `group`），禁止用空字符串 + 普通双列行布局冒充。
- **自检**：左右列表可独立修改数据而不必改动对方结构；仅右侧行在浏览器中与静态稿对齐无偏移。

## 6. 与现有规范的关系

- **列表行高度与对齐**（`list-row-height-alignment.md`）：双列中的**每一列**仍须满足行高、列宽、`flex-shrink: 0` 等要求；**续讲/仅右侧行**在数据上仍用独立 `rowKind` 与模板，在 **布局上**须与 `list-row-height-alignment.md` **第 8 节**一致：使用与首行同宽的**课包空槽**保证讲次/状态/更新列纵向对齐，**避免**仅靠「整行超大 `margin-left`」与 `normal` 行不在同一列网格上对齐。
- **列表项溢出**（`list-item-overflow.md`）：左右列内动态文案仍须 max-width / ellipsis 等处理。
- **单行不换行**（`list-style.md`）：每行 flex 行保持 `flex-wrap: nowrap`（若设计为单行横向排布）。

## 7. 反例与正例（概念）

**反例**：`courseDataList: [{ courseName, lectureName, status, updater }]`，续讲行 `courseName: ''`，全部 `v-else` 同一模板。

**正例**：`packageList` + `lectureList`，`v-for` 右列，`rowKind === 'right_only'` 单独模板 + **课包列空槽（宽度 W_package）** + 与 `normal` 行统一的行高/间距，左侧 `packageList[i].title` 与右侧 `lectureList[i]` 解耦。
