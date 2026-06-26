---
name: ppt-vision-replica
description: |
  将PPT截图或信息图转换为可编辑的PPTX文件。此技能基于Images2Slides论文(arXiv:2602.07645)实现，
  利用视觉-语言模型(VLM)进行区域理解，通过坐标映射算法将像素坐标转换为PPTX坐标。
  支持复杂形状降级处理策略（custGeom/渐变/透明等无法直接还原的形状转为PNG嵌入）。
  触发场景：用户上传PPT截图并要求复刻、用户要求分析PPT结构、用户希望将图片PPT转换为可编辑版本。
version: 1.5.0
requires:
  os: [linux, darwin, win32]
  npm: [pptxgenjs]
  python: [Pillow]   # 仅复杂形状降级时需要
  filesystem: true    # 读写临时PNG和输出PPTX文件
  network: true       # 调用外部VLM处理图像（图片数据会发送到配置的VLM服务端点）
---

> **⚠️ 使用前须知**
> - **图片数据发送**：第一步 VLM 图像分析会将截图发送到配置的 VLM 服务端点（如 OpenClaw image 工具 / MiniMax Vision / GPT-4V 等）。请勿使用本技能处理涉密或敏感的幻灯片。
> - **文件系统**：技能会生成临时 PNG 文件和输出 PPTX 文件，确保运行环境允许文件读写操作。
> - **运行时依赖**：需提前安装 `npm install -g pptxgenjs`；如需复杂形状降级，还需安装 Python + Pillow。

# PPT视觉复刻技能 (v1.5)

将静态PPT截图/信息图转换为可编辑PPTX文件的完整工作流。

## 核心算法 (Images2Slides论文适配)

### 坐标映射 (Pixel → EMU)

```
EMU = Pixel × (914400 / DPI)
Slide_X = (Image_X / Image_Width) × Slide_Width_EMU
Slide_Y = (Image_Y / Image_Height) × Slide_Height_EMU
```

标准16:9幻灯片尺寸: 9144000 × 5143500 EMU

## 工作流程

### 阶段1: 图像分析（开放式 VLM 调用）

第一步的图片识别为开放式设计，可灵活接入任意具备图像理解能力的工具——
如 OpenClaw 内置 `image` 工具（默认，MiniMax Vision VLM）、MCP VLM 服务、GPT-4V 等。
后续坐标映射和 PPT 生成逻辑与具体 VLM 解耦，保持稳定。

**必须**使用以下增强版 Prompt，以确保符号精度和格式完整性：

```javascript
const ENHANCED_PROMPT = `分析这张PPT截图，精确输出所有可见区域的信息。

输出格式为JSON数组，每个元素包含：
{
  "id": "数字",
  "type": "rectangle | roundedRect | text | line | image",
  "role": "header_bar | title | subtitle | body | data_card | footer | decorator | bullet_list",
  "bounds": { "x": 像素, "y": 像素, "width": 像素, "height": 像素 },
  "color": "#十六进制颜色（文字颜色或形状填充色）",
  "backgroundColor": "#背景填充色（仅形状适用）",
  "lineColor": "#边框颜色（如有边框）",
  "lineWidth": 边框宽度,
  "content": "文字内容（保持原版的所有标点符号，全角/半角符号原样保留）",
  "fontSize": 字号数字（磅），
  "fontFamily": "字体名称",
  "fontWeight": "normal | bold",
  "align": "left | center | right",
  "lineSpacing": 行间距倍数（1.0/1.5/2.0），
  "charSpacing": 字符间距（磅），
  "bulletType": "无bullet则null，有bullet则填 ■ / ✓ / - 等符号",
  "cornerRadius": 圆角大小（仅roundedRect适用），
  "zIndex": 叠加层级（从0开始）
}

⚠️ 特别注意：
1. content 必须保持原版的所有标点符号，包括全角括号（）和半角括号()的区别
2. 不要添加或删除任何字符
3. 项目符号（■、✓、1.、-）必须原样记录在 bulletType 字段
4. 识别所有行间距较大的文本框，填写 lineSpacing
5. 边框矩形必须填写 lineColor，填充矩形填写 backgroundColor
6. zIndex按照视觉层叠顺序从后到前递增`;
```

### 阶段2: 结构化数据解析

调用 `scripts/coordinate_mapper.js`，支持4种JSON提取策略，自动容错：

