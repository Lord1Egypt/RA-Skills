# venn · 韦恩图

**适用：** 概念重叠关系、共同特征、差异对比、交集分析（2–3集合）
**高度：** 200px

---

## 变体 A · 双圆韦恩（200px）

```html
<svg viewBox="0 0 460 200" style="width:100%;height:200px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 左圆 -->
  <circle cx="170" cy="100" r="90" fill="rgba(59,130,246,0.15)" stroke="#3b82f6" stroke-width="1.5"/>
  <!-- 右圆 -->
  <circle cx="290" cy="100" r="90" fill="rgba(16,185,129,0.15)" stroke="#10b981" stroke-width="1.5"/>
  <!-- 交集高亮 -->
  <clipPath id="leftClip">
    <circle cx="170" cy="100" r="90"/>
  </clipPath>
  <circle cx="290" cy="100" r="90" fill="rgba(139,92,246,0.2)" clip-path="url(#leftClip)"/>

  <!-- 左圆独有文字 -->
  <text x="118" y="90" text-anchor="middle" font-size="9.5" fill="#93c5fd" font-weight="700">仅 A 有</text>
  <text x="118" y="106" text-anchor="middle" font-size="8.5" fill="#93c5fd">特征 1</text>
  <text x="118" y="120" text-anchor="middle" font-size="8.5" fill="#93c5fd">特征 2</text>
  <text x="118" y="134" text-anchor="middle" font-size="8.5" fill="#93c5fd">特征 3</text>

  <!-- 交集文字 -->
  <text x="230" y="90" text-anchor="middle" font-size="9.5" fill="#e2e8f0" font-weight="700">共同</text>
  <text x="230" y="106" text-anchor="middle" font-size="8.5" fill="#c4b5fd">共同点 1</text>
  <text x="230" y="120" text-anchor="middle" font-size="8.5" fill="#c4b5fd">共同点 2</text>
  <text x="230" y="134" text-anchor="middle" font-size="8.5" fill="#c4b5fd">共同点 3</text>

  <!-- 右圆独有文字 -->
  <text x="342" y="90" text-anchor="middle" font-size="9.5" fill="#6ee7b7" font-weight="700">仅 B 有</text>
  <text x="342" y="106" text-anchor="middle" font-size="8.5" fill="#6ee7b7">特征 X</text>
  <text x="342" y="120" text-anchor="middle" font-size="8.5" fill="#6ee7b7">特征 Y</text>
  <text x="342" y="134" text-anchor="middle" font-size="8.5" fill="#6ee7b7">特征 Z</text>

  <!-- 圆标题 -->
  <text x="136" y="28" text-anchor="middle" font-size="11" font-weight="800" fill="#3b82f6">集合 A</text>
  <text x="324" y="28" text-anchor="middle" font-size="11" font-weight="800" fill="#10b981">集合 B</text>

  <!-- 底部说明 -->
  <text x="230" y="192" text-anchor="middle" font-size="8.5" fill="var(--dt)">A ∩ B 交集 · 共同特征区域</text>
</svg>
```

---

## 变体 B · 三圆韦恩（220px）

```html
<svg viewBox="0 0 460 220" style="width:100%;height:220px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 三个圆（等边三角形排列，cx偏移形成重叠） -->
  <!-- 上圆（蓝） -->
  <circle cx="230" cy="80"  r="80" fill="rgba(59,130,246,0.12)" stroke="#3b82f6" stroke-width="1.5"/>
  <!-- 左下圆（绿） -->
  <circle cx="170" cy="168" r="80" fill="rgba(16,185,129,0.12)" stroke="#10b981" stroke-width="1.5"/>
  <!-- 右下圆（紫） -->
  <circle cx="290" cy="168" r="80" fill="rgba(139,92,246,0.12)" stroke="#8b5cf6" stroke-width="1.5"/>

  <!-- 圆标题 -->
  <text x="230" y="20" text-anchor="middle" font-size="10" font-weight="700" fill="#93c5fd">A 集合</text>
  <text x="88"  y="210" text-anchor="middle" font-size="10" font-weight="700" fill="#6ee7b7">B 集合</text>
  <text x="372" y="210" text-anchor="middle" font-size="10" font-weight="700" fill="#c4b5fd">C 集合</text>

  <!-- 区域标注 -->
  <!-- A 独有 -->
  <text x="230" y="58" text-anchor="middle" font-size="8" fill="#93c5fd">仅 A</text>
  <!-- B 独有 -->
  <text x="145" y="192" text-anchor="middle" font-size="8" fill="#6ee7b7">仅 B</text>
  <!-- C 独有 -->
  <text x="315" y="192" text-anchor="middle" font-size="8" fill="#c4b5fd">仅 C</text>
  <!-- A∩B -->
  <text x="188" y="138" text-anchor="middle" font-size="8" fill="#e2e8f0">A∩B</text>
  <!-- A∩C -->
  <text x="272" y="138" text-anchor="middle" font-size="8" fill="#e2e8f0">A∩C</text>
  <!-- B∩C -->
  <text x="230" y="186" text-anchor="middle" font-size="8" fill="#e2e8f0">B∩C</text>
  <!-- 三者交集 -->
  <text x="230" y="150" text-anchor="middle" font-size="9" fill="var(--t)" font-weight="700">A∩B∩C</text>
  <text x="230" y="162" text-anchor="middle" font-size="8" fill="var(--dt)">核心交集</text>
</svg>
```

**参数说明：**
- 双圆：两圆心距 = 120px，r = 90px（重叠区宽约 60px）
- 三圆：三圆心构成等边三角形，圆心间距 ≈ 90px，r = 80px
- 交集区用 clipPath 叠加更深颜色（或直接靠 opacity 叠加产生自然混色）
- 各区域文字放置于区域视觉中心点
