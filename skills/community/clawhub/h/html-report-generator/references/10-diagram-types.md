# 10 · 业务图谱库（Architecture / Flow / Data / Hierarchy / Decision）

> 覆盖汇报场景五大图谱族。每类给出：识别关键词 + SVG 结构公式 + 完整代码示例。
> 若用户要求的图谱不在本库 → 执行末尾的【网络查询流程】。

---

## ⚡ 快速选型表

| 用户说了什么 | 图谱族 | 首选类型 |
|------------|--------|---------|
| 系统结构、微服务、组件关系、网络拓扑 | 架构图 | 分层架构 / C4 上下文图 |
| 流程、审批、跨部门协作、漏斗、路线图 | 流程图 | 泳道图 / 漏斗图 / 时间轴 |
| 流向、分配、占比、预算拆解 | 进阶数据图 | Sankey / Treemap / Bullet |
| 组织、汇报关系、优先级、市场矩阵 | 层级分析 | 金字塔 / 2×2矩阵 / 同心圆 |
| 决策、风险、任务分配、选项对比 | 决策图 | 风险矩阵 / 决策树 / RACI |

---

## 一、架构图族

### 1a · 分层架构图（Layered Architecture）

**结构公式**：N 个水平色带从上到下，每带内左右排列组件方块，带间连接箭头。

