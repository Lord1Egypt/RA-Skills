# 特性速查手册(creative-layouts · 特性组合参考)

> **定位(2026-08-02 起变更):本手册从"创意模式教学"降为"特性速查"。**
> 写页的页面形态一律以 `page-archetypes.md`(**43 个原型**)与 `design-principles.md`(设计总纲)为准;
> 本手册只在原型已定、需要查"某特性怎么写"(渐变/预设几何/上下标/图表/旋转/虚线/阴影)时使用。
>
> **使用限制(去 AI 味纪律,违反即踩"主流 AI PPT"指纹)**:
> - 模式 1(渐变英雄区)、模式 5(渐变装饰条)——**仅封面/章节分隔/收尾页**可用,内容页禁用
> - 模式 3(渐变 KPI 卡)——**仅仪表盘原型(阅读/混合档)**;大数字带一律裸排细线分隔(原型 17)
> - 模式 6(渐变左边框引用块)——整体弃用,引用页用原型 6(巨引号+正体)
> - 模式 4(时间线炫技三件套:虚线+渐变圆+旋转标签)——默认弃用,时间线用原型 14(实线+圆点+正立字);旋转标签仅在用户明确要求"活泼"时
> - 模式 2(流程图)、模式 7(对比卡)、模式 8(代码展示)——可用,但遵循原型 13/12 的裸排变体优先
>
> `layout-recipes.md` 覆盖基础容器写法(三卡片横排/左右分栏/统计数字带/纵向堆叠);
> 容器内需要 P2 特性(渐变/几何/上下标/图表/旋转/虚线/阴影)时,回本手册查写法。
>
> **配套**:`design-principles.md`(设计契约)、`page-archetypes.md`(页面形态)、`html-spec.md`(转换契约)、`density-tiers.md`(密度上限)。

---

## 特性选择决策树(写页前先过一遍)

```
这一页要放图?
├─ 装饰图/渐变/几何纹理 → background-image on shape(截图,2x DPI)
├─ 内容照片/产品图(可替换) → <img data-object>(原生,object-fit 必写)
└─ 矢量图形/流程线/多边形 → <svg>(截图)或 data-shape(原生形状,优先)

这一页要画形状?
├─ 矩形/圆角/椭圆 → 默认(border-radius 判定)
├─ 三角/箭头/星形/chevron/流程图 → data-shape="..."(80+ 预设,见 html-spec 5.4)
├─ 渐变填充 → nativeGradient:true + linear-gradient(原生可编辑;默认关)
├─ radial/conic 渐变 → 截图(兜底,2x DPI 观感达标)
└─ 需要阴影/虚线边框 → box-shadow(真实参数)+ border:dashed/dotted(原生 dashType)

这一页的文字?
├─ 段落内差异化 → <span> 富样式(斜体/下划线/删除线/颜色/字体/字距/超链接)
├─ 化学式/脚注/数学式 → <sup>/<sub>(原生上下标)
├─ 列表 → <ul>/<ol>(原生 bullet/number,LI 直接含文字)
├─ 代码块 → <pre><code>(保留空白,white-space:pre)
└─ 大小写变换 → text-transform:uppercase/lowercase/capitalize

这一页有数据?
├─ 表格 → <table>(原生可编辑,colspan/rowspan/底纹/边框全支持)
├─ 图表 → data-chart='{...}'(原生 bar/line/area/pie/doughnut)
└─ Chart.js/ECharts canvas → <canvas>(截图,至少可见)

这一页要旋转?
├─ 纯旋转 → transform:rotate(Ndeg)(原生,origin 须居中)
└─ 缩放/斜切/平移 → 不支持(validate ERROR),改用宽高/图片表达

这一页有视觉特效?
├─ mix-blend-mode/filter/backdrop-filter/clip-path → 整体截图(文字放外侧独立 textbox)
└─ 渐变文字(background-clip:text) → 整体截图(连带文字)
```

---

## 模式 1 · 渐变英雄区(原生渐变 + 叠加文字)—— ⚠️ 仅封面/分隔/收尾页

