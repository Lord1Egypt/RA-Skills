# 05 · 内容规则与图表库

---

## 反偷懒强制约束

> AI 偷懒的核心手段：间距虚大 + 内容极少 + 卡片大量留白。以下规则全部可量化，每格生成后逐条自查。

### 间距硬上限

| 属性 | 硬上限 | 偷懒常见值（禁止） |
|------|--------|----------------|
| 网格 `gap` | **8px** | 16–24px |
| 卡片 `padding` 上下 | **8px** | 16–20px |
| 卡片 `padding` 左右 | **12px** | 20–24px |
| 标题 `margin-bottom` | **5px** | 10–16px |
| 文字 `line-height` | **1.45** | 1.6–2.0 |
| `.ct` `padding-top` | **0（禁止）** | 12–20px |

### 75% 填充率规则

每个卡片：**文字 + 图表高度 ≥ 卡片可用高度的 75%**

```
布局C 每格：高 281px，padding 上下各 8px → 可用 265px
最低要求：265 × 75% = 199px 必须被内容填满

❌ 偷懒：标题 22px + 正文 1 行 18px = 40px → 占比 15%，不通过
✅ 合格：标题 22px + 正文 4 行 72px + SVG 80px + mini 35px = 209px → 79%，通过
```

判断方法：视觉上看卡片背景色区域，若背景色面积 > 内容面积，即不通过。

### 三层内容结构（每格必须）

```
层次 1：标题行（主题词 + 核心数字，1 行）
层次 2：正文段落（含 ≥2 个数字/专有名词，3–5 行）
层次 3：下方增强组件（三选一）
         ├── mini 数据卡片行（2–4 个，flex 排列）
         ├── 内嵌 SVG 图表（条形/折线/进度条）
         └── 数据网格（2×2 或 3×1 数字块）
```

**只有层次 1+2 没有层次 3 = 偷懒，必须补充。**

### 5 问自查表（每格回答，≥4 个"是"才通过）

```
□ 正文字数 ≥ 40 字（布局B行内除外）？
□ 正文含 ≥ 2 个具体数字或百分比？
□ 有第 3 层内容组件（mini卡/SVG/数据块）？
□ 卡片内无超过 30px 的空白连续区域？
□ 行高 ≤ 1.45，gap ≤ 8px，padding-top ≤ 8px？
```

---

## 内容写作规范

### 禁止空洞描述

```
❌ 该攻击危害严重，具有重要研究价值。（0 个数字）
❌ 防御方案效果良好，推荐采用。（0 个数字，0 个专有名词）
❌ 模型存在漏洞，需要及时修复。（废话）
```

### 必须紧凑数据

```
✅ FGSM 单步成功率 63%，PGD-40 步达 97%，ε≤0.03 时人眼无法分辨。
✅ PGD 对抗训练鲁棒精度 +34%，代价仅 -5.2%；C&W 可 bypass 蒸馏防御（Carlini 2017）。
✅ 停车标志贴纸攻击（Eykholt 2018）：30m 外误识率 91%，任意光照条件有效。
```

**每个卡片至少包含 2 个具体数字或专有名词（论文作者/年份/工具名/百分比/毫秒/px）。**

### 关键词高亮规范

```html
<!-- 数字/百分比 → <b> -->
<b style="color:var(--t);">97%</b>

<!-- 公式/代码 → <em>（等宽主色）-->
<em style="color:var(--p);font-style:normal;font-family:monospace;">δ=ε·sign(∇ₓJ)</em>

<!-- 专有名词/论文 → <b> -->
<b style="color:var(--t);">PGD-AT</b>（Madry 2018）
```

---

## SVG 图表库

> 所有 SVG 必须有真实坐标轴标签和数值，**禁止纯装饰形状**。

### 图表 1 · 横向条形图（55px 高，卡片内嵌）

