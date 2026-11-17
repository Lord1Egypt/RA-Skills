# LeaferJS 显示对象完整参考

LeaferJS 的显示对象分为容器类和图形类，所有显示对象都继承自 UI 基类。

## 容器类

### App
应用容器，管理多层结构。

**继承**: App > Leafer > Group > UI

**关键属性**:
- `tree: Leafer` - 设计层，存放主要内容
- `sky: Leafer` - 天空层，放置 UI 控件
- `editor: Editor` - 图形编辑器实例
- `mode: 'normal' | 'draw'` - 应用模式

**方法**:
- `addLeafer(config)` - 添加渲染层
- `setMode(mode)` - 设置应用模式

**示例**:
```typescript
import { App } from 'leafer-ui'

const app = new App({
    view: window,
    editor: {}  // 自动创建 tree、sky、editor
})
```

---

### Leafer
引擎渲染层，可独立运行。

**继承**: Leafer > Group > UI

**配置**:
- `view: Window | HTMLElement | string` - 渲染目标
- `width: number` - 宽度（0 表示自适应）
- `height: number` - 高度（0 表示自适应）
- `fill: string` - 背景色
- `grow: boolean` - 自动生长模式

**方法**:
- `add(child)` - 添加子元素
- `addMany(children)` - 批量添加子元素
- `remove(child)` - 移除子元素
- `find(condition)` - 查找元素
- `destroy()` - 销毁引擎

**生命周期事件**:
- `LeaferEvent.READY` - 引擎准备就绪
- `LeaferEvent.VIEW_READY` - 视图准备就绪
- `LeaferEvent.REQUEST_RENDER` - 请求渲染

**示例**:
```typescript
import { Leafer } from 'leafer-ui'

const leafer = new Leafer({
    view: window,
    fill: '#333'
})

// 自适应布局
const autoLeafer = new Leafer({
    view: window,
    fill: '#333'
})

// 固定尺寸
const fixedLeafer = new Leafer({
    view: window,
    width: 800,
    height: 600,
    fill: '#333'
})
```

---

### Group
基础容器，管理子元素。

**继承**: Group > UI

**关键属性**:
- `children: UI[]` - 子元素数组
- `numChildren: number` - 子元素数量

**方法**:
- `add(child, index?)` - 添加子元素
- `addMany(...children)` - 批量添加
- `remove(child)` - 移除子元素
- `removeAll()` - 移除所有子元素
- `getChildAt(index)` - 获取指定索引子元素
- `getChildIndex(child)` - 获取子元素索引
- `hasChild(child)` - 判断是否包含子元素

**示例**:
```typescript
import { Leafer, Group, Rect } from 'leafer-ui'

const leafer = new Leafer({ view: window })
const group = new Group()

group.add(new Rect({ width: 100, height: 100, fill: 'red' }))
group.add(new Rect({ x: 100, width: 100, height: 100, fill: 'blue' }))

leafer.add(group)
```

---

### Box
带背景的容器，支持 padding。

**继承**: Box > Group > UI

**关键属性**:
- `flow: 'x' | 'y'` - 自动布局方向（需 flow 插件）
- `gap: number` - 子元素间距
- `padding: number | number[]` - 内边距
- `stroke: string` - 边框颜色
- `fill: string | IColor` - 背景填充

**方法**:
- `scrollTo(x, y)` - 滚动到指定位置（需 scroll 插件）
- `updateLayout()` - 更新布局

**示例**:
```typescript
import { Leafer, Box, Rect } from 'leafer-ui'

const leafer = new Leafer({ view: window })

const box = new Box({
    x: 50,
    y: 50,
    padding: 20,
    fill: '#333',
    stroke: '#666',
    gap: 10
})

box.add(new Rect({ width: 50, height: 50, fill: 'red' }))
box.add(new Rect({ width: 50, height: 50, fill: 'blue' }))

leafer.add(box)
```

---

### Frame
固定尺寸的容器，支持滚动和裁剪。

**继承**: Frame > Box > Group > UI

