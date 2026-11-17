# LeaferJS 样式系统完整参考

LeaferJS 提供接近专业设计工具的丰富视觉效果。

---

## 填充 (fill)

### 纯色填充

```typescript
rect.fill = '#32cd79'
rect.fill = 'rgb(50, 205, 121)'
rect.fill = 'rgba(50, 205, 121, 0.5)'
rect.fill = '#32cd79ff'
rect.fill = 'hsl(150, 70%, 60%)'
rect.fill = 'hwb(150 20% 20%)'
```

### 渐变填充

#### 线性渐变

```typescript
rect.fill = {
    type: 'linear',
    from: 'top',      // 起点位置: 'top', 'bottom', 'left', 'right' 或百分比/像素
    to: 'bottom',     // 终点位置
    stops: [
        { offset: 0, color: '#32cd79' },
        { offset: 0.5, color: '#ffcd00' },
        { offset: 1, color: '#ff6b6b' }
    ]
}

// 或使用角度
rect.fill = {
    type: 'linear',
    angle: 45,        // 角度（度）
    stops: [
        { offset: 0, color: '#32cd79' },
        { offset: 1, color: '#ff6b6b' }
    ]
}

// 简写
rect.fill = {
    type: 'linear',
    from: 'left',
    to: 'right',
    stops: { 0: '#32cd79', 1: '#ff6b6b' }
}
```

#### 径向渐变

```typescript
rect.fill = {
    type: 'radial',
    x: 0.5,           // 中心点 X (0-1)
    y: 0.5,           // 中心点 Y (0-1)
    radius: 0.5,      // 半径 (0-1)
    stops: [
        { offset: 0, color: '#ffcd00' },
        { offset: 1, color: '#ff6b6b' }
    ]
}

// 椭圆径向渐变
rect.fill = {
    type: 'radial',
    x: 0.5,
    y: 0.5,
    radiusX: 0.5,     // X 轴半径
    radiusY: 0.3,     // Y 轴半径
    stops: [
        { offset: 0, color: '#32cd79' },
        { offset: 1, color: '#0066ff' }
    ]
}
```

#### 角向渐变 (圆锥渐变)

```typescript
rect.fill = {
    type: 'angular',
    x: 0.5,
    y: 0.5,
    angle: 0,         // 起始角度
    stops: [
        { offset: 0, color: 'red' },
        { offset: 0.17, color: 'orange' },
        { offset: 0.33, color: 'yellow' },
        { offset: 0.5, color: 'green' },
        { offset: 0.67, color: 'blue' },
        { offset: 0.83, color: 'indigo' },
        { offset: 1, color: 'violet' }
    ]
}
```

### 图案填充

```typescript
rect.fill = {
    type: 'image',
    url: 'pattern.png',
    mode: 'repeat',   // 'repeat', 'repeat-x', 'repeat-y', 'no-repeat'
    scale: 1,         // 图案缩放
    x: 0,             // 图案偏移 X
    y: 0              // 图案偏移 Y
}

// 固定平铺图案
rect.fill = {
    type: 'image',
    url: 'pattern.png',
    mode: 'repeat',
    scaleFixed: true  // 图案大小不随元素缩放
}

// 图案间距控制
rect.fill = {
    type: 'image',
    url: 'pattern.png',
    mode: 'repeat',
    spacing: 10      // 图案间距
}

// 图案交错排列
rect.fill = {
    type: 'image',
    url: 'pattern.png',
    mode: 'repeat',
    stagger: true     // 交错排列
}
```

### 清除填充

```typescript
rect.fill = ''        // 清除填充
rect.fill = null
rect.fill = undefined
```

---

## 描边 (stroke)

### 基础描边

```typescript
rect.stroke = '#333'          // 描边颜色
rect.strokeWidth = 2          // 描边宽度
rect.strokeAlign = 'center'   // 对齐: 'center', 'inside', 'outside'
```

### 描边样式

```typescript
// 虚线
rect.strokeDashArray = [10, 5]    // [实线长度, 间隙长度]
rect.strokeDashOffset = 0          // 虚线偏移

// 线帽
rect.strokeCap = 'round'            // 'butt', 'round', 'square'

// 连接
rect.strokeJoin = 'round'           // 'miter', 'round', 'bevel'
rect.strokeMiterLimit = 4           // 斜接限制

// 渐变描边
rect.stroke = {
    type: 'linear',
    stops: { 0: '#32cd79', 1: '#ff6b6b' }
}
```