```html
<svg viewBox="0 0 940 220" style="width:100%;height:220px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="la-arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#64748b"/>
    </marker>
  </defs>
  <!-- 层1：表现层 -->
  <rect x="0" y="0" width="940" height="52" rx="4" fill="rgba(59,130,246,0.1)" stroke="rgba(59,130,246,0.3)" stroke-width="1"/>
  <text x="10" y="14" font-size="9" font-weight="700" fill="#3b82f6" text-transform="uppercase" letter-spacing="1">PRESENTATION</text>
  <rect x="120" y="8" width="140" height="34" rx="4" fill="rgba(59,130,246,0.2)" stroke="rgba(59,130,246,0.4)" stroke-width="1"/>
  <text x="190" y="29" text-anchor="middle" font-size="10" font-weight="600" fill="#93c5fd">Web App</text>
  <rect x="280" y="8" width="140" height="34" rx="4" fill="rgba(59,130,246,0.2)" stroke="rgba(59,130,246,0.4)" stroke-width="1"/>
  <text x="350" y="29" text-anchor="middle" font-size="10" font-weight="600" fill="#93c5fd">Mobile App</text>
  <rect x="440" y="8" width="140" height="34" rx="4" fill="rgba(59,130,246,0.2)" stroke="rgba(59,130,246,0.4)" stroke-width="1"/>
  <text x="510" y="29" text-anchor="middle" font-size="10" font-weight="600" fill="#93c5fd">Admin Portal</text>
  <!-- 层2：应用层 -->
  <rect x="0" y="58" width="940" height="52" rx="4" fill="rgba(139,92,246,0.1)" stroke="rgba(139,92,246,0.3)" stroke-width="1"/>
  <text x="10" y="72" font-size="9" font-weight="700" fill="#8b5cf6">APPLICATION</text>
  <rect x="120" y="66" width="140" height="34" rx="4" fill="rgba(139,92,246,0.2)" stroke="rgba(139,92,246,0.4)" stroke-width="1"/>
  <text x="190" y="87" text-anchor="middle" font-size="10" font-weight="600" fill="#c4b5fd">API Gateway</text>
  <rect x="280" y="66" width="140" height="34" rx="4" fill="rgba(139,92,246,0.2)" stroke="rgba(139,92,246,0.4)" stroke-width="1"/>
  <text x="350" y="87" text-anchor="middle" font-size="10" font-weight="600" fill="#c4b5fd">Auth Service</text>
  <rect x="440" y="66" width="140" height="34" rx="4" fill="rgba(139,92,246,0.2)" stroke="rgba(139,92,246,0.4)" stroke-width="1"/>
  <text x="510" y="87" text-anchor="middle" font-size="10" font-weight="600" fill="#c4b5fd">Business Logic</text>
  <rect x="600" y="66" width="140" height="34" rx="4" fill="rgba(139,92,246,0.2)" stroke="rgba(139,92,246,0.4)" stroke-width="1"/>
  <text x="670" y="87" text-anchor="middle" font-size="10" font-weight="600" fill="#c4b5fd">Message Queue</text>
  <!-- 层3：数据层 -->
  <rect x="0" y="116" width="940" height="52" rx="4" fill="rgba(6,182,212,0.1)" stroke="rgba(6,182,212,0.3)" stroke-width="1"/>
  <text x="10" y="130" font-size="9" font-weight="700" fill="#06b6d4">DATA</text>
  <rect x="120" y="124" width="140" height="34" rx="4" fill="rgba(6,182,212,0.2)" stroke="rgba(6,182,212,0.4)" stroke-width="1"/>
  <text x="190" y="145" text-anchor="middle" font-size="10" font-weight="600" fill="#67e8f9">PostgreSQL</text>
  <rect x="280" y="124" width="140" height="34" rx="4" fill="rgba(6,182,212,0.2)" stroke="rgba(6,182,212,0.4)" stroke-width="1"/>
  <text x="350" y="145" text-anchor="middle" font-size="10" font-weight="600" fill="#67e8f9">Redis Cache</text>
  <rect x="440" y="124" width="140" height="34" rx="4" fill="rgba(6,182,212,0.2)" stroke="rgba(6,182,212,0.4)" stroke-width="1"/>
  <text x="510" y="145" text-anchor="middle" font-size="10" font-weight="600" fill="#67e8f9">Object Storage</text>
  <!-- 层间箭头 -->
  <line x1="190" y1="42" x2="190" y2="66" stroke="#64748b" stroke-width="1.5" marker-end="url(#la-arr)"/>
  <line x1="350" y1="42" x2="350" y2="66" stroke="#64748b" stroke-width="1.5" marker-end="url(#la-arr)"/>
  <line x1="510" y1="42" x2="510" y2="66" stroke="#64748b" stroke-width="1.5" marker-end="url(#la-arr)"/>
  <line x1="190" y1="100" x2="190" y2="124" stroke="#64748b" stroke-width="1.5" marker-end="url(#la-arr)"/>
  <line x1="350" y1="100" x2="350" y2="124" stroke="#64748b" stroke-width="1.5" marker-end="url(#la-arr)"/>
  <!-- 图例 -->
  <rect x="750" y="10" width="10" height="10" rx="2" fill="rgba(59,130,246,0.4)"/>
  <text x="764" y="19" font-size="8.5" fill="#64748b">表现层</text>
  <rect x="750" y="28" width="10" height="10" rx="2" fill="rgba(139,92,246,0.4)"/>
  <text x="764" y="37" font-size="8.5" fill="#64748b">应用层</text>
  <rect x="750" y="46" width="10" height="10" rx="2" fill="rgba(6,182,212,0.4)"/>
  <text x="764" y="55" font-size="8.5" fill="#64748b">数据层</text>
  <!-- 层4标签 -->
  <text x="470" y="185" text-anchor="middle" font-size="9" fill="#475569">▲ 根据实际层数增减，每层高度 = (580 - padding) ÷ N，间距 6px</text>
</svg>
```

### 1b · C4 上下文图（System Context）

**结构公式**：中心系统大框 + 四周用户/外部系统小框 + 双向或单向标注箭头。

```
布局规则：
  中心系统：约 200×80px，主色填充，置于 SVG 中央
  外部角色：80×40px 小框，围绕中心排布（上/下/左/右 各 1-2 个）
  连接线：带标注的曲线 path，label 说明数据流向
  外部系统：虚线边框区分于内部系统
```

---

## 二、流程图族

### 2a · 泳道图（Swimlane / Cross-functional）

