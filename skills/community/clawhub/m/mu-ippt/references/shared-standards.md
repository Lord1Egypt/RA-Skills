# 通用技术标准

PPT Master 的公共技术约束，消除跨角色文件的重复内容。

---

## 1. SVG 禁用特性黑名单

以下特性在生成 SVG 时**绝对禁止**使用——一旦使用，PPT 导出会出错：

| 禁用特性 | 说明 |
|----------------|-------------|
| `mask` | 遮罩 |
| `<style>` | 内嵌样式表 |
| `class` | CSS 选择器属性（`<defs>` 内的 `id` 是合法引用，**不在**禁止范围内） |
| External CSS | 外部样式表链接 |
| `<foreignObject>` | 嵌入外部内容 |
| `<symbol>` + `<use>` | 符号引用复用 |
| `textPath` | 沿路径排列文字 |
| `@font-face` | 自定义字体声明 |
| `<animate*>` / `<set>` | SVG 动画 |
| `<script>` / event attributes | 脚本和交互事件 |
| `<iframe>` | 嵌入框架 |

> **`marker-start` / `marker-end` 有条件允许**——详见 §1.1 的约束条件。转换器会将合规的 marker 映射为原生 DrawingML 的 `<a:headEnd>` / `<a:tailEnd>`。
>
> **`<image>` 上的 `clipPath` 有条件允许**——详见 §1.2 的约束条件。转换器会将合规的裁剪形状映射为原生 DrawingML 图片几何体（`<a:prstGeom>` 或 `<a:custGeom>`）。

---

### 1.1 线端标记（有条件允许）

`<line>` 和 `<path>` 元素上的 `marker-start` 和 `marker-end` **仅在**引用的 `<marker>` 满足以下所有条件时才允许使用：

| 要求 | 原因 |
|-------------|--------|
| `<marker>` 元素定义在 `<defs>` 内 | 转换器通过 id 索引查找 marker 定义 |
| `orient="auto"` | DrawingML 箭头沿线条切线方向自动旋转；其他 orient 值无法正确往返转换 |
| marker 形状**必须是以下之一**：封闭的 3 顶点 path/polygon（三角形）、封闭的 4 顶点 path/polygon（菱形）、`<circle>` / `<ellipse>`（椭圆形） | 这三种形状可以干净地映射到 DrawingML 的 `type="triangle" / "diamond" / "oval"`。其他形状会被静默丢弃并产生警告。 |
| marker 子元素的 `fill` **必须匹配**父线条的 `stroke` 颜色 | DrawingML 中箭头继承线条颜色——fill 不匹配会导致导出后显示异常。 |
| `markerWidth` / `markerHeight` 大致在 `3–15` 范围内 | 映射到 `sm`（<6）/ `med`（6–12）/ `lg`（>12）尺寸档位。 |

**使用边界**：

- `marker-start` / `marker-end` 仅用于以线条为主体的连接箭头。
- **不要**将 `marker` 用于块状/粗大/宽实心箭头——这类箭头的箭体才是主要视觉元素。
- 对于实心箭头，请绘制独立的封闭 `<path>` / `<polygon>`，可参考 `templates/charts/chevron_process.svg` 或 `templates/charts/process_flow.svg`。

**支持的 DrawingML 映射**：

| SVG Marker 形状 | DrawingML 输出 |
|------------------|------------------|
| `<path d="M0,0 L10,5 L0,10 Z"/>`（三角形） | `<a:tailEnd type="triangle" w="med" len="med"/>` |
| `<polygon points="0,0 10,5 0,10"/>` | `<a:tailEnd type="triangle" w="med" len="med"/>` |
| 4 顶点封闭 path/polygon | `<a:tailEnd type="diamond" .../>` |
| `<circle cx="5" cy="5" r="4"/>` | `<a:tailEnd type="oval" .../>` |

**推荐模板**——可直接复用的标准箭头定义：