**场景**:封面/章节首页/数据亮点页的视觉冲击区。**内容页禁用**(去 AI 味纪律)。
**特性组合**:原生线性渐变(`nativeGradient:true`)+ box-shadow + 圆角 + 富样式文字(run 级字号/颜色差异化)。

```html
<!-- 需在 slides.config.json 设 {"nativeGradient": true} -->
<!-- 渐变背景形状(原生可编辑,非截图) -->
<div data-object="true" data-object-type="shape"
     style="position:absolute;left:0;top:0;width:1920px;height:440px;
            background:linear-gradient(135deg,var(--brand-dark) 0%,var(--signal-blue) 100%);
            border-radius:0 0 24px 24px;
            box-shadow:0 8px 24px rgba(0,0,0,0.2);"></div>
<!-- 叠加标题(run 级字号 + 颜色差异) -->
<div data-object="true" data-object-type="textbox"
     style="position:absolute;left:100px;top:140px;width:1400px;height:140px;
            font-size:64px;font-weight:800;color:var(--white);line-height:1.2;">
  AI 赋能<span style="font-size:36px;color:rgba(255,255,255,0.7);"> — 从想法到落地</span>
</div>
<!-- 渐变副条(强调线) -->
<div data-object="true" data-object-type="shape"
     style="position:absolute;left:100px;top:300px;width:120px;height:6px;
            background:linear-gradient(to right,var(--accent-orange),var(--signal-red));border-radius:3px;"></div>
```

| 参数 | 调什么 |
|---|---|
| `linear-gradient(135deg,...)` | 角度(0/90/180/270/45/135)+ 色停;alpha<1 自动回退截图 |
| `border-radius:0 0 24px 24px` | 底部圆角(英雄区常用) |
| `box-shadow:0 8px 24px rgba(...)` | 真实阴影(offset/blur/color/alpha 全还原) |
| run 级 `font-size`/`color` | 同一 textbox 内字号/颜色差异化 |

⚠️ **渐变上的文字安全**:截图前页面全部文字会被隐藏,文字由独立 textbox 渲染,不会烙进截图。

---

## 模式 2 · 流程图(预设几何 + 旋转,零 SVG 依赖)

**场景**:流程步骤/决策树/箭头指引,用原生形状而非 SVG(可编辑)。
**特性组合**:`data-shape`(chevron/flowchartDecision/downArrow/rightArrow)+ 统一边框 + 旋转。

```html
<!-- chevron 步骤条(横向流程) -->
<div data-object="true" data-object-type="shape" data-shape="chevron"
     style="position:absolute;left:100px;top:400px;width:260px;height:80px;background:var(--brand-dark);"></div>
<div data-object="true" data-object-type="shape" data-shape="chevron"
     style="position:absolute;left:340px;top:400px;width:260px;height:80px;background:var(--signal-blue);"></div>
<div data-object="true" data-object-type="shape" data-shape="chevron"
     style="position:absolute;left:580px;top:400px;width:260px;height:80px;background:var(--signal-green);"></div>

<!-- 决策菱形(带边框) -->
<div data-object="true" data-object-type="shape" data-shape="flowchartDecision"
     style="position:absolute;left:900px;top:380px;width:180px;height:120px;
            background:var(--white);border:2px solid var(--accent-orange);"></div>

<!-- 向下箭头(连接器) -->
<div data-object="true" data-object-type="shape" data-shape="downArrow"
     style="position:absolute;left:970px;top:520px;width:40px;height:60px;background:var(--accent-orange);"></div>

<!-- 旋转的分支标签(transform:rotate) -->
<div data-object="true" data-object-type="textbox"
     style="position:absolute;left:820px;top:560px;width:160px;height:40px;
            font-size:18px;font-weight:600;color:var(--accent-orange);text-align:center;
            transform:rotate(-15deg);">异常分支</div>
```

| 常用 data-shape | 场景 |
|---|---|
| `chevron` | 流程步骤条(横向 V 形) |
| `rightArrow`/`leftArrow`/`downArrow`/`upArrow` | 方向指引/连接器 |
| `triangle`/`rtTriangle` | 箭头尖/强调标记 |
| `diamond`/`flowchartDecision` | 决策节点/判断框 |
| `flowchartTerminator` | 流程起止(圆角胶囊) |
| `star5`/`heart` | 评分/情感标记 |
| `plus`/`minus` | 增减标记 |
| `lightningBolt` | 闪电/能量/速度 |

