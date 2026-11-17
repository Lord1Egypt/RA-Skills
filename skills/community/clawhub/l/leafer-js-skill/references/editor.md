# LeaferJS 图形编辑器完整参考

LeaferJS 提供专业的图形编辑能力，支持多选、框选、变换、编组等操作。

---

## 基础配置

### 快速创建

```typescript
import { App, Rect } from 'leafer-ui'
import '@leafer-in/editor'
import '@leafer-in/viewport'

const app = new App({
    view: window,
    editor: {}  // 自动创建 tree 层、sky 层、editor
})

// 添加可编辑元素
app.tree.add(Rect.one({
    editable: true,    // 关键：使元素可被编辑
    fill: '#32cd79'
}, 100, 100))
```

### 访问编辑器

```typescript
// 通过 app.editor 访问
const editor = app.editor

// 检查是否可用
if (app.editor) {
    // 执行编辑操作
}
```

---

## Editor 配置选项

```typescript
const app = new App({
    view: window,
    editor: {
        // ========== 选择配置 ==========
        selector: true,              // 启用选择器（默认 true）
        select: 'press',             // 选择方式: 'press' | 'tap'
        multipleSelect: true,        // 允许多选（默认 true）
        boxSelect: true,             // 启用框选（默认 true）
        
        // ========== 编辑能力 ==========
        moveable: true,              // 可移动（默认 true）
        resizeable: true,            // 可调整大小（默认 true）
        rotateable: true,            // 可旋转（默认 true）
        skewable: true,              // 可倾斜（默认 true）
        
        // ========== 控制点样式 ==========
        stroke: '#32cd79',           // 编辑框描边色
        strokeWidth: 1,              // 编辑框描边宽度
        
        point: {                     // 顶点控制点
            width: 12,
            height: 12,
            fill: '#32cd79',
            stroke: 'white',
            strokeWidth: 2,
            cornerRadius: 2
        },
        
        middlePoint: {             // 边中点控制点
            width: 8,
            height: 8,
            fill: '#32cd79',
            stroke: 'white',
            strokeWidth: 2
        },
        
        rotatePoint: {             // 旋转控制点
            width: 16,
            height: 16,
            fill: '#32cd79',
            stroke: 'white',
            strokeWidth: 2
        },
        
        // 显示旋转控制点
        circle: {},  // 启用底部的旋转控制点
        
        // ========== 其他配置 ==========
        buttonsFixed: true,          // 按钮固定方位
        dimOthers: true,             // 淡化其他元素
        
        // 编辑大小方式
        editSize: 'scale'            // 'scale' | 'fontSize' | 'size'
    }
})
```

---

## Editor 属性

### 目标元素

```typescript
// 获取选中的元素
editor.target           // 当前选中的元素（单选）
editor.target           // 选中元素数组（多选）

// 选中列表
editor.list             // 选中元素数组（只读）
editor.leafList         // 选中元素列表对象（只读）

// 选中状态
editor.single           // 是否只选中了单个元素（只读）
editor.multiple         // 是否选中了多个元素（只读）
editor.editing          // 是否处于编辑状态（只读）
editor.innerEditing     // 是否处于内部编辑状态（只读）
```

### 变换元素

```typescript
// 代表元素
editor.element          // 选中元素的唯一代表（单选时为元素本身，多选时为模拟元素）

// 使用 element 进行变换操作
editor.move(10, 20)                          // 移动（增量）
editor.scaleOf('center', 1.1, 1.1)            // 围绕中心缩放
editor.rotateOf('center', 45)                 // 围绕中心旋转 45 度
editor.skewOf('center', 10, 0)              // 围绕中心倾斜
```

### 编辑器状态

```typescript
editor.visible          // 编辑器是否可见
editor.hittable         // 编辑器是否响应交互

dragging               // 是否正在拖拽
moving                 // 是否正在移动
resizing               // 是否正在调整大小
rotating               // 是否正在旋转
skewing                // 是否正在倾斜
gesturing              // 是否正在手势操作
```

