# step-indicator · 步骤指示器

**适用：** 流程进度状态、阶段完成情况、多步骤工作流
**高度：** 28px（紧凑横向）

---

## 变体 A · 5步骤圆点式（28px）

```html
<svg viewBox="0 0 290 28" style="width:100%;height:28px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 连接线（底层先画，不遮住圆点） -->
  <line x1="20" y1="12" x2="270" y2="12" stroke="#1e293b" stroke-width="1.5"/>
  <!-- 已完成段：绿色 -->
  <line x1="20" y1="12" x2="144" y2="12" stroke="var(--p)" stroke-width="2"/>

  <!-- 步骤1（完成） -->
  <circle cx="20"  cy="12" r="9" fill="var(--p)"/>
  <text x="20"  y="16" text-anchor="middle" font-size="8" fill="#fff" font-weight="700">✓</text>
  <text x="20"  y="26" text-anchor="middle" font-size="6.5" fill="#64748b">规划</text>

  <!-- 步骤2（完成） -->
  <circle cx="82"  cy="12" r="9" fill="var(--p)"/>
  <text x="82"  y="16" text-anchor="middle" font-size="8" fill="#fff" font-weight="700">✓</text>
  <text x="82"  y="26" text-anchor="middle" font-size="6.5" fill="#64748b">设计</text>

  <!-- 步骤3（当前，动态感） -->
  <circle cx="144" cy="12" r="9" fill="var(--p)" opacity="0.15"/>
  <circle cx="144" cy="12" r="9" fill="none" stroke="var(--p)" stroke-width="2"/>
  <circle cx="144" cy="12" r="4" fill="var(--p)"/>
  <text x="144" y="26" text-anchor="middle" font-size="6.5" fill="var(--p)" font-weight="700">开发</text>

  <!-- 步骤4（未开始） -->
  <circle cx="206" cy="12" r="9" fill="rgba(255,255,255,0.04)" stroke="#334155" stroke-width="1.5"/>
  <text x="206" y="16" text-anchor="middle" font-size="8.5" fill="#475569" font-weight="600">4</text>
  <text x="206" y="26" text-anchor="middle" font-size="6.5" fill="#475569">测试</text>

  <!-- 步骤5（未开始） -->
  <circle cx="270" cy="12" r="9" fill="rgba(255,255,255,0.04)" stroke="#334155" stroke-width="1.5"/>
  <text x="270" y="16" text-anchor="middle" font-size="8.5" fill="#475569" font-weight="600">5</text>
  <text x="270" y="26" text-anchor="middle" font-size="6.5" fill="#475569">上线</text>
</svg>
```

---

## 变体 B · 方块式步骤（30px）

```html
<svg viewBox="0 0 290 30" style="width:100%;height:30px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="stepArr" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto">
      <path d="M0,0 L0,5 L5,2.5 z" fill="#1e293b"/>
    </marker>
  </defs>

  <!-- 步骤块1（完成） -->
  <rect x="0" y="6" width="50" height="18" rx="4" fill="var(--p)"/>
  <text x="25" y="18" text-anchor="middle" font-size="8.5" fill="#fff" font-weight="700">规划</text>
  <line x1="52" y1="15" x2="60" y2="15" stroke="#1e293b" stroke-width="1.5" marker-end="url(#stepArr)"/>

  <!-- 步骤块2（完成） -->
  <rect x="62" y="6" width="50" height="18" rx="4" fill="var(--p)"/>
  <text x="87" y="18" text-anchor="middle" font-size="8.5" fill="#fff" font-weight="700">设计</text>
  <line x1="114" y1="15" x2="122" y2="15" stroke="#1e293b" stroke-width="1.5" marker-end="url(#stepArr)"/>

  <!-- 步骤块3（当前，高亮边框） -->
  <rect x="124" y="4" width="54" height="22" rx="4" fill="var(--pm)" stroke="var(--p)" stroke-width="2"/>
  <text x="151" y="18" text-anchor="middle" font-size="8.5" fill="var(--p)" font-weight="700">开发中</text>
  <line x1="180" y1="15" x2="188" y2="15" stroke="#334155" stroke-width="1.5" marker-end="url(#stepArr)"/>

  <!-- 步骤块4（未开始） -->
  <rect x="190" y="6" width="46" height="18" rx="4" fill="rgba(255,255,255,0.04)" stroke="#334155" stroke-width="1"/>
  <text x="213" y="18" text-anchor="middle" font-size="8.5" fill="#475569">测试</text>
  <line x1="238" y1="15" x2="246" y2="15" stroke="#334155" stroke-width="1.5" marker-end="url(#stepArr)"/>

  <!-- 步骤块5（未开始） -->
  <rect x="248" y="6" width="42" height="18" rx="4" fill="rgba(255,255,255,0.04)" stroke="#334155" stroke-width="1"/>
  <text x="269" y="18" text-anchor="middle" font-size="8.5" fill="#475569">上线</text>
</svg>
```

---

## 变体 C · 垂直步骤列表（每步18px，适合3-5步）

```html
<svg viewBox="0 0 220 90" style="width:100%;height:90px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 垂直连接线 -->
  <line x1="10" y1="8" x2="10" y2="82" stroke="#1e293b" stroke-width="1.5"/>
  <line x1="10" y1="8" x2="10" y2="50" stroke="var(--p)" stroke-width="2"/>

  <!-- 步骤1（完成） -->
  <circle cx="10" cy="10" r="7" fill="var(--p)"/>
  <text x="10" y="14" text-anchor="middle" font-size="7" fill="#fff">✓</text>
  <text x="24" y="11" font-size="9" fill="var(--t)" font-weight="700">阶段一：完成</text>
  <text x="24" y="21" font-size="7.5" fill="var(--dt)">成果：交付物A，耗时3天</text>

  <!-- 步骤2（完成） -->
  <circle cx="10" cy="32" r="7" fill="var(--p)"/>
  <text x="10" y="36" text-anchor="middle" font-size="7" fill="#fff">✓</text>
  <text x="24" y="33" font-size="9" fill="var(--t)" font-weight="700">阶段二：完成</text>
  <text x="24" y="43" font-size="7.5" fill="var(--dt)">成果：交付物B，耗时5天</text>

  <!-- 步骤3（当前） -->
  <circle cx="10" cy="54" r="7" fill="none" stroke="var(--p)" stroke-width="2"/>
  <circle cx="10" cy="54" r="3" fill="var(--p)"/>
  <text x="24" y="55" font-size="9" fill="var(--p)" font-weight="700">阶段三：进行中</text>
  <text x="24" y="65" font-size="7.5" fill="var(--dt)">预计完成：2天后</text>

  <!-- 步骤4（未开始） -->
  <circle cx="10" cy="76" r="7" fill="rgba(255,255,255,0.04)" stroke="#334155" stroke-width="1.5"/>
  <text x="10" y="80" text-anchor="middle" font-size="8" fill="#475569">4</text>
  <text x="24" y="77" font-size="9" fill="#475569">阶段四：待开始</text>
  <text x="24" y="87" font-size="7.5" fill="#475569">计划开始日期</text>
</svg>
```

**参数说明：**
- 横向5步：节点 cx 均匀分布 = 20 + (步骤-1) × 62.5
- 已完成节点：实心填充 + 勾号；当前：空心+内点；未开始：灰色
- 已完成连接线用主色覆盖底层灰线