⚠️ 完整 80+ 形状白名单见 `html-spec.md` 5.4 节;非法值 validate 报 ERROR。旋转 `transform-origin` 必须居中。

---

## 模式 3 · 数据仪表盘(flex + 渐变 KPI 卡 + 原生图表 + 原生表格)—— ⚠️ 仅仪表盘原型

**场景**:数据汇报页/KPI 仪表盘/季度复盘(阅读/混合档)。**演讲档 KPI 一律裸排**(原型 17)。
**特性组合**:flex 布局 + 渐变卡片 + 上下标 + run 级字距 + 原生图表(`data-chart`)+ 原生表格(`<table>`)。

```html
<!-- KPI 卡片行(flex 三栏)+ 渐变 + 上下标 -->
<div style="position:absolute;left:100px;top:200px;width:1720px;display:flex;gap:24px;">
  <div data-object="true" data-object-type="shape"
       style="flex:1;height:200px;background:linear-gradient(135deg,var(--brand-dark),var(--brand-dark-soft));
              border-radius:12px;padding:28px;">
    <div style="font-size:14px;letter-spacing:4px;color:rgba(255,255,255,0.6);font-weight:600;">ACCURACY</div>
    <div style="font-size:56px;font-weight:800;color:var(--white);line-height:1;margin-top:12px;">
      94.2<sup style="font-size:24px;">%</sup>
    </div>
    <div style="font-size:16px;color:var(--signal-green);margin-top:8px;letter-spacing:1px;">↑ 12% vs Q3</div>
  </div>
  <!-- 更多 KPI 卡(同结构,换渐变色) -->
</div>

<!-- 原生图表(data-chart) -->
<div data-object="true" data-chart='{"type":"bar","labels":["Q1","Q2","Q3","Q4"],"series":[{"name":"营收","values":[120,180,240,310]}]}'
     style="position:absolute;left:100px;top:440px;width:840px;height:320px;border:1px solid var(--border-light);border-radius:12px;padding:20px;"></div>

<!-- 原生表格 -->
<div data-object="true" data-object-type="table" style="position:absolute;left:980px;top:440px;width:840px;">
  <table style="width:100%;border-collapse:collapse;font-size:16px;">
    <tr style="background:var(--brand-dark);color:var(--white);">
      <th style="padding:12px;text-align:left;">指标</th>
      <th style="padding:12px;">Q3</th>
      <th style="padding:12px;">Q4</th>
      <th style="padding:12px;">增长</th>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:12px;">营收(亿)</td>
      <td style="padding:12px;text-align:center;">240</td>
      <td style="padding:12px;text-align:center;">310</td>
      <td style="padding:12px;text-align:center;color:var(--signal-green);">+29%</td>
    </tr>
  </table>
</div>
```

| 特性 | 要点 |
|---|---|
| `letter-spacing` | KPI 标签大字距(4-8px)提升专业感;run 级可差异化 |
| `<sup>`/`<sub>` | 百分号/单位上标,化学式下标 |
| `data-chart` | bar/line/area/pie/doughnut;`{"type","labels","series":[{"name","values"}]}` |
| `<table>` | 原生可编辑;colspan/rowspan/底纹/边框/对齐全支持 |

⚠️ 密度上限(见 `density-tiers.md`):演讲档表格 ≤6 行(含表头)、图表 ≤3 系列;超限拆页或拆多图。

---

## 模式 4 · 时间线(虚线连接 + 渐变节点 + 旋转标签)—— ⚠️ 默认用原型 14 替代

**场景**:发展历程/路线图/项目里程碑。**默认使用原型 14(实线+圆点+正立字)**;本模式的虚线/旋转标签仅在用户明确要求"活泼风"时使用。
**特性组合**:虚线边框(`border:dashed`)+ 渐变圆(`border-radius:50%`)+ 旋转文字(`transform:rotate`)。

