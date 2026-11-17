# HTML 幻灯片编写规范(html2pptx 无损还原契约)

> 只要严格遵守本规范写出的 HTML,经 `convert.js` 转换后的 PPTX 与浏览器渲染**像素级一致**。
> 本规范描述的是转换器支持的 HTML/CSS **子集**。每页写完后应通过 `validate.js` 预检(0 ERROR)。
>
> **2026-07-23 起新增三种布局方式**:A 绝对定位(经典)、B flex/grid/流式、C data-layout 声明式(见第 2 章)。

---

## 1. 页面骨架(每页必须严格如此)

```html
<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>页面标题</title>
<link rel="stylesheet" href="../assets/theme.css">
<style>
  html,body{margin:0;padding:0;overflow:hidden;}
  .slide-container{font-family:"Noto Sans SC","Inter",sans-serif;}
</style>
</head>
<body>
<div class="slide-container" style="position:relative;width:1920px;height:1080px;overflow:hidden;background:var(--off-white);">
  <!-- 所有可见元素都放在这里,每个都带 data-object 标记 -->
</div>
<template data-slide-notes>
  演讲者备注(可选),会写入 PPTX 的备注区。
</template>
</body>
</html>
```

**硬性要求**
- 画布固定 `1920×1080`,`.slide-container` 必须 `position:relative; overflow:hidden`
- `.slide-container` 的**纯色背景**会自动导出为 PPTX 幻灯片背景(深色页直接写容器底色即可,默认白);容器的**渐变/图片背景**不支持,请改用全画布 `data-object` shape(走截图还原)
- **所有**可见元素必须可归结到某个 `[data-object="true"]`(自身标记,或位于已标记祖先内部)
- **PPTX 叠放顺序 = DOM 顺序**(先画的在下、后画的在上)。`z-index` 只影响浏览器内合成(决定截图层效果),不改变 PPTX 叠放 —— **有重叠时让 DOM 顺序与期望叠放一致**,不要依赖 z-index

## 2. 布局的三种官方方式

### 方式 A · 绝对定位(经典,全部支持)

每个 `data-object` 用 `position:absolute` + `left/top/width/height` 直接给定坐标:

```html
<div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:940px;width:1720px;height:2px;background:var(--border-medium);z-index:1;"></div>
```

- 适合:页面骨架(眉题/标题/页码/页脚)、精确摆放的装饰、不规则版式
- `z-index` 照旧可写(浏览器合成需要),但 PPTX 叠放只看 DOM 顺序

### 方式 B · flex / grid / 流式(2026-07-23 起官方支持)

内容区可以用 flex/grid 容器排布 `data-object`,**坐标由布局引擎计算,提取器按计算后位置还原**:

```html
<!-- flex 容器:不标记、自身不可见;三个卡片是 data-object(flex 子级) -->
<div style="position:absolute;left:100px;top:380px;width:1720px;display:flex;gap:20px;">
  <div data-object="true" data-object-type="shape" style="flex:1;height:400px;background:var(--white);border:1px solid var(--border-light);border-radius:10px;padding:30px;">
    <!-- 卡片内部:未标记的流式子元素,随卡片递归提取 -->
    <div style="font-size:28px;font-weight:700;line-height:1.25;">卡片标题</div>
    <div style="font-size:18px;line-height:1.55;margin-top:20px;">正文……</div>
  </div>
  <div data-object="true" data-object-type="shape" style="flex:1;height:400px;background:var(--white);">…</div>
</div>
```

**契约**:
- 布局容器本身**不标记**,且自身不可见(无背景/边框/文字);它的可见子级必须每个都是 `data-object`(或在已标记元素内部)
- 容器自身的定位(在画布中的位置)仍用 `position:absolute` 给定 —— flex/grid 只负责容器**内部**排布
- 已标记卡片内部的未标记流式子元素(标题/正文/分隔线/徽章)**不需要也不能**再标 `data-object`(嵌套标记 = ERROR),会按实际位置逐个提取
- `gap`、`padding`、`margin`、`flex:N`、`grid-template-columns` 自由使用;`box-sizing:border-box` 下宽高即视觉宽高
- 容器内多个 `data-object` **重叠**时:叠放按 DOM 顺序(DOM 在后的在上),不要写 z-index(validate 会预警倒挂)
- 建议配合 `*{box-sizing:border-box}`(theme.css 已自带)

