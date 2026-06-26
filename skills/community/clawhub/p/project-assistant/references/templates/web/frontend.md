# Web前端项目分析

分析React、Vue、Angular等前端项目。

## 适用类型

- `react` - React项目
- `vue` - Vue项目
- `angular` - Angular项目
- `svelte` - Svelte项目
- `nextjs` - Next.js项目
- `nuxt` - Nuxt.js项目

## 执行步骤

### 1. 解析package.json

调用解析器：
```bash
python3 ~/.claude/tools/init/parsers/package_json_parser.py "$TARGET_DIR"
```

提取：
- 项目名称和版本
- 依赖列表
- scripts脚本
- 框架识别

### 2. 识别框架

检查依赖：
- `react`, `react-dom` → React
- `vue` → Vue
- `@angular/core` → Angular
- `svelte` → Svelte
- `next` → Next.js
- `nuxt` → Nuxt.js

### 3. 分析项目结构

```
src/
├── components/   # 组件
├── pages/        # 页面
├── hooks/        # Hooks (React)
├── composables/  # 组合式函数 (Vue)
├── store/        # 状态管理
├── api/          # API请求
├── utils/        # 工具函数
├── types/        # TypeScript类型
├── styles/       # 样式
└── assets/       # 静态资源
```

### 4. 识别状态管理

检查依赖：
- `redux`, `@reduxjs/toolkit` → Redux
- `mobx` → MobX
- `zustand` → Zustand
- `pinia` → Pinia
- `vuex` → Vuex
- `jotai`, `recoil` → 原子化状态

### 5. 识别UI框架

检查依赖：
- `antd`, `ant-design` → Ant Design
- `element-plus`, `element-ui` → Element
- `material-ui`, `@mui` → MUI
- `tailwindcss` → Tailwind CSS
- `chakra-ui` → Chakra UI

### 6. 生成文档

## 输出格式

```
项目初始化完成！

项目名称: {name}
项目类型: Web前端应用
主要语言: TypeScript/JavaScript
框架: {framework}
构建工具: {vite/webpack/next}
包管理器: {npm/yarn/pnpm}

技术栈:
  - 状态管理: {store}
  - UI框架: {ui}
  - 路由: {router}
  - 数据请求: {fetch}

模块统计:
  - 组件: {count} 个
  - 页面: {count} 个
  - Hooks: {count} 个

核心功能: {count} 项

已生成项目文档: .claude/project.md
```