---

## Editor 方法

### 选择操作

```typescript
// 选中元素
editor.select(element)
editor.select([element1, element2])   // 多选

// 取消选择
editor.cancel()

// 添加选中
editor.addItem(element)

// 移除选中
editor.removeItem(element)

// 判断是否选中
editor.hasItem(element)
```

### 编组操作

```typescript
// 编组
editor.group()

// 解组
editor.ungroup()

// 打开组（双击进入）
editor.openGroup()

// 关闭组（退出）
editor.closeGroup()

// 当前打开的组列表
editor.openedGroupList
```

### 层级操作

```typescript
// 移动到顶层
editor.toTop()

// 移动到底层
editor.toBottom()
```

### 锁定操作

```typescript
// 锁定
editor.lock()

// 解锁
editor.unlock()
```

### 变换操作（增量）

```typescript
// 移动
editor.move(10, 20)

// 围绕指定原点缩放
editor.scaleOf('center', 1.1, 1.1)
editor.scaleOf({ x: 100, y: 100 }, 1.1, 1.1)

// 围绕指定原点旋转
editor.rotateOf('center', 45)
editor.rotateOf({ x: 100, y: 100 }, 45)

// 围绕指定原点倾斜
editor.skewOf('center', 10, 0)

// 翻转
editor.flip('x')      // 水平翻转
editor.flip('y')      // 垂直翻转
```

### 内部编辑器

```typescript
// 打开内部编辑器
editor.openInnerEditor()

// 关闭内部编辑器
editor.closeInnerEditor()

// 获取内部编辑器实例
editor.getInnerEditor()
```

### 更新

```typescript
// 手动更新编辑器
editor.update()

// 更新编辑框位置
editor.updateEditBox()

// 获取编辑工具
editor.getEditTool()

// 更新编辑工具
editor.updateEditTool()
```

---

## Editor 事件

```typescript
import { EditorEvent, EditorMoveEvent, EditorScaleEvent } from '@leafer-in/editor'

// 选择事件
app.editor.on(EditorEvent.SELECT, (e) => {
    console.log('选中:', e.editor.list)
})

app.editor.on(EditorEvent.UNSELECT, (e) => {
    console.log('取消选择')
})

// 移动事件
app.editor.on(EditorMoveEvent.MOVE, (e) => {
    console.log('移动:', e.moveX, e.moveY)
})

// 缩放事件
app.editor.on(EditorScaleEvent.SCALE, (e) => {
    console.log('缩放:', e.scaleX, e.scaleY)
})

// 旋转事件
app.editor.on(EditorRotateEvent.ROTATE, (e) => {
    console.log('旋转:', e.rotation)
})

// 倾斜事件
app.editor.on(EditorSkewEvent.SKEW, (e) => {
    console.log('倾斜:', e.skewX, e.skewY)
})

// 编组事件
app.editor.on(EditorGroupEvent.GROUP, (e) => {
    console.log('编组:', e.group)
})

app.editor.on(EditorGroupEvent.UNGROUP, (e) => {
    console.log('解组')
})

// 内部编辑器事件
app.editor.on(InnerEditorEvent.OPEN, (e) => {
    console.log('打开内部编辑器')
})

app.editor.on(InnerEditorEvent.CLOSE, (e) => {
    console.log('关闭内部编辑器')
})
```

---

## 事件钩子

通过配置钩子函数可以在操作前修改数据：