**结构公式**：竖向分隔为 N 个泳道（每道代表一个角色），每道内水平排列流程步骤，跨道箭头表示交接。

```html
<svg viewBox="0 0 940 200" style="width:100%;height:200px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="sw-arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#475569"/>
    </marker>
  </defs>
  <!-- 泳道背景 -->
  <rect x="0" y="0" width="940" height="200" fill="rgba(255,255,255,0.02)" stroke="rgba(255,255,255,0.06)" stroke-width="1" rx="4"/>
  <!-- 泳道1：客户 -->
  <rect x="0" y="0" width="70" height="66" fill="rgba(59,130,246,0.15)" stroke="rgba(59,130,246,0.2)" stroke-width="1"/>
  <text x="35" y="37" text-anchor="middle" font-size="9" font-weight="700" fill="#3b82f6" transform="rotate(-0,35,37)">客户</text>
  <rect x="0" y="66" width="70" height="67" fill="rgba(139,92,246,0.12)" stroke="rgba(139,92,246,0.2)" stroke-width="1"/>
  <text x="35" y="103" text-anchor="middle" font-size="9" font-weight="700" fill="#8b5cf6">销售</text>
  <rect x="0" y="133" width="70" height="67" fill="rgba(16,185,129,0.12)" stroke="rgba(16,185,129,0.2)" stroke-width="1"/>
  <text x="35" y="170" text-anchor="middle" font-size="9" font-weight="700" fill="#10b981">财务</text>
  <!-- 分割线 -->
  <line x1="0" y1="66" x2="940" y2="66" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  <line x1="0" y1="133" x2="940" y2="133" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  <line x1="70" y1="0" x2="70" y2="200" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
  <!-- 步骤：客户道 -->
  <rect x="90" y="16" width="100" height="34" rx="5" fill="rgba(59,130,246,0.2)" stroke="rgba(59,130,246,0.4)" stroke-width="1"/>
  <text x="140" y="37" text-anchor="middle" font-size="9.5" font-weight="600" fill="#93c5fd">提交需求</text>
  <rect x="400" y="16" width="100" height="34" rx="5" fill="rgba(59,130,246,0.2)" stroke="rgba(59,130,246,0.4)" stroke-width="1"/>
  <text x="450" y="37" text-anchor="middle" font-size="9.5" font-weight="600" fill="#93c5fd">确认方案</text>
  <rect x="720" y="16" width="100" height="34" rx="5" fill="rgba(59,130,246,0.2)" stroke="rgba(59,130,246,0.4)" stroke-width="1"/>
  <text x="770" y="37" text-anchor="middle" font-size="9.5" font-weight="600" fill="#93c5fd">验收签字</text>
  <!-- 步骤：销售道 -->
  <rect x="245" y="82" width="100" height="34" rx="5" fill="rgba(139,92,246,0.2)" stroke="rgba(139,92,246,0.4)" stroke-width="1"/>
  <text x="295" y="103" text-anchor="middle" font-size="9.5" font-weight="600" fill="#c4b5fd">分析需求</text>
  <rect x="555" y="82" width="100" height="34" rx="5" fill="rgba(139,92,246,0.2)" stroke="rgba(139,92,246,0.4)" stroke-width="1"/>
  <text x="605" y="103" text-anchor="middle" font-size="9.5" font-weight="600" fill="#c4b5fd">提交报价</text>
  <!-- 步骤：财务道 -->
  <rect x="720" y="149" width="100" height="34" rx="5" fill="rgba(16,185,129,0.2)" stroke="rgba(16,185,129,0.4)" stroke-width="1"/>
  <text x="770" y="170" text-anchor="middle" font-size="9.5" font-weight="600" fill="#6ee7b7">开具发票</text>
  <!-- 连接箭头 -->
  <line x1="190" y1="33" x2="245" y2="33" stroke="#475569" stroke-width="1.5"/>
  <line x1="245" y1="33" x2="245" y2="82" stroke="#475569" stroke-width="1.5" marker-end="url(#sw-arr)"/>
  <line x1="345" y1="99" x2="400" y2="99" stroke="#475569" stroke-width="1.5"/>
  <line x1="400" y1="99" x2="400" y2="33" stroke="#475569" stroke-width="1.5" marker-end="url(#sw-arr)"/>
  <line x1="655" y1="99" x2="720" y2="99" stroke="#475569" stroke-width="1.5"/>
  <line x1="720" y1="99" x2="720" y2="33" stroke="#475569" stroke-width="1.5" marker-end="url(#sw-arr)"/>
  <line x1="820" y1="33" x2="860" y2="33" stroke="#475569" stroke-width="1.5"/>
  <line x1="820" y1="166" x2="860" y2="166" stroke="#475569" stroke-width="1.5"/>
</svg>
```

