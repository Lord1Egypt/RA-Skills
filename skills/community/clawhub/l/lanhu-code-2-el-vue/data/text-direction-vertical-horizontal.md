# 文字竖排与横排：识别与修复（通用规则）

## 1. 适用场景

将静态页（index.vue）改造为 Custom.vue 时，若设计稿中某段文字为**竖版排列**（竖排，每个字从上到下排成一列），而改造时未识别、仍按横版排布，会导致**版式与设计不一致**。本文档给出竖排/横排的识别规则、修复方法与需求文案，供改造与自检使用。

## 2. 竖排与横排的区分

| 版式 | 说明 | 典型场景 |
|------|------|----------|
| **竖排（竖版）** | 文字自上而下排列，多列时从右向左；单列时一字一行。 | 古诗词标题、作者；传统书法风格；部分卡片/列表标题。 |
| **横排（横版）** | 文字自左向右排列，多行时从上到下。 | 常规正文、按钮、表单、多数列表项。 |

## 3. 识别规则（通用）

### 3.1 如何判断设计稿中为竖排

在 index.css 中，若某文本类同时满足以下特征，应识别为**竖排**：

| 特征 | 说明 | 示例 |
|------|------|------|
| **窄宽高瘦** | 容器 `width` 约等于**单字宽度**（约 1em，如 14px～24px），`height` 明显大于 width，可容纳多字纵向排列。 | width: 20px; height: 60px（约 3 字竖排） |
| **line-height 与 width 接近** | 行高与“宽度”数值接近，便于一字一行。 | width: 20px; line-height: 20px |
| **设计语义** | 古诗词、文言、书法、传统风格等常采用竖排。 | 古诗标题、朝代·作者、对联等 |

**识别步骤：**

1. 在 index.vue 中定位列表项/卡片内的**标题、副标题、作者、朝代**等文案节点，记下其 class。
2. 在 index.css 中查该 class 的 **width、height、line-height**。
3. 若 **width 为 14px～24px 量级且 height 明显大于 width**（如 height 为 48px、60px、100px），且 line-height 与 width 接近，则识别为竖排。
4. 若 width 较大（如 80px 以上）、height 较小或未限制，或为多行横排布局，则识别为横排。

### 3.2 如何判断为横排

- width 较大或未限制，height 为单行或少量行高；或
- 未出现「窄宽高瘦」特征；或
- 设计语义为常规 UI 文案（按钮、标签、说明文字等）。

则按**横排**处理，无需添加 writing-mode。

## 4. 修复方法（通用）

### 4.1 竖排的 CSS 实现

对已识别为竖排的文本节点，在 Custom.vue 的样式中增加：

```css
.xxx_title_or_author {
  writing-mode: vertical-rl;   /* 竖排，从右到左（传统中文竖排） */
  text-orientation: upright;   /* 字正立，不旋转 */
  width: 20px;                 /* 约单字宽，与设计稿一致 */
  max-height: 120px;           /* 限制竖排总高度，防溢出；按设计稿与字数调整 */
  overflow: hidden;
  /* 保留原有 font-size、color、line-height、font-family、margin 等 */
  line-height: 20px;           /* 竖排时控制字间距，与设计一致 */
}
```

**要点：**

- **writing-mode: vertical-rl**：竖排、从右到左（多列时），与常见古风/诗词排版一致。若设计为从左到右竖排，改用 `vertical-lr`。
- **text-orientation: upright**：字符正立，不侧转。
- **display: inline-block**：竖排节点若为 inline 元素（如 `<span>`），须设 **display: inline-block**（或 block），否则 width、max-height 在部分浏览器下不生效，导致作者/标题区塌陷或错位。
- **width**：取设计稿中该文本的“窄边”数值（约单字宽），如 14px～24px。
- **max-height**：按设计稿的 height 与最大字数设定（如 48px、60px），避免竖排内容溢出；可与 list-item-overflow 规范结合，用 overflow: hidden 兜底。
- 若设计稿中该区域有 **text-align: right**，竖排下仍可保留，用于对齐。

### 4.2 竖排下的复合文案（如「朝代·作者」）

当竖排节点为**复合文案**（如「朝代 + 作者」：唐 + ·李白）且设计稿中该区域为**单列**（width 仅约单字宽，如 14px～15px）时：

- **禁止在竖排容器内用 `<br>` 分隔朝代与作者**：在 `writing-mode: vertical-rl` 下，`<br>` 会开启**新的一列**（block 方向换行），导致变成两列、与单列设计不符。
- **正确做法**：用**单段文案**拼接，如 `{{ poem.dynasty }}{{ poem.author ? '·' + poem.author : '' }}`，使「唐·李白」在同一竖列内自上而下排列（唐、·、李、白）。
- **height / max-height**：与设计稿一致（如 48px、60px），并设 overflow: hidden。

### 4.3 横排（默认）

无需设置 writing-mode，按常规横排布局与 list-item-overflow 规范处理宽度与溢出即可。

### 4.4 混合布局（如标题竖排 + 作者竖排）

同一列表项内可部分文案竖排、部分横排。仅对识别为竖排的节点添加 writing-mode，其余保持横排。

### 4.5 自检清单

- [ ] 已在 index.css 中根据「窄宽高瘦」与 line-height 判断每处标题/作者/副标题为竖排或横排。
- [ ] 所有识别为竖排的节点已设 `writing-mode: vertical-rl`（或 vertical-lr）、`text-orientation: upright`，**display: inline-block**（若为 span 等 inline 元素），width 与 max-height、line-height 与设计一致。
- [ ] 竖排下的「朝代·作者」等复合文案为单段拼接，未使用 `<br>`，避免竖排时变成多列。
- [ ] 竖排节点已设 overflow: hidden，长文案不溢出列表项。
- [ ] 在浏览器中核对列表项与设计稿，竖排文字方向与版式一致，作者区无塌陷、错位。

## 5. 需求文案（可直接用于任务/规范）

以下可作为「静态改动态」任务或规范中的需求描述：

- **文字竖排与横排**：改造时须根据 index.css 与设计稿**识别每处列表/卡片内标题、作者、副标题等为竖排还是横排**。识别规则：若该文本在 index.css 中为**窄宽高瘦**（width 约 14px～24px、height 明显大于 width、line-height 与 width 接近），或设计语义为古诗词/传统竖版，则视为**竖排**。竖排节点须在 Custom.vue 中设置 `writing-mode: vertical-rl`（或 vertical-lr）、`text-orientation: upright`、**display: inline-block**（若为 span 等 inline 元素），并保留与设计一致的 width、max-height、line-height、overflow: hidden；横排节点不设 writing-mode。**竖排下的复合文案**（如「朝代·作者」）若设计为单列，须用单段文案拼接（如 `dynasty + (author ? '·' + author : '')`），**不得使用 `<br>`**，否则竖排下会变成多列。改造后版式须与设计稿一致，作者区无塌陷、错位。
- **自检**：对照设计稿与 index.css 检查每处文案为竖排或横排；竖排处已正确设置 writing-mode、display: inline-block 与尺寸；竖排复合文案未用 `<br>`；无竖排被误做成横排或横排被误做成竖排。

## 6. 与现有规范的关系

- **样式匹配标准**（style-match-standard.md）：在匹配列表项/卡片的「完整匹配」或「简化匹配」时，除尺寸、颜色、字体外，**文字方向（竖排/横排）须与设计一致**，按本文档识别并实现。
- **列表项溢出**（list-item-overflow.md）：竖排时用 max-height + overflow: hidden 控制溢出，横排时用 max-width + overflow 控制；二者可同时满足。
