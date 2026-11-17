# LeaferJS 框架集成指南

LeaferJS 支持多种前端框架集成。以下是各框架的详细集成方法。

---

## Vue 3 集成

### 基础集成

```vue
<template>
  <div id="leafer-view"></div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { Leafer, Rect } from 'leafer-ui'

let leafer: Leafer

onMounted(() => {
  leafer = new Leafer({ view: 'leafer-view' })
  
  const rect = new Rect({
    x: 100, y: 100,
    width: 200, height: 200,
    fill: '#32cd79',
    cornerRadius: [50, 80, 0, 80],
    draggable: true
  })
  
  leafer.add(rect)
})

onUnmounted(() => {
  leafer?.destroy()  // 必须销毁
})
</script>

<style scoped>
#leafer-view {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
```

### 完整封装组件

```vue
<!-- LeaferCanvas.vue -->
<template>
  <div ref="containerRef" class="leafer-container">
    <div id="leafer-view" class="leafer-view"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { Leafer, Rect, Group } from 'leafer-ui'
import type { IUIInputData } from 'leafer-ui'

interface Props {
  width?: number
  height?: number
  elements?: IUIInputData[]
  fill?: string
}

const props = withDefaults(defineProps<Props>(), {
  width: 800,
  height: 600,
  elements: () => [],
  fill: '#f5f5f5'
})

const emit = defineEmits<{
  ready: [leafer: Leafer]
  tap: [element: any]
}>()

const containerRef = ref<HTMLDivElement>()
let leafer: Leafer

onMounted(() => {
  leafer = new Leafer({
    view: 'leafer-view',
    width: props.width,
    height: props.height,
    fill: props.fill
  })
  
  // 添加初始元素
  props.elements.forEach(data => {
    leafer.add(new Rect(data))
  })
  
  emit('ready', leafer)
})

onUnmounted(() => {
  leafer?.destroy()
})

// 响应式更新元素
watch(() => props.elements, (newElements) => {
  if (!leafer) return
  
  leafer.removeAll()
  newElements.forEach(data => {
    leafer.add(new Rect(data))
  })
})
</script>

<style scoped>
.leafer-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.leafer-view {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
```

### 使用图形编辑器

```vue
<template>
  <div id="leafer-view"></div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { App, Rect } from 'leafer-ui'
import '@leafer-in/editor'
import '@leafer-in/viewport'

let app: App

onMounted(() => {
  app = new App({
    view: 'leafer-view',
    editor: {}
  })
  
  // 添加可编辑元素
  app.tree.add(Rect.one({
    editable: true,
    fill: '#32cd79',
    cornerRadius: 8
  }, 100, 100))
  
  app.tree.add(Rect.one({
    editable: true,
    fill: '#ffcd00',
    cornerRadius: 8
  }, 300, 100))
})

onUnmounted(() => {
  app?.destroy()
})
</script>

<style scoped>
#leafer-view {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
```

### 使用 Pinia 管理状态

```typescript
// stores/leafer.ts
import { defineStore } from 'pinia'
import { ref, shallowRef } from 'vue'
import { Leafer, Rect } from 'leafer-ui'

export const useLeaferStore = defineStore('leafer', () => {
  // 使用 shallowRef 避免深度代理
  const leafer = shallowRef<Leafer>()
  const elements = ref<any[]>([])
  
  function init(view: string | HTMLElement) {
    leafer.value = new Leafer({ view })
  }
  
  function addRect(data: any) {
    const rect = new Rect(data)
    leafer.value?.add(rect)
    elements.value.push(rect)
    return rect
  }
  
  function destroy() {
    leafer.value?.destroy()
    leafer.value = undefined
    elements.value = []
  }
  
  return {
    leafer,
    elements,
    init,
    addRect,
    destroy
  }
})
```

### Vue 注意事项

1. **不要使用响应式数据存储 leafer 实例**
   ```typescript
   // ❌ 错误
   const leafer = ref<Leafer>()
   
   // ✅ 正确
   let leafer: Leafer
   // 或使用 shallowRef
   const leafer = shallowRef<Leafer>()
   ```

2. **在 onUnmounted 中销毁**
   ```typescript
   onUnmounted(() => {
     leafer?.destroy()
   })
   ```

---

## React 集成

