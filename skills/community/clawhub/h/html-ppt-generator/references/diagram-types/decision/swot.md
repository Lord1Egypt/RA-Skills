# swot · SWOT 分析

**适用：** 战略分析、企业/产品/项目的优劣势-机会-威胁四象限分析
**高度：** 280px

**结构公式：** 2×2 四格，每格多条要点文本，格间共享轴标签。

> **颜色说明：** SWOT 四象限颜色为语义固定色，不随 design-system 主题变化：
> 优势（S）= `var(--success,#10b981)` · 劣势（W）= `var(--danger,#ef4444)`
> 机会（O）= `var(--info,#3b82f6)` · 威胁（T）= `var(--warning,#f59e0b)`
> 中心标签背景 = `var(--bg,#0f172a)` · 中轴线 = `rgba(255,255,255,0.12)`

```html
<svg viewBox="0 0 700 280" style="width:100%;height:280px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 四象限背景 -->
  <!-- 左上：优势 Strengths（绿） -->
  <rect x="0"   y="0"   width="345" height="135" rx="5"
        fill="rgba(16,185,129,0.1)" stroke="rgba(16,185,129,0.35)" stroke-width="1.5"/>
  <!-- 右上：劣势 Weaknesses（红） -->
  <rect x="355" y="0"   width="345" height="135" rx="5"
        fill="rgba(239,68,68,0.1)"  stroke="rgba(239,68,68,0.35)"  stroke-width="1.5"/>
  <!-- 左下：机会 Opportunities（蓝） -->
  <rect x="0"   y="145" width="345" height="135" rx="5"
        fill="rgba(59,130,246,0.1)" stroke="rgba(59,130,246,0.35)" stroke-width="1.5"/>
  <!-- 右下：威胁 Threats（橙） -->
  <rect x="355" y="145" width="345" height="135" rx="5"
        fill="rgba(245,158,11,0.1)" stroke="rgba(245,158,11,0.35)" stroke-width="1.5"/>

  <!-- 象限标题 -->
  <text x="172" y="20" text-anchor="middle" font-size="13" font-weight="900" fill="#10b981">S · 优势</text>
  <text x="172" y="35" text-anchor="middle" font-size="8.5" fill="var(--dt)">Strengths · 内部有利因素</text>
  <text x="527" y="20" text-anchor="middle" font-size="13" font-weight="900" fill="#ef4444">W · 劣势</text>
  <text x="527" y="35" text-anchor="middle" font-size="8.5" fill="var(--dt)">Weaknesses · 内部不利因素</text>
  <text x="172" y="165" text-anchor="middle" font-size="13" font-weight="900" fill="#3b82f6">O · 机会</text>
  <text x="172" y="180" text-anchor="middle" font-size="8.5" fill="var(--dt)">Opportunities · 外部有利因素</text>
  <text x="527" y="165" text-anchor="middle" font-size="13" font-weight="900" fill="#f59e0b">T · 威胁</text>
  <text x="527" y="180" text-anchor="middle" font-size="8.5" fill="var(--dt)">Threats · 外部不利因素</text>

  <!-- S 优势要点（左上格） -->
  <text x="16" y="58"  font-size="9" fill="#6ee7b7">✓ 核心技术壁垒深厚，专利 128 项</text>
  <text x="16" y="74"  font-size="9" fill="#6ee7b7">✓ 品牌认知度行业前三，NPS 72</text>
  <text x="16" y="90"  font-size="9" fill="#6ee7b7">✓ 用户规模 2.4亿，数据护城河</text>
  <text x="16" y="106" font-size="9" fill="#6ee7b7">✓ 研发团队 800人，人效领先</text>
  <text x="16" y="122" font-size="9" fill="#6ee7b7">✓ 毛利率 68%，现金流充裕</text>

  <!-- W 劣势要点（右上格） -->
  <text x="370" y="58"  font-size="9" fill="#fca5a5">✗ 国际化布局滞后，海外营收仅 8%</text>
  <text x="370" y="74"  font-size="9" fill="#fca5a5">✗ 组织层级过多，决策响应慢</text>
  <text x="370" y="90"  font-size="9" fill="#fca5a5">✗ 硬件供应链依赖单一供应商</text>
  <text x="370" y="106" font-size="9" fill="#fca5a5">✗ AI 算法能力相比头部有差距</text>
  <text x="370" y="122" font-size="9" fill="#fca5a5">✗ 客户集中度高，TOP5 占 45%</text>

  <!-- O 机会要点（左下格） -->
  <text x="16" y="202"  font-size="9" fill="#93c5fd">→ 东南亚市场年增速 38%，蓝海</text>
  <text x="16" y="218"  font-size="9" fill="#93c5fd">→ AI 政策利好，百亿补贴窗口</text>
  <text x="16" y="234"  font-size="9" fill="#93c5fd">→ 老龄化催生银发经济新需求</text>
  <text x="16" y="250"  font-size="9" fill="#93c5fd">→ 竞争对手整合并购机会期</text>
  <text x="16" y="266"  font-size="9" fill="#93c5fd">→ 绿色转型催生新产品线空间</text>

  <!-- T 威胁要点（右下格） -->
  <text x="370" y="202"  font-size="9" fill="#fcd34d">⚡ 头部平台跨界竞争，资本雄厚</text>
  <text x="370" y="218"  font-size="9" fill="#fcd34d">⚡ 数据隐私法规趋严，合规成本↑</text>
  <text x="370" y="234"  font-size="9" fill="#fcd34d">⚡ 芯片出口管制影响研发进度</text>
  <text x="370" y="250"  font-size="9" fill="#fcd34d">⚡ 宏观需求下行，客户预算收缩</text>
  <text x="370" y="266"  font-size="9" fill="#fcd34d">⚡ 人才争夺激烈，核心团队流失</text>

  <!-- 中轴分割线 -->
  <line x1="350" y1="0"   x2="350" y2="280" stroke="rgba(255,255,255,0.12)" stroke-width="2"/>
  <line x1="0"   y1="140" x2="700" y2="140" stroke="rgba(255,255,255,0.12)" stroke-width="2"/>

  <!-- 中心标签 -->
  <rect x="318" y="124" width="64" height="32" rx="4" fill="var(--bg,#0f172a)" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
  <text x="350" y="138" text-anchor="middle" font-size="8" fill="#94a3b8">内部</text>
  <text x="350" y="150" text-anchor="middle" font-size="8" fill="#94a3b8">外部</text>
</svg>
```

**参数说明：**
- 四象限各 345×135px，格间距 10px（共用分割线）
- 每格 5 条要点，行间距 16px，从 y=58 起
- 优势=绿（#10b981），劣势=红（#ef4444），机会=蓝（#3b82f6），威胁=橙（#f59e0b）
- 中心交叉点放内部/外部轴标签框
- 要点前缀：优势=✓，劣势=✗，机会=→，威胁=⚡（增强辨识度）
