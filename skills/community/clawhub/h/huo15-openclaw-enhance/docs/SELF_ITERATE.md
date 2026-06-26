# enhance 持续自我迭代 SOP

> 用户硬要求（2026-04-25）：
>
> 1. **不断自我迭代** — 每 3 天对照 Claude Code（官方 docs / 本地 npm 源码 / 反编译 Claude Desktop APP）做一次能力 gap 调研，挑高 ROI 候选落地。
> 2. **零侵入** — 永远不动 openclaw 核心代码、不复制龙虾原生功能。重叠功能以龙虾为准。
> 3. **skill 走 ClawHub** — 任何要新增 / 修改的 skill **必须先在本地 `huo15-skills/` 里写好 → 发布到 ClawHub → 然后让本插件的 `skill-installer.ts` 引用 slug**。**插件代码里绝不内嵌 skill 内容**。

本文档把这套迭代节奏沉淀成 SOP，每次迭代结束直接更新这里。

---

## 1. 三个信息源

| 源 | 路径 | 用途 |
|---|---|---|
| **Claude Code 官方 docs** | https://docs.claude.com/en/docs/claude-code/ + 子页 | 最权威能力清单 — 看 hooks/skills/slash-commands/sessions/modes 各页 |
| **Claude Code npm 包源码** | `~/.nvm/versions/node/<ver>/lib/node_modules/@anthropic-ai/claude-code/` | `sdk-tools.d.ts` 揭示 SDK 工具/Hook/Agent 的真实类型定义；`bin/` 入口 |
| **Claude Desktop APP（反编译）** | `/Applications/Claude.app/Contents/Resources/app.asar` | 解包后 `.vite/build/` 下有完整业务逻辑 — workers、UI、native helpers 都在 |

### 反编译 Claude Desktop（验证可行）

```bash
# 解包（不修改原 app）
mkdir -p /tmp/claude-app-extract
npx --yes @electron/asar extract /Applications/Claude.app/Contents/Resources/app.asar /tmp/claude-app-extract

# 关键工程目录
ls /tmp/claude-app-extract/.vite/build/
#   ├─ index.js                              # 主进程 bundle (10k+ 行)
#   ├─ index.pre.js                          # 预加载
#   ├─ mainView.js / mainWindow.js / quickWindow.js / aboutWindow.js / buddy.js
#   ├─ coworkArtifact.js / findInPage.js / computerUseTeach.js
#   ├─ mcp-runtime/{directMcpHost.js, nodeHost.js}
#   ├─ shell-path-worker/shellPathWorker.js
#   ├─ sqlite-worker/sqliteWorker.node.js
#   └─ transcript-search-worker/transcriptSearchWorker.js   ← v5.7 灵感来源
```

**v5.7 transcript-search 就是这样找到的** —— Claude Desktop 用纯流式扫 JSONL + indexOf，**不用 SQL FTS5**。我们直接照搬，省下了 v5.5.1 路线图里"建 session_messages 新表 + FTS"的工作量。

清理：`rm -rf /tmp/claude-app-extract` 不留痕。

---

## 2. 候选迭代池（按 ROI 排序，每次更新）

