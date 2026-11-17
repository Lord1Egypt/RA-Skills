# network-hub — 网络与辐射骨架

> 多对多的关系结构。两个变体：中心辐射（一个核心，外围若干）和关系网（节点间任意连线）。

## ⚠️ 先读这一条

**节点多且多对多双向时，不要硬塞进中心辐射。**

Hub & Spoke 的隐含假设是「外围节点之间互不相干，全部只和中心连」。一旦 A、B、C 之间也有关系（A↔B、B↔C），Hub & Spoke 就会丢掉这些交叉关联，图变得比原关系网更简单也更错。

判断方法：**问自己「外围两个节点之间有关系吗？」**
- 没有 → Hub & Spoke
- 有 → 关系网（Force-free 手工布局）

---

## 变体 A：中心辐射 Hub & Spoke

**语义**：一个核心主题/能力，外围 N 个支撑要素。

### 坐标公式（N 个外围节点）

```
中心 cx, cy  = 510, 230
中心圆 r_c   = 66
外围半径 R   = 168
外围节点圆 r_n = 40
θ_i          = -90° + i*(360/N)        从正上方开始，顺时针

节点位置      (cx + R·cosθ,  cy + R·sinθ)
连线起点      (cx + (R-r_n)·cosθ,  cy + (R-r_n)·sinθ)   ← 外圆边缘
连线终点      (cx + r_c·cosθ,  cy + r_c·sinθ)           ← 中心圆边缘
```

**连线必须落在节点和圆心的连线上（径向）**，两端各自抵到圆的边缘。手估端点会在斜向位置留下明显缝隙——6 个节点时这个缝隙非常显眼。

```html
<svg viewBox="0 0 1020 460" width="100%">
<line x1="510" y1="102" x2="510" y2="164" stroke="#b9c3cc" stroke-width="2"/>
<line x1="621" y1="166" x2="567" y2="197" stroke="#b9c3cc" stroke-width="2"/>
<line x1="621" y1="294" x2="567" y2="263" stroke="#b9c3cc" stroke-width="2"/>
<line x1="510" y1="358" x2="510" y2="296" stroke="#b9c3cc" stroke-width="2"/>
<line x1="399" y1="294" x2="453" y2="263" stroke="#b9c3cc" stroke-width="2"/>
<line x1="399" y1="166" x2="453" y2="197" stroke="#b9c3cc" stroke-width="2"/>
<circle cx="510" cy="230" r="66" fill="#1a1a2e"/>
<text x="510" y="238" class="t" fill="#ffffff" text-anchor="middle">数据中台</text>
<circle cx="510" cy="62"  r="40" fill="#c0392b"/>
<text x="510" y="69" class="sm" fill="#ffffff" text-anchor="middle">采集</text>
<circle cx="656" cy="146" r="40" fill="#2c3e50"/>
<text x="656" y="153" class="sm" fill="#ffffff" text-anchor="middle">治理</text>
<circle cx="656" cy="314" r="40" fill="#2c3e50"/>
<text x="656" y="321" class="sm" fill="#ffffff" text-anchor="middle">服务</text>
<circle cx="510" cy="398" r="40" fill="#7f8c8d"/>
<text x="510" y="405" class="sm" fill="#ffffff" text-anchor="middle">资产</text>
<circle cx="364" cy="314" r="40" fill="#2c3e50"/>
<text x="364" y="321" class="sm" fill="#ffffff" text-anchor="middle">分析</text>
<circle cx="364" cy="146" r="40" fill="#7f8c8d"/>
<text x="364" y="153" class="sm" fill="#ffffff" text-anchor="middle">安全</text>
</svg>
```

**N = 4 / 5 / 6 的常用 θ 与坐标**（R=168, r_n=40, r_c=66）：

| θ | 节点 | 连线 |
|---|---|---|
| -90° | (510, 62) | (510,102) → (510,164) |
| 0° | (678, 230) | (638,230) → (576,230) |
| 90° | (510, 398) | (510,358) → (510,296) |
| 180° | (342, 230) | (382,230) → (444,230) |
| -30° | (656, 146) | (621,166) → (567,197) |
| 30° | (656, 314) | (621,294) → (567,263) |
| 150° | (364, 314) | (399,294) → (453,263) |
| 210° | (364, 146) | (399,166) → (453,197) |

### 硬规则

- **连接线不带箭头**（`stroke="#b9c3cc"`），方向已由「中心—外围」的位置关系说清楚，加箭头是噪音。
- **中心节点最深色、最大字号**（`.t`），外围用 `.sm` + 中等色。
- **N ≤ 6。** 7 个外围节点时圆周已经很挤，标签会碰。
- **N ≥ 4 时才用 Hub & Spoke。** 只有 3 个外围节点时，箭头串或 [structure-block](structure-block.md) 的三栏更清楚。
- 第一个节点放正上方（`θ = -90°`），顺时针排。起点定在正上方比定在 3 点方向好读。

