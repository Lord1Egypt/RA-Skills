# structure-block — 框架骨架

> 若干**并列模块**的集合。框和框之间**没有关系线**——它们靠位置、尺寸、底色表达从属和权重。三个变体：便当格、分层框架、对比矩阵。

## 何时用 / 何时不用

| ✅ 用 | ❌ 不用 |
|---|---|
| 多主题概览、特性清单、能力盘点 | 模块之间有明确的流转或从属（用 [flow-cycle](flow-cycle.md) / [hierarchy-tree](hierarchy-tree.md)） |
| 并列维度评分、优劣势对比 | 需要表达因果（框架不画关系线） |
| 现状 vs 目标的逐项拆解 | 内容有先后顺序（用 [linear-sequence](linear-sequence.md)） |

**这一族的共同点：没有连线。** 框与框的关系全靠空间和视觉权重表达。如果你要在框之间画箭头，说明骨架选错了。

---

## 变体 A：便当格 Bento Grid

**语义**：不等大的格子拼成的模块墙。1 个主格 + 若干辅格。

### 硬规则

1. **必须有一个 hero 格。** 全部等大 = 没有重点，等于没做层级。
2. **格子尺寸要有变化**（2×2 / 1×2 / 2×1 / 1×1），但**不能乱**——大格放核心结论，小格放支撑。
3. **所有格子的外边界对齐**。便当盒能拼合是因为槽位规整，随意摆放就散了。
4. **文字量克制**：一格一个标题 + 一行说明（≤ 12 字）。文字多就该拆页。

### 坐标公式（3×3 槽位）

```
网格左 x0   = 20
网格顶 y0   = 60
槽宽 cw     = 320
槽高 ch     = 130
槽间距 gap  = 20
cell(i,j)  x = x0 + j*(cw + gap)
            y = y0 + i*(ch + gap)
viewBox    0 0 1020 470      （3 行时：60 + 3*130 + 2*20 = 490，取 490）
```

```html
<svg viewBox="0 0 1020 490" width="100%">
<text x="20" y="32" class="t" fill="#1a1a2e">平台能力全景</text>
<rect x="20"  y="60"  width="660" height="280" rx="6" fill="#1a1a2e"/>
<text x="48"  y="112" class="t"   fill="#ffffff">统一数据底座</text>
<text x="48"  y="146" class="sm"  fill="#cccccc">打通采集、治理、服务全链路</text>
<text x="48"  y="196" class="sm"  fill="#cccccc">· 12 个业务域接入</text>
<text x="48"  y="226" class="sm"  fill="#cccccc">· 日均 3 亿次调用</text>
<text x="48"  y="256" class="sm"  fill="#cccccc">· 复用率 78%</text>
<rect x="700" y="60"  width="300" height="130" rx="6" fill="#c0392b"/>
<text x="724" y="112" class="tb" fill="#ffffff">自助分析</text>
<text x="724" y="146" class="sm" fill="#ffd9d4">取数从 3 天到 5 分钟</text>
<rect x="700" y="210" width="300" height="130" rx="6" fill="#eef1f4"/>
<text x="724" y="262" class="tb" fill="#1a1a2e">指标平台</text>
<text x="724" y="296" class="sm" fill="#7f8c8d">统一口径，减少争议</text>
<rect x="20"  y="360" width="320" height="110" rx="6" fill="#eef1f4"/>
<text x="44"  y="404" class="tb" fill="#1a1a2e">数据治理</text>
<text x="44"  y="436" class="sm" fill="#7f8c8d">标准先行，质量可控</text>
<rect x="360" y="360" width="320" height="110" rx="6" fill="#eef1f4"/>
<text x="384" y="404" class="tb" fill="#1a1a2e">资产目录</text>
<text x="384" y="436" class="sm" fill="#7f8c8d">找得到，才用得上</text>
<rect x="700" y="360" width="300" height="110" rx="6" fill="#eef1f4"/>
<text x="724" y="404" class="tb" fill="#1a1a2e">成本治理</text>
<text x="724" y="436" class="sm" fill="#7f8c8d">按量计费，省下 30%</text>
</svg>
```

### 要点

- **Hero 格用最深的色**（`#1a1a2e`），辅格用浅色（`#eef1f4`）。整张图的视线焦点。
- **强调格用红色**（`#c0392b`）——只给一个，用来标记最重要的那个辅格。
- **格内文字左边距统一 24px**（`x = 格左 + 24`），所有格对齐到同一条隐形竖线。
- **格内文字纵向**：标题 `y = 格顶 + 52`，说明 `y = 格顶 + 86`，要点行每行 +30。

### 变体：等分格

不需要 hero 时用等分格（全部 320×130）。但**必须有一个格用不同底色**标出重点，否则读者不知道该看哪格。

---

## 变体 B：分层框架 Layered Framework

**语义**：N 层横向堆叠，层与层是支撑关系。见 [hierarchy-tree](hierarchy-tree.md) 变体 B，此处只列选择依据。