| # | 候选 | 来源 | 形态 | 估算 | 状态 |
|---|------|------|------|------|------|
| ✅ | **transcript-search** | Claude Desktop transcriptSearchWorker | Plugin 模块 | ~200 行 | 已落地 v5.7.0 |
| ✅ | **before_compaction 噪音 hook 删除 + memory_purge 工具** | 用户实测 enhance 库 613 条全为 auto-compact 噪音 | Plugin hot-fix | ~80 行净改动 | 已落地 **v5.7.1**（2026-04-26 计划外 hot-fix）|
| ✅ | **hardening 套件**（Map LRU + safety_log TTL + corpus tag 黑名单）| Explore agent 全代码审计 + 防御未来类似 v5.7.1 的 noise factory | Plugin patch | ~120 行 | 已落地 **v5.7.2**（2026-04-26 同日延伸防御）|
| ✅ | **config-doctor 启动期诊断** | 用户装 v5.7.2 仍爆 'Context limit exceeded'，根因是 openclaw 配置陷阱（缺 reserveTokensFloor / model maxTokens 过大），enhance 主动诊断把信号给到用户 | Plugin 模块 + 工具 | ~200 行 | 已落地 **v5.7.3**（2026-04-26 同日，calendar 外第 3 次 hot-fix）|
| ✅ | **config-doctor 扩展扫已装插件 bare pluginApi** | 用户报"提示插件要求 2026.2.24"实际是其它插件违反 ">=X.Y.Z" 规则；扫所有装的 plugin package.json 检测 bare → 给 fix 命令 | Plugin 模块扩展 | ~80 行净增 | 已落地 **v5.7.4**（2026-04-26 同日，calendar 外第 4 次 hot-fix）|
| ✅ | **config-doctor 扫 channel-plugin 缺顶层 channelConfigs** | 修 wechat-service 的"channel plugin manifest declares ... without channelConfigs metadata"警告时，发现 enhance 已扫 bare pluginApi / async register / 旧版 tool 字段三类反模式但漏了这条；扫 manifest 顶层 channels[] 与 channelConfigs，找出未覆盖的 channelId 给可粘贴 patch 示例 | Plugin 模块扩展 | ~70 行净增 | 已落地 **v5.7.25**（2026-05-01，calendar 外 fast-track，跟 wechat-service v2.2.1 hotfix 同期）|
| ✅ | **skill-recommender 按需求自动挑 skill** | 用户提"看看 Claude 是怎么做的"——反编译发现 Claude Desktop 就是 name+description 注入 system prompt 让 LLM 挑；enhance 改成按需工具：扫多路径（含 WeCom workspace-*）+ CJK 双字滑窗 + alias 强 boost + 三段式（已装 / 未装 / 自建规划） | Plugin 模块 + 工具 | ~270 行 | 已落地 **v5.7.5/6**（2026-04-26 同日第 5 次）|
| ✅ | **session-lifecycle 接 openclaw 4.22 五个 hook** | 用户要求"结合 claude 官网+本地源码看 enhance 还能补啥"——跑完整 SOP 发现 openclaw 4.22 暴露 29 hook，enhance 只用 4 个；接 session_start/end/before_reset/subagent_*/ended 闭环生命周期 | Plugin 模块 | ~250 行 | 已落地 **v5.7.7**（2026-04-26 同日第 6 次）|
| ✅ | **全面适配 openclaw 4.24（typed hooks + manifest 元数据）** | 用户要求"enhance 帮我全面适配 openclaw 最新版"——发现 api.on 是完全 typed 但 enhance 14 处 as any 屏蔽；全部清理 + 升 peerDep + 加 enabledByDefault/uiHints/activation | Plugin 全面适配 | ~600 行 diff | 已落地 **v5.7.8/9**（2026-04-26 同日第 7 次）|
| ❌ | **tool-result-optimizer**（接 tool_result_persist 大结果截断+摘要）| openclaw 4.22 hook | ~~Plugin 模块~~ | ~~~100 行~~ | **2026-04-27 调研判定：违反红线 #2 — openclaw 4.24 已内置 `truncateToolResultMessage / truncateToolResultText / maxSingleToolResultChars`（在 wait-for-idle-before-flush bundle 里），compaction 阶段会按需截断；plugin 重做就是复制原生功能。Skip。** |
| 2 | **artifacts 多版本管理（轻量）** | Claude Desktop artifacts 表 | Plugin 模块 + SQLite | ~250 行 | 待选（v5.8）|
| 3 | **frames 父子 session 关系** | Claude Desktop frames 表 | Plugin 模块 + SQLite | ~150 行 | 待选（v5.8）|
| 4 | **auto-memory-curator cron 触发** | enhance 已有 skill，缺定时器 | Plugin 模块 | ~40 行 + cron 命令 | 待选 |
| 2 | **path-rules**（plan/explore 写入静态参数白名单）| Claude Code Settings | Plugin 模块 | ~150 行 | 待选 |
| 3 | **WeCom push notification 桥接** | Claude Code Notifications | Plugin 模块 + WeCom webhook | ~100 行（需 @huo15/wecom 协作）| 待选 |
| 4 | **skill-creator** skill | Claude Code 内置 skill | **Skill**（先发 ClawHub 再让 enhance 引用）| 半天 | 待选 |
| ❌ | **less-permission-prompts** skill | Claude Code 内置 skill | ~~**Skill**~~ | ~~半天~~ | **2026-04-27 obsolete — Claude Code 2.1.111 (April 15) 已内置 `/less-permission-prompts` 为 bundled skill。再造就是复制 Claude Code 原生。Skip。** |
| 6 | **init-soul** skill | Claude Code 内置 skill | **Skill** | 半天 | 待选 |
| 7 | **cowork artifact**（多 agent 协作产物管理）| Claude Desktop coworkArtifact.js | Plugin 模块（待调研）| 1 天 | 待选 |

