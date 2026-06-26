# 标准布局模板（MainLayout）

所有原型工程都必须包含此布局。使用 Arco Design 原生组件，整体背景色为 `var(--color-fill-2)`。

## 布局结构

```
┌─────────────────────────────────────────────────────┐
│  Header (48px)  背景: color-fill-2                  │
│  [平台名]  [Tab][Tab][Tab]              [头像]       │
├──────────┬──────────────────────────────────────────┤
│  Sider   │  Content Area                            │
│  (200px) │  背景: color-bg-white                    │
│  背景:   │  border-radius: 8px 0 0 0                │
│  fill-2  │                                          │
│  a-menu  │  <slot />                                │
│  [折叠◀] │                                          │
└──────────┴──────────────────────────────────────────┘
```

## 完整 MainLayout.vue 代码

```vue
<template>
  <a-layout class="main-layout">
    <!-- Header -->
    <a-layout-header class="main-header">
      <IconHisense class="header-logo" />
      <span class="platform-name">{{ platformName }}</span>
      <a-menu
        v-if="showHeaderTabs"
        mode="horizontal"
        :selected-keys="[activeTab]"
        class="header-nav"
        @menu-item-click="(key: string) => activeTab = key"
      >
        <a-menu-item v-for="tab in headerTabs" :key="tab.key">
          {{ tab.label }}
        </a-menu-item>
      </a-menu>
      <div class="header-spacer" />
      <a-dropdown trigger="hover">
        <a-avatar :size="32" class="header-avatar">
          <icon-user />
        </a-avatar>
        <template #content>
          <a-doption>个人中心</a-doption>
          <a-doption>账号设置</a-doption>
          <a-doption>退出登录</a-doption>
        </template>
      </a-dropdown>
    </a-layout-header>

    <a-layout class="main-body">
      <!-- Sider：collapsed-width="48" 折叠后只显示图标 -->
      <a-layout-sider
        :width="200"
        :collapsed="siderCollapsed"
        :collapsed-width="48"
        class="main-sider"
        :trigger="null"
      >
        <a-menu
          v-model:selected-keys="selectedKeys"
          v-model:open-keys="openKeys"
          :collapsed="siderCollapsed"
          :style="{ width: '100%' }"
          @menu-item-click="handleMenuClick"
        >
          <template v-for="item in menuItems" :key="item.key">
            <a-sub-menu v-if="item.children?.length" :key="item.key">
              <template #icon><component :is="item.icon" /></template>
              <template #title>{{ item.label }}</template>
              <a-menu-item v-for="child in item.children" :key="child.key">
                {{ child.label }}
              </a-menu-item>
            </a-sub-menu>
            <a-menu-item v-else :key="item.key">
              <template #icon><component :is="item.icon" /></template>
              {{ item.label }}
            </a-menu-item>
          </template>
        </a-menu>
        <!-- 折叠/展开按钮，固定在 Sider 底部 -->
        <div class="sider-collapse-btn" @click="siderCollapsed = !siderCollapsed">
          <icon-menu-fold v-if="!siderCollapsed" />
          <icon-menu-unfold v-else />
        </div>
      </a-layout-sider>

      <!-- Content -->
      <a-layout-content class="main-content">
        <slot />
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script setup lang="ts">
import { ref, computed, markRaw } from 'vue'
import { IconUser, IconLeft, IconRight } from '@arco-design/web-vue/es/icon'
import { IconHome, IconList, IconEdit, IconDashboard, IconHisense } from '@arco-iconbox/vue-pangea-mobile'

const props = withDefaults(defineProps<{
  platformName?: string
}>(), {
  platformName: '原型演示系统',
})

const siderCollapsed = ref(false)
const selectedKeys = ref<string[]>(['home'])
const openKeys = ref<string[]>([])

// ── 模块/子应用配置 ──────────────────────────────────────
// 每个 Tab 代表一个模块，拥有独立的左侧菜单
// 如果只有一个模块，顶部 Tab 自动隐藏
const modules = [
  {
    key: 'workspace',
    label: '工作台',
    menus: [
      { key: 'home', label: '首页', icon: markRaw(IconHome) },
      { key: 'list', label: '列表管理', icon: markRaw(IconList) },
    ],
  },
  {
    key: 'system',
    label: '系统管理',
    menus: [
      { key: 'dashboard', label: '数据看板', icon: markRaw(IconDashboard) },
      {
        key: 'form-group', label: '表单管理', icon: markRaw(IconEdit),
        children: [
          { key: 'form-basic', label: '基础表单' },
          { key: 'form-step', label: '分步表单' },
        ],
      },
    ],
  },
]

const activeTab = ref(modules[0].key)

// 是否显示顶部 Tab（只有一个模块时隐藏）
const showHeaderTabs = computed(() => modules.length > 1)

// 顶部 Tab 列表
const headerTabs = modules.map(m => ({ key: m.key, label: m.label }))

// 当前模块对应的左侧菜单
const menuItems = computed(() => {
  const mod = modules.find(m => m.key === activeTab.value)
  return mod?.menus ?? []
})

const handleMenuClick = (key: string) => {
  selectedKeys.value = [key]
  // 有路由时跳转：router.push({ name: key })
}
</script>

<style scoped lang="less">
.main-layout {
  height: 100vh;
  overflow: hidden;
  background: var(--color-fill-2);
}

// ── Header ────────────────────────────────────────────────
.main-header {
  height: 48px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  padding: 0 16px 0 20px;
  gap: 16px;
  background: var(--color-fill-2);

  :deep(&.arco-layout-header) {
    background: var(--color-fill-2);
  }
}

.platform-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-1);
  white-space: nowrap;
  flex-shrink: 0;
}

.header-logo {
  font-size: 96px;
  color: rgb(var(--primary-6));
  flex-shrink: 0;
}

.header-nav {
  flex: 1;
  height: 48px;
  background: transparent !important;
  border-bottom: none !important;

  :deep(.arco-menu-light) {
    background: transparent;
  }

  :deep(.arco-menu-inner) {
    padding: 0;
  }

  :deep(.arco-menu-item) {
    background: transparent;
  }
}

.header-avatar {
  cursor: pointer;
  background: rgb(var(--primary-3));
  color: #fff;
  flex-shrink: 0;
}

.header-spacer {
  flex: 1;
}

// ── Body ──────────────────────────────────────────────────
.main-body {
  flex: 1;
  overflow: hidden;
  background: var(--color-fill-2);
}

// ── Sider ─────────────────────────────────────────────────
.main-sider {
  background: var(--color-fill-2);
  border-right: none;
  overflow-y: auto;
  box-shadow: none;

  // sider 内部用 flex 列布局，菜单撑满、折叠按钮固定底部
  :deep(.arco-layout-sider-children) {
    background: var(--color-fill-2);
    display: flex;
    flex-direction: column;
  }

  :deep(.arco-menu),
  :deep(.arco-menu-light) {
    background: var(--color-fill-2);
    flex: 1;
    overflow-y: auto;
  }

  // 默认菜单项：背景透明，融入 fill-2
  :deep(.arco-menu-item),
  :deep(.arco-menu-inline-header) {
    background: transparent;

    &:hover {
      background: var(--color-fill-3);
    }
  }

  :deep(.arco-menu-item.arco-menu-selected) {
    background: var(--color-bg-white) !important;
    color: rgb(var(--primary-6)) !important;
  }

  :deep(.arco-menu-inline-content) {
    background: transparent;
  }
}

// 折叠/展开按钮
.sider-collapse-btn {
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--color-text-3);
  border-top: 1px solid var(--color-border-2);
  font-size: 16px;
  flex-shrink: 0;

  &:hover {
    color: var(--color-text-1);
    background: var(--color-fill-3);
  }
}

// ── Content ───────────────────────────────────────────────
.main-content {
  overflow: hidden;
  background: var(--color-fill-2);

  // 页面组件根元素：白色背景，左上角圆角
  :deep(> *) {
    width: 100%;
    height: 100%;
    background: var(--color-bg-white);
    border-radius: 8px 0 0 0;
    overflow: hidden;
  }
}
</style>
```

