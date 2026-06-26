# icon-array · 图标数组/百格图

**适用：** 频率/概率可视化（如"100人中有X人"）、受众比例、风险人群展示
**高度：** 80px（10×10格）

---

## 变体 A · 人形图标数组（80px，10×10=100个单元）

```html
<svg viewBox="0 0 200 80" style="width:100%;height:80px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 10×10 人形图标阵列，每格 20×8px -->
  <!-- 使用简化人形：圆头+身体 -->
  <!-- 高亮前 N 个（示例：高亮前 27 个 = 27%） -->

  <!-- 行1（1-10）：1-10全高亮 -->
  <circle cx="10" cy="7" r="2.5" fill="var(--p)"/><rect x="8.5" y="10" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="30" cy="7" r="2.5" fill="var(--p)"/><rect x="28.5" y="10" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="50" cy="7" r="2.5" fill="var(--p)"/><rect x="48.5" y="10" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="70" cy="7" r="2.5" fill="var(--p)"/><rect x="68.5" y="10" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="90" cy="7" r="2.5" fill="var(--p)"/><rect x="88.5" y="10" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="110" cy="7" r="2.5" fill="var(--p)"/><rect x="108.5" y="10" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="130" cy="7" r="2.5" fill="var(--p)"/><rect x="128.5" y="10" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="150" cy="7" r="2.5" fill="var(--p)"/><rect x="148.5" y="10" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="170" cy="7" r="2.5" fill="var(--p)"/><rect x="168.5" y="10" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="190" cy="7" r="2.5" fill="var(--p)"/><rect x="188.5" y="10" width="3" height="5" rx="1" fill="var(--p)"/>

  <!-- 行2（11-20）：11-20全高亮 -->
  <circle cx="10" cy="23" r="2.5" fill="var(--p)"/><rect x="8.5" y="26" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="30" cy="23" r="2.5" fill="var(--p)"/><rect x="28.5" y="26" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="50" cy="23" r="2.5" fill="var(--p)"/><rect x="48.5" y="26" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="70" cy="23" r="2.5" fill="var(--p)"/><rect x="68.5" y="26" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="90" cy="23" r="2.5" fill="var(--p)"/><rect x="88.5" y="26" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="110" cy="23" r="2.5" fill="var(--p)"/><rect x="108.5" y="26" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="130" cy="23" r="2.5" fill="var(--p)"/><rect x="128.5" y="26" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="150" cy="23" r="2.5" fill="var(--p)"/><rect x="148.5" y="26" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="170" cy="23" r="2.5" fill="var(--p)"/><rect x="168.5" y="26" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="190" cy="23" r="2.5" fill="var(--p)"/><rect x="188.5" y="26" width="3" height="5" rx="1" fill="var(--p)"/>

  <!-- 行3（21-30）：21-27高亮，28-30未亮 -->
  <circle cx="10" cy="39" r="2.5" fill="var(--p)"/><rect x="8.5" y="42" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="30" cy="39" r="2.5" fill="var(--p)"/><rect x="28.5" y="42" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="50" cy="39" r="2.5" fill="var(--p)"/><rect x="48.5" y="42" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="70" cy="39" r="2.5" fill="var(--p)"/><rect x="68.5" y="42" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="90" cy="39" r="2.5" fill="var(--p)"/><rect x="88.5" y="42" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="110" cy="39" r="2.5" fill="var(--p)"/><rect x="108.5" y="42" width="3" height="5" rx="1" fill="var(--p)"/>
  <circle cx="130" cy="39" r="2.5" fill="var(--p)"/><rect x="128.5" y="42" width="3" height="5" rx="1" fill="var(--p)"/>
  <!-- 28-30未高亮 -->
  <circle cx="150" cy="39" r="2.5" fill="rgba(255,255,255,0.1)"/><rect x="148.5" y="42" width="3" height="5" rx="1" fill="rgba(255,255,255,0.1)"/>
  <circle cx="170" cy="39" r="2.5" fill="rgba(255,255,255,0.1)"/><rect x="168.5" y="42" width="3" height="5" rx="1" fill="rgba(255,255,255,0.1)"/>
  <circle cx="190" cy="39" r="2.5" fill="rgba(255,255,255,0.1)"/><rect x="188.5" y="42" width="3" height="5" rx="1" fill="rgba(255,255,255,0.1)"/>

  <!-- 行4-7（31-70）：全部未高亮（简化写法：矩形块代替） -->
  <!-- 行4 -->
  <circle cx="10"  cy="55" r="2.5" fill="rgba(255,255,255,0.1)"/><rect x="8.5"   y="58" width="3" height="5" rx="1" fill="rgba(255,255,255,0.1)"/>
  <circle cx="30"  cy="55" r="2.5" fill="rgba(255,255,255,0.1)"/><rect x="28.5"  y="58" width="3" height="5" rx="1" fill="rgba(255,255,255,0.1)"/>
  <circle cx="50"  cy="55" r="2.5" fill="rgba(255,255,255,0.1)"/><rect x="48.5"  y="58" width="3" height="5" rx="1" fill="rgba(255,255,255,0.1)"/>
  <circle cx="70"  cy="55" r="2.5" fill="rgba(255,255,255,0.1)"/><rect x="68.5"  y="58" width="3" height="5" rx="1" fill="rgba(255,255,255,0.1)"/>
  <circle cx="90"  cy="55" r="2.5" fill="rgba(255,255,255,0.1)"/><rect x="88.5"  y="58" width="3" height="5" rx="1" fill="rgba(255,255,255,0.1)"/>
  <circle cx="110" cy="55" r="2.5" fill="rgba(255,255,255,0.1)"/><rect x="108.5" y="58" width="3" height="5" rx="1" fill="rgba(255,255,255,0.1)"/>
  <circle cx="130" cy="55" r="2.5" fill="rgba(255,255,255,0.1)"/><rect x="128.5" y="58" width="3" height="5" rx="1" fill="rgba(255,255,255,0.1)"/>
  <circle cx="150" cy="55" r="2.5" fill="rgba(255,255,255,0.1)"/><rect x="148.5" y="58" width="3" height="5" rx="1" fill="rgba(255,255,255,0.1)"/>
  <circle cx="170" cy="55" r="2.5" fill="rgba(255,255,255,0.1)"/><rect x="168.5" y="58" width="3" height="5" rx="1" fill="rgba(255,255,255,0.1)"/>
  <circle cx="190" cy="55" r="2.5" fill="rgba(255,255,255,0.1)"/><rect x="188.5" y="58" width="3" height="5" rx="1" fill="rgba(255,255,255,0.1)"/>

  <!-- 标注 -->
  <text x="0" y="77" font-size="9" fill="var(--p)" font-weight="700">27/100</text>
  <text x="50" y="77" font-size="8.5" fill="var(--dt)">人受影响</text>
  <rect x="130" y="70" width="7" height="7" rx="1" fill="var(--p)"/>
  <text x="141" y="77" font-size="7.5" fill="var(--dt)">受影响</text>
  <rect x="170" y="70" width="7" height="7" rx="1" fill="rgba(255,255,255,0.1)"/>
  <text x="181" y="77" font-size="7.5" fill="var(--dt)">未受影响</text>
</svg>
```

