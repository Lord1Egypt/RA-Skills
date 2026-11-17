---
name: leafer-js
description: |
  为 Claude 提供 LeaferJS Canvas 图形引擎的全面支持。
  
  当用户需要创建、开发或调试 LeaferJS 应用时，请立即使用此 Skill。
  
  LeaferJS 是一个现代化的 Canvas 引擎，专注于图形编辑、复杂 UI 构建和交互应用开发。
  支持瞬间创建100万个图形，性能卓越。
  
  适用于以下场景：
  - 创建图形编辑器（如 Figma、Canva 类工具）
  - 开发互动应用、小游戏
  - 构建可视化系统、数据大屏
  - 开发 AI 无限画布应用
  - 生成图片与短视频内容
  - 创建组态软件、工业监控
  
  当用户提到以下关键词时触发：LeaferJS、Leafer、Canvas 引擎、图形编辑、
  画布应用、可视化、图形交互、动画系统、UI 布局、图形编辑器
  
  即使用户没有明确说"Skill"，只要涉及 LeaferJS 相关开发，都应该使用此 Skill。
compatibility: |
  - 支持环境：Web、Web Worker、Node.js、微信小程序
  - 包管理器：npm、pnpm、yarn、bun
  - 框架集成：Vue、React、Next.js、Nuxt
  - TypeScript 完全支持
---

# LeaferJS 开发 Skill

## 核心能力

LeaferJS 是一款革新、好用的 Canvas 引擎，轻松实现专业图形编辑。

### 主要特点
- **超高性能**：瞬间创建100万个图形
- **完整图形编辑**：多选、框选、编组、变换、吸附等专业能力
- **强大动画系统**：CSS风格过渡、关键帧、路径动画、精灵帧
- **丰富交互系统**：手势识别、拖拽、缩放、旋转、事件捕获/冒泡
- **多端统一**：Web、Worker、Node.js、小程序一套 API
- **自动布局**：类似 Flex 的 Flow 布局系统

### 适用场景
1. **图形编辑应用**：在线画图、图片编辑器、设计工具、流程图、思维导图
2. **小游戏**：2D游戏、游戏UI、动画界面
3. **互动应用**：教育互动、可视化页面、产品演示、H5互动
4. **组态软件**：工业组态、监控大屏、设备拓扑
5. **图片/视频生成**：海报生成、AI图片生成、短视频封面

---

## 快速开始

### 安装

```bash
# 基础 UI 包（推荐，70KB min+gzip）
npm install leafer-ui

# 全量包（含所有插件）
npm install leafer
```

### 创建第一个应用

```typescript
import { Leafer, Rect } from 'leafer-ui'

const leafer = new Leafer({
    view: window,
    fill: '#333'
})

const rect = new Rect({
    x: 100,
    y: 100,
    width: 100,
    height: 100,
    fill: '#32cd79',
    draggable: true
})

leafer.add(rect)
```

### 使用 App 结构（推荐编辑器场景）

```typescript
import { App, Rect } from 'leafer-ui'
import '@leafer-in/editor'
import '@leafer-in/viewport'

const app = new App({
    view: window,
    editor: {}  // 自动创建 tree 层、sky 层、editor
})

app.tree.add(Rect.one({ 
    editable: true, 
    fill: '#32cd79' 
}, 100, 100))
```

---

## 运行环境配置

### Web 浏览器

**ES Module 导入（推荐）**:
```typescript
import { Leafer, Rect } from 'leafer-ui'
```

**CDN Script 引入**:
```html
<!-- 生产环境 -->
<script src="https://unpkg.com/leafer-ui@2.1.0/dist/web.min.js"></script>
<!-- 开发环境 -->
<script src="https://unpkg.com/leafer-ui@2.1.0/dist/web.js"></script>
<!-- ES Module -->
<script type="module">
  import { Leafer } from 'https://unpkg.com/leafer-ui@2.1.0/dist/web.module.min.js'
</script>

<script>
  const { Leafer, Rect } = LeaferUI
  // 注意：Image、PointerEvent、DragEvent 需使用别名
  const { MyImage, MyPointerEvent, MyDragEvent } = LeaferUI
</script>
```

### Vue 3 集成

