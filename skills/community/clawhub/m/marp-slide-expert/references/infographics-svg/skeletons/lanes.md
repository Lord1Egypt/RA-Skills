# lanes — 并行泳道骨架

> 多个实体在**同一时间轴**上并行推进。横轴是时间，纵轴是实体。

## 何时用 / 何时不用

| ✅ 用 | ❌ 不用 |
|---|---|
| 多国/多部门/多产品的同步演进 | 只有一条线在走（用 [linear-sequence](linear-sequence.md)） |
| 同一阶段各方的不同做法 | 实体之间不是并列关系（用 [hierarchy-tree](hierarchy-tree.md)） |
| 跨职能时间线、迁移计划、版本节奏 | 各方事件之间有强因果（那是网络图） |

---

## 硬规则

1. **所有泳道共享一条时间轴。** 竖直分隔线必须贯穿全部泳道，否则读者无法对齐时间。
2. **时间刻度只标在最上方一条**，不要每条都标。
3. **同一时间点上的事件竖直对齐。** 这是泳道图的全部价值——让人看出"这几件事同时发生"。
4. **泳道内的事件沿轴等距排，间距不小于 120px。** 挤在一起就失去"时间感"了。

---

## 变体：并行泳道 Swimlanes

### 坐标公式（N 条泳道，M 个阶段）

```
时间轴       y = 50，x 从 150 → 980
时间刻度标签  y = 36            ← 必须在轴线上方；SVG 里不要再放标题，会和它撞
阶段竖线      x_k = 150 + k*(830/M)   y 从 50 → 泳道底部
泳道标签区    x = 20 → 140（text-anchor="end"，x=130）
泳道底色      x=150 w=830
泳道高 h      = 86
泳道间距      = 14
y_i          = 66 + i*(h + 14)        第 1 条 66–152，第 2 条 166–252
事件圆心 cy   = y_i + 40
事件标签 y    = cy + 34                （放圆下方，不放圆内）
viewBox       0 0 1020 (66 + N*100 + 34)
```

**阶段竖线必须落在事件列的正中间。** 竖线是「时间格」边界，事件是格里的内容——两者错位，整张图就散了。

```html
<svg viewBox="0 0 1020 300" width="100%">
<defs>
<marker id="a1" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#c0392b"/></marker>
</defs>
<text x="290" y="36" class="sm" fill="#7f8c8d" text-anchor="middle">Q1</text>
<text x="565" y="36" class="sm" fill="#7f8c8d" text-anchor="middle">Q2</text>
<text x="840" y="36" class="sm" fill="#7f8c8d" text-anchor="middle">Q3</text>
<line x1="150" y1="50" x2="980" y2="50" stroke="#c0392b" stroke-width="2" marker-end="url(#a1)"/>
<line x1="428" y1="50" x2="428" y2="256" stroke="#dcdcdc" stroke-width="1" stroke-dasharray="3 4"/>
<line x1="703" y1="50" x2="703" y2="256" stroke="#dcdcdc" stroke-width="1" stroke-dasharray="3 4"/>
<rect x="150" y="66"  width="830" height="86" fill="#f7f8f9"/>
<rect x="150" y="166" width="830" height="86" fill="#f7f8f9"/>
<text x="130" y="118" class="tb" fill="#1a1a2e" text-anchor="end">基础设施</text>
<text x="130" y="218" class="tb" fill="#1a1a2e" text-anchor="end">业务应用</text>
<line x1="290" y1="106" x2="565" y2="106" stroke="#c9ced4" stroke-width="2"/>
<circle cx="290" cy="106" r="18" fill="#2c3e50"/>
<text x="290" y="113" class="sm" fill="#ffffff" text-anchor="middle">P1</text>
<text x="290" y="140" class="lbl" text-anchor="middle">试点</text>
<circle cx="565" cy="106" r="18" fill="#2c3e50"/>
<text x="565" y="113" class="sm" fill="#ffffff" text-anchor="middle">P2</text>
<text x="565" y="140" class="lbl" text-anchor="middle">扩面</text>
<circle cx="840" cy="206" r="18" fill="#c0392b"/>
<text x="840" y="213" class="sm" fill="#ffffff" text-anchor="middle">P3</text>
<text x="840" y="240" class="lbl" text-anchor="middle">收敛</text>
</svg>
```

### 要点

- **泳道底色隔行深浅**（`#f7f8f9` / 白），横向阅读时视线不会串道。
- **事件标签放节点下方**（`y = cy + 37`），不要放圆内——圆太小放不下中文。
- 泳道名右对齐到 `x=130`，与时间轴之间留 20px。
- **里程碑事件用强调色**（`#c0392b`），普通事件用中性色。眼睛会先找到里程碑，这通常正是你要的。
- **同泳道的事件之间加一条水平连线**，线要画在圆的下面。没有这条线，事件看起来是散落的；有了它，整条泳道才读成「一条时间线上的推进」。

### 变体：Roadmap 路线图

不画泳道背景条，只画一条主时间轴 + 上下交错的事件。事件多的适合这种（泳道色块会太挤）。

```
主轴 y = 230，贯穿 x=60 → 980
事件 1 y=170（轴上），事件 2 y=290（轴下），交替
连接：M 事件cx,轴y V 事件y
```

### 变体：对照泳道

两条泳道（如"现状 / 目标"或"我方 / 竞品"），每条 3–4 个节点。适合做 before/after 的时间化对比。

---

## 连线

| 关系 | 画法 |
|---|---|
| 时间推进 | 顶部横线 + 箭头（`stroke-width="2"`） |
| 阶段分隔 | 竖直虚线 `#dcdcdc` `stroke-dasharray="3 4"`，无箭头 |
| 事件 → 时间轴 | 短竖线 `stroke="#dcdcdc"`，无箭头 |
| 同泳道事件相连 | 水平细线 `stroke="#c9ced4" stroke-width="2"`，**先画线再画圆**（圆压在线上，读起来是「事件串在一条时间线上」而不是「线穿过圆」） |
| 跨泳道依赖 | 横向连线 + 虚线箭头（`depends_on`） |

## 文字排布

- 泳道名 `.tb` 19px，右对齐 `x=130`
- 事件标签 `.lbl` 15px 灰色，居中 `x = 事件cx`
- 时间刻度 `.sm` 灰色，`y=42`
- 泳道名 ≤ 5 个中文字（标签区宽 120px，`.tb` 19px 下 5 字 = 95px）
