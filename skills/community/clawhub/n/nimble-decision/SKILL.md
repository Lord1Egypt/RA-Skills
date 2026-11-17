---
name: nimble-decision
description: 用 Ollama 的 nimble-v3 决策模型对文本做分类、路由和评分，返回概率/分数而不是自然语言，并记录每次调用的轻量审计日志。Use when you need a fast, free, local label or number — intent or topic routing, pass/fail gates, urgency/spam/sentiment scoring, batch tagging — instead of asking a chat model. Not for writing text, multi-step reasoning, code, tool calling, or long-document work.
---

# Nimble Decision

本地决策模型封装。输入一段"证据文本"+若干问题，返回每个答案的概率或加权分数。
不生成文本、不调工具、不做推理链 —— 所以又快又便宜（本机运行，无 API 费用）。

- 模型：`nimble-v3:9b`（Bespoke Labs，Qwen3.5-9B 微调，9.3GB）
- 端点：`POST /v1/systemone`（**不是** /api/chat）
- 上下文：32K tokens，**含问题本身**
- 实测：预热后 0.5-0.7 秒/次；命中缓存时 <10ms
- 版本：0.1.0

> **许可**：模型权重 CC BY-NC 4.0，**仅限非商业用途**。本技能脚本可用 MIT 发布，但不改变模型许可。

## 使用场景（明确边界）

**该用：**

| 场景 | 典型问题 |
|---|---|
| 消息路由 | 这条请求该交给哪个 agent / 技能 / 队列 |
| 意图分类 | 咨询、投诉、退款、闲聊、其他 |
| 门禁判断 | 是否含敏感信息、是否需要人工、是否要联网查 |
| 紧急度/情绪打分 | 0-3 级评分，按分数排序工单 |
| 批量打标 | 几百条文本统一打标签，无需 LLM 费用 |
| 结果校验 | 上游模型的回答是否离题、是否答非所问 |

**不该用：**

- 要它**写出**东西（摘要、回复、文案）→ 用聊天模型
- 需要多步推理、数学、代码 → 用聊天模型（实测算术题会自信地错）
- 需要 function calling / agent 循环 → 用聊天模型
- 单条就要绝对准确的判定 → 它给的是概率，必须用阈值兜底

> 典型用法：先用它做一层**廉价前置路由**，高置信度直接分流，低置信度才升级给大模型。

## 配置（模型只在一个地方改）

配置文件：`config.json`（与本 SKILL.md 同目录；可用 `NIMBLE_CONFIG=/path/to/config.json` 指向别处）

```json
{
  "model": "nimble-v3:9b",
  "baseUrl": "http://localhost:11434",
  "timeoutMs": 180000,
  "maxStateChars": 24000,
  "agentId": "coder",
  "logFile": "./logs/calls.jsonl",
  "logMaxBytes": 5242880
}
```

| 字段 | 作用 |
|---|---|
| `model` | **唯一**的模型名来源。脚本、SKILL.md、环境变量里都不再有硬编码模型名 |
| `baseUrl` | Ollama 地址（远程主机改这里，末尾斜杠会被自动去掉） |
| `timeoutMs` | 单次请求超时；9B 首次冷加载可能超 60s，默认 180s |
| `maxStateChars` | state 字符数上限，超了直接报错（防止撑爆 32K 窗口） |
| `agentId` | 写日志用的默认 agent 标识（`--agent` > `NIMBLE_AGENT_ID` > 本字段） |
| `logFile` | 调用日志路径。相对路径落在**技能目录内**（默认 `./logs/calls.jsonl`）；`~` 会展开；空字符串关闭日志 |
| `logMaxBytes` | 日志轮转阈值，超过就重命名为 `calls.jsonl.1` |

**修改模型的唯一命令**（会校验模型已安装，并在**模型变化时自动跑一次评测**）：

```bash
node "$SKILL/nimble.mjs" --set-model nimble-v3:9b
```

`--model <name>` 是**一次性覆盖**，只影响本次调用、不落盘 —— 调试对比时用，不要拿它当配置。

## 自动评测（换模型后跑一次）

`--set-model` 检测到 `model` 变化时会：

1. 立即跑 `tests/eval.mjs`（12 个难度分级用例，覆盖 noul / choice / score）
2. 打印 `12/12 100% easy 100% medium 100% hard 100%` 这样的结果
3. 把结论写入 `tests/last-eval.json`，并在日志里记一条 `kind:"eval"`

