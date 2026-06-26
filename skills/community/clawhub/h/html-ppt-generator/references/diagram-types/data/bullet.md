# bullet · Bullet 子弹图

**适用：** KPI 目标对比、实际 vs 计划、多指标达成率
**高度：** 26px/条，多条叠加时 = 条数 × 30px

**结构公式：** 三层叠加水平条——背景区间（浅→深三段）+ 实际值条 + 目标竖线。

```html
<!-- 单条 Bullet Chart，高度 26px，可叠加多条 -->
<svg viewBox="0 0 480 26" style="width:100%;height:26px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 标签 -->
  <text x="0" y="17" font-size="9.5" font-weight="600" fill="var(--mt)">销售额</text>
  <!-- 背景区间：差/良/优（三段透明度递增） -->
  <rect x="65" y="6" width="380" height="14" rx="2" fill="rgba(255,255,255,0.04)"/>
  <rect x="65" y="6" width="228" height="14" rx="2" fill="rgba(255,255,255,0.07)"/>
  <rect x="65" y="6" width="152" height="14" rx="2" fill="rgba(255,255,255,0.11)"/>
  <!-- 实际值（80%） -->
  <rect x="65" y="9" width="304" height="8" rx="1" fill="var(--p)"/>
  <!-- 目标线（90%） -->
  <rect x="407" y="4" width="3" height="18" rx="1" fill="#f59e0b"/>
  <!-- 数值标签 -->
  <text x="373" y="17" font-size="8.5" fill="var(--mt)">80%</text>
  <text x="410" y="17" font-size="8.5" fill="#f59e0b">目标90%</text>
</svg>
```

**多指标叠加示例（3条，78px）：**
```html
<svg viewBox="0 0 480 78" style="width:100%;height:78px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 条1：销售额 80% -->
  <text x="0" y="17" font-size="9.5" font-weight="600" fill="var(--mt)">销售额</text>
  <rect x="65" y="6" width="380" height="14" rx="2" fill="rgba(255,255,255,0.04)"/>
  <rect x="65" y="6" width="228" height="14" rx="2" fill="rgba(255,255,255,0.07)"/>
  <rect x="65" y="9" width="304" height="8" rx="1" fill="var(--p)"/>
  <rect x="407" y="4" width="3" height="18" rx="1" fill="#f59e0b"/>
  <text x="373" y="17" font-size="8.5" fill="var(--mt)">80%</text>
  <!-- 条2：利润率 65% -->
  <text x="0" y="43" font-size="9.5" font-weight="600" fill="var(--mt)">利润率</text>
  <rect x="65" y="32" width="380" height="14" rx="2" fill="rgba(255,255,255,0.04)"/>
  <rect x="65" y="32" width="190" height="14" rx="2" fill="rgba(255,255,255,0.07)"/>
  <rect x="65" y="35" width="247" height="8" rx="1" fill="#10b981"/>
  <rect x="342" y="30" width="3" height="18" rx="1" fill="#f59e0b"/>
  <text x="255" y="43" font-size="8.5" fill="var(--mt)">65%</text>
  <!-- 条3：客户满意度 92% -->
  <text x="0" y="69" font-size="9.5" font-weight="600" fill="var(--mt)">满意度</text>
  <rect x="65" y="58" width="380" height="14" rx="2" fill="rgba(255,255,255,0.04)"/>
  <rect x="65" y="58" width="285" height="14" rx="2" fill="rgba(255,255,255,0.07)"/>
  <rect x="65" y="61" width="350" height="8" rx="1" fill="#8b5cf6"/>
  <rect x="380" y="56" width="3" height="18" rx="1" fill="#f59e0b"/>
  <text x="358" y="69" font-size="8.5" fill="var(--mt)">92%</text>
</svg>
```

**参数说明：**
- 标签列宽 60px（x=0~60），图表区 x=65 起，总宽 380px = 100%
- 实际值宽 = 380 × 实际%
- 目标线 x = 65 + 380 × 目标%，宽 3px，高 18px（超出图表上下各 2px）
- 背景三段区间建议比例：差区 0~40%，良区 40~75%，优区 75~100%