```javascript
const { parseAnalysisToRegions, mapAllRegions } = require('./coordinate_mapper');

// 解析分析结果（自动处理全角符号校正和bullet识别）
const regions = parseAnalysisToRegions(analysisText);

// 批量映射坐标
const mappedRegions = mapAllRegions(regions, imageWidth, imageHeight);
```

**新增功能（v1.1）：**
- `normalizeSymbols(text)` — 全角/半角符号校正
- `detectBullet(text)` — 识别并提取bullet符号类型
- 4策略JSON解析容错（直接解析 → 数组提取 → 对象提取 → 代码块提取）

### 阶段3: PPT生成

调用 `scripts/ppt_generator.js`：

```javascript
const { saveFromRegions } = require('./ppt_generator');

await saveFromRegions(mappedRegions, 'output.pptx', {
  imageWidth: 2100,
  imageHeight: 1192,
  background: '#FFFFFF'  // 可选背景色
});
```

## 区域类型映射

| VLM输出 | PptxGenJS方法 | v1.1新增支持 |
|--------|--------------|------------|
| rectangle (filled) | `slide.addShape('rect')` | backgroundColor / lineColor |
| rectangle (border) | `slide.addShape('rect')` | lineWidth / dashType |
| **roundedRect** | `slide.addShape('roundRect')` | ✅ 新增 cornerRadius |
| text | `slide.addText()` | ✅ lineSpacing / charSpacing / bullet |
| line | `slide.addShape('line')` | dashType |
| image | `slide.addImage()` | data(base64) / path |
| **复杂形状** | `slide.addImage()` + Python绘制PNG | ✅ v1.2新增 |

---

## 复杂形状降级处理策略 (v1.2)

> **核心思路**：pptxgenjs 无法还原的复杂图形，改用 **Python/Pillow 绘制精确 PNG（透明背景）→ 嵌入 PPT** 的方式替代。

### 何时触发降级

遇到以下情况时，应将该形状标记为 `type: "complex_shape"`，使用降级策略处理：

| 形状特征 | 判断依据 |
|---------|---------|
| **自定义多边形路径** | XML中存在 `<a:custGeom>` 标签，包含贝塞尔曲线、不规则路径 |
| **透明渐变填充** | 多色渐变（3个以上 stop）或带透明度通道（alpha < 100%）的渐变 |
| **复合渐变方向** | 渐变角度非水平/垂直（非0/90/180/270度），如斜向渐变 |
| **发光/阴影特效** | `<a:outerShdw>`, `<a:glow>` 等复杂效果 pptxgenjs 渲染误差大 |
| **不规则遮罩/裁切** | 图片经过自定义路径裁切（`<p:spPr><a:custGeom>` 包裹图片） |
| **VLM识别为渐变箭头/装饰图形** | 从截图分析中识别出类型为装饰性渐变形状 |

---

### 降级处理工作流

```
┌─────────────────────────────────────────────────────┐
│ 1. 判断是否为复杂形状（见上表）                          │
│    ├── 有原版PPTX → 从XML提取精确路径和颜色参数            │
│    └── 仅截图 → 用VLM估算形状轮廓和渐变颜色                │
│                                                     │
│ 2. 用Python/Pillow绘制透明背景PNG                       │
│    ├── 绘制精确路径（参考XML坐标 或 VLM估算像素）           │
│    ├── 应用渐变/透明/特效                               │
│    └── 输出 RGBA 透明背景 PNG                          │
│                                                     │
│ 3. 嵌入PPT（addImage）                               │
│    └── 坐标与原版对应（EMU换算或比例缩放）                  │
└─────────────────────────────────────────────────────┘
```

---

### 从原版XML提取形状参数（有源文件时优先）

当有原版 `.pptx` 可解包时，可获取最精确的参数：

```bash
# 解包PPTX
unzip original.pptx -d pptx_unpacked/
# 查看形状XML
cat pptx_unpacked/ppt/slides/slide1.xml
```

**关键字段提取：**