### 基础集成

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
      
      const rect = new Rect({
        x: 100, y: 100,
        width: 200, height: 200,
        fill: '#32cd79',
        cornerRadius: [50, 80, 0, 80],
        draggable: true
      })
      
      leaferRef.current.add(rect)
    })
    
    return () => {
      leaferRef.current?.destroy()
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

### 完整封装组件

```tsx
// components/LeaferCanvas.tsx
import { useEffect, useRef, useCallback } from 'react'
import { Leafer, Rect, App } from 'leafer-ui'

interface LeaferCanvasProps {
  width?: number
  height?: number
  mode?: 'leafer' | 'app'
  onReady?: (instance: Leafer | App) => void
}

export default function LeaferCanvas({
  width = 800,
  height = 600,
  mode = 'leafer',
  onReady
}: LeaferCanvasProps) {
  const instanceRef = useRef<Leafer | App | null>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    let isDestroy = false
    
    const init = async () => {
      const { Leafer, Rect, App } = await import('leafer-ui')
      
      if (isDestroy || !containerRef.current) return
      
      if (mode === 'app') {
        const { Editor } = await import('@leafer-in/editor')
        const { Viewport } = await import('@leafer-in/viewport')
        
        instanceRef.current = new App({
          view: containerRef.current,
          editor: {}
        })
      } else {
        instanceRef.current = new Leafer({
          view: containerRef.current,
          width,
          height
        })
      }
      
      onReady?.(instanceRef.current)
    }
    
    init()
    
    return () => {
      instanceRef.current?.destroy()
      isDestroy = true
    }
  }, [mode, width, height])

  return (
    <div 
      ref={containerRef}
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

### 使用 Hook

```typescript
// hooks/useLeafer.ts
import { useEffect, useRef, useCallback } from 'react'
import { Leafer } from 'leafer-ui'

export function useLeafer(view?: string | HTMLElement) {
  const leaferRef = useRef<Leafer | null>(null)
  const initializedRef = useRef(false)
  
  useEffect(() => {
    if (!view || initializedRef.current) return
    
    let isDestroy = false
    initializedRef.current = true
    
    const init = async () => {
      const { Leafer } = await import('leafer-ui')
      if (isDestroy) return
      
      leaferRef.current = new Leafer({ view })
    }
    
    init()
    
    return () => {
      leaferRef.current?.destroy()
      isDestroy = true
      initializedRef.current = false
    }
  }, [view])
  
  const add = useCallback((element: any) => {
    leaferRef.current?.add(element)
  }, [])
  
  return {
    leafer: leaferRef.current,
    add
  }
}
```

### React 注意事项

1. **异步加载 leafer-ui**
   ```tsx
   useEffect(() => {
     import('leafer-ui').then(({ Leafer }) => {
       // 初始化
     })
   }, [])
   ```

2. **处理开发环境 useEffect 执行两次**
   ```tsx
   useEffect(() => {
     let isDestroy = false
     
     // 初始化代码
     
     return () => {
       leafer?.destroy()
       isDestroy = true
     }
   }, [])
   ```

---

## Next.js 集成

### 客户端组件

```tsx
// components/LeaferView.tsx
'use client'

import { useEffect, useRef, useState } from 'react'

export default function LeaferView() {
  const leaferRef = useRef<any>(null)
  const [isReady, setIsReady] = useState(false)

  useEffect(() => {
    let isDestroy = false
    
    const init = async () => {
      const { Leafer, Rect } = await import('leafer-ui')
      
      if (isDestroy) return
      
      leaferRef.current = new Leafer({ view: 'leafer-view' })
      
      leaferRef.current.add(new Rect({
        x: 100, y: 100,
        width: 200, height: 200,
        fill: '#32cd79',
        draggable: true
      }))
      
      setIsReady(true)
    }
    
    init()
    
    return () => {
      leaferRef.current?.destroy()
      isDestroy = true
    }
  }, [])

  return (
    <div 
      id="leafer-view" 
      style={{ 
        width: '100%', 
        height: '100%',
        minHeight: '600px'
      }} 
    />
  )
}
```

### 在页面中使用

```tsx
// app/page.tsx
import LeaferView from './components/LeaferView'

export default function Home() {
  return (
    <main style={{ width: '100vw', height: '100vh' }}>
      <LeaferView />
    </main>
  )
}
```

### SSR 处理

```tsx
// components/DynamicLeafer.tsx
import dynamic from 'next/dynamic'

const LeaferView = dynamic(
  () => import('./LeaferView'),
  { 
    ssr: false,  // 禁用 SSR
    loading: () => <div>Loading...</div>
  }
)

export default function DynamicLeafer() {
  return <LeaferView />
}
```

### Next.js 配置

```javascript
// next.config.js
module.exports = {
  webpack: (config) => {
    // 处理 leafer-ui 的模块
    config.module.rules.push({
      test: /leafer-ui/,
      resolve: {
        fullySpecified: false
      }
    })
    return config
  }
}
```

---

## Nuxt 集成

### 客户端插件

```typescript
// plugins/leafer.client.ts
import { Leafer } from 'leafer-ui'

export default defineNuxtPlugin(() => {
  return {
    provide: {
      leafer: {
        create: (options: any) => new Leafer(options)
      }
    }
  }
})
```

### 组件中使用

```vue
<template>
  <div ref="leaferRef"></div>
</template>

<script setup lang="ts">
const leaferRef = ref<HTMLDivElement>()
let leafer: Leafer

onMounted(() => {
  const { $leafer } = useNuxtApp()
  
  leafer = $leafer.create({
    view: leaferRef.value
  })
  
  // 添加内容
  const { Rect } = await import('leafer-ui')
  leafer.add(new Rect({
    x: 100, y: 100,
    width: 200, height: 200,
    fill: '#32cd79'
  }))
})

onUnmounted(() => {
  leafer?.destroy()
})
</script>
```

### Nuxt 配置

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  build: {
    transpile: ['leafer-ui']
  },
  vite: {
    optimizeDeps: {
      include: ['leafer-ui']
    }
  }
})
```

---

## 框架通用最佳实践

### 1. 避免响应式代理

```typescript
// ❌ 错误 - Vue reactive
const state = reactive({
  leafer: new Leafer({ view: 'view' })
})

// ❌ 错误 - React state
const [leafer, setLeafer] = useState(new Leafer({ view: 'view' }))

// ✅ 正确
let leafer: Leafer
// Vue: const leafer = shallowRef<Leafer>()
// React: const leaferRef = useRef<Leafer>(null)
```

### 2. 异步加载

```typescript
// 在 useEffect / onMounted 中异步加载
useEffect(() => {
  import('leafer-ui').then(({ Leafer }) => {
    // 确保 canvas context 环境已准备好
    const leafer = new Leafer({ view: 'view' })
  })
}, [])
```

### 3. 及时销毁

```typescript
// Vue
onUnmounted(() => {
  leafer?.destroy()
})

// React
useEffect(() => {
  return () => {
    leaferRef.current?.destroy()
  }
}, [])
```

### 4. 类型支持

```typescript
// 安装类型支持
npm install -D @leafer-ui/interface

// 使用类型
import type { ILeafer, IRect } from '@leafer-ui/interface'

function initCanvas(leafer: ILeafer) {
  // ...
}
```

### 5. 服务端渲染处理

```typescript
// 只在客户端执行
if (typeof window !== 'undefined') {
  const { Leafer } = await import('leafer-ui')
  // ...
}

// 或使用框架的客户端标识
// Next.js: 'use client'
// Vue: <ClientOnly>
// Nuxt: .client.ts
```

---

## 完整示例：图形编辑器应用

### Vue 3 版本

```vue
<template>
  <div class="editor-container">
    <div class="toolbar">
      <button @click="addRect">添加矩形</button>
      <button @click="addCircle">添加圆形</button>
      <button @click="deleteSelected" :disabled="!hasSelection">删除</button>
      <button @click="exportImage">导出</button>
    </div>
    <div id="leafer-view" class="canvas"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { App, Rect, Ellipse } from 'leafer-ui'
import '@leafer-in/editor'
import '@leafer-in/viewport'
import '@leafer-in/export'

const app = ref<App>()
const hasSelection = ref(false)

onMounted(() => {
  app.value = new App({
    view: 'leafer-view',
    fill: '#f5f5f5',
    editor: {}
  })
  
  // 监听选择变化
  app.value.editor?.on('select', () => {
    hasSelection.value = app.value!.editor.list.length > 0
  })
})

onUnmounted(() => {
  app.value?.destroy()
})

function addRect() {
  app.value?.tree.add(Rect.one({
    editable: true,
    fill: '#32cd79',
    cornerRadius: 8
  }, 100 + Math.random() * 200, 100 + Math.random() * 200))
}

function addCircle() {
  app.value?.tree.add(Ellipse.one({
    editable: true,
    fill: '#ffcd00'
  }, 100 + Math.random() * 200, 100 + Math.random() * 200, 100, 100))
}

function deleteSelected() {
  app.value?.editor.list.forEach(item => item.remove())
  app.value!.editor.target = null
  hasSelection.value = false
}

async function exportImage() {
  const blob = await app.value?.tree.export('png')
  if (blob) {
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'canvas.png'
    a.click()
  }
}
</script>

<style scoped>
.editor-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.toolbar {
  padding: 16px;
  border-bottom: 1px solid #ddd;
  display: flex;
  gap: 8px;
}

.canvas {
  flex: 1;
  position: relative;
}

button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
}

button:hover:not(:disabled) {
  background: #f5f5f5;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
```