**ROI 排序原则**：

1. **有现成实现可参考**（如 transcript-search 有 Claude Desktop worker）> 凭空设计
2. **Plugin 模块** ROI 通常 > Skill（Plugin 改一次所有 agent 受益，Skill 要语义召唤）
3. **解决用户实测痛点**（如 long session 找不回历史）> 锦上添花
4. **完全非侵入**（只读 / 自建数据）> 需要 hook 配合
5. **代码量 < 200 行**（一次能写完）> 大工程

---

## 3. 标准迭代流程（每 3 天一次）

### Step 1 — 信息更新（10–15 min）

```bash
# 1. 拉最新 docs（用 WebFetch 或浏览器）
#    最常变化的页：hooks / skills / sessions / modes / recent-additions

# 2. 重装 Claude Code 到最新（看 sdk-tools.d.ts 有没有新 type）
npm i -g @anthropic-ai/claude-code

# 3. 检查 Claude Desktop 有没有自动更新
ls -la /Applications/Claude.app/Contents/Info.plist | head -3
```

### Step 2 — Gap 比对（15–30 min）

```bash
# 列 enhance 当前的 hook + tool 注册
grep -RnE 'api\.(on|registerTool|registerMemory)' \
  /Users/jobzhao/workspace/projects/openclaw/huo15-openclaw-enhance/src \
  /Users/jobzhao/workspace/projects/openclaw/huo15-openclaw-enhance/index.ts

# 列 Claude Code SDK 的所有 hook + tool 类型
grep -E '^(export|tool: ")' \
  ~/.nvm/versions/node/$(node -v | tr -d v)/lib/node_modules/@anthropic-ai/claude-code/sdk-tools.d.ts \
  | head -60
```

把当前候选池里的 #1–#7 与最新清单 diff，更新候选状态。

### Step 3 — 选 1 个 ROI 最高的落地（1–4 h）

按下面的 Plugin vs Skill 决策树挑形态：

```
新需求来了 →
├─ 用户一句话召唤 + 单次输出？           → Skill
├─ 需要 hook / 跨 session 状态 / DB？    → Plugin
├─ 用户可能不装 plugin 也想用？          → Skill
└─ 形态混合？                            → Plugin（主动）+ Skill（人工召唤）
```

### Step 4 — 发布（半小时）

**Plugin 模块发布（v5.X.Y）**：

```bash
cd /Users/jobzhao/workspace/projects/openclaw/huo15-openclaw-enhance
# typecheck
npx tsc --noEmit
# bump 版本（package.json + openclaw.plugin.json + SKILL.md + CHANGELOG.md + README.md）
# commit + tag + push
git push origin main && git push origin vX.Y.Z
git push github main && git push github vX.Y.Z
# 双发布
npm publish --access public "--//registry.npmjs.org/:_authToken=npm_<TOKEN>"
CLAWHUB_TOKEN=clh_<TOKEN> clawhub publish . --workdir . --dir . --version X.Y.Z --tags latest,plugin
```

