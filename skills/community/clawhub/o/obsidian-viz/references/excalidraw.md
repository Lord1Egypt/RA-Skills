# Excalidraw 格式规范

Excalidraw 是一个手绘风格的白板工具，支持自由布局和丰富的图形元素。

## 三种输出模式

| 模式 | 扩展名 | 触发词 | 打开方式 |
|------|--------|--------|---------|
| Obsidian（默认）| `.md` | Excalidraw、画图、流程图 | Obsidian Excalidraw 插件 |
| 标准 | `.excalidraw` | 标准Excalidraw、standard | excalidraw.com |
| 动画 | `.excalidraw` | 动画图、animate | excalidraw-animate |

## Obsidian 模式文件结构

**必须严格遵守以下格式**：

```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw]
---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠==


%%
# Drawing
```json
{ EXCALIDRAW_JSON }
```
%%
```

**关键约束**：
- 警告行与 `%%` 之间必须有**两个空行**
- JSON 代码块使用 ` ```json ` 语言标签
- `%%` 分隔符必须各占独立一行
- YAML frontmatter 必须包含 `excalidraw-plugin: parsed`

## 标准模式文件结构

纯 JSON 文件，无 Markdown 包装：

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [ ...元素数组... ],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

## 元素 JSON Schema

### 所有元素通用字段

```json
{
  "id": "unique-id-string",
  "type": "rectangle | ellipse | diamond | arrow | text | line",
  "x": 0,
  "y": 0,
  "width": 200,
  "height": 80,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#ffffff",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": null,
  "seed": 1234567890,
  "version": 1,
  "versionNonce": 1234567890,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1234567890000,
  "link": null,
  "locked": false
}
```

**字段说明**：
- `id`：全局唯一标识符（字符串）
- `type`：元素类型
- `x`, `y`：左上角坐标
- `width`, `height`：宽度和高度
- `angle`：旋转角度（弧度）
- `strokeColor`：边框颜色（十六进制）
- `backgroundColor`：填充颜色（十六进制）
- `fillStyle`：填充样式（`solid` / `hachure` / `cross-hatch`）
- `strokeWidth`：边框宽度（1-4）
- `strokeStyle`：边框样式（`solid` / `dashed` / `dotted`）
- `roughness`：手绘粗糙度（**固定为 1**）
- `opacity`：不透明度（0-100）
- `seed`：随机种子（用于手绘效果）
- `boundElements`：绑定的元素（箭头或文字）

### 文本元素额外字段

```json
{
  "type": "text",
  "text": "文本内容",
  "fontSize": 20,
  "fontFamily": 5,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": null,
  "originalText": "文本内容",
  "autoResize": true,
  "lineHeight": 1.25
}
```

**字段说明**：
- `text`：显示的文本内容
- `fontSize`：字体大小（16-24 常用）
- `fontFamily`：**固定为 5（Excalifont，手绘字体）**
- `textAlign`：水平对齐（`left` / `center` / `right`）
- `verticalAlign`：垂直对齐（`top` / `middle` / `bottom`）
- `containerId`：如果文字嵌入形状，填写形状的 `id`
- `originalText`：原始文本（必须与 `text` 相同）
- `autoResize`：**必须为 true**

### 形状+嵌入文字的双元素模式

**形状元素**：
```json
{
  "id": "shape-1",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 80,
  "boundElements": [
    {
      "type": "text",
      "id": "text-1"
    }
  ],
  ...
}
```

**文字元素**：
```json
{
  "id": "text-1",
  "type": "text",
  "text": "节点标签",
  "x": 150,
  "y": 130,
  "width": 100,
  "height": 20,
  "containerId": "shape-1",
  "textAlign": "center",
  "verticalAlign": "middle",
  ...
}
```

**关键点**：
- 形状的 `boundElements` 包含文字的 `id`
- 文字的 `containerId` 指向形状的 `id`
- 文字位置在形状内部居中

### 箭头元素额外字段

```json
{
  "type": "arrow",
  "x": 300,
  "y": 140,
  "width": 200,
  "height": 0,
  "points": [
    [0, 0],
    [200, 0]
  ],
  "startBinding": {
    "elementId": "shape-1",
    "focus": 0,
    "gap": 8
  },
  "endBinding": {
    "elementId": "shape-2",
    "focus": 0,
    "gap": 8
  },
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "elbowed": false
}
```

**字段说明**：
- `points`：相对坐标数组（第一个点为 `[0, 0]`）
- `startBinding`：起点绑定的元素
- `endBinding`：终点绑定的元素
- `elementId`：绑定元素的 `id`
- `focus`：绑定位置偏移（通常为 0）
- `gap`：与元素边缘的间距（通常为 8）
- `startArrowhead`：起点箭头类型（`null` / `arrow` / `dot`）
- `endArrowhead`：终点箭头类型（`null` / `arrow` / `dot`）

## 箭头坐标计算公式

### 水平箭头（从左到右）

```
source 右中点:  x = src.x + src.width + 8,  y = src.y + src.height/2
target 左中点:  x = tgt.x - 8,              y = tgt.y + tgt.height/2

