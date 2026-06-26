# fishbone · 鱼骨图（石川图）

**适用：** 根本原因分析、问题归因、质量管理、6M 分析（人/机/料/法/环/测）
**高度：** 220px

**结构公式：** 中央主骨（横线）+ 左端问题框 + 右端效果框 + 上下各 N 根斜骨（原因类别） + 子骨（具体原因）。

```html
<svg viewBox="0 0 860 220" style="width:100%;height:220px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="fb-arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#475569"/>
    </marker>
  </defs>

  <!-- 主骨（中央横线） -->
  <line x1="80" y1="110" x2="800" y2="110" stroke="#475569" stroke-width="2.5" marker-end="url(#fb-arr)"/>

  <!-- 效果框（右端） -->
  <rect x="800" y="86" width="58" height="48" rx="5" fill="rgba(239,68,68,0.15)" stroke="#ef4444" stroke-width="1.5"/>
  <text x="829" y="108" text-anchor="middle" font-size="9" fill="#fca5a5" font-weight="700">问题</text>
  <text x="829" y="122" text-anchor="middle" font-size="9" fill="#fca5a5" font-weight="700">结果</text>

  <!-- ===== 上方大骨（3根）===== -->
  <!-- 大骨1：人（左1） -->
  <line x1="200" y1="110" x2="140" y2="48" stroke="#3b82f6" stroke-width="2" marker-end="url(#fb-arr)"/>
  <text x="132" y="42" text-anchor="middle" font-size="10" font-weight="700" fill="#93c5fd">人员</text>
  <!-- 子骨 -->
  <line x1="158" y1="82" x2="185" y2="82" stroke="#3b82f6" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="153" y="85" text-anchor="end" font-size="8" fill="var(--dt)">技能不足</text>
  <line x1="175" y1="68" x2="196" y2="95" stroke="#3b82f6" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="167" y="65" text-anchor="end" font-size="8" fill="var(--dt)">培训缺失</text>

  <!-- 大骨2：机（中） -->
  <line x1="430" y1="110" x2="360" y2="36" stroke="#8b5cf6" stroke-width="2" marker-end="url(#fb-arr)"/>
  <text x="350" y="30" text-anchor="middle" font-size="10" font-weight="700" fill="#c4b5fd">设备</text>
  <!-- 子骨 -->
  <line x1="380" y1="66" x2="408" y2="66" stroke="#8b5cf6" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="375" y="69" text-anchor="end" font-size="8" fill="var(--dt)">设备老化</text>
  <line x1="400" y1="50" x2="420" y2="83" stroke="#8b5cf6" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="393" y="46" text-anchor="end" font-size="8" fill="var(--dt)">维护不足</text>

  <!-- 大骨3：法（右） -->
  <line x1="630" y1="110" x2="570" y2="38" stroke="#10b981" stroke-width="2" marker-end="url(#fb-arr)"/>
  <text x="560" y="32" text-anchor="middle" font-size="10" font-weight="700" fill="#6ee7b7">方法</text>
  <!-- 子骨 -->
  <line x1="582" y1="62" x2="610" y2="62" stroke="#10b981" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="577" y="65" text-anchor="end" font-size="8" fill="var(--dt)">流程混乱</text>
  <line x1="600" y1="48" x2="622" y2="82" stroke="#10b981" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="593" y="44" text-anchor="end" font-size="8" fill="var(--dt)">标准缺失</text>

  <!-- ===== 下方大骨（3根）===== -->
  <!-- 大骨4：料（左1） -->
  <line x1="250" y1="110" x2="175" y2="178" stroke="#f59e0b" stroke-width="2" marker-end="url(#fb-arr)"/>
  <text x="165" y="188" text-anchor="middle" font-size="10" font-weight="700" fill="#fcd34d">材料</text>
  <!-- 子骨 -->
  <line x1="196" y1="148" x2="224" y2="148" stroke="#f59e0b" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="192" y="151" text-anchor="end" font-size="8" fill="var(--dt)">质量差异</text>
  <line x1="210" y1="162" x2="238" y2="134" stroke="#f59e0b" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="203" y="175" text-anchor="end" font-size="8" fill="var(--dt)">供应不稳</text>

  <!-- 大骨5：环（中） -->
  <line x1="500" y1="110" x2="436" y2="180" stroke="#06b6d4" stroke-width="2" marker-end="url(#fb-arr)"/>
  <text x="425" y="190" text-anchor="middle" font-size="10" font-weight="700" fill="#67e8f9">环境</text>
  <!-- 子骨 -->
  <line x1="450" y1="158" x2="478" y2="144" stroke="#06b6d4" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="445" y="162" text-anchor="end" font-size="8" fill="var(--dt)">温湿度异常</text>
  <line x1="463" y1="170" x2="488" y2="128" stroke="#06b6d4" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="458" y="175" text-anchor="end" font-size="8" fill="var(--dt)">噪声干扰</text>

  <!-- 大骨6：测（右） -->
  <line x1="690" y1="110" x2="636" y2="176" stroke="#ef4444" stroke-width="2" marker-end="url(#fb-arr)"/>
  <text x="625" y="186" text-anchor="middle" font-size="10" font-weight="700" fill="#fca5a5">测量</text>
  <!-- 子骨 -->
  <line x1="648" y1="154" x2="672" y2="140" stroke="#ef4444" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="643" y="158" text-anchor="end" font-size="8" fill="var(--dt)">仪器误差</text>
  <line x1="660" y1="168" x2="682" y2="128" stroke="#ef4444" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="655" y="173" text-anchor="end" font-size="8" fill="var(--dt)">记录不准</text>

  <!-- 图题 -->
  <text x="80" y="12" font-size="10" fill="var(--dt)">根因分析 · 鱼骨图（Ishikawa Diagram）</text>
</svg>
```

**参数说明：**
- 主骨：横线 y=110（中央），从 x=80 到 x=800
- 上方大骨：从主骨上的锚点（x=200/430/630，y=110）斜向左上约 45°
- 下方大骨：从锚点斜向左下约 45°
- 子骨：从大骨上的点出发，接近水平，短线 + 末端文字
- 右端效果框：`x=800, y=86, width=58, height=48`
- 6M 分类：人/机/法（上），料/环/测（下）；颜色各自独立