```html
<svg viewBox="0 0 290 55" style="width:100%;height:55px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <text x="0"   y="11" font-size="9" fill="#64748b">FGSM</text>
  <rect x="46"  y="2"  width="122" height="9" rx="2" fill="var(--p)"/>
  <text x="172" y="11" font-size="9" fill="var(--mt)">63%</text>

  <text x="0"   y="28" font-size="9" fill="#64748b">PGD-40</text>
  <rect x="46"  y="19" width="188" height="9" rx="2" fill="#8b5cf6"/>
  <text x="238" y="28" font-size="9" fill="var(--mt)">97%</text>

  <text x="0"   y="45" font-size="9" fill="#64748b">C&amp;W</text>
  <rect x="46"  y="36" width="169" height="9" rx="2" fill="#ef4444"/>
  <text x="219" y="45" font-size="9" fill="var(--mt)">87%</text>
</svg>
```

---

### 图表 2 · 折线面积图（85px 高，带渐变填充）

```html
<svg viewBox="0 0 290 85" style="width:100%;height:85px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="ga" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="var(--p)" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="var(--p)" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <!-- 坐标轴 -->
  <line x1="24" y1="6"  x2="24"  y2="62" stroke="#1e293b" stroke-width="1"/>
  <line x1="24" y1="62" x2="270" y2="62" stroke="#1e293b" stroke-width="1"/>
  <line x1="24" y1="36" x2="270" y2="36" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="3,3"/>
  <!-- 面积填充 + 折线 -->
  <polygon points="24,54 78,44 132,33 186,22 240,14 270,10 270,62 24,62" fill="url(#ga)"/>
  <polyline points="24,54 78,44 132,33 186,22 240,14 270,10" fill="none" stroke="var(--p)" stroke-width="1.8"/>
  <!-- 数据点 -->
  <circle cx="24"  cy="54" r="2.5" fill="var(--p)"/>
  <circle cx="132" cy="33" r="2.5" fill="var(--p)"/>
  <circle cx="270" cy="10" r="2.5" fill="var(--p)"/>
  <!-- 标签 -->
  <text x="24"  y="74" font-size="8.5" fill="#64748b" text-anchor="middle">2020</text>
  <text x="132" y="74" font-size="8.5" fill="#64748b" text-anchor="middle">2022</text>
  <text x="270" y="74" font-size="8.5" fill="#64748b" text-anchor="middle">2024</text>
  <text x="20"  y="54" font-size="8.5" fill="#64748b" text-anchor="end">43%</text>
  <text x="20"  y="10" font-size="8.5" fill="#64748b" text-anchor="end">99%</text>
</svg>
```

---

### 图表 3 · 雷达图（190×190px，含双数据集）

> ⚠ 每份报告雷达图最多出现 2 次。

```html
<svg viewBox="0 0 200 190" style="width:190px;height:180px;" xmlns="http://www.w3.org/2000/svg">
  <!-- 背景网格（3层六边形） -->
  <polygon points="100,12 170,54 170,138 100,180 30,138 30,54"   fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="1.5"/>
  <polygon points="100,36 146,62 146,114 100,140 54,114 54,62"   fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="1"/>
  <polygon points="100,60 122,74 122,98 100,112 78,98  78,74"    fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="0.8"/>
  <!-- 数据集 A -->
  <polygon points="100,18 164,60 155,132 100,172 38,126 44,56"
           fill="rgba(239,68,68,0.15)" stroke="#ef4444" stroke-width="1.5"/>
  <!-- 数据集 B（可选） -->
  <polygon points="100,38 136,62 135,106 100,130 64,106 62,58"
           fill="rgba(99,102,241,0.12)" stroke="#6366f1" stroke-width="1" stroke-dasharray="3,2"/>
  <!-- 轴标签 -->
  <text x="100" y="7"   text-anchor="middle" font-size="8.5" fill="#94a3b8">维度A</text>
  <text x="178" y="57"  font-size="8.5" fill="#94a3b8">维度B</text>
  <text x="178" y="142" font-size="8.5" fill="#94a3b8">维度C</text>
  <text x="100" y="192" text-anchor="middle" font-size="8.5" fill="#94a3b8">维度D</text>
  <text x="2"   y="142" font-size="8.5" fill="#94a3b8" text-anchor="end">维度E</text>
  <text x="2"   y="57"  font-size="8.5" fill="#94a3b8" text-anchor="end">维度F</text>
  <!-- 图例 -->
  <line x1="18" y1="162" x2="32" y2="162" stroke="#ef4444" stroke-width="1.5"/>
  <text x="35" y="165" font-size="8" fill="#9ca3af">方案A</text>
  <line x1="64" y1="162" x2="78" y2="162" stroke="#6366f1" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="81" y="165" font-size="8" fill="#9ca3af">方案B</text>
</svg>
```

