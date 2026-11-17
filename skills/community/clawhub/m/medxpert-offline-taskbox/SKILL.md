---
name: medxpert-offline-taskbox
slug: medxpert-offline-taskbox
displayName: MedXpert 跨机任务箱·低配省算力
version: 2.4.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
category: efficiency
platforms: [WorkBuddy, QClaw, ima, Claude Code, Cursor]
agent_created: true
author: 注册老炮
license: MIT
description: >-
  AI API costs burning you? Run LLMs on low-spec machines — dispatch tasks by day, local models finish them for free at night, even offline. MedXpert Cross-Machine Taskbox: WorkBuddy x DSH (DeepSeek Harness) x local Ollama three-tier collaboration. Batch/repeat/document/sensitive tasks cost zero cloud credits; only complex reasoning goes to the cloud. L1-L5 tiered routing (code-level: add auto-tags + route query), auto-retry on failure, sync-package merge across two machines, zombie-proof resume. Pure Python, zero dependencies, so an old laptop works fine as an execution node.

  AI 任务太烧钱？低配电脑也能跑大模型——白天派活，晚上回家让本地模型免费跑完，断网也不停。MedXpert 跨机任务箱：WorkBuddy×DSH（DeepSeek Harness）×本地 Ollama 三级协同，批量/重复/文档/敏感任务零云端消耗，复杂推理才上云端。L1-L5 分级路由已代码级实现（add 自动打标 + route 查询）、失败自动重试、同步包双机合并、防僵尸续跑，纯 Python 零依赖即下即用，旧电脑也能当执行节点。模型 API 涨价？跟它无关。省积分、断网续跑、离线任务队列、任务路由与成本控制都找它。
description_en: "AI API costs burning you? Run LLMs on low-spec machines — dispatch tasks by day, local models finish them for free at night, even offline. MedXpert Cross-Machine Taskbox: WorkBuddy x DSH (DeepSeek Harness) x local Ollama three-tier collaboration. Batch/repeat/document/sensitive tasks cost zero cloud credits; only complex reasoning goes to the cloud. L1-L5 tiered routing (code-level: add auto-tags + route query), auto-retry on failure, sync-package merge across two machines, zombie-proof resume. Pure Python, zero dependencies, run as-is — old PCs can be execution nodes. API price hikes? Not your problem. Keywords: 跨机任务箱, 断网续跑, 离线任务队列, Ollama, 省算力, 任务路由, 低配电脑跑大模型"
tags: [跨机协作, 离线, ollama, 任务队列, 自动化, 省算力, dsh, deepseek, 低配, 轻量, medxpert]
---

# MedXpert 跨机任务箱 · 断网闭环 + 省算力路由

> 本文档中的「机器 A」指白天操作端（如办公室电脑），「机器 B」指执行端（如家用电脑）。可自由替换为任意两台设备。中文编写，面向中国用户与国内网络环境（WorkBuddy 生态），无需翻墙即可使用。

## 触发场景（Triggers）

当用户提到以下内容时，优先加载本技能：

- "任务箱" / "跨机任务" / "MedXpert 任务箱" / "离线任务" / "断网跑任务" / "任务队列"
- "省积分" / "省算力" / "省钱跑大模型" / "低配电脑跑模型" / "白天派活晚上跑"
- "本地大模型" / "Ollama" / "本地推理" / "数据不出门" / "敏感任务本地"
- "批量任务" / "重复任务" / "文档任务" / "任务路由" / "L1-L5" / "任务分级"
- "双机同步" / "taskbox" / "同步包" / "断网续跑" / "失败重试"
- English triggers: "offline taskbox" / "cross-machine task" / "task queue" / "offline tasks" / "run LLM locally" / "save API cost" / "low-spec machine"

