# hierarchy-tree — 层级骨架

> 严格的**从属关系**：A 包含 B，A 是 B 的上级。菱形向上收敛，天然回答「所以呢」。

## 何时用 / 何时不用

| ✅ 用 | ❌ 不用 |
|---|---|
| 组织架构、分类体系、价值拆解 | 兄弟节点之间还有横向关系（改用 [network-hub](network-hub.md)） |
| 理论框架、方法论分解 | 层级超过 3 层（讲不清，见硬规则） |
| 目标 → 举措 → 任务的映射（单边树） | 节点之间是并列而非从属（用 [structure-block](structure-block.md)） |

**关键区分**：如果兄弟节点之间**还有横向连线**（A 和 C 也相关），那不是树——树的定义就是兄弟之间没关系。这时候硬画成树会丢掉那些横向关联，改用网络图。

---

## 变体 A：关系树 Value Tree

### 坐标公式（3 层）

```
根     x=425  y=12   w=200  h=62   rx=6     中心 cx=525
二层   y=150  h=56   w=160   rx=6            中心 cx 各自算
叶子   y=290  h=54   w=130   rx=4            x = 40 / 180 / 320（步距 140，间隙 10）

连接器中继 y：
  根 → 二层：  根底 74  →  中继 108  →  二层顶 150
  二层 → 叶子： 二层底 206 →  中继 238  →  叶子顶 290

直角连接器公式：M 父cx,父底 V 中继y H 子cx V 子顶
```

```html
<svg viewBox="0 0 1020 460" width="100%">
<defs>
<marker id="a4" markerWidth="9" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8 z" fill="#c0392b"/></marker>
</defs>
<rect x="425" y="12" width="200" height="62" rx="6" fill="#1a1a2e"/>
<text x="525" y="52" class="t" fill="#ffffff" text-anchor="middle">企业价值</text>
<rect x="60"  y="150" width="160" height="56" rx="6" fill="#2c3e50"/>
<text x="140" y="186" class="tb" fill="#ffffff" text-anchor="middle">客户价值</text>
<rect x="280" y="150" width="160" height="56" rx="6" fill="#2c3e50"/>
<text x="360" y="186" class="tb" fill="#ffffff" text-anchor="middle">业务增长</text>
<rect x="500" y="150" width="160" height="56" rx="6" fill="#2c3e50"/>
<text x="580" y="186" class="tb" fill="#ffffff" text-anchor="middle">组织能力</text>
<rect x="720" y="150" width="160" height="56" rx="6" fill="#2c3e50"/>
<text x="800" y="186" class="tb" fill="#ffffff" text-anchor="middle">资金效率</text>
<path d="M525,74 V108 H140 V146" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<path d="M525,74 V108 H360 V146" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<path d="M525,74 V108 H580 V146" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<path d="M525,74 V108 H800 V146" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<rect x="40"  y="290" width="130" height="54" rx="4" fill="#fdecea" stroke="#e74c3c" stroke-width="1.5"/>
<text x="105" y="323" class="sm" fill="#1a1a2e" text-anchor="middle">客户洞察</text>
<rect x="180" y="290" width="130" height="54" rx="4" fill="#fdecea" stroke="#e74c3c" stroke-width="1.5"/>
<text x="245" y="323" class="sm" fill="#1a1a2e" text-anchor="middle">品牌资产</text>
<rect x="320" y="290" width="130" height="54" rx="4" fill="#eef1f4" stroke="#7f8c8d" stroke-width="1.5"/>
<text x="385" y="323" class="sm" fill="#1a1a2e" text-anchor="middle">客户成功</text>
<rect x="460" y="290" width="130" height="54" rx="4" fill="#fdecea" stroke="#e74c3c" stroke-width="1.5"/>
<text x="525" y="323" class="sm" fill="#1a1a2e" text-anchor="middle">营收增长</text>
<rect x="600" y="290" width="130" height="54" rx="4" fill="#eef1f4" stroke="#7f8c8d" stroke-width="1.5"/>
<text x="665" y="323" class="sm" fill="#1a1a2e" text-anchor="middle">研发效能</text>
<rect x="740" y="290" width="130" height="54" rx="4" fill="#eef1f4" stroke="#7f8c8d" stroke-width="1.5"/>
<text x="805" y="323" class="sm" fill="#1a1a2e" text-anchor="middle">人才密度</text>
<rect x="860" y="290" width="100" height="54" rx="4" fill="#eef1f4" stroke="#7f8c8d" stroke-width="1.5"/>
<text x="910" y="323" class="sm" fill="#1a1a2e" text-anchor="middle">资本回报</text>
<path d="M140,206 V238 H105 V284" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<path d="M140,206 V238 H245 V284" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<path d="M360,206 V238 H385 V284" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<path d="M580,206 V238 H525 V284" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<path d="M580,206 V238 H665 V284" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<path d="M800,206 V238 H805 V284" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<path d="M800,206 V238 H910 V284" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<line x1="140" y1="392" x2="910" y2="392" stroke="#c0392b" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#a4)"/>
<text x="525" y="422" class="lbl" text-anchor="middle">闭环：业务反馈 → 价值迭代</text>
</svg>
```