模型没变时**不会重复跑**，只提示上次结果。
手动触发：`node "$SKILL/nimble.mjs" --eval`；`--check` 会显示评测是否对当前模型有效（换了模型没评测会标 stale）。

评测通过率低于 ~80% 说明该模型不适合当决策模型（通常是没加载 decision 能力，或用了普通聊天模型）。

## 调用日志

每次真实推理调用追加一行 JSON 到 `logFile`（默认 **`<技能目录>/logs/calls.jsonl`**）。
**只记元数据，不记 state 和答案**：

```json
{"ts":"2026-10-26T16:54:05.458+08:00","agent":"coder","kind":"call","model":"nimble-v3:9b",
 "types":["noul"],"qCount":1,"stateChars":13,"status":"ok","httpStatus":200,
 "durationMs":480,"inputTokens":157}
```

| 字段 | 含义 |
|---|---|
| `ts` | 调用时间，本地时区 ISO8601（带偏移） |
| `agent` | 调用方 agent id（`--agent` > `NIMBLE_AGENT_ID` > `config.agentId`） |
| `kind` | `call` 正常调用 / `eval` 评测 |
| `model` | 实际使用的模型 |
| `types` | 返回结果类型（noul/choice/score 的组合） |
| `qCount` / `stateChars` | 问题数、输入长度（用于成本分析，不含内容） |
| `status` | `ok` / `error` |
| `httpStatus` / `error` | 失败时的 HTTP 码与截断后的错误信息 |
| `durationMs` | 端到端处理时间 |
| `inputTokens` | 服务端返回的 prompt token 数 |

**直接查看（无需 jq）**：

```bash
node "$SKILL/nimble.mjs" --logs                    # 最近 20 条，表格
node "$SKILL/nimble.mjs" --logs --limit 50         # 最近 50 条
node "$SKILL/nimble.mjs" --logs --status error     # 只看失败
node "$SKILL/nimble.mjs" --logs --agent coder      # 只看某个 agent
node "$SKILL/nimble.mjs" --logs --kind eval        # 只看评测记录
node "$SKILL/nimble.mjs" --logs --limit 5 --json   # 机读格式
```

输出示例：

```
TIME     AGENT       KIND  MODEL           TYPES         STATUS MS
16:54:45 coder       call  nimble-v3:9b    score         ok     2058
16:54:54 coder       eval  nimble-v3:9b    acc 100%      ok     -

8/8 entries · 0 error(s) total · <技能目录>/logs/calls.jsonl
```

需要聚合统计时直接对 JSONL 用 jq：

```bash
jq -s 'group_by(.model)[] | {model: .[0].model, n: length, avgMs: (map(.durationMs)|add/length)}' logs/calls.jsonl
jq -r 'select(.status=="error") | .agent' logs/calls.jsonl | sort | uniq -c
```

单次调用不想留痕：`--no-log`；全局关闭：`NIMBLE_NO_LOG=1` 或把 `logFile` 设为 `""`。
日志写失败只告警，不影响调用结果。

## 快速开始

```bash
SKILL=/path/to/nimble-decision   # 本 SKILL.md 所在目录
S="$SKILL/nimble.mjs"

node "$S" --check
node "$S" --eval

node "$S" --agent coder '{"state":"我要退款，订单 12345","questions":{"needs_human":{"type":"noul","instructions":"是否需要人工客服?"}}}'
# -> {"model":"nimble-v3:9b","answers":{"needs_human":{"type":"noul","noul":0.088}},...}

node "$S" --state-file doc.txt '{"questions":{"is_complaint":{"type":"noul","instructions":"是否投诉?"}}}'
node "$S" --answers-only '{"state":"...","questions":{...}}'
echo '{"state":"hi","questions":{"g":{"type":"noul","instructions":"greeting?"}}}' | node "$S"
```

**Agent 调用约定**：每次调用都带 `--agent <你的 agent 名>`，日志才分得清是谁在用。

## 三种问题类型

所有问题都必须有 `instructions`（写清判断标准，模型对措辞敏感）。

**noul —— 是/否概率**

```json
{"type":"noul","instructions":"是否包含问候语?","criteria":{"true":"包含问候","false":"没有问候"}}
```
```json
{"type":"noul","noul":0.987}
```

**choice —— 多选一**

