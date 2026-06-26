---
name: orbcafe-stdreport-workflow
description: Build ORBCAFE standard report/list pages with CStandardPage, CTable, CSmartFilter, useStandardReport, persistence, and quickCreate/quickEdit/quickDelete using official examples-proven patterns. Use for filters, pagination, variants/layout, or report orchestration, especially when prior implementation had no visible effect.
---

# ORBCAFE StdReport Workflow

## Workflow

1. 执行安装与运行前置。
2. 先对照 `skills/orbcafe-ui-component-usage/references/module-contracts.md`，确认这是 `Hook-first` 模块。
3. 用 `references/component-selection.md` 选择 `integrated` 或 table-only。
4. 基于 `references/recipes.md` 生成最小可运行代码。
5. 用 `references/guardrails.md` 强制检查 identity、分页、持久化、i18n。
6. 按官方 examples 补齐验收与排障步骤。

## Installation and Bootstrapping (Mandatory)

```bash
npm install orbcafe-ui @mui/material @mui/icons-material @mui/x-date-pickers @emotion/react @emotion/styled dayjs
```

本仓库联调时，严格按官方顺序：

```bash
# repo root
npm run build

cd examples
npm install
npm run dev
```

参考实现：
- `examples/app/_components/StdReportExampleClient.tsx`
- `examples/app/std-report/page.tsx`

## Mandatory rules

- 始终设置 identity：
  - `metadata.id` for `useStandardReport`
  - `id` for `CStandardPage`
  - `appId` for standalone `CTable` / `CSmartFilter`
- 默认优先 `useStandardReport + CStandardPage mode="integrated"`。
- 始终从 `orbcafe-ui` 包入口导入，不导入私有 `src/components/*`。
- 需要 locale 时优先用 `CAppPageLayout.locale` 或 `OrbcafeI18nProvider`。
- `quickCreate/quickEdit/quickDelete` 开启时，始终给出 async 回调并写清 payload 结构。
- 后端不支持 `limit=-1` 时，在 `fetchData` 层显式转换，不要把 ALL 模式直接透传。

## Examples-Based Experience Summary

- 先用 `useStandardReport` 产出 `pageProps`，再注入 `tableProps.quick*` 扩展，稳定且可维护。
- 通过 `metadata.variants` 提供默认视图，再让用户落地保存，能减少首次空白配置。
- 列渲染尽量只做展示转换，筛选值保持机器稳定值（例如 `active/pending/inactive`）。
- 表格放在固定高度容器（例如 `calc(100vh - 120px)`）可避免页面整体滚动抖动。

## Output Contract

0. `Mode`: `Hook-first`.
1. `Pattern`: integrated page or table-only.
2. `Code`: paste-ready, imports from `orbcafe-ui` only.
3. `Data contract`: columns/filters/rows/fetchData shape.
4. `Verify`: 启动页面、筛选生效、分页切换、quick 操作触发、刷新后配置保留。
5. `Troubleshooting`: 至少包含以下排查项：
   - 忘记 `metadata.id/id/appId` 导致变体/布局“没效果”
   - 没有先 `npm run build`（本地 `file:..` 依赖场景）
   - 错误导入路径或 Next 客户端边界导致组件不渲染
