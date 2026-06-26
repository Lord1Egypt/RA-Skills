# Bento Grid 布局系统

## 画布参数

```
固定画布: width=1280px, height=720px
标题区: x=40, y=20, w=1200, h=50
内容区: x=40, y=80, w=1200, h=580
卡片间距: gap=20px
卡片圆角: border-radius=12px
卡片内边距: padding=24px
```

## CSS Grid 实现

所有布局通过 CSS Grid 精确实现。内容区容器统一定义：

```css
.content-area {
  position: absolute;
  left: 40px; top: 80px;
  width: 1200px; height: 580px;
  display: grid;
  gap: 20px;
}
```

## 页面类型布局

### 封面页 (cover)
- 大标题居中或左对齐, font-size=48-56px, accent-primary 色
- 副标题 font-size=24px
- 演讲人/日期/公司 底部小号文字 font-size=16px
- 装饰: 品牌色块、几何线条、配图（渐隐融合技法）
- **不使用 Bento Grid**，自由排版

### 目录页 (toc)
- 根据 Part 数量选择等大卡片网格布局

**布局决策规则**：
- 1 Part：单卡居中（可用 accent 色条装饰）
- 2 Parts：2 栏等宽布局
- 3 Parts：3 栏等宽布局
- 4 Parts：2x2 网格布局
- 5+ Parts：3+2 网格布局（第一行3卡，第二行2卡居中）

| Part 数量 | grid-template-columns | 单卡尺寸 |
|---------|----------------------|---------|
| 1 | 单卡居中 | 800x300 |
| 2 | 1fr 1fr | 590x540 |
| 3 | repeat(3, 1fr) | 387x540 |
| 4 | 1fr 1fr / 1fr 1fr (2x2) | 590x260 |
| 5+ | repeat(3, 1fr) / repeat(2, 1fr) (3+2) | 混合 |

**每张目录卡内容**：Part 编号（大号 accent 色）+ 章节标题 + 简短描述（如需要）

### 章节封面 (section)
- "PART 0X" font-size=20px, accent-primary, letter-spacing=2px
- 标题 font-size=44px, font-weight=700
- 导语 font-size=18px, color=text-secondary
- 大量留白，营造呼吸感
- **不使用 Bento Grid**，居中排版

### 结束页 (end)
- 标题 font-size=44px 居中
- 核心要点 3-5 个, font-size=18px
- 联系方式/CTA 底部

---

## 7 种内容页布局

所有基于内容区 (1200x580px, 起始坐标 40,80)。

### 1. 单一焦点

适用: 1个核心论点/大数据全屏展示

```css
.content-area { grid-template: 1fr / 1fr; }
/* 卡片: 1200x580 */
```

### 2. 50/50 对称

适用: 对比、并列概念

```css
.content-area { grid-template: 1fr / 1fr 1fr; }
/* 左: 590x580 | 右: 590x580 */
```

### 3. 非对称两栏 (2/3 + 1/3)

适用: 主次关系。**最常用的布局。**

```css
.content-area { grid-template: 1fr / 2fr 1fr; }
/* 主: 790x580 | 辅: 390x580 */
```

### 4. 三栏等宽

适用: 3个并列比较

```css
.content-area { grid-template: 1fr / repeat(3, 1fr); }
/* 卡1: 387x580 | 卡2: 387x580 | 卡3: 386x580 */
```

### 5. 主次结合 (大 + 两小)

适用: 层级关系。**推荐：信息层次丰富时优先选择。**

```css
.content-area { grid-template: 1fr 1fr / 2fr 1fr; }
/* 主: 790x580 (span 2 rows) | 辅1: 390x280 | 辅2: 390x280 */
```

主卡片需设置 `grid-row: 1 / -1;` 跨两行。

### 6. 顶部英雄式

适用: 总分关系。**推荐：总分结构清晰时优先选择。**

**3子项版（最常用）**：
```css
.content-area { grid-template: auto 1fr / repeat(3, 1fr); }
/* 英雄: 1200x260 (span 3 cols) | 子1-3: 387x300 */
```

**4子项版**：
```css
.content-area { grid-template: auto 1fr / repeat(4, 1fr); }
/* 英雄: 1200x260 (span 4 cols) | 子1-4: 285x300 */
```