### 方式 C · data-layout 声明式自动布局(2026-07-23 起支持)

容器写 `data-layout` 策略,子级只声明份数/高度,**坐标由转换器内置解析器统一计算**(解析在提取前把子级改写成绝对定位,语义随后与方式 A 完全一致):

```html
<!-- columns:横向分栏。容器须显式 width+height;子级 data-layout-w 写份数或像素 -->
<div data-layout="columns" data-layout-gap="20" style="position:absolute;left:100px;top:340px;width:1720px;height:400px;">
  <div data-object="true" data-layout-w="1fr"   style="background:var(--white);padding:30px;…">卡片 1</div>
  <div data-object="true" data-layout-w="1.2fr" style="background:var(--brand-dark);padding:30px;…">卡片 2</div>
  <div data-object="true" data-layout-w="300"   style="background:var(--white);padding:30px;…">固定 300px 侧栏</div>
</div>

<!-- stack:纵向堆叠。容器须显式 width;子级 data-layout-h 写高度 -->
<div data-layout="stack" data-layout-gap="24" style="position:absolute;left:100px;top:300px;width:1720px;">
  <div data-object="true" data-layout-h="120" style="background:var(--white);…">条目 1</div>
  <div data-object="true" data-layout-h="120" style="background:var(--white);…">条目 2</div>
</div>

<!-- grid:等宽网格。容器须显式 width + data-layout-cols;子级 data-layout-h 写高度,行高取该行最大 -->
<div data-layout="grid" data-layout-cols="4" data-layout-gap="20" style="position:absolute;left:100px;top:800px;width:1720px;">
  <div data-object="true" data-layout-h="160" style="background:var(--white);…">格子</div>
</div>
```

**契约**:
- 容器:`position:absolute` + 显式 `width`(columns 还要显式 `height`)+ `data-layout` 策略;**不标记、自身不可见**
- 子级:必须标 `data-object="true"`;**禁止**在 style 里写 `position/left/top/width/height`(几何全交给解析器,混写 = ERROR);视觉样式(背景/padding/圆角/z-index)照常写
- `columns` 的份数语义与浏览器 `flex:1` 一致:份数分配**内容盒**(各子级 padding/border 不同则外宽不同);像素值指外宽
- ❌ 禁止嵌套 `data-layout` 容器(容器内需要二次排布时,子级内部用方式 B 的 flex/grid 即可)
- 解析器对无 `data-layout` 的页面是恒等 no-op;非法布局在 validate 报 ERROR、在 convert 直接失败
- 样板页:`assets/slide-template-layout.html`(与 flex 版逐 prim 等价)

## 3. 元素标记(data-object)

