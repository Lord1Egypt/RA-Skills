# LeaferJS 事件系统完整参考

LeaferJS 提供接近浏览器原生的事件系统，支持事件捕获、冒泡、穿透。

## 事件监听方式

### 方式1：on() 方法

```typescript
element.on(eventType, listener, options?)
```

### 方式2：once() 方法

只触发一次：

```typescript
element.once(eventType, listener)
```

### 方式3：配置属性

```typescript
const rect = new Rect({
    onTap: (e) => { console.log('tapped') },
    onDrag: (e) => { console.log('dragging') }
})
```

### 移除监听

```typescript
element.off(eventType, listener?)  // 移除指定监听
element.off(eventType)             // 移除该类型所有监听
element.off()                      // 移除所有监听
```

---

## 事件类型

### 指针事件 (PointerEvent)

```typescript
import { PointerEvent } from 'leafer-ui'
```

| 事件 | 说明 | 触发条件 |
|------|------|----------|
| `PointerEvent.DOWN` | 指针按下 | 鼠标按下/触摸开始 |
| `PointerEvent.UP` | 指针释放 | 鼠标释放/触摸结束 |
| `PointerEvent.TAP` | 点击 | 快速按下并释放 |
| `PointerEvent.DOUBLE_TAP` | 双击 | 快速连续两次点击 |
| `PointerEvent.LONG_PRESS` | 长按 | 按下保持一定时间 |
| `PointerEvent.MOVE` | 指针移动 | 鼠标/触摸移动 |
| `PointerEvent.ENTER` | 指针进入 | 进入元素区域 |
| `PointerEvent.LEAVE` | 指针离开 | 离开元素区域 |
| `PointerEvent.OVER` | 指针悬停 | 进入元素（冒泡） |
| `PointerEvent.OUT` | 指针离开 | 离开元素（冒泡） |

```typescript
rect.on(PointerEvent.TAP, (e) => {
    console.log('点击位置:', e.x, e.y)
})

rect.on(PointerEvent.MOVE, (e) => {
    console.log('当前位置:', e.x, e.y)
})
```

### 拖拽事件 (DragEvent)

```typescript
import { DragEvent } from 'leafer-ui'
```

| 事件 | 说明 |
|------|------|
| `DragEvent.START` | 拖拽开始 |
| `DragEvent.DRAG` | 拖拽中 |
| `DragEvent.STOP` | 拖拽停止 |

```typescript
// 启用拖拽
rect.draggable = true

rect.on(DragEvent.START, (e) => {
    console.log('开始拖拽')
})

rect.on(DragEvent.DRAG, (e) => {
    console.log('拖拽偏移:', e.moveX, e.moveY)
    console.log('总移动距离:', e.totalX, e.totalY)
})

rect.on(DragEvent.STOP, (e) => {
    console.log('拖拽结束')
})
```

### 放置事件 (DropEvent)

```typescript
import { DropEvent } from 'leafer-ui'
```

| 事件 | 说明 |
|------|------|
| `DropEvent.ENTER` | 拖拽进入 |
| `DropEvent.LEAVE` | 拖拽离开 |
| `DropEvent.DROP` | 放置 |

```typescript
// 启用放置
target.dropable = true

target.on(DropEvent.ENTER, (e) => {
    target.fill = '#ffcd00'  // 高亮
})

target.on(DropEvent.LEAVE, (e) => {
    target.fill = '#32cd79'  // 恢复原色
})

target.on(DropEvent.DROP, (e) => {
    console.log('放置元素:', e.drag)
})
```

### 滑动手势 (SwipeEvent)

```typescript
import { SwipeEvent } from 'leafer-ui'
```

| 事件 | 说明 |
|------|------|
| `SwipeEvent.SWIPE` | 滑动手势 |

```typescript
rect.on(SwipeEvent.SWIPE, (e) => {
    console.log('滑动方向:', e.direction)  // 'up' | 'down' | 'left' | 'right'
    console.log('滑动速度:', e.velocity)
})
```

### 移动事件 (MoveEvent)

```typescript
import { MoveEvent } from 'leafer-ui'
```

| 事件 | 说明 |
|------|------|
| `MoveEvent.START` | 移动开始 |
| `MoveEvent.MOVE` | 移动中 |
| `MoveEvent.END` | 移动结束 |

