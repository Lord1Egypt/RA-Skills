---
name: openviking-memory-triage
description: "Triage OpenViking memory pipeline failures (empty memory, no extraction, recall misses): write a probe to expose the quota layer, check server-side events, then diagnose across network, auth, quota, threshold, and extraction layers."
---

# OpenViking 记忆管线分诊（记忆空白 / 没抽取 / 召回想不起来）

用于：主人说「openviking 是不是没正常运行」「控制台记忆库是空的、没有今天的记忆」「怎么想不起之前的事」；或要确认长期记忆管线（capture → 抽取 → recall）端到端是否健康。
产出：**五层分诊结论**（网络 / 鉴权 / 配额 / 阈值 / 抽取）+ 服务端落盘证据 + 出路。
（装/配插件 → 随包技能 `install-openviking-memory`；本机配置体检 → `openclaw-config-audit`；模型 provider 不可用 → `openclaw-model-health-triage`。）

## 前置事实（实测，勿重踩）

- **`memory_recall` 返回空 ≠ 管线健康**：配额耗尽与「本来就没记忆」现象**完全相同**（都回 `count:0`、不报错）——只读 recall 判不出配额层，必须用**写路径**探针。
- ⚠️ **`openviking status --json` 的 `health.ok:true` 是假绿灯**：它的 health 只验 key 探针（`keyProbe.detail` 报「API key has full user context」照样成立），**不验真实读写**。实测同一时刻它报 `health.ok:true` + `compatibility:compatible` + `slotActive:true`，而每轮 `afterTurn` 写入与 `auto-recall` 检索**全部 403**。⇒ **判活只认实弹探针 + 当轮日志，不认 status 的 health 字段**；用 status 汇报「一切正常」就是把加载成功当成了在干活。
- **每轮的真实成败在网关日志里，且比 outbox 更早更全**：`openclaw logs --limit 300` 取回后**在调用方做正则筛选**（`journalctl … | grep … | tail` 这类多级管道常被审批绑定层拒，单条命令 + 调用方筛选更稳）。三条指纹：`openviking: afterTurn failed: OpenViking request failed: HTTP <code>` = **写路径**每轮失败；`openviking: auto-recall context search failed: AllCredentialsFailedError` = **读路径**每轮失败；`[context-engine] durable turn advancement remains queued: …` = 失败条目已堆进 outbox 等重试。日志按时间正序覆盖当前时段 ⇒ 一次 `limit 300` 就能判「**现在**还坏不坏」，不必去翻 sqlite outbox 的历史快照。
- **`memory_store` 是唯一能暴露配额层的探针**：它走 `commit(wait=true)`，真正触发服务端抽取。回 `429 / AccountQuotaExceeded`（文案含 `It will reset at <日期>`）= **月配额耗尽**，与 commit 阈值无关。
- **成功判据看服务端落盘，不看工具返回值**：`ov_list viking://user/default/memories/events/<YYYY>/<MM>/<DD>/` 有没有当天文件（配额恢复后实测数秒内出现）。
- **URI 三坑**：`<uid>` 实测是 `default`——用登录名（`viking://user/<登录名>/…`）回 `PERMISSION_DENIED`；`viking://user/memories` 里 `memories` 是保留名，回 `INVALID_URI`；`viking://user` 根只有一个 `default` 条目。
- **`memory_store` 超 exec 预算 ⇒ 返回值必丢，且这不代表失败**：服务端抽取常 >10s，exec 回 `status:"waiting"` 后会话被丢、**返回值永久丢失**。⇒ 调用后**不要**等返回值，**更不要**盲目重试（会重复写入）；直接 `ov_list` 查落盘。（长命令的 exec 会话闲置被静默回收 → `multi-dimension-audit` 前置事实。）
- **capture 与抽取是两段，别混**：会话消息每轮都被追加（`sessions/` 一直在长），但**只有跨过 `commitTokenThresholdRatio`（默认 0.5 × 上下文）或走 `/compact` / `memory_store` 才触发抽取**。⇒ `sessions/` 有新目录**不代表**记忆在生成。
- **分类目录是预创建的空容器**：`memories/{cases,entities,events,experiences,preferences,skills,tools,trajectories}` 恒存在、`size=0`、abstract「not ready」——**是骨架不是证据**；判断有无记忆要看里面的文件（尤其 `events/<日期>/`）。
- ⚠️ **outbox 里的 `last_error` / `attempt_count` 是历史快照，绝不能当现状**：表 `context_engine_turn_outbox`（`agents/<id>/agent/openclaw-agent.sqlite`，只读打开）列 `(advancement_key, engine_id, owner_plugin_id, session_id, payload_json, attempt_count, last_attempt_at, last_error, created_at)`。实测一笔 `last_error` 写着「实例已欠费关停」而 `last_attempt_at` 是 **16 天前**，据此判「已停服、建议关插件」是**错的**——实弹 `ov_search` 当场返回 10 条结果，服务健康。**定「死没死」只认实弹探针**（`ov_search` / `ov_list` / `memory_recall` 任一成功即活）；查 outbox 只能回答「历史上失败过什么」。反向同理：**探针失败也不能单次定论**——同一工具间隔分钟级**连探两次**仍同错（如 `ProductUnordered`）才定「当前真故障」（实测欠费定案即用此法）；单次失败先查自身调用方式（参数名、参数类型）再归因服务。
- **积压与「恢复后不重试」是两回事**：实测 667 行 / 103 MB（payload 均值 110 KB、最大 1.6 MB），其中 **654 行 `attempt_count = 0`——一次都没重试过**，只有 13 行进过重试（最高 87 次）。远端恢复后队列**不会自动排空**，新条目仍在持续入队。⇒ 看到堆积先分清：还在报错 = 查五层；`attempt_count=0` 堆积 = 历史死信，等它自愈没指望，需手工清（且清完**文件不会变小**，只是释放空闲页供复用，见 `openclaw-config-audit/references/会话库膨胀分诊.md` §A 判据 4）。
- **「记忆系统正常吗」要测两层独立故障面**：内置检索（`memory_search`，本地索引）与 OpenViking 管线（`ov_*`，远端）互不代表对方——本机曾出现一层健康、另一层分别故障的双向组合。实弹探测：远端用 `ov_search` 任意词，本地用 `memory_search` 任意词。
- **`memory_search` 返回 `disabled:true, error:"index sources changed"` = 索引源失配静默暂停**（gateway 重启 + 大量文件变更后出现），不是没记忆：跑 `openclaw memory status --index --agent main` 触发重建（实测 339 文件/4166 chunks），回读 `Dirty: no` + `Embeddings: ready` 后**再实弹搜一次**验证恢复。重建是大事务，库 WAL 会临时涨到几十 MB，autocheckpoint 自会回落，不要手动 checkpoint（判据见 `openclaw-gateway-performance-triage/references/网关日志信号.md` slow SQLite 行）。
- **不要在 shell 里读密钥做探针**：把 `apiKey` 读出来拼进 `curl` 会被审批层拦（`risk=high`，属凭证探测），且主人已配置 MCP 工具时那是更差的取证方式——`ov_search` 本身就完成了探活且不碰密钥。