---

### 图表 4 · 时间轴（横向，38px 高）

```html
<svg viewBox="0 0 540 38" style="width:100%;height:38px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <line x1="10" y1="12" x2="530" y2="12" stroke="#1e293b" stroke-width="1.5"/>
  <!-- 节点 1 -->
  <circle cx="60"  cy="12" r="5" fill="var(--p)"/>
  <text x="60"  y="27" text-anchor="middle" font-size="8.5" fill="#64748b">2016</text>
  <text x="60"  y="37" text-anchor="middle" font-size="8" fill="var(--mt)">事件A · 88%</text>
  <!-- 节点 2 -->
  <circle cx="200" cy="12" r="5" fill="var(--p)"/>
  <text x="200" y="27" text-anchor="middle" font-size="8.5" fill="#64748b">2018</text>
  <text x="200" y="37" text-anchor="middle" font-size="8" fill="var(--mt)">事件B · 91%</text>
  <!-- 节点 3 -->
  <circle cx="360" cy="12" r="5" fill="#ef4444"/>
  <text x="360" y="27" text-anchor="middle" font-size="8.5" fill="#64748b">2020</text>
  <text x="360" y="37" text-anchor="middle" font-size="8" fill="#fca5a5">事件C · 100%</text>
  <!-- 节点 4 -->
  <circle cx="500" cy="12" r="5" fill="#10b981"/>
  <text x="500" y="27" text-anchor="middle" font-size="8.5" fill="#64748b">2023</text>
  <text x="500" y="37" text-anchor="middle" font-size="8" fill="#6ee7b7">事件D · 76%</text>
</svg>
```

---

### 图表 5 · 甘特条（进度/计划，38px 高）

```html
<svg viewBox="0 0 540 38" style="width:100%;height:38px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <rect x="0"   y="4" width="175" height="14" rx="3" fill="rgba(239,68,68,0.8)"/>
  <text x="88"  y="14" text-anchor="middle" font-size="8.5" fill="white">阶段1：W1-2</text>
  <rect x="179" y="4" width="175" height="14" rx="3" fill="rgba(99,102,241,0.8)"/>
  <text x="267" y="14" text-anchor="middle" font-size="8.5" fill="white">阶段2：W3-4</text>
  <rect x="358" y="4" width="175" height="14" rx="3" fill="rgba(16,185,129,0.8)"/>
  <text x="445" y="14" text-anchor="middle" font-size="8.5" fill="white">阶段3：W5-6</text>
  <text x="0"   y="33" font-size="8" fill="#64748b">Week 1</text>
  <text x="175" y="33" font-size="8" fill="#64748b">Week 3</text>
  <text x="354" y="33" font-size="8" fill="#64748b">Week 5</text>
  <text x="530" y="33" font-size="8" fill="#64748b" text-anchor="end">Week 6</text>
</svg>
```

---

### 图表 6 · 柱状图（对比，75px 高）

```html
<svg viewBox="0 0 290 75" style="width:100%;height:75px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 基准线 -->
  <line x1="20" y1="55" x2="280" y2="55" stroke="#1e293b" stroke-width="1"/>
  <line x1="20" y1="35" x2="280" y2="35" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="2,3"/>
  <line x1="20" y1="15" x2="280" y2="15" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="2,3"/>
  <!-- 柱 -->
  <rect x="30"  y="20" width="30" height="35" rx="2" fill="var(--p)" opacity="0.9"/>
  <rect x="80"  y="10" width="30" height="45" rx="2" fill="var(--p)"/>
  <rect x="130" y="25" width="30" height="30" rx="2" fill="#ef4444"/>
  <rect x="180" y="5"  width="30" height="50" rx="2" fill="var(--p)"/>
  <rect x="230" y="15" width="30" height="40" rx="2" fill="#10b981"/>
  <!-- 标签 -->
  <text x="45"  y="65" text-anchor="middle" font-size="8" fill="#64748b">A</text>
  <text x="95"  y="65" text-anchor="middle" font-size="8" fill="#64748b">B</text>
  <text x="145" y="65" text-anchor="middle" font-size="8" fill="#64748b">C</text>
  <text x="195" y="65" text-anchor="middle" font-size="8" fill="#64748b">D</text>
  <text x="245" y="65" text-anchor="middle" font-size="8" fill="#64748b">E</text>
  <!-- Y轴 -->
  <text x="16"  y="58" font-size="8" fill="#64748b" text-anchor="end">0%</text>
  <text x="16"  y="38" font-size="8" fill="#64748b" text-anchor="end">50%</text>
  <text x="16"  y="18" font-size="8" fill="#64748b" text-anchor="end">100%</text>
</svg>
```

