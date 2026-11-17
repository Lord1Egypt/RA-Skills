# LeaferJS 运行环境配置指南

LeaferJS 支持多种运行环境，包括 Web 浏览器、Web Worker、Node.js 服务端和微信小程序。

---

## Web 浏览器

### 现代浏览器支持

| 浏览器 | 最低版本 | 备注 |
|--------|----------|------|
| Chrome | >= 51 | 完全支持 |
| Firefox | >= 53 | 完全支持 |
| Safari | >= 10 | 完全支持 |
| Edge | >= 79 | 完全支持 |
| IE | 不支持 | 请使用现代浏览器 |

### ES Module 导入（推荐）

```typescript
import { Leafer, Rect } from 'leafer-ui'

const leafer = new Leafer({
    view: window,
    fill: '#f5f5f5'
})

leafer.add(new Rect({
    x: 100, y: 100,
    width: 200, height: 200,
    fill: '#32cd79'
}))
```

### CDN Script 引入

**生产环境（压缩版）：**
```html
<script src="https://unpkg.com/leafer-ui@2.1.0/dist/web.min.js"></script>
<script>
    const { Leafer, Rect } = LeaferUI
    
    const leafer = new Leafer({
        view: window,
        fill: '#f5f5f5'
    })
    
    leafer.add(new Rect({
        x: 100, y: 100,
        width: 200, height: 200,
        fill: '#32cd79'
    }))
</script>
```

**开发环境（完整版）：**
```html
<script src="https://unpkg.com/leafer-ui@2.1.0/dist/web.js"></script>
```

**ES Module CDN：**
```html
<script type="module">
    import { Leafer, Rect } from 'https://unpkg.com/leafer-ui@2.1.0/dist/web.module.min.js'
    
    const leafer = new Leafer({
        view: window,
        fill: '#f5f5f5'
    })
    
    leafer.add(new Rect({
        x: 100, y: 100,
        width: 200, height: 200,
        fill: '#32cd79'
    }))
</script>
```

### 命名冲突处理

当使用 CDN 方式时，以下全局对象可能与浏览器原生对象冲突，需要使用别名：

```html
<script src="https://unpkg.com/leafer-ui@2.1.0/dist/web.min.js"></script>
<script>
    const { 
        Leafer, 
        Rect,
        Image: LeaferImage,        // 别名避免冲突
        PointerEvent: LeaferPointerEvent,
        DragEvent: LeaferDragEvent
    } = LeaferUI
</script>
```

### 视口配置

```typescript
// 全屏模式
const leafer = new Leafer({
    view: window,  // 自动适应窗口大小
    fill: '#f5f5f5'
})

// 指定容器（id 字符串，不加 #）
const leafer = new Leafer({
    view: 'leafer-container',
    width: 800,
    height: 600
})

// 指定 DOM 元素
const container = document.getElementById('leafer-container')
const leafer = new Leafer({
    view: container,
    width: 800,
    height: 600
})
```

### 响应式画布

```typescript
import { Leafer, Rect, ResizeEvent } from 'leafer-ui'

const leafer = new Leafer({
    view: window,
    fill: '#f5f5f5',
    width: window.innerWidth,
    height: window.innerHeight
})

// 监听窗口大小变化
window.addEventListener('resize', () => {
    leafer.resize({
        width: window.innerWidth,
        height: window.innerHeight
    })
})

// 或使用 ResizeEvent
leafer.on(ResizeEvent.RESIZE, (e) => {
    console.log('画布大小改变:', e.width, e.height)
})
```

### 高清屏适配（DPR）

```typescript
const leafer = new Leafer({
    view: window,
    fill: '#f5f5f5',
    pixelRatio: window.devicePixelRatio || 1  // 自动适配高清屏
})

// 固定像素比（性能优先）
const leafer = new Leafer({
    view: window,
    pixelRatio: 1  // 固定为 1，减少渲染开销
})

// 导出时提高像素比
const blob = await leafer.export('png', { pixelRatio: 2 })
```

### 触摸设备优化

```typescript
const app = new App({
    view: window,
    fill: '#f5f5f5',
    mobile: true,  // 启用移动端优化
    editor: {
        moveable: 'gesture',     // 手势移动
        resizeable: 'gesture',   // 手势缩放
        rotateable: 'gesture'    // 手势旋转
    }
})
```