**关键属性**:
- `width: number` - 固定宽度（必需）
- `height: number` - 固定高度（必需）
- `scrollX: number` - 水平滚动位置
- `scrollY: number` - 垂直滚动位置
- `overflow: 'hidden' | 'scroll'` - 溢出处理

**滚动属性**（需 scroll 插件）:
- `scrollable: boolean` - 是否可滚动
- `scrollbar: boolean` - 是否显示滚动条
- `scrollTo(x, y)` - 滚动到位置

**示例**:
```typescript
import { Leafer, Frame, Rect } from 'leafer-ui'

const leafer = new Leafer({ view: window })

const frame = new Frame({
    x: 50,
    y: 50,
    width: 200,
    height: 200,
    fill: '#333',
    overflow: 'hidden'
})

// 添加超出尺寸的内容
frame.add(new Rect({ x: 150, y: 150, width: 100, height: 100, fill: 'red' }))

leafer.add(frame)
```

---

## 图形元素

### Rect
矩形、圆角矩形。

**继承**: Rect > UI

**关键属性**:
- `width: number` - 宽度（必需）
- `height: number` - 高度（必需）
- `cornerRadius: number | number[]` - 圆角半径
  - `20` - 所有角相同
  - `[20, 10]` - [左上/右下, 右上/左下]
  - `[20, 10, 30]` - [左上, 右上/左下, 右下]
  - `[20, 10, 30, 40]` - [左上, 右上, 右下, 左下]

**静态方法**:
- `Rect.one(data, x?, y?, width?, height?)` - 快速创建矩形

**示例**:
```typescript
import { Leafer, Rect } from 'leafer-ui'

const leafer = new Leafer({ view: window })

// 基础矩形
const rect1 = new Rect({
    x: 100,
    y: 100,
    width: 100,
    height: 100,
    fill: '#32cd79'
})

// 圆角矩形
const rect2 = new Rect({
    x: 250,
    y: 100,
    width: 100,
    height: 100,
    cornerRadius: [20, 0, 20, 0],
    fill: '#ffcd00'
})

// 使用静态方法
const rect3 = Rect.one({ fill: 'red', cornerRadius: 50 }, 400, 100, 100, 100)

leafer.add(rect1)
leafer.add(rect2)
leafer.add(rect3)
```

---

### Ellipse
椭圆、圆形。

**继承**: Ellipse > UI

**关键属性**:
- `width: number` - 宽度（必需）
- `height: number` - 高度（必需）
- `startAngle: number` - 起始角度（弧度）
- `endAngle: number` - 结束角度（弧度）
- `innerRadius: number` - 内半径（0-1，用于圆环）

**示例**:
```typescript
import { Leafer, Ellipse } from 'leafer-ui'

const leafer = new Leafer({ view: window })

// 圆形
const circle = new Ellipse({
    x: 100,
    y: 100,
    width: 100,
    height: 100,
    fill: '#32cd79'
})

// 椭圆
const ellipse = new Ellipse({
    x: 250,
    y: 100,
    width: 150,
    height: 100,
    fill: '#ffcd00'
})

// 扇形
const sector = new Ellipse({
    x: 450,
    y: 100,
    width: 100,
    height: 100,
    startAngle: 0,
    endAngle: Math.PI,
    fill: '#ff6b6b'
})

leafer.add(circle)
leafer.add(ellipse)
leafer.add(sector)
```

---

### Line
直线、带箭头的线条。

**继承**: Line > UI

**关键属性**:
- `points: number[]` - 点坐标 [x1, y1, x2, y2, ...]
- `from: IPointData` - 起点
- `to: IPointData` - 终点
- `stroke: string` - 线条颜色
- `strokeWidth: number` - 线条宽度
- `arrow: 'none' | 'start' | 'end' | 'both'` - 箭头位置（需 arrow 插件）