```typescript
leafer.on(MoveEvent.MOVE, (e) => {
    console.log('视口移动:', e.moveX, e.moveY)
})
```

### 缩放事件 (ZoomEvent)

```typescript
import { ZoomEvent } from 'leafer-ui'
```

| 事件 | 说明 |
|------|------|
| `ZoomEvent.ZOOM` | 缩放 |

```typescript
leafer.on(ZoomEvent.ZOOM, (e) => {
    console.log('缩放比例:', e.scale)
    console.log('缩放中心:', e.origin)
})
```

### 旋转事件 (RotateEvent)

```typescript
import { RotateEvent } from 'leafer-ui'
```

| 事件 | 说明 |
|------|------|
| `RotateEvent.ROTATE` | 旋转 |

```typescript
leafer.on(RotateEvent.ROTATE, (e) => {
    console.log('旋转角度:', e.rotation)
})
```

### 键盘事件 (KeyEvent)

```typescript
import { KeyEvent } from 'leafer-ui'
```

| 事件 | 说明 |
|------|------|
| `KeyEvent.DOWN` | 按键按下 |
| `KeyEvent.UP` | 按键释放 |
| `KeyEvent.PRESS` | 按键按下（字符输入） |

```typescript
app.on(KeyEvent.DOWN, (e) => {
    console.log('按键:', e.code)     // 'KeyA'
    console.log('键值:', e.key)      // 'a'
    
    if (e.metaKey) console.log('按住 Command')
    if (e.ctrlKey) console.log('按住 Ctrl')
    if (e.shiftKey) console.log('按住 Shift')
    if (e.altKey) console.log('按住 Alt')
})

// 特定按键
app.on(KeyEvent.DOWN, (e) => {
    switch(e.code) {
        case 'Delete':
            // 删除选中元素
            if (app.editor?.element) {
                app.editor.element.remove()
            }
            break
        case 'KeyC':
            if (e.metaKey || e.ctrlKey) {
                // 复制
                console.log('复制')
            }
            break
    }
})
```

---

## 生命周期事件

### Leafer 事件

```typescript
import { LeaferEvent } from 'leafer-ui'
```

| 事件 | 说明 |
|------|------|
| `LeaferEvent.READY` | Leafer 准备就绪 |
| `LeaferEvent.VIEW_READY` | 视图准备就绪 |
| `LeaferEvent.REQUEST_RENDER` | 请求渲染 |
| `LeaferEvent.RENDER` | 渲染完成 |

```typescript
leafer.on(LeaferEvent.READY, () => {
    console.log('Leafer 准备就绪')
})

leafer.on(LeaferEvent.VIEW_READY, () => {
    console.log('视图渲染完成')
})
```

### 渲染事件

```typescript
import { RenderEvent } from 'leafer-ui'
```

| 事件 | 说明 |
|------|------|
| `RenderEvent.START` | 渲染开始 |
| `RenderEvent.END` | 渲染结束 |
| `RenderEvent.REQUEST` | 请求渲染 |

```typescript
leafer.on(RenderEvent.START, () => {
    console.log('渲染开始')
})

leafer.on(RenderEvent.END, () => {
    console.log('渲染结束')
})
```

### 布局事件

```typescript
import { LayoutEvent } from 'leafer-ui'
```

| 事件 | 说明 |
|------|------|
| `LayoutEvent.REQUEST` | 请求布局 |
| `LayoutEvent.BEFORE` | 布局前 |
| `LayoutEvent.AFTER` | 布局后 |

```typescript
element.on(LayoutEvent.AFTER, () => {
    console.log('布局完成')
})
```

### 尺寸变化事件

```typescript
import { ResizeEvent } from 'leafer-ui'
```

| 事件 | 说明 |
|------|------|
| `ResizeEvent.RESIZE` | 尺寸变化 |

```typescript
leafer.on(ResizeEvent.RESIZE, (e) => {
    console.log('新尺寸:', e.width, e.height)
})
```

---

## 编辑器事件

```typescript
import { EditorEvent, EditorMoveEvent, EditorScaleEvent } from '@leafer-in/editor'
```

### 选择事件