---

## Web Worker

在 Web Worker 中使用 LeaferJS 进行后台图形渲染，避免阻塞主线程。

### 安装

```bash
npm install @leafer-ui/worker
```

### Worker 线程

```typescript
// worker.ts
importScripts('https://unpkg.com/@leafer-ui/worker@2.1.0/dist/worker.min.js')

const { Leafer, Rect, Text } = LeaferUI

// 创建离屏画布
const leafer = new Leafer({
    width: 800,
    height: 600
})

// 添加内容
leafer.add(Rect.one({
    x: 100, y: 100,
    width: 200, height: 200,
    fill: '#32cd79'
}))

leafer.add(Text.one({
    text: 'Worker 渲染',
    fontSize: 24,
    fill: '#333'
}, 100, 50))

// 导出图片并发送给主线程
leafer.export('png').then((result) => {
    self.postMessage({
        type: 'image',
        data: result.data  // base64 图片数据
    })
})

// 监听主线程消息
self.onmessage = (e) => {
    switch(e.data.type) {
        case 'addRect':
            leafer.add(new Rect(e.data.props))
            break
        case 'export':
            leafer.export(e.data.format || 'png').then((result) => {
                self.postMessage({ type: 'exported', data: result.data })
            })
            break
    }
}
```

### 主线程

```typescript
// main.ts
const worker = new Worker('./worker.js')

// 接收 Worker 消息
worker.onmessage = (e) => {
    if (e.data.type === 'image') {
        const img = new Image()
        img.src = e.data.data
        document.body.appendChild(img)
    }
}

// 向 Worker 发送指令
worker.postMessage({
    type: 'addRect',
    props: {
        x: 300, y: 100,
        width: 150, height: 100,
        fill: '#ffcd00'
    }
})

worker.postMessage({ type: 'export', format: 'jpg' })
```

### 批量生成图片

```typescript
// image-generator.worker.ts
importScripts('https://unpkg.com/@leafer-ui/worker@2.1.0/dist/worker.min.js')

const { Leafer, Rect, Text } = LeaferUI

self.onmessage = async (e) => {
    const { items } = e.data
    const results = []
    
    for (const item of items) {
        const leafer = new Leafer({
            width: item.width,
            height: item.height
        })
        
        // 添加背景
        leafer.add(new Rect({
            width: item.width,
            height: item.height,
            fill: item.bgColor || '#fff'
        }))
        
        // 添加内容
        leafer.add(new Text({
            text: item.text,
            fontSize: 32,
            fill: '#333',
            x: item.width / 2,
            y: item.height / 2,
            textAlign: 'center'
        }))
        
        // 导出
        const result = await leafer.export('png')
        results.push({
            id: item.id,
            data: result.data
        })
        
        // 清理
        leafer.destroy()
    }
    
    self.postMessage({ type: 'batchComplete', results })
}
```

---

## Node.js 服务端

在 Node.js 中使用 LeaferJS 生成图片、PDF 等。

### 安装

```bash
npm install @leafer-ui/node skia-canvas
```

### 基础使用

```typescript
import { Leafer, Rect, Text, useCanvas } from '@leafer-ui/node'
import skia from 'skia-canvas'

// 必须：注册 Canvas 实现
useCanvas('skia', skia)

async function generateImage() {
    const leafer = new Leafer({
        width: 800,
        height: 600
    })
    
    // 添加图形
    leafer.add(new Rect({
        x: 100, y: 100,
        width: 200, height: 200,
        fill: '#32cd79',
        cornerRadius: 16
    }))
    
    leafer.add(new Text({
        text: 'Hello Node.js!',
        fontSize: 32,
        fill: '#333',
        x: 100, y: 50
    }))
    
    // 导出图片
    const result = await leafer.export('png')
    
    // 保存到文件
    const fs = await import('fs')
    fs.writeFileSync('output.png', result.data, 'base64')
    
    // 清理
    leafer.destroy()
    
    return result.data
}

generateImage()
```

### HTTP 服务