```xml
<defs>
  <marker id="arrowHead" markerWidth="10" markerHeight="10" refX="9" refY="5"
          orient="auto" markerUnits="strokeWidth">
    <path d="M0,0 L10,5 L0,10 Z" fill="#1976D2"/>
  </marker>
</defs>
<line x1="100" y1="200" x2="400" y2="200" stroke="#1976D2" stroke-width="3"
      marker-end="url(#arrowHead)"/>
```

> ⚠️ 警告：无法识别的 marker 形状（弯曲路径、多段路径、超过 4 个顶点等）会被转换器**静默丢弃**并产生警告——线条仍会渲染，但不带箭头。如果需要特殊箭头形状，请退而使用手动绘制的 `<polygon>` 三角形。

---

### 1.2 图片裁剪（有条件允许）

`<image>` 元素上的 `clip-path` 在引用的 `<clipPath>` 满足以下条件时允许使用：

| 要求 | 原因 |
|-------------|--------|
| `<clipPath>` 元素定义在 `<defs>` 内 | 转换器通过 id 索引查找裁剪定义 |
| 仅包含**一个**形状子元素 | 使用第一个子元素；多个子元素不会合成 |
| 形状为以下之一：`<circle>`、`<ellipse>`、`<rect>`（带 rx/ry）、`<path>`、`<polygon>` | 这些形状可映射为 DrawingML 几何体（预设或自定义） |
| **仅用于 `<image>` 元素** | 非图片元素使用 clip-path 是**禁止的** |

**使用边界**：

- `clip-path` **仅用于**将 `<image>` 元素裁剪为非矩形形状（圆形头像、圆角照片框、六角形肖像等）。
- **不要**在形状元素上使用 `clip-path`（`<rect>`、`<circle>`、`<path>`、`<g>`、`<text>` 等）——直接绘制目标形状即可。一个被裁剪成圆形的矩形就是一个圆形，直接画 `<circle>` 就好。
- PowerPoint 的 SVG 渲染器**无法正确渲染 `clipPath`**（图片会变成不可见，形状会丢失裁剪）。原生 PPTX 转换器可以处理，但 SVG 参考版本会显示不正确。

**支持的 DrawingML 映射**：

| SVG 裁剪形状 | DrawingML 输出 | 使用场景 |
|----------------|------------------|----------|
| `<circle>` / `<ellipse>` | `<a:prstGeom prst="ellipse"/>` | 圆形头像、椭圆框 |
| `<rect rx="..."/>` | `<a:prstGeom prst="roundRect"/>` 带 adj 值 | 圆角矩形照片框 |
| `<path>` / `<polygon>` | `<a:custGeom>` 带路径命令 | 六角形、菱形、自定义形状 |

**推荐模板**——圆形图片裁剪：

```xml
<defs>
  <clipPath id="avatarClip">
    <circle cx="200" cy="200" r="100"/>
  </clipPath>
</defs>
<image href="../images/photo.jpg" x="100" y="100" width="200" height="200"
       clip-path="url(#avatarClip)" preserveAspectRatio="xMidYMid slice"/>
```

**圆角矩形裁剪**——用于卡片式图片框：

```xml
<defs>
  <clipPath id="cardClip">
    <rect x="60" y="120" width="400" height="250" rx="16"/>
  </clipPath>
</defs>
<image href="../images/banner.jpg" x="60" y="120" width="400" height="250"
       clip-path="url(#cardClip)" preserveAspectRatio="xMidYMid slice"/>
```

> ⚠️ 警告：非图片元素上使用 `clip-path` 是**禁止的**——质量检查器会将其报告为错误。对于形状，请直接绘制目标几何体；对于组，请重新组织布局。

---

## 2. PPT 兼容性替代方案

| 禁止语法 | 正确替代方案 |
|---------------|---------------------|
| `fill="rgba(255,255,255,0.1)"` | `fill="#FFFFFF" fill-opacity="0.1"` |
| `<g opacity="0.2">...</g>` | 在每个子元素上分别设置 `fill-opacity` / `stroke-opacity` |
| `<image opacity="0.3"/>` | 在图片之后叠加 `<rect fill="背景色" opacity="0.7"/>` 遮罩层 |