### 多描边

```typescript
rect.stroke = [
    { color: '#333', width: 4 },      // 外圈
    { color: 'white', width: 2 }      // 内圈
]
```

---

## 阴影 (shadow)

### 外阴影

```typescript
rect.shadow = {
    x: 4,               // X 偏移
    y: 4,               // Y 偏移
    blur: 8,            // 模糊半径
    color: '#00000040'  // 阴影颜色
}

// 简写
rect.shadow = '4px 4px 8px #00000040'

// 多个阴影
rect.shadow = [
    { x: 2, y: 2, blur: 4, color: '#00000020' },
    { x: 4, y: 4, blur: 8, color: '#00000010' }
]

// 固定阴影（不随元素缩放）
rect.shadow = {
    x: 4, y: 4, blur: 8, color: '#00000040',
    scaleFixed: true
}

// 固定阴影（随画布缩放）
rect.shadow = {
    x: 4, y: 4, blur: 8, color: '#00000040',
    scaleFixed: 'zoom-in'
}
```

### 内阴影 (innerShadow)

```typescript
rect.innerShadow = {
    x: 4,
    y: 4,
    blur: 8,
    color: '#00000030'
}

// 多个内阴影
rect.innerShadow = [
    { x: 2, y: 2, blur: 4, color: '#00000020' },
    { x: -2, y: -2, blur: 4, color: '#ffffff20' }
]
```

### Box 阴影

容器元素的阴影：

```typescript
box.boxShadow = {
    x: 0,
    y: 4,
    blur: 12,
    color: '#00000015'
}
```

---

## 模糊效果

### 元素模糊 (blur)

```typescript
rect.blur = 5         // 高斯模糊半径
```

### 背景模糊 (backgroundBlur)

```typescript
// 元素背后的内容模糊
rect.backgroundBlur = 10

// 配合半透明使用
rect.fill = 'rgba(255, 255, 255, 0.8)'
rect.backgroundBlur = 10
```

---

## 混合模式 (blendMode)

```typescript
rect.blendMode = 'multiply'
```

可用混合模式：

| 模式 | 效果 |
|------|------|
| `'normal'` | 正常（默认） |
| `'multiply'` | 正片叠底 |
| `'screen'` | 滤色 |
| `'overlay'` | 叠加 |
| `'darken'` | 变暗 |
| `'lighten'` | 变亮 |
| `'color-dodge'` | 颜色减淡 |
| `'color-burn'` | 颜色加深 |
| `'hard-light'` | 强光 |
| `'soft-light'` | 柔光 |
| `'difference'` | 差值 |
| `'exclusion'` | 排除 |
| `'hue'` | 色相 |
| `'saturation'` | 饱和度 |
| `'color'` | 颜色 |
| `'luminosity'` | 亮度 |

### 子元素混合模式

子元素与父元素内容的混合：

```typescript
rect.childBlendMode = 'multiply'
```

---

## 裁剪与遮罩

### 裁剪 (clip)

```typescript
// 元素作为裁剪区域
parent.clip = true

// 或使用 clipPath
parent.clipPath = {
    type: 'rect',
    x: 0, y: 0,
    width: 100, height: 100
}
```

### 遮罩 (mask)

```typescript
// 使用另一个元素作为遮罩
rect.mask = maskElement

// 或使用遮罩图像
rect.mask = {
    type: 'image',
    url: 'mask.png'
}
```

### 擦除 (eraser)

```typescript
// 从父元素中擦除该元素区域
eraser.eraser = true
```

---

## 滤镜 (filter)

需要 `@leafer-in/filter` 插件。

```typescript
import '@leafer-in/filter'
```

### 可用滤镜