```xml
<!-- 自定义路径形状 -->
<a:custGeom>
  <a:pathLst>
    <a:path w="5725" h="1294">   <!-- 路径画布尺寸（EMU相对坐标）-->
      <a:moveTo><a:pt x="2852" y="0"/></a:moveTo>  <!-- 起点 -->
      <a:cubicBezTo>...</a:cubicBezTo>              <!-- 贝塞尔曲线 -->
      <a:lnTo>...</a:lnTo>                          <!-- 直线段 -->
    </a:path>
  </a:pathLst>
</a:custGeom>

<!-- 渐变填充 -->
<a:gradFill>
  <a:gsLst>
    <a:gs pos="0"><a:srgbClr val="FFFFFF"/></a:gs>    <!-- 白色，pos=0% -->
    <a:gs pos="100000"><a:srgbClr val="C00000"/></a:gs> <!-- 红色，pos=100% -->
  </a:gsLst>
  <a:lin ang="16200000" scaled="0"/>  <!-- ang=16200000 = 270°（EMU角度单位：60000/度）-->
</a:gradFill>

<!-- 形状在组合(grpSp)中的位置 -->
<a:off x="696" y="2680"/>  <!-- 相对于组的偏移 -->
<a:ext cx="5725" cy="1294"/>  <!-- 形状尺寸 -->
```

**EMU角度转换公式：**
```
实际角度（度）= EMU角度值 / 60000
例: 16200000 / 60000 = 270°（即从上到下的渐变方向）
```

**组合坐标转绝对坐标公式：**
```javascript
// grp = { off: {x, y}, ext: {cx, cy}, chOff: {x, y}, chExt: {cx, cy} }
function absPos(grp, shape) {
  const scaleX = grp.ext.cx / grp.chExt.cx;
  const scaleY = grp.ext.cy / grp.chExt.cy;
  return {
    x: grp.off.x + (shape.x - grp.chOff.x) * scaleX,
    y: grp.off.y + (shape.y - grp.chOff.y) * scaleY,
    cx: shape.cx * scaleX,
    cy: shape.cy * scaleY,
  };
}
```

---

### Python/Pillow 绘制复杂形状 PNG（模板）

```python
"""
复杂形状PNG生成模板
适用于：自定义多边形 + 渐变填充 + 透明背景
"""
from PIL import Image, ImageDraw
import numpy as np

# ========== 配置区 ==========
OUTPUT_PATH = "complex_shape.png"
# 画布尺寸（可按EMU比例或屏幕像素设定，建议宽度1000+）
CANVAS_W = 1200
CANVAS_H = 280

# 渐变颜色（从上到下，可扩展多个停止点）
GRADIENT_STOPS = [
    (0.0,   (255, 255, 255)),   # 白色 #FFFFFF
    (1.0,   (192,   0,   0)),   # 深红 #C00000
]

# 形状路径点（归一化坐标 0~1，按原版路径节点填写）
# 说明：从XML的 custGeom 路径坐标除以路径画布宽高即可归一化
SHAPE_POINTS_NORMALIZED = [
    (0.498, 0.0),   # 顶部尖角
    (1.0,   0.25),  # 右上
    (1.0,   1.0),   # 右下
    (0.0,   1.0),   # 左下
    (0.0,   0.25),  # 左上
]
# ========== 配置区结束 ==========

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def gradient_color(y_ratio, stops):
    """根据y比例插值渐变颜色"""
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        if p0 <= y_ratio <= p1:
            t = (y_ratio - p0) / (p1 - p0)
            return lerp_color(c0, c1, t)
    return stops[-1][1]

# 创建透明画布
img = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))

# 构建蒙版（形状区域）
mask = Image.new("L", (CANVAS_W, CANVAS_H), 0)
draw_mask = ImageDraw.Draw(mask)
pixel_points = [(int(x * CANVAS_W), int(y * CANVAS_H)) for x, y in SHAPE_POINTS_NORMALIZED]
draw_mask.polygon(pixel_points, fill=255)

# 逐行填充渐变色
pixels = img.load()
mask_pixels = mask.load()
for row in range(CANVAS_H):
    y_ratio = row / CANVAS_H
    color = gradient_color(y_ratio, GRADIENT_STOPS)
    for col in range(CANVAS_W):
        if mask_pixels[col, row] > 0:
            pixels[col, row] = (*color, mask_pixels[col, row])

img.save(OUTPUT_PATH)
print(f"已生成: {OUTPUT_PATH} ({CANVAS_W}x{CANVAS_H})")
```

**贝塞尔曲线采样（针对含 `cubicBezTo` 的复杂路径）：**

