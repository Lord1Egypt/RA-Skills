---
name: orbcafe-kanban-detail
description: Build ORBCAFE Kanban boards with CKanbanBoard/CKanbanBucket/CKanbanCard/useKanbanBoard and wire card clicks into DetailInfo using official examples patterns. Use for bucket-card styling, drag-drop workflow boards, controlled board state, and Kanban-to-detail navigation, especially when UI renders but drag or click behavior has no effect.
---

# ORBCAFE Kanban + Detail

## Workflow

1. 先对照 `skills/orbcafe-ui-component-usage/references/module-contracts.md`，确认这是 `Hook-first` 模块。
2. 执行安装与最小可运行接入。
3. 用 `references/recipes.md` 输出实现骨架。
4. 用 `references/guardrails.md` 检查受控状态、拖拽移动、空 bucket 接收和 DetailInfo 路由。
5. 输出验收步骤与“没效果”排障。

## Installation and Bootstrapping (Mandatory)

```bash
npm install orbcafe-ui @mui/material @mui/icons-material @mui/x-date-pickers @emotion/react @emotion/styled dayjs
```

本仓库联调：

```bash
npm run build
cd examples
npm install
npm run dev
```

参考实现：
- `examples/app/kanban/page.tsx`
- `examples/app/_components/KanbanExampleClient.tsx`
- `examples/app/detail-info/[id]/DetailInfoExampleClient.tsx`
- `src/components/Kanban/README.md`

## Output Contract

0. `Mode`: `Hook-first`.
1. `Chosen module`: Kanban and whether DetailInfo chaining is required.
2. `Minimal implementation`: `useKanbanBoard + CKanbanBoard` first.
3. `Data model`: buckets/cards/tools shape.
4. `Verify`: 至少包括拖拽跨 bucket、生效后的状态更新、空 bucket 可接收、点击进入 DetailInfo。
5. `Troubleshooting`: 至少 3 条“能看到 UI 但拖拽/点击没效果”的排查项。

## Examples-Based Experience Summary

- 优先 `useKanbanBoard + CKanbanBoard`，不要只渲染组件而不托管 `model`。
- bucket 与 card 的样式能力分别通过 `CKanbanBucket` / `CKanbanCard` 暴露，但拖拽交互由 `CKanbanBoard` 统一编排。
- 需要 reducer/store/optimistic update 时优先复用 `createKanbanBoardModel` 和 `moveKanbanCard`。
- Detail 链接放在 Client Component 的 `onCardClick` 中，避免把路由行为写进 Server 层。
