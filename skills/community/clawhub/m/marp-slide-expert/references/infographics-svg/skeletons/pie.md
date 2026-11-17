# pie — 饼图 / 环形图（占比对比）

> 整体切成几份，看份额。**每页 1–3 个饼**——一个饼讲"构成"，两三个饼并排讲"构成怎么变的"。

## 何时用 / 何时不用

| ✅ 用 | ❌ 不用 |
|---|---|
| 占比构成：收入构成、流量来源、预算分配、时间去向 | 扇区超过 5 个（先合并成"其他"） |
| 2–3 个时点/对象的构成对比（同分类、同配色） | 比绝对值大小——饼图比不出 23% vs 25%，用条形图 |
| 一两个饼，讲"大头在哪" | 份额都差不多（四个 25% 的饼没有信息量） |

**三个饼是上限。** 更多对象改用 100% 堆叠条——一排饼会让读者来回数颜色。

## 变体：饼图 Pie Chart

### 扇区画法（弧线公式）

```
角度        从 -90°（正上方）开始，顺时针；p% 对应 p × 3.6°
扇区 i      θ_start = -90° + Σ(前 i 个百分比) × 3.6
路径        M cx,cy
            L (cx + r·cos θ_start, cy + r·sin θ_start)
            A r,r 0 largeArc 1 (cx + r·cos θ_end, cy + r·sin θ_end) Z
largeArc    扇区角度 > 180° 取 1，否则 0
百分比标签  放在中角线、0.6r 处（+5px 光学修正）；< 8% 的扇区把标签移到饼外
```

单饼 r=130；双饼 r=120；三饼 r=105（本模板，cx = 190 / 510 / 830，cy = 190）。多饼对比时**分类顺序、颜色映射、图例三者全部对齐**——不一致的对比图在撒谎。

```html
<svg viewBox="0 0 1020 420" width="100%">
<path d="M190,190 L190,85 A105,105 0 1 1 157.6,289.9 Z" fill="#c0392b"/>
<path d="M190,190 L157.6,289.9 A105,105 0 0 1 105.1,128.3 Z" fill="#2c3e50"/>
<path d="M190,190 L105.1,128.3 A105,105 0 0 1 190,85 Z" fill="#95a5a6"/>
<path d="M510,190 L510,85 A105,105 0 1 1 438.1,266.5 Z" fill="#c0392b"/>
<path d="M510,190 L438.1,266.5 A105,105 0 0 1 433.5,118.1 Z" fill="#2c3e50"/>
<path d="M510,190 L433.5,118.1 A105,105 0 0 1 510,85 Z" fill="#95a5a6"/>
<path d="M830,190 L830,85 A105,105 0 1 1 730.1,222.4 Z" fill="#c0392b"/>
<path d="M830,190 L730.1,222.4 A105,105 0 0 1 768.3,105.1 Z" fill="#2c3e50"/>
<path d="M830,190 L768.3,105.1 A105,105 0 0 1 830,85 Z" fill="#95a5a6"/>
<text x="252.2" y="204.9" class="tb" fill="#ffffff" text-anchor="middle">55%</text>
<text x="130.1" y="214.5" class="tb" fill="#ffffff" text-anchor="middle">30%</text>
<text x="161.4" y="138.9" class="sm" fill="#1a1a2e" text-anchor="middle">15%</text>
<text x="568.6" y="218.2" class="tb" fill="#ffffff" text-anchor="middle">62%</text>
<text x="447" y="197" class="tb" fill="#ffffff" text-anchor="middle">25%</text>
<text x="485" y="137.2" class="sm" fill="#1a1a2e" text-anchor="middle">13%</text>
<text x="881" y="232" class="tb" fill="#ffffff" text-anchor="middle">70%</text>
<text x="770.1" y="175.5" class="tb" fill="#ffffff" text-anchor="middle">20%</text>
<text x="810.5" y="135.1" class="sm" fill="#1a1a2e" text-anchor="middle">10%</text>
<text x="190" y="64" class="tb" fill="#2c3e50" text-anchor="middle">2023</text>
<text x="510" y="64" class="tb" fill="#2c3e50" text-anchor="middle">2024</text>
<text x="830" y="64" class="tb" fill="#2c3e50" text-anchor="middle">2025</text>
<rect x="372" y="372" width="14" height="14" fill="#c0392b"/>
<text x="392" y="384" class="sm" fill="#1a1a2e">产品</text>
<rect x="484" y="372" width="14" height="14" fill="#2c3e50"/>
<text x="504" y="384" class="sm" fill="#1a1a2e">服务</text>
<rect x="596" y="372" width="14" height="14" fill="#95a5a6"/>
<text x="616" y="384" class="sm" fill="#1a1a2e">其他</text>
<text x="510" y="410" class="lbl" text-anchor="middle">同一配色跨三饼同义 · 各饼合计 100%</text>
</svg>
```

