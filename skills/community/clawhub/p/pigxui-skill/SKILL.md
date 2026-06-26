---
name: pigxui-skill
version: 1.0.0
description: PigX UI Pro 前端开发指南 - Vue 3 + TypeScript + Element Plus。当用户提到 PigX UI、PigX 前端、lgb-mgui 项目、Vue 3 企业级后台开发、Element Plus 后台开发时使用此技能。
---

# PigX UI 前端开发 Skill

> PigX UI Pro 企业级前端开发指南 - Vue 3 + TypeScript + Element Plus

## 项目信息

| 属性 | 值 |
|------|-----|
| 框架 | Vue 3 (Composition API) |
| 语言 | TypeScript |
| UI 库 | Element Plus |
| 状态管理 | Pinia |
| 路由 | Vue Router |
| 构建工具 | Vite |
| CSS 框架 | Tailwind CSS + DaisyUI |
| 版本 | 5.12.0 |

## 本地项目路径

```
D:\WorkSpace\my_workspace\lhb\lgb-mgui
```

## 官方文档

- 文档入口: https://docs.pig4cloud.com（需要微信扫码登录）

---

## 常用命令

```bash
# 安装依赖
pnpm install

# 启动开发服务 (默认端口 8888)
pnpm dev

# 生产构建
pnpm build

# Docker 构建
pnpm build:docker

# ESLint 检查修复
pnpm lint:eslint

# Prettier 格式化
pnpm prettier
```

---

## 项目结构

```
lgb-mgui/
├── src/
│   ├── api/              # API 请求定义
│   ├── assets/           # 静态资源
│   ├── components/       # 可复用组件（全局自动注册）
│   ├── directive/        # 自定义指令
│   ├── hooks/            # 组合式函数
│   ├── i18n/             # 国际化配置
│   ├── layout/           # 布局组件
│   ├── router/           # 路由配置（后端控制）
│   ├── stores/           # Pinia 状态管理
│   ├── theme/            # 主题样式
│   ├── types/            # TypeScript 类型定义
│   ├── utils/            # 工具函数
│   ├── views/            # 页面组件
│   ├── App.vue           # 根组件
│   └── main.ts           # 入口文件
├── public/               # 公共资源
├── vite.config.mts       # Vite 配置
├── tailwind.config.js    # Tailwind 配置
└── tsconfig.json         # TypeScript 配置
```

---

## 核心开发规范

### 1. API 调用规范

所有 API 必须放在 `src/api/` 目录下：

```typescript
// src/api/admin/audit.ts
import request from '/@/utils/request';

export function fetchList(query?: Object) {
  return request({
    url: '/admin/audit/page',
    method: 'get',
    params: query,
  });
}
```

**使用方式**：
```typescript
const { data } = await fetchList(query);
```

**自动处理的请求头**：
- `Authorization` - Token 自动注入
- `TENANT-ID` - 租户 ID 自动注入
- 请求/响应加解密

### 2. 路由架构

- **后端控制路由**：路由由后端 API 返回，前端动态注入
- **两级嵌套**：路由最多支持两级嵌套（keep-alive 兼容）
- **动态加载**：使用 `import.meta.glob` 动态加载组件

### 3. 状态管理 (Pinia)

```typescript
// src/stores/userInfo.ts
import { defineStore } from 'pinia';

export const useUserInfoStore = defineStore('userInfo', {
  state: () => ({
    user: null,
    token: '',
  }),
  actions: {
    async login(credentials) {
      // ...
    },
  },
  persist: true,
});
```

### 4. 组件规范

使用 `<script setup>` 语法，添加 `name` 属性以支持 keep-alive：

```vue
<script setup lang="ts" name="MyComponent">
// 组件逻辑
</script>
```

### 5. 样式规范

**Tailwind CSS**：
```vue
<div class="flex items-center justify-between p-4 bg-white dark:bg-gray-800">
</div>
```

**暗色模式**：
```scss
[data-theme='dark'] {
  // 暗色样式
}
```

---

## 常见开发任务

### 新增页面

1. 在 `src/views/` 下创建页面组件
2. 后端配置菜单和路由
3. 在 `src/api/` 中定义相关 API

### 新增 API 接口

```typescript
// src/api/module/example.ts
import request from '/@/utils/request';

export function getList(params: any) {
  return request({
    url: '/module/example/list',
    method: 'get',
    params,
  });
}
```

### 新增 Store

```typescript
// src/stores/myStore.ts
import { defineStore } from 'pinia';

export const useMyStore = defineStore('myStore', {
  state: () => ({ items: [] }),
  getters: {
    itemCount: (state) => state.items.length,
  },
  actions: {
    async fetchItems() {}
  },
  persist: true,
});
```

---

## 注意事项

1. **路径别名**：`/@/` 指向 `src/` 目录
2. **自动导入**：Vue、Vue Router、Pinia API 自动导入
3. **Token 管理**：自动注入 `Authorization` 头
4. **租户支持**：自动注入 `TENANT-ID` 头
5. **请求加密**：默认开启，可通过 `Enc-Flag: false` 关闭

---

## 参考文档

- Vue 3 文档: https://vuejs.org
- Element Plus 文档: https://element-plus.org
- Tailwind CSS 文档: https://tailwindcss.com

## 参考资料

更多前端文档请参考 `references/` 目录下的文档文件。