---
name: kb-keyword-graph
description: >-
  第二大脑（2brain）知识库的「关键词图谱」能力 Skill。当用户想了解某个 2brain
  知识库「有什么 / 讲什么 / 知识结构 / 主题分布 / 重点 / 资料之间的关系」，
  或明确提到关键词图谱 / 知识图谱 / 词云 / topic distribution / keyword graph /
  knowledge structure 时触发，拉取该库的三层关键词树并按四类任务解读：
  ① 知识结构（structure）② 关键词图谱（graph，渐进环形交互图）③ 主题分布
  （topics）④ 解释资料关系（relate，两个关键词在树中的层级关系）。即使用户没说
  「图谱」二字（如只问"这个库里都有什么/主要讲哪些方面"）也覆盖。注意：本 Skill
  的「知识库」特指 2brain 平台上的库（按名称或 base_id 定位），不路由到飞书
  Wiki / 云文档；不做入库、问答（chat）、建库等写操作。
user-invocable: true
license: MIT
metadata:
  requires:
    bins: ["python3"]
  env:
    - TWOBRAIN_GRAPH_KEY
    - TWOBRAIN_BASE_ID
    - TWOBRAIN_API_BASE
---

# 2Brain 关键词图谱

把第二大脑的「关键词图谱」能力封装为一个可稳定重复触发的只读工作流。
所有任务共享一份从 `keyword_api` 拉来的**三层关键词树**（keywords_tree），
四个子命令只是对同一份数据做不同解读。引擎：`scripts/kw_graph.py`（python3 标准库，无第三方依赖）。

## 首次使用（安装即用）

```bash
# 方式一：私有配置文件（推荐，token 不进环境/不落产物）
mkdir -p ~/.config/2brain-keyword-map
cat > ~/.config/2brain-keyword-map/config.json <<'JSON'
{ "token": "2B-你的图谱APIKey", "base_id": 700 }
JSON
chmod 700 ~/.config/2brain-keyword-map && chmod 600 ~/.config/2brain-keyword-map/config.json

# 方式二：环境变量（临时/CI）
export TWOBRAIN_GRAPH_KEY="2B-..."      # 2brain 平台「关键词图谱」API Key（Bearer）
export TWOBRAIN_BASE_ID=700             # 目标库的整数 base_id（可被 --base-id 覆盖）
# 课程环境需指到 test：export TWOBRAIN_API_BASE="https://test.2brain.ai/api"

# 自检
python3 scripts/kw_graph.py fetch --base-id 700
```

图谱 API Key 在 2brain 平台生成，与上传/问答 Key 不同。宿主机需能访问 `TWOBRAIN_API_BASE`（默认 `https://test.2brain.ai/api`）。

## 隐私与数据流（只读 · 不采集个人数据 · 无自主行为）

这是一个**只读**的知识库解读 skill，能力和数据流很窄，清单如下：

**① 能力**：只需 `python3`（标准库，无第三方依赖）。读写范围仅限缓存目录
`~/.local/state/2brain-keyword-map/`（存拉到的关键词树）；skill 目录本身只读。
**不跑 shell、不注册 cron、不做任何自主/定时行为**——每次都是你请求时才执行一次。

**② 发往外部的数据（极少）**：只向固定的 2brain 端点
`<TWOBRAIN_API_BASE>/kbase/keywords/keyword_api` 发送**一个整数 base_id**，
收回该库的关键词树。**不发送任何个人数据、文档内容、简历、对话**——base_id 只是库编号。
除这一个 2brain 端点外，不连任何第三方（无爬虫、无外部 LLM）。

**③ 凭证纪律**：图谱 API Key 只从**你自己配置的位置**读取——环境变量
`TWOBRAIN_GRAPH_KEY` 或私有文件 `~/.config/2brain-keyword-map/config.json`（建议 0600）。
**不读取 skill 目录之外的宿主凭证**（不碰 OpenClaw auth store）。Key 只作
`Authorization: Bearer` 头发给固定端点，**绝不**写进 HTML/JSON 产物、日志、URL 或对话
（引擎已保证产物零 token，可 grep 验证）。

**④ 边界**：不入库、不建库、不删改、不问答；不代替你操作；输出的关键词/计数/百分比
**只来自 API 真实返回**，为空就如实报"资料不足"，不编造。

## 任务路由（先判断意图，再读对应执行文档，再跑对应子命令）