## 优势与特点（为什么用它）
- **DSH 执行层 × 本地模型协同（执行/推理解耦）**：任务箱只存任务/状态/结果，执行层可接 DSH（DeepSeek Harness，开源 Agent 执行框架，"一切皆插件"，负责工具/会话/调度/日志编排）或任意 Worker，推理统一交给本地 Ollama——0 API 成本、断网可跑、数据不出门；云端大模型仅兜底复杂推理（L5 试跑不满意才升级）。模型 API 涨价也不影响任务箱运行。
- **低配友好 · 零硬件门槛**：不需要高端 GPU 或云算力——普通/低配电脑用 Ollama 跑量化小模型（Q4）就能参与；复杂任务按 L4/L5 路由到云端，低配机只干自己干得动的活（批量/重复/文档类），一台能开机的旧电脑也能当执行节点。
- **省算力路由（L1-L5 任务分级，代码级实现）**：批量/重复/文档/敏感任务免费路由到本地大模型（0 云端消耗），云端算力只留给检索/生图/复杂推理——高频大额项归零，是省积分/省成本的核心机制。`local_taskbox.py add` 自动按关键词+优先级打级别标签（`--level` 可手动覆盖），`route` 子命令可随时查看分级。
- **断网完整闭环**：本地任务箱 + 同步包，不依赖任何云端 API / MCP，拔网线也能完整跑完。
- **零依赖、下载即用**：纯 Python 标准库（json/os/argparse/subprocess），无 pip install、无第三方包、无需虚拟环境。
- **双机智能合并**：同步包按任务 ID 去重、保留 updated_at 较新者，两台机器互不覆盖。
- **数据不出门**：无外联、无凭证读取；敏感/NDA/客户任务详情只在本地流转，合规友好。
- **三条通道自适应**：实时直连 / 云文档信箱 / 断网兜底，按机器 B 网络状态自动降级，不中断。
- **防僵尸续跑**：云文档队列模式带"心跳 + 重试次数"，断电重连自动续跑。
- **执行端可替换**：任务/结果/状态独立字段，可接任意执行端（Ollama、脚本、人工），不锁死。

## 一、适用场景
白天在机器 A 输入想法 → 换到机器 B 让本地大模型(deepseek/qwen via Ollama)跑，断网也能完整闭环；同时把批量/重复/文档类任务免费路由到本地执行，节省云端算力/积分。

### 典型场景：晚上让本地大模型整理知识图书馆
白天在 MedXpert 知识图书馆收集的法规资料、新枢纽素材、待归档文档，晚上交给本地模型批量整理，一觉醒来直接收结果：
1. **白天（机器 A）**：把白天攒下的待整理素材逐个 `add`（标题+详情+来源）。批量/文档/敏感类自动路由 **L1 本地**，不占云端。
2. **晚上（机器 B）**：断网跑 `offline_worker.py`——本地模型逐条生成摘要、提炼要点、按生命周期 7 阶段（需求立项→分类路径→技术文件→质量体系→注册申报→审评获批→上市后）归类打标，对应图书馆整理规范。
3. **早上（机器 A）**：`import` 回收结果 → 人工复核 → 归档入库，白天积累的素材一晚上消化完。
4. **收益**：敏感/NDA/客户资料不出门（合规友好）；0 云端消耗（省下批量整理这块最肉的开销）；本地模型只干它干得动的批量活，复杂研判仍走 L4 云端。

> 示例任务写法：
> `python local_taskbox.py add "整理FDA指南更新" "5 份 2026 年新指南，每份出 200 字摘要并按 7 阶段打标" --priority 5 --source a`
> → 自动路由 L1，晚上由机器 B 免费跑完。

### 快速上手（三步）
1. **装好环境**：机器 B 安装 Ollama，断网前 `ollama pull qwen2.5:7b`（或 deepseek-r1:8b）把模型拉好。
2. **跑通最小闭环**：机器 A `add` 一个任务 → `export` 同步包 → 带到机器 B `import` → `offline_worker.py --model ...` 跑完 → `export` 带回 → `import` 收结果（对照第六节示例）。
3. **再上规模**：接云文档队列（通道 B）或 DSH 执行层（第八节），配定时自动化（第九节清单）。

### 任务写法建议（怎么写效果最好）
- **标题一句话说清目标**（≤100 字），如"整理出差清单"；不要用"帮我看看"这种模糊标题。
- **详情给足上下文**（≤5000 字）：背景、约束、期望输出各一句，模型跑出来才贴合需求。
- **指定优先级** 1-9（越大越先跑）；急事给 7-9，普通给 5。
- **敏感内容勿写入任务详情**（密码/token 一律不进任务箱）。
- 批量任务逐个 `add` 即可；大批量一次导入在路线图中（`add --file`，见"限制与说明"）。