## 工程目录结构

```
src/
├── main.ts
├── App.vue                    ← <MainLayout><router-view /></MainLayout>
├── layouts/
│   └── MainLayout.vue         ← 标准布局（必须生成）
├── router/
│   └── index.ts
├── types/
│   └── arco-iconbox.d.ts      ← 需声明 IconLeft、IconRight（折叠按钮用）
└── views/
    └── XxxPage.vue            ← 只写内容，不含布局
```

## App.vue

```vue
<template>
  <MainLayout>
    <router-view />
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from './layouts/MainLayout.vue'
</script>

<style>
#app { width: 100%; height: 100vh; }
</style>
```

## 页面组件规范

页面组件只负责内容区域，不包含 Header/Sider：

```vue
<template>
  <div class="xxx-page">
    <!-- 内容 -->
  </div>
</template>

<style scoped lang="less">
.xxx-page {
  height: 100%;
  // 不要设置 background，由 MainLayout 的 .main-content 提供白色背景
}
</style>
```

## 关键设计规格

| 区域 | 规格 |
|------|------|
| 整体/Header/Sider 背景 | `var(--color-fill-2)` |
| Header 高度 | 48px |
| Header 底部边框 | 无 |
| Sider 宽度 | 200px（展开）/ 48px（折叠，只显示图标） |
| Sider 右边框 | 无 |
| 菜单项默认背景 | `transparent`（融入 fill-2） |
| 菜单项选中背景 | `var(--color-bg-white)` + 主色文字 |
| 折叠按钮 | Sider 底部，高 40px，`border-top: 1px solid var(--color-border-2)` |
| 内容区背景 | `var(--color-bg-white)`，`border-radius: 8px 0 0 0` |

## 注意事项

- 顶部 Tab 代表模块/子应用，每个模块拥有独立的左侧菜单，切换 Tab 时菜单跟着切换
- 如果只有一个模块（`modules` 数组长度为 1），顶部 Tab 自动隐藏，只显示左侧菜单
- `modules` 数组是核心配置，生成时根据业务场景替换，不要照搬示例

- `IconLeft` / `IconRight` 来自 `@arco-design/web-vue/es/icon`，不需要在 `arco-iconbox.d.ts` 中声明
- 生成工程时，`arco-iconbox.d.ts` 中需要声明 MainLayout 里用到的 Pangea 图标（如 `IconHome`、`IconList` 等）
- 菜单项配置（`menuItems`、`headerTabs`）根据实际需求替换，不要照搬示例
