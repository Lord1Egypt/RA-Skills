# LeaferJS 调试指南

本文档介绍 LeaferJS 的调试工具和性能优化方法。

---

## Debug 工具

### 启用调试模式

```typescript
import { Leafer, Debug } from 'leafer-ui'

// 启用调试
Debug.enable = true

// 设置过滤级别
Debug.filter = 'RunTime'  // 只显示运行时信息
```

### 调试级别

| 级别 | 说明 |
|------|------|
| `'RunTime'` | 运行时性能信息 |
| `'Layout'` | 布局计算信息 |
| `'Render'` | 渲染信息 |
| `'Hit'` | 命中检测信息 |
| `'Event'` | 事件信息 |
| `'All'` | 所有信息 |

### 性能监控

```typescript
import { Leafer, Rect, Debug } from 'leafer-ui'

const leafer = new Leafer({ view: window })

// 启用调试
Debug.enable = true
Debug.filter = 'RunTime'

// 测试创建性能
console.time('create')
const rects = []
for (let i = 0; i < 10000; i++) {
    rects.push(new Rect({
        x: (i % 100) * 12,
        y: Math.floor(i / 100) * 12,
        width: 10, height: 10,
        fill: `hsl(${(i * 3) % 360}, 70%, 60%)`,
        draggable: true
    }))
}
console.timeEnd('create')  // 创建时间

// 测试渲染性能
console.time('add')
leafer.addMany(rects)
console.timeEnd('add')  // 渲染时间

// 查看 Debug 输出的 FPS 和内存信息
```

---

## 性能测试

### 基准测试方法

```typescript
import { Leafer, Rect, Text, Debug } from 'leafer-ui'

class Benchmark {
    results: { test: string; time: number }[] = []
    
    async run(name: string, fn: () => void, iterations = 1) {
        const times: number[] = []
        
        for (let i = 0; i < iterations; i++) {
            const start = performance.now()
            await fn()
            const end = performance.now()
            times.push(end - start)
        }
        
        const avg = times.reduce((a, b) => a + b, 0) / times.length
        this.results.push({ test: name, time: avg })
        console.log(`${name}: ${avg.toFixed(2)}ms`)
    }
    
    report() {
        console.table(this.results)
    }
}

// 使用示例
const benchmark = new Benchmark()
const leafer = new Leafer({ view: window })

await benchmark.run('创建 1000 个矩形', () => {
    const rects = []
    for (let i = 0; i < 1000; i++) {
        rects.push(new Rect({
            x: i * 2, y: 100,
            width: 10, height: 10,
            fill: 'red'
        }))
    }
    leafer.removeAll()
    leafer.addMany(rects)
}, 10)

benchmark.report()
```

### 内存分析

```typescript
// 记录初始内存
const startMemory = performance.memory?.usedJSHeapSize

// 创建大量元素
const elements = []
for (let i = 0; i < 100000; i++) {
    elements.push(new Rect({
        x: i % 1000,
        y: Math.floor(i / 1000),
        width: 5, height: 5,
        fill: 'blue'
    }))
}

// 记录创建后内存
const midMemory = performance.memory?.usedJSHeapSize

// 清理
leafer.addMany(elements)
leafer.removeAll()
elements.length = 0

// 强制垃圾回收后记录（开发工具中手动触发）
const endMemory = performance.memory?.usedJSHeapSize

console.log({
    start: startMemory,
    mid: midMemory,
    end: endMemory,
    createOverhead: midMemory - startMemory,
    cleanupOverhead: endMemory - startMemory
})
```

---

## 常见问题排查

### 画布不显示

```typescript
// 检查 1: 容器是否存在
const container = document.getElementById('leafer-view')
console.log('容器存在:', !!container)

// 检查 2: 容器尺寸
console.log('容器尺寸:', container?.offsetWidth, container?.offsetHeight)

// 检查 3: 正确初始化
const leafer = new Leafer({
    view: 'leafer-view',  // 注意：不加 #
    width: 800,
    height: 600
})

// 检查 4: 元素是否被添加
const rect = new Rect({
    x: 100, y: 100,
    width: 100, height: 100,
    fill: 'red'
})
leafer.add(rect)
console.log('子元素数量:', leafer.children.length)
```

### 元素不响应事件

```typescript
// 问题 1: 未设置可交互
const rect = new Rect({
    x: 100, y: 100,
    width: 100, height: 100,
    fill: 'red'
})

// 解决方案：设置 hittable 为 true（默认 true）
rect.hittable = true

// 或设置 draggable 自动启用交互
rect.draggable = true

// 问题 2: 事件监听错误
// 错误：事件类型字符串
rect.on('click', () => {})  // ❌

// 正确：使用事件常量
import { PointerEvent } from 'leafer-ui'
rect.on(PointerEvent.TAP, () => {})  // ✅

// 问题 3: 事件冒泡被阻止
rect.on(PointerEvent.TAP, (e) => {
    e.stopPropagation()  // 阻止冒泡
})
```

### 动画不生效