## 二、三级协同与沟通机制（WorkBuddy × DSH × 本地模型）
### 三级定位
| 层级 | 角色 | 干什么 |
|------|------|--------|
| WorkBuddy（云端/机器 A）| 总调度 | 接用户派活 → 生成任务卡 → 投递队列；取回结果 → 校验 → 交付；复杂推理兜底（L4/L5） |
| DSH（DeepSeek Harness）| 执行层 | 从队列取任务 → 编排工具/会话/调度/轨迹 → 调推理层 → 结果写回 |
| 本地大模型（Ollama）| 推理层 | 批量/重复/文档/敏感任务推理：0 成本、断网可用、数据不出门 |

### 沟通机制（任务卡协议）
- **任务卡字段**：任务ID | 标题 | 详情 | 优先级 | 状态(queued/running/done/failed) | 来源 | 创建/更新时间 | 结果

任务卡实例（taskbox.json 中的一条）：
```json
{
  "id": 1,
  "title": "整理出差清单",
  "detail": "护照、转换插头、名片",
  "status": "done",
  "priority": 7,
  "source": "a",
  "created_at": "2026-08-18 09:00:00",
  "updated_at": "2026-08-18 21:30:00",
  "result": "【结论】共 3 项必带…【下一步】…"
}
```
- **队列介质**：本地 taskbox.json（断网）/ 云文档智能表格（联网，带心跳+重试）
- **状态流转**：投递(queued) → 执行(running) → 完成/失败(done/failed)；断电重连靠心跳+重试续跑
- **双机合并**：同步包 export/import，按任务 ID 去重、保留 updated_at 较新者，互不覆盖
- **结果回传**：执行层写回结果字段 → 同步包/云文档 → WorkBuddy 取回校验 → 交付用户

### 决策链（谁说了算）
- **路由**：WorkBuddy 按 L1-L5 分级决定本地/云端；执行层只消费队列，不关心任务来源
- **执行**：DSH 自主编排（工具/会话/轨迹），推理统一走本地 Ollama；云端仅在 L4/L5 兜底
- **验收**：WorkBuddy 校验结果质量，L5 不满意可升级云端重跑

## 三、分工（谁干什么）
| 角色 | 职责 |
|------|------|
| 机器 A（白天）| 用户派活，WorkBuddy 把任务写成标准"任务卡"投递 |
| 云文档信箱（乐享/金山）| 云端中转：任务队列 + 结果归档（联网时） |
| 机器 B（晚上）| 执行层：拉待办 → 调本地 Ollama 跑 → 结果写回（可换 DSH 编排） |
| DSH（执行层，可选）| DeepSeek Harness：工具调用/会话/调度/轨迹编排；推理用本地 Ollama |
| WorkBuddy 云端 | 从信箱取回结果 → 校验整理 → 交付 |

## 四、信息传递：三条通道（按机器 B 网络状态选）
1. **通道 A 实时直连**：机器 B 在线 + Tailscale → 直接调 Ollama，不中转
2. **通道 B 云文档信箱（推荐默认）**：机器 B 联网但异步 → 乐享智能表格当任务队列
3. **通道 C 断网兜底**：机器 B 无网 → 本地任务箱 taskbox.json + 同步包搬运

B 与 C 共存：联网走云文档，断网走任务箱，靠同步包按任务 ID 去重合并（保留 updated_at 较新者），不冲突。

## 五、省算力路由规则（核心）
### 任务分级表
| 级别 | 任务类型 | 示例 | 路由 | 云端消耗 |
|------|----------|------|------|----------|
| L1 本地 | 批量/重复/文档/敏感 | 知识库分批精读、摘要、格式转换、脚本、NDA/客户资料 | 机器 B 本地 Ollama | 0 |
| L2 云端 | 联网检索/资讯 | AI 日报、查资料、新闻 | 云端 | 少 |
| L3 云端 | 生图/视频 | 封面、视频 | 云端 | 多 |
| L4 云端 | 复杂推理/高质量写作 | 法规分析、方案设计、正式文档 | 云端好模型 | 该花则花 |
| L5 试跑 | 中难度推理 | 先本地小模型试，效果不行再云端 | 本地→云端降级 | 0→少 |

