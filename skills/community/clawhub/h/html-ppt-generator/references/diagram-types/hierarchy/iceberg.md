# iceberg · 冰山模型

**适用：** 显性/隐性分析、能力冰山、文化冰山、问题根因的深层结构展示
**高度：** 240px

**结构公式：** 水面线分割上下区域；水面以上为可见部分（1–2层），水面以下为隐藏部分（3–5层），越往下越宽，每层梯形。

```html
<svg viewBox="0 0 700 240" style="width:100%;height:240px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- 水面渐变 -->
    <linearGradient id="waterGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0ea5e9" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#0369a1" stop-opacity="0.5"/>
    </linearGradient>
    <!-- 冰山主体渐变 -->
    <linearGradient id="iceGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#e2e8f0" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#94a3b8" stop-opacity="0.7"/>
    </linearGradient>
  </defs>

  <!-- 水面以上：可见部分（三角形顶部） -->
  <!-- 层1 顶峰（最小，可见行为） -->
  <polygon points="350,4 410,72 290,72" fill="rgba(255,255,255,0.15)" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>
  <text x="350" y="44" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--t)">可见行为</text>
  <text x="350" y="58" text-anchor="middle" font-size="8.5" fill="var(--dt)">技能 · 结果 · 言语</text>

  <!-- 水面线 -->
  <rect x="0" y="72" width="700" height="3" fill="url(#waterGrad)"/>
  <text x="10" y="82" font-size="8" fill="#0ea5e9">水 面 · 可 见 约 10%</text>
  <line x1="0" y1="75" x2="700" y2="75" stroke="#0ea5e9" stroke-width="0.5" stroke-dasharray="4,3" opacity="0.6"/>

  <!-- 水面标注波纹 -->
  <path d="M0,75 Q87,68 175,75 Q262,82 350,75 Q437,68 525,75 Q612,82 700,75"
        fill="none" stroke="#0ea5e9" stroke-width="1" opacity="0.4"/>

  <!-- 水面以下背景（蓝色水体） -->
  <rect x="0" y="75" width="700" height="165" fill="rgba(14,165,233,0.06)"/>

  <!-- 层2：态度与知识（略宽） -->
  <polygon points="280,78 420,78 450,118 250,118"
           fill="rgba(99,102,241,0.2)" stroke="rgba(99,102,241,0.5)" stroke-width="1.2"/>
  <text x="350" y="100" text-anchor="middle" font-size="9.5" fill="#a5b4fc" font-weight="700">态度 · 知识</text>
  <text x="350" y="113" text-anchor="middle" font-size="8" fill="var(--dt)">认知框架 · 显性知识</text>

  <!-- 层3：价值观（更宽） -->
  <polygon points="240,122 460,122 500,162 200,162"
           fill="rgba(59,130,246,0.2)" stroke="rgba(59,130,246,0.5)" stroke-width="1.2"/>
  <text x="350" y="143" text-anchor="middle" font-size="9.5" fill="#93c5fd" font-weight="700">价值观 · 信念</text>
  <text x="350" y="157" text-anchor="middle" font-size="8" fill="var(--dt)">思维方式 · 假设前提</text>

  <!-- 层4：深层动机（更宽） -->
  <polygon points="190,166 510,166 555,200 145,200"
           fill="rgba(8,145,178,0.2)" stroke="rgba(8,145,178,0.5)" stroke-width="1.2"/>
  <text x="350" y="185" text-anchor="middle" font-size="9.5" fill="#67e8f9" font-weight="700">深层动机 · 潜意识模式</text>
  <text x="350" y="198" text-anchor="middle" font-size="8" fill="var(--dt)">自我认同 · 内在驱动</text>

  <!-- 层5：最深（底部，最宽） -->
  <polygon points="135,203 565,203 610,235 90,235"
           fill="rgba(2,132,199,0.18)" stroke="rgba(2,132,199,0.4)" stroke-width="1.2"/>
  <text x="350" y="223" text-anchor="middle" font-size="9.5" fill="#38bdf8" font-weight="700">根本假设 · 文化底层逻辑</text>

  <!-- 左侧标注 -->
  <text x="4" y="50" font-size="8" fill="var(--mt)" font-weight="700">可见层</text>
  <text x="4" y="62" font-size="7.5" fill="#64748b">约 10%</text>
  <line x1="78" y1="48" x2="280" y2="40" stroke="#475569" stroke-width="0.8" stroke-dasharray="3,2"/>

  <text x="4" y="110" font-size="8" fill="var(--mt)" font-weight="700">隐藏层</text>
  <text x="4" y="122" font-size="7.5" fill="#64748b">约 90%</text>
  <line x1="78" y1="108" x2="240" y2="100" stroke="#475569" stroke-width="0.8" stroke-dasharray="3,2"/>

  <!-- 百分比标注 -->
  <text x="692" y="50"  text-anchor="end" font-size="8" fill="var(--dt)">10%</text>
  <text x="692" y="100" text-anchor="end" font-size="8" fill="var(--dt)">30%</text>
  <text x="692" y="145" text-anchor="end" font-size="8" fill="var(--dt)">55%</text>
  <text x="692" y="185" text-anchor="end" font-size="8" fill="var(--dt)">75%</text>
  <text x="692" y="220" text-anchor="end" font-size="8" fill="var(--dt)">90%</text>
</svg>
```

**参数说明：**
- 水面线固定在 y=75（约占总高30%以上为可见区）
- 梯形每层比上层宽约 40–50px（左右各扩 20–25px）
- 越往下颜色越深（从白→浅蓝→深蓝），alpha 叠加
- 层数建议 4–6 层；水面以上 1–2 层，以下 3–4 层
- 左侧竖向标注可见/隐藏百分比；右侧可加累积百分比
