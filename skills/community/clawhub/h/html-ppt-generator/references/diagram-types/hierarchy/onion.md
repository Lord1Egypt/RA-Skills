# onion · 同心圆/洋葱图

**适用：** 价值层次、产品核心-扩展-外围、技术依赖圈层、品牌感知圈
**高度：** 220px

**结构公式：** N 个同心圆共享圆心，从内到外依次代表核心→外围层级，每圈 opacity 递减。

```
构建规则：
  N 个同心圆共享圆心 (cx, cy)
  最内圈：核心价值，实色填充，r 最小（约 35–45px）
  向外每圈：opacity 递减 0.15 步长，r 递增 40–50px
  文字标签：在圆环中点 text-anchor="middle"（圆心y ± 偏移）
  可加扇形分割线（path arc）细分每圈为不同部分
```

```html
<svg viewBox="0 0 440 220" style="width:100%;height:220px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 圈4：最外层（基础设施/环境） -->
  <circle cx="220" cy="110" r="105" fill="rgba(99,102,241,0.08)" stroke="rgba(99,102,241,0.2)" stroke-width="1"/>
  <text x="220" y="20"  text-anchor="middle" font-size="9" fill="var(--dt)">外部环境</text>
  <!-- 圈3 -->
  <circle cx="220" cy="110" r="78"  fill="rgba(99,102,241,0.12)" stroke="rgba(99,102,241,0.25)" stroke-width="1"/>
  <text x="220" y="40"  text-anchor="middle" font-size="9" fill="var(--mt)">生态系统</text>
  <!-- 圈2 -->
  <circle cx="220" cy="110" r="52"  fill="rgba(99,102,241,0.2)"  stroke="rgba(99,102,241,0.35)" stroke-width="1.5"/>
  <text x="220" y="66"  text-anchor="middle" font-size="9.5" font-weight="600" fill="var(--t)">产品层</text>
  <!-- 圈1：核心 -->
  <circle cx="220" cy="110" r="30"  fill="var(--p)" opacity="0.9"/>
  <text x="220" y="107" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">核心</text>
  <text x="220" y="120" text-anchor="middle" font-size="8.5" fill="rgba(255,255,255,0.8)">价值</text>
  <!-- 右侧引线标注（可选） -->
  <line x1="302" y1="88" x2="340" y2="70" stroke="rgba(255,255,255,0.15)" stroke-width="0.8"/>
  <text x="344" y="68" font-size="8.5" fill="var(--dt)">产品功能</text>
  <line x1="325" y1="100" x2="360" y2="90" stroke="rgba(255,255,255,0.1)" stroke-width="0.8"/>
  <text x="364" y="88" font-size="8.5" fill="var(--dt)">合作伙伴</text>
  <line x1="324" y1="115" x2="360" y2="115" stroke="rgba(255,255,255,0.08)" stroke-width="0.8"/>
  <text x="364" y="118" font-size="8.5" fill="var(--dt)">市场环境</text>
</svg>
```

**扇形分割变体（每圈分为4扇）：**
```
每扇形：<path d="M cx,cy L cx+r,cy A r,r 0 0,1 cx,cy-r Z" fill="..." opacity="..."/>
rotate 变换实现旋转分区：transform="rotate(角度, cx, cy)"
4扇：0° / 90° / 180° / 270°；3扇：0° / 120° / 240°
```

**参数说明：**
- 各圈半径建议：核心 30px → 每圈 +26px（3圈=30/56/82px，4圈=30/56/82/108px）
- fill opacity 从内到外：0.9 → 0.2（4圈步长约 0.23）
- 圆心 cy = SVG高度/2（居中），cx = 视宽度留右侧标注空间而定