```typescript
const app = new App({
    view: window,
    editor: {
        // 移动前钩子
        beforeMove(item, moveX, moveY) {
            // 限制移动范围
            const newX = item.x + moveX
            const newY = item.y + moveY
            
            if (newX < 0) return false
            if (newY < 0) return false
            if (newX > 800) return false
            if (newY > 600) return false
            
            return true  // 返回 true 继续操作
        },
        
        // 缩放前钩子
        beforeScale(item, scaleX, scaleY) {
            // 限制最小尺寸
            if (item.width * scaleX < 10) return false
            if (item.height * scaleY < 10) return false
            
            // 修改缩放值
            return { scaleX: Math.max(scaleX, 0.1), scaleY: Math.max(scaleY, 0.1) }
        },
        
        // 旋转前钩子
        beforeRotate(item, rotation) {
            // 限制旋转角度
            if (rotation > 360) rotation = rotation % 360
            return rotation
        },
        
        // 倾斜前钩子
        beforeSkew(item, skewX, skewY) {
            // 限制倾斜角度
            if (skewX > 45) skewX = 45
            return { skewX, skewY }
        }
    }
})
```

---

## 自定义编辑工具

### 注册编辑工具

```typescript
import { EditTool, registerEditTool } from '@leafer-in/editor'

// 自定义矩形编辑工具
class MyRectTool extends EditTool {
    // 工具类型
    get tag(): string {
        return 'Rect'
    }
    
    // 编辑时的行为
    onMove(e: EditorMoveEvent) {
        super.onMove(e)
        // 自定义移动逻辑
    }
    
    onScale(e: EditorScaleEvent) {
        super.onScale(e)
        // 自定义缩放逻辑
    }
}

// 注册工具
registerEditTool('Rect', MyRectTool)
```

### 自定义内部编辑器

```typescript
import { InnerEditor, registerInnerEditor } from '@leafer-in/editor'

// 自定义文本内部编辑器
class MyTextEditor extends InnerEditor {
    onOpen() {
        // 创建输入框
        this.input = document.createElement('textarea')
        // ...
    }
    
    onClose() {
        // 销毁输入框
        // ...
    }
}

// 注册
registerInnerEditor('Text', MyTextEditor)
```

---

## 按钮组

### 添加自定义按钮

```typescript
import { Box, PointerEvent } from 'leafer-ui'

// 创建按钮
const deleteBtn = Box.one({
    around: 'center',
    fill: '#ff6b6b',
    cornerRadius: 16,
    cursor: 'pointer',
    children: [{
        tag: 'Text',
        text: '删除',
        fill: 'white',
        padding: [6, 12]
    }]
})

// 添加到编辑器按钮组
app.editor.buttons.add(deleteBtn)

// 绑定事件
deleteBtn.on(PointerEvent.TAP, () => {
    // 删除选中元素
    app.editor.list.forEach(item => item.remove())
    app.editor.target = null
})
```

### 按钮配置

```typescript
const app = new App({
    view: window,
    editor: {
        buttonsFixed: true,        // 按钮固定方位（旋转时不跟随旋转）
        buttons: {
            around: 'bottom',       // 按钮组位置: 'top' | 'bottom' | 'left' | 'right'
            gap: 10                 // 按钮间距
        }
    }
})
```

---

## 完整示例

### 基础编辑器

```typescript
import { App, Rect, Ellipse, Text } from 'leafer-ui'
import '@leafer-in/editor'
import '@leafer-in/viewport'

const app = new App({
    view: window,
    fill: '#f5f5f5',
    editor: {
        stroke: '#0066ff',
        circle: {}  // 显示旋转控制点
    }
})

// 添加多种可编辑元素
app.tree.add(Rect.one({
    editable: true,
    fill: '#32cd79',
    cornerRadius: 8
}, 100, 100, 150, 100))

app.tree.add(Ellipse.one({
    editable: true,
    fill: '#ffcd00'
}, 350, 150, 100, 100))

app.tree.add(Text.one({
    text: '可编辑文本',
    fontSize: 24,
    fill: '#333',
    editable: true
}, 100, 250))

// 选中第一个元素
app.editor.select(app.tree.children[0])
```

### 带快捷键的编辑器

