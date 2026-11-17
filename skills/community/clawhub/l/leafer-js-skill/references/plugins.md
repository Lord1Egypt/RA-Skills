# LeaferJS 插件系统完整参考

LeaferJS 提供丰富的官方插件，通过 `@leafer-in/*` 命名空间安装。

## 安装方式

### NPM/Packages

```bash
# 安装全部插件（推荐）
npm install leafer

# 或单独安装 UI 包 + 所需插件
npm install leafer-ui
npm install @leafer-in/editor @leafer-in/animate
```

### Script 标签（CDN）

```html
<!-- 核心 -->
<script src="https://unpkg.com/leafer-ui@2.1.0/dist/leafer-ui.min.js"></script>

<!-- 插件 -->
<script src="https://unpkg.com/@leafer-in/editor@2.1.0/dist/editor.min.js"></script>
<script src="https://unpkg.com/@leafer-in/animate@2.1.0/dist/animate.min.js"></script>
```

---

## 动画插件 (@leafer-in/animate)

丰富的动画系统，支持 CSS 风格过渡、关键帧、路径动画。

### 安装

```bash
npm install @leafer-in/animate @leafer-in/color
```

### 导入

```typescript
import { Animate, AnimateEvent } from '@leafer-in/animate'
```

### 使用方式

**方式1：Animate 类**

```typescript
import { Animate } from '@leafer-in/animate'

const animate = new Animate(
    target,           // 动画目标元素
    keyframes,        // 关键帧或目标状态
    options           // 动画选项
)
```

**方式2：animate() 方法**

```typescript
const animate = rect.animate(
    { x: 500, rotation: 360 },
    { duration: 2, easing: 'ease-out' }
)
```

**方式3：transition 属性**

```typescript
rect.transition = { duration: 0.5 }
rect.x = 500  // 自动动画
```

**方式4：animation 属性**

```typescript
rect.animation = {
    style: { x: 500 },
    duration: 2,
    loop: true
}
```

### Animate 选项

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| duration | number | 0 | 动画时长（秒） |
| easing | string | 'ease' | 缓动函数 |
| delay | number | 0 | 延迟时间（秒） |
| speed | number | 1 | 播放速度倍率 |
| loop | boolean \| number | false | 循环播放/次数 |
| loopDelay | number | 0 | 循环间隔（秒） |
| swing | boolean \| number | false | 摇摆循环 |
| reverse | boolean | false | 反向播放 |
| autoplay | boolean | true | 自动播放 |
| join | boolean | false | 加入初始状态作为第一帧 |
| jump | boolean | false | 首帧跳转 |

### 缓动函数

- `'linear'` - 线性
- `'ease'` - 默认缓动
- `'ease-in'`, `'ease-out'`, `'ease-in-out'` - 缓入缓出
- `'quad'`, `'cubic'`, `'quart'`, `'quint'` - 多项式
- `'sine'`, `'circ'`, `'back'`, `'bounce'`, `'elastic'` - 特殊效果
- 组合：`'ease-in-out-bounce'` 等

### Animate 方法

- `play()` - 播放动画
- `pause()` - 暂停动画
- `stop()` - 停止并跳转到结束
- `seek(time)` - 跳转到指定时间
- `kill()` - 强制完成并销毁
- `destroy()` - 销毁动画

### 关键帧格式

```typescript
// 简单关键帧（从当前状态到目标状态）
{ x: 500, fill: '#ff0000' }

// 多关键帧数组
[
    { style: { x: 100 }, duration: 0.5 },
    { style: { x: 200 }, duration: 1, easing: 'bounce-out' },
    { x: 300 }  // 使用默认 duration
]
```

### 示例

```typescript
import { Leafer, Rect } from 'leafer-ui'
import { Animate } from '@leafer-in/animate'

const leafer = new Leafer({ view: window })

const rect = new Rect({
    x: 50, y: 100,
    width: 100, height: 100,
    fill: '#32cd79'
})

leafer.add(rect)

// 基础动画
new Animate(rect, { x: 500 }, { duration: 2 })

// 摇摆动画
new Animate(
    rect,
    { x: 500, rotation: 360, fill: '#ffcd00' },
    { duration: 2, swing: true, easing: 'ease-in-out' }
)

// 关键帧动画
new Animate(rect, [
    { style: { scaleX: 1.5, fill: '#ffcd00' }, duration: 0.5 },
    { style: { scaleX: 1, fill: '#32cd79' }, duration: 0.5 },
    { style: { x: 500 }, duration: 1 }
], {
    loop: true,
    join: true
})
```

