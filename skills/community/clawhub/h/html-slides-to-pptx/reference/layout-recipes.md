# 版式配方库(方式 B/C:flex/grid 与 data-layout 官方写法)

> 每个配方 = 一段可直接复制的结构 + 参数表。容器全部**不标记、自身不可见**;
> 可见叶子(卡片/格子/条目)是 `data-object`。
> 方式 B(flex/grid)坐标由浏览器布局引擎计算;方式 C(data-layout)坐标由转换器解析器计算。
> 完整契约见 `html-spec.md` 第 2 章;样板页:`slide-template-flex.html`(B)、`slide-template-layout.html`(C)。

---

## 配方 1 · 三卡片横排(flex row 或 columns)

**场景**:并列要点/特性/方案对比,3-4 张卡片。

方式 B(flex):

```html
<div style="position:absolute;left:100px;top:380px;width:1720px;display:flex;gap:20px;">
  <div data-object="true" data-object-type="shape" style="flex:1;height:400px;background:var(--white);border:1px solid var(--border-light);border-radius:10px;z-index:1;padding:30px;">
    <div style="font-size:28px;font-weight:700;line-height:1.25;color:var(--charcoal);">卡片标题</div>
    <div style="font-size:24px;line-height:1.55;margin-top:20px;color:var(--text-primary);">正文</div>
  </div>
  <!-- 卡片 2、3 同上;其中一张可换 var(--deep-navy) 底 + flex:1.2 做高亮 -->
</div>
```

方式 C(data-layout,子级连宽高都不用写):

```html
<div data-layout="columns" data-layout-gap="20" style="position:absolute;left:100px;top:380px;width:1720px;height:400px;">
  <div data-object="true" data-layout-w="1fr" style="background:var(--white);border:1px solid var(--border-light);border-radius:10px;z-index:1;padding:30px;">
    <div style="font-size:28px;font-weight:700;line-height:1.25;color:var(--charcoal);">卡片标题</div>
    <div style="font-size:24px;line-height:1.55;margin-top:20px;color:var(--text-primary);">正文</div>
  </div>
  <div data-object="true" data-layout-w="1.2fr" style="background:var(--deep-navy);border-radius:10px;z-index:1;padding:30px;">…高亮卡…</div>
</div>
```

| 参数 | 调什么 |
|---|---|
| `top/height` | 卡片带在页中的纵向位置与高度 |
| `gap` | 卡片间距(常用 20-40px) |
| `flex:1` / `data-layout-w="1.2fr"` | 等宽 / 加宽某张(份数作用于内容盒,与 flex:1 语义一致) |
| `padding:30px` | 卡内边距(border-box 下不增加外尺寸) |

⚠️ 卡片高亮顶条:方式 B/C 下把顶条做成卡片第一个流式子元素(`height:5px;background:...`,配合负 margin 贴顶),或整页保留方式 A 的绝对定位顶条。

---

## 配方 2 · 左右分栏(grid 两列 或 columns)

**场景**:左图右文 / 左论点右论据 / 主辅双栏。

方式 B(grid):

```html
<div style="position:absolute;left:100px;top:320px;width:1720px;display:grid;grid-template-columns:7fr 5fr;gap:60px;">
  <div data-object="true" data-object-type="shape" style="height:560px;background:var(--card-bg);border-radius:10px;z-index:1;padding:40px;">
    <!-- 主栏内容(流式子元素) -->
  </div>
  <div data-object="true" data-object-type="shape" style="height:560px;background:var(--deep-navy);border-radius:10px;z-index:1;padding:40px;">
    <!-- 辅栏内容 -->
  </div>
</div>
```

方式 C(columns):

```html
<div data-layout="columns" data-layout-gap="60" style="position:absolute;left:100px;top:320px;width:1720px;height:560px;">
  <div data-object="true" data-layout-w="7fr" style="background:var(--card-bg);border-radius:10px;z-index:1;padding:40px;">…</div>
  <div data-object="true" data-layout-w="5fr" style="background:var(--deep-navy);border-radius:10px;z-index:1;padding:40px;">…</div>
</div>
```

| 参数 | 调什么 |
|---|---|
| `7fr 5fr` / `"7fr"+"5fr"` | 栏宽比(等宽写 `1fr 1fr` 或两个 `"1fr"`) |
| `gap:60px` | 栏间距(分栏宜大,40-80px) |

---

## 配方 3 · 统计数字带(grid N 列)

**场景**:KPI 一排大数字,4-6 格。

方式 B(grid)与方式 C(data-layout)二选一:

