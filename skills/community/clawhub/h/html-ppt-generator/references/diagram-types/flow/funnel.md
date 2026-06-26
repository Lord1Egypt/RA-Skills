# funnel · 漏斗图

**适用：** 转化率分析、用户路径、销售漏斗、流失分析
**高度：** 160–200px（4–5层）

**结构公式：** N 个梯形叠加，每层比上层窄（宽度 = 总宽 × 该层比例），颜色渐变，标注数值和转化率。

**梯形坐标计算公式：**
```
每层梯形（polygon）坐标：
  层 i 顶边宽 W_top = 总宽 × ratio_i
  层 i 底边宽 W_bot = 总宽 × ratio_(i+1)
  x_top_left  = (总宽 - W_top) / 2 + offset_x
  x_top_right = (总宽 + W_top) / 2 + offset_x
  x_bot_left  = (总宽 - W_bot) / 2 + offset_x
  x_bot_right = (总宽 + W_bot) / 2 + offset_x
  y_top = i × 层高，y_bot = (i+1) × 层高
  points = "x_tl,y_top x_tr,y_top x_br,y_bot x_bl,y_bot"
```

```html
<svg viewBox="0 0 600 200" style="width:100%;height:200px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 层1：曝光 100% → 宽560 -->
  <polygon points="20,0 580,0 540,38 60,38" fill="rgba(59,130,246,0.7)"/>
  <text x="300" y="24" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">曝光量 · 100,000</text>
  <!-- 层2：点击 54% → 宽302 -->
  <polygon points="60,40 540,40 460,78 140,78" fill="rgba(139,92,246,0.7)"/>
  <text x="300" y="64" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">点击量 · 54,000 · 54%</text>
  <!-- 层3：注册 22% → 宽123 -->
  <polygon points="140,80 460,80 400,118 200,118" fill="rgba(245,158,11,0.75)"/>
  <text x="300" y="104" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">注册量 · 22,000 · 41%</text>
  <!-- 层4：付费 8% → 宽45 -->
  <polygon points="200,120 400,120 355,158 245,158" fill="rgba(239,68,68,0.75)"/>
  <text x="300" y="144" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">付费量 · 8,000 · 36%</text>
  <!-- 层5：复购 3% → 宽17 -->
  <polygon points="245,160 355,160 330,195 270,195" fill="rgba(16,185,129,0.8)"/>
  <text x="300" y="182" text-anchor="middle" font-size="9" font-weight="700" fill="#fff">复购 · 3,000 · 38%</text>
  <!-- 右侧转化率标注 -->
  <text x="556" y="24" font-size="8" fill="#64748b">100%</text>
  <text x="556" y="64" font-size="8" fill="#64748b">54%↓</text>
  <text x="556" y="104" font-size="8" fill="#64748b">22%↓</text>
  <text x="556" y="144" font-size="8" fill="#64748b">8%↓</text>
  <text x="556" y="182" font-size="8" fill="#64748b">3%↓</text>
</svg>
```

**参数说明：**
- 颜色从蓝→紫→黄→红→绿，视觉引导由宽到窄的收缩感
- 每层高 38–40px，层间留 2px 间隙避免颜色混叠
- 右侧标注绝对转化率；层内文字标注相对转化率（较上层的%）
- 若层数≤3，每层可适当加高至 55px 以增强可读性
