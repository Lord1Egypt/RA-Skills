# pyramid · 金字塔图

**适用：** 组织层级、需求层次、技术栈依赖、战略优先级
**高度：** 200px（4层）

**结构公式：** N 层梯形叠加，从顶（最小/最高优先）到底（最大/基础层），同色系递减 opacity。

```html
<svg viewBox="0 0 400 200" style="width:100%;height:200px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 第1层（顶，最重要） -->
  <polygon points="200,8 260,58 140,58" fill="var(--p)" opacity="0.9"/>
  <text x="200" y="40" text-anchor="middle" font-size="9.5" font-weight="700" fill="#fff">战略层</text>
  <!-- 第2层 -->
  <polygon points="140,61 260,61 300,108 100,108" fill="var(--p)" opacity="0.65"/>
  <text x="200" y="90" text-anchor="middle" font-size="9.5" font-weight="600" fill="#fff">管理层</text>
  <!-- 第3层 -->
  <polygon points="100,111 300,111 348,160 52,160" fill="var(--p)" opacity="0.4"/>
  <text x="200" y="141" text-anchor="middle" font-size="9.5" font-weight="600" fill="var(--t)">执行层</text>
  <!-- 第4层（底，基础） -->
  <polygon points="52,163 348,163 380,196 20,196" fill="var(--p)" opacity="0.2"/>
  <text x="200" y="184" text-anchor="middle" font-size="9.5" font-weight="600" fill="var(--t)">基础设施</text>
  <!-- 右侧标注（可选） -->
  <line x1="350" y1="33" x2="390" y2="33" stroke="rgba(255,255,255,0.2)" stroke-width="0.8"/>
  <text x="392" y="37" font-size="8.5" fill="var(--dt)">5%</text>
  <line x1="305" y1="84" x2="390" y2="84" stroke="rgba(255,255,255,0.2)" stroke-width="0.8"/>
  <text x="392" y="88" font-size="8.5" fill="var(--dt)">20%</text>
  <line x1="350" y1="135" x2="390" y2="135" stroke="rgba(255,255,255,0.2)" stroke-width="0.8"/>
  <text x="392" y="139" font-size="8.5" fill="var(--dt)">35%</text>
  <line x1="382" y1="179" x2="390" y2="179" stroke="rgba(255,255,255,0.2)" stroke-width="0.8"/>
  <text x="392" y="183" font-size="8.5" fill="var(--dt)">40%</text>
</svg>
```

**参数说明：**
- 层数 N=4 时，每层高约 48px；N=3 时每层约 64px
- opacity 从顶到底：0.9 → 0.65 → 0.4 → 0.2（步长约 0.23）
- 每层梯形顶边比底层梯形窄 60–80px（每侧收窄 30–40px）
- 右侧引线 + 标注适合显示百分比/人数，可选是否显示
- 若顶层太小（高<35px），文字改用 font-size:8px 或移到右侧