**示例**:
```typescript
import { Leafer, Line } from 'leafer-ui'
import '@leafer-in/arrow'

const leafer = new Leafer({ view: window })

// 两点连线
const line1 = new Line({
    from: { x: 100, y: 100 },
    to: { x: 200, y: 200 },
    stroke: '#32cd79',
    strokeWidth: 2
})

// 多点折线
const line2 = new Line({
    points: [300, 100, 350, 150, 400, 100, 450, 150],
    stroke: '#ffcd00',
    strokeWidth: 3,
    arrow: 'end'  // 终点箭头
})

leafer.add(line1)
leafer.add(line2)
```

---

### Polygon
多边形。

**继承**: Polygon > UI

**关键属性**:
- `points: number[]` - 顶点坐标 [x1, y1, x2, y2, ...]
- `width: number` - 包围盒宽度
- `height: number` - 包围盒高度
- `fill: string` - 填充色
- `stroke: string` - 描边色

**示例**:
```typescript
import { Leafer, Polygon } from 'leafer-ui'

const leafer = new Leafer({ view: window })

// 三角形
const triangle = new Polygon({
    x: 100,
    y: 100,
    points: [0, 0, 50, 100, 100, 0],
    fill: '#32cd79'
})

// 菱形
const diamond = new Polygon({
    x: 250,
    y: 100,
    width: 100,
    height: 100,
    points: [50, 0, 100, 50, 50, 100, 0, 50],
    fill: '#ffcd00',
    stroke: '#333',
    strokeWidth: 2
})

leafer.add(triangle)
leafer.add(diamond)
```

---

### Star
星形。

**继承**: Star > UI

**关键属性**:
- `width: number` - 宽度（必需）
- `height: number` - 高度（必需）
- `points: number` - 顶点数（默认 5）
- `innerRadius: number` - 内半径比例（0-1，默认 0.5）

**示例**:
```typescript
import { Leafer, Star } from 'leafer-ui'

const leafer = new Leafer({ view: window })

// 五角星
const star1 = new Star({
    x: 100,
    y: 100,
    width: 100,
    height: 100,
    points: 5,
    innerRadius: 0.5,
    fill: '#ffcd00'
})

// 六角星
const star2 = new Star({
    x: 250,
    y: 100,
    width: 100,
    height: 100,
    points: 6,
    innerRadius: 0.6,
    fill: '#32cd79'
})

leafer.add(star1)
leafer.add(star2)
```

---

### Path
路径，支持 SVG Path 语法。

**继承**: Path > UI

**关键属性**:
- `path: string | IPathCommand[]` - 路径数据
  - 字符串格式：SVG Path 命令
  - 数组格式：命令对象数组
- `windingRule: 'nonzero' | 'evenodd'` - 填充规则

**路径命令**:
- `M x y` - 移动到
- `L x y` - 直线到
- `H x` - 水平线
- `V y` - 垂直线
- `C x1 y1 x2 y2 x y` - 三次贝塞尔曲线
- `Q x1 y1 x y` - 二次贝塞尔曲线
- `A rx ry x-axis-rotation large-arc-flag sweep-flag x y` - 圆弧
- `Z` - 闭合路径

**示例**:
```typescript
import { Leafer, Path } from 'leafer-ui'

const leafer = new Leafer({ view: window })

// SVG Path 字符串
const path1 = new Path({
    x: 100,
    y: 100,
    path: 'M 0 0 L 100 0 L 50 100 Z',
    fill: '#32cd79'
})

// 复杂路径
const path2 = new Path({
    x: 250,
    y: 100,
    path: `
        M 50 0
        C 77.6 0 100 22.4 100 50
        C 100 77.6 77.6 100 50 100
        C 22.4 100 0 77.6 0 50
        C 0 22.4 22.4 0 50 0
        M 25 50
        L 75 50
        M 50 25
        L 50 75
    `,
    fill: 'none',
    stroke: '#ffcd00',
    strokeWidth: 4
})

leafer.add(path1)
leafer.add(path2)
```

---

### Pen
画笔，程序化绘制路径。

**继承**: Pen > UI