```html
<!-- B -->
<div style="position:absolute;left:100px;top:800px;width:1720px;display:grid;grid-template-columns:repeat(4,1fr);gap:20px;">
  <div data-object="true" data-object-type="shape" style="height:160px;background:var(--white);border:1px solid var(--border-light);border-radius:10px;z-index:1;padding:24px;">
    <div class="num" style="font-size:44px;font-weight:800;color:var(--lenovo-red);line-height:1.1;">87<span style="font-size:22px;font-weight:600;">%</span></div>
    <div style="font-size:16px;color:var(--text-secondary);line-height:1.4;margin-top:8px;">指标说明</div>
  </div>
</div>

<!-- C:格子只写高度 -->
<div data-layout="grid" data-layout-cols="4" data-layout-gap="20" style="position:absolute;left:100px;top:800px;width:1720px;">
  <div data-object="true" data-layout-h="160" style="background:var(--white);border:1px solid var(--border-light);border-radius:10px;z-index:1;padding:24px;">
    <div class="num" style="font-size:44px;font-weight:800;color:var(--lenovo-red);line-height:1.1;">87<span style="font-size:22px;font-weight:600;">%</span></div>
    <div style="font-size:16px;color:var(--text-secondary);line-height:1.4;margin-top:8px;">指标说明</div>
  </div>
</div>
```

| 参数 | 调什么 |
|---|---|
| `repeat(4,1fr)` / `data-layout-cols="4"` | 列数;5-6 格直接改 N,无需重算宽度 |
| 数字行 | 混合字号(44px 数字 + 22px 单位)是支持特性,行高自动按最大字号推算 |

---

## 配方 4 · 纵向条目堆叠(flex column 或 stack)

**场景**:时间轴、步骤列表、多行结论堆叠。

方式 B(flex column):

```html
<div style="position:absolute;left:100px;top:300px;width:1720px;display:flex;flex-direction:column;gap:24px;">
  <div data-object="true" data-object-type="shape" style="height:120px;background:var(--white);border:1px solid var(--border-light);border-radius:10px;z-index:1;padding:24px;display:flex;align-items:center;gap:24px;">
    <div style="width:64px;height:64px;background:var(--lenovo-red);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:900;color:#FFF;">1</div>
    <div style="flex:1;">
      <div style="font-size:24px;font-weight:700;line-height:1.3;">步骤标题</div>
      <div style="font-size:16px;color:var(--text-secondary);line-height:1.4;margin-top:4px;">步骤说明</div>
    </div>
  </div>
</div>
```

方式 C(stack):

```html
<div data-layout="stack" data-layout-gap="24" style="position:absolute;left:100px;top:300px;width:1720px;">
  <div data-object="true" data-layout-h="120" style="background:var(--white);border:1px solid var(--border-light);border-radius:10px;z-index:1;padding:24px;display:flex;align-items:center;gap:24px;">
    …同上内部结构(对象内部 flex 对齐不受 data-layout 限制)…
  </div>
</div>
```

| 参数 | 调什么 |
|---|---|
| `gap:24px` | 条目间距 |
| 条内 `display:flex;align-items:center` | 序号圆与文字水平居中对齐(对象内部 flex,一直支持) |

⚠️ 阶梯缩进(每层右移):方式 B 给每条加 `margin-left:0/150/300px`;方式 C 下改在每个条目的内部结构上做(或该区块用方式 A)。

---

## 通用规则(所有配方)

1. 容器:只写 `position:absolute` + 画布内位置 + 排布方式(`display:flex|grid` 或 `data-layout`),**不写** `data-object`、背景、边框
2. 叶子:每个可见卡片/格子/条目写 `data-object="true"`;其内部标题/正文/徽章/分隔线都是未标记流式子元素
3. 重叠:同容器内多个 data-object 需要重叠时,想压底的放 DOM 前面(勿用 z-index)
4. 骨架:眉题/标题/页码/页脚保持方式 A 绝对定位,与内容区互不干扰
5. 方式 C 子级:style 里不写 position/left/top/width/height(混写 = validate ERROR)

---

## 进阶:创意布局组合

本文件覆盖基础骨架(三卡片/分栏/统计带/堆叠)。**渐变/预设几何/上下标/原生图表表格/旋转/虚线/阴影等 P2 新特性的创意组合** 见 `creative-layouts.md`:

- 模式 1 · 渐变英雄区(原生渐变 + 叠加文字)
- 模式 2 · 流程图(预设几何 + 旋转,零 SVG 依赖)
- 模式 3 · 数据仪表盘(flex + 渐变 KPI 卡 + 原生图表 + 原生表格)
- 模式 4 · 时间线(虚线连接 + 渐变节点 + 旋转标签)
- 模式 5 · 渐变装饰条 + 阴影卡片矩阵(data-layout grid)
- 模式 6 · 引用块(渐变左边框 + 斜体 + 超链接)
- 模式 7 · 对比卡(非统一边框 + 预设几何图标 + 阴影)
- 模式 8 · 代码展示(渐变背景 + 虚线边框 + pre/code)

`creative-layouts.md` 还含**特性选择决策树**(写页前先过一遍)和**"我想做 X"特性速查表**(按需求索引到模式)。