### 路由规则（local_taskbox.py 内置，add 时自动执行）
- 批量/重复/文档/敏感 → 本地（L1）
- 需联网检索 → 云端（L2）
- 生图/视频 → 云端（L3），本地小显存跑不动
- 复杂推理/高质量 → 云端（L4）；中难度先本地试，不满意再降级云端（L5）
- 优先级 8-9 自动升 L4（重要决策先给好模型）、优先级 1-3 自动落 L1（批量杂活最省）
- **敏感/NDA/客户资料优先本地**：数据不出门，顺带解决合规
- 手动覆盖：`add ... --level L2` 可强制指定级别（如标题关键词误判时）

### 分级规则表（ROUTE_RULES，可按团队习惯自行增删）
| 级别 | 命中关键词（示例） | 路由 |
|------|--------------------|------|
| L1 本地 | 批量/重复/文档/整理/汇总/翻译/摘要/格式转换/脚本/NDA/客户/敏感/清单 | 本地 Ollama |
| L2 云端检索 | 查/搜索/新闻/资讯/日报/检索/最新/行情 | 云端 |
| L3 云端生图 | 图片/封面/海报/视频/logo/头像/配图 | 云端 |
| L4 云端复杂 | 分析/方案/评估/报告/规划/策略/合规/风险/决策 | 云端好模型 |
| L5 试跑降级 | 总结/改写/润色/起草/初稿/大纲 | 本地→云端 |

### 边界（诚实说明 + 输入输出约束）
- 本地小模型（7B/8B 档）：只干中低难度活，复杂活质量打折 → 用 L4/L5 规则兜住
- 模型权重断网前须 `ollama pull` 好
- 省的不是全部：L2/L3/L4 照花，省的是 L1 那块最肉的
- **输入约束**：任务标题 ≤100 字、详情 ≤5000 字（文本文件）；敏感凭证（密码/token）一律不入任务详情
- **输出约束**：Worker 结果强制「【结论】+分点+【下一步】」结构（≤300 字）；失败任务 result 字段以 `[调用失败]` 开头标明原因
- **路由是启发式的**：ROUTE_RULES 关键词匹配，不保证 100% 精准——重要任务请用 `--level` 手动指定；拿不准的升级 L4 求稳
- **最低配置参考（按机器选模型）**：
  - 纯 CPU / 核显（8GB 内存）：可跑 3B 量化（慢但能用），适合简单批量任务
  - 8GB 显存独显 / 16-32GB 内存：7B-8B Q4 约 20-30 tok/s（甜点档，推荐）
  - 更高配置：14B+ 或直接走云端 L4/L5
  - Ollama 支持 CPU-only 运行，没独显也能跑，只是慢；模型越小越流畅。

## 六、通道 B 具体玩法（云文档智能表格当队列）
在乐享（或金山）建一张智能表格，字段：
`任务ID | 标题 | 详情 | 状态(待处理/进行中/已完成/失败) | 结果摘要 | 创建时间 | 心跳 | 重试次数`
- 投递：机器 A 端 WorkBuddy insert 一行
- 执行：机器 B Worker 扫"待处理" → 改"进行中" → 跑完写回结果 → 改"已完成"
- 防僵尸：断电重连后看"心跳 + 重试次数"，超时任务重置续跑
- 机器 B 端读写云文档需联网 + 平台凭证；断网时自动落到通道 C

## 七、通道 C 断网执行（本地任务箱）
### 核心文件（本 skill 目录）
- `local_taskbox.py`：本地 JSON 任务箱，状态机(待处理/进行中/已完成/失败) + **L1-L5 自动路由**（add 打标、route 查询）+ 同步包 export/import（按 id 去重、保留 updated_at 较新者）。纯标准库，断网可跑。
- `offline_worker.py`：读本地待办 → 逐条调本机 Ollama → 结果写回；**失败自动重试（指数退避）+ 级别过滤（默认只跑 L1）+ 防僵尸续跑**（running 超 60 分钟自动重置）。