> 完整实现已打包在 `scripts/complex_shape.py`，支持命令行直接调用：
> ```bash
> python scripts/complex_shape.py \
>     --output complex_shape.png \
>     --width 1200 --height 280 \
>     --gradient-stops "0.0:#FFFFFF,1.0:#C00000" \
>     --polygon "0.498,0.0 1.0,0.25 1.0,1.0 0.0,1.0 0.0,0.25"
> ```

---

### 嵌入PPT（addImage）

```javascript
const PptxGenJS = require('pptxgenjs');

// EMU → 英寸（pptxgenjs坐标单位为英寸）
const EMU_PER_INCH = 914400;
function emuToInch(emu) { return emu / EMU_PER_INCH; }

// 嵌入生成的PNG（坐标来自absPos计算结果）
slide.addImage({
  path: './complex_shape.png',    // 或 data: base64String
  x: emuToInch(absPos.x),
  y: emuToInch(absPos.y),
  w: emuToInch(absPos.cx),
  h: emuToInch(absPos.cy),
});
```

---

### 仅有截图时的降级策略

当没有原版PPTX只有截图时：

1. **用VLM分析形状**：在分析Prompt中要求输出形状类型为 `complex_shape`，描述渐变颜色和方向
2. **坐标估算**：从像素坐标按比例转换为PPT EMU坐标（精度约±5%）
3. **颜色提取**：要求VLM输出渐变起止色的十六进制值
4. **形状近似**：若路径复杂，可用多边形近似（顶点数≥6通常足够）

更新VLM分析Prompt中的type枚举，增加：
```json
"type": "complex_shape",
"shapeDescription": "渐变方向/颜色/形状类型的文字描述，供Python绘制参考",
"gradientStops": [{"pos": 0, "color": "#FFFFFF"}, {"pos": 1, "color": "#C00000"}],
"gradientAngle": 270
```

---

## 短期优化清单（v1.1已实现）

| 优先级 | 问题 | 解决方案 |
|--------|------|----------|
| P0 | 括号全角/半角差异 | 增强Prompt要求保留原版符号 |
| P0 | bullet符号丢失或错误 | 新增 `detectBullet()` + bulletType字段 |
| P0 | 行间距不一致 | 支持 `lineSpacing` 参数映射 |
| P0 | 字符间距丢失 | 支持 `charSpacing` 参数映射 |
| P1 | JSON解析失败 | 4策略容错解析 |
| P1 | 圆角矩形显示为直角 | 新增 roundedRect 类型 |

## 快速执行命令

```javascript
const { parseAnalysisToRegions, mapAllRegions } = require('./coordinate_mapper');
const { saveFromRegions } = require('./ppt_generator');

async function main(analysisResult, imageWidth, imageHeight, outputPath) {
  // 1. 解析区域（含符号校正）
  const regions = parseAnalysisToRegions(analysisResult);
  // 2. 坐标映射
  const mapped = mapAllRegions(regions, imageWidth, imageHeight);
  // 3. 生成PPTX
  await saveFromRegions(mapped, outputPath, { imageWidth, imageHeight });
}
```

## 输出规范

生成的PPTX必须包含：
- 所有可见区域精确复刻
- 正确的叠加顺序(zIndex)
- 准确的颜色值
- 可编辑的文本内容（含正确的符号和行间距）

## 依赖

- Node.js + pptxgenjs
- 图像理解工具（开放式，默认 OpenClaw 内置 `image` 工具 / MiniMax Vision MCP）
- coordinate_mapper.js（坐标转换 + 符号校正）
- ppt_generator.js（PPT生成 + 格式支持）

---

## 方案B：基于原版PPTX的内容替换（ZIP直接操作法）

> **适用场景**：用户有原版 `.pptx` 文件，只需替换文字内容，保留所有样式、母版、配色、custGeom、媒体文件。  
> **优点**：100%保留原版视觉效果，无需重建任何形状，文件结构完整可靠。  
> **与方案A的选择原则**：有原版PPTX → 优先方案B；仅有截图 → 方案A（从零生成）。

---

### 核心思路

PPTX 本质是一个 ZIP 压缩包。直接用 Python `zipfile` 操作：
- 只替换 `ppt/slides/slide1.xml`（幻灯片内容）
- 完整保留其他所有文件（母版/布局/主题/媒体/标签等）

```
原版PPTX (89个文件)
  └── ppt/slides/slide1.xml  ← 只替换这一个文件
  └── ppt/slideMasters/      ← 保留
  └── ppt/slideLayouts/      ← 保留
  └── ppt/theme/             ← 保留
  └── ppt/media/             ← 保留（图片、SVG等）
  └── [Content_Types].xml    ← 保留
  └── ...所有其他文件         ← 保留
```