**2子项版**：
```css
.content-area { grid-template: auto 1fr / 1fr 1fr; }
/* 英雄: 1200x280 (span 2 cols) | 子1-2: 590x280 */
```

英雄卡片需设置 `grid-column: 1 / -1;` 跨所有列。

### 7. 混合网格

适用: 高信息密度, 4-6个异构块。**推荐：信息密度最高时优先选择。**

**2x3 网格**：
```css
.content-area { grid-template: repeat(3, 1fr) / 1fr 1fr; }
/* 6个卡片: 各 590x180 */
```

可通过 `grid-row`/`grid-column` 的 span 让个别卡片跨行/跨列，形成大小混搭效果。

**关键约束**: 所有卡片不得超出内容区边界（x+w<=1240, y+h<=660），间距>=20px，禁止重叠。

---

## 布局决策矩阵

| 内容特征 | 推荐布局 | 卡片数 |
|---------|---------|-------|
| 1 个核心论点/数据 | 单一焦点 | 1 |
| 2 个对比/并列 | 50/50 对称 | 2 |
| 主概念 + 补充 | 非对称两栏 | 2 |
| 3 个并列要素 | 三栏等宽 | 3 |
| 1 核心 + 2 辅助 | 主次结合 | 3 |
| 综述 + 3-4 子项 | 顶部英雄式 | 4-5 |
| 4-6 异构块 | 混合网格 | 4-6 |

**选择优先级**：避免"单一焦点"（除非确实只有一个全屏内容）。内容>=3块时，优先选择主次结合/英雄式/混合网格。

---

## 12 种卡片内容类型

### text（文本卡片）
- 标题: h3, 18-20px, 700 weight
- 正文: p, 13-14px, line-height 1.8
- 关键词用 `<strong>` 或 `<span class="highlight">` 高亮
- **最低要求**: 标题 + 至少 2 段正文（每段 30-50 字）

### data（数据卡片）
- 核心数字: 36-48px, 800 weight, accent 色
- 单位/标签: 14-16px, text-secondary
- 补充解读: 13px
- 推荐搭配一个 CSS 可视化（进度条/对比柱/环形图）
- **最低要求**: 核心数字 + 单位 + 趋势 + 解读 + 可视化

### list（列表卡片）
- 圆点: 6-8px 圆点, accent 色
- 文字: 13px, line-height 1.6
- 交替使用不同 accent 色圆点增加层次感
- **最低要求**: 至少 4 条列表项，每条 15-30 字

### tag_cloud（标签云）
- 容器: flex-wrap, gap=8px
- 标签: 圆角胶囊形, 12px, accent 色边框
- **最低要求**: 至少 5 个标签

### process（流程卡片）
- 节点: 32px 圆形, accent 色, 居中步骤数字
- 连线: **真实 `<div>` 元素**（禁止 ::before/::after）
- 箭头: **内联 SVG `<polygon>`**（禁止 CSS border 三角形）
- **最低要求**: 至少 3 个步骤，每步标题 + 一句描述

### data_highlight（大数据高亮区）
- 用于封面或重点页的超大数据展示
- 数字: 64-80px, 900 weight, accent 色
- 副标题 + 补充数据行
- **最低要求**: 1 个超大数字 + 副标题 + 补充数据行

### timeline（时间线卡片）
- 用于展示时间序列、发展历程、项目里程碑
- 结构: 垂直时间轴线 + 圆点节点 + 内容卡片
- 时间轴线: 2px 宽, accent 渐变色
- 节点: 22px 圆形, accent 色 + 发光效果
- 内容卡片: 日期标签 + 标题 + 描述文字
- **HTML 结构**:
  ```html
  <div class="card-timeline">
    <div class="timeline-line"></div>
    <div class="timeline-item">
      <div class="timeline-node"></div>
      <div class="timeline-content">
        <span class="timeline-date">2024.Q1</span>
        <h4>阶段标题</h4>
        <p>阶段描述文字</p>
      </div>
    </div>
    <!-- 更多 timeline-item -->
  </div>
  ```
- **CSS 要点**: timeline-line 是真实 div, 不是 border; timeline-node 是真实 div, 不是 ::before
- **最低要求**: 至少 3 个时间节点