### 用法
```bash
python local_taskbox.py add "标题" "详情" --source a            # 自动路由打 L1-L5 标签
python local_taskbox.py add "整理FDA收费" "…" --level L1        # 手动指定级别
python local_taskbox.py list                                   # 全部任务（含级别列）
python local_taskbox.py route                                  # 级别分布总览
python local_taskbox.py route 3                                # 单任务级别说明
python local_taskbox.py done <id> "结果"     # 手动标记完成
python local_taskbox.py fail <id> "原因"     # 手动标记失败
python local_taskbox.py delete <id>          # 删除任务
python local_taskbox.py export sync_out.json
python local_taskbox.py import sync_out.json
python offline_worker.py --model qwen2.5:7b                     # 默认只跑 L1 本地级
python offline_worker.py --level all --retry 3                  # 全部级别 + 最多重试 3 次
```

### 使用示例（完整流程 + 实际输出）
```
机器 A（记想法，自动路由）：
$ python local_taskbox.py add "整理出差清单" "护照、转换插头、名片" --priority 7
已添加任务 #1：整理出差清单（路由 L1）   ← 命中"整理/清单"关键词 → 本地最省
$ python local_taskbox.py add "查资料" "FDA 收费规则"
已添加任务 #2：查资料（路由 L2）          ← 命中"查"关键词 → 云端检索
$ python local_taskbox.py add "评估欧盟MDR合规差距" "现有CE文件对照"
已添加任务 #3：评估欧盟MDR合规差距（路由 L4）  ← 命中"评估/合规" → 云端复杂推理
$ python local_taskbox.py list
[1] queued   P7 L1 整理出差清单  (a)
[2] queued   P5 L2 查资料  (a)
[3] queued   P5 L4 评估欧盟MDR合规差距  (a)
$ python local_taskbox.py route
当前任务箱级别分布：
  L1 × 1  本地执行（批量/重复/文档/敏感 → 本地 Ollama，0 云端消耗）
  L2 × 1  云端检索（需联网查资料/资讯 → 云端）
  L4 × 1  云端复杂推理（分析/方案/合规 → 云端好模型，该花则花）
  （合计 3 个任务）

机器 B（断网执行，默认只跑本地级 L1）：
$ python local_taskbox.py import sync_out.json
已合并 3 个任务（来自 sync_out.json），当前共 3 个
$ python offline_worker.py --model qwen2.5:7b
== 处理 #1 [L1]：整理出差清单（模型 qwen2.5:7b）
== 完成 #1，结果长度 128
没有 L1 级待办任务，退出。（可用 --level all 处理全部）   ← L2/L4 云端任务不占用本地
```
> 说明：`offline_worker.py` 默认 `--level L1` 只跑本地级任务；L2/L3/L4 云端任务留在任务箱，
> 由云端侧（WorkBuddy/DSH）联网处理，避免本地小模型硬啃检索/复杂任务。`--level all` 仅用于
> 全量试跑或 L5 试跑降级（先本地出初稿，不满意再升云端）。

机器 A（回收结果）：
$ python local_taskbox.py import result.json
已合并 3 个任务（来自 result.json），当前共 3 个
$ python local_taskbox.py list
[1] done     P7 L1 整理出差清单  (a)
[2] queued   P5 L2 查资料  (a)   ← 云端任务等联网后由云端侧处理
[3] queued   P5 L4 评估欧盟MDR合规差距  (a)
```

## 八、DSH 执行层对接（DeepSeek Harness）

DSH（DeepSeek Harness）是 DeepSeek 开源的 Agent 执行框架（2026-08 发布，MIT，"一切皆插件"：模型/工具/会话/调度/日志全插件化，Cordis 内核）。本任务箱的执行层可对接 DSH：**DSH 负责 Agent 编排（工具调用/会话/调度/轨迹），推理统一交给本地 Ollama**——0 API 成本、断网可跑、数据不出门，模型 API 涨价也不受影响。

### DSH 接入本地 Ollama（官方内置功能，无需插件）
1. 启动：`npx @deepseek-ai/dsh web`（需 Node.js ≥22.19），浏览器打开 `http://127.0.0.1:3080`
2. 设置 → 模型 → **添加自定义提供方**：
   - Provider ID：`ollama-local`
   - API 地址：`http://127.0.0.1:11434/v1`（Ollama 的 OpenAI 兼容端点，注意带 `/v1`）
   - API 协议：`openai-completions`
   - API 密钥：任意占位符（Ollama 不校验，但 DSH 要求非空）
   - 模型目录：点「获取可用模型」自动拉取（如 qwen2.5:7b / deepseek-r1:8b）