### 2b · 漏斗图（Funnel）

**结构公式**：N 个梯形叠加，每层比上层窄（宽度=总宽×该层比例），颜色渐变，标注数值和转化率。

```
每层梯形（polygon）坐标计算：
  层 i 顶边宽 W_top = 总宽 × ratio_i
  层 i 底边宽 W_bot = 总宽 × ratio_(i+1)
  x_top_left  = (总宽 - W_top) / 2
  x_top_right = (总宽 + W_top) / 2
  x_bot_left  = (总宽 - W_bot) / 2
  x_bot_right = (总宽 + W_bot) / 2
  y_top = i × 层高，y_bot = (i+1) × 层高
  points = "x_tl,y_top x_tr,y_top x_br,y_bot x_bl,y_bot"
```

---

## 三、进阶数据图族

### 3a · Sankey 桑基图

**结构公式**：左侧来源节点（竖条）→ 流量路径（宽度=占比的 bezier 曲线）→ 右侧去向节点。

```
SVG 构建步骤：
1. 计算每个节点的 y 起点（累加各流出/流入量的高度）
2. 左节点：<rect x="0" y="{start}" width="16" height="{nodeH}" fill="主色"/>
3. 右节点：<rect x="总宽-16" y="{start}" width="16" height="{nodeH}" fill="对比色"/>
4. 流量路径：
   <path d="M 16,{src_y_mid}
            C {总宽×0.4},{src_y_mid} {总宽×0.6},{dst_y_mid} {总宽-16},{dst_y_mid}"
         fill="none" stroke="var(--p)" stroke-width="{flowWidth}" opacity="0.4"/>
5. 节点标签：<text> 标注名称和数值
```

### 3b · Bullet 子弹图（目标对比）

**结构公式**：三层叠加水平条——背景区间（浅灰→深灰三段）+ 实际值条 + 目标线。

```html
<!-- 单条 Bullet Chart，高度约 26px，可叠加多条 -->
<svg viewBox="0 0 480 26" style="width:100%;height:26px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 标签 -->
  <text x="0" y="17" font-size="9.5" font-weight="600" fill="var(--mt)" style="width:60px">销售额</text>
  <!-- 背景区间：差/良/优 -->
  <rect x="65" y="6" width="380" height="14" rx="2" fill="rgba(255,255,255,0.04)"/>
  <rect x="65" y="6" width="228" height="14" rx="2" fill="rgba(255,255,255,0.07)"/>
  <rect x="65" y="6" width="152" height="14" rx="2" fill="rgba(255,255,255,0.11)"/>
  <!-- 实际值：80% -->
  <rect x="65" y="9" width="304" height="8" rx="1" fill="var(--p)"/>
  <!-- 目标线：90% -->
  <rect x="407" y="4" width="3" height="18" rx="1" fill="#f59e0b"/>
  <!-- 数值标签 -->
  <text x="373" y="17" font-size="8.5" fill="var(--mt)">80%</text>
  <text x="410" y="17" font-size="8.5" fill="#f59e0b">目标90%</text>
</svg>
```

### 3c · Treemap 树图（面积=价值）

**结构公式**：递归矩形分割算法（Squarified），父节点 = 大矩形，子节点 = 内部小矩形拼贴。