---

## 图形编辑器插件 (@leafer-in/editor)

专业级图形编辑能力，支持多选、框选、变换、编组等。

### 依赖

需要同时安装 resize 插件：
```bash
npm install @leafer-in/editor @leafer-in/resize
```

### 导入

```typescript
import { Editor, EditorEvent } from '@leafer-in/editor'
```

### 在 App 中使用

**推荐方式**：配置 editor 对象自动创建

```typescript
import { App, Rect } from 'leafer-ui'
import '@leafer-in/editor'
import '@leafer-in/viewport'

const app = new App({
    view: window,
    editor: {}  // 自动创建 tree、sky、editor
})

// 添加 editable 元素
app.tree.add(Rect.one({
    editable: true,
    fill: '#32cd79'
}, 100, 100))
```

**手动创建**：

```typescript
const app = new App({ view: window })

app.tree = app.addLeafer({ type: 'design' })
app.sky = app.addLeafer()
app.sky.add(app.editor = new Editor())
```

### Editor 关键属性

| 属性 | 类型 | 说明 |
|------|------|------|
| target | UI \| UI[] | 选中的目标元素 |
| element | UI | 选中的代表元素（多选时为模拟元素） |
| list | UI[] | 选中元素列表 |
| single | boolean | 是否单选 |
| multiple | boolean | 是否多选 |
| editing | boolean | 是否处于编辑状态 |
| innerEditing | boolean | 是否内部编辑状态 |
| groupOpening | boolean | 是否处于打开组状态 |
| visible | boolean | 编辑器是否可见 |
| hittable | boolean | 是否响应交互 |

### Editor 方法

**选择操作**：
- `select(target)` - 选中元素
- `cancel()` - 取消选择
- `addItem(item)` - 添加到选择
- `removeItem(item)` - 从选择中移除
- `hasItem(item)` - 判断是否选中某元素

**编组操作**：
- `group()` - 编组
- `ungroup()` - 解组
- `openGroup()` - 打开组
- `closeGroup()` - 关闭组

**层级操作**：
- `toTop()` - 移到顶层
- `toBottom()` - 移到底层

**变换操作**（增量）：
- `move(x, y)` - 移动
- `scaleOf(origin, x, y)` - 缩放
- `rotateOf(origin, angle)` - 旋转
- `skewOf(origin, x, y)` - 倾斜
- `flip(axis)` - 翻转

**锁定**：
- `lock()` - 锁定选中元素
- `unlock()` - 解锁

### Editor 配置

```typescript
const app = new App({
    view: window,
    editor: {
        // 选择配置
        selector: true,           // 启用选择器
        select: 'press',          // 选择方式: 'press' | 'tap'
        multipleSelect: true,     // 允许多选
        boxSelect: true,          // 启用框选
        
        // 编辑能力
        moveable: true,           // 可移动
        resizeable: true,         // 可调整大小
        rotateable: true,         // 可旋转
        skewable: true,           // 可倾斜
        
        // 控制点样式
        point: {
            width: 12,
            height: 12,
            fill: '#32cd79',
            stroke: 'white',
            strokeWidth: 2
        },
        middlePoint: {
            width: 8,
            height: 8
        },
        rotatePoint: {
            width: 16,
            height: 16
        },
        
        // 其他
        stroke: '#32cd79',        // 编辑框描边色
        strokeWidth: 1,           // 编辑框描边宽
        circle: {},               // 显示旋转控制点
        
        // 按钮组
        buttonsFixed: true,       // 按钮固定方位
        buttons: { around: 'bottom', gap: 10 }
    }
})
```

### Editor 事件

- `EditorEvent.SELECT` - 选择变化
- `EditorEvent.MOVE` - 移动
- `EditorEvent.SCALE` - 缩放
- `EditorEvent.ROTATE` - 旋转
- `EditorEvent.SKEW` - 倾斜
- `EditorEvent.GROUP` - 编组/解组
- `EditorEvent.INNER` - 内部编辑器

```typescript
app.editor.on(EditorEvent.SELECT, (e) => {
    console.log('选中:', e.editor.list)
})

app.editor.on(EditorEvent.MOVE, (e) => {
    console.log('移动:', e.moveX, e.moveY)
})
```

### 事件钩子

可在配置中设置钩子函数，修改操作数据：