每个可见元素(文本块、色块、线条、图片背景)都要标:

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:88px;width:1000px;z-index:10;">…</div>
<div data-object="true" data-object-type="shape"  style="position:absolute;left:100px;top:940px;width:1720px;height:2px;background:var(--border-medium);z-index:1;"></div>
```

- `data-object-type="textbox"` — 含文字的元素
- `data-object-type="shape"` — 色块/线条/卡片/图片背景
- ⚠️ 漏标 `data-object="true"` 的可见元素**会整个消失**(validate 报 ERROR)
- ❌ **禁止嵌套标记**:`data-object` 内部不要再标 `data-object`(内层标记无效;外层内部的子元素本就会按位置逐个提取)
- 已标记元素**内部**的未标记子元素(bg 色块、文字 div)会被递归提取,这是方式 B 的基础

## 4. 文字规则

### 4.1 基本
- 文字放在 `textbox` 里;一个 textbox 可含多个块级子 div(每个子 div 成为独立段落),或含 `<span>` 行内变色/加粗
- 换行用 `<br>`(还原为 PPTX 软换行)
- `font-weight ≥ 600` → PPTX 粗体;< 600 → 常规。**只用 400/600/700/800/900,避免 500**(500 会退化为常规)
- **行内富样式(2026-07-27 起支持)**:`<i>/<em>` 或 `font-style:italic` → 斜体;`<u>` 或 `text-decoration:underline` → 下划线;`<s>/<del>` 或 `line-through` → 删除线;`<a href>` → 可点击超链接
- **run 级字体**:textbox 内 span 可指定不同 `font-family`(如 `.num` 用 Inter/Arial 排数字),逐 run 还原
- **上下标(2026-07-27 P2 起)**:`<sup>`/`<sub>` 标签或 `vertical-align:super/sub` → 原生上标/下标
- **run 级字距(2026-07-27 P2 起)**:span 可指定不同 `letter-spacing`,逐 run 还原(与 textbox 级 letter-spacing 独立)
- `text-transform:uppercase/lowercase/capitalize` → 按计算样式变换文本后写入
- `letter-spacing`、`text-align`(left/center/right/justify) 均支持

### 4.2 行高(重要)
- **多行文字必须显式设 `line-height`**(如 `line-height:1.55` 或 `31px`),否则行距不可控
- 单行文字可不设(默认 top 对齐无影响)

### 4.3 垂直居中(固定高度容器内文字居中)

**推荐方式:flexbox 居中**(提取器自动识别,PPTX 精确还原):

```html
<!-- ✅ 推荐:flexbox 垂直居中(适用于单行/多行/任意 padding) -->
<div data-object="true" data-object-type="textbox"
     style="position:absolute;left:840px;top:496px;width:240px;height:240px;
            display:flex;flex-direction:column;justify-content:center;align-items:center;">
  <div style="font-size:32px;font-weight:800;color:var(--white);line-height:1.3;">四大条件<br>同时成熟</div>
  <div style="font-size:17px;color:rgba(255,255,255,.6);margin-top:10px;">历史性对接</div>
</div>
```

**备选方式:line-height 等于容器高度**(仅适用于**单行**且**无 padding**的徽章):

```html
<!-- ✅ 备选:单行徽章用 line-height=height -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:1390px;top:876px;width:400px;height:44px;background:var(--accent-orange);z-index:5;"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:1390px;top:876px;width:400px;height:44px;text-align:center;z-index:10;">
  <div style="font-size:20px;font-weight:800;color:var(--brand-dark);line-height:44px;letter-spacing:2px;">AI = 人类的"智力外挂"</div>
</div>
```

**❌ 禁止:非对称 padding**(会导致 PPTX 顶对齐偏移):

```html
<!-- ❌ 错误:padding-top 推下文字在浏览器有效,但 PPTX 会顶对齐 -->
<div style="padding-top:64px;">文字</div>
<!-- 原因:非对称 padding 无法通过 valign:middle 精确还原,提取器会判为多行 top 对齐 -->
```

**规则**:
- 多行文字或需要 padding 时:**优先用 flexbox**(`display:flex` + `justify-content:center`)
- 单行徽章(无 padding)时:可用 `line-height` 等于容器 `height`
- **禁止**用非对称 padding(如 `padding-top:64px` 而 `padding-bottom:0`)来推动垂直位置——浏览器有效但 PPTX 会顶对齐

### 4.4 颜色
- 文字用**不透明纯色**(`var(--white)`、`var(--brand-dark-soft)`)
- ⚠️ `rgba(255,255,255,.75)` 这类半透明文字会退化为纯色 → 请预先手算与底色的混合色,直接写混合后的 hex
- ✅ 推荐用 `theme.css` 里的 CSS 变量(`var(--brand-primary)`),计算样式时自动解析
  （2026-08-06 P6:语义名 `--brand-primary`/`--brand-dark` 为正规名;`--lenovo-red`/`--deep-navy` 是向后兼容别名,新页面别再用）

## 5. 形状 / 背景规则

### 5.1 纯色形状
- `background:#hex` + 可选 `border:1px solid #hex` + `border-radius:Npx`(>0 变圆角矩形;`50%` 变椭圆;px 半径达到半高时,宽高接近的盒子判为正圆,长方形盒保持胶囊/stadium)
- ✅ **非统一边框也支持**(如 `border-top:6px solid red`、`border-left:4px solid black`):转换器会逐边生成细条。但带圆角的卡片仍建议统一边框(逐边细条不贴合圆角)
- ✅ **虚线/点线边框(2026-07-27 起)**:`border:2px dashed` / `dotted` → 原生虚线样式(统一边框直接 dashType;非统一的虚线边生成虚线 line 形状)
- ✅ **box-shadow(2026-07-27 起)按真实参数还原**:第一层非 inset 阴影的偏移/模糊/颜色/透明度映射为原生外阴影;spread 与多层不还原(validate WARN)
- ✅ **纯旋转(2026-07-27 起)**:`transform:rotate(Ndeg)` → 原生旋转(绕中心);`transform-origin` 必须居中;scale/skew/translate 仍禁止(validate ERROR)

