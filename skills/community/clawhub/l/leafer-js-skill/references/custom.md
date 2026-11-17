# LeaferJS 自定义元素

本文档介绍如何创建自定义 UI 元素和扩展 LeaferJS。

---

## 自定义 UI 基础

### 继承 UI 基类

```typescript
import { UI, registerUI } from 'leafer-ui'

// 定义自定义元素
class MyShape extends UI {
    // 定义属性
    customColor: string = '#32cd79'
    customRadius: number = 50
    
    // 重写绘制方法
    __draw(context: any, data: any) {
        const { x, y, width, height } = data
        
        // 自定义绘制逻辑
        context.beginPath()
        context.arc(x + width / 2, y + height / 2, this.customRadius, 0, Math.PI * 2)
        context.fillStyle = this.customColor
        context.fill()
    }
    
    // 定义包围盒
    __updateBox(): void {
        const r = this.customRadius
        this.__setBox(0, 0, r * 2, r * 2)
    }
}

// 注册自定义元素
registerUI('MyShape', MyShape)

// 使用自定义元素
const shape = new MyShape({
    x: 100, y: 100,
    customColor: '#ff6b6b',
    customRadius: 60
})

leafer.add(shape)
```

### 使用装饰器

```typescript
import { UI, registerUI, dataType, boundsType } from 'leafer-ui'

class Star extends UI {
    @dataType(5)
    points: number  // 星形顶点数
    
    @dataType(50)
    innerRadius: number  // 内半径
    
    @dataType(100)
    outerRadius: number  // 外半径
    
    @boundsType('width')
    size: number  // 自动计算包围盒
    
    __draw(context: any, data: any) {
        const { x, y } = data
        const cx = x + this.size / 2
        const cy = y + this.size / 2
        
        context.beginPath()
        for (let i = 0; i < this.points * 2; i++) {
            const radius = i % 2 === 0 ? this.outerRadius : this.innerRadius
            const angle = (i * Math.PI) / this.points - Math.PI / 2
            const px = cx + radius * Math.cos(angle)
            const py = cy + radius * Math.sin(angle)
            
            if (i === 0) context.moveTo(px, py)
            else context.lineTo(px, py)
        }
        context.closePath()
        context.fillStyle = this.fill
        context.fill()
        
        if (this.stroke) {
            context.strokeStyle = this.stroke
            context.lineWidth = this.strokeWidth
            context.stroke()
        }
    }
    
    __updateBox(): void {
        const size = this.outerRadius * 2
        this.__setBox(0, 0, size, size)
    }
}

registerUI('Star', Star)

// 使用
const star = new Star({
    x: 200, y: 200,
    points: 5,
    innerRadius: 30,
    outerRadius: 80,
    fill: '#ffd700',
    stroke: '#ff8c00',
    strokeWidth: 3
})

leafer.add(star)
```

---

## 自定义容器

### 特殊布局容器

```typescript
import { Group, registerUI } from 'leafer-ui'

class GridLayout extends Group {
    columns: number = 3
    gap: number = 10
    
    // 自动布局子元素
    __layout() {
        const children = this.children
        const colWidth = (this.width - (this.columns - 1) * this.gap) / this.columns
        
        children.forEach((child, index) => {
            const col = index % this.columns
            const row = Math.floor(index / this.columns)
            
            child.x = col * (colWidth + this.gap)
            child.y = row * (child.height + this.gap)
            child.width = colWidth
        })
    }
    
    // 添加元素时自动布局
    add(child: any) {
        super.add(child)
        this.__layout()
    }
}

registerUI('GridLayout', GridLayout)

// 使用
const grid = new GridLayout({
    x: 50, y: 50,
    width: 600,
    columns: 3,
    gap: 20
})

// 添加子元素
for (let i = 0; i < 9; i++) {
    grid.add(new Rect({
        height: 100,
        fill: `hsl(${i * 40}, 70%, 60%)`,
        cornerRadius: 8
    }))
}

leafer.add(grid)
```

