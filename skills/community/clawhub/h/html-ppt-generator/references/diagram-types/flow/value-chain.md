# value-chain · 价值链分析

**适用：** 波特价值链、业务活动分解、成本/价值贡献分析、竞争优势来源识别
**高度：** 220px

**结构公式：** 底部支持活动（水平色带）+ 顶部主要活动（箭头形色块序列）+ 右端利润箭头。

```html
<svg viewBox="0 0 860 220" style="width:100%;height:220px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- ===主要活动（上部，5个梯形箭头）=== -->
  <!-- 活动1：采购 -->
  <polygon points="0,10 148,10 165,60 148,110 0,110" fill="rgba(59,130,246,0.15)" stroke="rgba(59,130,246,0.4)" stroke-width="1.5"/>
  <text x="78"  y="52" text-anchor="middle" font-size="9.5" font-weight="700" fill="#93c5fd">进货物流</text>
  <text x="78"  y="66" text-anchor="middle" font-size="8"   fill="var(--dt)">采购 · 验收</text>
  <text x="78"  y="80" text-anchor="middle" font-size="8"   fill="var(--dt)">库存管理</text>
  <text x="78"  y="96" text-anchor="middle" font-size="8"   fill="#60a5fa">成本占比 12%</text>

  <!-- 活动2：生产 -->
  <polygon points="168,10 316,10 333,60 316,110 168,110 185,60" fill="rgba(139,92,246,0.15)" stroke="rgba(139,92,246,0.4)" stroke-width="1.5"/>
  <text x="250" y="52" text-anchor="middle" font-size="9.5" font-weight="700" fill="#c4b5fd">生产运营</text>
  <text x="250" y="66" text-anchor="middle" font-size="8"   fill="var(--dt)">制造 · 装配</text>
  <text x="250" y="80" text-anchor="middle" font-size="8"   fill="var(--dt)">质量控制</text>
  <text x="250" y="96" text-anchor="middle" font-size="8"   fill="#a78bfa">成本占比 35%</text>

  <!-- 活动3：出货物流 -->
  <polygon points="336,10 484,10 501,60 484,110 336,110 353,60" fill="rgba(6,182,212,0.15)" stroke="rgba(6,182,212,0.4)" stroke-width="1.5"/>
  <text x="418" y="52" text-anchor="middle" font-size="9.5" font-weight="700" fill="#67e8f9">出货物流</text>
  <text x="418" y="66" text-anchor="middle" font-size="8"   fill="var(--dt)">配送 · 仓储</text>
  <text x="418" y="80" text-anchor="middle" font-size="8"   fill="var(--dt)">订单处理</text>
  <text x="418" y="96" text-anchor="middle" font-size="8"   fill="#22d3ee">成本占比 18%</text>

  <!-- 活动4：市场营销 -->
  <polygon points="504,10 652,10 669,60 652,110 504,110 521,60" fill="rgba(245,158,11,0.15)" stroke="rgba(245,158,11,0.4)" stroke-width="1.5"/>
  <text x="582" y="52" text-anchor="middle" font-size="9.5" font-weight="700" fill="#fcd34d">市场营销</text>
  <text x="582" y="66" text-anchor="middle" font-size="8"   fill="var(--dt)">品牌 · 广告</text>
  <text x="582" y="80" text-anchor="middle" font-size="8"   fill="var(--dt)">渠道管理</text>
  <text x="582" y="96" text-anchor="middle" font-size="8"   fill="#fbbf24">成本占比 22%</text>

  <!-- 活动5：服务 -->
  <polygon points="672,10 760,10 777,60 760,110 672,110 689,60" fill="rgba(16,185,129,0.15)" stroke="rgba(16,185,129,0.4)" stroke-width="1.5"/>
  <text x="722" y="52" text-anchor="middle" font-size="9.5" font-weight="700" fill="#6ee7b7">售后服务</text>
  <text x="722" y="66" text-anchor="middle" font-size="8"   fill="var(--dt)">客服 · 维修</text>
  <text x="722" y="80" text-anchor="middle" font-size="8"   fill="var(--dt)">退换货</text>
  <text x="722" y="96" text-anchor="middle" font-size="8"   fill="#34d399">成本占比 8%</text>

  <!-- 利润箭头 -->
  <polygon points="780,10 860,10 860,110 780,110 797,60" fill="rgba(239,68,68,0.2)" stroke="rgba(239,68,68,0.5)" stroke-width="1.5"/>
  <text x="828" y="52" text-anchor="middle" font-size="9.5" font-weight="700" fill="#fca5a5">利润</text>
  <text x="828" y="68" text-anchor="middle" font-size="11"  font-weight="900" fill="#ef4444">毛利</text>
  <text x="828" y="83" text-anchor="middle" font-size="11"  font-weight="900" fill="#ef4444">42%</text>

  <!-- 标题行 -->
  <text x="430" y="7" text-anchor="middle" font-size="8" fill="#64748b">主要活动（Primary Activities）</text>

  <!-- ===支持活动（下部，4个色带）=== -->
  <text x="430" y="128" text-anchor="middle" font-size="8" fill="#64748b">支持活动（Support Activities）</text>

  <!-- 支持1：企业基础设施 -->
  <rect x="0" y="132" width="860" height="18" rx="3" fill="rgba(100,116,139,0.15)" stroke="rgba(100,116,139,0.3)" stroke-width="1"/>
  <text x="10"  y="145" font-size="8.5" font-weight="700" fill="#94a3b8">企业基础设施</text>
  <text x="200" y="145" font-size="8" fill="#64748b">财务 · 法务 · 战略规划 · IT基础设施 · 行政管理</text>

  <!-- 支持2：人力资源管理 -->
  <rect x="0" y="152" width="860" height="18" rx="3" fill="rgba(139,92,246,0.1)" stroke="rgba(139,92,246,0.2)" stroke-width="1"/>
  <text x="10"  y="165" font-size="8.5" font-weight="700" fill="#a78bfa">人力资源管理</text>
  <text x="200" y="165" font-size="8" fill="#64748b">招聘 · 培训 · 绩效考核 · 薪酬激励 · 文化建设</text>

  <!-- 支持3：技术开发 -->
  <rect x="0" y="172" width="860" height="18" rx="3" fill="rgba(59,130,246,0.1)" stroke="rgba(59,130,246,0.2)" stroke-width="1"/>
  <text x="10"  y="185" font-size="8.5" font-weight="700" fill="#93c5fd">技术开发 R&amp;D</text>
  <text x="200" y="185" font-size="8" fill="#64748b">产品研发 · 工艺改进 · 专利保护 · 数字化转型</text>

  <!-- 支持4：采购管理 -->
  <rect x="0" y="192" width="860" height="18" rx="3" fill="rgba(16,185,129,0.1)" stroke="rgba(16,185,129,0.2)" stroke-width="1"/>
  <text x="10"  y="205" font-size="8.5" font-weight="700" fill="#6ee7b7">采购管理</text>
  <text x="200" y="205" font-size="8" fill="#64748b">供应商管理 · 战略寻源 · 合同谈判 · 质量认证</text>

  <!-- 竞争优势标注 -->
  <rect x="580" y="157" width="120" height="14" rx="3" fill="rgba(239,68,68,0.12)" stroke="rgba(239,68,68,0.3)" stroke-width="1"/>
  <text x="640" y="168" text-anchor="middle" font-size="7.5" fill="#fca5a5">★ 核心竞争优势</text>
</svg>
```

**参数说明：**
- 主要活动：5个梯形箭头（polygon）水平排列，每个宽约 148–168px
- 梯形右端点 x = 下个活动左端点 - 3px（留间隙）
- 利润块用右端矩形（最后一块）
- 支持活动：4个水平色带，高18px，从 y=132 起，间距0
- 每条支持活动：左端标题（font-weight:700），右侧说明文字
- 价值链viewBox用 860px 宽以容纳5个主要活动