**助记**：PPT 不识别 rgba、组透明度和图片透明度。

> 箭头：连接线优先使用带合规 `<marker>` 的 `marker-end`（参见 §1.1）——转换器会生成自动旋转的原生 DrawingML 箭头。对于块状箭头/粗箭头，使用独立的封闭形状代替 `marker`；可参考 `templates/charts/chevron_process.svg`（阶段箭头）和 `templates/charts/process_flow.svg`（混合流程布局）。

---

## 3. 画布格式速查表

### 演示文稿

| 格式 | viewBox | 尺寸 | 比例 |
|--------|---------|------------|-------|
| PPT 16:9 | `0 0 1280 720` | 1280x720 | 16:9 |
| PPT 4:3 | `0 0 1024 768` | 1024x768 | 4:3 |

### 社交媒体

| 格式 | viewBox | 尺寸 | 比例 |
|--------|---------|------------|-------|
| 小红书 | `0 0 1242 1660` | 1242x1660 | 3:4 |
| 微信朋友圈 / Instagram Post | `0 0 1080 1080` | 1080x1080 | 1:1 |
| Story / 抖音竖版 | `0 0 1080 1920` | 1080x1920 | 9:16 |

### 营销物料

| 格式 | viewBox | 尺寸 | 比例 |
|--------|---------|------------|-------|
| 微信公众号头图 | `0 0 900 383` | 900x383 | 2.35:1 |
| 横版 Banner | `0 0 1920 1080` | 1920x1080 | 16:9 |
| 竖版海报 | `0 0 1080 1920` | 1080x1920 | 9:16 |
| A4 印刷（150dpi） | `0 0 1240 1754` | 1240x1754 | 1:1.414 |

---

## 4. SVG 基础规则

- **viewBox** 必须与画布尺寸一致（`width`/`height` 必须与 `viewBox` 匹配）
- **背景**：使用 `<rect>` 定义页面背景色
- **换行**：使用 `<tspan>` 手动换行；`<foreignObject>` 是禁止的
- **字体**：仅使用系统字体（Microsoft YaHei、Arial、Calibri 等）；`@font-face` 是禁止的
- **样式**：仅使用内联样式（`fill="..."` `font-size="..."`）；`<style>` / `class` 是禁止的（`<defs>` 内的 `id` 是合法的）
- **颜色**：使用 HEX 值；透明度使用 `fill-opacity` / `stroke-opacity`
- **图片引用**：`<image href="../images/xxx.png" preserveAspectRatio="xMidYMid slice"/>`
- **图标占位符**：`<use data-icon="chunk/name" x="" y="" width="48" height="48" fill="#HEX"/>`（默认图标库）；或在该演示选用的图标库下使用 `tabler-filled/name` / `tabler-outline/name`（后处理阶段自动嵌入）。始终包含图标库前缀。**一套演示文稿 = 一个图标库——禁止混用。**

### 元素分组（必须遵守）

逻辑相关的元素**必须**用 `<g>` 标签包裹。这样导出的 PPTX 中会生成 PowerPoint 组合，便于选中、移动和编辑幻灯片。

> ⚠️ 警告：**仅 `<g opacity="...">` 被禁止**（参见 §2）。用于结构分组的普通 `<g>` 是必须的。

**需要分组的内容**：

| 分组单元 | 包含内容 |
|---------------|----------|
| 卡片/面板 | 背景矩形 + 阴影 + 图标 + 标题 + 正文 |
| 流程步骤 | 序号圆圈 + 图标 + 标签 + 描述 |
| 列表项 | 项目符号/序号 + 图标 + 标题 + 描述 |
| 图标-文字组合 | 图标元素 + 旁边的标签 |
| 页眉 | 标题 + 副标题 + 装饰线条 |
| 页脚 | 页码 + 品牌标识 |
| 装饰元素集 | 相关的装饰形状（圆环、光球、圆点） |