| 用户意图信号 | 任务 | 子命令 | 执行文档 |
|---|---|---|---|
| 「这个库里有什么 / 知识结构 / 有哪些方面 / 结构是怎样的」 | 知识结构 | `structure` | [references/workflows.md](references/workflows.md#structure) |
| 「关键词图谱 / 知识图谱 / 词云 / 画个图看看」 | 关键词图谱 | `graph --html <路径>` | [references/workflows.md](references/workflows.md#graph) |
| 「主要讲哪些主题 / 主题分布 / 哪块内容最多 / 重点是什么」 | 主题分布 | `topics` | [references/workflows.md](references/workflows.md#topics) |
| 「X 和 Y 有什么关系 / 这两块内容怎么联系的」 | 解释关系 | `relate --a X --b Y` | [references/workflows.md](references/workflows.md#relate) |
| 登录/401/连接失败/图谱为空 | 排错 | — | [references/workflows.md](references/workflows.md#troubleshooting) |

意图模糊时（如只说"看看这个库"）：默认先做 `structure`，把一级主题摆出来，再问用户想深入哪一类。**先向用户复述你判断的任务和目标库，再执行。**

## 公共约束（四类任务都必须遵守）

**知识库定位——永远不硬编码 base_id**：
1. 用户给了整数 base_id → 直接用（`--base-id`）。
2. 用户只给库名 → 当前实现按 base_id 工作；若不知道 id，向用户要 base_id（别替用户猜一个数字去试）。
3. 用户啥都没给 → 用配置里的默认 base_id，并在输出里注明用的是哪个库。

**凭证纪律（硬性）**：
- token 只经 `Authorization: Bearer` 头发给固定的 2brain 端点；
- **绝不**把 token 打印到对话、写进 HTML/JSON 产物、放进日志或 URL query；
- 引擎已保证产物不含 token；你转述结果时也不要复述 Key。

**输出纪律**：
- 每个任务的数字（节点数、count、百分比、权重）**只能来自 `kw_graph.py` 的 stdout**，不得凭记忆或想象编造。
- 关键词图谱只显示**同级占比百分比**（节点在其直接兄弟中的 count 占比），不显示原始 count；每组同级合计 100%。这**不是**全库绝对占比。
- 图谱/结构为空或关键词极少 → 如实说「该库资料不足以成图」，不要自由发挥补内容。
- 解读关系（relate）只基于关键词在树中的**层级同现**，显式声明：不代表因果、语义等价、文档级来源。

**只读边界（本 Skill 不做）**：
- 不入库、不抓取、不建库、不删库、不改库；
- 不做 2brain 问答（chat）——那是另一条能力；
- 不路由到飞书 Wiki / 云文档 / 本地文件——「知识库」在这里特指 2brain 平台的库。

**缓存与幂等**：命中的树缓存到 `~/.local/state/2brain-keyword-map/graphs/<base_id>.json`。用户隔一会儿再问同一个库，直接命中缓存即可；想要最新用 `--fresh` 重拉（如刚入库了新资料）。

## 输入输出示例（关键词图谱）

**Input**（用户对 agent 说）：

> 帮我看下求职库（base 700）的关键词图谱

**执行**：

```bash
python3 scripts/kw_graph.py graph --base-id 700 --html /tmp/kw-700.html
```

**引擎 stdout**（你据此转述，不要照搬 JSON 给用户）：

```json
{"ok": true, "task": "graph", "base_id": 700, "file_count": 256,
 "levels": {"l1": 10, "l2": 21, "l3": 45},
 "metric": "sibling_count_percentage", "html": "/tmp/kw-700.html"}
```

**你给用户的话（示例模板）**：

> 库 700（256 篇资料）的关键词图谱已生成：10 个一级主题、21 个二级、45 个三级。
> 最重的一级主题是 Research 和 Technical。图在 `/tmp/kw-700.html`，点一级主题会在同一张图里展开二级、三级。图上百分比是同级占比，不是全库占比。

## 脚本清单

| 文件 | 职责 |
|---|---|
| `scripts/kw_graph.py` | 引擎：凭证解析 + `keyword_api` 客户端 + 缓存 + 四子命令（structure/topics/graph/relate）+ 环形 HTML 渲染 |

## 边界（再次强调）

- 只读 2brain 关键词图谱；不写、不问答、不建库。
- 数字只来自引擎输出；不编造关键词或关系。
- token 永不出现在任何产物或对话里。
