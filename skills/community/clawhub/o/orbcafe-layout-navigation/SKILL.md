---
name: orbcafe-layout-navigation
description: Build ORBCAFE application shell and navigation with CAppPageLayout, NavigationIsland, useNavigationIsland, i18n, markdown renderer, and CPageTransition using official examples patterns. Use for app frame, user menu, locale switching, navigation tree, and route transition UX, especially when UI renders but behavior looks inactive.
---

# ORBCAFE Layout + Navigation

## Workflow

1. 先对照 `skills/orbcafe-ui-component-usage/references/module-contracts.md`，确认这是 `Hook-first` 模块。
2. 执行安装与基础壳层接入。
3. 用 `references/patterns.md` 选择 full shell 或 nav-only。
4. 用 `references/guardrails.md` 逐条检查 locale、hydration、菜单动作和动效。
5. 以官方 examples 的 layout/providers/page 骨架产出代码。

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
- `examples/app/layout.tsx`
- `examples/app/providers.tsx`
- `examples/app/_components/HomeDemoClient.tsx`
- `examples/app/_components/StdReportExampleClient.tsx`

## Output Contract

0. `Mode`: `Hook-first`.
1. `Layout decision`: full shell vs nav-only.
2. `Code snippet`: app frame with minimal props.
3. `Runtime safety`: locale、hydration、route 高亮安全策略。
4. `Verify`: 菜单跳转、locale 切换、用户菜单动作、过渡动画。
5. `Troubleshooting`: 至少包含 3 条“页面看起来没反应”排查项。

## Examples-Based Experience Summary

- 在 App Router 下优先采用 `Server page -> Client page` 分层，不在 client 首屏直接消费 Promise 语义路由参数。
- `usePathname` 高亮逻辑使用 `mounted` 防抖策略，避免 SSR/CSR 首帧不一致。
- `CAppPageLayout` 内部负责壳层，业务页只注入 menu/user/logo/children，避免重复造壳。
- `CPageTransition` 持续使用 `160-260ms`，仅用 transform/opacity 变换，性能更稳。
- `Providers` 层集中挂载 `ThemeProvider + LocalizationProvider + GlobalMessage`，避免每页重复配置。