```typescript
// 模糊
rect.filter = 'blur(5px)'

// 亮度
rect.filter = 'brightness(1.5)'    // >1 变亮，<1 变暗

// 对比度
rect.filter = 'contrast(1.2)'

// 灰度
rect.filter = 'grayscale(1)'       // 0-1

// 色相旋转
rect.filter = 'hue-rotate(90deg)'

// 反色
rect.filter = 'invert(1)'

// 不透明度
rect.filter = 'opacity(0.5)'

// 饱和度
rect.filter = 'saturate(1.5)'

// 复古
rect.filter = 'sepia(1)'

// 组合
rect.filter = 'blur(5px) brightness(1.2) saturate(1.5)'
```

---

## 不透明度

```typescript
rect.opacity = 0.5        // 0-1
rect.visible = false      // 完全隐藏（不参与渲染）
```

### 组透明度（无叠加）

组内元素的透明度不相互叠加：

```typescript
group.groupOpacity = true
```

---

## 圆角 (cornerRadius)

```typescript
// 统一圆角
rect.cornerRadius = 8

// 分别设置
rect.cornerRadius = [20, 10, 20, 10]  // [左上, 右上, 右下, 左下]
rect.cornerRadius = [20, 10]         // [左上/右下, 右上/左下]
rect.cornerRadius = [20, 10, 20]     // [左上, 右上/左下, 右下]
```

### 平滑圆角

需要 `@leafer-in/corner` 插件：

```typescript
rect.cornerSmoothing = true
```

---

## 像素对齐

```typescript
rect.pixelAligned = true      // 像素对齐，使边缘更清晰
```

---

## 光标样式

```typescript
rect.cursor = 'pointer'        // 悬停时鼠标样式
```

可用光标值：
- `'default'`
- `'pointer'`
- `'move'`
- `'grab'` / `'grabbing'`
- `'crosshair'`
- `'text'`
- `'wait'`
- `'help'`
- `'not-allowed'`
- `'zoom-in'` / `'zoom-out'`
- `'nw-resize'` / `'ne-resize'` / `'sw-resize'` / `'se-resize'`
- `'n-resize'` / `'s-resize'` / `'w-resize'` / `'e-resize'`
- `'ns-resize'` / `'ew-resize'` / `'nesw-resize'` / `'nwse-resize'`

---

## 状态样式

需要 `@leafer-in/state` 插件。

```typescript
import '@leafer-in/state'

const rect = new Rect({
    fill: '#32cd79',
    
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
            x: 0, y: 4, blur: 8, color: '#00000020'
        }
    },
    
    disabledStyle: {            // 禁用状态
        opacity: 0.5
    }
})
```

---

## 过渡动画

```typescript
// 设置过渡
rect.transition = {
    duration: 0.3,
    easing: 'ease-out'
}

// 修改属性时自动动画
rect.x = 500
rect.fill = '#ff0000'
rect.scale = 1.5

// 移除过渡
rect.transition = false
```

---

## 完整示例

### 卡片设计

```typescript
import { Leafer, Box, Text, Rect } from 'leafer-ui'

const leafer = new Leafer({ view: window })

const card = new Box({
    x: 100,
    y: 100,
    width: 300,
    padding: 20,
    
    // 背景
    fill: {
        type: 'linear',
        from: 'top',
        to: 'bottom',
        stops: {
            0: '#ffffff',
            1: '#f8f9fa'
        }
    },
    
    // 圆角
    cornerRadius: 16,
    
    // 阴影
    shadow: {
        x: 0,
        y: 8,
        blur: 24,
        color: '#00000015'
    },
    
    // 边框
    stroke: '#e9ecef',
    strokeWidth: 1,
    strokeAlign: 'inside'
})

// 标题
const title = new Text({
    text: '高级卡片',
    fontSize: 20,
    fontWeight: 'bold',
    fill: '#333',
    marginBottom: 12
})

// 内容区域
const content = new Rect({
    width: '100%',
    height: 100,
    fill: '#f1f3f5',
    cornerRadius: 8,
    marginBottom: 16
})

// 按钮
const button = new Rect({
    x: 'right',
    width: 100,
    height: 40,
    fill: '#32cd79',
    cornerRadius: 20,
    cursor: 'pointer'
})

button.add(new Text({
    x: 'center',
    y: 'center',
    text: '确认',
    fill: 'white',
    fontSize: 14
}))

card.add(title)
card.add(content)
card.add(button)

leafer.add(card)
```