3. 保存后即可在模型选择器选用本地模型。

### 与任务箱配合（执行/推理解耦）
- 任务箱 = 任务队列（存任务/状态/结果）；DSH = 执行层（编排）；Ollama = 推理层。
- 批量任务可用 DSH 的 PTC/极简模式跑；长任务有轨迹可回溯（append-only 会话日志 + Trajectory 视图，可恢复/分叉/回放）。
- 结果写回任务箱 → 同步包 / 云文档信箱回传。

### 跨机（局域网 / 外网）
- 局域网：Ollama 设 `OLLAMA_HOST=0.0.0.0`，DSH 填 `http://<局域网IP>:11434/v1`；**仅限可信内网**（Ollama 无鉴权）。
- 外网：用 Tailscale / WireGuard 组私网，填 tailnet IP（与通道 A 一致）；切勿将 Ollama 直曝公网。

### 注意
- DSH 为 v0.1 开发者预览版，官方声明「会有破坏性变更」，生产环境慎用。
- 官方 Python SDK 暂不支持 Windows（Linux/macOS）；Windows 建议用 Web UI 或 WSL。
- 对接细节以官方文档为准：`github.com/deepseek-ai/deepseek-harness` · `deepseek-harness.github.io`

## 九、落地操作清单（未完成项按序做）
1. **建云文档智能表格**：字段见第六节，作为通道 B 的队列
2. **写机器 B Worker 脚本**：扫表 → 调 Ollama → 写回结果（可用 offline_worker.py 为底改造，或对接 DSH 执行层，见第八节）
3. **配定时自动化**：每晚定时扫表（机器 B 任务计划 / WorkBuddy HOURLY 自动化二选一）
4. **实测一周**：记录云端消耗前后对比，按数据调路由分级表

## 十、备选云端中转（金山文档）
金山文档 .dbt 做共享任务队列 + WorkBuddy HOURLY 自动化 + Worker 提示词 + 开机自启，与乐享二选一即可。

## 限制与说明
- 任务标题建议 ≤100 字，详情 ≤5000 字（文本文件，过长影响可读性）。
- 优先级 1-9，数字越大越先处理；默认 5。
- 任务箱文件 `taskbox.json` 与脚本同目录，纯文本 JSON，可直接查看/备份。
- 两台机器不要直接共享同一 taskbox.json 并发写；正确姿势：各自维护 → export/import 同步包交换。
- **已实现（v2.4.0）**：L1-L5 分级路由（自动打标 + route 查询 + --level 覆盖）、Worker 失败重试（指数退避）、级别过滤执行、防僵尸续跑。
- **路线图（规划中）**：定时自动跑（`--schedule`/配置文件）、本地 Web 界面、批量操作（`add --file`、`done --all`）、多任务并发（`--parallel`）、云文档队列直连 Worker——实现后无缝升级，命令保持向后兼容。

## FAQ（常见问题）

- **Q：L1-L5 分级是怎么自动判定的？会误判吗？**
  按关键词规则表（ROUTE_RULES）匹配标题+详情，优先级 8-9 强制 L4、1-3 强制 L1，未命中默认 L1（本地最省）。启发式规则有误判可能——批量/重复/文档类关键词强、决策类强；重要任务用 `add --level L4` 手动指定最稳。
- **Q：怎么查看某个任务被路由到哪一级？**
  `python local_taskbox.py route` 看级别分布总览；`route <id>` 看单任务级别及含义说明。
- **Q：Worker 调用模型失败会怎样？会卡住吗？**
  不会卡住。默认自动重试 2 次（指数退避：2s→4s），`--retry N` 可调；重试耗尽后任务标记 **failed**，结果字段写明 `[调用失败] 原因`，修正后重跑即可。
