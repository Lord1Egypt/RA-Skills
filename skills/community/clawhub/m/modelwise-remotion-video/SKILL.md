---
name: Remotion Video Skill
description: 基于 Remotion 的动画演示视频创作技能，提供丰富的动画组件和视频模板。By ModelWise team.
version: 1.0.0
tags:
  - video
  - animation
  - remotion
  - react
author: ModelWise team
---

# Remotion Video Skill

> **By ModelWise team** - Professional AI Agent Solutions

基于 Remotion 的动画演示视频制作技能。

## 功能特性

### 基础动画组件
- **FadeIn/FadeOut** - 淡入淡出动画
- **SlideIn** - 滑动入场动画（支持四个方向）
- **ScaleIn** - 缩放入场动画（支持 spring 效果）
- **Typewriter** - 打字机文字效果
- **WordHighlight** - 文字高亮动画

### 场景过渡效果
- **TransitionScene** - 封装 @remotion/transitions
- 支持 fade、slide、wipe 等过渡效果

### 视频模板
- **ProductDemo** - 产品演示模板
- **TitleSequence** - 标题动画模板
- **DataVisualization** - 数据展示模板

### 视频配置预设
- **landscape**: 1920x1080 (16:9 横屏)
- **portrait**: 1080x1920 (9:16 竖屏)
- **square**: 1080x1080 (1:1 正方形)

## 使用方法

### 1. 安装依赖
```bash
npm install
```

### 2. 启动开发服务器
```bash
npm run studio
```

### 3. 渲染视频
```bash
npx remotion render HelloDemo out/demo.mp4
```

## 项目结构

```
remotion-video-skill/
├── package.json           # 项目依赖
├── tsconfig.json          # TypeScript 配置
├── remotion.config.ts     # Remotion 配置
├── SKILL.md               # 技能说明文档
├── task.md                # 任务进度记录
└── src/
    ├── Root.tsx           # 入口文件
    ├── components/        # 可复用动画组件
    ├── compositions/      # 视频组合/模板
    └── utils/             # 工具函数
```

## 开发指南

### 创建新的动画组件
在 `src/components/` 目录下创建新的组件文件。

### 创建新的视频模板
1. 在 `src/compositions/` 创建模板文件
2. 在 `src/Root.tsx` 中注册新的 Composition

### 使用动画预设
```typescript
import { springPresets, easingPresets } from "./utils/animations";
```

## 技术栈
- React 18
- Remotion 4.x
- TypeScript 5.x
- @remotion/transitions