```typescript
const app = new App({
    view: window,
    editor: {
        beforeMove(item, moveX, moveY) {
            // 限制移动范围
            if (item.x + moveX < 0) return false
            return true
        },
        beforeScale(item, scaleX, scaleY) {
            // 限制最小尺寸
            if (item.width * scaleX < 10) return false
            return true
        }
    }
})
```

### 完整示例

```typescript
import { App, Rect, Ellipse, Box, PointerEvent } from 'leafer-ui'
import '@leafer-in/editor'
import '@leafer-in/viewport'

const app = new App({
    view: window,
    fill: '#f5f5f5',
    editor: {
        stroke: '#0066ff',
        circle: {}
    }
})

// 添加可编辑元素
const rect = Rect.one({
    editable: true,
    fill: '#32cd79',
    cornerRadius: 8
}, 100, 100, 150, 100)

const circle = Ellipse.one({
    editable: true,
    fill: '#ffcd00'
}, 350, 150, 100, 100)

app.tree.add(rect)
app.tree.add(circle)

// 监听选择事件
app.editor.on(EditorEvent.SELECT, (e) => {
    console.log('选中元素:', e.editor.list.length)
})

// 添加自定义按钮
const deleteBtn = Box.one({
    around: 'center',
    fill: '#ff6b6b',
    cornerRadius: 4,
    cursor: 'pointer',
    children: [{
        tag: 'Text',
        text: '删除',
        fill: 'white',
        padding: [4, 8]
    }]
})

app.editor.buttons.add(deleteBtn)

deleteBtn.on(PointerEvent.TAP, () => {
    app.editor.list.forEach(item => item.remove())
    app.editor.target = null
})
```

---

## 视口控制插件 (@leafer-in/viewport)

控制视图的缩放和平移。

### 安装

```bash
npm install @leafer-in/viewport
```

### 导入

```typescript
import '@leafer-in/viewport'
```

### 配置

```typescript
const app = new App({
    view: window,
    // 视口配置
    move: {                        // 平移配置
        holdSpaceKey: true,        // 按住空格键拖拽
        holdMiddleKey: true,       // 按住中键拖拽
        drag: true                 // 拖拽画布
    },
    zoom: {                        // 缩放配置
        min: 0.1,                  // 最小缩放
        max: 10,                   // 最大缩放
        disabled: false            // 禁用缩放
    },
    wheel: {                       // 滚轮配置
        zoom: true,                // 滚轮缩放
        zoomSpeed: 0.01,           // 缩放速度
        move: true,                // 滚轮平移
        moveSpeed: 1               // 平移速度
    }
})
```

### View 插件 (@leafer-in/view)

更高级的视图控制。

```typescript
import '@leafer-in/view'

// 可用方法（通过 app.tree.zoom 访问）
app.tree.zoom.zoomIn()           // 放大
app.tree.zoom.zoomOut()          // 缩小
app.tree.zoom.fit()              // 适应屏幕
app.tree.zoom.fitWidth()         // 适应宽度
app.tree.zoom.fitHeight()        // 适应高度
app.tree.zoom.focus(target)      // 聚焦元素
```

---

## 滚动条插件 (@leafer-in/scroll)

为 Frame 容器添加滚动条。

### 安装

```bash
npm install @leafer-in/scroll
```

### 导入

```typescript
import '@leafer-in/scroll'
```

### 使用

```typescript
import { Leafer, Frame, Rect } from 'leafer-ui'
import '@leafer-in/scroll'

const leafer = new Leafer({ view: window })

const frame = new Frame({
    x: 50,
    y: 50,
    width: 300,
    height: 200,
    fill: '#f5f5f5',
    overflow: 'scroll',         // 启用滚动
    scrollbar: true,            // 显示滚动条
    scrollable: true            // 可滚动
})

// 添加超出尺寸的内容
frame.add(new Rect({ y: 0, width: 280, height: 100, fill: 'red' }))
frame.add(new Rect({ y: 150, width: 280, height: 100, fill: 'blue' }))
frame.add(new Rect({ y: 300, width: 280, height: 100, fill: 'green' }))

leafer.add(frame)

// 滚动控制
frame.scrollTo(0, 100)          // 滚动到位置
frame.scrollX = 50              // 设置水平滚动位置
frame.scrollY = 100             // 设置垂直滚动位置
```

### 滚动条样式