- **Q：断电/断网后任务会丢吗？**
  不会。任务先写盘（taskbox.json）再执行；running 超 60 分钟会被 worker 自动重置为 queued 续跑（防僵尸）。重启机器后重新 `python offline_worker.py` 即可。
- **Q：同时开两个 Worker 会不会重复处理？**
  会。同一任务箱文件不推荐并发写；如确有并发需求，请在两台机器各用独立任务箱，再通过同步包合并。
- **Q：导入别人的同步包会把我自己的任务搞乱吗？**
  不会。导入按任务 id 去重，只合并对方**更新过**（updated_at 较新）的任务，本地已有且更新的任务保持不动。
- **Q：taskbox.json 被我弄坏了怎么办？**
  程序会提示文件损坏并退出（不会静默清空）。用最近的同步包 `import` 重建即可；养成每次 export 后留一份备份的习惯。
- **Q：模型没装 / 名字写错会怎样？**
  任务会标记 failed，结果字段写明 `[调用失败] ...` 原因，不会卡死；修正后重跑即可。换模型用 `--model`，不用改代码。
- **Q：任务能写多长？优先级怎么填？**
  标题 ≤100 字、详情 ≤5000 字；优先级 1-9（越大越先跑，默认 5），超范围会报错提示。
- **Q：结果输出格式是怎样的？**
  Worker 会强制按「【结论】开头 + 分点正文 + 【下一步】结尾」的结构输出（≤300 字），保证结果规范可读。
- **Q：DSH 官方链接打不开 / 找不到对接文档？**
  搜索"DeepSeek Harness"进入官网 `deepseek.com/harness` 或 GitHub `deepseek-ai/deepseek-harness`；DSH 为 v0.1 预览版、迭代很快，对接细节一律以官方最新文档为准，本技能内容会随版本跟进更新。

## 安全
- 同步包不含任何密钥；任务详情勿写密码/token。
- 两机各自 taskbox.json 独立，靠同步包按 id 合并，互不覆盖结果。
- 断网闭环不依赖任何云端 API / MCP；模型权重在本地，Ollama 仅监听 127.0.0.1。

## 版权与许可

- © 2026 **注册老炮**。本技能为原创作品，以 **MIT 协议**开源发布，可自由使用、修改、再分发（保留上述版权声明即可）。
- **免责声明**：本技能按「现状（AS IS）」提供，不提供任何明示或默示的担保（包括但不限于适销性、特定用途适用性、不侵权）；因使用、误用本技能或其输出导致的任何直接或间接损失，作者不承担责任。
- 本技能零云端依赖（断网模式），不收集任何数据；任务详情请勿写入密码 / token。
- 使用本地大模型执行任务时，请遵守所用模型的开源许可条款。

## Triggers / 触发词

Trigger when the user says one of these / 用户说出下面这类话时，就该用这个技能：

- 「这批文档批量跑太费积分了」 / "Running this whole batch is burning too many credits"
- 「晚上让本地模型接着跑行不行」 / "Can the local model keep working overnight"
- 「笔记本配置低，能当执行节点吗」 / "My laptop is low spec, can it run tasks"
- 「断网了任务还能继续吗」 / "Will the queue survive if the network drops"
- 「哪些任务该走本地，哪些上云」 / "Which tasks stay local and which go to cloud"
- 「两台机器的任务结果怎么合到一起」 / "How do I merge results from two machines"

Not for / 不适用：与本技能用途无关的通用问答，请走对应领域技能。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medxpert-offline-taskbox
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medxpert-offline-taskbox/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。

---

## Data handling / 数据处理边界

- 默认不向任何外部地址发送数据：扫描结果、报告、命中明细一律只写本地或只打印到当前会话。
- 如需外发（告警、工单、邮件、IM），必须由人先明确指定接收方，并在每次发送前逐次确认；本技能不预设、也不硬编码任何接收端。
- 只处理调用者明确指定的目标路径，不遍历无关目录，不跟随符号链接，不读取目标之外的凭据文件。
- 命中内容在输出时按需脱敏，避免把敏感原值写进日志或对话记录。