```typescript
import { Leafer, Rect, Text, useCanvas } from '@leafer-ui/node'
import skia from 'skia-canvas'
import http from 'http'

useCanvas('skia', skia)

const server = http.createServer(async (req, res) => {
    const url = new URL(req.url || '', `http://${req.headers.host}`)
    
    if (url.pathname === '/generate') {
        const width = parseInt(url.searchParams.get('width') || '800')
        const height = parseInt(url.searchParams.get('height') || '600')
        const text = url.searchParams.get('text') || 'Hello'
        
        const leafer = new Leafer({ width, height })
        
        // 创建卡片
        leafer.add(new Rect({
            width, height,
            fill: '#f5f5f5'
        }))
        
        leafer.add(new Rect({
            x: 20, y: 20,
            width: width - 40,
            height: height - 40,
            fill: '#fff',
            cornerRadius: 16,
            shadow: { x: 0, y: 4, blur: 12, color: '#00000015' }
        }))
        
        leafer.add(new Text({
            text,
            fontSize: 48,
            fill: '#333',
            x: width / 2,
            y: height / 2,
            textAlign: 'center'
        }))
        
        const result = await leafer.export('png')
        
        res.writeHead(200, {
            'Content-Type': 'image/png',
            'Content-Length': Buffer.byteLength(result.data, 'base64')
        })
        res.end(Buffer.from(result.data, 'base64'))
        
        leafer.destroy()
    } else {
        res.writeHead(404)
        res.end('Not Found')
    }
})

server.listen(3000, () => {
    console.log('Server running at http://localhost:3000')
})
```

### Express 集成

```typescript
import express from 'express'
import { Leafer, Rect, Text, useCanvas } from '@leafer-ui/node'
import skia from 'skia-canvas'

useCanvas('skia', skia)

const app = express()

// 生成海报 API
app.get('/poster', async (req, res) => {
    const { title = '标题', content = '内容' } = req.query
    
    const leafer = new Leafer({
        width: 800,
        height: 1000
    })
    
    // 背景
    leafer.add(new Rect({
        width: 800,
        height: 1000,
        fill: '#fff'
    }))
    
    // 标题
    leafer.add(new Text({
        text: title as string,
        fontSize: 48,
        fontWeight: 'bold',
        fill: '#333',
        x: 40, y: 60
    }))
    
    // 内容
    leafer.add(new Text({
        text: content as string,
        fontSize: 24,
        fill: '#666',
        x: 40, y: 140
    }))
    
    const result = await leafer.export('png')
    
    res.set('Content-Type', 'image/png')
    res.send(Buffer.from(result.data, 'base64'))
    
    leafer.destroy()
})

app.listen(3000)
```

### 批量生成缩略图

```typescript
import { Leafer, Rect, useCanvas } from '@leafer-ui/node'
import skia from 'skia-canvas'
import fs from 'fs'
import path from 'path'

useCanvas('skia', skia)

async function generateThumbnails(inputDir: string, outputDir: string) {
    const files = fs.readdirSync(inputDir)
    
    for (const file of files) {
        if (!file.endsWith('.png')) continue
        
        const leafer = new Leafer({
            width: 200,
            height: 200
        })
        
        // 读取原图并创建缩略图
        const imageData = fs.readFileSync(path.join(inputDir, file))
        const base64 = imageData.toString('base64')
        
        leafer.add(new Rect({
            width: 200,
            height: 200,
            fill: { type: 'image', url: `data:image/png;base64,${base64}` }
        }))
        
        const result = await leafer.export('jpg', { quality: 0.8 })
        
        const outputName = file.replace('.png', '_thumb.jpg')
        fs.writeFileSync(
            path.join(outputDir, outputName),
            result.data,
            'base64'
        )
        
        leafer.destroy()
    }
}
```

### PDF 导出

```typescript
import { Leafer, Rect, Text, useCanvas } from '@leafer-ui/node'
import skia from 'skia-canvas'

useCanvas('skia', skia)

