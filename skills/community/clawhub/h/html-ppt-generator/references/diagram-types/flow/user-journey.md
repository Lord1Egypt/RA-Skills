# user-journey · 用户旅程图

**适用：** 用户体验分析、服务触点梳理、情感曲线、CX/UX 场景展示
**高度：** 220px

**结构公式：** 顶部阶段栏 + 中部接触点 + 底部情感曲线（折线高低表示情绪）。

```html
<svg viewBox="0 0 860 220" style="width:100%;height:220px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="ujGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#10b981" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- 阶段标题栏 -->
  <rect x="0"   y="0" width="172" height="28" rx="4" fill="rgba(59,130,246,0.15)" stroke="rgba(59,130,246,0.3)" stroke-width="1"/>
  <rect x="175" y="0" width="172" height="28" rx="4" fill="rgba(139,92,246,0.15)" stroke="rgba(139,92,246,0.3)" stroke-width="1"/>
  <rect x="350" y="0" width="172" height="28" rx="4" fill="rgba(245,158,11,0.15)" stroke="rgba(245,158,11,0.3)" stroke-width="1"/>
  <rect x="525" y="0" width="172" height="28" rx="4" fill="rgba(16,185,129,0.15)" stroke="rgba(16,185,129,0.3)" stroke-width="1"/>
  <rect x="700" y="0" width="160" height="28" rx="4" fill="rgba(239,68,68,0.15)"  stroke="rgba(239,68,68,0.3)"  stroke-width="1"/>

  <text x="86"  y="18" text-anchor="middle" font-size="10" font-weight="700" fill="#93c5fd">认知</text>
  <text x="261" y="18" text-anchor="middle" font-size="10" font-weight="700" fill="#c4b5fd">探索</text>
  <text x="436" y="18" text-anchor="middle" font-size="10" font-weight="700" fill="#fcd34d">购买</text>
  <text x="611" y="18" text-anchor="middle" font-size="10" font-weight="700" fill="#6ee7b7">使用</text>
  <text x="780" y="18" text-anchor="middle" font-size="10" font-weight="700" fill="#fca5a5">留存</text>

  <!-- 接触点行 -->
  <text x="0" y="48" font-size="8.5" fill="#64748b" font-weight="600">接触点</text>
  <!-- 阶段1 接触点 -->
  <rect x="10"  y="36" width="70" height="20" rx="3" fill="rgba(255,255,255,0.05)" stroke="#334155" stroke-width="1"/>
  <text x="45"  y="50" text-anchor="middle" font-size="8" fill="var(--mt)">社交媒体</text>
  <rect x="90"  y="36" width="70" height="20" rx="3" fill="rgba(255,255,255,0.05)" stroke="#334155" stroke-width="1"/>
  <text x="125" y="50" text-anchor="middle" font-size="8" fill="var(--mt)">广告投放</text>
  <!-- 阶段2 -->
  <rect x="185" y="36" width="70" height="20" rx="3" fill="rgba(255,255,255,0.05)" stroke="#334155" stroke-width="1"/>
  <text x="220" y="50" text-anchor="middle" font-size="8" fill="var(--mt)">官网浏览</text>
  <rect x="265" y="36" width="70" height="20" rx="3" fill="rgba(255,255,255,0.05)" stroke="#334155" stroke-width="1"/>
  <text x="300" y="50" text-anchor="middle" font-size="8" fill="var(--mt)">产品对比</text>
  <!-- 阶段3 -->
  <rect x="360" y="36" width="70" height="20" rx="3" fill="rgba(255,255,255,0.05)" stroke="#334155" stroke-width="1"/>
  <text x="395" y="50" text-anchor="middle" font-size="8" fill="var(--mt)">加入购物车</text>
  <rect x="440" y="36" width="70" height="20" rx="3" fill="rgba(255,255,255,0.05)" stroke="#334155" stroke-width="1"/>
  <text x="475" y="50" text-anchor="middle" font-size="8" fill="var(--mt)">支付结算</text>
  <!-- 阶段4 -->
  <rect x="535" y="36" width="70" height="20" rx="3" fill="rgba(255,255,255,0.05)" stroke="#334155" stroke-width="1"/>
  <text x="570" y="50" text-anchor="middle" font-size="8" fill="var(--mt)">开箱体验</text>
  <rect x="615" y="36" width="70" height="20" rx="3" fill="rgba(255,255,255,0.05)" stroke="#334155" stroke-width="1"/>
  <text x="650" y="50" text-anchor="middle" font-size="8" fill="var(--mt)">客服支持</text>
  <!-- 阶段5 -->
  <rect x="710" y="36" width="65" height="20" rx="3" fill="rgba(255,255,255,0.05)" stroke="#334155" stroke-width="1"/>
  <text x="743" y="50" text-anchor="middle" font-size="8" fill="var(--mt)">会员权益</text>
  <rect x="784" y="36" width="68" height="20" rx="3" fill="rgba(255,255,255,0.05)" stroke="#334155" stroke-width="1"/>
  <text x="818" y="50" text-anchor="middle" font-size="8" fill="var(--mt)">口碑推荐</text>

  <!-- 情感分隔线 -->
  <line x1="0" y1="70" x2="860" y2="70" stroke="#1e293b" stroke-width="1"/>
  <text x="0" y="84" font-size="8.5" fill="#64748b" font-weight="600">情感</text>
  <!-- 情感区间参考线 -->
  <line x1="0" y1="100" x2="860" y2="100" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="3,3"/>
  <line x1="0" y1="130" x2="860" y2="130" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="3,3"/>
  <text x="864" y="78"  font-size="7.5" fill="#10b981">😊</text>
  <text x="864" y="103" font-size="7.5" fill="#f59e0b">😐</text>
  <text x="864" y="133" font-size="7.5" fill="#ef4444">😞</text>

  <!-- 情感面积填充 -->
  <polygon points="45,110 125,90 220,105 300,115 395,130 475,145 570,90 650,80 743,85 818,78 818,155 45,155"
           fill="url(#ujGrad)"/>
  <!-- 情感曲线 -->
  <polyline points="45,110 125,90 220,105 300,115 395,130 475,145 570,90 650,80 743,85 818,78"
            fill="none" stroke="#10b981" stroke-width="2.5" stroke-linejoin="round"/>
  <!-- 情感节点 -->
  <circle cx="45"  cy="110" r="4" fill="#10b981"/>
  <circle cx="125" cy="90"  r="4" fill="#10b981"/>
  <circle cx="220" cy="105" r="4" fill="#10b981"/>
  <circle cx="300" cy="115" r="4" fill="#f59e0b"/>
  <circle cx="395" cy="130" r="4" fill="#f59e0b"/>
  <circle cx="475" cy="145" r="5" fill="#ef4444"/><!-- 痛点 -->
  <circle cx="570" cy="90"  r="4" fill="#10b981"/>
  <circle cx="650" cy="80"  r="4" fill="#10b981"/>
  <circle cx="743" cy="85"  r="4" fill="#10b981"/>
  <circle cx="818" cy="78"  r="4" fill="#10b981"/>

  <!-- 痛点标注 -->
  <line x1="475" y1="140" x2="475" y2="160" stroke="#ef4444" stroke-width="1" stroke-dasharray="2,2"/>
  <rect x="432" y="160" width="86" height="16" rx="3" fill="rgba(239,68,68,0.1)" stroke="rgba(239,68,68,0.3)" stroke-width="1"/>
  <text x="475" y="172" text-anchor="middle" font-size="8" fill="#fca5a5">⚠ 支付失败痛点</text>

  <!-- 关键机会标注 -->
  <line x1="650" y1="76" x2="650" y2="60" stroke="#10b981" stroke-width="1" stroke-dasharray="2,2"/>
  <rect x="613" y="48" width="74" height="14" rx="3" fill="rgba(16,185,129,0.1)" stroke="rgba(16,185,129,0.3)" stroke-width="1"/>
  <text x="650" y="58" text-anchor="middle" font-size="7.5" fill="#6ee7b7">✦ 超预期体验</text>

  <!-- 分隔线 -->
  <line x1="173" y1="0"  x2="173" y2="185" stroke="#1e293b" stroke-width="0.8" stroke-dasharray="3,3"/>
  <line x1="348" y1="0"  x2="348" y2="185" stroke="#1e293b" stroke-width="0.8" stroke-dasharray="3,3"/>
  <line x1="523" y1="0"  x2="523" y2="185" stroke="#1e293b" stroke-width="0.8" stroke-dasharray="3,3"/>
  <line x1="698" y1="0"  x2="698" y2="185" stroke="#1e293b" stroke-width="0.8" stroke-dasharray="3,3"/>

  <!-- 底部行动建议 -->
  <text x="0" y="200" font-size="8.5" fill="#64748b" font-weight="600">机会点</text>
  <text x="45"  y="215" text-anchor="middle" font-size="8" fill="var(--dt)">精准触达</text>
  <text x="261" y="215" text-anchor="middle" font-size="8" fill="var(--dt)">降低决策成本</text>
  <text x="436" y="215" text-anchor="middle" font-size="8" fill="#fca5a5">优化支付流程 ★</text>
  <text x="611" y="215" text-anchor="middle" font-size="8" fill="var(--dt)">强化首次体验</text>
  <text x="780" y="215" text-anchor="middle" font-size="8" fill="var(--dt)">激励推荐机制</text>
</svg>
```

**参数说明：**
- 情感曲线 Y 轴：78（高兴）/ 100（中性）/ 130（不满），高度越小情绪越好
- 痛点节点用 #ef4444 + 较大 r=5 突出；高光点用 #10b981
- 阶段宽度可按实际步骤数均分总宽（860px ÷ N 阶段）
- 每阶段接触点 2 个，宽约 70px，间距 10px