---

## 变体 B · 方格百格图（更紧凑，70px）

```html
<svg viewBox="0 0 205 70" style="width:100%;height:70px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 10×10 方格，每格 16×5px，间距1px -->
  <!-- 高亮前42格（42%） -->
  <!-- 行1（1-10，全亮） -->
  <rect x="0"   y="0" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="18"  y="0" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="36"  y="0" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="54"  y="0" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="72"  y="0" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="90"  y="0" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="108" y="0" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="126" y="0" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="144" y="0" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="162" y="0" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <!-- 行2（11-20，全亮） -->
  <rect x="0"   y="7" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="18"  y="7" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="36"  y="7" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="54"  y="7" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="72"  y="7" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="90"  y="7" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="108" y="7" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="126" y="7" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="144" y="7" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="162" y="7" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <!-- 行3（21-30，全亮） -->
  <rect x="0"   y="14" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="18"  y="14" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="36"  y="14" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="54"  y="14" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="72"  y="14" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="90"  y="14" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="108" y="14" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="126" y="14" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="144" y="14" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="162" y="14" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <!-- 行4（31-40，全亮） -->
  <rect x="0"   y="21" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="18"  y="21" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="36"  y="21" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="54"  y="21" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="72"  y="21" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="90"  y="21" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="108" y="21" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="126" y="21" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="144" y="21" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="162" y="21" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <!-- 行5（41-50，41-42亮，43-50暗） -->
  <rect x="0"   y="28" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="18"  y="28" width="16" height="5" rx="1" fill="var(--p)" opacity="0.9"/>
  <rect x="36"  y="28" width="16" height="5" rx="1" fill="rgba(255,255,255,0.08)"/>
  <rect x="54"  y="28" width="16" height="5" rx="1" fill="rgba(255,255,255,0.08)"/>
  <rect x="72"  y="28" width="16" height="5" rx="1" fill="rgba(255,255,255,0.08)"/>
  <rect x="90"  y="28" width="16" height="5" rx="1" fill="rgba(255,255,255,0.08)"/>
  <rect x="108" y="28" width="16" height="5" rx="1" fill="rgba(255,255,255,0.08)"/>
  <rect x="126" y="28" width="16" height="5" rx="1" fill="rgba(255,255,255,0.08)"/>
  <rect x="144" y="28" width="16" height="5" rx="1" fill="rgba(255,255,255,0.08)"/>
  <rect x="162" y="28" width="16" height="5" rx="1" fill="rgba(255,255,255,0.08)"/>
  <!-- 行6-10（51-100）：全暗 -->
  <rect x="0"  y="35" width="180" height="5"  rx="1" fill="rgba(255,255,255,0.08)"/>
  <rect x="0"  y="42" width="180" height="5"  rx="1" fill="rgba(255,255,255,0.08)"/>
  <rect x="0"  y="49" width="180" height="5"  rx="1" fill="rgba(255,255,255,0.08)"/>
  <rect x="0"  y="56" width="180" height="5"  rx="1" fill="rgba(255,255,255,0.08)"/>
  <rect x="0"  y="63" width="180" height="5"  rx="1" fill="rgba(255,255,255,0.08)"/>
  <!-- 注：行6-10用矩形整行简化，实际需要每格独立 -->

  <!-- 说明文字 -->
  <text x="188" y="20" font-size="22" font-weight="900" fill="var(--p)" text-anchor="middle">42%</text>
  <text x="188" y="32" font-size="7.5" fill="var(--dt)" text-anchor="middle">达标率</text>
  <text x="188" y="42" font-size="7" fill="var(--dt)" text-anchor="middle">100人中</text>
  <text x="188" y="52" font-size="7" fill="var(--dt)" text-anchor="middle">42人达标</text>
</svg>
```

**参数说明：**
- 变体A（人形）：每格20px宽，圆头r=2.5，身体3×5px
- 变体B（方格）：每格16×5px，间距1px，共10列×10行
- 高亮前N格（从左到右，从上到下）
- 高亮色=var(--p)；未高亮=rgba(255,255,255,0.08)
- 适合表示"N/100人"类概率数据