### 虚拟列表容器

```typescript
import { Group, Rect, registerUI } from 'leafer-ui'

class VirtualList extends Group {
    itemHeight: number = 50
    totalItems: number = 1000
    visibleCount: number = 10
    scrollTop: number = 0
    
    private pool: Rect[] = []
    private visibleItems: Rect[] = []
    
    __init() {
        // 创建可见区域的元素池
        for (let i = 0; i < this.visibleCount + 2; i++) {
            const item = new Rect({
                height: this.itemHeight,
                fill: '#fff',
                stroke: '#eee'
            })
            this.pool.push(item)
        }
        
        this.__updateVisibleItems()
    }
    
    __updateVisibleItems() {
        const startIndex = Math.floor(this.scrollTop / this.itemHeight)
        const offset = this.scrollTop % this.itemHeight
        
        // 移除不在可见区域的元素
        this.visibleItems.forEach(item => item.remove())
        this.visibleItems = []
        
        // 复用元素池
        for (let i = 0; i < this.visibleCount + 2; i++) {
            const dataIndex = startIndex + i
            if (dataIndex >= this.totalItems) break
            
            const item = this.pool[i]
            item.y = (startIndex + i) * this.itemHeight - this.scrollTop
            item.width = this.width
            
            // 渲染数据
            this.__renderItem(item, dataIndex)
            
            this.add(item)
            this.visibleItems.push(item)
        }
    }
    
    __renderItem(item: Rect, index: number) {
        // 这里可以自定义渲染逻辑
        // 例如添加文本、图标等
    }
    
    // 滚动方法
    scrollTo(y: number) {
        this.scrollTop = Math.max(0, Math.min(
            y,
            this.totalItems * this.itemHeight - this.height
        ))
        this.__updateVisibleItems()
    }
}

registerUI('VirtualList', VirtualList)
```

---

## 自定义渲染

### 使用自定义 Canvas 绘制

```typescript
import { UI, registerUI } from 'leafer-ui'

class Wave extends UI {
    amplitude: number = 20
    frequency: number = 0.02
    phase: number = 0
    speed: number = 0.05
    
    __draw(context: any, data: any) {
        const { x, y, width, height } = data
        
        context.beginPath()
        context.moveTo(x, y + height / 2)
        
        for (let px = x; px <= x + width; px += 2) {
            const py = y + height / 2 + 
                Math.sin((px - x) * this.frequency + this.phase) * this.amplitude
            context.lineTo(px, py)
        }
        
        context.lineTo(x + width, y + height)
        context.lineTo(x, y + height)
        context.closePath()
        
        context.fillStyle = this.fill
        context.fill()
    }
    
    // 动画更新
    update() {
        this.phase += this.speed
        this.forceUpdate() // 强制重绘
    }
}

registerUI('Wave', Wave)

// 使用
const wave = new Wave({
    x: 0, y: 300,
    width: 800, height: 100,
    fill: 'rgba(100, 200, 255, 0.5)'
})

leafer.add(wave)

// 动画循环
setInterval(() => {
    wave.update()
}, 16)
```

### 离屏渲染