```typescript
const frame = new Frame({
    scrollbar: {
        color: '#999',          // 滚动条颜色
        hoverColor: '#666',     // 悬停颜色
        width: 8,               // 滚动条宽度
        padding: 2              // 内边距
    }
})
```

---

## 箭头插件 (@leafer-in/arrow)

为线条添加箭头。

### 安装

```bash
npm install @leafer-in/arrow
```

### 导入

```typescript
import '@leafer-in/arrow'
```

### 使用

```typescript
import { Leafer, Line } from 'leafer-ui'
import '@leafer-in/arrow'

const leafer = new Leafer({ view: window })

// 基础箭头
const line1 = new Line({
    from: { x: 100, y: 100 },
    to: { x: 300, y: 100 },
    stroke: '#333',
    strokeWidth: 2,
    arrow: 'end'               // 终点箭头
})

// 双向箭头
const line2 = new Line({
    points: [100, 200, 300, 200],
    stroke: '#333',
    strokeWidth: 2,
    arrow: 'both'              // 两端都有箭头
})

// 自定义箭头样式
const line3 = new Line({
    from: { x: 100, y: 300 },
    to: { x: 300, y: 300 },
    stroke: '#333',
    strokeWidth: 3,
    arrow: 'end',
    arrowStyle: {
        size: 15,               // 箭头大小
        angle: 30,            // 箭头角度
        fill: '#ff6b6b'       // 箭头填充色
    }
})

leafer.add(line1)
leafer.add(line2)
leafer.add(line3)
```

### 箭头位置

- `'none'` - 无箭头
- `'start'` - 起点
- `'end'` - 终点（默认）
- `'both'` - 两端

---

## HTML 插件 (@leafer-in/html)

在 Leafer 中渲染 HTML 内容。

### 安装

```bash
npm install @leafer-in/html
```

### 导入

```typescript
import '@leafer-in/html'
```

### 使用

```typescript
import { Leafer, HTML } from 'leafer-ui'
import '@leafer-in/html'

const leafer = new Leafer({ view: window })

// 基础 HTML
const html = new HTML({
    x: 100,
    y: 100,
    width: 300,
    height: 200,
    html: '<div style="padding: 20px; background: #f5f5f5;">
        <h2>HTML 内容</h2>
        <p>支持完整的 HTML 和 CSS</p>
        <button style="padding: 8px 16px;">按钮</button>
    </div>'
})

leafer.add(html)
```

---

## 状态插件 (@leafer-in/state)

交互状态样式系统。

### 安装

```bash
npm install @leafer-in/state
```

### 导入

```typescript
import '@leafer-in/state'
```

### 使用

```typescript
import { Leafer, Rect } from 'leafer-ui'
import '@leafer-in/state'

const leafer = new Leafer({ view: window })

const rect = new Rect({
    x: 100,
    y: 100,
    width: 150,
    height: 100,
    fill: '#32cd79',
    cornerRadius: 8,
    
    // 状态样式
    hoverStyle: {               // 悬停状态
        fill: '#ffcd00',
        scale: 1.05
    },
    pressStyle: {               // 按下状态
        fill: '#ff6b6b',
        scale: 0.95
    },
    focusStyle: {               // 聚焦状态
        stroke: '#0066ff',
        strokeWidth: 2
    },
    selectedStyle: {            // 选中状态
        stroke: '#32cd79',
        strokeWidth: 2,
        shadow: {
            x: 0, y: 4, blur: 8, color: '#00000040'
        }
    },
    disabledStyle: {            // 禁用状态
        opacity: 0.5
    }
})

leafer.add(rect)
```

### 状态类型

| 状态 | 触发条件 |
|------|----------|
| hover | 鼠标悬停 |
| press | 按下 |
| focus | 获得焦点 |
| selected | 被选中（配合编辑器） |
| disabled | 禁用状态 |

---

## 自动布局插件 (@leafer-in/flow)

类似 Flex 的自动布局系统。

### 安装

```bash
npm install @leafer-in/flow
```

### 导入

```typescript
import '@leafer-in/flow'
```

### Box 容器配置

