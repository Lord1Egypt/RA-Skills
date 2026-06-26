# flowchart · 流程图

**适用：** 步骤流程、决策分支、系统流转
**两种变体：9a 横向线性 / 9b 决策菱形**

---

## 变体 9a · 横向线性流程（4步，60px高）

```html
<svg viewBox="0 0 940 60" style="width:100%;height:60px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#475569"/>
    </marker>
  </defs>
  <!-- 步骤1 -->
  <rect x="0"   y="8" width="190" height="38" rx="5" fill="var(--pm)" stroke="var(--bd)" stroke-width="1"/>
  <text x="95"  y="24" text-anchor="middle" font-size="10" font-weight="700" fill="var(--p)">步骤 01</text>
  <text x="95"  y="38" text-anchor="middle" font-size="9" fill="var(--mt)">阶段名称</text>
  <line x1="194" y1="27" x2="218" y2="27" stroke="#475569" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- 步骤2 -->
  <rect x="220" y="8" width="190" height="38" rx="5" fill="var(--pm)" stroke="var(--bd)" stroke-width="1"/>
  <text x="315" y="24" text-anchor="middle" font-size="10" font-weight="700" fill="var(--p)">步骤 02</text>
  <text x="315" y="38" text-anchor="middle" font-size="9" fill="var(--mt)">阶段名称</text>
  <line x1="414" y1="27" x2="438" y2="27" stroke="#475569" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- 步骤3（强调） -->
  <rect x="440" y="8" width="190" height="38" rx="5" fill="var(--p)"/>
  <text x="535" y="24" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">步骤 03</text>
  <text x="535" y="38" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.7)">关键阶段</text>
  <line x1="634" y1="27" x2="658" y2="27" stroke="#475569" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- 步骤4 -->
  <rect x="660" y="8" width="190" height="38" rx="5" fill="rgba(16,185,129,0.12)" stroke="rgba(16,185,129,0.3)" stroke-width="1"/>
  <text x="755" y="24" text-anchor="middle" font-size="10" font-weight="700" fill="#10b981">步骤 04</text>
  <text x="755" y="38" text-anchor="middle" font-size="9" fill="#6ee7b7">完成</text>
  <line x1="854" y1="27" x2="900" y2="27" stroke="#475569" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- 完成标记 -->
  <circle cx="920" cy="27" r="16" fill="rgba(16,185,129,0.15)" stroke="#10b981" stroke-width="1.5"/>
  <text x="920" y="32" text-anchor="middle" font-size="14" fill="#10b981">✓</text>
</svg>
```

---

## 变体 9b · 菱形决策节点（垂直，带分支，200px高）

```html
<svg viewBox="0 0 300 200" style="width:100%;height:200px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr2" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto">
      <path d="M0,0 L0,5 L5,2.5 z" fill="#475569"/>
    </marker>
  </defs>
  <!-- 开始 -->
  <rect x="100" y="5" width="100" height="30" rx="15" fill="var(--p)"/>
  <text x="150" y="25" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">开始条件</text>
  <line x1="150" y1="35" x2="150" y2="55" stroke="#475569" stroke-width="1.5" marker-end="url(#arr2)"/>
  <!-- 决策菱形 -->
  <polygon points="150,58 210,85 150,112 90,85" fill="rgba(245,158,11,0.15)" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="150" y="89" text-anchor="middle" font-size="9" font-weight="600" fill="#f59e0b">条件判断?</text>
  <!-- 是：向右 -->
  <line x1="210" y1="85" x2="248" y2="85" stroke="#475569" stroke-width="1.5" marker-end="url(#arr2)"/>
  <text x="228" y="80" text-anchor="middle" font-size="8" fill="#10b981">是</text>
  <rect x="250" y="70" width="46" height="30" rx="4" fill="rgba(16,185,129,0.15)" stroke="#10b981" stroke-width="1"/>
  <text x="273" y="89" text-anchor="middle" font-size="9" font-weight="600" fill="#10b981">执行A</text>
  <!-- 否：向左 -->
  <line x1="90" y1="85" x2="52" y2="85" stroke="#475569" stroke-width="1.5" marker-end="url(#arr2)"/>
  <text x="70" y="80" text-anchor="middle" font-size="8" fill="#ef4444">否</text>
  <rect x="4" y="70" width="46" height="30" rx="4" fill="rgba(239,68,68,0.15)" stroke="#ef4444" stroke-width="1"/>
  <text x="27" y="89" text-anchor="middle" font-size="9" font-weight="600" fill="#ef4444">执行B</text>
  <!-- 汇合 -->
  <line x1="273" y1="100" x2="273" y2="160" stroke="#475569" stroke-width="1" stroke-dasharray="3,2"/>
  <line x1="27"  y1="100" x2="27"  y2="160" stroke="#475569" stroke-width="1" stroke-dasharray="3,2"/>
  <line x1="27"  y1="160" x2="150" y2="160" stroke="#475569" stroke-width="1.5"/>
  <line x1="273" y1="160" x2="150" y2="160" stroke="#475569" stroke-width="1.5"/>
  <line x1="150" y1="160" x2="150" y2="172" stroke="#475569" stroke-width="1.5" marker-end="url(#arr2)"/>
  <!-- 结束 -->
  <rect x="100" y="174" width="100" height="24" rx="12" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
  <text x="150" y="190" text-anchor="middle" font-size="9" fill="var(--mt)">结果输出</text>
</svg>
```

> 复杂业务流程（跨部门、漏斗）→ 见 `10-diagram-types.md`