async function generatePDF() {
    const leafer = new Leafer({
        width: 595,   // A4 宽度 (72 DPI)
        height: 842   // A4 高度
    })
    
    // 添加内容
    leafer.add(new Rect({
        width: 595, height: 842,
        fill: '#fff'
    }))
    
    leafer.add(new Text({
        text: 'PDF 文档',
        fontSize: 36,
        fill: '#333',
        x: 50, y: 50
    }))
    
    // 导出 PDF
    const result = await leafer.export('pdf')
    
    const fs = await import('fs')
    fs.writeFileSync('document.pdf', result.data, 'base64')
    
    leafer.destroy()
}
```

---

## 微信小程序

### 环境要求

- 微信小程序基础库 >= 3.6.0
- 启用 npm 支持

### 安装

```bash
npm install @leafer-ui/miniapp
```

### 基础用法

```typescript
// pages/index/index.ts
import { Leafer, Rect } from '@leafer-ui/miniapp'

Page({
    data: {
        canvasReady: false
    },
    
    onReady() {
        // 获取 Canvas 上下文
        const query = wx.createSelectorQuery()
        query.select('#leafer')
            .fields({ node: true, size: true })
            .exec((res) => {
                const canvas = res[0].node
                
                // 创建 Leafer 实例
                const leafer = new Leafer({
                    view: canvas,
                    width: res[0].width,
                    height: res[0].height
                })
                
                // 添加矩形
                leafer.add(new Rect({
                    x: 100, y: 100,
                    width: 100, height: 100,
                    fill: '#32cd79',
                    draggable: true
                }))
                
                this.leafer = leafer
            })
    },
    
    // 接收交互事件（约定方法名）
    receiveEvent(e: any) {
        // 事件会自动转发到 Leafer
    }
})
```

```xml
<!-- pages/index/index.wxml -->
<canvas
    id="leafer"
    type="2d"
    class="leafer-canvas"
    catchtouchstart="receiveEvent"
    catchtouchmove="receiveEvent"
    catchtouchend="receiveEvent"
    catchtouchcancel="receiveEvent"
/>
```

```css
/* pages/index/index.wxss */
page {
    height: 100%;
}

.leafer-canvas {
    width: 100%;
    height: 100%;
}
```

### 使用事件转发（推荐）

```typescript
// pages/index/index.ts
import { Leafer, Rect } from '@leafer-ui/miniapp'
import { PointerEvent } from 'leafer-ui'

Page({
    leafer: null as Leafer | null,
    
    onReady() {
        const query = wx.createSelectorQuery()
        query.select('#leafer')
            .fields({ node: true, size: true })
            .exec((res) => {
                const canvas = res[0].node
                
                this.leafer = new Leafer({
                    view: canvas,
                    width: res[0].width,
                    height: res[0].height,
                    eventer: this  // 绑定事件转发
                })
                
                const rect = new Rect({
                    x: 100, y: 100,
                    width: 100, height: 100,
                    fill: '#32cd79',
                    draggable: true
                })
                
                rect.on(PointerEvent.TAP, () => {
                    console.log('矩形被点击')
                    wx.showToast({ title: '点击了矩形' })
                })
                
                this.leafer.add(rect)
            })
    },
    
    // 约定的事件接收方法
    receiveEvent(e: any) {
        // Leafer 会自动处理
    },
    
    onUnload() {
        this.leafer?.destroy()
    }
})
```

### 图形编辑器

```typescript
// pages/editor/editor.ts
import { App, Rect } from '@leafer-ui/miniapp'
import '@leafer-ui/miniapp/editor'

Page({
    app: null as any,
    
    onReady() {
        const query = wx.createSelectorQuery()
        query.select('#editor')
            .fields({ node: true, size: true })
            .exec((res) => {
                const canvas = res[0].node
                
                this.app = new App({
                    view: canvas,
                    width: res[0].width,
                    height: res[0].height,
                    editor: {},
                    eventer: this
                })
                
                // 添加可编辑元素
                this.app.tree.add(Rect.one({
                    editable: true,
                    fill: '#32cd79',
                    cornerRadius: 8
                }, 100, 100))
            })
    },
    
    receiveEvent(e: any) {
        // 处理交互事件
    },
    
    // 添加矩形
    addRect() {
        this.app?.tree.add(Rect.one({
            editable: true,
            fill: '#ffcd00',
            cornerRadius: 8
        }, 100 + Math.random() * 200, 100 + Math.random() * 200))
    },
    
    // 删除选中
    deleteSelected() {
        const selected = this.app?.editor?.list
        if (selected) {
            selected.forEach((item: any) => item.remove())
            this.app.editor.target = null
        }
    },
    
    onUnload() {
        this.app?.destroy()
    }
})
```

```xml
<!-- pages/editor/editor.wxml -->
<view class="container">
    <view class="toolbar">
        <button size="mini" bindtap="addRect">添加矩形</button>
        <button size="mini" bindtap="deleteSelected">删除</button>
    </view>
    <canvas
        id="editor"
        type="2d"
        class="editor-canvas"
        catchtouchstart="receiveEvent"
        catchtouchmove="receiveEvent"
        catchtouchend="receiveEvent"
        catchtouchcancel="receiveEvent"
    />