```typescript
import { App, Rect, KeyEvent } from 'leafer-ui'
import '@leafer-in/editor'

const app = new App({
    view: window,
    editor: {}
})

// 添加元素
for (let i = 0; i < 5; i++) {
    app.tree.add(new Rect({
        x: 100 + i * 150,
        y: 100,
        width: 100,
        height: 100,
        fill: '#32cd79',
        editable: true,
        cornerRadius: 8
    }))
}

// 键盘快捷键
app.on(KeyEvent.DOWN, (e) => {
    const editor = app.editor
    if (!editor?.element) return
    
    // Cmd/Ctrl + 按键
    if (e.metaKey || e.ctrlKey) {
        switch(e.code) {
            case 'KeyC':  // 复制
                const clone = editor.element.clone()
                clone.x += 20
                clone.y += 20
                app.tree.add(clone)
                editor.select(clone)
                break
                
            case 'KeyG':  // 编组/解组
                if (editor.multiple) {
                    editor.group()
                } else if (editor.element.tag === 'Group') {
                    editor.ungroup()
                }
                break
                
            case 'KeyA':  // 全选
                e.preventDefault()
                editor.select(app.tree.children)
                break
        }
    }
    
    // 单按键
    switch(e.code) {
        case 'Delete':
        case 'Backspace':
            // 删除选中元素
            editor.list.forEach(item => item.remove())
            editor.target = null
            break
            
        case 'ArrowUp':
            if (e.shiftKey) {
                editor.move(0, -10)
            } else {
                editor.move(0, -1)
            }
            break
        case 'ArrowDown':
            if (e.shiftKey) {
                editor.move(0, 10)
            } else {
                editor.move(0, 1)
            }
            break
        case 'ArrowLeft':
            if (e.shiftKey) {
                editor.move(-10, 0)
            } else {
                editor.move(-1, 0)
            }
            break
        case 'ArrowRight':
            if (e.shiftKey) {
                editor.move(10, 0)
            } else {
                editor.move(1, 0)
            }
            break
            
        case 'BracketRight':  // ]
            editor.toTop()
            break
        case 'BracketLeft':   // [
            editor.toBottom()
            break
    }
})
```

### 带属性面板的编辑器

```typescript
import { App, Rect, Box, Text, PointerEvent } from 'leafer-ui'
import '@leafer-in/editor'

const app = new App({
    view: window,
    editor: {}
})

// 侧边栏 - 显示选中元素属性
const sidebar = Box.one({
    x: 650, y: 20,
    width: 200,
    fill: 'white',
    cornerRadius: 8,
    shadow: { x: 0, y: 4, blur: 12, color: '#00000015' },
    padding: 16
})

const title = Text.one({
    text: '属性',
    fontSize: 16,
    fontWeight: 'bold',
    fill: '#333'
}, 0, 0)

const xText = Text.one({
    y: 30,
    fontSize: 14,
    fill: '#666'
}, 0, 0)

const yText = Text.one({
    y: 55,
    fontSize: 14,
    fill: '#666'
}, 0, 0)

const widthText = Text.one({
    y: 80,
    fontSize: 14,
    fill: '#666'
}, 0, 0)

const heightText = Text.one({
    y: 105,
    fontSize: 14,
    fill: '#666'
}, 0, 0)

sidebar.add(title)
sidebar.add(xText)
sidebar.add(yText)
sidebar.add(widthText)
sidebar.add(heightText)
app.sky.add(sidebar)

// 监听选择变化
app.editor.on(EditorEvent.SELECT, updatePanel)
app.editor.on(EditorMoveEvent.MOVE, updatePanel)
app.editor.on(EditorScaleEvent.SCALE, updatePanel)

function updatePanel() {
    const el = app.editor?.element
    if (el) {
        xText.text = `X: ${Math.round(el.x)}`
        yText.text = `Y: ${Math.round(el.y)}`
        widthText.text = `宽度: ${Math.round(el.width)}`
        heightText.text = `高度: ${Math.round(el.height)}`
    } else {
        xText.text = 'X: -'
        yText.text = 'Y: -'
        widthText.text = '宽度: -'
        heightText.text = '高度: -'
    }
}

// 添加示例元素
app.tree.add(new Rect({
    x: 100, y: 100,
    width: 150, height: 100,
    fill: '#32cd79',
    editable: true,
    cornerRadius: 8
}))
```