### 毛玻璃效果

```typescript
import { Leafer, Box, Text, Rect } from 'leafer-ui'

const leafer = new Leafer({ view: window })

// 背景图片
const bg = new Rect({
    width: 800,
    height: 600,
    fill: {
        type: 'linear',
        from: 'top left',
        to: 'bottom right',
        stops: {
            0: '#667eea',
            1: '#764ba2'
        }
    }
})

// 毛玻璃卡片
const glassCard = new Box({
    x: 200,
    y: 150,
    width: 400,
    height: 300,
    padding: 40,
    
    // 半透明白色背景
    fill: 'rgba(255, 255, 255, 0.25)',
    
    // 背景模糊
    backgroundBlur: 20,
    
    // 圆角
    cornerRadius: 24,
    
    // 边框
    stroke: 'rgba(255, 255, 255, 0.3)',
    strokeWidth: 1
})

glassCard.add(new Text({
    text: 'Glassmorphism',
    fontSize: 32,
    fontWeight: 'bold',
    fill: 'white'
}))

glassCard.add(new Text({
    y: 60,
    text: 'This is a glassmorphism card with background blur effect.',
    fontSize: 16,
    fill: 'rgba(255, 255, 255, 0.8)',
    lineHeight: 1.5
}))

leafer.add(bg)
leafer.add(glassCard)
```

### 渐变按钮

```typescript
import { Leafer, Rect, Text } from 'leafer-ui'

const leafer = new Leafer({ view: window })

const button = new Rect({
    x: 100,
    y: 100,
    width: 160,
    height: 50,
    
    // 渐变填充
    fill: {
        type: 'linear',
        from: 'left',
        to: 'right',
        stops: {
            0: '#667eea',
            1: '#764ba2'
        }
    },
    
    // 圆角
    cornerRadius: 25,
    
    // 阴影
    shadow: {
        x: 0,
        y: 4,
        blur: 15,
        color: '#667eea50'
    },
    
    // 交互
    cursor: 'pointer',
    hoverStyle: {
        shadow: {
            x: 0, y: 6, blur: 20,
            color: '#667eea60'
        }
    },
    pressStyle: {
        scale: 0.98
    }
})

button.add(new Text({
    x: 'center',
    y: 'center',
    text: 'Gradient',
    fill: 'white',
    fontSize: 16,
    fontWeight: 'bold'
}))

leafer.add(button)
```

### 霓虹效果

```typescript
import { Leafer, Rect } from 'leafer-ui'

const leafer = new Leafer({ view: window })

// 深色背景
leafer.add(new Rect({
    width: 800,
    height: 600,
    fill: '#0a0a0a'
}))

// 霓虹方块
const neonBox = new Rect({
    x: 300,
    y: 200,
    width: 200,
    height: 200,
    fill: 'transparent',
    stroke: '#00ff88',
    strokeWidth: 2,
    cornerRadius: 16,
    
    // 多重发光阴影
    shadow: [
        { x: 0, y: 0, blur: 20, color: '#00ff8840' },
        { x: 0, y: 0, blur: 40, color: '#00ff8820' },
        { x: 0, y: 0, blur: 60, color: '#00ff8810' }
    ]
})

leafer.add(neonBox)
```

### 材质设计

```typescript
import { Leafer, Rect, Ellipse } from 'leafer-ui'

const leafer = new Leafer({ view: window, fill: '#f5f5f5' })

// 阴影层级
const shadows = {
    z1: { x: 0, y: 1, blur: 3, color: '#00000015' },
    z2: { x: 0, y: 3, blur: 6, color: '#00000020' },
    z3: { x: 0, y: 6, blur: 12, color: '#00000025' },
    z4: { x: 0, y: 10, blur: 20, color: '#00000030' },
    z5: { x: 0, y: 15, blur: 30, color: '#00000035' }
}

// 浮动按钮
const fab = new Ellipse({
    x: 600,
    y: 400,
    width: 56,
    height: 56,
    fill: '#ff4081',
    shadow: shadows.z3,
    cursor: 'pointer',
    
    hoverStyle: {
        shadow: shadows.z4
    },
    pressStyle: {
        shadow: shadows.z5
    }
})

leafer.add(fab)
```