```typescript
app.editor.on(EditorEvent.SELECT, (e) => {
    console.log('选中元素:', e.editor.list)
    console.log('是否多选:', e.editor.multiple)
})

app.editor.on(EditorEvent.UNSELECT, (e) => {
    console.log('取消选中')
})
```

### 变换事件

```typescript
// 移动
app.editor.on(EditorMoveEvent.MOVE, (e) => {
    console.log('移动:', e.moveX, e.moveY)
})

// 缩放
app.editor.on(EditorScaleEvent.SCALE, (e) => {
    console.log('缩放:', e.scaleX, e.scaleY)
})

// 旋转
app.editor.on(EditorRotateEvent.ROTATE, (e) => {
    console.log('旋转:', e.rotation)
})

// 倾斜
app.editor.on(EditorSkewEvent.SKEW, (e) => {
    console.log('倾斜:', e.skewX, e.skewY)
})
```

### 编组事件

```typescript
app.editor.on(EditorGroupEvent.GROUP, (e) => {
    console.log('编组:', e.group)
})

app.editor.on(EditorGroupEvent.UNGROUP, (e) => {
    console.log('解组')
})
```

### 内部编辑器事件

```typescript
app.editor.on(InnerEditorEvent.OPEN, (e) => {
    console.log('打开内部编辑器')
})

app.editor.on(InnerEditorEvent.CLOSE, (e) => {
    console.log('关闭内部编辑器')
})
```

---

## 动画事件

```typescript
import { AnimateEvent } from '@leafer-in/animate'
```

| 事件 | 说明 |
|------|------|
| `AnimateEvent.PLAY` | 动画开始播放 |
| `AnimateEvent.PAUSE` | 动画暂停 |
| `AnimateEvent.UPDATE` | 动画更新中 |
| `AnimateEvent.LOOP` | 动画循环 |
| `AnimateEvent.COMPLETED` | 动画完成 |
| `AnimateEvent.DESTROY` | 动画销毁 |

```typescript
const animate = rect.animate({ x: 500 }, { duration: 2 })

animate.on(AnimateEvent.PLAY, () => {
    console.log('动画开始')
})

animate.on(AnimateEvent.UPDATE, (e) => {
    console.log('当前位置:', e.style.x)
})

animate.on(AnimateEvent.COMPLETED, () => {
    console.log('动画完成')
})
```

---

## 子元素事件 (ChildEvent)

```typescript
import { ChildEvent } from 'leafer-ui'
```

| 事件 | 说明 |
|------|------|
| `ChildEvent.ADD` | 添加子元素 |
| `ChildEvent.REMOVE` | 移除子元素 |

```typescript
container.on(ChildEvent.ADD, (e) => {
    console.log('添加子元素:', e.child)
})

container.on(ChildEvent.REMOVE, (e) => {
    console.log('移除子元素:', e.child)
})
```

---

## 属性变化事件 (PropertyEvent)

```typescript
import { PropertyEvent } from 'leafer-ui'
```

| 事件 | 说明 |
|------|------|
| `PropertyEvent.BEFORE_CHANGE` | 属性变化前 |
| `PropertyEvent.CHANGE` | 属性变化 |

```typescript
element.on(PropertyEvent.CHANGE, (e) => {
    console.log('属性变化:', e.attrName, e.newValue)
})

// 监听特定属性
element.on(PropertyEvent.CHANGE, 'x', (e) => {
    console.log('x 变化:', e.newValue)
})
```

---

## 事件属性与方法

### 事件对象属性

```typescript
event.type          // 事件类型
event.target        // 事件目标元素
event.current       // 当前处理元素
event.bubbles       // 是否冒泡
event.cancelable    // 是否可取消

// 位置信息
event.x             // 相对于元素的位置 X
event.y             // 相对于元素的位置 Y
event.screenX       // 屏幕坐标 X
event.screenY       // 屏幕坐标 Y

// 原始事件
event.origin        // 原始 DOM 事件
```

### 事件方法

```typescript
event.stop()        // 停止传播（阻止冒泡和捕获）
event.stopPropagation()  // 阻止冒泡
event.preventDefault()   // 阻止默认行为
```

---

## 事件捕获与冒泡