```html
<!-- 水平虚线时间轴 -->
<div data-object="true" data-object-type="shape"
     style="position:absolute;left:100px;top:500px;width:1720px;height:0;
            border-top:2px dashed var(--border-medium);"></div>

<!-- 渐变圆节点(每个节点不同渐变) -->
<div data-object="true" data-object-type="shape"
     style="position:absolute;left:180px;top:470px;width:60px;height:60px;border-radius:50%;
            background:linear-gradient(135deg,var(--accent-orange),var(--signal-red));
            box-shadow:0 4px 12px rgba(243,152,0,0.4);"></div>
<div data-object="true" data-object-type="shape"
     style="position:absolute;left:560px;top:470px;width:60px;height:60px;border-radius:50%;
            background:linear-gradient(135deg,var(--signal-blue),var(--code-highlight));"></div>
<div data-object="true" data-object-type="shape"
     style="position:absolute;left:940px;top:470px;width:60px;height:60px;border-radius:50%;
            background:linear-gradient(135deg,var(--signal-green),var(--code-text));"></div>

<!-- 旋转的年份标签(交替上下) -->
<div data-object="true" data-object-type="textbox"
     style="position:absolute;left:150px;top:560px;width:120px;height:40px;
            font-size:24px;font-weight:700;color:var(--accent-orange);text-align:center;
            transform:rotate(-12deg);">2023</div>
<div data-object="true" data-object-type="textbox"
     style="position:absolute;left:530px;top:400px;width:120px;height:40px;
            font-size:24px;font-weight:700;color:var(--signal-blue);text-align:center;
            transform:rotate(12deg);">2024</div>

<!-- 节点说明(交替上下) -->
<div data-object="true" data-object-type="textbox"
     style="position:absolute;left:100px;top:620px;width:220px;height:60px;
            font-size:16px;color:var(--text-primary);line-height:1.5;text-align:center;">
  产品发布<br><span style="font-size:14px;color:var(--text-tertiary);">首个 AI 工作流</span>
</div>
```

| 参数 | 调什么 |
|---|---|
| `border-top:2px dashed` | 虚线轴线(dashed→dashType;dotted→sysDot) |
| `border-radius:50%` + 渐变 | 渐变圆节点(宽高接近时为正圆) |
| `transform:rotate(±Ndeg)` | 标签交替倾斜(年份上倾/下倾) |
| 节点 `box-shadow` | 节点投影(真实参数) |

⚠️ 旋转 `transform-origin` 必须居中(PPTX 绕中心旋转);非居中 validate 报 WARN。

---

## 模式 5 · 渐变装饰条 + 阴影卡片矩阵(data-layout grid)—— ⚠️ 渐变条仅封面/分隔/收尾

**场景**:特性矩阵/方案对比/产品功能展示。**顶部渐变条仅封面/分隔/收尾页**;内容页的卡片矩阵去掉渐变条,且每 deck ≤2 页(去 AI 味反模式 7)。
**特性组合**:原生渐变条 + `data-layout="grid"` + box-shadow 卡片 + letter-spacing 编号。

```html
<!-- 顶部渐变装饰条(全宽,原生渐变) -->
<div data-object="true" data-object-type="shape"
     style="position:absolute;left:0;top:0;width:1920px;height:8px;
            background:linear-gradient(to right,var(--brand-dark),var(--signal-blue),var(--code-highlight));"></div>

<!-- grid 卡片矩阵(方式 C,子级只写高度) -->
<div data-layout="grid" data-layout-cols="3" data-layout-gap="24"
     style="position:absolute;left:100px;top:160px;width:1720px;">
  <div data-object="true" data-layout-h="300"
       style="background:var(--white);border-radius:12px;
              box-shadow:0 4px 16px rgba(0,0,0,0.1);padding:32px;">
    <div style="font-size:14px;letter-spacing:6px;color:var(--signal-blue);font-weight:700;">01</div>
    <div data-shape-ignore style="font-size:24px;font-weight:700;margin-top:16px;color:var(--brand-dark);">智能分析</div>
    <div style="font-size:16px;color:var(--text-secondary);margin-top:12px;line-height:1.55;">自动识别数据模式,生成洞察建议</div>
    <div style="margin-top:20px;padding-top:16px;border-top:1px solid var(--border-light);font-size:14px;color:var(--signal-blue);">
      <a href="#" style="color:inherit;text-decoration:none;">了解更多 →</a>
    </div>
  </div>
  <!-- 卡片 2、3 同结构,换编号/标题/正文/链接色 -->
</div>
```