### 5.2 渐变 / 图片 / SVG(截图还原)
- `background:linear-gradient(...)` / `conic-gradient(...)` / `background-image:url(...)` 的 shape 会被**精确截图**为 PNG 原位贴回,视觉 100% 一致
- ✅ **原生线性渐变(2026-07-27 P2 1.6,opt-in)**:开启 `nativeGradient:true` 后,`linear-gradient` → 原生可编辑渐变形状(`a:gradFill`);色停含 alpha<1 时回退截图;`radial/conic-gradient` 恒走截图
- `<svg>` 元素(流程线、多边形、虚线、图表等)同样**整体截图**还原,透明度/虚线样式无损
  - **内联 SVG 图标(2026-08-05 起)**:`assets/icons.md` 40 枚自绘线性图标,整段内联复制;**stroke/fill 必须显式 hex,禁 `currentColor`**(截图前文字隐藏会把 currentColor 变透明,图标空白;validate 有静态 WARN);`<use href="外部.svg">` 外链在 file:// 下不渲染,不可用
- ✅ 渐变/截图区域上叠加文字是**安全的**:截图前**页面上全部文字**会被临时隐藏(含截图元素内部的文字子元素),文字由可编辑文本框单独渲染
- ✅ **`<img>` 已支持(2026-07-27 P1)**:原生可编辑图片;`object-fit:cover/contain` 映射原生 sizing,`fill/none` 直接拉伸。本地 `file://` 与 `http(s)://` 图片均支持

### 5.2.1 `<img>` 与 `background-image` 的契约(2026-07-27 D6 拍板)

两种放图方式各司其职,**按用途选**:

| 用途 | 推荐方式 | 理由 |
|---|---|---|
| **装饰图**(渐变/几何/抽象纹理/纯视觉氛围) | `background-image` on `data-object="shape"` | 走截图路径(2x DPI),视觉 100% 一致;可叠加圆角/混合模式/clip-path;体积可控(`capture.imageType:jpeg`) |
| **内容照片/产品图/可替换图片**(需要原图分辨率、后续在 PPT 里替换) | `<img data-object="true">` | 原生 `a:blip` 嵌入,可编辑替换;object-fit 映射原生 sizing;原图分辨率优于截图 |

**`<img>` 硬契约**:
- **必须显式声明 `object-fit`**(`cover`/`contain`/`fill`/`none`);缺省时 validate 报 WARN(默认 `fill` 会拉伸变形,且与浏览器默认 `fill` 行为不可区分)
- `data-object="true"` 标记同其他元素;`data-object-type` 可省(自动判 image)
- 网络图(`http(s)://`)由转换器预取后嵌入;跨域受限图建议先本地化
- 与 `background-image` 共存的场景:背景层用 `background-image`(装饰),前景照片用 `<img>`(内容)——两者独立 `data-object`,按 DOM 序叠放

### 5.3 新表现形式(2026-07-27 P1 起)

| 元素 | 支持 | 说明 |
|---|---|---|
| `<img>` | ✅ 原生图片 | `object-fit:cover/contain/fill`;http 图自动取回嵌入 |
| `<table>` | ✅ 原生表格 | 单元格文本/对齐/底纹/边框/`colspan`/`rowspan`;列宽行高按计算值 |
| `<ul>/<ol>` | ✅ 原生 bullet/number | LI 直接含文字即挂原生项目符号;文字位置近似(详见行为细则) |
| `<canvas>` | ✅ 截图还原 | 解决"图表空白"——canvas 绘制结果整体截图 |
| `data-chart` 声明式图表 | ✅ 原生可编辑图表 | 任一元素挂 `data-chart='{...}'`(`type/labels/series/options`)→ bar/line/area/pie/doughnut |
| 图标字体(iconfont/FontAwesome/Material Icons) | ✅ 自动截图 | 命中 `config.iconFonts` 的文字元素整体截图,避免 PPT 端字体缺失错字 |
| `pre`/`code` | ✅ 保留空白 | `white-space:pre` 不折叠;CODE/KBD/SAMP 内联 |
| `mix-blend-mode`/`filter`/`backdrop-filter`/`clip-path` | ⚠️ 整体截图 | 特效元素转截图(不可编辑);文字请放外侧独立 textbox 叠加 |

