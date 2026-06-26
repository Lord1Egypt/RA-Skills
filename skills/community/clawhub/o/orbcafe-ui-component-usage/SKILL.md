---
name: orbcafe-ui-component-usage
description: Route ORBCAFE UI requests to the correct module skill and enforce official examples-based integration baseline. Use when requests are ambiguous, cross-module, or when prior attempts had "no effect"; classify to StdReport, Graph+Detail+Agent, Layout+Navigation, Pivot+AINav, or AgentUI Chat and require install/startup/verification steps.
---

# ORBCAFE UI Router

## Workflow

1. 执行安装与接入基线（必须）。
2. 使用 `references/skill-routing-map.md` 判定目标模块 skill。
3. 使用 `references/module-contracts.md` 先确认目标模块的公共入口、hook 策略、标准 example 与验证方式。
4. 只加载目标模块所需 references，不加载无关内容。
5. 使用 `references/public-export-index.md` 约束导入边界。
6. 使用 `references/integration-baseline.md` 执行 Next.js 与 hydration 检查。
7. 输出模块决策、最小可运行代码、验收步骤、排障步骤。

## Installation Baseline (Mandatory)

每次都先给出可执行安装方式，不允许省略：

```bash
npm install orbcafe-ui @mui/material @mui/icons-material @mui/x-date-pickers @emotion/react @emotion/styled dayjs
```

如果是本仓库联调（以 `examples` 为准）：

```bash
# repo root
npm run build

# examples app
cd examples
npm install
npm run dev
```

Tailwind 项目必须包含：

```js
// tailwind.config.js
content: ["./node_modules/orbcafe-ui/dist/**/*.{js,mjs}"]
```

## Output Contract

Always provide:

1. `Decision`: 选择哪个模块 skill，并说明依据。
2. `Paste-ready code`: 仅从 `orbcafe-ui` 入口导入。
3. `Data shape`: 最小必需字段结构。
4. `Verify`: 至少 3 条可执行验收步骤（启动、交互、持久化/回调）。
5. `Troubleshooting`: 至少 3 条“没效果”排查点。

Before writing code, explicitly state one of:

- `Hook-first`: 该模块以公开 hook 为主入口。
- `Component-first`: 该模块以公开组件 + callbacks 为主入口。

## Examples-First Rules

- 先复用官方 examples 的骨架，再做业务改造。
- 优先参考：
  - `examples/README.md`
- `examples/app/layout.tsx`
- `examples/app/providers.tsx`
- `examples/app/_components/*.tsx`
- 强制遵守 Next.js App Router 经验：
  - 在 Server Page 解包 `params/searchParams` 后再传入 Client 组件。
  - 首屏避免 `Date.now()/Math.random()/window/localStorage/usePathname` 直接决定结构。
  - 必要时使用 `mounted` 防止 hydration mismatch。