**示例**：

```xml
<g id="card-benefits-1">
  <rect x="60" y="115" width="565" height="260" rx="20" fill="#FFFFFF" filter="url(#shadow)"/>
  <use data-icon="bolt" x="108" y="163" width="44" height="44" fill="#0071E3"/>
  <text x="105" y="270" font-size="56" font-weight="bold" fill="#0071E3">10×</text>
  <text x="250" y="270" font-size="30" font-weight="bold" fill="#1D1D1F">Faster</text>
  <text x="105" y="310" font-size="18" fill="#6E6E73">Reduce production time from days to hours.</text>
</g>
```

**命名规范**：在 `<g>` 标签上使用描述性的 `id` 属性（如 `card-1`、`step-discover`、`header`、`footer`）。id 不是必须的，但推荐使用以提升可读性。

---

## 5. 后处理流水线（3 步）

必须按顺序执行——禁止跳过步骤或添加额外参数：

```bash
# 1. 将演讲备注拆分为逐页备注文件
python3 scripts/total_md_split.py <project_path>

# 2. SVG 后处理（图标嵌入、图片裁剪/嵌入、文字拉平、圆角矩形转路径）
python3 scripts/finalize_svg.py <project_path>

# 3. 导出 PPTX（从 svg_final/ 导出，默认嵌入演讲备注）
python3 scripts/svg_to_pptx.py <project_path> -s final
# 输出: exports/<project_name>_<timestamp>.pptx + exports/<project_name>_<timestamp>_svg.pptx
```

**禁止事项**：
- 绝不能用 `cp` 替代 `finalize_svg.py`
- 绝不能直接从 `svg_output/` 导出——必须从 `svg_final/` 导出（使用 `-s final`）
- 绝不能添加 `--only` 等额外参数

**重新运行规则**：后处理完成后，对 `svg_output/` 的任何修改（包括页面修改、新增或删除）都需要重新运行第 2 步和第 3 步。只有 `notes/total.md` 也被修改时，才需要重新运行第 1 步。

---

## 6. 阴影与遮罩技法

> `<mask>` 元素和 `<image opacity="...">` 是禁止的。请始终使用堆叠的 `<rect>` 或渐变遮罩代替（参见 §2）。

### 阴影

#### 滤镜柔阴影——推荐方案

最适合：卡片、浮动面板、悬浮元素。`svg_to_pptx` 转换器会自动将 `feGaussianBlur` + `feOffset` 转换为原生 PPTX 的 `<a:outerShdw>`。

```xml
<defs>
  <filter id="softShadow" x="-15%" y="-15%" width="140%" height="140%">
    <feGaussianBlur in="SourceAlpha" stdDeviation="12"/>
    <feOffset dx="0" dy="6" result="offsetBlur"/>
    <feFlood flood-color="#000000" flood-opacity="0.15" result="shadowColor"/>
    <feComposite in="shadowColor" in2="offsetBlur" operator="in" result="shadow"/>
    <feMerge>
      <feMergeNode in="shadow"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
</defs>
<rect x="60" y="60" width="400" height="240" rx="12" fill="#FFFFFF" filter="url(#softShadow)"/>
```

推荐参数：
```
stdDeviation:   10–16    （值越小越锐利，值越大越柔和）
flood-opacity:  0.12–0.20  （太低在 PPTX 中会看不见）
dy:             4–8      （垂直偏移 > 水平偏移，模拟自然顶光效果）
dx:             0–2
```

#### 彩色阴影

最适合：强调按钮、品牌色卡片。使用元素自身的色系而非黑色。

```xml
<filter id="colorShadow" x="-15%" y="-15%" width="140%" height="140%">
  <feGaussianBlur in="SourceAlpha" stdDeviation="10"/>
  <feOffset dx="0" dy="6" result="offsetBlur"/>
  <feFlood flood-color="#1A73E8" flood-opacity="0.20" result="shadowColor"/>
  <feComposite in="shadowColor" in2="offsetBlur" operator="in" result="shadow"/>
  <feMerge>
    <feMergeNode in="shadow"/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>
```

