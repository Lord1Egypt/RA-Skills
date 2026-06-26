# layered · 分层架构图

**适用：** 系统组件/微服务/网络拓扑/技术栈分层
**高度：** 220px（3层）；每增/减一层 ±58px

**结构公式：** N 个水平色带从上到下，每带内左右排列组件方块，带间连接箭头。

```html
<svg viewBox="0 0 940 220" style="width:100%;height:220px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="la-arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#64748b"/>
    </marker>
  </defs>
  <!-- 层1：表现层 -->
  <rect x="0" y="0" width="940" height="52" rx="4" fill="rgba(59,130,246,0.1)" stroke="rgba(59,130,246,0.3)" stroke-width="1"/>
  <text x="10" y="14" font-size="9" font-weight="700" fill="#3b82f6">PRESENTATION</text>
  <rect x="120" y="8" width="140" height="34" rx="4" fill="rgba(59,130,246,0.2)" stroke="rgba(59,130,246,0.4)" stroke-width="1"/>
  <text x="190" y="29" text-anchor="middle" font-size="10" font-weight="600" fill="#93c5fd">Web App</text>
  <rect x="280" y="8" width="140" height="34" rx="4" fill="rgba(59,130,246,0.2)" stroke="rgba(59,130,246,0.4)" stroke-width="1"/>
  <text x="350" y="29" text-anchor="middle" font-size="10" font-weight="600" fill="#93c5fd">Mobile App</text>
  <rect x="440" y="8" width="140" height="34" rx="4" fill="rgba(59,130,246,0.2)" stroke="rgba(59,130,246,0.4)" stroke-width="1"/>
  <text x="510" y="29" text-anchor="middle" font-size="10" font-weight="600" fill="#93c5fd">Admin Portal</text>
  <!-- 层2：应用层 -->
  <rect x="0" y="58" width="940" height="52" rx="4" fill="rgba(139,92,246,0.1)" stroke="rgba(139,92,246,0.3)" stroke-width="1"/>
  <text x="10" y="72" font-size="9" font-weight="700" fill="#8b5cf6">APPLICATION</text>
  <rect x="120" y="66" width="140" height="34" rx="4" fill="rgba(139,92,246,0.2)" stroke="rgba(139,92,246,0.4)" stroke-width="1"/>
  <text x="190" y="87" text-anchor="middle" font-size="10" font-weight="600" fill="#c4b5fd">API Gateway</text>
  <rect x="280" y="66" width="140" height="34" rx="4" fill="rgba(139,92,246,0.2)" stroke="rgba(139,92,246,0.4)" stroke-width="1"/>
  <text x="350" y="87" text-anchor="middle" font-size="10" font-weight="600" fill="#c4b5fd">Auth Service</text>
  <rect x="440" y="66" width="140" height="34" rx="4" fill="rgba(139,92,246,0.2)" stroke="rgba(139,92,246,0.4)" stroke-width="1"/>
  <text x="510" y="87" text-anchor="middle" font-size="10" font-weight="600" fill="#c4b5fd">Business Logic</text>
  <rect x="600" y="66" width="140" height="34" rx="4" fill="rgba(139,92,246,0.2)" stroke="rgba(139,92,246,0.4)" stroke-width="1"/>
  <text x="670" y="87" text-anchor="middle" font-size="10" font-weight="600" fill="#c4b5fd">Message Queue</text>
  <!-- 层3：数据层 -->
  <rect x="0" y="116" width="940" height="52" rx="4" fill="rgba(6,182,212,0.1)" stroke="rgba(6,182,212,0.3)" stroke-width="1"/>
  <text x="10" y="130" font-size="9" font-weight="700" fill="#06b6d4">DATA</text>
  <rect x="120" y="124" width="140" height="34" rx="4" fill="rgba(6,182,212,0.2)" stroke="rgba(6,182,212,0.4)" stroke-width="1"/>
  <text x="190" y="145" text-anchor="middle" font-size="10" font-weight="600" fill="#67e8f9">PostgreSQL</text>
  <rect x="280" y="124" width="140" height="34" rx="4" fill="rgba(6,182,212,0.2)" stroke="rgba(6,182,212,0.4)" stroke-width="1"/>
  <text x="350" y="145" text-anchor="middle" font-size="10" font-weight="600" fill="#67e8f9">Redis Cache</text>
  <rect x="440" y="124" width="140" height="34" rx="4" fill="rgba(6,182,212,0.2)" stroke="rgba(6,182,212,0.4)" stroke-width="1"/>
  <text x="510" y="145" text-anchor="middle" font-size="10" font-weight="600" fill="#67e8f9">Object Storage</text>
  <!-- 层间箭头 -->
  <line x1="190" y1="42" x2="190" y2="66" stroke="#64748b" stroke-width="1.5" marker-end="url(#la-arr)"/>
  <line x1="350" y1="42" x2="350" y2="66" stroke="#64748b" stroke-width="1.5" marker-end="url(#la-arr)"/>
  <line x1="510" y1="42" x2="510" y2="66" stroke="#64748b" stroke-width="1.5" marker-end="url(#la-arr)"/>
  <line x1="190" y1="100" x2="190" y2="124" stroke="#64748b" stroke-width="1.5" marker-end="url(#la-arr)"/>
  <line x1="350" y1="100" x2="350" y2="124" stroke="#64748b" stroke-width="1.5" marker-end="url(#la-arr)"/>
  <!-- 图例 -->
  <rect x="750" y="10" width="10" height="10" rx="2" fill="rgba(59,130,246,0.4)"/>
  <text x="764" y="19" font-size="8.5" fill="#64748b">表现层</text>
  <rect x="750" y="28" width="10" height="10" rx="2" fill="rgba(139,92,246,0.4)"/>
  <text x="764" y="37" font-size="8.5" fill="#64748b">应用层</text>
  <rect x="750" y="46" width="10" height="10" rx="2" fill="rgba(6,182,212,0.4)"/>
  <text x="764" y="55" font-size="8.5" fill="#64748b">数据层</text>
  <!-- 提示文字 -->
  <text x="470" y="185" text-anchor="middle" font-size="9" fill="#475569">▲ 根据实际层数增减，每层高度 = (580 - padding) ÷ N，间距 6px</text>
</svg>
```

**参数说明：**
- 每层色系独立（蓝/紫/青），通过 rgba 透明度区分层带与组件块
- 层标签：左上角 font-weight:700，字号 9px，各层主色
- 每层高 52px，层间距 6px；每增加一层整体高度 +58px
- 组件块：宽 140px，高 34px，rx=4；起始 x=120，间距 160px
