---
name: matrix-bnuhs
description: Matrix-BNUHS知识协作网络系统。为教育场景提供多维度知识组织、协作编辑、版本控制和权限管理能力。当用户需要(1)搭建知识管理系统、(2)构建教育场景应用、(3)实现多维矩阵组织、(4)创建协作编辑功能、(5)部署React前端应用时使用此skill。基于React + TypeScript构建，支持知识胶囊、多维矩阵、虚拟思想家等功能。
---

# Matrix-BNUHS 知识协作网络

## 概述

Matrix-BNUHS是北师大附中M2项目的知识协作网络系统，为教育场景提供知识管理支持。

## 特性

- **多维矩阵**: 支持多维度知识组织
- **协作编辑**: 多人实时协作
- **版本控制**: 完整的版本历史
- **权限管理**: 细粒度权限控制

## 技术栈

- **前端**: React 18 + TypeScript
- **样式**: CSS Modules
- **构建**: Vite
- **后端**: Python FastAPI (可选)

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/wanyview1/Matrix-BNUHS.git
cd Matrix-BNUHS

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

服务启动: http://localhost:5173

## 核心组件

### KnowledgeSalonScenarios

知识沙龙场景组件，支持多角色对话。

```tsx
import { KnowledgeSalonScenarios } from './components/KnowledgeSalonScenarios';

// 使用
<KnowledgeSalonScenarios 
  roles={['学生', '教师', '专家']}
  onMessage={handleMessage}
/>
```

### CapsuleSystem

知识胶囊管理系统。

```typescript
interface Capsule {
  id: string;
  title: string;
  content: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}
```

## API端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/matrix` | GET | 获取矩阵 |
| `/api/node` | POST | 创建节点 |
| `/api/collab` | POST | 协作编辑 |
| `/api/capsule` | GET/POST | 知识胶囊CRUD |

## 目录结构

```
matrix-bnu hs/
├── App.tsx              # 主应用组件
├── index.tsx           # 入口文件
├── components/         # React组件
│   ├── KnowledgeSalonScenarios.tsx
│   ├── CapsuleViewer.tsx
│   └── MatrixGrid.tsx
├── config/             # 配置文件
│   └── schoolConfig.ts
├── types.ts            # TypeScript类型
└── docs/               # 文档
    ├── DEPLOYMENT_GUIDE.md
    └── KNOWLEDGE_SALON_GUIDE.md
```

## 教育场景用例

### 1. 知识沙龙

```tsx
// 创建知识讨论场景
const salonConfig = {
  topic: "科学探索",
  participants: [
    { role: "学生", perspective: "好奇" },
    { role: "教师", perspective: "引导" },
    { role: "专家", perspective: "专业" }
  ]
};
```

### 2. 知识胶囊

```typescript
// 创建知识胶囊
const capsule = {
  title: "量子力学基础",
  content: "# 量子力学...\n\n波函数...",
  tags: ["物理", "量子", "入门"],
  level: "intermediate"
};
```

### 3. 多维矩阵

```typescript
// 定义知识维度
const matrix = {
  dimensions: [
    { name: "学科", values: ["物理", "化学", "生物"] },
    { name: "难度", values: ["入门", "进阶", "高级"] },
    { name: "类型", values: ["概念", "计算", "实验"] }
  ]
};
```

## 部署

### Vercel部署

```bash
# 安装Vercel CLI
npm i -g vercel

# 部署
vercel --prod
```

### Docker部署

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm run build
EXPOSE 5173
CMD ["npm", "run", "preview"]
```

## 资源

- **GitHub**: https://github.com/wanyview1/Matrix-BNUHS
- **ClawHub**: https://clawhub.com
- **文档**: docs/DEPLOYMENT_GUIDE.md

---

*Built with ❤️ by KAI*