```vue
<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { Leafer, Rect } from 'leafer-ui'

let leafer: Leafer

onMounted(() => {
  leafer = new Leafer({ view: 'leafer-view' })
  
  leafer.add(new Rect({
    x: 100, y: 100,
    width: 200, height: 200,
    fill: '#32cd79',
    draggable: true
  }))
})

onUnmounted(() => {
  leafer?.destroy()  // 必须销毁
})
</script>

<template>
  <div id="leafer-view"></div>
</template>

<style scoped>
#leafer-view {
  position: absolute;
  top: 0; left: 0;
  width: 100%;
  height: 100%;
}
</style>
```

**注意事项**：leafer 及元素不能直接挂载到响应式数据上，会造成内部层层代理，拖慢运行速度。

### React 集成

```tsx
import { useEffect, useRef } from 'react'
import { Leafer, Rect } from 'leafer-ui'

export default function LeaferCanvas() {
  const leaferRef = useRef<Leafer | null>(null)

  useEffect(() => {
    let isDestroy = false
    
    import('leafer-ui').then(({ Leafer, Rect }) => {
      if (isDestroy) return
      
      leaferRef.current = new Leafer({ view: 'leafer-view' })
      
      leaferRef.current.add(new Rect({
        x: 100, y: 100,
        width: 200, height: 200,
        fill: '#32cd79',
        draggable: true
      }))
    })

    return () => {
      leaferRef.current?.destroy()  // 必须销毁
      isDestroy = true
    }
  }, [])

  return (
    <div 
      id="leafer-view" 
      style={{ 
        position: 'absolute', 
        top: 0, left: 0, 
        width: '100%', 
        height: '100%' 
      }} 
    />
  )
}
```

### Next.js 集成

```tsx
'use client'  // 标识为客户端组件

import { useEffect, useRef, useState } from 'react'

export default function LeaferView() {
  const leaferRef = useRef<any>(null)
  
  useEffect(() => {
    let isDestroy = false
    
    import('leafer-ui').then(({ Leafer, Rect }) => {
      if (isDestroy) return
      
      leaferRef.current = new Leafer({ view: 'leafer-view' })
      
      leaferRef.current.add(new Rect({
        x: 100, y: 100,
        width: 200, height: 200,
        fill: '#32cd79',
        draggable: true
      }))
    })
    
    return () => {
      leaferRef.current?.destroy()
      isDestroy = true
    }
  }, [])

  return <div id="leafer-view" style={{ width: '100%', height: '100%' }} />
}
```

### Web Worker

```bash
npm install @leafer-ui/worker
```

```js
// main.js
const worker = new Worker('./worker.js')

worker.onmessage = (e) => {
  const image = new Image()
  image.src = e.data
  document.body.appendChild(image)
}
```

```js
// worker.js
importScripts('https://unpkg.com/@leafer-ui/worker@2.1.0/dist/worker.min.js')

const { Leafer, Rect } = LeaferUI

const leafer = new Leafer({ width: 800, height: 600 })
leafer.add(Rect.one({ fill: '#32cd79' }, 100, 100))

leafer.export('jpg').then((result) => {
  self.postMessage(result.data)
})
```

### Node.js 服务端

```bash
npm install @leafer-ui/node skia-canvas
```

```typescript
import { Leafer, Rect, useCanvas } from '@leafer-ui/node'
import skia from 'skia-canvas'

useCanvas('skia', skia)  // 必须

const leafer = new Leafer({ width: 800, height: 600 })
leafer.add(Rect.one({ fill: '#32cd79' }, 100, 100))

// 生成图片
const result = await leafer.export('png')
// result.data 是 base64 图片数据

// HTTP 服务示例
import http from 'http'

http.createServer(async (req, res) => {
  const leafer = new Leafer({ width: 800, height: 600 })
  leafer.add(Rect.one({ fill: '#32cd79' }, 100, 100))
  
  const result = await leafer.export('png')
  
  res.writeHead(200, { 'Content-Type': 'text/html' })
  res.write(`<img src="${result.data}" />`)
  res.end()
}).listen(3000)
```

### 微信小程序

```bash
npm install @leafer-ui/miniapp
```

```typescript
// index.ts
import { Leafer, Rect } from '@leafer-ui/miniapp'

Page({
  onReady() {
    const leafer = new Leafer({
      view: 'leafer',
      eventer: this
    })
    
    leafer.add(new Rect({
      x: 100, y: 100,
      width: 100, height: 100,
      fill: '#32cd79',
      draggable: true
    }))
  },
  receiveEvent() {}  // 约定接收交互事件的方法名
})
```

```xml
<!-- index.wxml -->
<canvas
  id="leafer"
  type="2d"
  catchtouchstart="receiveEvent"
  catchtouchmove="receiveEvent"
  catchtouchend="receiveEvent"
  catchtouchcancel="receiveEvent"
/>
```