---

### ⚠️ 关键注意事项

1. **必须用完整原版PPTX为基础**，不能用手动解包再重新打包的目录（极易缺失文件）
2. **中文文本被拆散在多个 `<a:r>` 标签中**，不能直接字符串替换，需整段 `<a:p>` 替换
3. **XML中特殊字符必须转义**：`<` → `&lt;`，`>` → `&gt;`，`&` → `&amp;`
4. **替换前先用 `xmllint --noout` 或 `xml.etree.ElementTree` 验证XML有效性**

---

### 完整替换脚本模板

```python
import zipfile, re, io

src = '/path/to/original.pptx'   # 原版完整PPTX
out = '/path/to/output.pptx'      # 输出路径

# 1. 读取 slide1.xml
with zipfile.ZipFile(src, 'r') as z:
    xml = z.read('ppt/slides/slide1.xml').decode('utf-8')

# =============================================
# 2. 文本替换（两种策略，按情况选用）
# =============================================

# --- 策略A：简单单Run替换（文本完整在一个 <a:t> 标签内）---
# 格式：(旧文本含尖括号定位符, 新文本含尖括号定位符)
simple_replacements = [
    ('>旧文本1<', '>新文本1<'),
    ('>旧文本2<', '>新文本2<'),
    # ⚠️ 如果新文本含 < 或 > 必须转义：
    ('>旧文本3<', '>误差&lt;1%<'),
]
for old, new in simple_replacements:
    xml = xml.replace(old, new)

# --- 策略B：整段替换（中文被拆散在多个 <a:r> 中时使用）---
def replace_para_containing(xml_str, search_text, new_text, rPr_override=None):
    """
    找到包含 search_text 的整个 <a:p> 段落，替换为只含 new_text 的新段落。
    保留原段落的 pPr（段落格式）和 rPr（文字格式）。
    """
    idx = xml_str.find(f'>{search_text}<')
    if idx < 0:
        print(f'⚠️  未找到文本：{search_text}')
        return xml_str
    start = xml_str.rfind('<a:p>', 0, idx)
    end = xml_str.find('</a:p>', idx) + 6
    old_para = xml_str[start:end]
    # 提取段落格式
    pPr_match = re.search(r'<a:pPr.*?</a:pPr>', old_para, re.DOTALL)
    pPr = pPr_match.group() if pPr_match else ''
    # 提取文字格式（优先自闭合 rPr）
    if rPr_override:
        rPr = rPr_override
    else:
        rPr_match = re.search(r'<a:rPr(?:\s[^>]*)*/>', old_para)
        if not rPr_match:
            rPr_match = re.search(r'<a:rPr.*?</a:rPr>', old_para, re.DOTALL)
        rPr = rPr_match.group() if rPr_match else '<a:rPr/>'
    new_para = f'<a:p>{pPr}<a:r>{rPr}<a:t>{new_text}</a:t></a:r></a:p>'
    return xml_str.replace(old_para, new_para, 1)

# 调用示例
xml = replace_para_containing(xml, '原始文本片段', '替换后的完整文本')
# 如果连 search_text 的定位符也找不到，说明文本被拆散更细，
# 此时需检查XML原文，找到任意未被拆散的子串作为 search_text

# =============================================
# 3. 验证XML有效性（替换后必做）
# =============================================
import xml.etree.ElementTree as ET
try:
    ET.fromstring(xml)
    print('✅ XML验证通过')
except ET.ParseError as e:
    print(f'❌ XML解析错误：{e}')
    # 定位错误行列，检查是否有未转义的特殊字符

# =============================================
# 4. 打包输出（保留原文件所有内容）
# =============================================
buf = io.BytesIO()
with zipfile.ZipFile(src, 'r') as zin:
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == 'ppt/slides/slide1.xml':
                zout.writestr(item, xml.encode('utf-8'))
            else:
                zout.writestr(item, zin.read(item.filename))

with open(out, 'wb') as f:
    f.write(buf.getvalue())
print(f'✅ 已生成：{out}')
```

---

### 调试技巧