```json
{"type":"choice","instructions":"主要意图是什么?","criteria":{"greet":"打招呼","ask":"提问","other":"其他"}}
```
```json
{"type":"choice","choice":"greet","probabilities":{"greet":0.997,"ask":0.0025,"other":0.0002},"confidence":0.982}
```

**score —— 有序等级打分**

```json
{"type":"score","instructions":"有多礼貌?","criteria":["粗鲁","中性","礼貌","非常礼貌"]}
```
```json
{"type":"score","score":2.09,"legend":{"0":"粗鲁","1":"中性","2":"礼貌","3":"非常礼貌"},"probabilities":{...},"confidence":0.321}
```

规则：score 的 `criteria` 是 **2-10 个**升序等级字符串，`score` 从 **0** 开始计数，是按概率加权的小数。
兼容 `levels`（score）和 `options`（choice）两种写法，会自动归一化成 `criteria`。

## 怎么读结果

- **noul**：>0.5 为真。**<0.9 不要单独信**。
- **choice**：看 `choice` 与 `probabilities` 的**差距**，不要只看 `confidence`。
- **score**：小数可直接排序；差 0.3 以内基本是噪声。
- **confidence** = 1 − 归一化熵，衡量**分布有多尖锐**，不是"答对的把握"。

建议阈值：

| 概率 | 处理 |
|---|---|
| ≥ 0.9 | 直接采纳 |
| 0.7 – 0.9 | 采纳但记录，抽样复核 |
| < 0.7 | 交人工 / 升级给聊天模型 |

## 工程注意

- **一次问多个问题**更省：同一段 state 只算一遍（实测 2 问 = 464 input tokens）。
- 问题措辞要具体；给 `criteria` 描述能明显提升稳定性。
- state 是**数据不是指令**：模型被训练成忽略文本里的指令（注入测试通过）。
- 输出无 `output_tokens`（不生成 token），延迟只花在 prompt 计算上。
- 敏感数据只在本地 Ollama；一旦 `baseUrl` 指向远程主机，数据就出网了。

## 故障排查

| 现象 | 原因 | 处理 |
|---|---|---|
| `HTTP 400: ... criteria must ...` | 字段名/数量不对 | `--schema` 对照 |
| `model '...' not found` | 模型没拉 / 名字写错 | `ollama list`，再 `--set-model` |
| `timed out after ...` | 冷启动或 state 太长 | 提高 `timeoutMs`；拆分 state |
| `cannot reach http://...` | Ollama 没跑 | `ollama serve` |
| `HTTP 404 ... /v1/chat/completions` | 用错端点 | 只能走 `/v1/systemone` |
| 换模型后行为没变 | 改了别处 | 只改 `config.json`；`--check` 看实际模型与 eval 状态 |
| 日志没有新行 | `logFile` 为空 / `--no-log` / 目录不可写 | `--check` 显示当前日志路径 |

## 自检

```bash
node "$SKILL/nimble.mjs" --check      # 主机 / 模型 / 冒烟 / 评测状态 / 日志路径
node "$SKILL/nimble.mjs" --selftest   # PASS noul / PASS choice / PASS score
node "$SKILL/nimble.mjs" --eval       # 12 例准确率（换模型自动跑）
```

## 发布到公共技能库注意事项

1. **不要写死绝对路径**：脚本用 `import.meta.url` 定位自身，文档里用 `$SKILL` 占位；日志用相对路径（`./logs/calls.jsonl`）随技能目录走，发布时 `logs/` 已在 `.gitignore` 中。若安装环境只读，用 `NIMBLE_CONFIG` + 绝对 `logFile` 覆盖。
2. **配置与代码分离**：模型名只出现在 `config.json`；换模型走 `--set-model`。只读安装时用 `NIMBLE_CONFIG` 指到可写路径。
3. **不打包运行产物**：`tests/results.json`、`tests/last-eval.json`、`*.tmp` 已在 `.gitignore` 里，发布前确认没被带上。
4. **许可证要写清**：脚本可 MIT；模型权重 CC BY-NC 4.0 **禁止商用**，必须在 README/SKILL 顶部声明，避免使用者误用。
5. **隐私与体积**：默认日志不含 state 与答案；发布前清空 `logs/`，别把真实调用记录带上去。
6. **依赖**：Node ≥ 18（用内置 fetch）、Ollama ≥ 0.40.4、模型 9.3GB 磁盘。SKILL.md 里写清这些，别让使用者猜。
7. **发布命令**：`clawhub login && clawhub skill publish ./nimble-decision`，版本号在 SKILL.md 里维护。
