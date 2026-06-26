# matrix-2x2 · 2×2 矩阵

**适用：** BCG 矩阵、SWOT 分析、优先级矩阵、风险-收益矩阵、竞争定位
**高度：** 280px

**结构公式：** 四象限背景色块 + 坐标轴标签 + 数据气泡（大小=第三维度）。

```html
<svg viewBox="0 0 380 280" style="width:100%;height:280px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 四象限背景 -->
  <rect x="40" y="10"  width="155" height="120" rx="3" fill="rgba(16,185,129,0.08)"  stroke="rgba(16,185,129,0.15)"  stroke-width="1"/>
  <rect x="200" y="10" width="155" height="120" rx="3" fill="rgba(59,130,246,0.08)"  stroke="rgba(59,130,246,0.15)"  stroke-width="1"/>
  <rect x="40" y="135" width="155" height="120" rx="3" fill="rgba(245,158,11,0.08)"  stroke="rgba(245,158,11,0.15)"  stroke-width="1"/>
  <rect x="200" y="135" width="155" height="120" rx="3" fill="rgba(239,68,68,0.08)"  stroke="rgba(239,68,68,0.15)"   stroke-width="1"/>
  <!-- 象限标题 -->
  <text x="118" y="30"  text-anchor="middle" font-size="10" font-weight="700" fill="#10b981">明星产品</text>
  <text x="278" y="30"  text-anchor="middle" font-size="10" font-weight="700" fill="#3b82f6">问题产品</text>
  <text x="118" y="155" text-anchor="middle" font-size="10" font-weight="700" fill="#f59e0b">现金牛</text>
  <text x="278" y="155" text-anchor="middle" font-size="10" font-weight="700" fill="#ef4444">瘦狗产品</text>
  <!-- 象限说明 -->
  <text x="118" y="48"  text-anchor="middle" font-size="8.5" fill="var(--dt)">高增长·高份额</text>
  <text x="278" y="48"  text-anchor="middle" font-size="8.5" fill="var(--dt)">高增长·低份额</text>
  <text x="118" y="173" text-anchor="middle" font-size="8.5" fill="var(--dt)">低增长·高份额</text>
  <text x="278" y="173" text-anchor="middle" font-size="8.5" fill="var(--dt)">低增长·低份额</text>
  <!-- 数据气泡（大小=市场规模） -->
  <circle cx="110" cy="80" r="18" fill="rgba(16,185,129,0.3)"  stroke="#10b981" stroke-width="1.5"/>
  <text x="110" y="84"  text-anchor="middle" font-size="8.5" fill="#10b981">A</text>
  <circle cx="250" cy="70" r="12" fill="rgba(59,130,246,0.3)"  stroke="#3b82f6" stroke-width="1.5"/>
  <text x="250" y="74"  text-anchor="middle" font-size="8.5" fill="#3b82f6">B</text>
  <circle cx="130" cy="200" r="22" fill="rgba(245,158,11,0.3)" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="130" y="204" text-anchor="middle" font-size="8.5" fill="#f59e0b">C</text>
  <circle cx="270" cy="210" r="9"  fill="rgba(239,68,68,0.3)"  stroke="#ef4444" stroke-width="1.5"/>
  <text x="270" y="214" text-anchor="middle" font-size="8.5" fill="#ef4444">D</text>
  <!-- 坐标轴分割线 -->
  <line x1="40" y1="133" x2="355" y2="133" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
  <line x1="197" y1="10" x2="197" y2="255" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
  <!-- 坐标轴标签 -->
  <text x="118" y="268" text-anchor="middle" font-size="8.5" fill="#64748b">← 低份额</text>
  <text x="278" y="268" text-anchor="middle" font-size="8.5" fill="#64748b">高份额 →</text>
  <text x="18" y="70"  text-anchor="middle" font-size="8.5" fill="#64748b" transform="rotate(-90,18,70)">高增长</text>
  <text x="18" y="200" text-anchor="middle" font-size="8.5" fill="#64748b" transform="rotate(-90,18,200)">低增长</text>
</svg>
```

**参数说明：**
- 四象限各 155×120px，中轴线 x=197 / y=133
- 气泡半径 r = sqrt(市场规模) × 缩放系数（r 范围建议 8–25px）
- 替换为其他矩阵时：只需修改象限标题/颜色/轴标签，气泡逻辑相同
- SWOT 变体：象限名→优势/劣势/机遇/威胁，气泡→关键项目文字块