**方法**:
- `moveTo(x, y)` - 移动画笔
- `lineTo(x, y)` - 画直线
- `bezierCurveTo(cp1x, cp1y, cp2x, cp2y, x, y)` - 三次贝塞尔曲线
- `quadraticCurveTo(cpx, cpy, x, y)` - 二次贝塞尔曲线
- `arcTo(x1, y1, x2, y2, radius)` - 圆弧
- `arc(x, y, radius, startAngle, endAngle)` - 圆弧
- `ellipse(x, y, radiusX, radiusY, rotation, startAngle, endAngle)` - 椭圆弧
- `rect(x, y, w, h)` - 矩形
- `roundRect(x, y, w, h, radii)` - 圆角矩形
- `closePath()` - 闭合路径
- `clear()` - 清除路径

**示例**:
```typescript
import { Leafer, Pen } from 'leafer-ui'

const leafer = new Leafer({ view: window })

const pen = new Pen({
    x: 100,
    y: 100,
    fill: '#32cd79',
    stroke: '#333',
    strokeWidth: 2
})

pen.moveTo(0, 0)
pen.lineTo(100, 0)
pen.lineTo(100, 50)
pen.quadraticCurveTo(50, 100, 0, 50)
pen.closePath()

leafer.add(pen)
```

---

## 媒体元素

### Image
图片。

**继承**: Image > UI

**关键属性**:
- `url: string` - 图片 URL
- `width: number` - 宽度（可选，默认原图宽度）
- `height: number` - 高度（可选，默认原图高度）
- `crop: ICrop` - 裁剪配置
  - `x, y, width, height` - 裁剪区域
- `padding: IFourNumber` - 内边距（配合 fill 使用）

**方法**:
- `load()` - 加载图片
- `resizeWidth(width)` - 按宽度缩放
- `resizeHeight(height)` - 按高度缩放

**示例**:
```typescript
import { Leafer, Image } from 'leafer-ui'

const leafer = new Leafer({ view: window })

// 基础图片
const img1 = new Image({
    x: 100,
    y: 100,
    url: 'https://example.com/image.png',
    width: 200
})

// 裁剪显示
const img2 = new Image({
    x: 350,
    y: 100,
    url: 'https://example.com/image.png',
    width: 150,
    height: 150,
    crop: { x: 50, y: 50, width: 100, height: 100 }
})

leafer.add(img1)
leafer.add(img2)
```

---

### SVG
SVG 图形。

**继承**: SVG > UI

**关键属性**:
- `url: string` - SVG URL 或 data URL
- `width: number` - 宽度（可选）
- `height: number` - 高度（可选）

**示例**:
```typescript
import { Leafer, SVG } from 'leafer-ui'

const leafer = new Leafer({ view: window })

// 加载 SVG 文件
const svg1 = new SVG({
    x: 100,
    y: 100,
    url: 'https://example.com/icon.svg',
    width: 100,
    height: 100
})

// 使用 Data URL
const svgContent = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="40" fill="#32cd79"/>
</svg>`
const dataUrl = 'data:image/svg+xml;base64,' + btoa(svgContent)

const svg2 = new SVG({
    x: 250,
    y: 100,
    url: dataUrl,
    width: 100,
    height: 100
})

leafer.add(svg1)
leafer.add(svg2)
```

---

### Canvas
Canvas 元素。

**继承**: Canvas > UI

**关键属性**:
- `width: number` - 宽度（必需）
- `height: number` - 高度（必需）
- `canvas: HTMLCanvasElement` - Canvas 元素

**方法**:
- `getContext(type)` - 获取渲染上下文
- `resize(width, height)` - 调整尺寸

**示例**:
```typescript
import { Leafer, Canvas } from 'leafer-ui'

const leafer = new Leafer({ view: window })

const canvas = new Canvas({
    x: 100,
    y: 100,
    width: 200,
    height: 150
})

// 获取 2D 上下文进行绘制
const ctx = canvas.getContext('2d')
ctx.fillStyle = '#32cd79'
ctx.fillRect(0, 0, 100, 100)