```css
/* index.wxss */
page { height: 100%; }
#leafer { width: 100%; height: 100%; }
```

**小程序环境要求**：微信小程序基础库 >= 3.6.0

---

## 项目初始化

### 使用 create-leafer 命令行工具

```bash
# 创建 Vue + Leafer 项目
npm create leafer@latest my-vue-app -- --template vue

# 创建 React + Leafer 项目
npm create leafer@latest my-react-app -- --template react

# 创建纯 Leafer 项目
npm create leafer@latest my-app

# 使用 pnpm
pnpm create leafer@latest my-app

# 在现有项目中安装 Leafer
npm create leafer@latest -- --init
```

### 在现有项目中集成

```bash
# 安装基础包
npm install leafer-ui

# 安装插件（按需）
npm install @leafer-in/animate @leafer-in/editor @leafer-in/viewport

# 安装类型支持
npm install -D @types/node
```

---

## 项目结构

```
examples/       # 完整可运行示例代码
guide/          # 教程文档
reference/      # API 参考文档
plugin/         # 插件文档
src/            # TypeScript 源码（用于理解类结构）
```

### 关键文档位置

- **显示对象**：`reference/display/` - 所有图形元素
- **属性方法**：`reference/property/` - UI 属性和方法
- **事件类型**：`reference/event/` - 所有事件
- **插件中心**：`plugin/in/` - 官方插件使用文档
- **快速入门**：`guide/basic/` - 分步骤教程

---

## 核心概念

### 1. 显示对象层次

```
App
├── tree (Leafer) - 设计层，存放主要内容
│   ├── Group/Box/Frame - 容器
│   │   ├── Rect/Ellipse/Text/Image/Path - 图形元素
│   └── Editor - 编辑器
└── sky (Leafer) - 天空层，放置UI控件
```

**关键元素**：
- **App**：应用容器，管理多层结构
- **Leafer**：渲染层，可独立运行
- **Group**：基础容器
- **Box**：带背景的容器，支持 padding
- **Frame**：固定尺寸的容器，支持滚动
- **UI**：所有可视元素的基类

**图形元素**：
- **Rect**：矩形、圆角矩形
- **Ellipse**：椭圆、圆形
- **Line**：直线、带箭头
- **Polygon**：多边形
- **Star**：星形
- **Path**：路径
- **Pen**：画笔，自由绘制
- **Text**：文本
- **Image**：图片
- **SVG**：SVG 图形
- **Canvas**：Canvas 元素

### 2. 核心插件

**必需插件**（通过 `leafer` 全量包自动安装）：
- `@leafer-in/animate` - 动画系统
- `@leafer-in/editor` - 图形编辑器
- `@leafer-in/viewport` - 视口控制
- `@leafer-in/scroll` - 滚动条
- `@leafer-in/arrow` - 箭头
- `@leafer-in/html` - HTML 渲染
- `@leafer-in/state` - 交互状态
- `@leafer-in/flow` - 自动布局
- `@leafer-in/text-editor` - 文本编辑
- `@leafer-in/robot` - 游戏精灵
- `@leafer-in/find` - 查找
- `@leafer-in/filter` - 滤镜
- `@leafer-in/export` - 导出
- `@leafer-in/resize` - 调整大小
- `@leafer-in/color` - 颜色处理
- `@leafer-in/motion-path` - 路径动画
- `@leafer-in/scale-fixed` - 固定缩放
- `@leafer-in/corner` - 圆角
- `@leafer-in/bright` - 亮度

### 3. 坐标系统

- **世界坐标系 (World)**：全局绝对坐标
- **本地坐标系 (Local)**：相对于父元素
- **Box 坐标系**：相对于元素自身的包围盒
- **页面坐标系 (Page)**：考虑视口偏移

### 4. 事件系统

**UI 事件**：
- PointerEvent - 指针事件（DOWN, UP, TAP, MOVE, ENTER, LEAVE）
- DragEvent - 拖拽事件（START, DRAG, STOP）
- DropEvent - 放置事件
- SwipeEvent - 滑动手势
- MoveEvent - 移动事件
- ZoomEvent - 缩放事件
- RotateEvent - 旋转事件
- KeyEvent - 键盘事件

**生命周期事件**：
- LeaferEvent - 引擎生命周期（READY, VIEW_READY）
- RenderEvent - 渲染事件（START, END）
- LayoutEvent - 布局事件
- ResizeEvent - 尺寸变化
- WatchEvent - 数据监听