```
布局算法（简化版，适合 4-8 个节点）：
  按值从大到小排序
  交替水平/垂直切分剩余矩形
  每个节点：<rect> + 内部 <text>（名称 + 值）
  颜色：按层级用渐变或按分类用色相区分
  最小可见节点尺寸：40×30px（小于此不显示标签）
```

---

## 四、层级分析图族

### 4a · 金字塔图（Pyramid）

```html
<svg viewBox="0 0 400 200" style="width:100%;height:200px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 第1层（顶，最重要） -->
  <polygon points="200,8 260,58 140,58" fill="var(--p)" opacity="0.9"/>
  <text x="200" y="40" text-anchor="middle" font-size="9.5" font-weight="700" fill="#fff">战略层</text>
  <!-- 第2层 -->
  <polygon points="140,61 260,61 300,108 100,108" fill="var(--p)" opacity="0.65"/>
  <text x="200" y="90" text-anchor="middle" font-size="9.5" font-weight="600" fill="#fff">管理层</text>
  <!-- 第3层 -->
  <polygon points="100,111 300,111 348,160 52,160" fill="var(--p)" opacity="0.4"/>
  <text x="200" y="141" text-anchor="middle" font-size="9.5" font-weight="600" fill="var(--t)">执行层</text>
  <!-- 第4层（底，基础） -->
  <polygon points="52,163 348,163 380,196 20,196" fill="var(--p)" opacity="0.2"/>
  <text x="200" y="184" text-anchor="middle" font-size="9.5" font-weight="600" fill="var(--t)">基础设施</text>
  <!-- 右侧标注（可选） -->
  <line x1="350" y1="33" x2="390" y2="33" stroke="rgba(255,255,255,0.2)" stroke-width="0.8"/>
  <text x="392" y="37" font-size="8.5" fill="var(--dt)">5%</text>
  <line x1="305" y1="84" x2="390" y2="84" stroke="rgba(255,255,255,0.2)" stroke-width="0.8"/>
  <text x="392" y="88" font-size="8.5" fill="var(--dt)">20%</text>
</svg>
```

### 4b · 2×2 矩阵（BCG / SWOT / 优先级矩阵通用模板）

```html
<svg viewBox="0 0 380 280" style="width:100%;height:280px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 四象限背景 -->
  <rect x="40" y="10" width="155" height="120" rx="3" fill="rgba(16,185,129,0.08)" stroke="rgba(16,185,129,0.15)" stroke-width="1"/>
  <rect x="200" y="10" width="155" height="120" rx="3" fill="rgba(59,130,246,0.08)" stroke="rgba(59,130,246,0.15)" stroke-width="1"/>
  <rect x="40" y="135" width="155" height="120" rx="3" fill="rgba(245,158,11,0.08)" stroke="rgba(245,158,11,0.15)" stroke-width="1"/>
  <rect x="200" y="135" width="155" height="120" rx="3" fill="rgba(239,68,68,0.08)" stroke="rgba(239,68,68,0.15)" stroke-width="1"/>
  <!-- 象限标题 -->
  <text x="118" y="30" text-anchor="middle" font-size="10" font-weight="700" fill="#10b981">明星产品</text>
  <text x="278" y="30" text-anchor="middle" font-size="10" font-weight="700" fill="#3b82f6">问题产品</text>
  <text x="118" y="155" text-anchor="middle" font-size="10" font-weight="700" fill="#f59e0b">现金牛</text>
  <text x="278" y="155" text-anchor="middle" font-size="10" font-weight="700" fill="#ef4444">瘦狗产品</text>
  <!-- 象限说明文字 -->
  <text x="118" y="48" text-anchor="middle" font-size="8.5" fill="var(--dt)">高增长·高份额</text>
  <text x="278" y="48" text-anchor="middle" font-size="8.5" fill="var(--dt)">高增长·低份额</text>
  <text x="118" y="173" text-anchor="middle" font-size="8.5" fill="var(--dt)">低增长·高份额</text>
  <text x="278" y="173" text-anchor="middle" font-size="8.5" fill="var(--dt)">低增长·低份额</text>
  <!-- 数据气泡（示例，大小=市场规模） -->
  <circle cx="110" cy="80" r="18" fill="rgba(16,185,129,0.3)" stroke="#10b981" stroke-width="1.5"/>
  <text x="110" y="84" text-anchor="middle" font-size="8.5" fill="#10b981">A</text>
  <circle cx="250" cy="70" r="12" fill="rgba(59,130,246,0.3)" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="250" y="74" text-anchor="middle" font-size="8.5" fill="#3b82f6">B</text>
  <circle cx="130" cy="200" r="22" fill="rgba(245,158,11,0.3)" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="130" y="204" text-anchor="middle" font-size="8.5" fill="#f59e0b">C</text>
  <circle cx="270" cy="210" r="9" fill="rgba(239,68,68,0.3)" stroke="#ef4444" stroke-width="1.5"/>
  <text x="270" y="214" text-anchor="middle" font-size="8.5" fill="#ef4444">D</text>
  <!-- 坐标轴 -->
  <text x="118" y="270" text-anchor="middle" font-size="8.5" fill="#64748b">← 相对市场份额 →</text>
  <text x="18" y="96" text-anchor="middle" font-size="8.5" fill="#64748b" transform="rotate(-90,18,96)">市场增长率</text>
</svg>
```