将 `flood-color` 替换为元素的品牌色；`flood-opacity` 保持在 0.15–0.25 之间。

#### 发光效果

最适合：标题高亮、关键指标、主视觉文字。转换器会自动将不带 `feOffset` 的 `feGaussianBlur` 转换为原生 PPTX 的 `<a:glow>`。

```xml
<defs>
  <filter id="titleGlow" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur in="SourceAlpha" stdDeviation="6" result="blur"/>
    <feFlood flood-color="#1A73E8" flood-opacity="0.45" result="glowColor"/>
    <feComposite in="glowColor" in2="blur" operator="in" result="glow"/>
    <feMerge>
      <feMergeNode in="glow"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
</defs>
<text x="640" y="360" text-anchor="middle" font-size="48" fill="#1A73E8" filter="url(#titleGlow)">Key Insight</text>
```

推荐参数：
```
stdDeviation:   4–8      （值越小越含蓄，值越大越醒目）
flood-color:    品牌色或强调色（不要用黑色）
flood-opacity:  0.35–0.55  （比阴影更强以确保可见性）
```

**与阴影的关键区别**：没有 `<feOffset>` 元素（或 dx=0/dy=0）。转换器以此区分发光和阴影。

#### 堆叠矩形阴影——高兼容性备选方案

最适合：需要兼容旧版 PowerPoint 的场景。在主卡片后方堆叠 2–3 个半透明矩形：

```xml
<!-- 阴影层（从后到前，最大偏移在最底层） -->
<rect x="68" y="72" width="400" height="240" rx="16" fill="#000000" fill-opacity="0.03"/>
<rect x="65" y="69" width="400" height="240" rx="14" fill="#000000" fill-opacity="0.05"/>
<rect x="62" y="66" width="400" height="240" rx="12" fill="#1A73E8" fill-opacity="0.04"/>
<!-- 主卡片 -->
<rect x="60" y="60" width="400" height="240" rx="12" fill="#FFFFFF"/>
```

### 图片遮罩

#### 线性渐变遮罩——最常用

最适合：图文页面。渐变方向应与文字位置一致（文字在左 → 渐变朝左变暗）。

```xml
<image href="..." x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
<defs>
  <linearGradient id="imgOverlay" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%"   stop-color="#1A1A2E" stop-opacity="0.85"/>
    <stop offset="55%"  stop-color="#1A1A2E" stop-opacity="0.30"/>
    <stop offset="100%" stop-color="#1A1A2E" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect x="0" y="0" width="1280" height="720" fill="url(#imgOverlay)"/>
```

#### 底部渐变条

最适合：封面页和全图页面，标题在底部。

```xml
<defs>
  <linearGradient id="bottomBar" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%"   stop-color="#000000" stop-opacity="0"/>
    <stop offset="100%" stop-color="#000000" stop-opacity="0.72"/>
  </linearGradient>
</defs>
<rect x="0" y="380" width="1280" height="340" fill="url(#bottomBar)"/>
```

#### 径向渐变遮罩——暗角效果

最适合：全屏氛围页；将注意力引导到画面中央。

```xml
<defs>
  <radialGradient id="vignette" cx="50%" cy="50%" r="70%">
    <stop offset="0%"   stop-color="#000000" stop-opacity="0"/>
    <stop offset="100%" stop-color="#000000" stop-opacity="0.58"/>
  </radialGradient>
</defs>
<rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>
```

#### 品牌色遮罩

最适合：需要强烈品牌视觉的页面。

```xml
<defs>
  <linearGradient id="brandOverlay" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%"   stop-color="#005587" stop-opacity="0.80"/>
    <stop offset="100%" stop-color="#005587" stop-opacity="0.10"/>
  </linearGradient>
</defs>
<rect x="0" y="0" width="1280" height="720" fill="url(#brandOverlay)"/>
```