**编辑器事件**：
- EditorEvent - 选择变化
- EditorMoveEvent - 移动
- EditorScaleEvent - 缩放
- EditorRotateEvent - 旋转
- EditorSkewEvent - 倾斜
- EditorGroupEvent - 编组
- InnerEditorEvent - 内部编辑

**动画事件**：
- AnimateEvent - 动画事件（PLAY, UPDATE, COMPLETED）

---

## 详细参考文档

### [显示对象](references/display.md)
所有图形元素的完整参考，包括：
- 容器：App, Leafer, Group, Box, Frame
- 图形：Rect, Ellipse, Line, Polygon, Star, Path, Pen
- 媒体：Image, SVG, Canvas
- 文本：Text

### [插件系统](references/plugins.md)
所有官方插件的使用方法：
- 安装方式
- 配置选项
- 使用示例
- 事件监听

### [动画系统](references/animation.md)
完整的动画功能：
- 基础动画
- 关键帧动画
- 过渡动画
- 路径动画
- 摇摆循环

### [事件系统](references/events.md)
所有事件类型的详细说明：
- UI 交互事件
- 编辑器事件
- 动画事件
- 生命周期事件

### [样式系统](references/styles.md)
视觉样式完整参考：
- 填充（纯色、渐变、图案）
- 描边
- 阴影（外阴影、内阴影、Box阴影）
- 滤镜效果
- 混合模式

### [编辑器系统](references/editor.md)
图形编辑器完整指南：
- 配置与创建
- 选择与框选
- 变换操作
- 编组与解组
- 自定义编辑工具

### [框架集成](references/framework.md)
前端框架集成指南：
- Vue 3 - 组件封装、Pinia 状态管理、注意事项
- React - Hooks、异步加载、SSR 处理
- Next.js - 客户端组件、动态导入、配置优化
- Nuxt - 客户端插件、配置选项

### [运行环境](references/environment.md)
各运行环境配置：
- Web 浏览器 - CDN、ESM、响应式、高清屏适配
- Web Worker - 后台渲染、批量生成
- Node.js - 服务端渲染、HTTP 服务、Express 集成
- 微信小程序 - 基础用法、图形编辑器、性能优化

### [实用示例](references/examples.md)
实际应用场景示例：
- 图形编辑器 - 完整画板、流程图编辑器
- 小游戏 - 打砖块、贪吃蛇
- 数据可视化 - 柱状图、饼图
- 海报生成 - 社交媒体海报、证书生成器
- 思维导图、无限画布、图片编辑器

### [调试指南](references/debugging.md)
调试和性能优化：
- Debug 工具 - 调试级别、性能监控
- 性能测试 - 基准测试、内存分析
- 常见问题排查 - 画布不显示、事件不响应、动画问题
- 框架集成问题、渲染诊断、内存泄漏排查

### [自定义元素](references/custom.md)
创建自定义 UI 元素和扩展：
- 自定义 UI 基础 - 继承 UI 基类、装饰器
- 自定义容器 - 特殊布局、虚拟列表
- 自定义渲染 - 自定义绘制、离屏渲染
- 自定义插件 - 创建插件、缓动函数、编辑工具
- 扩展 Leafer 类、自定义事件

---

## 常用代码模式

### 创建可编辑的图形

```typescript
import { App, Rect } from 'leafer-ui'
import '@leafer-in/editor'

const app = new App({ view: window, editor: {} })

const rect = new Rect({
    width: 100,
    height: 100,
    fill: '#32cd79',
    editable: true  // 关键：使元素可被编辑
})

app.tree.add(rect)
```

### 添加动画

```typescript
import { Animate } from '@leafer-in/animate'

// 方式1：使用 Animate 类
new Animate(rect, 
    { x: 500, rotation: 360 },  // 目标状态
    { duration: 2, loop: true }  // 选项
)

// 方式2：使用 animate() 方法
rect.animate(
    { x: 500 },
    { duration: 2, easing: 'ease-out' }
)

// 方式3：使用 transition 属性
rect.transition = { duration: 0.5 }
rect.x = 500  // 自动动画
```

### 监听事件

```typescript
import { PointerEvent, DragEvent } from 'leafer-ui'

rect.on(PointerEvent.TAP, (e) => {
    console.log('点击了矩形')
})

rect.on(DragEvent.DRAG, (e) => {
    console.log('拖拽中:', e.x, e.y)
})
```