arrow 原点:     同 source 右中点
arrow points:   [[0, 0], [width_diff, y_diff]]

width_diff = (tgt.x - 8) - (src.x + src.width + 8)
y_diff     = (tgt.y + tgt.height/2) - (src.y + src.height/2)
```

### 垂直箭头（从上到下）

```
source 下中点:  x = src.x + src.width/2,  y = src.y + src.height + 8
target 上中点:  x = tgt.x + tgt.width/2,  y = tgt.y - 8

arrow 原点:     同 source 下中点
arrow points:   [[0, 0], [x_diff, height_diff]]

x_diff      = (tgt.x + tgt.width/2) - (src.x + src.width/2)
height_diff = (tgt.y - 8) - (src.y + src.height + 8)
```

### 示例计算

假设：
- 源节点：`x=100, y=100, width=200, height=80`
- 目标节点：`x=400, y=100, width=200, height=80`

计算：
```
source 右中点: x = 100 + 200 + 8 = 308, y = 100 + 40 = 140
target 左中点: x = 400 - 8 = 392, y = 100 + 40 = 140

arrow 原点: x = 308, y = 140
arrow points: [[0, 0], [84, 0]]
  width_diff = 392 - 308 = 84
  y_diff = 140 - 140 = 0
```

箭头元素：
```json
{
  "type": "arrow",
  "x": 308,
  "y": 140,
  "width": 84,
  "height": 0,
  "points": [[0, 0], [84, 0]],
  "startBinding": {"elementId": "src-id", "focus": 0, "gap": 8},
  "endBinding": {"elementId": "tgt-id", "focus": 0, "gap": 8},
  "endArrowhead": "arrow"
}
```

## 样式常量

### 字体

```json
{
  "fontFamily": 5,        // Excalifont（手绘字体，必须固定）
  "fontSize": 20,         // 16（小字）/ 20（正文）/ 24（标题）
  "autoResize": true      // 必须为 true
}
```

### 手绘效果

```json
{
  "roughness": 1,         // 手绘粗糙度（固定为 1）
  "strokeWidth": 2,       // 边框宽度（1-4）
  "fillStyle": "solid"    // 填充样式（solid / hachure / cross-hatch）
}
```

### 配色方案

| 颜色名 | strokeColor | backgroundColor | 推荐用途 |
|--------|-------------|-----------------|---------|
| white | `#1e1e1e` | `#ffffff` | 默认节点 |
| blue | `#1971c2` | `#d0ebff` | 流程 / 动作 |
| green | `#2f9e44` | `#d3f9d8` | 开始 / 结束 / 成功 |
| yellow | `#e67700` | `#fff9db` | 判断 / 注意 |
| red | `#c92a2a` | `#ffe3e3` | 错误 / 警告 |
| purple | `#862e9c` | `#f8f0fc` | 外部 / 特殊 |
| gray | `#495057` | `#f1f3f5` | 子流程 / 次要 |

## 八种图表子类型布局算法

### 1. Flowchart（流程图）

**布局规则**：
- 顶部 ellipse 起始节点
- 每步向下 140px
- decision 用 diamond
- 分支向左右偏移 ±120px

**示例布局**：
```
开始 (ellipse, y=0)
  ↓ (140px)
步骤1 (rectangle, y=140)
  ↓
判断 (diamond, y=280)
  ├→ 是 (rectangle, x+120, y=420)
  └→ 否 (rectangle, x-120, y=420)
  ↓
结束 (ellipse, y=560)
```