### 速查表

| 场景 | 推荐技法 | 避免使用 |
|----------|-----------------------|-------|
| 卡片/面板阴影 | 滤镜柔阴影（`flood-opacity` ≤ 0.12） | 硬黑色阴影 |
| 强调/CTA 按钮 | 彩色阴影（同色系） | 通用灰色阴影 |
| 标题/指标高亮 | 发光滤镜（品牌色，无偏移） | 在正文上过度使用 |
| 图文页面 | 线性渐变遮罩（方向与文字侧一致） | 整张图片覆盖均匀平坦透明度 |
| 封面/全图页面 | 底部渐变条 + 品牌色 | 纯黑色遮罩 |
| 氛围/主视觉页面 | 径向暗角 | 未处理的原始图片 |
| 需要最大 PPT 兼容性 | 堆叠矩形阴影 | 基于滤镜的阴影 |

---

## 7. 描边、文字与形状效果

### stroke-dasharray——虚线/点线

转换为原生 PPTX 的 `<a:prstDash>`。建议使用预设模式以获得最佳效果：

| SVG 值 | PPTX 预设 | 最佳用途 |
|-----------|-------------|----------|
| `4,4` | Dash | 通用虚线、分隔线 |
| `2,2` | Dot (sysDot) | 细微点线边框、占位轮廓 |
| `8,4` | Long dash | 时间轴连接线、流程箭头 |
| `8,4,2,4` | Long dash-dot | 技术图纸、标注线 |

```xml
<rect x="60" y="60" width="400" height="240" rx="12"
  fill="none" stroke="#999999" stroke-width="2" stroke-dasharray="4,4"/>

<line x1="100" y1="360" x2="1180" y2="360"
  stroke="#CCCCCC" stroke-width="1" stroke-dasharray="2,2"/>
```

### stroke-linejoin

控制线段在拐角处的连接方式。支持的值会转换为原生 PPTX 线条连接类型：

| SVG 值 | PPTX 等效 | 最佳用途 |
|-----------|-----------------|----------|
| `round` | Round join | 平滑折线图、有机形状 |
| `bevel` | Bevel join | 技术图示 |
| `miter` | Miter join（默认） | 尖角矩形、箭头 |

```xml
<polyline points="100,200 200,100 300,200" fill="none"
  stroke="#1A73E8" stroke-width="3" stroke-linejoin="round"/>
```

### text-decoration

支持的文字装饰会转换为原生 PPTX 文字格式：

| SVG 值 | PPTX 等效 | 最佳用途 |
|-----------|-----------------|----------|
| `underline` | 单下划线 | 强调、链接、关键术语 |
| `line-through` | 删除线 | 已移除项、改前/改后对比 |

```xml
<text x="100" y="200" font-size="20" fill="#333333" text-decoration="underline">Important Term</text>

<!-- 逐 tspan 设置装饰 -->
<text x="100" y="240" font-size="18" fill="#333333">
  Regular text <tspan text-decoration="line-through" fill="#999999">old value</tspan> new value
</text>
```

### 渐变填充——linearGradient 与 radialGradient

在 `<defs>` 中定义的渐变通过 `fill="url(#id)"` 引用，会转换为原生 PPTX 的 `<a:gradFill>`。可用作形状填充（不仅仅是遮罩层），打造精致的表面效果。

**线性渐变**——最适合按钮、标题栏、背景面板：

```xml
<defs>
  <linearGradient id="btnGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#1A73E8"/>
    <stop offset="100%" stop-color="#0D47A1"/>
  </linearGradient>
</defs>
<rect x="540" y="600" width="200" height="48" rx="24" fill="url(#btnGrad)"/>
```

**径向渐变**——最适合聚光背景、圆形装饰：