</view>
```

```css
/* pages/editor/editor.wxss */
.container {
    display: flex;
    flex-direction: column;
    height: 100vh;
}

.toolbar {
    padding: 16rpx;
    background: #f5f5f5;
    display: flex;
    gap: 16rpx;
}

.editor-canvas {
    flex: 1;
    width: 100%;
}
```

### 小程序性能优化

```typescript
// 使用离屏 Canvas 提升性能
Page({
    onReady() {
        // 创建离屏 Canvas
        const offscreenCanvas = wx.createOffscreenCanvas({
            type: '2d',
            width: 800,
            height: 600
        })
        
        // 在离屏 Canvas 上绘制
        const leafer = new Leafer({
            view: offscreenCanvas,
            width: 800,
            height: 600
        })
        
        // 绘制完成后绘制到主 Canvas
        const query = wx.createSelectorQuery()
        query.select('#main')
            .fields({ node: true })
            .exec((res) => {
                const mainCanvas = res[0].node
                const ctx = mainCanvas.getContext('2d')
                
                // 将离屏内容绘制到主画布
                ctx.drawImage(offscreenCanvas, 0, 0)
            })
    }
})
```

---

## 各环境通用配置

### TypeScript 类型支持

```bash
npm install -D @leafer-ui/interface
```

```typescript
import type { ILeafer, IRect, IApp } from '@leafer-ui/interface'

function initCanvas(leafer: ILeafer) {
    // 使用类型定义
}
```

### 环境检测

```typescript
// 检测运行环境
const isWeb = typeof window !== 'undefined'
const isNode = typeof process !== 'undefined' && process.versions?.node
const isWorker = typeof importScripts === 'function'
const isMiniApp = typeof wx !== 'undefined' && wx.getSystemInfoSync

// 条件导入
async function initLeafer() {
    if (isNode) {
        const { Leafer } = await import('@leafer-ui/node')
        return Leafer
    } else if (isMiniApp) {
        const { Leafer } = await import('@leafer-ui/miniapp')
        return Leafer
    } else {
        const { Leafer } = await import('leafer-ui')
        return Leafer
    }
}
```

### 内存管理

```typescript
// 及时销毁实例
function cleanup(leafer: Leafer) {
    // 移除所有元素
    leafer.removeAll()
    
    // 移除事件监听
    leafer.off()
    
    // 销毁实例
    leafer.destroy()
}

// 元素池复用
class ElementPool {
    private pool: Rect[] = []
    
    get() {
        return this.pool.pop() || new Rect()
    }
    
    release(rect: Rect) {
        rect.remove()
        this.pool.push(rect)
    }
}
```

---

## 最佳实践

1. **Web 环境**
   - 使用 ES Module 导入以获得更好的 Tree Shaking
   - 根据场景选择合适的像素比
   - 使用 `willReadFrequently` 优化频繁读取

2. **Worker 环境**
   - 适合批量图片生成
   - 主线程和 Worker 之间只传递必要数据
   - 及时释放不再使用的 Leafer 实例

3. **Node.js 环境**
   - 必须调用 `useCanvas()` 注册 Canvas 实现
   - 服务端生成图片后及时清理内存
   - 使用流式处理大批量任务

4. **小程序环境**
   - 使用 `type="2d"` Canvas
   - 正确设置 `eventer` 接收交互事件
   - 页面卸载时调用 `destroy()`