### 备选：环形 Donut（代码不渲染）

中心留白放"总量 / 首位占比"。外径 150、内径 88；扇区路径比实心饼多两段——外弧顺时针走到终点后，**向内折、沿内弧逆时针返回**：

```
M (外圆起点) A ro,ro 0 la 1 (外圆终点)      ← 外弧，顺时针
L (内圆终点) A ri,ri 0 la 0 (内圆起点) Z    ← 内弧，逆时针返回
```

```html
<svg viewBox="0 0 1020 480" width="100%">
<path d="M510,90 A150,150 0 0 1 556.4,382.7 L537.2,323.7 A88,88 0 0 0 510,152 Z" fill="#c0392b"/>
<path d="M556.4,382.7 A150,150 0 0 1 360,240 L422,240 A88,88 0 0 0 537.2,323.7 Z" fill="#2c3e50"/>
<path d="M360,240 A150,150 0 0 1 510,90 L510,152 A88,88 0 0 0 422,240 Z" fill="#95a5a6"/>
<text x="510" y="242" class="t" fill="#1a1a2e" text-anchor="middle">45%</text>
<text x="510" y="272" class="sm" fill="#7f8c8d" text-anchor="middle">产品占比</text>
<rect x="700" y="150" width="14" height="14" fill="#c0392b"/>
<text x="722" y="162" class="sm" fill="#1a1a2e">产品 45%</text>
<rect x="700" y="184" width="14" height="14" fill="#2c3e50"/>
<text x="722" y="196" class="sm" fill="#1a1a2e">服务 30%</text>
<rect x="700" y="218" width="14" height="14" fill="#95a5a6"/>
<text x="722" y="230" class="sm" fill="#1a1a2e">其他 25%</text>
<text x="510" y="446" class="lbl" text-anchor="middle">环形图：中心留给总量或首位占比</text>
</svg>
```

## 硬规则

1. **单页 1–3 个饼。** 一个讲构成；两三个同分类对比讲变化——超过三个换堆叠条。
2. **扇区 ≤ 5 个，从大到小顺时针排。** 小份额合并成"其他"，永远放最后。
3. **合计必须 100%。** 画之前先把数字加一遍——弧长就是算术，加错了肉眼能看出来。
4. **多饼对比：同分类同颜色，图例只出现一次（共享）。** 换色 = 换义，对比直接失效。
5. **百分比写数字。** 弧长给"感觉"，数值给"事实"，两者都要。
6. **不要 3D、不要爆炸分离、不要阴影。** 扇形本来就难读，特效只会更糟。
7. **< 8% 的小扇区**：标签移到饼外，或只靠图例辨认，别硬塞在扇形里。

## 文字排布

- 饼上方是标题（`.tb` 深色），多饼标题同一基线
- 扇区内百分比：`.tb` 反白；浅灰扇区改用 `.sm` 深色字（反白在浅色上读不出）
- 共享图例一行居中在饼下；注脚 `.lbl` 收底