| 参数 | 调什么 |
|---|---|
| 渐变条 `linear-gradient(to right,...)` | 多色渐变装饰条(三色/四色均可) |
| `data-layout-cols="3"` | 列数;2/3/4 列常用 |
| `data-layout-h="300"` | 卡片高度(行高取该行最大) |
| `box-shadow:0 4px 16px rgba(...)` | 卡片投影(真实参数,非固定近似) |
| `letter-spacing:6px` | 编号大字距(专业感) |
| `<a href>` | 卡内超链接(原生可点击) |

---

## 模式 6 · 引用块(渐变左边框 + 斜体 + 超链接)—— ⛔ 整体弃用

**场景**:金句/专家引用/客户证言。**本模式为典型 AI 指纹,引用页一律用原型 6(巨引号+正体)**;本节仅保留斜体/超链接的特性写法参考。
**特性组合**:渐变细条 + 斜体(`font-style:italic`)+ 超链接(`<a href>`)+ run 级样式差异。

```html
<!-- 渐变左边框(竖向渐变细条) -->
<div data-object="true" data-object-type="shape"
     style="position:absolute;left:100px;top:400px;width:6px;height:180px;
            background:linear-gradient(to bottom,var(--accent-orange),var(--signal-red));border-radius:3px;"></div>

<!-- 引用文字(斜体 + run 级强调 + 超链接) -->
<div data-object="true" data-object-type="textbox"
     style="position:absolute;left:130px;top:400px;width:1500px;height:180px;
            font-size:30px;font-style:italic;color:var(--text-primary);line-height:1.6;">
  "AI 不是替代人类,而是<i>放大</i>人类的创造力。"
  <br><span style="font-size:18px;font-style:normal;color:var(--text-tertiary);letter-spacing:1px;">
    — 参阅 <a href="https://example.com/report" style="color:var(--signal-blue);">完整报告</a>
  </span>
</div>
```

| 特性 | 要点 |
|---|---|
| 竖向渐变细条 | `linear-gradient(to bottom,...)` + 小 `width`(4-8px)+ `border-radius` |
| `font-style:italic` | 整段斜体;`<i>`/`<em>` 局部斜体 |
| `<a href>` | 超链接(原生可点击,PowerPoint 中可跳转) |
| run 级 `font-style`/`color`/`font-size` | 同段内差异化(署名小字/正体/不同色) |

---

## 模式 7 · 对比卡(非统一边框 + 预设几何图标 + 阴影)

**场景**:方案对比/优劣势对照/前后对比。
**特性组合**:非统一边框(单边强调 `border-top:Npx`)+ box-shadow + 预设几何图标(`data-shape="star5"`/`heart`/`lightningBolt`)。

```html
<!-- 左卡:绿色顶边(优势) -->
<div data-object="true" data-object-type="shape"
     style="position:absolute;left:100px;top:300px;width:540px;height:360px;
            background:var(--white);border-top:8px solid var(--signal-green);border-radius:8px;
            box-shadow:0 4px 16px rgba(0,0,0,0.08);">
</div>
<!-- 左卡内容:五角星评分 + 优势列表 -->
<div data-object="true" data-object-type="shape" data-shape="star5"
     style="position:absolute;left:130px;top:340px;width:32px;height:32px;background:var(--accent-orange);"></div>
<div data-object="true" data-object-type="textbox"
     style="position:absolute;left:180px;top:335px;width:200px;height:40px;
            font-size:22px;font-weight:700;color:var(--signal-green);line-height:40px;">方案 A</div>
<div data-object="true" data-object-type="textbox"
     style="position:absolute;left:130px;top:400px;width:480px;height:200px;font-size:18px;line-height:1.8;">
  <ul style="padding-left:20px;margin:0;">
    <li>部署简单,开箱即用</li>
    <li>成本可控,按需付费</li>
    <li>社区活跃,文档完善</li>
  </ul>
</div>

<!-- 右卡:红色顶边(劣势) -->
<div data-object="true" data-object-type="shape"
     style="position:absolute;left:680px;top:300px;width:540px;height:360px;
            background:var(--white);border-top:8px solid var(--signal-red);border-radius:8px;
            box-shadow:0 4px 16px rgba(0,0,0,0.08);">
</div>
<!-- 右卡内容:闪电图标 + 劣势列表 -->
<div data-object="true" data-object-type="shape" data-shape="lightningBolt"
     style="position:absolute;left:710px;top:340px;width:28px;height:36px;background:var(--signal-red);"></div>
<div data-object="true" data-object-type="textbox"
     style="position:absolute;left:760px;top:335px;width:200px;height:40px;
            font-size:22px;font-weight:700;color:var(--signal-red);line-height:40px;">方案 B</div>
```