### 限制编辑区域

```typescript
import { App, Rect, Frame } from 'leafer-ui'
import '@leafer-in/editor'
import '@leafer-in/viewport'

const app = new App({
    view: window,
    editor: {
        // 限制在父容器内移动
        beforeMove(item, moveX, moveY) {
            const parent = item.parent
            if (!parent) return true
            
            const newX = item.x + moveX
            const newY = item.y + moveY
            
            // 限制在 Frame 内
            if (newX < 0) return false
            if (newY < 0) return false
            if (newX + item.width > parent.width) return false
            if (newY + item.height > parent.height) return false
            
            return true
        },
        
        // 限制最小尺寸
        beforeScale(item, scaleX, scaleY) {
            if (item.width * scaleX < 50) return false
            if (item.height * scaleY < 50) return false
            return true
        }
    }
})

// 创建编辑区域
const frame = new Frame({
    x: 50, y: 50,
    width: 500, height: 400,
    fill: '#f5f5f5',
    stroke: '#ddd'
})

frame.add(new Rect({
    x: 50, y: 50,
    width: 150, height: 100,
    fill: '#32cd79',
    editable: true
}))

app.tree.add(frame)
```

### 移动端手势编辑

```typescript
import { App, Rect, Frame } from 'leafer-ui'
import '@leafer-in/editor'
import '@leafer-in/viewport'

const app = new App({
    view: window,
    fill: '#333',
    mobile: true,  // 启用移动端支持
    editor: {
        // 手势控制
        moveable: 'gesture',      // 移动：手势
        resizeable: 'gesture',    // 缩放：手势
        rotateable: 'gesture'     // 旋转：手势
    }
})

// 添加编辑内容
const content = Frame.one({
    children: [
        Rect.one({
            editable: true,
            fill: '#FEB027',
            cornerRadius: [20, 0, 0, 20]
        }, 100, 100),
        Rect.one({
            editable: true,
            fill: '#FFE04B',
            cornerRadius: [0, 20, 20, 0]
        }, 300, 100)
    ]
}, 50, 50, 500, 400)

app.tree.add(content)
```

### 绘制模式

```typescript
import { App, DragEvent, Rect } from 'leafer-ui'
import '@leafer-in/editor'

const app = new App({
    view: window,
    editor: {}
})

// 添加几个示例元素
app.tree.add(Rect.one({ editable: true, fill: '#32cd79' }, 100, 300, 100, 100))

// 进入绘制模式
function enterDrawMode() {
    app.mode = 'draw'
    
    let rect: Rect
    
    const events = [
        app.on_(DragEvent.START, () => {
            rect = new Rect({ fill: '#32cd79', editable: true })
            app.tree.add(rect)
        }),
        
        app.on_(DragEvent.DRAG, (e: DragEvent) => {
            if (rect) rect.set(e.getPageBounds())
        })
    ]
    
    // 5秒后退出绘制模式
    setTimeout(() => {
        app.off_(events)
        app.mode = 'normal'
    }, 5000)
}

// 按钮触发绘制模式
const drawBtn = Rect.one({
    fill: '#0066ff',
    cornerRadius: 4,
    cursor: 'pointer'
}, 20, 20, 80, 32)

drawBtn.add(Text.one({
    text: '绘制',
    fill: 'white',
    x: 'center',
    y: 'center'
}))

app.tree.add(drawBtn)
drawBtn.on(PointerEvent.TAP, enterDrawMode)
```