```typescript
import { Animate } from '@leafer-in/animate'

// 问题 1: 目标状态已达到
const rect = new Rect({ x: 0, y: 0, fill: 'red' })

// 动画从当前值到目标值，如果当前值已是目标值则看不到变化
new Animate(rect, { x: 0 }, { duration: 1 })  // 无效果

// 正确：设置不同的目标值
new Animate(rect, { x: 100 }, { duration: 1 })  // ✅

// 问题 2: 动画被销毁
const animate = new Animate(rect, { x: 100 }, { duration: 1 })
animate.destroy()  // 立即停止并销毁

// 问题 3: 在 React/Vue 中元素被重新创建
// 解决方案：确保元素引用稳定
```

### 框架集成问题

#### Vue 响应式问题

```typescript
import { ref, shallowRef } from 'vue'
import { Leafer, Rect } from 'leafer-ui'

// ❌ 错误：响应式会深度代理
const leafer = ref<Leafer>()
const elements = ref<Rect[]>([])

// ✅ 正确：使用普通变量或 shallowRef
let leafer: Leafer
const elements = shallowRef<Rect[]>([])

// ❌ 错误：直接修改响应式对象
function addRect() {
    const rect = new Rect({ fill: 'red' })
    elements.value.push(rect)  // 会触发响应式代理
}

// ✅ 正确：重新赋值整个数组
function addRect() {
    const rect = new Rect({ fill: 'red' })
    elements.value = [...elements.value, rect]
}
```

#### React Hook 问题

```typescript
import { useEffect, useRef } from 'react'
import { Leafer } from 'leafer-ui'

// ❌ 错误：useEffect 执行两次导致重复创建
function Component() {
    useEffect(() => {
        const leafer = new Leafer({ view: 'view' })
    }, [])
    
    return <div id="view" />
}

// ✅ 正确：使用 ref 和 cleanup
function Component() {
    const leaferRef = useRef<Leafer | null>(null)
    
    useEffect(() => {
        let destroyed = false
        
        import('leafer-ui').then(({ Leafer }) => {
            if (destroyed) return
            leaferRef.current = new Leafer({ view: 'view' })
        })
        
        return () => {
            destroyed = true
            leaferRef.current?.destroy()
        }
    }, [])
    
    return <div id="view" />
}
```

---

## 渲染问题诊断

### 检查渲染流程

```typescript
import { RenderEvent } from 'leafer-ui'

// 监听渲染事件
leafer.on(RenderEvent.START, () => {
    console.log('渲染开始')
})

leafer.on(RenderEvent.END, () => {
    console.log('渲染结束')
})

// 检查 FPS
let frameCount = 0
let lastTime = performance.now()

setInterval(() => {
    const now = performance.now()
    const fps = Math.round(frameCount * 1000 / (now - lastTime))
    console.log('FPS:', fps)
    frameCount = 0
    lastTime = now
}, 1000)

leafer.on(RenderEvent.END, () => {
    frameCount++
})
```

### 重绘优化检测

```typescript
// 检测不必要的重绘
import { RenderEvent } from 'leafer-ui'

let renderCount = 0
leafer.on(RenderEvent.END, () => {
    renderCount++
    console.log(`渲染次数: ${renderCount}`)
})

// 避免频繁属性更新（每次更新都触发渲染）
const rect = new Rect()

// ❌ 错误：触发 3 次渲染
rect.x = 100
rect.y = 100
rect.fill = 'red'

// ✅ 正确：只触发 1 次渲染
rect.set({ x: 100, y: 100, fill: 'red' })
```

---

## 事件调试

### 事件日志

```typescript
import { PointerEvent, DragEvent, DropEvent } from 'leafer-ui'

function logEvents(target: any, name: string) {
    const events = [
        PointerEvent.DOWN,
        PointerEvent.UP,
        PointerEvent.TAP,
        PointerEvent.MOVE,
        PointerEvent.ENTER,
        PointerEvent.LEAVE,
        DragEvent.START,
        DragEvent.DRAG,
        DragEvent.STOP,
        DropEvent.DROP
    ]
    
    events.forEach(event => {
        target.on(event, (e: any) => {
            console.log(`${name}: ${event}`, {
                x: e.x,
                y: e.y,
                target: e.target?.constructor?.name
            })
        })
    })
}

// 使用
const rect = new Rect({ fill: 'red', draggable: true })
logEvents(rect, 'Rect')
leafer.add(rect)
```

### 事件传播分析

```typescript
// 查看事件冒泡路径
rect.on(PointerEvent.TAP, (e) => {
    const path: string[] = []
    let current = e.target
    while (current) {
        path.push(current.constructor.name)
        current = current.parent
    }
    console.log('事件路径:', path.join(' -> '))
})

// 阻止默认行为和冒泡
rect.on(PointerEvent.DOWN, (e) => {
    e.preventDefault()  // 阻止默认行为
    e.stopPropagation() // 阻止冒泡
})
```

---

## 内存泄漏排查

### 检查元素引用