```typescript
import { Leafer, Box, Rect } from 'leafer-ui'
import '@leafer-in/flow'

const leafer = new Leafer({ view: window })

const container = new Box({
    x: 50,
    y: 50,
    padding: 20,
    fill: '#f5f5f5',
    cornerRadius: 8,
    
    // Flow 布局配置
    flow: 'x',                  // 排列方向: 'x' | 'y'
    gap: 10,                    // 子元素间距
    wrap: true,                 // 是否换行
    align: 'center',            // 对齐: 'start' | 'center' | 'end' | 'stretch'
    justify: 'center',          // 主轴对齐
    itemAlign: 'center'         // 交叉轴对齐
})

// 子元素自动排列
container.add(new Rect({ width: 80, height: 60, fill: 'red' }))
container.add(new Rect({ width: 80, height: 60, fill: 'blue' }))
container.add(new Rect({ width: 80, height: 60, fill: 'green' }))

leafer.add(container)
```

### Flow 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| flow | 'x' \| 'y' | 排列方向 |
| gap | number | 间距 |
| wrap | boolean | 是否换行 |
| align | string | 主轴对齐方式 |
| justify | string | 交叉轴对齐方式 |
| itemAlign | string | 子元素对齐 |

---

## 文本编辑插件 (@leafer-in/text-editor)

双击文本进入编辑状态。

### 安装

```bash
npm install @leafer-in/text-editor
```

### 导入

```typescript
import '@leafer-in/text-editor'
```

### 使用

```typescript
import { App, Text } from 'leafer-ui'
import '@leafer-in/editor'
import '@leafer-in/text-editor'

const app = new App({
    view: window,
    editor: {}
})

const text = new Text({
    x: 100,
    y: 100,
    text: '双击编辑文本',
    fontSize: 24,
    fill: '#333',
    editable: true            // 可编辑
})

app.tree.add(text)
// 双击文本即可进入编辑模式
```

---

## 游戏插件 (@leafer-in/robot)

游戏精灵元素，集成帧动画和动作预设。

### 安装

```bash
npm install @leafer-in/robot
```

### 导入

```typescript
import { Robot } from '@leafer-in/robot'
```

### 使用

```typescript
import { Leafer } from 'leafer-ui'
import { Robot } from '@leafer-in/robot'

const leafer = new Leafer({ view: window })

const robot = new Robot({
    x: 100,
    y: 100,
    width: 64,
    height: 64,
    
    // 帧动画配置
    animation: {
        image: 'sprite-sheet.png',
        frames: [[0, 0], [64, 0], [128, 0], [192, 0]],  // 帧坐标
        duration: 0.5,           // 动画时长
        loop: true
    },
    
    // 动作预设
    states: {
        idle: {
            frames: [[0, 0], [64, 0]],
            duration: 1
        },
        walk: {
            frames: [[128, 0], [192, 0], [256, 0], [320, 0]],
            duration: 0.5
        },
        attack: {
            frames: [[384, 0], [448, 0]],
            duration: 0.3
        }
    }
})

leafer.add(robot)

// 切换状态
robot.play('walk')
```

---

## 查找插件 (@leafer-in/find)

高级查找功能。

### 安装

```bash
npm install @leafer-in/find
```

### 导入

```typescript
import '@leafer-in/find'
```

### 使用

```typescript
// 基础查找已在核心中提供，此插件增强功能
const results = leafer.find('.class-name')     // 按类名查找
const results = leafer.find('#id')             // 按 id 查找
const results = leafer.find('[draggable]')   // 按属性查找
```

---

## 滤镜插件 (@leafer-in/filter)

Canvas 滤镜效果。

### 安装

```bash
npm install @leafer-in/filter
```

### 导入

```typescript
import '@leafer-in/filter'
```

### 使用

```typescript
import { Leafer, Rect } from 'leafer-ui'
import '@leafer-in/filter'

const leafer = new Leafer({ view: window })

const rect = new Rect({
    x: 100,
    y: 100,
    width: 200,
    height: 150,
    fill: '#32cd79',
    
    // 滤镜
    filter: 'blur(5px) brightness(1.2)'
})

leafer.add(rect)
```

### 可用滤镜

- `blur(n)` - 模糊
- `brightness(n)` - 亮度
- `contrast(n)` - 对比度
- `grayscale(n)` - 灰度
- `hue-rotate(n)` - 色相旋转
- `invert(n)` - 反色
- `opacity(n)` - 不透明度
- `saturate(n)` - 饱和度
- `sepia(n)` - 复古

---

## 导出插件 (@leafer-in/export)

导出为图片、SVG。

### 安装

```bash
npm install @leafer-in/export
```

### 导入

```typescript
import '@leafer-in/export'
```

### 使用

