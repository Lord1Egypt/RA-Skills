# Acme Dashboard

> 30 秒速览：面向运营经理的 B2B 分析仪表盘。优化优先级：加载速度 > 交互 > 视觉。
> 新代码按下方目录结构放进对应模块；动手前先看该模块 README。

## 工作风格
- 先给方案再写代码；不确定时列选项，不要猜。
- 汇报用中文，代码与注释用英文；文件引用用绝对路径。
- 不说「Great question!」这类客套，直接给结论。

## 跨会话记忆
- 任务开始前扫一遍 `MEMORY.md`；结束后把新的非显然结论写回。

## 铁律
1. 用 named export（路由文件除外）。
2. 禁 `any`，用泛型或接口替代。
3. 单组件不超过 200 行（有充分理由可超）。

## 技术栈（tech stack）
- Next.js 15 App Router + TypeScript
- Tailwind CSS + shadcn/ui
- PostgreSQL（数据层）

Do NOT introduce unless explicitly requested:
- Redux（已迁移到 React Context + Zustand）
- styled-components（全站 Tailwind，不收 CSS-in-JS）
- MongoDB（数据层锁定 PostgreSQL）

## 目录结构（directory · 新代码放哪里）
```
src/
  app/        # 路由与页面
  components/ # 复用组件
  lib/        # 工具与数据访问
```

## 延伸文档（Tier 2，按需打开）
- 架构总览：`docs/architecture.md`
- API 文档：`docs/api.md`
