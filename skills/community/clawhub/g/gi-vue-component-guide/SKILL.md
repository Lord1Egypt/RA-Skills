---
name: gi-vue-component-guide
description: Design and implement Vue 3 components following best practices. Use when creating Vue components, defining props/emits, or when the user asks for Vue component structure or composition API patterns.
tags: ["vue", "vue3", "component", "composition-api", "ant-design", "frontend"]
---

# Vue 3 组件规范

按团队规范设计与实现 Vue 3 组件，适用于 Composition API + Ant Design 技术栈。

## 何时使用

- 用户请求「写一个 Vue 组件」「设计组件结构」
- 定义 Props、Emits、Slots
- 使用 Composition API 组织逻辑
- 与 Ant Design 组件集成

## 项目结构

```
src/
├── components/     # 可复用组件
├── views/          # 页面级组件
├── router/
├── services/
├── stores/
├── types/
└── utils/
```

## 组件设计原则

### 1. 命名

- 组件文件：PascalCase，如 `UserCard.vue`、`DataTable.vue`
- 组件注册：与文件名一致
- Props：camelCase，如 `userName`、`isLoading`

### 2. 单文件结构顺序

```vue
<script setup lang="ts">
// 1. imports
// 2. props & emits 定义
// 3. 响应式状态
// 4. 计算属性
// 5. 方法
// 6. 生命周期 / watch
</script>

<template>
  <!-- 模板 -->
</template>

<style scoped>
/* 样式 */
</style>
```

### 3. Props 定义

```typescript
interface Props {
  /** 用户 ID */
  userId: number
  /** 是否加载中 */
  loading?: boolean
  /** 自定义类名 */
  class?: string
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})
```

- 必填项不加 `?`
- 提供默认值用 `withDefaults`
- 复杂类型从 `types/` 导入

### 4. Emits 定义

```typescript
const emit = defineEmits<{
  (e: 'update', value: string): void
  (e: 'submit', payload: { id: number; name: string }): void
}>()
```

### 5. 与 Ant Design 集成

- 表单：`a-form` + `a-form-item`，使用 `v-model` 或 `v-decorator`（视版本）
- 表格：`a-table`，columns 用 `defineColumns` 或常量
- 弹窗：`a-modal`，`v-model:open` 控制显隐
- 按钮：`a-button`，type 区分 primary/default/danger

### 6. 请求与状态

```typescript
// 从 services 调用 API
import { getUserList } from '@/services/user'

const loading = ref(false)
const data = ref<User[]>([])

async function fetchData() {
  loading.value = true
  try {
    data.value = await getUserList(params)
  } finally {
    loading.value = false
  }
}
```

### 7. 类型定义

- 组件 Props/Emits 的 payload 类型放在 `types/` 或组件同目录
- 使用 `interface` 或 `type`，避免 `any`

## 示例模板

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { User } from '@/types/user'

interface Props {
  title?: string
}
const props = withDefaults(defineProps<Props>(), { title: '默认标题' })

const emit = defineEmits<{ (e: 'confirm', id: number): void }>()

const list = ref<User[]>([])
const loading = ref(false)

onMounted(() => {
  // 初始化
})
</script>

<template>
  <div class="user-card">
    <a-spin :spinning="loading">
      <!-- 内容 -->
    </a-spin>
  </div>
</template>

<style scoped>
.user-card { /* ... */ }
</style>
```

## 常见模式

- **受控/非受控**：优先受控（v-model），必要时支持非受控
- **插槽**：默认 slot + 具名 slot（如 `header`、`footer`）
- **样式**：优先 `scoped`，避免污染；使用 CSS 变量统一主题