```xml
<defs>
  <radialGradient id="spotBg" cx="50%" cy="50%" r="70%">
    <stop offset="0%" stop-color="#1A73E8" stop-opacity="0.15"/>
    <stop offset="100%" stop-color="#1A73E8" stop-opacity="0"/>
  </radialGradient>
</defs>
<circle cx="640" cy="360" r="300" fill="url(#spotBg)"/>
```

### transform: rotate——元素旋转

旋转会转换为原生 PPTX 的 `<a:xfrm rot="...">`。支持所有元素类型：`rect`、`circle`、`ellipse`、`line`、`path`、`polygon`、`polyline`、`image` 和 `text`。

```xml
<!-- 旋转的装饰元素 -->
<rect x="100" y="100" width="60" height="60" fill="#1A73E8" fill-opacity="0.1"
  transform="rotate(45, 130, 130)"/>

<!-- 旋转的文字标签 -->
<text x="50" y="400" font-size="14" fill="#999999"
  transform="rotate(-90, 50, 400)">Y-Axis Label</text>
```

**语法**：`rotate(angle)` 或 `rotate(angle, cx, cy)`，其中 `cx,cy` 为旋转中心。正角度为顺时针旋转。

### 弧形路径——环形图/饼图

使用 `<path>` 绘制环形图或饼图扇区时，弧线端点坐标必须通过三角函数精确计算。**绝不能估算或近似弧线端点**——即使很小的误差也会导致完全错误的形状。

**计算公式**（圆心 `cx,cy`，半径 `r`，角度 `θ` 单位为度）：
```
x = cx + r × cos(θ × π / 180)
y = cy + r × sin(θ × π / 180)
```

**关键规则**：
1. 从 **-90°**（12 点钟方向）开始，顺时针旋转
2. 每个扇区跨越 `百分比 × 360°`
3. 扇区 > 180° 时使用 **large-arc flag = 1**，否则为 **0**
4. sweep-direction = 1（顺时针）用于外弧，0（逆时针）用于内弧回程
5. **务必验证**所有扇区角度之和等于 360°，且最后一个扇区的终点与第一个扇区的起点重合

**示例——75% 环形扇区**（圆心 400,400，外半径 r=180，内半径 r=100）：
```
起始角度: -90°    → outer(400, 220), inner(400, 300)
终止角度: -90+270=180° → outer(220, 400), inner(300, 400)
Large-arc flag: 1 (270° > 180°)

<path d="M 400,220 A 180,180 0 1,1 220,400 L 300,400 A 100,100 0 1,0 400,300 Z"/>
```

### 斜线上的多边形箭头

> 连接线优先使用 `marker-end` / `marker-start`（参见 §1.1）。对于块状/宽实心/非连接箭头，使用独立的 polygon 或 path 几何体代替 `marker`。

在使用 `<polygon>` 三角形作为箭头时，**水平或垂直线条**上的箭头可以用简单的点偏移。但**斜线**上的箭头必须旋转三角形顶点以匹配线条方向。

**方法**：使用线条的方向向量计算三角形顶点：

```
给定线条从 (x1,y1) 到 (x2,y2)：
1. 方向向量: dx = x2-x1, dy = y2-y1
2. 归一化: len = √(dx²+dy²), ux = dx/len, uy = dy/len
3. 垂直向量: px = -uy, py = ux
4. 箭头尖端 = (x2, y2)
5. 后方点 1 = (x2 - ux×12 + px×5,  y2 - uy×12 + py×5)
6. 后方点 2 = (x2 - ux×12 - px×5,  y2 - uy×12 - py×5)
```

**示例——斜线**从 (260,310) 到 (370,430)：
```
dx=110, dy=120, len≈162.8, ux=0.676, uy=0.737
px=-0.737, py=0.676
尖端: (370, 430)
后方1: (370-8.1-3.7, 430-8.8+3.4) = (358.2, 424.6)
后方2: (370-8.1+3.7, 430-8.8-3.4) = (365.6, 417.8)

<polygon points="370,430 365.6,417.8 358.2,424.6" fill="#C8A96E"/>
```