## 步骤

1. **结构门（廉价、必要不充分）**
   查 `plugins.slots.contextEngine` 是否为 `openviking`、`plugins.entries.openviking.config` 是否有 `baseUrl`。不在 ⇒ 管线未接管，走配置修复（`openclaw-config-audit`），本流程止。
   完成判据：能说出「插件在该槽位且有 baseUrl」，或明确排除结构问题——**结构正常 ≠ 管线健康**，必须继续。
   ⚠️ 主人说「是不是欠费/挂了」时，**先跑一次实弹探针**（`ov_search` 任意词）再谈结论；不要先查 outbox 的 `last_error` 就下判断。
2. **写探针定性**
   调 `memory_store`（短文本，如一条连通性测试），**不等返回值**。
   完成判据：已发起写入（后续一律以服务端落盘取证，不依赖返回值）。
3. **落盘取证 + 五层归因**
   查 `ov_list viking://user/default/memories/events/<YYYY>/<MM>/<DD>/`，并看 `memories/` 各分类目录 `modTime`；对照下表落到**唯一一层**。

   | 层 | 判据 | 出路 |
   |---|---|---|
   | 网络 | `ov_list` 超时 / 连接失败 | 查网络与 `baseUrl` |
   | 鉴权-凭据 | `401`（key 被吊销/轮换/从未生效；`/health` 通而 API 拒） | 重签 `apiKey`（SecretRef 坑见 `openclaw-config-audit`）；升级客户端不改变结论，见 `openclaw-extension-update` 的「升级后错误一字不变即坐实 key 失效」 |
   | 鉴权-授权 | `403` 或 `AllCredentialsFailedError`（key 被**接受**、该操作被拒） | 查 key 的 scope / 套餐 / 端点是否放行这条读写路径——授权面问题，与 key 有没有效是两回事，别并进 401 一起「重签了事」 |
   | **配额** | `429 AccountQuotaExceeded` + `reset` 日期 | 等重置 / 让主人升级套餐 |
   | 阈值 | 落盘在、今天无新文件，且未跨阈值 | 正常；要立刻抽就 `/compact` |
   | 抽取 | store 未报错但 `events/<当天>/` 始终无文件 | 服务端 pipeline（VLM/embedding）问题 → 交 OpenViking 管理员 |

   完成判据：结论附证据（错误码 / 目录与 modTime），不把「配额耗尽」误报成「插件坏了」。
4. **交付 + 记账**
   回报「哪层坏了 / 证据 / 出路」；结论与实测更正写当日 `memory/YYYY-MM-DD.md`。
   完成判据：主人拿到可复核结论与下一步。

## 边界

- 只做**分诊**：不改 `commitTokenThresholdRatio`（调低更烧配额，**配额刚恢复尤其别动**）、不代主人升级套餐、不改插件代码。
- 服务端抽取 pipeline（VLM/embedding）不在本机范围 ⇒ 如实说明交管理员，不为「全绿」硬凑。
- 写长期记忆时，**「当前状态」类事实取自当日日志末尾或 `memory/projects.md`**，不取日志开头——日志按时间正序追加，开头＝当天最早状态，取开头会把过期快照写成长期记忆。