### 硬规则

1. **最多 3 层。** 第 4 层开始听众就断了，宁可拆页。层数超了先想能不能聚合。
2. **一行一个子节点，共享父节点的中继 y。** 画一段横线穿过所有子节点的 cx，比画三条独立折线干净。
3. **父节点深色实心 + 白字，叶子浅底 + 描边。** 靠填色深浅表达层级，不靠字号——字号变化在 3 层里看不出来。
4. **描边色区分归属**：属于客户侧的叶子描红边（`#e74c3c`），属于内部侧的描灰边（`#7f8c8d`）。
5. **层级连接线不带箭头。** 方向已经由上下位置说清楚了，加箭头是噪音。线用 `stroke="#b9c3cc"` 浅灰，退到背景里。
6. **叶子之间留 10px 间隙**（`x=40 / 180 / 320`，宽 130）。

### 叶子数量

每层子节点 ≤ 4 个。5 个叶子时 `x = 20 / 262 / 504 / 746`（步距 242，宽 212），或改成两行。

### 闭环叠加

底部加虚线（`y=392`，文字 `y=422`）把静态的树变成「反馈驱动的迭代」。

### 变体：组织架构式（含侧分叉）

真实组织架构里经常出现「助理 / 秘书挂在某位高管下」这种**侧分叉**——它和正父子关系不一样：从父节点的**底部右侧**拉出一根细线到一个同层的小方块，没有更深的孩子。

```
侧分叉 y  = 父块底 y_父 + 6
侧分叉 cx = 父块右 cx_父 + 父宽/2 + 24
侧块宽   = 100，h = 38（比正方块矮一档）
侧块文字 .sm，居中
侧分叉线 stroke="#b9c3cc" stroke-width="1.5"，**无箭头**
```

```html
<rect x="425" y="12"  width="200" height="62" rx="6" fill="#1a1a2e"/>
<text x="525" y="52" class="t" fill="#ffffff" text-anchor="middle">企业价值</text>
<rect x="175" y="150" width="160" height="56" rx="6" fill="#2c3e50"/>
<text x="255" y="186" class="tb" fill="#ffffff" text-anchor="middle">客户价值</text>
<!-- 从「客户价值」底部的右侧拉一根线到助理方块 -->
<line x1="335" y1="206" x2="830" y2="230" stroke="#b9c3cc" stroke-width="1.5"/>
<rect x="830" y="212" width="100" height="38" rx="4" fill="none" stroke="#7f8c8d" stroke-width="1" stroke-dasharray="3 3"/>
<text x="880" y="236" class="sm" fill="#1a1a2e" text-anchor="middle">助理</text>
```

**什么时候用**：
- 组织架构图：高管 + 助理/秘书
- 项目负责人 + 协助角色（PM + Tech Lead）
- 系统组件 + 旁路工具

**不要用**：
- 真正的从属关系（应该用普通的父子连线）
- 旁系分支 > 2 个（太多会让图变乱，改成单独的图）

