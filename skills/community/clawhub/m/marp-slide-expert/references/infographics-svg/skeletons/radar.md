# radar — 雷达图（多维画像）

> 同一个对象在 **N 个维度**上同时看，或 2–3 个对象叠在同一组轴上对比。轴就是维度，半径就是得分——哪边鼓、哪边瘪一眼可见。

## 何时用 / 何时不用

| ✅ 用 | ❌ 不用 |
|---|---|
| 多个对象同维度对比：本品 vs 竞品、现状 vs 目标 | 单一维度内的精确排序（用条形图或表格） |
| 看"形状"：多维画像——团队技能盘、产品竞争力、个人能力盘 | 维度 > 8 个（轴挤成一团，标签放不下） |
| 维度数 5–7，各维有统一满分刻度 | 各维刻度不同（有的满分 5、有的满分 100）——先归一化再画 |

**和 [wheel 平衡轮](wheel.md) 的分工**：雷达图是**多对象**同轴叠比的折线多边形；只有一个对象、要问「短板在哪、离目标还差多少」时用平衡轮——玫瑰图式的扇形花瓣，形状和雷达一眼可分。别把平衡轮画成雷达轮廓。

## 变体：雷达图 Radar Chart

### 坐标公式（N 轴）

```
圆心 cx, cy = 510, 250        半径 R = 180
轴 i 角度     θ_i = -90° + i*(360/N)          从正上方开始，顺时针
轴顶点       (cx + R*cos θ_i,  cy + R*sin θ_i)
数值换算     r(v) = R * v / v_max             所有轴共用同一个 v_max
网格环       同一组角度上取 1/4、1/2、3/4、1 倍 R
轴标签锚点   (cx + (R+26)*cos θ_i, cy + (R+26)*sin θ_i)
             左右两侧分别 text-anchor="start" / "end"，正上/正下用 "middle"
```

N=6、R=180 的现成顶点：

| 轴 | 角度 | 顶点（R 处） | 标签示例 |
|---|---|---|---|
| 0 | -90° | 510,70 | 品牌 |
| 1 | -30° | 665.9,160 | 产品力 |
| 2 | 30° | 665.9,340 | 渠道 |
| 3 | 90° | 510,430 | 服务 |
| 4 | 150° | 354.1,340 | 技术 |
| 5 | 210° | 354.1,160 | 价格 |

```html
<svg viewBox="0 0 1020 500" width="100%">
<polygon points="510,205 549,227.5 549,272.5 510,295 471,272.5 471,227.5" fill="none" stroke="#dcdcdc" stroke-width="1"/>
<polygon points="510,160 587.9,205 587.9,295 510,340 432.1,295 432.1,205" fill="none" stroke="#dcdcdc" stroke-width="1"/>
<polygon points="510,115 626.9,182.5 626.9,317.5 510,385 393.1,317.5 393.1,182.5" fill="none" stroke="#dcdcdc" stroke-width="1"/>
<polygon points="510,70 665.9,160 665.9,340 510,430 354.1,340 354.1,160" fill="none" stroke="#b9c3cc" stroke-width="1.5"/>
<line x1="510" y1="250" x2="510" y2="70" stroke="#dcdcdc" stroke-width="1"/>
<line x1="510" y1="250" x2="665.9" y2="160" stroke="#dcdcdc" stroke-width="1"/>
<line x1="510" y1="250" x2="665.9" y2="340" stroke="#dcdcdc" stroke-width="1"/>
<line x1="510" y1="250" x2="510" y2="430" stroke="#dcdcdc" stroke-width="1"/>
<line x1="510" y1="250" x2="354.1" y2="340" stroke="#dcdcdc" stroke-width="1"/>
<line x1="510" y1="250" x2="354.1" y2="160" stroke="#dcdcdc" stroke-width="1"/>
<polygon points="510,142 650.3,169 619.1,313 510,394 432.1,295 416.5,196" fill="none" stroke="#2c3e50" stroke-width="2" stroke-dasharray="6 4"/>
<polygon points="510,88 603.5,196 634.7,322 510,340 400.9,313 385.3,178" fill="#c0392b" fill-opacity="0.18" stroke="#c0392b" stroke-width="2.5"/>
<circle cx="510" cy="88" r="4" fill="#c0392b"/>
<circle cx="603.5" cy="196" r="4" fill="#c0392b"/>
<circle cx="634.7" cy="322" r="4" fill="#c0392b"/>
<circle cx="510" cy="340" r="4" fill="#c0392b"/>
<circle cx="400.9" cy="313" r="4" fill="#c0392b"/>
<circle cx="385.3" cy="178" r="4" fill="#c0392b"/>
<text x="510" y="44" class="tb" fill="#1a1a2e" text-anchor="middle">品牌</text>
<text x="688" y="147" class="tb" fill="#1a1a2e">产品力</text>
<text x="688" y="353" class="tb" fill="#1a1a2e">渠道</text>
<text x="510" y="456" class="tb" fill="#1a1a2e" text-anchor="middle">服务</text>
<text x="332" y="353" class="tb" fill="#1a1a2e" text-anchor="end">技术</text>
<text x="332" y="147" class="tb" fill="#1a1a2e" text-anchor="end">价格</text>
<line x1="60" y1="40" x2="92" y2="40" stroke="#c0392b" stroke-width="3"/>
<text x="100" y="46" class="sm" fill="#1a1a2e">本品（实线）</text>
<line x1="60" y1="68" x2="92" y2="68" stroke="#2c3e50" stroke-width="2" stroke-dasharray="6 4"/>
<text x="100" y="74" class="sm" fill="#1a1a2e">竞品（虚线）</text>
<text x="510" y="488" class="lbl" text-anchor="middle">各维满分 5 · 数据为示意</text>
</svg>
```

## 硬规则

1. **轴数 5–7。** 6 最稳。少于 5 形状失去意义，多于 7 标签打架——改分组矩阵。
2. **所有轴同一套刻度。** 画之前先归一化；刻度值写进注脚（`各维满分 5`），否则读者无法读数。
3. **系列 ≤ 3。** 第一个用半透明填充 + 实线，后面只描边：第二个虚线、第三个点线。三层填充叠起来就成一团泥。
4. **顶点加小圆点**（`r=4`）。读者要能沿轴读出具体值，没有圆点的折线会滑过去。
5. **顶点半径 = R × 数值 / 满分，不许手调。** 为了让形状好看挪顶点，比没有图更糟。
6. **轴必须独立。** 两个高度相关的维度会互相放大、形状失真；不独立就换 [matrix-quadrant](matrix-quadrant.md)。

## 变体

| 变体 | 改法 | 用在 |
|---|---|---|
| 单系列 | 只画实线 + 填充，删图例 | 单对象画像 |
| 现状 vs 目标 | 现状实线填充、目标虚线不填充 | 差距分析——和平衡轮互补，平衡轮更细 |
| 归一化双轴 | 先把不同量纲换算成同一满分，再套公式 | 维度天然不同刻度时（收入 / 满意度 / 覆盖率） |

## 文字排布

- 轴标签：`.tb` 深色 `#1a1a2e`，锚点按角度选 `start` / `end` / `middle`，别压在轴线上
- 图例：左上角两行，示例线与数据线**同色同线型**，`.sm` 文字
- 注脚：`.lbl` 居中，"各维满分 X · 数据为示意"
