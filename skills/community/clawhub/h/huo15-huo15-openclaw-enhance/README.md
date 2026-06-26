# 火一五·克劳德·龙虾增强插件

---

<div align="center">

<img src="https://tools.huo15.com/uploads/images/system/logo-colours.png" alt="火一五Logo" style="width: 120px; height: auto; display: inline; margin: 0;" />

</div>

<div align="center">

<h3>打破信息孤岛，用一套系统驱动企业增长</h3>
<h3>加速企业用户向全场景人工智能机器人转变</h3>


</div>
<div align="center">

| 🏫 教学机构 | 👨‍🏫 讲师 | 📧 联系方式         | 💬 QQ群      | 📺 配套视频                         |
|:-----------:|:--------:|:------------------:|:-----------:|:-----------------------------------:|
| 逸寻智库 | Job | support@huo15.com | 1093992108  | [📺 B站视频](https://space.bilibili.com/400418085) |

</div>
---

## 简介

**火一五·克劳德·龙虾增强插件 v6.0.0** 是 [OpenClaw 2026.4.24+](https://github.com/openclaw/openclaw) 的**非侵入式**增强插件，对标 Claude Code 的 Agent Harness 体验 + 设计能力套件 + 开发辅助套件；**所有能力重叠处都以龙虾为准**，绝不复制或覆盖龙虾原生功能。

完全通过公共 Plugin SDK 实现，**不修改任何核心代码**，一键安装即可使用。
（非龙虾团队开发）

### v6.0.0 npm 包改名 + ClawHub 重新注册（2026-05-02）

> **BREAKING（npm 包名）**：`@huo15/openclaw-enhance` → `@huo15/huo15-openclaw-enhance`

老 npm 包对应的 ClawHub slug `huo15-openclaw-enhance` 上有 ghost manifest 死结——1.3.0-5.1.0 期间 27 个版本 pluginApi=bare `2026.2.24`（早于本仓 §6.1 红线"compat.pluginApi 必须 ranged"修复），ClawHub plugin entry record 在那段历史首次注册时缓存了 bare 值，后续 publish 不刷新 record 字段，OpenClaw 走 `clawhub:` 协议解析时永远拿到老 manifest 报 `requires plugin API 2026.2.24`。

**修复**：换 npm 包名（与 `huo15-huihuoyun-odoo` 等 huo15-* 命名规范对齐）+ 新 ClawHub slug `huo15-huo15-openclaw-enhance`，让 ClawHub 重新创建一个干净的 plugin entry。OpenClaw plugin id 仍是 `enhance`，老用户配置不需迁移。详见 [CHANGELOG.md](./CHANGELOG.md) v6.0.0 段。

老 npm 包已 deprecate；老 ClawHub slug 已 hide。已装老版本用户跑[迁移命令](#老版本用户迁移v5x--v600)即可。

### v5.7.24 BOT 文件分享 URL 改成独立兄弟 prefix（2026-05-01）

URL 从 v5.7.23 的 `/plugins/enhance/share/...`（dashboard 子路径，靠 bridge dispatch）改成 v5.7.24 的 `/plugins/enhance-share/...`（独立 SDK prefix route，不依赖 dashboard）。

| 维度 | v5.7.23 | v5.7.24 |
|---|---|---|
| URL | `https://<域>/plugins/enhance/share/<token>-...` | `https://<域>/plugins/enhance-share/<token>-...` |
| 路由实现 | dashboard handler 顶部 `tryHandleSubRoute` 转给 bridge 注册的 share handler | bot-share-link 自己 `api.registerHttpRoute({ path: "/plugins/enhance-share", ... })` |
| dashboard.ts 改动 | +3 行（dispatch + detect） | 1 行（detect only），跟 v5.7.22 同 |
| bridge 复杂度 | 102 行 | 76 行（去掉 dispatch 相关） |

**SDK overlap 规则**：`prefixMatchPath` 用的是 `startsWith(\`${prefix}/\`)`，分隔必须是 `/`。所以 `/plugins/enhance-share` ≠ `/plugins/enhance` 的子前缀（中间是 `-`），SDK 不会拒绝。

**baseUrl 自动检测仍 zero-config**：dashboard handler + share handler 都调 `detectBaseUrlFromRequest(req)` 抓 host，访问过任一即缓存。

### v5.7.23 BOT 文件分享桥升级 zero-config（2026-05-01）

复用 dashboard 已经在跑的 `/plugins/enhance` prefix route，通过新增的 [http-route-bridge](src/utils/http-route-bridge.ts) 子分发到 `/plugins/enhance/share/<token>-<filename>`。**v5.7.24 已替换为独立兄弟 prefix 方案，不再 dispatch。**

### v5.7.22 BOT 文件分享桥：企微/钉钉大文件兜底（2026-05-01）

**用户痛点**：播客生成 90MB mp3，企微插件直接传不了；钉钉同样卡死大文件。需要把本地文件投到一个目录、返回临时下载 URL 给用户自取。

**三个工具**（tier=1，全分层都暴露）：

| 工具 | 作用 |
|---|---|
| `enhance_share_file(filePath, label?, expireHours?, copyMode?)` | 把本地文件投递到 `<shareRoot>/files/<token>-<basename>`，返回临时 URL（默认 24h 过期） |
| `enhance_share_list()` | 列当前活跃分享 + 顺手清过期 |
| `enhance_share_revoke(token \| filename)` | 立刻撤销（删本地文件 + manifest 条目） |

**安全闸门**：路径黑名单（`/.ssh/ /.aws/ /.gnupg/ /etc/` 等不让分享）、绝对路径校验、`..` 防 traversal、500MB 大小上限、12 hex token 不可枚举遍历、HTTP handler 内 filename 防越界（不能含 `/ \\ ..`）。**零 child_process**（fs.copyFileSync），lazy cleanup（不在 register 期跑后台任务）。

### v5.7.12 model-router: 速度+精度+覆盖率三重增强（2026-05-01）

**1. 响应速度**：路由决策缓存（TTL 30s）、极短 prompt 短路（<50 字符直走 M2.7）、`getBestModel` 结果缓存

**2. 任务识别精度**：超长 prompt（>2000 字符）→ 直接 pro；写作/摘要按长度分叉（短→flash，长→pro）；中文关键词专项优化

**3. 新增 12 类任务识别**：翻译/写作/数据分析/debug/情绪/数学/摘要/检索/闲聊/报告/多步骤/快速问答

### v5.7.11 model-router: 修复 WeCom 图片路由到 MiniMax-VL-01（2026-04-30）

**用户反馈**："图片路由到 M2.7 报 content empty，M2.7 是 text-only 模型不支持图片"

问题根因：`detectPromptInlineMedia` 只检测 `[image]` 和 `[media attached` 标记，但 WeCom 图片到达时 prompt 里只有文件路径（`~/.openclaw/media/inbound/xxx.png`），没有这些标记，导致图片检测失败，一直路由到 text-only 的 M2.7。

修复：在 `detectPromptInlineMedia` 中新增 WeCom 媒体路径格式检测——任何包含 `~/.openclaw/media/inbound/*.png|jpg|jpeg|gif|webp|bmp` 的 prompt 都会被识别为图片，自动路由到 `MiniMax-VL-01`（vision 模型）。

| 场景 | 修复前 | 修复后 |
|---|---|---|
| WeCom 发图片 | 路由到 M2.7 → API 报 content empty | 路由到 VL-01 → 正常识别 |

### v5.7.8 全面适配 openclaw 2026.4.24（2026-04-26 同日）

| 维度 | 改动 |
|---|---|
| `peerDependencies.openclaw` | `^2026.4.22` → **`^2026.4.24`** |
| `build.openclawVersion` | `2026.4.11` → **`2026.4.24`** |
| `compat.pluginApi` | `>=2026.4.11` → **`>=2026.4.24`** |
| `api.on(...as any)` 14 处 → **0 处** | 全部改成 typed hook，让 SDK PluginHookHandlerMap[K] 自动推断 event/ctx |
| `(event: any, ctx: any)` 5 处 → **0 处** | 同上 |
| `openclaw.plugin.json` 加 3 字段 | `enabledByDefault: true` / `uiHints` / `activation.onAgentHarnesses` |
| 修隐藏 bug | self-check.ts 的 `PluginHookBeforeAgentReplyResult.handled` 必填问题之前被 `as any` 屏蔽，现在 typecheck 强制修对 |

### v5.7.7 session-lifecycle：接入 openclaw 4.22 五个 hook 闭环 session 生命周期（2026-04-26 同日）

跑了完整 SOP 第 1+2 步后发现 **openclaw 4.22 暴露 29 个 hook，enhance 只用了 4 个**。落地最高 ROI 的 5 个 hook：

| Hook | 行为 |
|---|---|
| `session_start` | idle > 30min 时插入"🚀 会话开始/续启"章节占位 |
| `session_end` | 加"🏁 会话结束"章节 + flush in_progress todo 到 project memory |
| `before_reset` | reset 前抢救最近 3 章节 + 全部未完成 todo 到 decision memory + 推 notification |
| `subagent_spawned` / `subagent_ended` | 派生/结束自动落 chapter（跟 enhance_spawn_task 闭环）|

防 noise factory 三层防御：30 秒 dedup + 低 importance + 专用 tag（吸收 v5.7.1 教训）。

### v5.7.5 skill-recommender：按需求挑 skill / 推荐未装 / 给自建规划（2026-04-26 同日）

调研：反编译 Claude Desktop 发现 skill auto-discovery 本质是 `"Available skills: ${list}."` 注入到 system prompt。enhance 改成**按需工具**避免每轮 prompt 占 schema：

工具 `enhance_skill_recommend(query, ...)` 三段式输出：

| 段 | 内容 | 触发条件 |
|---|---|---|
| 🎯 已装 skill | 按相关度排序 + 召唤建议 | 命中 ≥ threshold |
| 📦 ClawHub 未装候选 | 11 个 huo15-* + `openclaw skills install <slug>` | 默认包含 |
| 🛠️ 自建规划 | slug + frontmatter 模板 + 触发词 + 内容大纲 + 红线 #3 提醒 | 已装命中 < threshold |

实测精度：

| 查询 | 命中 | 分数 |
|---|---|---|
| "帮我 review 这个 PR" | huo15-openclaw-code-review | 0.60 |
| "代码简化" | huo15-openclaw-simplify | 1.00 |
| "做安全审查" | huo15-openclaw-security-review | 0.96 |

关键修复：扫 `~/.openclaw/workspace-*/skills/`（WeCom 多 agent 隔离的子工作区）— 用户机器实测扫到 **56 个 skill 跨 27 个路径**。

### v5.7.4 config-doctor 扩展：扫已装插件 bare pluginApi（2026-04-26 同日）

用户反馈："提示插件要求 2026.2.24，但是我的 openclaw 已经是 2026.4.22" — 这是**其它插件**的 `compat.pluginApi` 写成 bare 字符串（精确匹配）导致 openclaw 启动失败。enhance 主动扫所有装的 plugin package.json，检测违规并给 fix 命令。

实测命中：
- `~/.openclaw/extensions/tips/package.json` v1.0.0 → `pluginApi: "2026.4.11"`（bare）
- `~/.openclaw/node_modules/@huo15/huo15-huihuoyun-odoo/package.json` v1.2.0 → `pluginApi: "2026.2.24"`（bare）

### v5.7.3 config-doctor（2026-04-26 同日，继 v5.7.2）

直击高频反馈"装上插件还是 'Context limit exceeded'"。**这不是 enhance 的锅**，是 openclaw 自身配置陷阱：

- **缺失 `agents.defaults.compaction.reserveTokensFloor`** — openclaw 4.22 把字段从顶层 `compaction.*` 挪到嵌套路径，老用户配置文件没自动迁移 → 用 4.22 默认值（很小） → 长 session 必爆
- **某 model maxTokens ≥ contextWindow/2** — 例如 MiniMax-M2.7 默认 maxTokens=131072 / contextWindow=204800，每轮预留输出吃 64% budget → 剩 73k 给 input/tools/memory/history 几轮必爆

**新增 `enhance_config_doctor` 模块（tier=1，minimal 也启用）**：

- 启动期 sync 读 `~/.openclaw/openclaw.json` 检查上述两类陷阱
- 发现问题：log warn + 推仪表盘通知 + 给可粘贴 fix 命令（python3 inline JSON 改写，**不调 child_process**，**不擅自改用户配置**）
- 工具 `enhance_config_doctor` 按需重检（修完用来确认 ✅）

### v5.7.2 hardening（2026-04-26 同日，继 v5.7.1）

对全代码库做了一次审计，修 4 类潜在 bug + 升 peerDep `^2026.4.22`：

- **进程内 Map LRU 上限** — `mode-gate` / `session-recap` 之前跨 session 永不清，多 agent 场景会泄漏；现在加 200/200/500 三档 cap + FIFO 淘汰
- **safety_log / notifications 启动期 TTL** — `getDb()` 自动清 90 天前旧记录
- **memory corpus tag 黑名单** — `auto-compact / auto-checkpoint / audit / internal` 永不召回，防御未来 noise hook
- **enhance_memory_store 拒收保留 tag** — 用户/agent 显式滥用保留词时立即报错

### v5.7.1 hot-fix（2026-04-26）

**修：删除把每次 auto-compact 事件作为 decision 类记忆插入的 `before_compaction` hook。**

- 之前实测单 agent 24h 积累 **613 条全为噪音**（tag=auto-compact），关键词命中率 0.43-0.51 普遍过 0.5 阈值，把真正的决策记忆挤出 prompt 上下文
- 新增工具 `enhance_memory_purge` — 按 `tag` / `category` / `contentLike` 批量清理，`dry_run` 默认 true（仅预览匹配数）
- 历史噪音清理一行：`enhance_memory_purge tag="auto-compact" dry_run=false`，或 `sqlite3 ~/.openclaw/memory/enhance-memory.sqlite "DELETE FROM memories WHERE tags LIKE '%auto-compact%'; VACUUM;"`

### v5.7 新特性（2026-04-25）

**📜 历史会话搜索 — 照搬 Claude Desktop 实现**

> 反编译参考 `/Applications/Claude.app/Contents/Resources/app.asar` 里的 `transcriptSearchWorker.js`（94 行官方实现）— 发现 Claude Desktop 不用 SQL FTS5，纯流式扫 JSONL + indexOf。直接搬到 openclaw 的 `~/.openclaw/agents/<agent>/sessions/*.jsonl`。

| 工具 | 用途 | 实测性能 |
|------|------|---------|
| `enhance_transcript_search` | 全文搜历史会话，找『我上次怎么做的』 | 79 个 session 中扫 30 个 → **3-5 ms** 找到 5 hits |

参数：`query` 必填；可选 `agentId / limit (1-50) / includeReset / caseSensitive`。

模块 `tier=2`（balanced/full 默认启用，minimal 下不暴露）。

### v5.6 新特性（2026-04-24）

**针对 long session 提早爆 context 的容量优化**

| 配置项 | 暴露工具数 (v5.7) | 适用场景 |
|--------|-----------|---------|
| `toolTier: "minimal"` | 10 | 上下文极紧 / 最小核心模式（记忆、状态栏、章节、模式、spawn） |
| `toolTier: "balanced"` *(默认)* | 19 | 多数日常会话 — 加 todo / 章节标记 / 定时任务桥 / **transcript-search** |
| `toolTier: "full"` | 27 | 需要工作流自动化 / safety / session-recap / skill-doctor 时 |

- **工具分层（toolTier）** — 按需暴露 schema，每轮 prompt 减负
- **Workflow 5→2 工具合并** — 用 `action=` 派发器收敛同类操作
- **26 个工具描述压缩 -62%** — 每轮 prompt 节省约 1400 token

> ⚠️ 如果你的 `~/.openclaw/openclaw.json` 中 `compaction.reserveTokensFloor` ≥ 100000，请改回 **20000**（>205k 总窗会让每次压缩都失败）。这是 openclaw 配置项，与本插件无关。

### 核心特性

- **多 Agent 隔离** — 完美适配 WeCom 插件的动态 Agent 功能，每个企微用户/群组拥有独立的记忆、任务、章节、宠物与定时工作流
- **结构化记忆（corpus supplement）** — 按 user/project/feedback/reference/decision 五类分类存储，**通过 `registerMemoryCorpusSupplement` 并入龙虾 `memory` 搜索结果**，不自建第二套向量库
- **工具安全补丁** — 仅作为**观察员**存在（尊重龙虾原生 `tools.allow/deny`），统计错误分类、给出退避建议，从不擅自重试或硬拦截
- **提示词增强** — 仅保留 `qualityGuidelines`，其它早已由龙虾系统提示词覆盖，不重复
- **任务/章节/模式闸门** — Claude Code TodoWrite / mark_chapter / plan-explore 的龙虾化实现；模式闸门在 `before_tool_call` 阻止计划/探索模式误触写操作
- **状态栏 / 技能巡检 / 子任务孵化** — 一行看全当前状态；诊断技能目录缺失；把"现在不该做"的副作用登记为延期任务
- **定时任务桥** — 登记工作流时返回一条 `openclaw cron add` 命令，**调度归龙虾**，插件只负责触发时装填上下文
- **增强仪表盘（含小火苗宠物）** — Web UI 实时查看记忆 / 任务 / 章节 / 定时 / 宠物状态，支持按 Agent 筛选

---

## 一键安装

> ⚠️ **v6.0.0 起 npm 包改名**：`@huo15/openclaw-enhance` → `@huo15/huo15-openclaw-enhance`（与 `huo15-huihuoyun-odoo` 等其他 huo15-* 包命名规范对齐 + 让 ClawHub 重新创建干净的 plugin entry，绕开老 slug 1.3.0-5.1.0 期间 27 个 bare pluginApi 留下的 ghost manifest 死结）。OpenClaw plugin id 仍是 `enhance`，老用户配置 `~/.openclaw/openclaw.json` 里 `plugins.entries.enhance.*` 不需要迁移。

```bash
openclaw plugins install @huo15/huo15-openclaw-enhance --force
openclaw restart
```

### 老版本用户迁移（v5.x → v6.0.0）

如果你之前装了 `@huo15/openclaw-enhance`：

```bash
# 1. 卸载老 plugin（OpenClaw 内部 plugin id 是 enhance）
openclaw plugins uninstall enhance

# 2. 装新包（npm 包名变了，但 OpenClaw plugin id 还是 enhance）
openclaw plugins install @huo15/huo15-openclaw-enhance --force

# 3. 重启
openclaw restart
```

**配置兼容**：用户机器上 `~/.openclaw/openclaw.json` 里 `plugins.entries.enhance.config.*`（如 `botShare.baseUrl`）的 key 不需要改，因为 plugin id 还是 `enhance`。

老 npm 包 `@huo15/openclaw-enhance` 已 deprecate；老 ClawHub slug `huo15-openclaw-enhance` 已 hide（已装用户仍可 update 兜底，但搜索看不到）。详见 [CHANGELOG.md](./CHANGELOG.md) v6.0.0 段。

安装完成后访问仪表盘：`http://localhost:18789/plugins/enhance/`

---

## 功能模块（v5.6.0 全量，标注分层）

> 标注 `[L1/L2/L3]` 的是工具模块，分别在 minimal / balanced / full 三档下暴露给模型；非工具模块（仪表盘 / 提示词 / kb-corpus / 自检）一律常驻。

| 模块 | 分层 | 说明 | Agent 工具 |
|------|------|------|-----------|
| **分类记忆（并入龙虾搜索）** | L1 | user/project/feedback/reference/decision 五类；作为 corpus supplement 与龙虾 `memory` 合并排名 | `enhance_memory_store` `enhance_memory_search` `enhance_memory_review` |
| **状态栏** | L1 | 一行/详情/json 三格式快照（模式、任务、记忆、宠物、通知） | `enhance_statusline` |
| **子任务派发** | L1 | 返回可粘贴的 `openclaw agent` CLI 命令，跨 agent 派发 | `enhance_spawn_task` |
| **模式闸门** | L1 | plan / explore / normal；前两种下 `before_tool_call` 阻止写操作；含 ExitPlanMode 审批 | `enhance_set_mode` `enhance_current_mode` `enhance_exit_plan_mode` |
| **章节标记** | L2 | session 级「mark_chapter」 | `enhance_mark_chapter` `enhance_chapter_list` |
| **任务追踪** | L2 | Claude Code TodoWrite 语义；SQLite 持久化；会警告多 in_progress | `enhance_todo_write` `enhance_todo_update` `enhance_todo_list` |
| **定时任务桥** | L2 | 返回 `openclaw cron add` CLI 命令，尊重龙虾原生 cron-cli | `enhance_loop_register` `enhance_loop_list` `enhance_loop_disable` |
| **历史会话搜索（v5.7）** | L2 | 流式扫 `~/.openclaw/agents/<agent>/sessions/*.jsonl`，照搬 Claude Desktop 算法（无索引、无新表） | `enhance_transcript_search` |
| **工作流自动化（v5.6 合并）** | L3 | 触发词 → 行为指令注入；CRUD 收敛到单工具（action 派发） | `enhance_workflow` `enhance_task` |
| **工具安全观察** | L3 | 错误分类（429/5xx/网络）+ 指数退避建议；不拦截，不重试 | `enhance_safety_log` `enhance_retry_status` `enhance_safety_rules` |
| **任务规划** | L3 | 把多步任务拆解保存为 plan 工件 | `enhance_task_plan` |
| **会话回顾（75min idle）** | L3 | idle 自动 prependContext「上次到这儿」 | `enhance_session_recap` |
| **技能巡检** | L3 | 只读检查 11 个增强技能安装状态 + 给出 clawhub 修复命令 | `enhance_skill_doctor` |
| **技能安装器** | L1 | 返回 11 个配套 skill 的一键安装 CLI 命令（不执行） | `enhance_install_skills` |
| **记忆整合** | L1 | hook 注入：把命中的记忆与查询条件合成上下文片段 | `enhance_memory_consolidate` |
| **提示词增强** | — | 追加 `qualityGuidelines`，其它已由龙虾系统提示词覆盖 | 自动（hook 注入） |
| **共享知识库语料** | — | 桥接 `~/.openclaw/kb/shared/` 到龙虾 `memory_search`（corpus="kb"） | 自动（corpus supplement） |
| **输出自检** | — | 空响应/错误关键词检查 | 自动（after-response hook） |
| **增强仪表盘** | — | Web UI：记忆 / 任务 / 章节 / 定时 / 孵化子任务 / 小火苗 | `http://localhost:18789/plugins/enhance/` |

## 与龙虾原生的关系（设计契约）

| 能力 | 龙虾原生 | enhance 策略 |
|------|---------|--------------|
| 记忆向量库（LanceDB） | ✅ 龙虾负责 | **enhance 不自建**；改为 corpus supplement 并入搜索 |
| 记忆系统提示词 | ✅ 龙虾负责 | enhance 只在段落底部追加一行工具说明（如果龙虾提供 `registerMemoryPromptSupplement`） |
| 工具 allow/deny | ✅ 龙虾负责 | enhance 只**观察**结果、做错误分类；不拦截 |
| 任务清单 / 计划文件 | ⚠️ 无对应原语 | enhance 独立实现（SQLite），语义对齐 Claude Code |
| Cron 调度 | ✅ 龙虾 cron-cli | enhance 不管理调度；只在触发时注入 instructions |
| 技能安装 | ✅ ClawHub | enhance 只读巡检，不擅自安装 |

---

## 增强技能

安装时会自动注入 8 个增强技能到 `workspace/skills/`（4 个工作流 + 4 个设计）：

### 工作流模式

| 技能 | 说明 | 灵感来源 |
|------|------|---------|
| `huo15-openclaw-plan-mode` | 结构化规划模式 — 执行复杂任务前先做需求分析、方案设计、风险评估 | Claude Code Plan Agent |
| `huo15-openclaw-explore-mode` | 深度探索模式 — 只读调研代码库/系统/话题后再给出结论 | Claude Code Explore Agent |
| `huo15-openclaw-verify-mode` | 验证检查模式 — 检查工作成果、运行测试、验证假设 | Claude Code Verification Agent |
| `huo15-openclaw-memory-curator` | 记忆整理 — 定期审查记忆、提取洞察、清理过期条目 | Claude Code auto-memory |

### 设计能力（v5.4 新增）

| 技能 | 说明 | 灵感来源 |
|------|------|---------|
| `huo15-openclaw-frontend-design` | 高保真 Web UI 原型 + 5 美学流派 + 反 AI Slop 硬红线 + Junior/Full 两趟渲染 | Anthropic frontend-design skill |
| `huo15-openclaw-design-director` | 设计方向顾问 — 5 流派 × 20 哲学 → 3 方向反差对比 + 强制推荐 | huashu-design 方向选型模式 |
| `huo15-openclaw-brand-protocol` | 品牌规范抓取 — Ask/Search/Download/Verify/Codify 5 步 → brand-spec.md | huashu Brand Protocol 5-step |
| `huo15-openclaw-design-critique` | 5 维设计评审 — 美学/可用性/品牌/内容/实现 + Keep/Fix/Quick Wins 三分类 | Web Design review 社区共识 |

---

## 配置说明

在 `openclaw.json` 的 `plugins.entries.enhance.config` 中配置各模块：

```json
{
  "plugins": {
    "allow": ["enhance"],
    "entries": {
      "enhance": {
        "enabled": true,
        "config": {
          "toolTier": "balanced",
          "memory": {
            "enabled": true,
            "autoCapture": true,
            "maxContextEntries": 5
          },
          "safety": {
            "enabled": true,
            "rules": [
              { "tool": "exec", "pattern": "rm -rf *", "action": "block", "reason": "危险命令" },
              { "tool": "exec", "pattern": "sudo *", "action": "block", "reason": "禁止 sudo" },
              { "tool": "file_write", "pathPattern": "*.env", "action": "block", "reason": "禁止写入环境变量文件" }
            ],
            "defaultAction": "allow"
          },
          "prompt": {
            "enabled": true,
            "sections": ["qualityGuidelines", "memoryContext"]
          },
          "workflows": { "enabled": true },
          "dashboard": { "enabled": true }
        }
      }
    }
  }
}
```

### `toolTier`（v5.6 新增）

| 取值 | 工具数 | 暴露的工具模块 | 适用场景 |
|------|--------|----------------|----------|
| `"minimal"` | 10 | 记忆 + 状态栏 + spawn + 模式 + 章节安装器 + integrator | 上下文紧 / 长会话 / 极简核心 |
| `"balanced"` *(默认)* | 19 | minimal + todo + 章节标记 + 定时任务桥 + **transcript-search (v5.7)** | 多数日常使用 |
| `"full"` | 27 | 全部，含 workflow / safety / task-planner / session-recap / skill-doctor | 工作流自动化 / 完整 harness |

修改 `toolTier` 后需要 `openclaw restart` 才能生效。

### 安全规则配置

| 字段 | 说明 |
|------|------|
| `tool` | 工具名称，支持通配符（如 `exec`、`file_*`） |
| `pattern` | 参数匹配模式，支持通配符（如 `rm -rf *`） |
| `pathPattern` | 文件路径匹配模式（如 `*.env`、`/etc/*`） |
| `action` | 匹配后动作：`block`（拦截）/ `log`（记录）/ `allow`（放行） |
| `reason` | 规则说明（可选） |

### 提示词段落配置

可选段落：`taskClassification`（任务分类）、`qualityGuidelines`（质量指引）、`memoryContext`（记忆上下文）、`safetyAwareness`（安全意识）

---

## 与 WeCom 动态 Agent 配合

当 WeCom 插件启用 `dynamicAgents` 后，每个用户/群组被分配独立的 `agentId`（如 `wecom-acct-ws-dm-hidaomax`）。增强包自动实现：

1. **记忆隔离** — 用户 A 存的记忆，用户 B 看不到
2. **日志隔离** — 每个用户的安全事件独立记录
3. **工作流隔离** — 用户 A 定义的工作流不影响用户 B
4. **上下文隔离** — 提示词增强只注入当前用户的记忆

**实现原理**：
- 工具使用 `OpenClawPluginToolFactory` 模式，从 `ctx.agentId` 获取当前 Agent
- 钩子从 `ctx.agentId` 获取当前 Agent
- SQLite 所有表包含 `agent_id` 列，查询时自动按 Agent 过滤

仪表盘支持 `?agent=wecom-acct-ws-dm-hidaomax` 参数查看特定用户数据。

---

## 设计理念

借鉴 Claude Code 的核心设计模式，适配 OpenClaw 的插件架构：

| 维度 | Claude Code 原版 | 火一五·克劳德·龙虾增强插件适配 |
|------|-----------------|--------------|
| 记忆系统 | 6 层记忆 + Agent frontmatter | 5 类分类 + SQLite agent_id 隔离 |
| 权限安全 | 5 层权限模型 + 异步分类器 | 规则匹配 + block/log/allow + 审计日志 |
| 提示词工程 | Memoized sections + 优先级系统 | 可配置段落 + appendSystemContext 注入 |
| Agent 系统 | 3 种 Agent 类型 + frontmatter 配置 | 4 个增强技能 + OpenClaw skill 系统 |
| 工作流 | 17 个生命周期事件 | 触发词驱动 + before_prompt_build 注入 |

---

## 版本历史

见 [CHANGELOG.md](./CHANGELOG.md)。

## License

MIT

---

<div align="center">

**公司名称：** 青岛火一五信息科技有限公司

**联系邮箱：** postmaster@huo15.com | **QQ群：** 1093992108

---

**关注逸寻智库公众号，获取更多资讯**

<img src="https://tools.huo15.com/uploads/images/system/qrcode_yxzk.jpg" alt="逸寻智库公众号二维码" style="width: 200px; height: auto; margin: 10px 0;" />

</div>

---