| 判据 | 用分层 | 用便当格 |
|---|---|---|
| 层与层有递进关系 | ✅ | ❌ |
| 各层内容独立 | ❌ | ✅ |
| 层数 ≤ 4 | ✅ | 任意 |
| 每层内部要再切分 | ✅ | 切格子 |

---

## 变体 C：对比矩阵 Comparison Matrix

**语义**：同一组维度 × 2–4 个对象，逐格填值。这是**量化**对比，和 2×2 象限完全不同——象限是空间定位，矩阵是表格化。

### 硬规则

1. **行 = 维度，列 = 对象。** 方向反了也可以，但全文必须一致。
2. **每格必须有值**（数字 / 强 / 中 / 弱 / ✓ / ✗）。空格会让读者以为是漏了。
3. **最优格高亮**（浅红底 `#fdecea` 或深色文字），最差格灰化。一张对比矩阵不做区分度，读者要自己逐格扫，等于没整理。
4. **列数 ≤ 4。** 5 列以后横向读不过来。

### 坐标公式（C 列，R 行）

```
行标签区 x  = 20 → 250
数据区      x = 250 → 1000
列宽 cw     = 750 / C
列中心      cx_c = 250 + cw*(c + 0.5)
表头文字 y  = 78
表头线 y    = 90
行高 rh     = 56
第 r 行数据 y = 90 + r*rh + 33          ← 行内垂直居中
高亮列底色  x = 250 + cw*C_recommended,  y = 92,  w = cw,  h = R*rh
viewBox     0 0 1020 (90 + R*rh + 50)
```

**高亮矩形必须严格等于一整列**（`x = 250 + cw*c`，`w = cw`）。手估的 x 和宽度会横跨两列，整张表的结论就指错了对象。

```html
<svg viewBox="0 0 1020 370" width="100%">
<text x="20" y="32" class="t" fill="#1a1a2e">三方案横向对比</text>
<rect x="750" y="92" width="250" height="224" fill="#fdecea"/>
<line x1="20" y1="90" x2="1000" y2="90" stroke="#1a1a2e" stroke-width="2"/>
<text x="375" y="78" class="tb" fill="#1a1a2e" text-anchor="middle">自建</text>
<text x="625" y="78" class="tb" fill="#1a1a2e" text-anchor="middle">采购</text>
<text x="875" y="78" class="tb" fill="#c0392b" text-anchor="middle">混合</text>
<text x="20"  y="123" class="sm" fill="#7f8c8d">上线周期</text>
<text x="20"  y="179" class="sm" fill="#7f8c8d">长期成本</text>
<text x="20"  y="235" class="sm" fill="#7f8c8d">可控性</text>
<text x="20"  y="291" class="sm" fill="#7f8c8d">团队要求</text>
<text x="375" y="123" class="sm" fill="#1a1a2e" text-anchor="middle">9 个月</text>
<text x="625" y="123" class="sm" fill="#1a1a2e" text-anchor="middle">2 个月</text>
<text x="875" y="123" class="tb" fill="#c0392b" text-anchor="middle">4 个月</text>
<text x="375" y="179" class="sm" fill="#1a1a2e" text-anchor="middle">高</text>
<text x="625" y="179" class="sm" fill="#1a1a2e" text-anchor="middle">中</text>
<text x="875" y="179" class="tb" fill="#c0392b" text-anchor="middle">低</text>
<text x="375" y="235" class="sm" fill="#1a1a2e" text-anchor="middle">完全</text>
<text x="625" y="235" class="sm" fill="#1a1a2e" text-anchor="middle">受限</text>
<text x="875" y="235" class="tb" fill="#c0392b" text-anchor="middle">较强</text>
<text x="375" y="291" class="sm" fill="#1a1a2e" text-anchor="middle">需 8 人</text>
<text x="625" y="291" class="sm" fill="#1a1a2e" text-anchor="middle">需 2 人</text>
<text x="875" y="291" class="tb" fill="#c0392b" text-anchor="middle">需 4 人</text>
<line x1="20" y1="330" x2="1000" y2="330" stroke="#dcdcdc" stroke-width="1"/>
<text x="20" y="352" class="lbl">混合方案在四项中三项最优</text>
</svg>
```

### 要点

- **表头和第一列是定位器**，用 `.tb` / `.sm` 加粗或深色。数据格用常规 `.sm`。
- **每行之间画极淡分隔线**（`#f7f8f9`，`stroke-width="1"`），帮助横向追踪。
- **推荐方案整列用浅红底**（`#fdecea`）+ 红色文字，一眼看出结论。
- 行数 ≤ 6，列数 ≤ 4。

---

## 连线

**没有连线。** 变体 C 顶部的横线和行分隔线是**表格线**，不是关系线——`stroke-width` ≤ 2 且不带箭头。

需要关系线时，这个骨架就是选错了。

## 文字排布

- 图标题 `.t`，`y=32`
- 格标题 `.tb`，格内 `y = 格顶 + 52`
- 格说明 `.sm`，格内 `y = 格顶 + 86`
- 表格数据 `.sm` 居中，行内 `y = 行顶 + rh/2 + 6`
- 底部结论 `.lbl`
