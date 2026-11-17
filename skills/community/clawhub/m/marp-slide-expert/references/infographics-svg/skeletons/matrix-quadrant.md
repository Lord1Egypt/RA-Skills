# matrix-quadrant — 双维矩阵骨架

> 两条**相互独立**的轴交叉，把平面分成四个语义截然不同的区域，每个区域代表两个维度的一种组合。

## 何时用 / 何时不用

| ✅ 用 | ❌ 不用 |
|---|---|
| 恰好两个独立维度交叉分类 | 两个维度其实相关（那不是矩阵，是同一条轴切两刀） |
| 战略定位（BCG / Gartner 象限） | 维度超过 2 个（用 [structure-block](structure-block.md) 的对比矩阵） |
| 优先级排序（紧急 × 重要） | 维度是连续但不需要分象限（用 [structure-block](structure-block.md) 的散点+列表） |
| 利益相关方（权力 × 利益）、风险（概率 × 影响） | 需要表达流转关系（矩阵没有连线） |

**独立性检验**：如果 X 轴高的时候 Y 轴必然也高，那这两个轴不是独立的，象限会退化成一条对角线带，四个区域里有两个永远是空的。**画之前先想清楚两个轴是不是真的独立。**

---

## 硬规则

1. **两个轴必须相互独立且连续。** 违反这一条，矩阵就没有意义。
2. **中心十字必须视觉突出。** 两条轴的交点是整张图的锚点——它是分类系统本身，不是一条辅助线。
3. **每个象限都要有名字。** 象限名本身就是分析结论（"明星业务" / "现金牛" / "问题儿童" / "瘦狗"）。没有名字的象限只是四个空格子。
4. **位置必须反映真实数值。** 有数据时，值高的必须离原点更远，值相同的必须在同一高度/同一横坐标。**不要凭感觉摆**——这是矩阵唯一会骗人的地方。
5. **四个象限要有可区分的底色**，但要极淡（`#f2f7fa` / `#fdecea` 那一档），只有要强调的那个象限才给重色。

---

## 变体：双维矩阵 2×2

### 坐标公式

```
原点 (ox, oy) = (120, 470)          ← 左下角，Y 轴往上、底边线在这
象限宽 w      = 375
象限高 h      = 200
分割线        x = ox + w      = 495
              y = oy - h      = 270
X 轴线        (120,470) → (895,470)
Y 轴线        (120,470) → (120,55)
X 轴标题      y = 505           ← 超出安全线，必须配 _class: diagram 藏 footer
Y 轴标题      rotate(-90, 60, 270)
viewBox       0 0 1020 530
```

```html
<svg viewBox="0 0 1020 530" width="100%">
<defs>
<marker id="a3x" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#1a1a2e"/></marker>
<marker id="a3y" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#1a1a2e"/></marker>
</defs>
<rect x="120" y="70"  width="375" height="200" fill="#f2f7fa"/>
<rect x="495" y="70"  width="375" height="200" fill="#fdecea"/>
<rect x="120" y="270" width="375" height="200" fill="#f7f7f7"/>
<rect x="495" y="270" width="375" height="200" fill="#fdf6e8"/>
<line x1="120" y1="470" x2="895" y2="470" stroke="#1a1a2e" stroke-width="2" marker-end="url(#a3x)"/>
<line x1="120" y1="470" x2="120" y2="55"  stroke="#1a1a2e" stroke-width="2" marker-end="url(#a3y)"/>
<line x1="495" y1="70" x2="495" y2="470" stroke="#ffffff" stroke-width="3"/>
<line x1="120" y1="270" x2="870" y2="270" stroke="#ffffff" stroke-width="3"/>
<text x="500" y="505" class="sm" fill="#1a1a2e" text-anchor="middle" font-weight="700">相对市场份额 →</text>
<text x="60" y="270" class="sm" fill="#1a1a2e" text-anchor="middle" font-weight="700" transform="rotate(-90,60,270)">相对增长率 →</text>
<text x="140" y="98"  class="qt" fill="#7f8c8d">问题儿童</text>
<text x="140" y="120" class="sm" fill="#95a5a6">高增长 · 低份额</text>
<text x="515" y="98"  class="qt" fill="#c0392b">明星业务</text>
<text x="515" y="120" class="sm" fill="#e74c3c">高增长 · 高份额</text>
<text x="140" y="298"  class="qt" fill="#95a5a6">瘦狗业务</text>
<text x="140" y="320" class="sm" fill="#b2bec3">低增长 · 低份额</text>
<text x="515" y="298"  class="qt" fill="#2c3e50">现金牛</text>
<text x="515" y="320" class="sm" fill="#5d7d95">低增长 · 高份额</text>
<circle cx="700" cy="200" r="26" fill="#c0392b" opacity=".85"/>
<text x="735" y="206" class="sm" fill="#1a1a2e" font-weight="700">AI 助手</text>
<text x="880" y="30" class="lbl" text-anchor="end">气泡大小 = 收入贡献</text>
</svg>
```

### 要点

- 象限底色**极淡**。只有要强调的象限才给红调。文字用重色，**气泡才是主体**。
- 象限分隔线用**白色 3px**——灰色在浅底上显脏。
- 气泡标签放**右侧** `cx + r + 9`，不要压在圆上。
- 旋转的 Y 轴标题，`transform="rotate(-90,x,y)"` 的中心必须和文本的 `x,y` **完全一致**，否则飞出画布。
- X 轴标题在 `y=505`，超出底部安全线 —— **这一页必须加 `<!-- _class: diagram -->`**。

## 坐标换算（按数值定位）

给定两个维度值 `vx ∈ [0,1]`、`vy ∈ [0,1]`（先归一化到 0–1），点在象限内的位置：

```
px = ox + vx * (2*w)      象限区总宽 750
py = oy - vy * (2*h)      象限区总高 400
```

内部留白：在计算结果上加 `px += 40`、`py -= 40`，避免点贴到象限边缘或坐标轴上。

## 变体

| 变体 | 说明 | 什么时候用 |
|---|---|---|
| **Strategic** 战略象限 | 具名象限 + 定位的气泡/圆点 | BCG、Gartner、竞争格局 |
| **Decision** 决策象限 | 象限名本身就是行动指令（加投/攻坚/收割/放弃），象限内列条目 | 优先级排序、风险矩阵 |
| **Spectrum** 连续谱 | 不分象限边界，只有两条轴和散点 | 政治光谱、人格定位 |

**Decision 变体**：象限名要给**行动指令**（"加投""攻坚""收割""放弃"），不是只写名字。象限内改成文字列表而不是气泡。

## 连线

**矩阵没有连线。** 元素之间的关系由**空间位置**表达，不画关系线。需要表达关系就说明这个骨架选错了。

（唯一的例外：引导线。从点拉到轴上的细虚线，标出该点的具体读数。`stroke="#dcdcdc" stroke-dasharray="3 3" stroke-width="1"`）

## 文字排布

- 象限名 `.qt`（20px 粗体），放象限**内角**（左上象限的右下角，或右上象限的左下角——都朝中心，读起来聚拢）
- 象限说明 `.sm`，紧跟象限名下方 `dy=22`
- 气泡标签 `.sm` 常规字重
- 右上角注脚 `.lbl`，`y=30`（图顶安全区）
- 轴标题 `.sm` + `font-weight="700"`
