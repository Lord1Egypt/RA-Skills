# pest · PEST/PESTLE 分析

**适用：** 宏观环境分析、外部因素扫描（政治/经济/社会/技术 ± 法律/环境）
**高度：** 260px

**结构公式：** 2×2（PEST）或 2×3（PESTLE）格，每格多条要点，带图标前缀。

---

## 变体 A · PEST 四象限（260px）

```html
<svg viewBox="0 0 700 260" style="width:100%;height:260px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 四格背景 -->
  <rect x="0"   y="0"   width="344" height="126" rx="5" fill="rgba(59,130,246,0.1)"  stroke="rgba(59,130,246,0.3)"  stroke-width="1.5"/>
  <rect x="356" y="0"   width="344" height="126" rx="5" fill="rgba(16,185,129,0.1)"  stroke="rgba(16,185,129,0.3)"  stroke-width="1.5"/>
  <rect x="0"   y="134" width="344" height="126" rx="5" fill="rgba(245,158,11,0.1)"  stroke="rgba(245,158,11,0.3)"  stroke-width="1.5"/>
  <rect x="356" y="134" width="344" height="126" rx="5" fill="rgba(139,92,246,0.1)"  stroke="rgba(139,92,246,0.3)"  stroke-width="1.5"/>

  <!-- P：政治（左上） -->
  <text x="12" y="20" font-size="22" font-weight="900" fill="#3b82f6">P</text>
  <text x="38" y="18" font-size="11"  font-weight="700" fill="#93c5fd">Political · 政治</text>
  <line x1="10" y1="25" x2="334" y2="25" stroke="rgba(59,130,246,0.25)" stroke-width="1"/>
  <text x="12" y="42"  font-size="8.5" fill="#93c5fd">🏛 监管政策收紧，合规投入↑30%</text>
  <text x="12" y="58"  font-size="8.5" fill="#93c5fd">📋 数据本地化法规扩至15国</text>
  <text x="12" y="74"  font-size="8.5" fill="#93c5fd">🌐 地缘博弈加剧，供应链重构</text>
  <text x="12" y="90"  font-size="8.5" fill="#93c5fd">💼 政府数字化采购预算+45%</text>
  <text x="12" y="106" font-size="8.5" fill="#93c5fd">⚖ 反垄断调查常态化</text>

  <!-- E：经济（右上） -->
  <text x="368" y="20" font-size="22" font-weight="900" fill="#10b981">E</text>
  <text x="394" y="18" font-size="11"  font-weight="700" fill="#6ee7b7">Economic · 经济</text>
  <line x1="366" y1="25" x2="690" y2="25" stroke="rgba(16,185,129,0.25)" stroke-width="1"/>
  <text x="368" y="42"  font-size="8.5" fill="#6ee7b7">📈 GDP增速预测 5.2%，需求稳健</text>
  <text x="368" y="58"  font-size="8.5" fill="#6ee7b7">💱 汇率波动区间±8%，汇兑风险</text>
  <text x="368" y="74"  font-size="8.5" fill="#6ee7b7">🏦 央行降息25bp，融资成本降低</text>
  <text x="368" y="90"  font-size="8.5" fill="#6ee7b7">📦 通胀回落至2.3%，消费回暖</text>
  <text x="368" y="106" font-size="8.5" fill="#6ee7b7">🔄 供应链多元化重塑成本结构</text>

  <!-- S：社会（左下） -->
  <text x="12" y="154" font-size="22" font-weight="900" fill="#f59e0b">S</text>
  <text x="38" y="152" font-size="11"  font-weight="700" fill="#fcd34d">Social · 社会</text>
  <line x1="10" y1="159" x2="334" y2="159" stroke="rgba(245,158,11,0.25)" stroke-width="1"/>
  <text x="12" y="176"  font-size="8.5" fill="#fcd34d">👥 Z世代成主力消费群，体验优先</text>
  <text x="12" y="192"  font-size="8.5" fill="#fcd34d">👴 老龄化率达20%，银发市场扩大</text>
  <text x="12" y="208"  font-size="8.5" fill="#fcd34d">🌱 ESG意识提升，绿色溢价+12%</text>
  <text x="12" y="224"  font-size="8.5" fill="#fcd34d">🏠 远程办公固化，SaaS需求长期化</text>
  <text x="12" y="240"  font-size="8.5" fill="#fcd34d">📱 平均屏幕时长7.2h/天，数字依赖</text>

  <!-- T：技术（右下） -->
  <text x="368" y="154" font-size="22" font-weight="900" fill="#8b5cf6">T</text>
  <text x="394" y="152" font-size="11"  font-weight="700" fill="#c4b5fd">Technology · 技术</text>
  <line x1="366" y1="159" x2="690" y2="159" stroke="rgba(139,92,246,0.25)" stroke-width="1"/>
  <text x="368" y="176"  font-size="8.5" fill="#c4b5fd">🤖 生成式AI渗透率年增180%</text>
  <text x="368" y="192"  font-size="8.5" fill="#c4b5fd">⚡ 算力成本3年内降至1/10</text>
  <text x="368" y="208"  font-size="8.5" fill="#c4b5fd">🔐 量子计算威胁现有加密体系</text>
  <text x="368" y="224"  font-size="8.5" fill="#c4b5fd">🌐 5G/6G加速边缘计算普及</text>
  <text x="368" y="240"  font-size="8.5" fill="#c4b5fd">🧬 数字孪生在制造业覆盖率62%</text>

  <!-- 中轴线 -->
  <line x1="350" y1="0"   x2="350" y2="260" stroke="rgba(255,255,255,0.1)" stroke-width="1.5"/>
  <line x1="0"   y1="130" x2="700" y2="130" stroke="rgba(255,255,255,0.1)" stroke-width="1.5"/>

  <!-- 中心标签 -->
  <rect x="324" y="114" width="52" height="32" rx="4" fill="var(--bg,#0f172a)" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
  <text x="350" y="128" text-anchor="middle" font-size="9"  fill="#64748b" font-weight="700">PEST</text>
  <text x="350" y="141" text-anchor="middle" font-size="7.5" fill="#475569">分析</text>
</svg>
```

**参数说明：**
- 四格各 344×126px，格间距 12px
- 每格：大字母（22px 900）+ 英文/中文标题 + 分隔线 + 5条要点（8.5px，行距16px）
- 要点带 emoji 前缀增强可读性（可替换为 ● 或数字序号）
- PESTLE 变体：改为 3×2 格，增加 L（法律）和 E2（环境）两格
- 整体 viewBox 宽 700px，匹配宽布局卡片