---

## 数字块组件（无 SVG，纯 CSS）

### 3 格数字块

```html
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin-top:5px;flex-shrink:0;">
  <div style="background:var(--pm);border:1px solid var(--bd);border-radius:4px;padding:5px 7px;text-align:center;">
    <div style="font-size:18px;font-weight:700;color:var(--p);letter-spacing:-0.5px;line-height:1;">97%</div>
    <div style="font-size:9px;color:var(--dt);margin-top:2px;">攻击成功率</div>
  </div>
  <div style="background:var(--pm);border:1px solid var(--bd);border-radius:4px;padding:5px 7px;text-align:center;">
    <div style="font-size:18px;font-weight:700;color:var(--p);letter-spacing:-0.5px;line-height:1;">63%</div>
    <div style="font-size:9px;color:var(--dt);margin-top:2px;">单步成功率</div>
  </div>
  <div style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.25);border-radius:4px;padding:5px 7px;text-align:center;">
    <div style="font-size:18px;font-weight:700;color:#ef4444;letter-spacing:-0.5px;line-height:1;">100%</div>
    <div style="font-size:9px;color:var(--dt);margin-top:2px;">物理场景</div>
  </div>
</div>
```

### 防御对比列表（带圆点）

```html
<div style="display:flex;flex-direction:column;gap:4px;margin-top:4px;">
  <div style="display:flex;align-items:center;gap:6px;">
    <div style="width:7px;height:7px;border-radius:50%;background:#10b981;flex-shrink:0;"></div>
    <span style="font-size:11px;color:var(--t);font-weight:500;">PGD对抗训练</span>
    <span style="margin-left:auto;font-size:10px;color:#10b981;">鲁棒+34% / 精度-5.2%</span>
  </div>
  <div style="display:flex;align-items:center;gap:6px;">
    <div style="width:7px;height:7px;border-radius:50%;background:#f59e0b;flex-shrink:0;"></div>
    <span style="font-size:11px;color:var(--t);font-weight:500;">输入平滑</span>
    <span style="margin-left:auto;font-size:10px;color:#f59e0b;">速度10× / C&W无效</span>
  </div>
  <div style="display:flex;align-items:center;gap:6px;">
    <div style="width:7px;height:7px;border-radius:50%;background:#ef4444;flex-shrink:0;"></div>
    <span style="font-size:11px;color:var(--t);font-weight:500;">蒸馏防御</span>
    <span style="margin-left:auto;font-size:10px;color:#ef4444;">速度快 / C&W可破</span>
  </div>
</div>
```

### 进度条行

```html
<div style="display:flex;flex-direction:column;gap:4px;flex-shrink:0;">
  <div style="display:flex;align-items:center;gap:7px;font-size:9.5px;color:var(--dt);">
    <span style="width:52px;">FGSM</span>
    <div style="flex:1;height:3px;background:rgba(255,255,255,0.04);border-radius:2px;overflow:hidden;">
      <div style="width:63%;height:100%;background:linear-gradient(90deg,var(--p),color-mix(in srgb,var(--p) 70%,#fff));border-radius:2px;"></div>
    </div>
    <b style="color:var(--mt);">63%</b>
  </div>
  <div style="display:flex;align-items:center;gap:7px;font-size:9.5px;color:var(--dt);">
    <span style="width:52px;">PGD-40</span>
    <div style="flex:1;height:3px;background:rgba(255,255,255,0.04);border-radius:2px;overflow:hidden;">
      <div style="width:97%;height:100%;background:linear-gradient(90deg,#8b5cf6,#a78bfa);border-radius:2px;"></div>
    </div>
    <b style="color:var(--mt);">97%</b>
  </div>
</div>
```
