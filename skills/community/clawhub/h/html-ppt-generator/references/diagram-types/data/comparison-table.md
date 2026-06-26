# comparison-table · 特性对比表

**适用：** 多方案/产品/竞品特性横向对比，带评分、勾叉、分值的结构化比较
**高度：** 自适应（每行 32px × 行数）

---

## 变体 A · 勾叉对比（4方案×6特性，220px）

```html
<svg viewBox="0 0 700 220" style="width:100%;height:220px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 表头背景 -->
  <rect x="0"   y="0" width="700" height="30" rx="4" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>

  <!-- 列标题 -->
  <text x="130" y="19" text-anchor="middle" font-size="10" font-weight="700" fill="var(--mt)">特性/功能</text>
  <rect x="270" y="3"  width="100" height="24" rx="4" fill="var(--p)" opacity="0.9"/>
  <text x="320" y="19" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">方案 A ★</text>
  <text x="450" y="19" text-anchor="middle" font-size="10" font-weight="600" fill="var(--mt)">方案 B</text>
  <text x="580" y="19" text-anchor="middle" font-size="10" font-weight="600" fill="var(--mt)">方案 C</text>
  <text x="668" y="19" text-anchor="middle" font-size="10" font-weight="600" fill="var(--mt)">方案 D</text>

  <!-- 行1：功能完整性 -->
  <rect x="0" y="32" width="700" height="28" rx="2" fill="rgba(255,255,255,0.02)"/>
  <text x="10"  y="50" font-size="9" fill="var(--dt)">功能完整性</text>
  <text x="320" y="50" text-anchor="middle" font-size="13" fill="#10b981">✓</text>
  <text x="450" y="50" text-anchor="middle" font-size="13" fill="#10b981">✓</text>
  <text x="580" y="50" text-anchor="middle" font-size="13" fill="#ef4444">✗</text>
  <text x="668" y="50" text-anchor="middle" font-size="13" fill="#f59e0b">△</text>

  <!-- 行2：性能表现 -->
  <rect x="0" y="62" width="700" height="28" rx="2" fill="rgba(255,255,255,0.01)"/>
  <text x="10"  y="80" font-size="9" fill="var(--dt)">性能 &lt; 100ms</text>
  <text x="320" y="80" text-anchor="middle" font-size="13" fill="#10b981">✓</text>
  <text x="450" y="80" text-anchor="middle" font-size="13" fill="#f59e0b">△</text>
  <text x="580" y="80" text-anchor="middle" font-size="13" fill="#10b981">✓</text>
  <text x="668" y="80" text-anchor="middle" font-size="13" fill="#ef4444">✗</text>

  <!-- 行3：安全合规 -->
  <rect x="0" y="92" width="700" height="28" rx="2" fill="rgba(255,255,255,0.02)"/>
  <text x="10"  y="110" font-size="9" fill="var(--dt)">安全合规 ISO27001</text>
  <text x="320" y="110" text-anchor="middle" font-size="13" fill="#10b981">✓</text>
  <text x="450" y="110" text-anchor="middle" font-size="13" fill="#10b981">✓</text>
  <text x="580" y="110" text-anchor="middle" font-size="13" fill="#ef4444">✗</text>
  <text x="668" y="110" text-anchor="middle" font-size="13" fill="#ef4444">✗</text>

  <!-- 行4：可扩展性 -->
  <rect x="0" y="122" width="700" height="28" rx="2" fill="rgba(255,255,255,0.01)"/>
  <text x="10"  y="140" font-size="9" fill="var(--dt)">水平扩展支持</text>
  <text x="320" y="140" text-anchor="middle" font-size="13" fill="#10b981">✓</text>
  <text x="450" y="140" text-anchor="middle" font-size="13" fill="#ef4444">✗</text>
  <text x="580" y="140" text-anchor="middle" font-size="13" fill="#10b981">✓</text>
  <text x="668" y="140" text-anchor="middle" font-size="13" fill="#f59e0b">△</text>

  <!-- 行5：成本 -->
  <rect x="0" y="152" width="700" height="28" rx="2" fill="rgba(255,255,255,0.02)"/>
  <text x="10"  y="170" font-size="9" fill="var(--dt)">年度成本</text>
  <text x="320" y="170" text-anchor="middle" font-size="9" fill="var(--t)" font-weight="700">¥80万</text>
  <text x="450" y="170" text-anchor="middle" font-size="9" fill="var(--mt)">¥120万</text>
  <text x="580" y="170" text-anchor="middle" font-size="9" fill="var(--mt)">¥95万</text>
  <text x="668" y="170" text-anchor="middle" font-size="9" fill="var(--mt)">¥60万</text>

  <!-- 行6：综合评分 -->
  <rect x="0" y="182" width="700" height="30" rx="2" fill="rgba(var(--p-rgb,99,102,241),0.06)"
        stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  <text x="10"  y="201" font-size="9" fill="var(--t)" font-weight="700">综合评分</text>
  <text x="320" y="201" text-anchor="middle" font-size="12" fill="var(--p)" font-weight="800">92</text>
  <text x="450" y="201" text-anchor="middle" font-size="12" fill="var(--mt)">74</text>
  <text x="580" y="201" text-anchor="middle" font-size="12" fill="var(--mt)">68</text>
  <text x="668" y="201" text-anchor="middle" font-size="12" fill="var(--mt)">55</text>

  <!-- 列分隔线 -->
  <line x1="262" y1="0" x2="262" y2="212" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  <line x1="392" y1="0" x2="392" y2="212" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  <line x1="522" y1="0" x2="522" y2="212" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  <line x1="630" y1="0" x2="630" y2="212" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>

  <!-- 图例 -->
  <text x="10"  y="218" font-size="7.5" fill="#10b981">✓ 支持</text>
  <text x="70"  y="218" font-size="7.5" fill="#f59e0b">△ 部分</text>
  <text x="130" y="218" font-size="7.5" fill="#ef4444">✗ 不支持</text>
  <text x="540" y="218" font-size="7.5" fill="var(--dt)">★ 推荐方案</text>
</svg>
```