### 2. Mindmap（思维导图）

**布局规则**：
- 中心 ellipse
- L1 节点按角度均匀分布在半径 280px 圆上
- L2 节点在半径 500px 圆上
- 每个分支使用不同颜色

**角度计算**：
```
angle_i = i × (360 / N) - 90  // N 为 L1 节点数量
x = center_x + 280 × cos(angle_i) - width/2
y = center_y + 280 × sin(angle_i) - height/2
```

### 3. Hierarchy（层级图）

**布局规则**：
- 根节点居中顶部
- 每层 y+160
- 子节点水平均分
- 使用垂直箭头连接

**示例布局**：
```
        根节点 (y=0, x=center)
       /   |   \
      /    |    \
   L1-1  L1-2  L1-3 (y=160, 水平均分)
   / \    |    / \
L2-1 L2-2 L2-3 L2-4 L2-5 (y=320, 在父节点下方均分)
```

### 4. Timeline（时间线）

**布局规则**：
- 水平轴线 y=300
- 事件节点交替上下排列
- 小圆点标记轴上位置
- 垂直虚线连接事件到轴

**示例布局**：
```
事件1 (y=150)
  |
  • (y=300, 轴上)
  |
事件2 (y=450)
  |
  • (y=300, 轴上)
```

### 5. Comparison（对比图）

**布局规则**：
- 竖向分割线 x=center
- 左右各一列
- 行高 80px
- 顶部标题行

**示例布局**：
```
方案 A (x=center-150)  |  方案 B (x=center+150)
------------------------+------------------------
特点1                  |  特点1
特点2                  |  特点2
特点3                  |  特点3
```

### 6. Matrix（矩阵图）

**布局规则**：
- 2×2 四象限
- 十字分割线
- 轴标签在边缘
- 每个象限内容居中

**示例布局**：
```
        高优先级
           |
  象限2    |    象限1
           |
-----------+-----------
           |
  象限3    |    象限4
           |
        低优先级
```

### 7. Relationship（关系图）

**布局规则**：
- 同心环布局
- 每环 4-6 个节点
- 箭头可双向
- 中心节点最大

**示例布局**：
```
        L2-1
       /    \
    L1-1 -- 中心 -- L1-2
       \    /
        L2-2
```

### 8. Free-layout（自由布局）

**布局规则**：
- 按色块分组
- 组内间距 60px
- 组间间距 150px
- 无固定模式

## 中文文本规则

### 字符宽度估算

- Excalifont (fontFamily:5) 原生支持中文
- 每个中文字符宽度 ≈ fontSize px
- 容器宽度 = 字符数 × fontSize + 20% 内边距

**示例**：
```
文字："用户登录流程"（6 个字符）
fontSize: 20
估算宽度: 6 × 20 × 1.2 = 144px
实际设置: width = 150
```

### JSON 编码规则

- **禁止**对中文进行 Unicode 转义（`\u` 形式）
- `originalText` 字段必须与 `text` 字段完全相同
- 文件编码必须为 UTF-8

**错误示例**：
```json
{
  "text": "\u7528\u6237\u767b\u5f55",  // ❌ 不要这样
  "originalText": "用户登录"
}
```

**正确示例**：
```json
{
  "text": "用户登录",  // ✅ 直接使用中文
  "originalText": "用户登录"
}
```

## 动画模式元素排序

动画模式下，`elements` 数组的顺序决定元素出现顺序：

**推荐顺序**：
1. 标题文字
2. 背景形状（如果有）
3. 节点（从左到右 / 从上到下）
4. 节点标签文字（紧跟对应节点）
5. 箭头（按流程顺序）

**示例**：
```json
{
  "elements": [
    { "id": "title", "type": "text", "text": "流程图标题" },
    { "id": "node1", "type": "rectangle" },
    { "id": "text1", "type": "text", "containerId": "node1" },
    { "id": "node2", "type": "rectangle" },
    { "id": "text2", "type": "text", "containerId": "node2" },
    { "id": "arrow1", "type": "arrow", "startBinding": {"elementId": "node1"}, "endBinding": {"elementId": "node2"} }
  ]
}
```

## 常见错误清单