### 4c · 同心圆/洋葱图（Onion Diagram）

```
构建规则：
  N 个同心圆共享圆心 (cx, cy)
  最内圈：核心产品/价值，实色填充，r 最小
  向外每圈：opacity 递减 0.15 步长，r 递增 40-50px
  文字标签：沿每圈弧线放置或在圆环中点 text-anchor="middle"
  可加扇形分割线（path arc）细分每圈为不同部分
```

---

## 五、决策图族

### 5a · 风险矩阵（Risk Matrix）

```html
<svg viewBox="0 0 320 240" style="width:100%;height:240px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 5×5 热力格 -->
  <!-- 颜色规则：likelihood×impact → 绿/黄/橙/红 -->
  <!-- 行1（impact=5，最高） -->
  <rect x="40" y="10"  width="52" height="40" rx="1" fill="rgba(245,158,11,0.5)"/><text x="66" y="34" text-anchor="middle" font-size="8" fill="#fff">5</text>
  <rect x="94" y="10"  width="52" height="40" rx="1" fill="rgba(239,68,68,0.5)"/><text x="120" y="34" text-anchor="middle" font-size="8" fill="#fff">10</text>
  <rect x="148" y="10" width="52" height="40" rx="1" fill="rgba(239,68,68,0.7)"/><text x="174" y="34" text-anchor="middle" font-size="8" fill="#fff">15</text>
  <rect x="202" y="10" width="52" height="40" rx="1" fill="rgba(239,68,68,0.85)"/><text x="228" y="34" text-anchor="middle" font-size="8" fill="#fff">20</text>
  <rect x="256" y="10" width="52" height="40" rx="1" fill="rgba(239,68,68,1)"/><text x="282" y="34" text-anchor="middle" font-size="8" fill="#fff">25</text>
  <!-- 行2（impact=4） -->
  <rect x="40" y="52"  width="52" height="40" rx="1" fill="rgba(16,185,129,0.4)"/><text x="66" y="76" text-anchor="middle" font-size="8" fill="#fff">4</text>
  <rect x="94" y="52"  width="52" height="40" rx="1" fill="rgba(245,158,11,0.5)"/><text x="120" y="76" text-anchor="middle" font-size="8" fill="#fff">8</text>
  <rect x="148" y="52" width="52" height="40" rx="1" fill="rgba(245,158,11,0.7)"/><text x="174" y="76" text-anchor="middle" font-size="8" fill="#fff">12</text>
  <rect x="202" y="52" width="52" height="40" rx="1" fill="rgba(239,68,68,0.6)"/><text x="228" y="76" text-anchor="middle" font-size="8" fill="#fff">16</text>
  <rect x="256" y="52" width="52" height="40" rx="1" fill="rgba(239,68,68,0.8)"/><text x="282" y="76" text-anchor="middle" font-size="8" fill="#fff">20</text>
  <!-- 行3 -->
  <rect x="40" y="94"  width="52" height="40" rx="1" fill="rgba(16,185,129,0.3)"/><text x="66" y="118" text-anchor="middle" font-size="8" fill="#fff">3</text>
  <rect x="94" y="94"  width="52" height="40" rx="1" fill="rgba(16,185,129,0.5)"/><text x="120" y="118" text-anchor="middle" font-size="8" fill="#fff">6</text>
  <rect x="148" y="94" width="52" height="40" rx="1" fill="rgba(245,158,11,0.5)"/><text x="174" y="118" text-anchor="middle" font-size="8" fill="#fff">9</text>
  <rect x="202" y="94" width="52" height="40" rx="1" fill="rgba(245,158,11,0.7)"/><text x="228" y="118" text-anchor="middle" font-size="8" fill="#fff">12</text>
  <rect x="256" y="94" width="52" height="40" rx="1" fill="rgba(239,68,68,0.5)"/><text x="282" y="118" text-anchor="middle" font-size="8" fill="#fff">15</text>
  <!-- 行4/5 省略，以此类推 -->
  <!-- 轴标签 -->
  <text x="180" y="198" text-anchor="middle" font-size="8.5" fill="#64748b">← 可能性 (Likelihood) →</text>
  <text x="66"  y="208" text-anchor="middle" font-size="8" fill="#64748b">低(1)</text>
  <text x="282" y="208" text-anchor="middle" font-size="8" fill="#64748b">高(5)</text>
  <text x="14"  y="96" text-anchor="middle" font-size="8.5" fill="#64748b" transform="rotate(-90,14,96)">影响度</text>
  <!-- 风险点标注 -->
  <circle cx="174" cy="30" r="8" fill="none" stroke="#fff" stroke-width="2"/>
  <text x="174" y="33" text-anchor="middle" font-size="7.5" fill="#fff" font-weight="700">R1</text>
  <circle cx="228" cy="76" r="8" fill="none" stroke="#fff" stroke-width="2"/>
  <text x="228" y="79" text-anchor="middle" font-size="7.5" fill="#fff" font-weight="700">R2</text>
</svg>
```