---

## 变体 B · 评分条对比（3方案×5维度，180px）

```html
<svg viewBox="0 0 700 180" style="width:100%;height:180px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 表头 -->
  <rect x="0" y="0" width="700" height="26" rx="4" fill="rgba(255,255,255,0.04)"/>
  <text x="130" y="17" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--mt)">评估维度</text>
  <text x="340" y="17" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--p)">方案A</text>
  <text x="490" y="17" text-anchor="middle" font-size="9.5" font-weight="700" fill="#8b5cf6">方案B</text>
  <text x="630" y="17" text-anchor="middle" font-size="9.5" font-weight="700" fill="#10b981">方案C</text>

  <!-- 每行：维度名 + 3个评分条 -->
  <!-- 行1：技术成熟度 -->
  <text x="10" y="44" font-size="9" fill="var(--dt)">技术成熟度</text>
  <rect x="262" y="34" width="156" height="9" rx="4" fill="rgba(255,255,255,0.05)"/>
  <rect x="262" y="34" width="133" height="9" rx="4" fill="var(--p)" opacity="0.8"/><!-- 85% -->
  <text x="400" y="42" font-size="7.5" fill="var(--mt)">85</text>
  <rect x="414" y="34" width="152" height="9" rx="4" fill="rgba(255,255,255,0.05)"/>
  <rect x="414" y="34" width="107" height="9" rx="4" fill="#8b5cf6" opacity="0.8"/><!-- 70% -->
  <text x="523" y="42" font-size="7.5" fill="#c4b5fd">70</text>
  <rect x="558" y="34" width="134" height="9" rx="4" fill="rgba(255,255,255,0.05)"/>
  <rect x="558" y="34" width="107" height="9" rx="4" fill="#10b981" opacity="0.8"/><!-- 80% -->
  <text x="667" y="42" font-size="7.5" fill="#6ee7b7">80</text>

  <!-- 行2：实施周期 -->
  <text x="10" y="70" font-size="9" fill="var(--dt)">实施周期</text>
  <rect x="262" y="60" width="156" height="9" rx="4" fill="rgba(255,255,255,0.05)"/>
  <rect x="262" y="60" width="148" height="9" rx="4" fill="var(--p)" opacity="0.8"/><!-- 95% -->
  <text x="412" y="68" font-size="7.5" fill="var(--mt)">95</text>
  <rect x="414" y="60" width="152" height="9" rx="4" fill="rgba(255,255,255,0.05)"/>
  <rect x="414" y="60" width="91"  height="9" rx="4" fill="#8b5cf6" opacity="0.8"/><!-- 60% -->
  <text x="507" y="68" font-size="7.5" fill="#c4b5fd">60</text>
  <rect x="558" y="60" width="134" height="9" rx="4" fill="rgba(255,255,255,0.05)"/>
  <rect x="558" y="60" width="80"  height="9" rx="4" fill="#10b981" opacity="0.8"/><!-- 60% -->
  <text x="640" y="68" font-size="7.5" fill="#6ee7b7">60</text>

  <!-- 行3：成本控制 -->
  <text x="10" y="96" font-size="9" fill="var(--dt)">成本控制</text>
  <rect x="262" y="86" width="156" height="9" rx="4" fill="rgba(255,255,255,0.05)"/>
  <rect x="262" y="86" width="117" height="9" rx="4" fill="var(--p)" opacity="0.8"/><!-- 75% -->
  <text x="381" y="94" font-size="7.5" fill="var(--mt)">75</text>
  <rect x="414" y="86" width="152" height="9" rx="4" fill="rgba(255,255,255,0.05)"/>
  <rect x="414" y="86" width="122" height="9" rx="4" fill="#8b5cf6" opacity="0.8"/><!-- 80% -->
  <text x="538" y="94" font-size="7.5" fill="#c4b5fd">80</text>
  <rect x="558" y="86" width="134" height="9" rx="4" fill="rgba(255,255,255,0.05)"/>
  <rect x="558" y="86" width="128" height="9" rx="4" fill="#10b981" opacity="0.8"/><!-- 95% -->
  <text x="688" y="94" font-size="7.5" fill="#6ee7b7">95</text>

  <!-- 行4：团队适配度 -->
  <text x="10" y="122" font-size="9" fill="var(--dt)">团队适配度</text>
  <rect x="262" y="112" width="156" height="9" rx="4" fill="rgba(255,255,255,0.05)"/>
  <rect x="262" y="112" width="140" height="9" rx="4" fill="var(--p)" opacity="0.8"/><!-- 90% -->
  <text x="404" y="120" font-size="7.5" fill="var(--mt)">90</text>
  <rect x="414" y="112" width="152" height="9" rx="4" fill="rgba(255,255,255,0.05)"/>
  <rect x="414" y="112" width="99"  height="9" rx="4" fill="#8b5cf6" opacity="0.8"/><!-- 65% -->
  <text x="515" y="120" font-size="7.5" fill="#c4b5fd">65</text>
  <rect x="558" y="112" width="134" height="9" rx="4" fill="rgba(255,255,255,0.05)"/>
  <rect x="558" y="112" width="101" height="9" rx="4" fill="#10b981" opacity="0.8"/><!-- 75% -->
  <text x="661" y="120" font-size="7.5" fill="#6ee7b7">75</text>

  <!-- 行5：风险评估 -->
  <text x="10" y="148" font-size="9" fill="var(--dt)">风险评估</text>
  <rect x="262" y="138" width="156" height="9" rx="4" fill="rgba(255,255,255,0.05)"/>
  <rect x="262" y="138" width="133" height="9" rx="4" fill="var(--p)" opacity="0.8"/><!-- 85% -->
  <text x="397" y="146" font-size="7.5" fill="var(--mt)">85</text>
  <rect x="414" y="138" width="152" height="9" rx="4" fill="rgba(255,255,255,0.05)"/>
  <rect x="414" y="138" width="114" height="9" rx="4" fill="#8b5cf6" opacity="0.8"/><!-- 75% -->
  <text x="530" y="146" font-size="7.5" fill="#c4b5fd">75</text>
  <rect x="558" y="138" width="134" height="9" rx="4" fill="rgba(255,255,255,0.05)"/>
  <rect x="558" y="138" width="87"  height="9" rx="4" fill="#10b981" opacity="0.8"/><!-- 65% -->
  <text x="647" y="146" font-size="7.5" fill="#6ee7b7">65</text>

  <!-- 综合得分 -->
  <rect x="0" y="155" width="700" height="25" rx="3" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  <text x="10"  y="172" font-size="9" fill="var(--t)" font-weight="700">综合加权得分</text>
  <text x="340" y="172" text-anchor="middle" font-size="12" fill="var(--p)" font-weight="800">86</text>
  <text x="490" y="172" text-anchor="middle" font-size="12" fill="#8b5cf6" font-weight="700">70</text>
  <text x="630" y="172" text-anchor="middle" font-size="12" fill="#10b981" font-weight="700">75</text>

  <!-- 列线 -->
  <line x1="256" y1="0" x2="256" y2="180" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  <line x1="408" y1="0" x2="408" y2="180" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  <line x1="552" y1="0" x2="552" y2="180" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
</svg>
```

**参数说明：**
- 行高 30px（表头 26px），总高 = 行数 × 30 + 26
- 评分条宽度 = 列宽 × (分数/100)；满分 = 156px（列宽）
- 推荐方案列加高亮背景 `fill="var(--p)"` 替换表头
- ✓/✗/△ 符号字号 13px，对齐列中心 text-anchor="middle"
