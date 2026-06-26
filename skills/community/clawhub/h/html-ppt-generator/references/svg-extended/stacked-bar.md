# stacked-bar · 堆积条形图

**适用：** 多维度占比分解、成分构成、100%堆积对比
**高度：** 50px（单行）/ 90px（多行对比）

---

## 变体 A · 单行堆积（50px）

```html
<svg viewBox="0 0 290 50" style="width:100%;height:50px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 标签 -->
  <text x="0" y="10" font-size="8.5" fill="#64748b" font-weight="600">指标分布</text>
  <!-- 堆积条（总宽244px，从x=46开始，总100%） -->
  <!-- 段1：50% → 122px -->
  <rect x="46"  y="14" width="122" height="12" rx="2" fill="var(--p)" opacity="0.9"/>
  <text x="107" y="23" text-anchor="middle" font-size="7.5" fill="#fff" font-weight="700">50%</text>
  <!-- 段2：25% → 61px -->
  <rect x="168" y="14" width="61"  height="12" rx="0" fill="#8b5cf6" opacity="0.85"/>
  <text x="199" y="23" text-anchor="middle" font-size="7.5" fill="#fff" font-weight="700">25%</text>
  <!-- 段3：15% → 37px -->
  <rect x="229" y="14" width="37"  height="12" rx="0" fill="#10b981" opacity="0.85"/>
  <text x="247" y="23" text-anchor="middle" font-size="7.5" fill="#fff" font-weight="700">15%</text>
  <!-- 段4：10% → 24px -->
  <rect x="266" y="14" width="24"  height="12" rx="2" fill="#f59e0b" opacity="0.85"/>
  <!-- 图例 -->
  <rect x="46"  y="32" width="7" height="7" rx="1" fill="var(--p)"/>
  <text x="57"  y="39" font-size="7.5" fill="#64748b">A 50%</text>
  <rect x="100" y="32" width="7" height="7" rx="1" fill="#8b5cf6"/>
  <text x="111" y="39" font-size="7.5" fill="#64748b">B 25%</text>
  <rect x="155" y="32" width="7" height="7" rx="1" fill="#10b981"/>
  <text x="166" y="39" font-size="7.5" fill="#64748b">C 15%</text>
  <rect x="210" y="32" width="7" height="7" rx="1" fill="#f59e0b"/>
  <text x="221" y="39" font-size="7.5" fill="#64748b">D 10%</text>
</svg>
```

---

## 变体 B · 多行堆积对比（90px，3组）

```html
<svg viewBox="0 0 290 90" style="width:100%;height:90px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 列标签 -->
  <text x="0" y="8" font-size="7.5" fill="#64748b">2022</text>
  <!-- 行1（2022）：总244px -->
  <rect x="36" y="10" width="98"  height="14" rx="0" fill="var(--p)"  opacity="0.9"/>
  <rect x="134" y="10" width="73" height="14" rx="0" fill="#8b5cf6"  opacity="0.85"/>
  <rect x="207" y="10" width="49" height="14" rx="2" fill="#10b981"  opacity="0.85"/>
  <rect x="36"  y="10" width="4"  height="14" rx="2" fill="var(--p)"  opacity="0.9"/><!-- 左圆角 -->
  <text x="85"  y="20" text-anchor="middle" font-size="7.5" fill="#fff">40%</text>
  <text x="171" y="20" text-anchor="middle" font-size="7.5" fill="#fff">30%</text>
  <text x="232" y="20" text-anchor="middle" font-size="7.5" fill="#fff">20%</text>

  <text x="0" y="38" font-size="7.5" fill="#64748b">2023</text>
  <!-- 行2（2023） -->
  <rect x="36" y="28" width="122" height="14" rx="0" fill="var(--p)"  opacity="0.9"/>
  <rect x="158" y="28" width="61"  height="14" rx="0" fill="#8b5cf6"  opacity="0.85"/>
  <rect x="219" y="28" width="37"  height="14" rx="2" fill="#10b981"  opacity="0.85"/>
  <rect x="36"  y="28" width="4"   height="14" rx="2" fill="var(--p)"  opacity="0.9"/>
  <text x="97"  y="38" text-anchor="middle" font-size="7.5" fill="#fff">50%</text>
  <text x="189" y="38" text-anchor="middle" font-size="7.5" fill="#fff">25%</text>
  <text x="238" y="38" text-anchor="middle" font-size="7.5" fill="#fff">15%</text>

  <text x="0" y="56" font-size="7.5" fill="#64748b">2024</text>
  <!-- 行3（2024） -->
  <rect x="36" y="46" width="146" height="14" rx="0" fill="var(--p)"  opacity="0.9"/>
  <rect x="182" y="46" width="49"  height="14" rx="0" fill="#8b5cf6"  opacity="0.85"/>
  <rect x="231" y="46" width="30"  height="14" rx="2" fill="#ef4444"  opacity="0.85"/>
  <rect x="36"  y="46" width="4"   height="14" rx="2" fill="var(--p)"  opacity="0.9"/>
  <text x="109" y="56" text-anchor="middle" font-size="7.5" fill="#fff">60%</text>
  <text x="207" y="56" text-anchor="middle" font-size="7.5" fill="#fff">20%</text>
  <text x="246" y="56" text-anchor="middle" font-size="7.5" fill="#fff">12%</text>

  <!-- 图例 -->
  <rect x="36"  y="70" width="7" height="7" rx="1" fill="var(--p)"/>
  <text x="47"  y="77" font-size="7.5" fill="#64748b">主要</text>
  <rect x="90"  y="70" width="7" height="7" rx="1" fill="#8b5cf6"/>
  <text x="101" y="77" font-size="7.5" fill="#64748b">次要</text>
  <rect x="145" y="70" width="7" height="7" rx="1" fill="#10b981"/>
  <text x="156" y="77" font-size="7.5" fill="#64748b">其他</text>
  <rect x="200" y="70" width="7" height="7" rx="1" fill="#ef4444"/>
  <text x="211" y="77" font-size="7.5" fill="#64748b">异常</text>
</svg>
```

**参数说明：**
- 总可用宽 244px（x:46–290），每段宽 = 244 × 占比
- 段之间无缝衔接（第N段 x = 46 + 前面所有段宽之和）
- 最左段左端加圆角 rx=2，最右段右端加圆角 rx=2
- 段内文字居中：x = 段起点 + 段宽/2