### comparison（对比卡片）
- 用于方案对比、产品比较、商业模式对比
- 结构: 左右 50/50 分栏 + 中间 VS 标记
- 每侧: 标签 + 图片 + 标题 + 列表
- **HTML 结构**:
  ```html
  <div class="card-comparison">
    <div class="comparison-left">
      <span class="comparison-label">方案 A</span>
      <img src="..." alt="方案A图片">
      <h3>方案名称</h3>
      <ul>
        <li>优点1</li>
        <li>缺点1</li>
      </ul>
    </div>
    <div class="comparison-vs">VS</div>
    <div class="comparison-right">
      <span class="comparison-label">方案 B</span>
      <img src="..." alt="方案B图片">
      <h3>方案名称</h3>
      <ul>
        <li>优点1</li>
        <li>优点2</li>
      </ul>
    </div>
  </div>
  ```
- **图片要求**: 使用 `<img>` 标签, 高度建议 160px, object-fit: cover
- **最低要求**: 左右各至少 3 条对比项

### quote（引用卡片）
- 用于名人名言、客户证言、产品语录
- 结构: 大号引号装饰 + 语录正文 + 作者信息
- 引号: 120px Georgia 字体, 低透明度 accent 色
- 语录: 24px, line-height 1.8
- 作者区: 圆形头像 + 姓名 + 职位
- **HTML 结构**:
  ```html
  <div class="card-quote">
    <div class="quote-mark">"</div>
    <blockquote>语录内容...</blockquote>
    <div class="quote-author">
      <img src="头像URL" alt="头像">
      <div>
        <span class="author-name">姓名</span>
        <span class="author-title">职位/头衔</span>
      </div>
    </div>
  </div>
  ```
- **头像**: 56px 圆形, 边框使用 accent 色
- **最低要求**: 语录 + 作者姓名

### stat_block（统计块卡片）
- 用于核心数据展示、业绩汇报、产品参数
- 结构: 4 宫格布局, 每格顶部有色条
- **重要**: 顶部色条必须使用真实元素, 禁止 ::before
- **HTML 结构**:
  ```html
  <div class="card-stat-block">
    <div class="stat-item">
      <div class="stat-top-bar"></div>  <!-- 真实元素, 不是 ::before -->
      <span class="stat-number">99.9%</span>
      <span class="stat-label">数据标签</span>
    </div>
    <div class="stat-item">
      <div class="stat-top-bar accent-2"></div>
      <span class="stat-number">50ms</span>
      <span class="stat-label">数据标签</span>
    </div>
    <!-- 更多 stat-item -->
  </div>
  ```
- **CSS 要点**: `.stat-top-bar` 是真实 div, position:absolute; top:0; height:3px
- **最低要求**: 4 个数据项, 每项有数字 + 标签

### feature_grid（特性网格卡片）
- 用于产品功能介绍、服务特性展示
- 结构: 2×2 网格布局
- 每格: emoji 图标 + 标题 + 描述
- **HTML 结构**:
  ```html
  <div class="card-feature-grid">
    <div class="feature-item">
      <div class="feature-icon">🚀</div>
      <h4>特性标题</h4>
      <p>特性描述</p>
    </div>
    <div class="feature-item">
      <div class="feature-icon">🔒</div>
      <h4>特性标题</h4>
      <p>特性描述</p>
    </div>
    <!-- 更多 feature-item -->
  </div>
  ```
- **图标**: 使用 emoji, 40px 字号
- **交互**: 可选 hover 上浮效果
- **最低要求**: 4 个特性

### image_text（图文叠加卡片）
- 用于场景展示、案例介绍、产品说明
- 结构: 50/50 左右分栏, 一侧图片一侧文字
- 支持: 左图右文 / 左文右图 两种布局
- 图片区: 渐变遮罩叠加效果
- 文字区: 标签 + 标题 + 正文
- **HTML 结构**:
  ```html
  <!-- layout-right: 图片在右; layout-left: 图片在左 -->
  <div class="card-image-text layout-right">
    <div class="image-area">
      <img src="图片URL" alt="描述">
      <div class="image-overlay"></div>
    </div>
    <div class="text-area">
      <span class="tag">标签文字</span>
      <h3>标题</h3>
      <p>正文内容...</p>
    </div>
  </div>
  ```
- **图片**: 使用 `<img>` 标签, object-fit: cover
- **遮罩**: 使用 `<div class="image-overlay">`, linear-gradient 背景
- **最低要求**: 图片 + 标题 + 至少 2 段正文