```typescript
import { UI, registerUI, Leafer } from 'leafer-ui'

class CachedShape extends UI {
    private cacheCanvas: HTMLCanvasElement | null = null
    private cacheContext: CanvasRenderingContext2D | null = null
    private needsRedraw: boolean = true
    
    __draw(context: any, data: any) {
        const { x, y, width, height } = data
        
        // 初始化缓存
        if (!this.cacheCanvas || this.cacheCanvas.width !== width || this.cacheCanvas.height !== height) {
            this.cacheCanvas = document.createElement('canvas')
            this.cacheCanvas.width = width
            this.cacheCanvas.height = height
            this.cacheContext = this.cacheCanvas.getContext('2d')
            this.needsRedraw = true
        }
        
        // 只有需要时才重绘到缓存
        if (this.needsRedraw && this.cacheContext) {
            this.__drawToCache(this.cacheContext, width, height)
            this.needsRedraw = false
        }
        
        // 绘制缓存的图像
        if (this.cacheCanvas) {
            context.drawImage(this.cacheCanvas, x, y)
        }
    }
    
    __drawToCache(ctx: CanvasRenderingContext2D, width: number, height: number) {
        // 复杂的绘制逻辑
        // 例如：绘制渐变、阴影、复杂路径等
        const gradient = ctx.createLinearGradient(0, 0, width, height)
        gradient.addColorStop(0, '#ff6b6b')
        gradient.addColorStop(1, '#4ecdc4')
        
        ctx.fillStyle = gradient
        ctx.fillRect(0, 0, width, height)
        
        // 添加复杂装饰
        for (let i = 0; i < 10; i++) {
            ctx.beginPath()
            ctx.arc(
                Math.random() * width,
                Math.random() * height,
                Math.random() * 30 + 10,
                0, Math.PI * 2
            )
            ctx.fillStyle = 'rgba(255, 255, 255, 0.3)'
            ctx.fill()
        }
    }
    
    // 标记需要重绘
    invalidate() {
        this.needsRedraw = true
        this.forceUpdate()
    }
}

registerUI('CachedShape', CachedShape)
```

---

## 自定义插件

### 创建插件

```typescript
// plugins/my-effect.ts
import { Plugin, Leafer } from 'leafer-ui'

export class MyEffectPlugin extends Plugin {
    static type = 'MyEffect'
    
    effect: string = 'none'
    intensity: number = 1
    
    __onLoad(): void {
        // 插件加载时的初始化
        console.log('MyEffect 插件已加载')
    }
    
    __onDraw(context: any, data: any): void {
        // 在绘制前/后应用效果
        if (this.effect === 'glow') {
            context.save()
            context.globalCompositeOperation = 'lighter'
            context.filter = `blur(${10 * this.intensity}px)`
        }
    }
    
    __afterDraw(context: any): void {
        if (this.effect === 'glow') {
            context.restore()
        }
    }
}

// 注册插件
Leafer.registerPlugin(MyEffectPlugin)
```

### 自定义动画缓动函数

```typescript
import { Animate, registerEasing } from '@leafer-in/animate'

// 注册自定义缓动函数
registerEasing('bounce', (t: number) => {
    if (t < 1 / 2.75) {
        return 7.5625 * t * t
    } else if (t < 2 / 2.75) {
        return 7.5625 * (t -= 1.5 / 2.75) * t + 0.75
    } else if (t < 2.5 / 2.75) {
        return 7.5625 * (t -= 2.25 / 2.75) * t + 0.9375
    } else {
        return 7.5625 * (t -= 2.625 / 2.75) * t + 0.984375
    }
})

// 使用自定义缓动
rect.animate(
    { y: 300 },
    { duration: 1, easing: 'bounce' }
)
```

### 自定义编辑器工具

```typescript
import { EditTool, registerEditTool, EditorMoveEvent } from '@leafer-in/editor'

class CustomRectTool extends EditTool {
    get tag(): string {
        return 'Rect'
    }
    
    // 自定义移动行为
    onMove(e: EditorMoveEvent) {
        // 限制只能在水平方向移动
        e.moveY = 0
        super.onMove(e)
    }
    
    // 自定义缩放行为
    onScale(e: EditorScaleEvent) {
        // 保持正方形比例
        const avg = (e.scaleX + e.scaleY) / 2
        e.scaleX = avg
        e.scaleY = avg
        super.onScale(e)
    }
}

registerEditTool('Rect', CustomRectTool)
```

---

## 扩展 Leafer 类

### 扩展 App 类