侧分叉的颜色用浅灰虚线（`#b9c3cc` + `stroke-dasharray="3 3"`），和主父子连线（实线）视觉上分得开。

---

## 变体 B：分层框架 Layered Framework

**语义**：N 个横向堆叠的层/支柱，层与层是**支撑关系**而不是从属。用于「3 层能力模型」「4 大支柱」。

### 坐标公式（N 层）

```
层宽 w    = 900
层高 h    = 64
层间距    = 18
y_0       = 60
y_i       = y_0 + i*(h + 18)
中心 cx   = 510
```

```html
<svg viewBox="0 0 1020 420" width="100%">
<text x="60" y="36" class="sm" fill="#7f8c8d">自下而上：每一层支撑上一层</text>
<rect x="60" y="60"  width="900" height="64" rx="4" fill="#dcdcdc"/>
<text x="510" y="100" class="tb" fill="#1a1a2e" text-anchor="middle">L1 基础设施</text>
<rect x="60" y="142" width="900" height="64" rx="4" fill="#95a5a6"/>
<text x="510" y="182" class="tb" fill="#ffffff" text-anchor="middle">L2 平台能力</text>
<rect x="60" y="224" width="900" height="64" rx="4" fill="#2c3e50"/>
<text x="510" y="264" class="tb" fill="#ffffff" text-anchor="middle">L3 业务应用</text>
<rect x="60" y="306" width="900" height="64" rx="4" fill="#c0392b"/>
<text x="510" y="346" class="tb" fill="#ffffff" text-anchor="middle">L4 用户价值</text>
</svg>
```

**横向分层**（支柱模型）则把层旋转 90°：4 根竖条，`w=210`、`x = 20 / 245 / 470 / 695`、`h=300`、`y=70`。

### 要点

- 层数 ≤ 4。5 层以上没人记得住。
- **色阶由下到上（或左到右）递进**，最深色给顶层——顶层是结论。
- 层内可再切分小格（`x` 方向等分），表达「每层有 3 个组成部分」。

---

## 变体 C：单边映射树 Mapping

只有两层：左列是源，右列是目标，一一对应。

```
左列 x=60  w=300  h=56   y_i = 70 + i*74
右列 x=660 w=300  h=56   y_i 与左列同高
连接器：M 360,左cy H 620,右cy  →  水平直线，两端可加小圆点
```

**不要**画成双向箭头——映射是单向的。加箭头就成了一对多关系，容易误读。

---

## 配套外壳

| 外壳 | 改什么 | 几何底座 |
|---|---|---|
| **Tree / Root system** | 整棵树翻转 180°（根在下） | 变体 A 镜像 |
| **Pyramid 金字塔** | 顶层收成单点，层宽递减 `w_i = 220 - i*40` | 变体 B 改宽度公式 |
| **Onion 洋葱** | 矩形换成同心圆角矩形递减 | 变体 B 换形状 |
| **Foundation blocks 基础块** | 底部一层最宽，向上递减 | 变体 B 层宽递减 |
| **Strategic house 战略屋** | 顶层加屋顶三角，底层加地基矩形 | 变体 B + 上下各加一形状 |

完整隐喻表见 [../metaphors.md](../metaphors.md)。

## 连线

| 关系 | 画法 |
|---|---|
| 层级从属 | 浅灰 `#b9c3cc` 直角折线，`stroke-width="2"`，**无箭头** |
| 映射 | 细实线 `stroke-width="1.5"`，**无箭头** |
| 反馈闭环 | 虚线 `stroke-dasharray="6 5"` + marker，置于图底 |

## 文字排布

- 根节点文字：块内垂直居中 `y = 块顶 + 块高/2 + 19*0.4`（`.tb` 19px）
- 叶子文字：`.sm` 15px，块高 54 时 `y = 块顶 + 27 + 6 = 块顶 + 33`
- 标签 ≤ 4 个中文字；叶子框宽 130 时，5 字（95px）刚好，6 字（114px）就贴边了
- 底部注脚 `.lbl`，`y=422`