**Skill 发布（必须先 ClawHub 后插件引用，⚠️ 用户硬要求）**：

```bash
# 1. 先在 huo15-skills 仓库写 skill
cd /Users/jobzhao/workspace/projects/openclaw/huo15-skills
# 编辑 huo15-openclaw-<name>/SKILL.md 等

# 2. 发布到 ClawHub
CLAWHUB_TOKEN=clh_<TOKEN> clawhub publish ./huo15-openclaw-<name> --version 1.0.0

# 3. 等 ClawHub 索引可见（搜索能找到）
clawhub search huo15-openclaw-<name>

# 4. 然后到 enhance 仓库 src/modules/skill-installer.ts 把 slug 加到 CLAW_HUB_SKILLS
#    src/modules/skill-doctor.ts 同步加到 EXPECTED_SKILLS
#    bump enhance 版本 → 走上面的 plugin 发布流程
```

⚠️ **绝对不要在插件代码里内嵌 skill 内容**。Skill 必须独立发版，插件只引用 slug。

### Step 5 — 沉淀（10 min）

更新两处：

1. **本仓库 `docs/SELF_ITERATE.md`** 候选池 — 把已落地的标 ✅，新发现的加进去
2. **本地 KB `~/knowledge/huo15/`** — 一次发布写一篇 markdown 完整 post-mortem（含 design 决策、实测数据、踩过的坑）

---

## 4. 历史迭代记录

| 日期 | 版本 | 主题 | 来源 | 落地形态 |
|------|------|------|------|---------|
| 2026-04-23 | v5.4.0 | 设计能力套件（4 个 skill） | huashu-design + Anthropic frontend-design | 4 Skills |
| 2026-04-24 | v5.5.0 | 三层记忆/KB 协调（corpus="kb"） | Claude Code memory 文档 | Plugin 模块 |
| 2026-04-24 | v5.5.1 | 开发辅助三件套 + session-recap | Claude Code /simplify /security-review /review + idle recap | 3 Skills + 1 Plugin 模块 |
| 2026-04-24 | v5.6.0 | 工具分层 + workflow 5→2 + 描述压缩 | Long session context pressure 实测 | Plugin 容量优化 |
| 2026-04-25 | v5.7.0 | transcript-search（流式扫 jsonl） | 反编译 Claude Desktop transcriptSearchWorker | Plugin 模块 |
| 2026-04-26 | v5.7.1 | hot-fix：删 before_compaction 噪音 hook + 加 memory_purge | 用户实测 enhance 库 613 条全为 auto-compact 噪音 | Plugin hot-fix |
| 2026-04-26 | v5.7.2 | hardening：Map LRU + safety_log TTL + corpus tag 黑名单 + peerDep 4.22 | Explore agent 全代码审计后挑 4 项 ROI 最高的批量修 | Plugin patch |
| 2026-04-26 | v5.7.3 | config-doctor：启动期诊断 openclaw.json 陷阱（reserveTokensFloor 缺失 / model maxTokens 过大）| 用户实测装 v5.7.2 仍爆 'Context limit exceeded'，根因在 openclaw 配置而非插件 | Plugin 模块 |
| 2026-04-26 | v5.7.4 | config-doctor 扫已装插件 bare pluginApi | 用户报"插件要求 2026.2.24"实际是其它插件违反 ranged spec 规则 | Plugin 模块扩展 |
| 2026-04-26 | v5.7.5/6 | skill-recommender：按需求挑已装 skill / 推荐未装 / 给自建规划 | 用户提"看看 Claude 是怎么做的"——反编译 Claude Desktop loadSkills 启发 | Plugin 模块 |
| 2026-04-26 | v5.7.7 | session-lifecycle：接入 openclaw 4.22 的 session_start/end/before_reset/subagent_*/ended 五个 hook 闭环生命周期 | 跑完整 SOP 发现 openclaw 4.22 暴露 29 hook，enhance 只用 4 个；ROI top 5 候选 #1 | Plugin 模块 |
| 2026-04-26 | **v5.7.8/9** | **全面适配 openclaw 2026.4.24（typed hooks + manifest 元数据）** | **用户要求"全面适配最新版"——发现 api.on 完全 typed 但 enhance 14 处 as any 屏蔽** | **Plugin 全面适配** |
| 2026-04-27 | _no release_ | **本轮无新增**：跑完整 SOP，候选池 #1 (tool-result-optimizer) 调研发现违反红线 #2（openclaw 4.24 已内置截断）；候选池 #5 (/less-permission-prompts) 已被 Claude Code 2.1.111 内置；其它候选都 ≥ 250 行不适合 calendar 内吞。距 v5.7.9 仅 ~6 小时，避免 release fatigue。锚点推到 2026-04-30。 | Claude Code 2.1.108→2.1.119 + Claude Desktop 2026-04-24 build sweep | **Doc-only 沉淀** |