### 5.4 预设几何(2026-07-27 P2 起)

除 `rect`/`roundRect`/`ellipse` 外,可通过 `data-shape` 属性声明 pptxgenjs 60+ 预设形状:

```html
<!-- 三角形(流程图决策/箭头尖) -->
<div data-object="true" data-object-type="shape" data-shape="triangle"
     style="position:absolute;left:100px;top:100px;width:120px;height:100px;background:var(--brand-dark);"></div>

<!-- 右箭头(方向指示) -->
<div data-object="true" data-object-type="shape" data-shape="rightArrow"
     style="position:absolute;left:300px;top:100px;width:200px;height:80px;background:var(--accent-orange);"></div>

<!-- V 形 chevron(流程步骤) -->
<div data-object="true" data-object-type="shape" data-shape="chevron"
     style="position:absolute;left:600px;top:100px;width:180px;height:80px;background:var(--signal-blue);"></div>
```

**契约**:
- `data-shape` 值必须是 pptxgenjs 支持的预设形状名(白名单见 validate);非法值 → ERROR
- 声明 `data-shape` 时 `border-radius` 被忽略(形状由预设几何决定)
- `fill`(背景色)、`border`(统一边框)、`box-shadow`、`transform:rotate` 仍照常生效
- 常用形状速查:`triangle`/`rtTriangle`/`diamond`/`pentagon`/`hexagon`/`chevron`/`rightArrow`/`leftArrow`/`upArrow`/`downArrow`/`star5`/`heart`/`plus`/`minus`/`lightningBolt`/`flowchartDecision`/`flowchartTerminator`
- 完整白名单(80+ 种)见 `scripts/validate/dom-checks.js` 的 `PRESET_SHAPES` 集合

### 5.5 母版与转场(2026-07-27 P2 起,配置驱动)

母版(页码/页脚)和转场动画均由**配置文件**控制,非页面内属性:

**母版**(`slides.config.json`):
```json
{
  "master": {
    "pageNumbers": true,
    "footer": "© 2026 Company · 机密",
    "footerColor": "999999"
  }
}
```
- `pageNumbers: true` → 每页右下角自动页码(`defineSlideMaster` + `sldNum` 占位符)
- `footer: "文字"` → 每页底部居中页脚(逐页 `addText`)
- `footerColor` → 页码/页脚颜色(默认 `999999`)
- 缺省(不写 `master` 键)→ 无母版,每页独立(旧行为)

**转场**(`playlist.json`):
```json
{
  "playlist": [
    "01.html",
    {"file": "02.html", "transition": "fade"},
    {"file": "03.html", "transition": "push"},
    "04.html"
  ]
}
```
- playlist 项支持字符串(`"01.html"`)或对象(`{"file":"01.html","transition":"fade"}`)
- `transition` 值:`fade`(淡入)/`push`(推入)/`wipe`(擦除)/`cover`(覆盖)/`split`(分裂)
- 缺省(字符串项或无 transition 键)→ 无转场

**音视频**(页面内属性):
```html
<!-- video:poster 属性 → 截图做封面;src → addMedia 嵌入 -->
<video data-object="true" poster="cover.png" src="demo.mp4"
       style="position:absolute;left:100px;top:200px;width:640px;height:360px;"></video>

<!-- audio:src → addMedia 嵌入 -->
<audio data-object="true" src="narration.mp3"
       style="position:absolute;left:100px;top:700px;width:400px;height:60px;"></audio>
```
- `poster` 属性优先做封面;无 poster 时截取浏览器渲染帧(可能黑屏,validate WARN)
- `src` 支持本地文件路径(相对 HTML 解析);http 视频需先本地化
- 媒体文件不存在时 WARN 并跳过(不阻断转换)

