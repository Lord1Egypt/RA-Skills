# CLAUDE.md — 龙虾增强包（huo15-openclaw-enhance）接手第一入口

> Claude Code 自动加载本文件。任何账号 clone 本仓库后先读这里，再按需展开 `docs/`。
> 接手完整指南见 [docs/HANDOVER.md](docs/HANDOVER.md)。

## 是什么

`@huo15/huo15-openclaw-enhance` —— **非侵入式**的 OpenClaw（龙虾）插件。在不改龙虾核心、不重复龙虾原生能力的前提下，补齐「项目工程化 + 多 Agent 运营」维度的能力（结构化记忆、任务/章节追踪、配置体检、文件分享/预览、Claude Code 桥接、上下文守护等 36 个模块）。

- npm: `@huo15/huo15-openclaw-enhance`（当前 v6.7.19）
- 主仓库: https://cnb.cool/huo15/ai/huo15-openclaw-enhance （remote `origin`）
- GitHub 镜像: https://github.com/zhaobod1/huo15-openclaw-enhance （remote `github`，SSH 别名 `github-zhaobod1`）
- ClawHub slug: `huo15-huo15-openclaw-enhance`

## 最高铁律（违反即返工）

**Enhance OpenClaw, never modify or duplicate it. 龙虾有的，让龙虾管。**

加任何新功能前，先 `grep` `~/workspace/projects/openclaw/openclaw-source`（只读参考，禁改）找原生等价物：原生**有**就走原生 API（`registerMemoryCapability` / `on(hook, handler)` 等），原生**没有**才补。详见 [docs/decisions/](docs/decisions/)。

## 怎么跑

```bash
npm install
npm i openclaw@latest --no-save     # openclaw 是 peerDep，本地开发需另装最新 SDK 才能 typecheck
npx tsc --noEmit                    # 发版前必过（应 exit 0）
npm run build                       # tsc + 拷 package.json/openclaw.plugin.json 到 dist/
openclaw plugins install "$(pwd)"   # 装到本地 OpenClaw
```

入口 `index.ts` → `const enhancePlugin: OpenClawPluginDefinition = definePluginEntry({ id:"enhance", register })` → `export default enhancePlugin`。register 内先 `wrapApiForSafeHooks(rawApi)` 给所有模块 hook 套 try/catch，再 `initDb()`（better-sqlite3，失败降级不崩），按 `toolTier` 逐个 register 模块。架构见 [docs/architecture.md](docs/architecture.md)。

## 开发铁律（任何 @huo15/* 插件通用）

1. **`compat.pluginApi` 必须 semver range**（`>=2026.4.24`），不能裸版本；`peerDependencies.openclaw` 同理（`^2026.4.24`）。`build.openclawVersion` 是信息字段，裸版本 OK。
2. **禁 `child_process`**（execSync/spawn/spawnSync）—— 企业 npm 扫描器判高危整包拦截。需要跑外部命令的功能一律 **return-cliCmd 模式**。参考 `skill-installer.ts` / `scheduled-tasks-bridge.ts` / `spawn-task.ts`。
3. **`registerMemoryCorpusSupplement` / `registerMemoryPromptSupplement` 是单参**（pluginId 自动注入）。
4. **诊断不修复**：要「建议改龙虾配置」的功能一律 return-cliCmd，**永不** `fs.writeFileSync` 用户配置文件。
5. **LLM 输出过 sanitizer**：LLM 生成的 target/URL/路径一律不可信，发文件/广播前必经插件层闸门。
6. **default export 显式类型**：SDK 2026.6.x 起 `export default definePluginEntry(...)` 会撞 TS2742，必须 `const x: OpenClawPluginDefinition = definePluginEntry(...)` + `export default x`（**不是** `OpenClawPluginEntry`，那个 SDK 没导出）。见 docs/lessons。

## 发版 SOP（精简）

跨会话先对账（见 HANDOVER §5）→ bump `package.json.version` + 写 CHANGELOG → `build.openclawVersion` 改目标 runtime（compat/peer 保持 ranged）→ `tsc --noEmit` 过 → `npm run build`（删旧 dist 防残留）→ git commit + tag → **双 remote push**（`git push origin main && git push github main`，tag 同理）→ `npm publish` → `clawhub publish "$(pwd)" --version X.Y.Z`。

## 目录导航

| 路径 | 内容 |
|---|---|
| `index.ts` | 插件入口 |
| `src/modules/*` | 36 个功能模块，每个 register 一类能力 |
| `src/utils/*` | sqlite-store / safe-api-wrapper / resolve-home / notification-queue / latency-tracker |
| `docs/architecture.md` | 架构、模块清单、数据流 |
| `docs/PRD.md` | 产品需求、非目标边界 |
| `docs/HANDOVER.md` | 接手指南（环境/凭据指路/发布/当前状态） |
| `docs/decisions/*` | ADR 关键决策 |
| `docs/lessons/*` | 踩坑复盘 |
| `docs/SELF_ITERATE.md` | 每 3 天自我迭代 SOP |
