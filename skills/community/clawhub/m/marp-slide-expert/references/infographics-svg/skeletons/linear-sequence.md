# linear-sequence — 序列骨架

> 横向阅读的**有序**结构。两个变体：箭头串（等分步进）和阶梯（递进跃迁）。

## 何时用 / 何时不用

| ✅ 用 | ❌ 不用 |
|---|---|
| 有明确先后顺序：先做什么后做什么 | 顺序不重要，只是并列（用 [structure-block](structure-block.md)） |
| 阶段演进：L1→L2→L3，能力逐年提升 | 节点之间是「包含」关系（用 [hierarchy-tree](hierarchy-tree.md)） |
| 流程步骤、里程碑、流水线 | 流程会回到起点（用 [flow-cycle](flow-cycle.md)） |

---

## 变体 A：箭头串 Arrow Chain

**语义**：流程叙事，横向阅读。等分步进，每步权重相同。

### 坐标公式（N 步）

```
步距 step  = 192          （N=5 时 5 步占 10→996，viewBox 1020 内）
箭头宽 w   = 184          （= step - 8，8px 缝隙是必须的）
尖长 tip   = 34
矩形部分    = w - tip = 150
中线 y     = 145
序号圆 cy  = 46           （放在箭头上方，不嵌进箭头里）
文字中心 x = x_i + 75     （= 矩形部分中心 150/2，不是整个 184 的中心 —— 差 17px，看起来就是没对齐）
x_i        = 10 + i*192
```

**5 步 path = 矩形 + 右侧三角尖**。文字只放在矩形部分。

```html
<svg viewBox="0 0 1020 300" width="100%">
<defs>
<marker id="a2" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#c0392b"/></marker>
</defs>
<path d="M10,88  L160,88  L194,145  L160,202  L10,202 Z" fill="#95a5a6"/>
<path d="M202,88 L352,88 L386,145 L352,202 L202,202 Z" fill="#7f8c8d"/>
<path d="M394,88 L544,88 L578,145 L544,202 L394,202 Z" fill="#2c3e50"/>
<path d="M586,88 L736,88 L770,145 L736,202 L586,202 Z" fill="#a93226"/>
<path d="M778,88 L928,88 L962,145 L928,202 L778,202 Z" fill="#c0392b"/>
<circle cx="85"  cy="46" r="23" fill="#ffffff" stroke="#95a5a6" stroke-width="2.5"/>
<text x="85"  y="54" class="tb" fill="#95a5a6" text-anchor="middle">1</text>
<text x="85"  y="140" class="t"  fill="#ffffff" text-anchor="middle">愿景</text>
<text x="85"  y="168" class="sm" fill="#ffffff" text-anchor="middle" opacity=".85">统一共识</text>
<circle cx="277" cy="46" r="23" fill="#ffffff" stroke="#7f8c8d" stroke-width="2.5"/>
<text x="277" y="54" class="tb" fill="#7f8c8d" text-anchor="middle">2</text>
<text x="277" y="140" class="t"  fill="#ffffff" text-anchor="middle">共识</text>
<text x="277" y="168" class="sm" fill="#ffffff" text-anchor="middle" opacity=".85">对齐目标</text>
<circle cx="469" cy="46" r="23" fill="#ffffff" stroke="#2c3e50" stroke-width="2.5"/>
<text x="469" y="54" class="tb" fill="#2c3e50" text-anchor="middle">3</text>
<text x="469" y="140" class="t"  fill="#ffffff" text-anchor="middle">路径</text>
<text x="469" y="168" class="sm" fill="#ffffff" text-anchor="middle" opacity=".85">分期落地</text>
<circle cx="661" cy="46" r="23" fill="#ffffff" stroke="#a93226" stroke-width="2.5"/>
<text x="661" y="54" class="tb" fill="#a93226" text-anchor="middle">4</text>
<text x="661" y="140" class="t"  fill="#ffffff" text-anchor="middle">里程碑</text>
<text x="661" y="168" class="sm" fill="#ffffff" text-anchor="middle" opacity=".85">验收标准</text>
<circle cx="853" cy="46" r="23" fill="#ffffff" stroke="#c0392b" stroke-width="2.5"/>
<text x="853" y="54" class="tb" fill="#c0392b" text-anchor="middle">5</text>
<text x="853" y="140" class="t"  fill="#ffffff" text-anchor="middle">闭环</text>
<text x="853" y="168" class="sm" fill="#ffffff" text-anchor="middle" opacity=".85">持续演进</text>
<line x1="85" y1="252" x2="853" y2="252" stroke="#c0392b" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#a2)"/>
<text x="469" y="282" class="sm" fill="#7f8c8d" text-anchor="middle">每一步都有可交付物</text>
</svg>
```

> **本文档所有模板的 `marker id` 都是占位符。** 把多张图放进同一份 deck 时，按位置重编号：第 1 张用 `a1`，第 2 张用 `a3`，第 3 张用 `a5`……（每张图一个独立前缀）。`node scripts/svg-lint.mjs` 会把重复 id 报成 ERROR。

### ⚠️ 反面教材

做成 **6 点的空心 `>` 形**（左右各退 40px 咬合），左半边是**镂空的三角形空洞**，白字浮在洞里完全看不见。见过太多次，不要画成 chevron band。

### 要点

- 步距 204 > 宽度 196 = 8px 缝隙。箭头串读起来靠间隙分隔，缝隙是设计的一部分。
- 序号圆圈放箭头上方 `cy=46`，半径 23，白底 + 描边色。
- 底部虚线（§闭环叠加）把线性流程变成闭环——**这张图最值钱的一笔**。
- **色阶一色族走完**（灰 → 藏青 → 红），视觉焦点自然落在终点。超过 3 个色相就散了。