| 特性 | 要点 |
|---|---|
| `border-top:8px solid` | 单边强调条(非统一边框,逐边细条还原) |
| `data-shape="star5"`/`lightningBolt` | 语义图标(评分/能量/速度) |
| `box-shadow` | 卡片投影(真实参数) |
| `<ul><li>` | 原生列表 bullet(自动挂项目符号) |

⚠️ 圆角卡片仍建议统一边框(逐边细条不贴合圆角);单边强调条用 `border-top` 不受此限。

---

## 模式 8 · 代码展示(渐变背景 + 虚线边框 + pre/code)

**场景**:技术分享/开发者演讲/代码教学。
**特性组合**:原生渐变(深色)+ 虚线边框(`border:dashed`)+ `pre`/`code` 保留空白 + 等宽字体。

```html
<!-- 深色渐变代码背景(原生渐变) -->
<div data-object="true" data-object-type="shape"
     style="position:absolute;left:100px;top:300px;width:1720px;height:420px;
            background:linear-gradient(135deg,var(--code-bg),var(--brand-dark));border-radius:12px;
            border:2px dashed rgba(255,255,255,0.15);"></div>

<!-- 窗口圆点装饰(三个小圆) -->
<div data-object="true" data-object-type="shape"
     style="position:absolute;left:140px;top:330px;width:16px;height:16px;border-radius:50%;background:var(--signal-red);"></div>
<div data-object="true" data-object-type="shape"
     style="position:absolute;left:168px;top:330px;width:16px;height:16px;border-radius:50%;background:var(--signal-yellow);"></div>
<div data-object="true" data-object-type="shape"
     style="position:absolute;left:196px;top:330px;width:16px;height:16px;border-radius:50%;background:var(--signal-green);"></div>

<!-- 代码内容(pre 保留空白;code 内联;不同语法元素用 span 变色) -->
<div data-object="true" data-object-type="textbox"
     style="position:absolute;left:140px;top:380px;width:1640px;height:320px;">
  <pre style="font-family:'Courier New',monospace;font-size:20px;color:var(--code-text);line-height:1.6;white-space:pre;margin:0;"><code><span style="color:var(--code-highlight);">const</span> ai = <span style="color:var(--code-highlight);">new</span> Workflow({
  model: <span style="color:var(--signal-yellow);">"gpt-4"</span>,
  tools: [<span style="color:var(--signal-yellow);">"search"</span>, <span style="color:var(--signal-yellow);">"code"</span>, <span style="color:var(--signal-yellow);">"analyze"</span>],
  <span style="color:var(--code-comment);font-style:italic;">// 上下标示例:复杂度 O(n<sup>2</sup>)</span>
});</code></pre>
</div>
```

| 特性 | 要点 |
|---|---|
| 深色渐变背景 | `linear-gradient(135deg,var(--code-bg),var(--brand-dark))`(原生,可编辑) |
| `border:2px dashed rgba(...)` | 虚线边框(dashed→dashType) |
| `white-space:pre` | 保留缩进/空格(pre/code 默认) |
| `<code>` 内联 | CODE/KBD/SAMP 已入内联集,不被当块级拆散 |
| run 级 `color` + `font-style` | 语法高亮(关键字/字符串/注释不同色) |
| `<sup>` | 代码注释中的数学上标(如 O(n²)) |