### 使用 Flow 自动布局

```typescript
import { Box } from 'leafer-ui'
import '@leafer-in/flow'

const container = new Box({
    flow: 'x',           // 水平排列
    gap: 10,             // 间距
    padding: 20,         // 内边距
    fill: '#333'
})

// 子元素自动排列
container.add(new Rect({ fill: 'red', width: 50, height: 50 }))
container.add(new Rect({ fill: 'blue', width: 50, height: 50 }))
```

### 状态样式

```typescript
import '@leafer-in/state'

const rect = new Rect({
    fill: '#32cd79',
    hoverStyle: { fill: '#ffcd00' },      // 悬停状态
    pressStyle: { fill: '#ff6b6b' },      // 按下状态
    selectedStyle: { stroke: '#0066ff' }  // 选中状态
})
```

### 导出图片

```typescript
import '@leafer-in/export'

// 导出整个画布
const blob = await app.tree.export('png')

// 导出指定元素
const blob2 = await rect.export('png', { 
    pixelRatio: 2  // 高分辨率
})
```

---

## 性能优化

### 创建大量图形

```typescript
import { Leafer, Rect, Debug } from 'leafer-ui'

const leafer = new Leafer({ view: window })

// 启用调试
Debug.enable = true
Debug.filter = 'RunTime'

const startTime = Date.now()

// 使用 addMany 批量添加
const rects = []
for (let i = 0; i < 100000; i++) {
    rects.push(new Rect({
        x: (i % 100) * 12,
        y: Math.floor(i / 100) * 12,
        width: 10, height: 10,
        fill: `hsl(${(i * 3) % 360}, 70%, 60%)`,
        draggable: true
    }))
}

leafer.addMany(rects)  // 批量添加，性能更好

console.log('创建10万个矩形用时：', Date.now() - startTime, '毫秒')
```

### 批量操作

```typescript
// 使用 set() 批量设置属性
rect.set({
    x: 100,
    y: 100,
    fill: '#ff0000'
})

// 避免频繁更新
rect.x = 100  // ❌ 触发渲染
rect.y = 100  // ❌ 触发渲染
rect.fill = 'red'  // ❌ 触发渲染

rect.set({ x: 100, y: 100, fill: 'red' })  // ✅ 只触发一次渲染
```

---

## 最佳实践

1. **性能优化**
   - 大量图形时使用 `leafer.addMany()` 批量添加
   - 避免频繁更新单个属性，使用 `set()` 批量设置
   - 使用 `visible: false` 隐藏而非销毁暂时不用的元素

2. **内存管理**
   - 及时销毁不再使用的元素 `element.destroy()`
   - 移除事件监听 `off()` 避免内存泄漏
   - Vue/React 组件卸载时必须调用 `leafer.destroy()`

3. **编辑器开发**
   - 使用 App 结构而非单独 Leafer
   - 设置 `editable: true` 使元素可被选择编辑
   - 使用 `app.tree` 添加主要内容，`app.sky` 添加 UI 控件

4. **动画性能**
   - 优先使用 CSS 风格 transition 属性
   - 复杂动画使用 `willReadFrequently` 优化
   - 使用 `Animate` 实例控制精细动画

5. **框架集成注意事项**
   - leafer 及元素不能直接挂载到响应式数据上
   - 异步加载 leafer-ui 确保 canvas context 环境
   - 开发环境 useEffect 会执行多次，必须及时销毁

---

## 学习路径

1. **入门**：阅读 `guide/basic/leafer.md` 快速入门教程
2. **进阶**：学习 `guide/basic/` 目录下的交互、动画、布局教程
3. **深入**：研究 `examples/` 中的完整示例代码
4. **精通**：查阅 `reference/` 和 `plugin/` 完整 API 文档

---

## 在线资源

- 官网：https://www.leaferjs.com
- 在线 Playground：https://www.leaferjs.com/playground/
- 在线示例：https://www.leaferjs.com/examples/
- GitHub：https://github.com/leaferjs/leafer-ui

---

## 注意事项

1. LeaferJS 可简称为 Leafer
2. 插件需要先安装再导入使用
3. 编辑器功能必须在 App 中使用
4. 版本号请使用 `2.1.0` 或最新版本
5. `view` 参数为 id 字符串时**不加** `#` 号
6. 浏览器要求：Chrome >= 51, Firefox >= 53, Safari >= 10, Edge >= 79, IE 不支持