### 变体：分层辐射

外围节点再按重要性分**内环 / 外环**两圈：内环 R=130，外环 R=210。表达「直接支撑」和「间接支撑」。

---

## 变体 B：关系网 Network Graph

**语义**：节点间任意连线，无中心。知识图谱、依赖关系、利益关联。

### 手工布局法（不用力导向算法）

力导向的结果每次都不一样，**不要用**。按这个顺序手工摆：

1. **找出度数最高的 1–2 个节点**，放中心（若确实无中心，则按逻辑分组摆）
2. **其余节点按语义分组**（同一阵营 / 同一阶段 / 同一类型），每组内部紧凑
3. **组与组之间留大间隙**（≥60px），组内节点间距 40–60px
4. **连完之后手工理线**——优先消除交叉，必要时加中继点走 `V` `H` `V` 折线

### 坐标公式（3 阵营布局）

```
阵营 A 中心 (250, 200)   成员散布 ±50     ← 阵营节点 y 跟跨阵营红线 y 共线
阵营 B 中心 (770, 200)   成员散布 ±50
阵营 C 中心 (510, 350)   成员散布 ±50
节点 r = 34
跨阵营红线 y = 200（贯穿 A、B 中心）
阵营内连线：浅灰、细、无箭头
```

**阵营节点必须和跨阵营红线共线。** A、B 在 y=200，红线也走 y=200——这样节点的边缘正好落在红线上，**节点本身成为红线的视觉延伸**，而不是飘在上面让红线穿空。这是关系网最容易画错的一处：节点和主连线 y 错开，整张图读成「三个分散的阵营」而不是「一个紧密的网」。

```html
<svg viewBox="0 0 1020 460" width="100%">
<line x1="294" y1="200" x2="726" y2="200" stroke="#c0392b" stroke-width="2.5"/>
<line x1="300" y1="240" x2="480" y2="350" stroke="#7f8c8d" stroke-width="1.5"/>
<line x1="700" y1="240" x2="540" y2="350" stroke="#7f8c8d" stroke-width="1.5"/>
<circle cx="230" cy="200" r="34" fill="#2c3e50"/><text x="230" y="207" class="sm" fill="#ffffff" text-anchor="middle">A1</text>
<circle cx="320" cy="200" r="34" fill="#2c3e50"/><text x="320" y="207" class="sm" fill="#ffffff" text-anchor="middle">A2</text>
<circle cx="700" cy="200" r="34" fill="#c0392b"/><text x="700" y="207" class="sm" fill="#ffffff" text-anchor="middle">B1</text>
<circle cx="790" cy="200" r="34" fill="#c0392b"/><text x="790" y="207" class="sm" fill="#ffffff" text-anchor="middle">B2</text>
<circle cx="510" cy="370" r="34" fill="#7f8c8d"/><text x="510" y="377" class="sm" fill="#ffffff" text-anchor="middle">C1</text>
</svg>
```

### 硬规则

- **阵营节点 y 必须跟跨阵营主连线 y 共线。** 主连线要的就是把阵营串起来，节点飘了就成了三条断线。
- **节点数 ≤ 7。** 关系网最容易失控，超过 7 个节点线就开始糊。
- **有向关系用箭头，无向关系不带箭头。** 混用前先确定这张图要不要表达方向。
- **交叉 ≤ 3 处。** 超过说明布局错了，重排节点。
- **同阵营的连线用浅灰**（`#dcdcdc`），跨阵营的连线用强调色——这样视线能立刻分出「内部关系」和「外部关系」。

---

## 什么时候该降级

- 外围节点有明确**顺序** → [linear-sequence](linear-sequence.md) 箭头串
- 外围节点是**分类**不是关系 → [structure-block](structure-block.md) 便当格
- 外围节点是**时间轴上的阶段** → [lanes](lanes.md) 泳道
- 节点 > 7 或交叉 > 5 → 拆成多张图

## 连线

| 关系 | 画法 |
|---|---|
| 中心—外围 | 直线，浅灰 `#b9c3cc`，`stroke-width="2"`，**无箭头** |
| 阵营内关系 | 直线，最浅灰 `#dcdcdc`，`stroke-width="1.5"`，**无箭头** |
| 跨阵营关系 | 直线，强调色 `#c0392b`，`stroke-width="2.5"` + 箭头 |
| 依赖 | 虚线 `stroke-dasharray="6 5"` + 箭头 |

## 文字排布

- 圆形节点标签：圆心居中 `y = cy + 字号*0.4`（`.sm` 15px → `y = cy + 6`）
- 圆内标签 ≤ 3 个中文字（`r=40` 时 4 字 = 60px，勉强；`r=34` 时 3 字 = 45px 刚好）
- 标签放不下就放圆外：标签起点 `cx + r + 9`，`text-anchor="start"`
- 中心节点 `.t` 26px，4 字 = 104px，`r=66`（直径 132）放得下