下一次迭代锚点：**2026-04-30**（推迟 2 天；2026-04-27 跑完判定无新增后顺延；如果有新 Claude Code release 或线上 bug 反馈提前触发）。

### 2026-04-27 sweep 关键发现（doc-only 迭代）

**Claude Code 2.1.108 → 2.1.119（April 14–23 之间 11 个 patch）vs enhance 适用性**：

| Claude Code 新增 | 对 enhance 影响 |
|---|---|
| `/recap` 内置 (2.1.108) | enhance 已有 session-recap 模块，但路径不同（idle-detect injection vs 显式命令）。不冲突 |
| `/less-permission-prompts` 内置 (2.1.111) | 候选池 #5 标 obsolete（见上） |
| `/ultrareview` 内置 (2.1.111) | 不冲突，不补 |
| Push notification tool (2.1.110) | 候选池"WeCom push 桥接"可参考——但 push tool 是 Claude Code 自家，openclaw 没暴露 |
| PreCompact hook 标准化 (2.1.105) | enhance v5.7.1 已经移除 before_compaction 噪音 hook。无变 |
| Forked subagents `CLAUDE_CODE_FORK_SUBAGENT=1` (2.1.117) | Claude Code 特性，openclaw 子 agent 系统已独立；不补 |
| Hooks `duration_ms` (2.1.119) | Claude Code hook 系统，非 openclaw hooks。不补 |
| Skill `paths` 字段（按文件类型自动激活）| **Skill 侧改进**——huo15-* skill 可考虑加（如 huo15-openclaw-frontend-design 限 .tsx/.css）。属于 huo15-skills 仓库工作，不是 enhance 工作 |
| MCP `_meta["anthropic/maxResultSizeChars"]` 上限 500K (2.1.91, 4-2) | 证明大 tool result 是真实痛点——但 openclaw 已自带 `maxSingleToolResultChars` 内置截断（见候选池 #1 ❌） |

**openclaw 4.24 hook 完整清单 vs enhance 已用对比**（29 hook 中 enhance 用 9 个）：

| 已用 | 未用但有过候选/ROI | 未用且不适合 |
|---|---|---|
| before_prompt_build, before_agent_reply, before_reset, before_tool_call, after_tool_call, session_start, session_end, subagent_spawned, subagent_ended | tool_result_persist (❌ 见上)、subagent_spawning (overlap mode-gate)、agent_end (overlap session-recap idle)、before_message_write (overlap mode-gate)、before_install (overlap skill-doctor) | llm_input/output (太重)、inbound_claim/message_*/gateway_*/before_dispatch/reply_dispatch (route 层，非 enhance 关心) |

结论：**enhance 已用 9 个 hook 已经覆盖核心场景**；剩余 hook 要么 overlap 已有模块，要么不适合。

**Claude Desktop app.asar mtime = 2026-04-24** —— 跟 v5.7.x 那一轮反编译看的是同一个 build，没新东西。

### 关于"什么时候应该回报无新增"

每次跑这套 SOP 都硬塞迭代会累积"reschedule debt"——给候选池里塞次优的、给版本号小数点位填，最后变成又一次 `chore: bump npm-tracking 5.7.x → 5.7.x+1`。**正确做法是给"本轮调研报告 + 推后下次锚点"留出口**。判定规则：