---

## 通用最佳实践(所有创意模式)

1. **"可编辑优先"原则**:能用原生元素就不用截图——渐变用 `nativeGradient:true`、形状用 `data-shape`、图表用 `data-chart`、表格用 `<table>`
2. **"装饰截图,内容原生"原则**:装饰性背景图/纹理 → `background-image`(截图);内容照片 → `<img>`(原生,object-fit 必写)
3. **"叠加安全"原则**:截图元素上的文字必须放在独立 textbox 叠加(截图前文字会被全局隐藏,避免重影)
4. **"DOM 序即叠放序"原则**:有重叠时让 DOM 顺序与视觉叠放一致(先画的在下、后画的在上),不依赖 z-index
5. **"密度分档"原则**:按 `density-tiers.md` 选档;表格行数(≤6/8/12)、图表系列数(≤3/4/6)有硬上限,超限拆页
6. **"条件写入"原则**:新特性键(sup/sub/charSpacing/data-shape/gradient)只在非默认时写入,旧页零 diff——但这不影响你写新页时大胆用

---

## 特性速查表(按"我想做 X"索引)

| 我想做… | 用什么 | 参考模式 |
|---|---|---|
| 全宽渐变英雄区 | `linear-gradient` + `nativeGradient:true` | 模式 1 |
| 流程步骤条 | `data-shape="chevron"` | 模式 2 |
| 决策树/判断框 | `data-shape="flowchartDecision"` + `downArrow` | 模式 2 |
| 方向箭头 | `data-shape="rightArrow/leftArrow/upArrow/downArrow"` | 模式 2 |
| KPI 大数字 + 上下标 | `<sup>`/`<sub>` + `letter-spacing` | 模式 3 |
| 原生图表 | `data-chart='{"type":"bar",...}'` | 模式 3 |
| 原生表格 | `<table>` + `<tr><th><td>` | 模式 3 |
| 时间线/里程碑 | `border:dashed` + 渐变圆 + `transform:rotate` | 模式 4 |
| 卡片矩阵 + 编号 | `data-layout="grid"` + `letter-spacing` + `box-shadow` | 模式 5 |
| 渐变装饰条 | `linear-gradient(to right,...)` 全宽细条 | 模式 5 |
| 金句/引用 | 渐变细条 + `font-style:italic` + `<a href>` | 模式 6 |
| 方案对比 | `border-top:Npx` 单边强调 + `data-shape` 图标 | 模式 7 |
| 评分/星级 | `data-shape="star5"` | 模式 7 |
| 代码展示 | 深色渐变 + `border:dashed` + `<pre><code>` | 模式 8 |
| 化学式 | `<sub>`(H₂O)/ `<sup>`(E=mc²) | 模式 3 |
| 脚注/商标 | `vertical-align:super` + 小字号 | 模式 1 |
| 旋转标签 | `transform:rotate(±Ndeg)`(origin 居中) | 模式 4 |
| 虚线/点线边框 | `border:dashed` / `dotted` | 模式 4/8 |
| 真实阴影 | `box-shadow:0 4px 16px rgba(...)` | 全模式 |
| 超链接 | `<a href="url">` | 模式 5/6 |
| 列表项目符号 | `<ul><li>` / `<ol><li>`(LI 直接含文字) | 模式 7 |
| 等宽代码内联 | `<code>`/`<kbd>`/`<samp>` | 模式 8 |
| 大小写变换 | `text-transform:uppercase/lowercase/capitalize` | 模式 3(KPI 标签) |

---

## 与其他文档的关系

- **`html-spec.md`**:契约(每特性的合法写法/边界/validate 规则)——本手册的代码模板均符合契约
- **`layout-recipes.md`**:基础骨架配方(三卡片/分栏/统计带/堆叠)——本手册是进阶组合
- **`density-tiers.md`**:密度上限(表格行数/图表系列数)——创意不破密度
- **`interview-guide.md`** Q9 装饰强度:选"丰富"时优先从本手册选模式;选"简洁"时用基础配方
- **`brand-styles.md`**:品牌色板——本手册的渐变色/强调色替换为品牌色即品牌风