```typescript
import { App, IAppInputData } from 'leafer-ui'

interface IExtendedAppData extends IAppInputData {
    autoSave?: boolean
    saveInterval?: number
}

class ExtendedApp extends App {
    autoSave: boolean = false
    saveInterval: number = 30000
    
    constructor(data: IExtendedAppInputData) {
        super(data)
        
        this.autoSave = data.autoSave || false
        this.saveInterval = data.saveInterval || 30000
        
        if (this.autoSave) {
            this.__startAutoSave()
        }
    }
    
    private __startAutoSave() {
        setInterval(() => {
            this.save()
        }, this.saveInterval)
    }
    
    save(): void {
        // 导出数据
        const data = this.tree.children.map(child => child.toJSON())
        localStorage.setItem('autoSave', JSON.stringify(data))
        console.log('自动保存完成')
    }
    
    load(): void {
        const data = localStorage.getItem('autoSave')
        if (data) {
            const items = JSON.parse(data)
            items.forEach(item => {
                // 恢复元素
            })
        }
    }
}

// 使用
const app = new ExtendedApp({
    view: window,
    autoSave: true,
    saveInterval: 60000
})
```

### 扩展元素方法

```typescript
import { Rect } from 'leafer-ui'

// 添加便捷方法
declare module 'leafer-ui' {
    interface Rect {
        setColor(color: string): void
        highlight(duration?: number): void
    }
}

Rect.prototype.setColor = function(color: string) {
    this.fill = color
}

Rect.prototype.highlight = function(duration = 500) {
    const originalFill = this.fill
    this.fill = '#ffff00'
    
    setTimeout(() => {
        this.fill = originalFill
    }, duration)
}

// 使用
const rect = new Rect({ fill: '#red' })
rect.setColor('#32cd79')
rect.highlight(1000)
```

---

## 自定义事件

### 定义自定义事件

```typescript
import { Event } from 'leafer-ui'

class CustomEvent extends Event {
    static CUSTOM_EVENT = 'custom.event'
    
    data: any
    
    constructor(type: string, data?: any) {
        super(type)
        this.data = data
    }
}

// 触发自定义事件
const rect = new Rect({ fill: 'red' })

rect.on(CustomEvent.CUSTOM_EVENT, (e: CustomEvent) => {
    console.log('收到自定义事件:', e.data)
})

// 派发事件
rect.emitEvent(new CustomEvent(CustomEvent.CUSTOM_EVENT, { message: 'Hello' }))
```

---

## 性能优化技巧

### 对象池模式

```typescript
class ElementPool {
    private pools: Map<string, any[]> = new Map()
    
    get<T>(type: string, factory: () => T): T {
        const pool = this.pools.get(type) || []
        this.pools.set(type, pool)
        
        return (pool.pop() as T) || factory()
    }
    
    release(type: string, element: any) {
        const pool = this.pools.get(type) || []
        pool.push(element)
        this.pools.set(type, pool)
    }
    
    clear() {
        this.pools.clear()
    }
}

// 使用
const pool = new ElementPool()

// 获取元素
const rect = pool.get('rect', () => new Rect())
rect.set({ x: 100, y: 100, fill: 'red' })
leafer.add(rect)

// 回收元素
rect.remove()
pool.release('rect', rect)
```

### 延迟加载

```typescript
class LazyImage extends UI {
    src: string = ''
    placeholder: string = '#f0f0f0'
    private loaded: boolean = false
    private image: HTMLImageElement | null = null
    
    __draw(context: any, data: any) {
        const { x, y, width, height } = data
        
        if (!this.loaded) {
            // 显示占位符
            context.fillStyle = this.placeholder
            context.fillRect(x, y, width, height)
            
            // 异步加载图片
            this.__loadImage()
        } else if (this.image) {
            // 绘制图片
            context.drawImage(this.image, x, y, width, height)
        }
    }
    
    private __loadImage() {
        if (this.image) return
        
        this.image = new Image()
        this.image.onload = () => {
            this.loaded = true
            this.forceUpdate()
        }
        this.image.src = this.src
    }
}

registerUI('LazyImage', LazyImage)
```