1. 跑完 Step 2 gap 分析后，所有候选要么 hit 红线、要么估算 > 200 行（calendar 内不吞）、要么距上一次发版 < 12 小时（release fatigue）
2. → 回报"本轮无新增"
3. → SELF_ITERATE.md 历史表加一行（_no release_ 标记）
4. → 候选池里把已标 obsolete 的划 ❌（含理由），把还活着的更新状态
5. → 下次锚点 +3 天
6. → KB 写 post-mortem 沉淀这一轮的"为什么不做"

### 关于"诊断 vs 修复"的边界

v5.7.3 严格遵守"**诊断不修复**" — 即便 enhance 完全有能力 read/write `~/.openclaw/openclaw.json`，也只 `readFileSync` 不 `writeFileSync`。理由：
1. 红线 #1：不侵入式修改 openclaw（配置文件属于 openclaw 控制范围）
2. 用户对配置的掌控感 — 自己复制粘贴一行 python3 命令，至少看到改了啥
3. 排除责任 — 万一 fix 命令出错（比如把字段值打错），损失只是用户那一刻的副作用，不会让 enhance 担责"我装了插件配置就被改坏了"

**未来若加任何"建议改 openclaw 配置"的功能，硬约束：return-cliCmd 模式（输出 fix 命令字符串），永不 fs.writeFileSync 用户配置**。

### 发版前自查 checklist（v5.7.4 启示）

每次发布 plugin 前必跑：

```bash
# 1. 自查本插件 compat.pluginApi 是 ranged
grep -E '"pluginApi"' package.json openclaw.plugin.json
#   必须看到 ">=X.Y.Z" / "^X.Y.Z" / "~X.Y.Z"
#   绝不能看到裸的 "X.Y.Z" — 那会被 openclaw 解读为精确匹配

# 2. typecheck
npx tsc --noEmit

# 3. 跑一次本地 enhance_config_doctor 看自己安装目录有没有 bare plugin
#    （拿到 v5.7.4+ 之后此项自动）
```

为什么这条这么重要：v5.7.4 修的 bug 就是其它两个 huo15 插件作者（包括我自己）写 bare 字符串的失误造成的。**bare pluginApi 是 silent breakage** — 当时跑得好好，运行时一升级 openclaw 就炸。每次发版都自查能避免下个用户遭罪。

### 关于 hot-fix 的额外约束（v5.7.1 启示）

线上 bug（用户截图反馈）属于 **calendar 外触发** — 不等 cron 任务，立刻按照下面 fast-track 流程处理：

1. 用 Grep 直接定位 bug 代码（不要 Plan）
2. 修复 + typecheck（不要 release plan）
3. SQL 直接清用户残留数据（如本次 613 条），先 `cp ... .bak.before-vX.Y.Z-hotfix` 备份
4. 走标准发布流程（commit → tag → push 双 remote → npm + clawhub）
5. 把 bug 加进 SELF_ITERATE.md 候选池标 ✅，写一篇 KB post-mortem
6. 不影响下次 cron 调度（cron 还是 2026-04-28 跑）

---

## 5. 红线清单（永远不踩）

1. ❌ 不修改 openclaw 核心代码 / 不动 openclaw 仓库
2. ❌ 不复制龙虾原生功能（记忆向量库、tools.allow/deny、cron 调度、技能安装）
3. ❌ 插件代码里不内嵌 skill 内容（skill 必须独立发版到 ClawHub）
4. ❌ 不用 child_process（企业扫描器拦截 — 见 KB「No child_process in published plugins」）
5. ❌ 不在 plugin 里写 npm/pip/cli 一类的安装命令执行（必须用 return-cliCmd 模式让用户 / cron 执行）
6. ❌ ClawHub publish 不要一小时内发 5 个以上 new slug（rate limit）
7. ❌ 提交不带 secrets（即使是 publish-credentials.md 里的 token，不出现在 commit message 或 code）