⚠️ 警告：**绝不能在斜线上使用固定的向下/向右三角形**——箭头会指向错误的方向。

---

## 8. 排版美学（SVG 场景）

从 CSS/印刷设计翻译为 SVG 专用规则的高级排版原则。这些原则能将文字从"技术上正确"提升到"专业排版"水准。

### 均衡换行（等效于 CSS `text-wrap: balance`）

当标题或大标题跨越多个 `<tspan>` 行时，**尽可能将字符均匀分配到各行**。避免一行占满而下一行只剩 1-3 个字符的失衡断行。

**规则**：多行标题的每一行长度应在平均行长的 ±20% 以内。

```xml
<!-- ❌ 不好：不均衡 -->
<text x="640" y="200" text-anchor="middle" font-size="48">
  <tspan x="640" dy="0">Artificial Intelligence Transformation</tspan>
  <tspan x="640" dy="58">Strategy</tspan>
</text>

<!-- ✅ 好：均衡 -->
<text x="640" y="200" text-anchor="middle" font-size="48">
  <tspan x="640" dy="0">Artificial Intelligence</tspan>
  <tspan x="640" dy="58">Transformation Strategy</tspan>
</text>
```

### 避免孤字和寡行（等效于 CSS `text-wrap: pretty`）

- **孤字（Orphan）**：文本块最后一行只剩一个词或 1-2 个字符。通过调整换行位置来避免，确保最后一行至少有 4 个字符（中日韩文）或 2 个单词（拉丁文）。
- **寡行（Widow）**：段落的单独一行落在新列或新页的顶部。在 PPT 场景中：避免拆分文本块导致只有一行出现在不同的视觉区域。

**规则**：使用 `<tspan>` 编写多行正文时，确保最后一行至少包含平均行长的 30%。

### 悬挂标点（等效于 CSS `hanging-punctuation`）

对于中日韩文本，开头标点符号（「『（【〈）和结尾标点（」』）】〉、。，）应做视觉对齐——标点符号本身不应计入左边缘对齐。

**SVG 实现方式**：当中日韩文本行以标点符号开头时，将 `<tspan>` 的 x 坐标向左偏移约半个字号（例如，18px 字号时用 `x="32"` 代替 `x="40"`），以保持与非标点行的视觉对齐。

### 行间距

- **标题文字**：`<tspan>` 行间 `dy` = 字号 × 1.2（紧凑但可读）
- **正文文字**：`<tspan>` 行间 `dy` = 字号 × 1.5（舒适阅读）
- **密排正文**：`dy` = 字号 × 1.3（可接受的最小值）

### 数字格式一致性

- 数字列使用**等宽/表格对齐**：通过右对齐数字 `<tspan>` 或使用 `text-anchor="end"` 确保所有数字占据相同宽度
- 大数字：全篇统一使用千分位分隔符（1,234,567）或缩写形式（1.2M）
- 百分号、货币符号：全篇保持一致的间距和位置

---

## 9. 项目目录结构

```
project/
├── svg_output/    # 原始 SVG（执行者输出，包含占位符）
├── svg_final/     # 后处理后的最终 SVG（finalize_svg.py 输出）
├── images/        # 图片素材（用户提供 + AI 生成）
├── notes/         # 演讲备注（与 SVG 同名的 .md 文件）
│   └── total.md   # 完整的演讲备注文档（拆分前）
├── templates/     # 项目模板（如有）
└── *.pptx         # 导出的 PPT 文件
```

---

## 10. 技术图表专用规范

### 箭头语义

生成技术图表（架构图、流程图、Agent 图等）时，必须读取 `references/arrow-semantics.md` 并遵循箭头语义编码规范。

### 形状词汇

生成技术图表时，应优先使用 `references/shape-vocabulary.md` 中定义的标准化形状模板，确保语义一致性。

### 产品图标

当图表中出现已知技术产品时，应使用 `references/tech-product-icons.md` 中的品牌图标模板。
