# evidence — 论证骨架（图尔敏）

> 主张靠什么支撑。三个必需件（Claim / Grounds / Warrant）+ 三个可选件（Backing / Qualifier / Rebuttal）。

## 何时用 / 何时不用

| ✅ 用 | ❌ 不用 |
|---|---|
| 论文论点辩护、政策论证、说服性写作 | 只是罗列事实，没有推理链（用 [structure-block](structure-block.md)） |
| 逻辑推理分析、辩论准备 | 观点 vs 观点的对立（用 [structure-block](structure-block.md) 变体 C 的二元对比） |
| 决策依据拆解 | 时间演进（用 [lanes](lanes.md)） |

---

## ⚠️ 箭头方向（最容易画反的地方）

**所有箭头都表示「逻辑支撑」，必须指向被支撑的一方。视觉流向永远是自下而上，像一座楼。**

| 连线 | 方向 | 标签 |
|---|---|---|
| Grounds → Warrant | **向上** ↑ | 「所以」 |
| Warrant → Claim | **向上** ↑ | 「因为」 |
| Backing → Warrant | 侧向**向内** → | 「依据是」 |
| Rebuttal → Claim | 侧向**向内** → | 「除非」 |
| Qualifier → Claim | 侧向**向内** → | 「大概」 |

**绝对不要画成从 Claim 向下指到 Grounds。** 那把论证逻辑整个反过来了——图会读成「结论导致了证据」，这在逻辑上是错的，而且大多数人第一眼扫过去不会发现。

---

## 变体：图尔敏论证 Toulmin

### 坐标公式（Full 变体）

```
中心 cx        = 510
Claim 块       x=400 y=40  w=220 h=64   rx=6      中心 510
Grounds 块     x=380 y=400 w=260 h=72   rx=6      中心 510
Warrant 菱形   中心 (510, 250)，半宽 150，半高 62   ← 必须够大才放得下 6 字标签
Backing 块     x=740 y=300 w=220 h=72   rx=6      中心 850
Qualifier 标签  x=960 y=120  text-anchor="end"     （右上，浅灰文字）
Rebuttal 块    x=60  y=108 w=220 h=64   rx=6      中心 170
viewBox        0 0 1020 520
```

**三个 marker 对应三种线色**——线的 `stroke` 和箭头的 `fill` 必须一致，否则会出现深线配红箭头那种接缝。

```html
<svg viewBox="0 0 1020 520" width="100%">
<defs>
<marker id="a1" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#1a1a2e"/></marker>
<marker id="a2" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#e74c3c"/></marker>
<marker id="a3" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#7f8c8d"/></marker>
</defs>
<rect x="400" y="40"  width="220" height="64" rx="6" fill="#c0392b"/>
<text x="510" y="80"  class="t"  fill="#ffffff" text-anchor="middle">应当全面推行</text>
<rect x="60"  y="108" width="220" height="64" rx="6" fill="#fdecea" stroke="#e74c3c" stroke-width="1.5" stroke-dasharray="5 4"/>
<text x="170" y="148" class="sm" fill="#1a1a2e" text-anchor="middle">反例：小团队不适用</text>
<text x="960" y="120" class="sm" fill="#7f8c8d" text-anchor="end">限定：大部分场景</text>
<path d="M280,140 H360 V100 H400" fill="none" stroke="#e74c3c" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#a2)"/>
<path d="M510,400 V316" fill="none" stroke="#1a1a2e" stroke-width="2.5" marker-end="url(#a1)"/>
<text x="528" y="360" class="sm" fill="#7f8c8d">所以</text>
<path d="M510,104 V184" fill="none" stroke="#1a1a2e" stroke-width="2.5" marker-end="url(#a1)"/>
<text x="528" y="150" class="sm" fill="#7f8c8d">因为</text>
<path d="M510,188 L660,250 L510,312 L360,250 Z" fill="#2c3e50"/>
<text x="510" y="257" class="sm" fill="#ffffff" text-anchor="middle">试点数据充分</text>
<path d="M740,336 H706 Q666,336 666,300 Q666,268 666,252" fill="none" stroke="#7f8c8d" stroke-width="2" marker-end="url(#a3)"/>
<text x="690" y="286" class="sm" fill="#7f8c8d">依据</text>
<rect x="740" y="300" width="220" height="72" rx="6" fill="#eef1f4"/>
<text x="850" y="332" class="sm" fill="#1a1a2e" text-anchor="middle">第三方评估报告</text>
<text x="850" y="358" class="lbl" text-anchor="middle">（2025 抽样 2.4 万）</text>
<rect x="380" y="400" width="260" height="72" rx="6" fill="#2c3e50"/>
<text x="510" y="432" class="sm" fill="#ffffff" text-anchor="middle">6 个部门试点 9 个月</text>
<text x="510" y="456" class="lbl" fill="#cccccc" text-anchor="middle">效率 +32%，投入 -18%</text>
</svg>
```

---

## 硬规则

1. **箭头一律向上/向内**，理由见上。
2. **Claim 最大最深**（`.t` 26px + `#c0392b`），Grounds 次之（`.sm` + `#2c3e50`），其余元件更小更浅。
3. **Warrant 用菱形**——它是「推理」不是「事实」，形状本身就在说这件事。用矩形会把它和 Grounds 混为一谈。
4. **Rebuttal 视觉上要和主干区分**：虚线边框 + 浅底，别让它看起来像另一个 Grounds。
5. **Qualifier 不画框**，只放一行浅灰文字 + 一条细虚线。限定词是修饰，不是论点。

## 变体

| 变体 | 包含 | 用在 |
|---|---|---|
| **Simple** | Claim + Warrant + Grounds | 快速论证，三层竖排即可（`y=60 / 220 / 380`） |
| **Full** | 全部 6 件 | 正式论证、论文、辩论 |

**Simple 变体的最小形态**：三块横条 + 两条向上箭头，viewBox 高度 440 就够。

---

## 文字排布

- Claim `.t`，块内居中 `y = 块顶 + 块高/2 + 10`（26px）
- Grounds 两行时：主行 `y = 块顶 + 32`，副行 `y = 块顶 + 56`
- Warrant 菱形内文字 `y = 菱形中心 + 8`（15px）
- 箭头标签（所以/因为）放在箭头**右侧** `x = 线x + 20`，不要压在线上
- 顶部总括 `.sm` 灰色 `y=26`

## 连线

| 连线 | 画法 |
|---|---|
| Grounds → Warrant | 实线 `stroke-width="2.5"` + 向上箭头，`#1a1a2e` |
| Warrant → Claim | 实线 `stroke-width="2.5"` + 向上箭头，`#1a1a2e` |
| Backing → Warrant | 实线 `stroke-width="2"` + 向内箭头，曲线（`Q`）避开 Claim |
| Rebuttal → Claim | 虚线 `stroke-dasharray="5 4"` + 向内箭头，`#e74c3c` |
| Qualifier → Claim | 虚线 `stroke-width="1.5"` + 细箭头，灰色 |