**查找文本在XML中的实际位置：**
```python
# 先解包查看原始XML结构
with zipfile.ZipFile(src, 'r') as z:
    xml = z.read('ppt/slides/slide1.xml').decode('utf-8')

# 搜索目标文本（注意：可能是片段，不是完整句子）
target = '要查找的文本'
idx = xml.find(target)
if idx >= 0:
    print(xml[max(0, idx-200):idx+200])  # 打印前后200字符上下文
else:
    # 中文被拆散时，尝试搜索其中一个汉字或标点
    print('未找到完整文本，尝试搜索子串')
```

**判断应该用策略A还是B：**
```
文本在XML中是连续的 <a:t>完整文本</a:t> → 用策略A（简单替换）
文本被拆散为多个 <a:r>...<a:t>片</a:t></a:r><a:r>...<a:t>段</a:t></a:r> → 用策略B（整段替换）
```

---

### 常见错误与解决

| 错误 | 原因 | 解决 |
|------|------|------|
| PowerPoint无法读取文件 | 打包基础文件不完整（缺media/theme等） | 必须用原版完整PPTX为基础，不能用手动解包目录 |
| XML解析报错（column XXXX） | 替换文本含未转义的 `<` `>` `&` | 转义为 `&lt;` `&gt;` `&amp;` |
| 替换未生效 | 中文文本被拆散在多个 `<a:r>` 中 | 改用 `replace_para_containing()` 整段替换 |
| 找不到 search_text | 数字/标点与汉字分开在不同 run | 搜索纯汉字或标点子串定位，再整段替换 |
| slideMaster.xml.rels 为空 | 解包时内容丢失（此问题仅在手动解包时出现） | 从原版PPTX直接操作，不会有此问题 |

---

## 变更日志

### v1.5.0 (2026-03-27)
- **修复 ClawHub 审查问题**：新增 `requires` metadata 声明运行时依赖（npm:pptxgenjs, python:Pillow）
- **新增完整脚本**：`scripts/complex_shape.py` 提供可直接执行的复杂形状 PNG 生成工具
- **新增使用前须知**：明确图片数据发送至外部 VLM 的隐私说明、文件系统读写说明、运行时依赖

### v1.4.0 (2026-03-26)
- **VLM 调用方式升级**：移除 `minimax-understand-image` 技能依赖，改为开放式 VLM 调用设计，默认 OpenClaw 内置 `image` 工具
- 适配 MiniMax 作为模型提供商时的内置 Vision 能力

### v1.3.0 (2026-03-26)
- **新增"方案B：基于原版PPTX的内容替换（ZIP直接操作法）"**
  - 明确方案A（从零生成）vs 方案B（原版替换）的选择原则
  - 提供完整的 Python `zipfile` 操作模板（只替换 slide1.xml，保留所有其他文件）
  - 提供两种替换策略：策略A（简单单Run替换）+ 策略B（整段 `<a:p>` 替换）
  - 提供 `replace_para_containing()` 通用函数，解决中文文本被拆散在多个 `<a:r>` 的问题
  - 提供调试技巧（XML上下文打印、策略A/B判断方法）
  - 提供常见错误排查表（文件损坏/XML解析报错/替换未生效等）
  - 总结关键注意事项：必须用完整原版PPTX、特殊字符必须转义等

### v1.2.0 (2026-03-26)
- **新增"复杂形状降级处理策略"**（核心功能升级）
  - 明确7类需要降级的形状判断标准（custGeom/透明渐变/斜向渐变/特效/裁切等）
  - 提供完整的 Python/Pillow 绘制模板（含多边形 + 逐行渐变 + 透明背景）
  - 提供贝塞尔曲线采样函数（适配 XML `cubicBezTo`）
  - 提供XML参数提取指南（路径坐标、渐变色、EMU角度转换、组合坐标变换）
  - 提供 `addImage` 嵌入代码模板
  - 补充仅有截图时的降级策略（VLM估算 + 多边形近似）
  - 区域类型映射表新增 `complex_shape` 行

### v1.1.0 (2026-03-26)
- 增强分析Prompt（短期优化P0方案）
- 增加全角/半角符号校正 `normalizeSymbols()`
- 增加bullet符号识别 `detectBullet()`
- 增加行间距 `lineSpacing` 渲染支持
- 增加字符间距 `charSpacing` 渲染支持
- 增加圆角矩形 `roundedRect` 类型支持
- 增加JSON解析4策略容错
- 改进多行文本段落渲染

### v1.0.0 (2026-03-26)
- 初始版本，基于Images2Slides论文实现基本复刻流程