### 5b · RACI 矩阵

```html
<!-- RACI 用 HTML table 实现更清晰 -->
<div style="overflow:hidden;font-size:10px;">
  <table style="width:100%;border-collapse:collapse;">
    <thead>
      <tr style="background:var(--card);">
        <th style="padding:5px 8px;text-align:left;color:var(--mt);font-weight:600;border-bottom:1px solid var(--bd);width:200px;">任务/交付物</th>
        <th style="padding:5px;text-align:center;color:var(--mt);font-weight:600;border-bottom:1px solid var(--bd);">产品</th>
        <th style="padding:5px;text-align:center;color:var(--mt);font-weight:600;border-bottom:1px solid var(--bd);">研发</th>
        <th style="padding:5px;text-align:center;color:var(--mt);font-weight:600;border-bottom:1px solid var(--bd);">测试</th>
        <th style="padding:5px;text-align:center;color:var(--mt);font-weight:600;border-bottom:1px solid var(--bd);">运营</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom:1px solid rgba(255,255,255,0.03);">
        <td style="padding:5px 8px;color:var(--t);">需求文档</td>
        <td style="text-align:center;"><span style="background:rgba(239,68,68,0.15);color:#ef4444;border-radius:3px;padding:2px 7px;font-weight:700;font-size:9px;">A</span></td>
        <td style="text-align:center;"><span style="background:rgba(59,130,246,0.15);color:#3b82f6;border-radius:3px;padding:2px 7px;font-weight:700;font-size:9px;">C</span></td>
        <td style="text-align:center;"><span style="background:rgba(148,163,184,0.1);color:#94a3b8;border-radius:3px;padding:2px 7px;font-weight:700;font-size:9px;">I</span></td>
        <td style="text-align:center;"><span style="background:rgba(16,185,129,0.15);color:#10b981;border-radius:3px;padding:2px 7px;font-weight:700;font-size:9px;">R</span></td>
      </tr>
      <tr style="border-bottom:1px solid rgba(255,255,255,0.03);">
        <td style="padding:5px 8px;color:var(--t);">功能开发</td>
        <td style="text-align:center;"><span style="background:rgba(59,130,246,0.15);color:#3b82f6;border-radius:3px;padding:2px 7px;font-weight:700;font-size:9px;">C</span></td>
        <td style="text-align:center;"><span style="background:rgba(16,185,129,0.15);color:#10b981;border-radius:3px;padding:2px 7px;font-weight:700;font-size:9px;">R</span></td>
        <td style="text-align:center;"><span style="background:rgba(59,130,246,0.15);color:#3b82f6;border-radius:3px;padding:2px 7px;font-weight:700;font-size:9px;">C</span></td>
        <td style="text-align:center;"><span style="background:rgba(148,163,184,0.1);color:#94a3b8;border-radius:3px;padding:2px 7px;font-weight:700;font-size:9px;">I</span></td>
      </tr>
    </tbody>
  </table>
  <!-- 图例 -->
  <div style="display:flex;gap:12px;margin-top:5px;font-size:8.5px;">
    <span style="color:#10b981;"><b>R</b> Responsible 执行</span>
    <span style="color:#ef4444;"><b>A</b> Accountable 决策</span>
    <span style="color:#3b82f6;"><b>C</b> Consulted 咨询</span>
    <span style="color:#94a3b8;"><b>I</b> Informed 知会</span>
  </div>
</div>
```