leafer.add(canvas)
```

---

## 文本元素

### Text
文本。

**继承**: Text > UI

**关键属性**:
- `text: string` - 文本内容
- `fontSize: number` - 字体大小（默认 12）
- `fontFamily: string` - 字体（默认 'Arial'）
- `fontWeight: string | number` - 字重
- `color: string` - 文本颜色
- `fill: string` - 填充（与 color 等价）
- `stroke: string` - 描边颜色
- `strokeWidth: number` - 描边宽度
- `lineHeight: number` - 行高
- `letterSpacing: number` - 字间距
- `textAlign: 'left' | 'center' | 'right'` - 水平对齐
- `verticalAlign: 'top' | 'middle' | 'bottom'` - 垂直对齐
- `width: number` - 宽度（设置后自动换行）
- `height: number` - 高度
- `padding: number | number[]` - 内边距
- `wrap: boolean` - 是否自动换行
- `ellipsis: boolean | string` - 省略号配置

**动画支持**:
- `count: number` - 数字动画目标
- `duration: number` - 动画时长

**示例**:
```typescript
import { Leafer, Text } from 'leafer-ui'

const leafer = new Leafer({ view: window })

// 基础文本
const text1 = new Text({
    x: 100,
    y: 100,
    text: 'Hello LeaferJS',
    fontSize: 24,
    fill: '#333'
})

// 样式文本
const text2 = new Text({
    x: 100,
    y: 150,
    text: 'Styled Text',
    fontSize: 32,
    fontFamily: 'Georgia',
    fontWeight: 'bold',
    fill: '#32cd79',
    stroke: '#1a8c4e',
    strokeWidth: 1
})

// 多行文本
const text3 = new Text({
    x: 100,
    y: 220,
    width: 200,
    text: 'This is a long text that will wrap automatically when it reaches the width limit.',
    fontSize: 14,
    lineHeight: 1.5,
    wrap: true,
    fill: '#666'
})

// 数字动画
const text4 = new Text({
    x: 100,
    y: 300,
    text: '0',
    count: 1000,  // 动画到 1000
    duration: 2,  // 2秒
    fontSize: 48,
    fontWeight: 'bold',
    fill: '#ff6b6b'
})

leafer.add(text1)
leafer.add(text2)
leafer.add(text3)
leafer.add(text4)
```

---

## UI 基类通用属性和方法

所有显示对象都继承自 UI 基类，共享以下属性和方法。

### 布局属性

| 属性 | 类型 | 说明 |
|------|------|------|
| x | number | X 坐标 |
| y | number | Y 坐标 |
| width | number | 宽度 |
| height | number | 高度 |
| scaleX | number | X 轴缩放 |
| scaleY | number | Y 轴缩放 |
| rotation | number | 旋转角度（度） |
| skewX | number | X 轴倾斜 |
| skewY | number | Y 轴倾斜 |
| origin | string \| IPointData | 变换原点 |
| around | string \| IPointData | 锚点对齐 |
| offsetX | number | X 偏移 |
| offsetY | number | Y 偏移 |

### 样式属性

| 属性 | 类型 | 说明 |
|------|------|------|
| fill | string \| IColor | 填充 |
| stroke | string \| IColor | 描边 |
| strokeWidth | number | 描边宽度 |
| opacity | number | 不透明度 0-1 |
| visible | boolean | 是否可见 |
| blendMode | string | 混合模式 |
| shadow | IShadow | 阴影 |
| innerShadow | IShadow | 内阴影 |
| blur | number | 模糊 |

### 交互属性

| 属性 | 类型 | 说明 |
|------|------|------|
| draggable | boolean | 可拖拽 |
| editable | boolean | 可编辑 |
| hittable | boolean | 可命中检测 |
| hitChildren | boolean | 子元素可命中 |
| cursor | string | 光标样式 |
| hoverStyle | IUIInputData | 悬停样式 |
| pressStyle | IUIInputData | 按下样式 |
| focusStyle | IUIInputData | 聚焦样式 |
| selectedStyle | IUIInputData | 选中样式 |

### 标识属性

| 属性 | 类型 | 说明 |
|------|------|------|
| id | string | 唯一标识 |
| name | string | 名称 |
| className | string | 类名 |
| tag | string | 标签名 |
| data | any | 自定义数据 |

### 常用方法

**变换**:
- `move(x, y)` - 移动（增量）
- `scaleOf(origin, x, y)` - 缩放
- `rotateOf(origin, angle)` - 旋转
- `skewOf(origin, x, y)` - 倾斜

**数据操作**:
- `set(data)` - 批量设置属性
- `get(attr)` - 获取属性
- `reset()` - 重置为初始状态
- `clone()` - 克隆元素

**层级操作**:
- `toTop()` - 移到顶层
- `toBottom()` - 移到底层
- `zIndex = n` - 设置层级

**查找**:
- `find(condition)` - 查找子元素
- `findOne(condition)` - 查找单个
- `findTag(tag)` - 按标签查找
- `pick(point)` - 点选检测

**事件**:
- `on(type, listener)` - 监听事件
- `once(type, listener)` - 监听一次
- `off(type, listener?)` - 移除监听
- `emit(event)` - 触发事件

**导出**:
- `export(type, options)` - 导出为图片
- `toJSON()` - 转为 JSON
- `toString()` - 转为字符串

**生命周期**:
- `remove()` - 从父元素移除
- `destroy()` - 销毁元素
- `forceRender()` - 强制渲染
- `forceUpdate()` - 强制更新布局

---

## 静态方法

大多数图形元素提供 `one()` 静态方法用于快速创建：

```typescript
// Rect.one(data, x, y, width, height)
const rect = Rect.one({ fill: 'red' }, 100, 100, 50, 50)