## 6. 备注(演讲者备注)

```html
<template data-slide-notes>
【核心逻辑】…
【开场 · 30秒】…
</template>
```
内容原样写入 PPTX 备注区,不影响画面。

## 7. 字体

- 页面统一 `font-family:"Noto Sans SC","Inter",sans-serif`(中文 Noto Sans SC,数字/西文 Inter,可加 `.num{font-family:"Inter"}` 类)
- **默认字体映射**(2026-07-23 起):Noto Sans SC / PingFang SC → **Microsoft YaHei**,Inter → **Arial** —— PPTX 在 Windows/Office 上开箱即用
- 若演示机器装有 Noto Sans SC / Inter、想要 100% 字形一致,在 playlist 同级放 `slides.config.json`:
  ```json
  { "applyFontMap": false }
  ```
- 需要映射其他字体时,在同一文件里加:`{ "fontMap": { "源字体名": "目标字体名" } }`

## 8. 速查表

| 特性 | 状态 | 说明 |
|---|---|---|
| 方式 A:绝对定位 + data-object | ✅ | 经典写法,语义不变 |
| 方式 B:flex/grid/流式排布 data-object | ✅ | 容器不标记不可见,可见叶子全标记;提取按计算后位置 |
| 方式 C:data-layout(stack/columns/grid) | ✅ | 子级只声明份数/高度,坐标自动;禁止嵌套、禁止混写几何 |
| 容器内重叠 data-object | ⚠️ | 叠放按 DOM 顺序;z-index 倒挂时 validate 预警 |
| data-object 嵌套标记 | ❌ | 内层无效,validate 报 ERROR |
| 纯色背景/统一边框/圆角 | ✅ | 无损 |
| 非统一边框(单边强调条等) | ✅ | 逐边细条还原;圆角卡仍建议统一边框 |
| flex/grid 容器内部(对象内部对齐) | ✅ | 子项按实际位置逐个提取 |
| font-size/weight(≥600)/color/letter-spacing | ✅ | 无损 |
| 斜体/下划线/删除线/超链接/run 级字体 | ✅ | 2026-07-27 起原生 |
| 上下标 `<sup>`/`<sub>` / run 级字距 | ✅ | 2026-07-27 P2 起原生 |
| text-transform(uppercase 等) | ✅ | 2026-07-27 起按计算样式变换 |
| 显式 line-height(多行) | ✅ | 必须显式设置 |
| `<span>` 变色加粗 / `<br>` | ✅ | 无损 |
| linear/conic-gradient / background-image | ✅ | 截图还原(2x DPI),其上叠文字安全 |
| 原生线性渐变(nativeGradient:true) | ✅ | 2026-07-27 P2 起;linear-gradient → 原生 a:gradFill(可编辑);alpha<1/radial 回退截图 |
| `<svg>` 矢量图形 | ✅ | 整体截图还原(2x DPI);**内联 SVG 图标库见 `assets/icons.md`(40 枚,stroke 必须显式 hex,禁 currentColor——截图时会被文字隐藏规则变透明)** |
| 固定高单行 + line-height=height | ✅ | 识别为居中徽章 |
| template[data-slide-notes] | ✅ | 写入备注 |
| 容器纯色背景(深色页) | ✅ | 自动导出为幻灯片背景 |
| 元素超出画布(出血装饰) | ✅ | 截图自动取与画布的交集,不变形 |
| 混合字号行(如 130px 数字 + 44px 单位) | ✅ | 行高按最大 run 字号推算 |
| 胶囊 radius=半高(长方形盒) | ✅ | 保持 stadium 圆角矩形,不会变椭圆 |
| transform:rotate(纯旋转) | ✅ | 2026-07-27 起原生;origin 须居中 |
| transform 缩放/斜切/平移 | ❌ | 丢失(validate ERROR) |
| box-shadow | ✅ | 2026-07-27 起按真实参数还原第一层;spread/多层不还原 |
| 虚线/点线边框 | ✅ | 2026-07-27 起原生 dashType |
| 预设几何 data-shape(triangle/arrow/chevron 等) | ✅ | 2026-07-27 P2 起 80+ 预设形状 |
| 半透明文字 rgba | ⚠️ | 退化纯色,请预算混合色 |
| 元素 opacity | ⚠️ | 形状填充可折算,文字按不透明处理 |
| 竖排 writing-mode | ⚠️ | 实验性(eaVert),建议逐字 `<br>` |
| mix-blend-mode / filter / backdrop-filter / outline | ⚠️ | 整体截图(不可编辑);outline 不转换 |
| `<img>` 标签 | ✅ | 2026-07-27 起原生图片;**须显式 object-fit**(D6 契约,缺省 WARN);装饰图优先用 background-image |
| `<table>` / `<ul>` / `<ol>` | ✅ | 2026-07-27 起原生表格/项目符号 |
| `<canvas>` / `data-chart` | ✅ | canvas 截图;data-chart 原生图表 |
| `<iframe>/<form>` | ❌ | 不输出(validate ERROR) |
| `<video>` | ✅ | 2026-07-27 P2 起原生嵌入(addMedia);poster 截图做封面;建议设 poster 属性 |
| `<audio>` | ✅ | 2026-07-27 P2 起原生嵌入(addMedia) |
| 母版页码/页脚(config.master) | ✅ | 2026-07-27 P2 起;slides.config.json 配 `{"master":{"pageNumbers":true,"footer":"© xxx"}}` |
| 转场动画(playlist transition) | ✅ | 2026-07-27 P2 起;playlist 项 `{"file":"01.html","transition":"fade"}`;fade/push/wipe/cover/split |
| 漏标 data-object 的可见元素 | ❌ | 元素消失(validate ERROR) |