```typescript
// 导出整个画布
const blob = await app.tree.export('png', {
    pixelRatio: 2,            // 分辨率倍率
    quality: 0.9,             // 图片质量
    backgroundColor: 'white'    // 背景色
})

// 导出指定元素
const blob = await rect.export('png', { pixelRatio: 2 })

// 导出为 SVG
const svgString = await rect.export('svg')

// 下载
const link = document.createElement('a')
link.href = URL.createObjectURL(blob)
link.download = 'export.png'
link.click()
```

### 导出选项

| 属性 | 类型 | 说明 |
|------|------|------|
| pixelRatio | number | 分辨率倍率（默认1） |
| quality | number | 图片质量 0-1 |
| backgroundColor | string | 背景色 |
| trim | boolean | 裁剪空白 |
| bounds | IBounds | 指定导出区域 |

---

## 路径动画插件 (@leafer-in/motion-path)

沿路径运动的动画。

### 安装

```bash
npm install @leafer-in/motion-path
```

### 导入

```typescript
import '@leafer-in/motion-path'
```

### 使用

```typescript
import { Leafer, Rect, Path } from 'leafer-ui'
import '@leafer-in/motion-path'

const leafer = new Leafer({ view: window })

const path = new Path({
    path: 'M 100 300 Q 300 100 500 300 T 700 300',
    stroke: '#ddd',
    strokeWidth: 2
})

const rect = new Rect({
    width: 30,
    height: 30,
    fill: '#ff6b6b',
    motion: path,               // 沿路径运动
    motionPath: true           // 自动旋转以跟随路径
})

// 添加动画
rect.animate(
    { motion: 1 },             // 运动到路径终点
    { duration: 3, loop: true }
)

leafer.add(path)
leafer.add(rect)
```

---

## 其他插件

### 颜色处理 (@leafer-in/color)

颜色处理工具，动画插件的依赖。

### 调整大小 (@leafer-in/resize)

调整大小能力，编辑器插件的依赖。

### 固定缩放 (@leafer-in/scale-fixed)

元素保持固定大小，不随视图缩放。

```typescript
import '@leafer-in/scale-fixed'

const rect = new Rect({
    width: 100,
    height: 100,
    fill: 'red',
    scaleFixed: true          // 固定大小
})
```

### 圆角 (@leafer-in/corner)

增强的圆角控制能力。

### 亮度 (@leafer-in/bright)

元素亮度控制。

---

## 插件完整示例

```typescript
import { App, Rect, Ellipse, Text, Box, PointerEvent } from 'leafer-ui'
import '@leafer-in/editor'
import '@leafer-in/viewport'
import '@leafer-in/scroll'
import '@leafer-in/state'
import '@leafer-in/flow'
import '@leafer-in/animate'
import '@leafer-in/export'

const app = new App({
    view: window,
    fill: '#f5f5f5',
    editor: {},
    wheel: { zoom: true },
    move: { holdSpaceKey: true }
})

// 使用 Flow 自动布局
const container = new Box({
    x: 50, y: 50,
    padding: 20,
    fill: 'white',
    cornerRadius: 12,
    shadow: { x: 0, y: 4, blur: 12, color: '#00000010' },
    
    flow: 'y',
    gap: 10
})

// 添加可编辑卡片
const card = new Box({
    width: 300,
    padding: 15,
    fill: '#f8f9fa',
    cornerRadius: 8,
    editable: true,
    
    hoverStyle: { fill: '#e9ecef' },
    pressStyle: { scale: 0.98 }
})

const title = new Text({
    text: '可编辑卡片',
    fontSize: 18,
    fontWeight: 'bold',
    fill: '#333'
})

const desc = new Text({
    y: 30,
    text: '点击选中，拖拽移动，双击进组',
    fontSize: 14,
    fill: '#666'
})

card.add(title)
card.add(desc)

// 添加动画
new Animate(card, 
    { y: 10 },
    { duration: 0.3, easing: 'ease-out' }
)

container.add(card)
app.tree.add(container)

// 导出按钮
const exportBtn = new Box({
    x: 400, y: 50,
    padding: [10, 20],
    fill: '#32cd79',
    cornerRadius: 20,
    cursor: 'pointer',
    
    hoverStyle: { fill: '#2ab366' }
})

exportBtn.add(new Text({
    text: '导出图片',
    fill: 'white',
    fontSize: 14
}))

exportBtn.on(PointerEvent.TAP, async () => {
    const blob = await app.tree.export('png', { pixelRatio: 2 })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = 'design.png'
    link.click()
})

app.tree.add(exportBtn)
```