### 变体：步骤数 ≠ 5

```
step  = (1000 - 10) / N        （末步尖长后仍留 ~20px 右边距）
w     = step - 8
文字中心 = x_i + (w - tip) / 2  ← 矩形部分中心
```

N > 6 时单步过窄，4 字中文标签（`.tb` 19px ≈ 76px）放不下。**降到 6 步封顶**，更多步骤改成 [lanes](lanes.md) 泳道或分两行。

---

## 变体 B：阶梯 Staircase

**语义**：现状 → 目标的**逐级跃迁**。天然带方向感，适合成熟度、演进路径、转型阶段。

### 坐标公式（N 级）

```
x_i       = 20 + i*196
宽 w       = 176
高 height_i = 90 + i*60        ← 等差递增 = 台阶感
y_i       = 420 - height_i     ← 基线固定在 420
主标签 y  = y_i + height_i - 24   （相对块底往上）
副标签 y  = y_i + height_i - 46
注脚行 y  = 446              （基线 420 之下 26）
```

```html
<svg viewBox="0 0 1020 470" width="100%">
<defs>
<marker id="a1" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#c0392b"/></marker>
</defs>
<text x="20" y="30" class="sm" fill="#c0392b" font-weight="700">能力成熟度递进 →</text>
<line x1="20" y1="48" x2="990" y2="48" stroke="#c0392b" stroke-width="2" marker-end="url(#a1)"/>
<line x1="10" y1="420" x2="1010" y2="420" stroke="#dcdcdc" stroke-width="1.5"/>
<rect x="20"  y="330" width="176" height="90"  fill="#95a5a6"/>
<rect x="216" y="270" width="176" height="150" fill="#7f8c8d"/>
<rect x="412" y="210" width="176" height="210" fill="#2c3e50"/>
<rect x="608" y="150" width="176" height="270" fill="#a93226"/>
<rect x="804" y="90"  width="176" height="330" fill="#c0392b"/>
<text x="108" y="382" class="tb" fill="#ffffff" text-anchor="middle">L1</text>
<text x="108" y="404" class="sm" fill="#ffffff" text-anchor="middle" opacity=".85">个人英雄</text>
<text x="304" y="382" class="tb" fill="#ffffff" text-anchor="middle">L2</text>
<text x="304" y="404" class="sm" fill="#ffffff" text-anchor="middle" opacity=".85">团队协作</text>
<text x="500" y="382" class="tb" fill="#ffffff" text-anchor="middle">L3</text>
<text x="500" y="404" class="sm" fill="#ffffff" text-anchor="middle" opacity=".85">流程固化</text>
<text x="696" y="382" class="tb" fill="#ffffff" text-anchor="middle">L4</text>
<text x="696" y="404" class="sm" fill="#ffffff" text-anchor="middle" opacity=".85">平台化</text>
<text x="892" y="382" class="tb" fill="#ffffff" text-anchor="middle">L5</text>
<text x="892" y="404" class="sm" fill="#ffffff" text-anchor="middle" opacity=".85">自愈</text>
<text x="108" y="446" class="lbl" text-anchor="middle">靠个人</text>
<text x="892" y="446" class="lbl" text-anchor="middle">可自愈</text>
</svg>
```

### 硬规则

1. **高度不要等比。** 等比递增会变成柱状图，失去阶梯的叙事。等差（+60）才有「一级一级跳」的感觉。
2. **文字相对块底定位，不要按整块居中。** 块高不等时居中会飘——每级的字会忽高忽低。
3. **基线固定。** 所有块的底边都在 `y=420`，靠高度差形成台阶。
4. **一色族走完**：灰 `#95a5a6` → 藏青 `#2c3e50` → 红 `#c0392b`，强调色只给终点。

### 变体

- **金字塔**（strategy 关系）— 阶梯镜像，层宽递减 + 顶部单点。改 width 公式：`w_i = 176 - i*28`
- **Wave timeline** — 阶梯 + 节点间改 `C` 曲线
- **S-Curve**（技术从试验到普及）— 三段折线 polyline + 三个阶段底色
- **Mountain**（攻坚到高点再回落）— 三角折线 + 顶点强调
- **Bridge / Gap jump**（跨越鸿沟）— 水平带 + 缺口 + 跃起曲线

完整隐喻表见 [../metaphors.md](../metaphors.md)。

---

## 闭环叠加件

任何一张线性图下面加这一条，「一次性流程」就变成「持续演进」：

```html
<line x1="255" y1="392" x2="780" y2="392" stroke="#c0392b" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#a1)"/>
<text x="510" y="422" class="lbl" text-anchor="middle">闭环：反馈 → 迭代 → 新价值</text>
```

虚线在关系图里默认表示**反馈 / 依赖 / 可选路径**，实线箭头表示**流程 / 因果**。线型语义见 [../craft/connectors.md](../craft/connectors.md)。

---

## 连线

| 关系 | 画法 |
|---|---|
| 步与步之间 | 形状本身（尖头）就是箭头，不需要额外连线 |
| 反馈闭环 | `stroke-dasharray="6 5"` 虚线 + marker，置于图底 `y≈392–422` |
| 阶段递进方向 | 图顶 `y=30` 标题 + `y=48` 横线 + marker，标注「递进 →」 |

## 文字排布

- 序号用 `class="tb"`，步骤名用 `class="t"`，补充说明用 `class="sm"`
- 箭头串的文字纵向位置：主标题 `y=140`，副标签 `y=168`（块 88–202，视觉中线略偏上）
- 底部注脚用 `class="lbl"`，灰色，不抢主体
- 单步标签 ≤ 6 个中文字（见 [../craft/typography.md](../craft/typography.md)）