```typescript
// 事件捕获阶段监听
parent.on(PointerEvent.TAP, listener, { capture: true })

// 事件冒泡阶段监听（默认）
parent.on(PointerEvent.TAP, listener)

// 停止冒泡
child.on(PointerEvent.TAP, (e) => {
    e.stopPropagation()
})
```

---

## 事件穿透

```typescript
// 设置元素不阻挡下方元素的事件
rect.hittable = false

// 子元素不阻挡父元素
parent.hitChildren = false
```

---

## 完整示例

### 拖拽排序

```typescript
import { Leafer, Rect, DragEvent, DropEvent, Group } from 'leafer-ui'

const leafer = new Leafer({ view: window })
const container = new Group()

const items = []
const colors = ['#ff6b6b', '#ffcd00', '#32cd79', '#4dabf7']

for (let i = 0; i < 4; i++) {
    const item = new Rect({
        y: i * 70,
        width: 200,
        height: 60,
        fill: colors[i],
        cornerRadius: 8,
        draggable: true,
        dropable: true
    })
    
    // 记录原始位置
    let startY = 0
    
    item.on(DragEvent.START, () => {
        startY = item.y
        item.scale = 1.05
        item.shadow = { x: 0, y: 4, blur: 8, color: '#00000030' }
    })
    
    item.on(DragEvent.DRAG, (e) => {
        item.y = startY + e.totalY
    })
    
    item.on(DragEvent.STOP, () => {
        item.scale = 1
        item.shadow = null
        
        // 重新排序
        items.sort((a, b) => a.y - b.y)
        items.forEach((it, index) => {
            it.animate({ y: index * 70 }, { duration: 0.3 })
        })
    })
    
    items.push(item)
    container.add(item)
}

leafer.add(container)
```

### 键盘快捷键

```typescript
import { App, Rect, KeyEvent } from 'leafer-ui'
import '@leafer-in/editor'

const app = new App({ view: window, editor: {} })

// 添加可编辑元素
for (let i = 0; i < 3; i++) {
    app.tree.add(new Rect({
        x: 100 + i * 150,
        y: 100,
        width: 100,
        height: 100,
        fill: '#32cd79',
        editable: true
    }))
}

// 键盘快捷键
app.on(KeyEvent.DOWN, (e) => {
    const editor = app.editor
    if (!editor?.element) return
    
    const selected = editor.element
    
    switch(e.code) {
        case 'Delete':
        case 'Backspace':
            selected.remove()
            editor.target = null
            break
            
        case 'KeyC':
            if (e.metaKey || e.ctrlKey) {
                // 复制
                const clone = selected.clone()
                clone.x += 20
                clone.y += 20
                app.tree.add(clone)
            }
            break
            
        case 'ArrowUp':
            selected.y -= e.shiftKey ? 10 : 1
            break
        case 'ArrowDown':
            selected.y += e.shiftKey ? 10 : 1
            break
        case 'ArrowLeft':
            selected.x -= e.shiftKey ? 10 : 1
            break
        case 'ArrowRight':
            selected.x += e.shiftKey ? 10 : 1
            break
    }
})
```

### 画布平移缩放

```typescript
import { App, Rect, MoveEvent, ZoomEvent } from 'leafer-ui'
import '@leafer-in/viewport'

const app = new App({
    view: window,
    move: { drag: true },
    wheel: { zoom: true }
})

// 显示当前视口状态
const statusText = new Text({
    x: 20, y: 20,
    text: '平移: 0, 0  缩放: 1',
    fill: '#333',
    fontSize: 14
})

app.sky.add(statusText)

// 监听平移
app.tree.on(MoveEvent.MOVE, () => {
    updateStatus()
})

// 监听缩放
app.tree.on(ZoomEvent.ZOOM, () => {
    updateStatus()
})

function updateStatus() {
    const transform = app.tree.transform
    statusText.text = `平移: ${Math.round(transform.x)}, ${Math.round(transform.y)}  缩放: ${transform.scaleX.toFixed(2)}`
}

// 添加内容
for (let i = 0; i < 10; i++) {
    for (let j = 0; j < 10; j++) {
        app.tree.add(new Rect({
            x: i * 120,
            y: j * 120,
            width: 100,
            height: 100,
            fill: `hsl(${(i + j) * 30}, 70%, 60%)`,
            cornerRadius: 8
        }))
    }
}
```