```typescript
// 检查是否被正确移除
const rect = new Rect({ fill: 'red' })
leafer.add(rect)

console.log('父元素:', rect.parent) // Leafer

rect.remove()
console.log('父元素:', rect.parent) // null

// 检查事件监听是否被清理
const handler = () => console.log('clicked')
rect.on(PointerEvent.TAP, handler)

// 获取监听器数量
console.log('监听器数量:', rect.eventMap?.size || 0)

rect.off(PointerEvent.TAP, handler)
console.log('监听器数量:', rect.eventMap?.size || 0)
```

### 内存快照对比

```typescript
// 在浏览器开发者工具中

// 1. 记录初始内存快照
// DevTools -> Memory -> Take heap snapshot

// 2. 创建元素
for (let i = 0; i < 1000; i++) {
    leafer.add(new Rect({ fill: 'red' }))
}

// 3. 移除元素
leafer.removeAll()

// 4. 记录第二次快照
// DevTools -> Memory -> Take heap snapshot

// 5. 对比两次快照
// 查看 Rect 对象是否被正确回收
```

---

## 性能优化检查清单

### 渲染优化

```typescript
// ✅ 使用批量添加
const elements = []
for (let i = 0; i < 1000; i++) {
    elements.push(new Rect({ ... }))
}
leafer.addMany(elements)

// ✅ 使用 set 批量设置属性
rect.set({ x: 100, y: 100, fill: 'red' })

// ✅ 使用 willReadFrequently
const leafer = new Leafer({
    view: window,
    willReadFrequently: true
})

// ✅ 固定像素比
const leafer = new Leafer({
    view: window,
    pixelRatio: 1  // 性能优先
})

// ✅ 隐藏而非销毁暂时不用的元素
element.visible = false  // 性能好
// vs
element.remove()         // 需要时再创建，性能差
```

### 内存优化

```typescript
// ✅ 及时销毁
onUnmounted(() => {
    leafer?.destroy()
})

// ✅ 移除事件监听
const handler = () => {}
element.on(PointerEvent.TAP, handler)
element.off(PointerEvent.TAP, handler)  // 清理

// ✅ 使用对象池
class RectPool {
    private pool: Rect[] = []
    
    get(props: any) {
        const rect = this.pool.pop() || new Rect()
        rect.set(props)
        return rect
    }
    
    release(rect: Rect) {
        rect.remove()
        this.pool.push(rect)
    }
}
```

---

## 调试技巧

### 显示边界框

```typescript
// 查看元素的边界
const rect = new Rect({
    x: 100, y: 100,
    width: 200, height: 150,
    fill: '#32cd79'
})

leafer.add(rect)

// 打印边界信息
console.log('Bounds:', rect.bounds)
console.log('World Bounds:', rect.worldBounds)
console.log('Render Bounds:', rect.renderBounds)
```

### 颜色调试

```typescript
// 使用随机颜色区分元素
function randomColor() {
    return `hsl(${Math.random() * 360}, 70%, 60%)`
}

// 创建彩色网格便于观察
for (let i = 0; i < 100; i++) {
    leafer.add(new Rect({
        x: (i % 10) * 50,
        y: Math.floor(i / 10) * 50,
        width: 45, height: 45,
        fill: randomColor()
    }))
}
```

### 慢动作调试

```typescript
import { Animate } from '@leafer-in/animate'

// 放慢动画便于观察
new Animate(rect, 
    { x: 500, rotation: 360 },
    { duration: 5, easing: 'ease-in-out' }  // 延长到 5 秒
)

// 添加关键帧日志
const animate = new Animate(rect,
    [
        { x: 0, y: 0 },
        { x: 100, y: 0 },
        { x: 100, y: 100 },
        { x: 0, y: 100 }
    ],
    { duration: 4 }
)

animate.on(AnimateEvent.UPDATE, (e) => {
    console.log('动画进度:', e.progress)
})
```

---

## 错误处理

### 常见错误

```typescript
// 错误 1: 重复初始化
try {
    const leafer = new Leafer({ view: 'view' })
    const leafer2 = new Leafer({ view: 'view' })  // 错误：同一 view 只能有一个实例
} catch (e) {
    console.error('初始化错误:', e)
}

// 错误 2: 无效的 view
try {
    const leafer = new Leafer({ view: 'nonexistent' })  // 元素不存在
} catch (e) {
    console.error('View 错误:', e)
}

// 错误 3: 空值访问
const rect = new Rect()
rect.parent.x  // 错误：parent 为 null

// 正确做法
rect.parent?.x
```

### 全局错误捕获

```typescript
// 捕获 Leafer 内部错误
leafer.on('error', (e) => {
    console.error('Leafer 错误:', e)
})

// 全局错误捕获
window.addEventListener('error', (e) => {
    if (e.message?.includes('leafer')) {
        console.error('Leafer 相关错误:', e)
    }
})

window.addEventListener('unhandledrejection', (e) => {
    console.error('未处理的 Promise 错误:', e)
})
```
