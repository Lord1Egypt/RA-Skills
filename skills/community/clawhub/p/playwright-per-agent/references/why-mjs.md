# 为什么脚本是 `.mjs`（开发者参考）

> **本文件不是给最终用户看的**。是 skill 维护者/贡献者的技术选型说明。
> 如果你是想用这个 skill，跳过本节直接看 `SKILL.md`。

## 决策

脚本文件扩展名用 `.mjs` 而非 `.js` / `.cjs`。

## 3 个选项对比

| 选项 | 优 | 劣 | 适合场景 |
|---|---|---|---|
| `.mjs` ✓ | 显式 ESM、top-level await、无需 package.json、playwright 兼容 | 文件后缀特殊 | **本 skill（无 package.json 约束）** |
| `.js` + `"type": "module"` | 跟项目其他 .js 一致 | 需要新建 package.json | 单仓库 monorepo |
| `.cjs` | CJS 兼容老代码 | playwright ESM 还得 dynamic import | CJS 主导的老项目 |

## 为什么不是其他两个

- **`.cjs`**：Playwright 1.40+ 全面 ESM 化，用 `require('playwright')` 还能工作但 import 语法更干净；
  此外本 skill 不需要 CJS 兼容（没有老的 CommonJS 依赖需要桥接）。
- **`.js` + `"type": "module"`**：要在 `scripts/` 目录放一个 `package.json`，但 skill 文件结构规范
  （见 `~/.openclaw/workspace-main/skills/skill-creator-plus/SKILL.md`）只允许 `SKILL.md` + `_meta.json` +
  可选 `scripts/` / `references/` / `assets/`，没有 `package.json` 的位置。多一个文件就破坏了规范。
- **`.mjs`**：显式声明 ESM，无需任何配置文件。直接 import 直接用。

## ESM 给我们的能力

1. **Top-level await**（`.cjs` 不能用）：
   ```js
   if (import.meta.url === `file://${process.argv[1]}`) {
     // CLI demo entry
   }
   ```
2. **`import` 语法**（不需要 `require()` + 解构）：
   ```js
   import { chromium } from 'playwright';
   import { createHash } from 'node:crypto';
   ```
3. **静态可分析**：打包工具和 tree-shaker 更友好。
4. **Node 22 默认 ESM-first**（2026 标准）：`.mjs` 跟运行时默认行为一致。

## 改动成本

要改成 `.js` + `"type": "module"` 需要：
1. 新建 `scripts/package.json`：{ "type": "module" }
2. 改所有 `.mjs` 引用为 `.js`
3. 删 import URL 检查里的 `.mjs` 后缀

没必要 — `.mjs` 路径已经达到同样效果且更轻量。

## 何时考虑重审

如果出现以下情况，重审这个决定：
- 需要在 skill 里 require 一个老的 CJS 包（且无 ESM 替代）
- Node 版本要求降到 < 14（但 5.28 已要求 Node 22）
- skill-creator-plus 规范改变，scripts/ 里允许放 package.json