---

## 🌐 网络查询流程（当图谱不在以上库中时）

### 触发条件

用户描述的图谱类型**不在上述库中**，或描述模糊需要确认最佳视觉形式：

```
触发词举例：
  "画个 XXX 图"（从未见过的图名）
  "类似 McKinsey 那种矩阵"（需要查具体结构）
  "波士顿矩阵"/"飞轮模型"/"冰山模型"（需要查标准画法）
  "PESTLE 分析"/"VRIN 框架"（需查字段和布局）
```

### 查询步骤

```
Step 1 · 识别图谱名称
  从用户描述中提取图谱关键词
  示例："价值链分析" → 查询词 = "value chain diagram SVG structure"

Step 2 · WebSearch
  查询模板："{图谱名} diagram visual structure SVG"
  或中文："{图谱名} 画法 结构"
  目标：找到该图谱的标准组成元素和布局规则

Step 3 · 提取 SVG 构建规则
  从搜索结果中识别：
  - 有哪些基本形状（方框/圆/菱形/梯形/箭头）
  - 布局方向（左→右 / 上→下 / 环形 / 放射形）
  - 必填的标注（轴标签/象限名/流向说明）

Step 4 · 用本文件的 SVG 公式套入
  套用最相近的已知图谱 SVG 结构作为基础
  修改形状/颜色/标签 → 生成目标图谱
```

### 常见需查询图谱参考词

| 用户描述 | 建议搜索词 |
|---------|-----------|
| 飞轮模型 | flywheel diagram SVG circular |
| 冰山模型 | iceberg diagram SVG layers |
| 价值链 | Porter value chain diagram structure |
| 商业模式画布 | business model canvas layout |
| PESTLE/PEST | PESTLE analysis diagram table |
| 鱼骨图/石川图 | fishbone Ishikawa diagram SVG |
| 雷达/蜘蛛网 | spider radar chart SVG（→ 已在05-content图表3）|
| 甘特图 | Gantt chart SVG（→ 已在05-content图表5）|
