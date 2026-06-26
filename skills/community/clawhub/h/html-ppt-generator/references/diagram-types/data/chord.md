# chord · 弦图（关系矩阵）

**适用：** 多方关系强度、交叉流量、部门协作频率、双向依赖分析
**高度：** 260px

**结构公式：** 圆形外圈 N 个弧段（各方）+ 内部 bezier 曲线（关系强度，宽度=流量大小）。

```html
<svg viewBox="0 0 340 260" style="width:100%;height:260px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 圆心 cx=170, cy=130, 外圆R=105, 节点弧宽12 -->

  <!-- 外圈弧段（6个方）：每方约50°，间距10° -->
  <!-- 方A（蓝，0°~50°）-->
  <path d="M170,25 A105,105 0 0,1 252,55" fill="none" stroke="#3b82f6" stroke-width="12" stroke-linecap="round"/>
  <!-- 方B（绿，60°~110°）-->
  <path d="M261,68 A105,105 0 0,1 261,192" fill="none" stroke="#10b981" stroke-width="12" stroke-linecap="round"/>
  <!-- 方C（橙，120°~170°）-->
  <path d="M252,205 A105,105 0 0,1 170,235" fill="none" stroke="#f59e0b" stroke-width="12" stroke-linecap="round"/>
  <!-- 方D（紫，180°~230°）-->
  <path d="M157,234 A105,105 0 0,1 79,195" fill="none" stroke="#8b5cf6" stroke-width="12" stroke-linecap="round"/>
  <!-- 方E（红，240°~290°）-->
  <path d="M70,180 A105,105 0 0,1 70,60" fill="none" stroke="#ef4444" stroke-width="12" stroke-linecap="round"/>
  <!-- 方F（青，300°~350°）-->
  <path d="M79,46 A105,105 0 0,1 157,26" fill="none" stroke="#06b6d4" stroke-width="12" stroke-linecap="round"/>

  <!-- 弦（内部 bezier 关系线，宽度=关系强度） -->
  <!-- A-B（强，蓝绿混合）-->
  <path d="M252,55 C170,130 170,130 261,80" fill="none" stroke="#3b82f6" stroke-width="8" opacity="0.3"/>
  <!-- A-C（中）-->
  <path d="M240,40 C170,130 170,130 220,215" fill="none" stroke="#3b82f6" stroke-width="5" opacity="0.25"/>
  <!-- A-E（弱）-->
  <path d="M195,26 C170,130 170,130 72,72" fill="none" stroke="#3b82f6" stroke-width="3" opacity="0.2"/>
  <!-- B-D（强）-->
  <path d="M261,120 C170,130 170,130 88,205" fill="none" stroke="#10b981" stroke-width="7" opacity="0.3"/>
  <!-- B-F（中）-->
  <path d="M261,160 C170,130 170,130 140,27" fill="none" stroke="#10b981" stroke-width="4" opacity="0.25"/>
  <!-- C-E（强）-->
  <path d="M210,225 C170,130 170,130 70,120" fill="none" stroke="#f59e0b" stroke-width="9" opacity="0.28"/>
  <!-- D-F（中）-->
  <path d="M88,180 C170,130 170,130 120,27" fill="none" stroke="#8b5cf6" stroke-width="5" opacity="0.25"/>
  <!-- E-F（弱）-->
  <path d="M70,80 C170,130 170,130 90,36" fill="none" stroke="#ef4444" stroke-width="3" opacity="0.2"/>

  <!-- 方标签 -->
  <text x="210" y="22"  text-anchor="middle" font-size="9" fill="#93c5fd" font-weight="700">部门A</text>
  <text x="284" y="130" text-anchor="start"  font-size="9" fill="#6ee7b7" font-weight="700">部门B</text>
  <text x="210" y="252" text-anchor="middle" font-size="9" fill="#fcd34d" font-weight="700">部门C</text>
  <text x="78"  y="252" text-anchor="middle" font-size="9" fill="#c4b5fd" font-weight="700">部门D</text>
  <text x="18"  y="130" text-anchor="end"    font-size="9" fill="#fca5a5" font-weight="700">部门E</text>
  <text x="78"  y="22"  text-anchor="middle" font-size="9" fill="#67e8f9" font-weight="700">部门F</text>

  <!-- 中心圆（遮盖交叉线中心杂乱区）-->
  <circle cx="170" cy="130" r="32" fill="var(--bg,#0f172a)" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  <text x="170" y="126" text-anchor="middle" font-size="8.5" fill="var(--dt)">关系</text>
  <text x="170" y="138" text-anchor="middle" font-size="8.5" fill="var(--dt)">强度图</text>

  <!-- 图例 -->
  <line x1="10" y1="246" x2="30" y2="246" stroke="#475569" stroke-width="8" stroke-linecap="round" opacity="0.4"/>
  <text x="35" y="249" font-size="7.5" fill="#64748b">强关联</text>
  <line x1="90" y1="246" x2="110" y2="246" stroke="#475569" stroke-width="4" stroke-linecap="round" opacity="0.3"/>
  <text x="115" y="249" font-size="7.5" fill="#64748b">中等</text>
  <line x1="160" y1="246" x2="180" y2="246" stroke="#475569" stroke-width="2" stroke-linecap="round" opacity="0.25"/>
  <text x="185" y="249" font-size="7.5" fill="#64748b">弱关联</text>
</svg>
```

**参数说明：**
- 外圈弧段：`<path d="M x1,y1 A R,R 0 large-arc,sweep x2,y2"/>` stroke-width=12
- 弦（关系线）：bezier 两端点为对应弧段中点，控制点均为圆心（170,130）
- stroke-width 对应关系强度：强=8–10，中=4–6，弱=2–3
- stroke opacity=0.2–0.3；弦颜色跟随来源节点颜色
- 圆心覆盖圆 r≈32 遮住交叉杂乱区，放置图名
- 6个方向坐标（R=105）：0°(170,25), 60°(261,68~192), 120°(252,205), 180°(170,235), 240°(79,195~46)