| 错误 | 修复方法 |
|------|---------|
| 文字溢出形状 | 增加形状宽度；确保 `autoResize: true` |
| 箭头未连接到节点 | 检查 `elementId` 与实际节点 `id` 一致 |
| 箭头 `points` 方向错误 | `points` 是相对坐标，重新计算 |
| 重复 ID | 每个元素必须有全局唯一 `id` |
| `fontFamily` 错误 | 必须为 `5`，不得为 `1` 或 `3` |
| 中文乱码 | 确保文件 UTF-8 编码；JSON 中不转义 Unicode |
| Obsidian 不识别为 Excalidraw | 检查 YAML frontmatter 是否存在且格式正确 |
| `%%` 分隔符缺失 | 开头和结尾的 `%%` 必须各占独立一行 |
| 警告行与 `%%` 之间无空行 | 必须有两个空行 |
| `boundElements` 与 `containerId` 不匹配 | 形状的 `boundElements` 必须包含文字 ID，文字的 `containerId` 必须指向形状 ID |

## 完整示例：简单流程图

### Obsidian 模式

```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw]
---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠==


%%
# Drawing
```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    {
      "id": "start",
      "type": "ellipse",
      "x": 100,
      "y": 50,
      "width": 120,
      "height": 60,
      "strokeColor": "#2f9e44",
      "backgroundColor": "#d3f9d8",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "seed": 123456,
      "version": 1,
      "versionNonce": 123456,
      "isDeleted": false,
      "boundElements": [{"type": "text", "id": "start-text"}]
    },
    {
      "id": "start-text",
      "type": "text",
      "x": 130,
      "y": 70,
      "width": 60,
      "height": 20,
      "text": "开始",
      "fontSize": 20,
      "fontFamily": 5,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": "start",
      "originalText": "开始",
      "autoResize": true,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "seed": 123457,
      "version": 1,
      "versionNonce": 123457,
      "isDeleted": false
    },
    {
      "id": "arrow1",
      "type": "arrow",
      "x": 160,
      "y": 118,
      "width": 0,
      "height": 72,
      "points": [[0, 0], [0, 72]],
      "strokeColor": "#1e1e1e",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "seed": 123458,
      "version": 1,
      "versionNonce": 123458,
      "isDeleted": false,
      "startBinding": {"elementId": "start", "focus": 0, "gap": 8},
      "endBinding": {"elementId": "process", "focus": 0, "gap": 8},
      "startArrowhead": null,
      "endArrowhead": "arrow"
    },
    {
      "id": "process",
      "type": "rectangle",
      "x": 80,
      "y": 190,
      "width": 160,
      "height": 80,
      "strokeColor": "#1971c2",
      "backgroundColor": "#d0ebff",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "seed": 123459,
      "version": 1,
      "versionNonce": 123459,
      "isDeleted": false,
      "boundElements": [{"type": "text", "id": "process-text"}]
    },
    {
      "id": "process-text",
      "type": "text",
      "x": 120,
      "y": 220,
      "width": 80,
      "height": 20,
      "text": "处理数据",
      "fontSize": 20,
      "fontFamily": 5,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": "process",
      "originalText": "处理数据",
      "autoResize": true,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "seed": 123460,
      "version": 1,
      "versionNonce": 123460,
      "isDeleted": false
    }
  ],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```
%%
```

## 生成前必检清单

- [ ] 所有元素有全局唯一 `id`
- [ ] `fontFamily` 为 `5`（Excalifont）
- [ ] `roughness` 为 `1`
- [ ] 文本元素 `autoResize` 为 `true`
- [ ] 文本元素 `originalText` 与 `text` 相同
- [ ] 形状+文字：`boundElements` 与 `containerId` 正确绑定
- [ ] 箭头：`startBinding` 和 `endBinding` 的 `elementId` 存在
- [ ] 箭头：`points` 为相对坐标，第一个点为 `[0, 0]`
- [ ] 中文无 Unicode 转义（`\u` 形式）
- [ ] Obsidian 模式：YAML frontmatter 正确
- [ ] Obsidian 模式：警告行与 `%%` 之间有两个空行
- [ ] Obsidian 模式：`%%` 分隔符各占独立一行
- [ ] JSON 无尾随逗号
- [ ] 文件编码为 UTF-8