// Ellipse.one(data, x, y, width, height)
const circle = Ellipse.one({ fill: 'blue' }, 200, 200, 100, 100)

// Text.one(data, x, y)
const text = Text.one({ text: 'Hello' }, 300, 300)
```

---

## 完整示例

```typescript
import { Leafer, Rect, Ellipse, Text, Group, Box } from 'leafer-ui'

const leafer = new Leafer({
    view: window,
    fill: '#f5f5f5'
})

// 创建一个带标题的面板
const panel = new Box({
    x: 50,
    y: 50,
    width: 400,
    height: 300,
    fill: 'white',
    stroke: '#ddd',
    cornerRadius: 8,
    padding: 20,
    shadow: {
        x: 0,
        y: 4,
        blur: 12,
        color: '#00000020'
    }
})

// 标题
const title = new Text({
    text: '用户统计',
    fontSize: 20,
    fontWeight: 'bold',
    fill: '#333'
})

// 圆形头像
const avatarGroup = new Group({ y: 40 })

for (let i = 0; i < 5; i++) {
    const avatar = new Ellipse({
        x: i * 50,
        width: 40,
        height: 40,
        fill: `hsl(${i * 60}, 70%, 60%)`
    })
    avatarGroup.add(avatar)
}

// 数据展示
const dataBox = new Box({
    y: 100,
    width: 360,
    height: 120,
    fill: '#f8f9fa',
    cornerRadius: 6,
    padding: 15
})

dataBox.add(new Text({
    text: '本周新增: 1,234',
    fontSize: 16,
    fill: '#666'
}))

dataBox.add(new Text({
    y: 30,
    text: '活跃用户: 56,789',
    fontSize: 16,
    fill: '#666'
}))

dataBox.add(new Text({
    y: 60,
    text: '总用户数: 892,345',
    fontSize: 16,
    fill: '#666'
}))

// 按钮
const button = new Rect({
    x: 120,
    y: 240,
    width: 120,
    height: 40,
    fill: '#32cd79',
    cornerRadius: 20,
    draggable: true
})

button.add(new Text({
    x: 40,
    y: 12,
    text: '查看详情',
    fontSize: 14,
    fill: 'white'
}))

panel.add(title)
panel.add(avatarGroup)
panel.add(dataBox)
panel.add(button)

leafer.add(panel)
```