## 9. 写完自检

```bash
node "$SKILL_DIR/scripts/preview.js" slides/    # Step 3.5:先截图自查(填充/字号/对齐/去 AI 味)
node "$SKILL_DIR/scripts/validate.js" slides/   # 再跑预检
```
- **ERROR 必须清零**(否则转换必有缺漏)
- WARN 酌情处理(多数可接受)
- **设计检查(2026-08-02 起)**:项目级 `slides.config.json` 配 `design.tier` 后,validate 额外检查
  文字适配(溢出/欠载)、字号下限(绝对 14px + 档内正文下限)、画布填充(底部留白)、
  对齐误差(边缘离群/网格突变/子级溢出)——全部 WARN 级,是视觉质量的自动守门员;
  设计原则与阈值依据见 `design-principles.md`。

## 10. 转换器行为细则(排障时读)

- **叠放**:PPTX 按 DOM 深度优先顺序绘制;`z-index` 仅影响浏览器合成(截图层)
- **字号**:1px = 0.5pt 精确换算;**行高**用绝对磅值(spcPts),与替换字体无关;**边框宽度**同样 px→pt(1px=0.5pt)
- **截图**:按 `capture.scale`(默认 2)倍分辨率输出 PNG;渐变/图片/SVG/canvas/特效区域视觉 100% 一致;`capture.imageType:'jpeg'` 可降照片型背景体积
- **列表 bullet**:LI 直接含文字时挂原生项目符号;文字位置近似(PPT 文字相对浏览器右移约 14pt);LI 含块级子元素时不挂 bullet(把文字直接放 LI 内)
- **box-shadow**:提取第一层非 inset 阴影的 angle/distance/blur/color/opacity,映射原生外阴影
- **旋转**:纯 rotate 用未旋转几何(offset 链)+ 原生 rotate 参数;截图类(渐变/SVG)按旋转后包围盒截图,不标 rotate
- **单行判定**:盒高 ≤ 行高×1.3 → 单行(不换行,垂直居中);否则多行(顶部对齐,按绝对行距)
- **对齐推断**:显式 `text-align` 优先;flex 容器按 `justify-content` 推断水平对齐、`align-items:center` 推断垂直居中
- **提取顺序**:每个元素先产背景类基元(渐变/图片截图 或 纯色形状+非统一边框细条),再产文字;逐元素深度优先
- **配置**:`scripts/config/default.config.js` 是全部可调项的唯一事实源;项目级用 `slides.config.json` 覆盖(未知键/类型错误会报错)
