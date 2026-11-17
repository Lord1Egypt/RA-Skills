---
name: openapi-lark
description: 把项目 OpenAPI / Swagger spec（本地 yaml/json **或 http(s):// URL**）同步到飞书 / Lark wiki & docx 文档树。支持 single / tree / endpoint（每接口一个 wiki 子节点）三种结构，自动按 tag 拆分 + path-prefix 分子组，中文优先标题、allOf 扁平化、响应字段表 + JSON 示例、hash 缓存、dry-run 真不推线上。对接 chanfana / Hono / FastAPI / NestJS Swagger 的 runtime /openapi.json 端点。用于替代 yapi 文档管线。Trigger 当用户说「同步接口文档到飞书」「openapi 推到飞书」「openapi 推到 lark」「替换 yapi」「lark docs from openapi」「swagger to feishu」「飞书 API 文档自动化」「按 tag 拆文档」「每个接口一个文档」「runtime openapi URL 同步」「chanfana / Hono / FastAPI openapi 推到飞书」「openapi-lark」时。
---

# openapi-lark — OpenAPI → 飞书 / Lark wiki tree

> 决策规则：何时跑哪条命令，多服务怎么组织，故障怎么诊。
> 命令的具体 flag 看 `openapi-lark <cmd> --help`，不在本文件里维护（避免与 CLI 漂移）。

## 安装

一次性：

```bash
npx skills add leeguooooo/openapi-lark
```

之后所有命令走 `npx -y -p github:leeguooooo/openapi-lark openapi-lark <cmd>`，本 skill 已在调用前缀里嵌好。

**前置：**
- lark-cli 已安装：`npx @larksuite/cli@latest install`（官方唯一推荐方式；详见 [larksuite/cli](https://github.com/larksuite/cli)）+ `lark-cli auth login --recommend`
- 推荐 lark-cli ≥ 1.0.34（`auth check` 子命令，doctor 用它真验 scope）
- 项目里有 OpenAPI 3.x — 可以是 **本地文件**（`api/openapi.yaml`）**或 http(s):// URL**（runtime 生成的 `/openapi.json` 端点，见下文）

## URL openapi 源（chanfana / Hono / FastAPI / NestJS Swagger）

v1.10 新支持。runtime 生成 `/openapi.json` 的框架，不用再 `curl > 快照` 维护过期文件：

```yaml
services:
  - name: ai-girls
    openapi: https://ai-girls.example.workers.dev/openapi.json
    openapiHeaders:                  # 可选，鉴权头；${ENV} 插值
      Authorization: "Bearer ${OPENAPI_TOKEN}"
    openapiSnapshot: api/openapi.snapshot.json   # 可选，落盘做 git PR diff
    mode: endpoint
    docToken: ${LARK_DOC_AI_GIRLS}
```

- `${ENV}` 会被 config 加载阶段自动展开（保密信息不落盘）
- `openapiSnapshot` 写的是 fetch 后的原始 JSON（不是 dereferenced），便于 PR review API 变更
- `lint` / `doctor` 都已适配 URL 源（doctor 改做 HEAD 探活，不再误报 file not found）
- 已知限制：外部 `$ref` 跨 URL 不解析；chanfana / Hono / FastAPI 输出的 openapi 通常自包含，几乎不踩

## 多 service 项目（一个 wiki URL 接 N 个 openapi）

v1.8 新支持：项目里有多个 openapi spec（admin / game / internal / ...），用户只给一个 wiki 父节点 URL。工具自动在该父节点下建 N 个兄弟子节点，每个 service 一个。

```yaml
# .openapi-lark.yaml
parentDocToken: XJ51wLKIXidz...    # ← 用户给的 wiki URL 解析出来的 token
services:
  - name: admin
    openapi: api/generated/admin/openapi.json
    parentTitle: 管理端 API          # ← 自动创建的子节点标题
    mode: endpoint
  - name: game
    openapi: api/generated/game/openapi.json
    parentTitle: 用户端 API
    mode: endpoint
  - name: game-internal
    openapi: api/generated/game-internal/openapi.json
    parentTitle: 内部 API
    mode: endpoint
  - name: sports-event
    openapi: api/generated/sports-event/openapi.json
    parentTitle: 体育赛事 API
    mode: endpoint
```

首次 sync 自动建 4 个子节点；token 存到 `.openapi-lark/auto-tokens.json`（gitignored），后续 sync 复用。缓存 miss（换人 clone / 换机器 / 删了 `.openapi-lark/`）时会先列 parent 下已有子节点按标题认领，**不会重复建树**（v0.10.1+）。

## 单 service 项目（一个 openapi 一个 wiki URL）

```
[1] 飞书 wiki 创建父节点 —— ⚠ 必须是这个项目专属的节点
    在你的 wiki space 里手工新建一个 docx 节点（比如标题 "项目 X API"）。
    复制 URL，形如 https://<host>/wiki/<TOKEN>
    ⚠ 不要把 docToken 指向 wiki 空间根 / 多项目共享节点：sync 会把本项目的
      tag 节点散落进去跟别人混在一起，且 zombie 报告会误判别人的文档。
      （endpoint sync 会自动检测并 stderr 警告这种误配，见「docToken 防护」）

[2] 项目根 init
    cd <project>
    npx -y -p github:leeguooooo/openapi-lark openapi-lark init \
      --name <svc> \
      --openapi api/openapi.yaml \
      --doc-url <wiki url>
    # init 默认会往项目根 CLAUDE.md 注入一段"AI 怎么查本项目接口"的引导块
    # （幂等，begin/end marker 之间被托管；不想要加 --no-claude-md 跳过）

[3] 编辑 .openapi-lark.yaml，至少加这几项：
    services:
      - name: <svc>
        ...
        mode: endpoint             # 强烈推荐 endpoint 模式
        parentTitle: <项目 X>       # 防止父节点标题被覆盖

[4] 首次同步（~5-15 分钟，取决于接口数）
    openapi-lark sync

[5] 再次同步（hash 缓存生效，几秒）
    openapi-lark sync
```

把 `.openapi-lark.yaml`、`CLAUDE.md` 和 `.gitignore`（加 `.openapi-lark/`）提交进 git。

> 💡 重跑 `init` 是安全的：用 yaml Document API 改写，保留你手写的注释和 `tagAliases` 等自定义字段；CLAUDE.md 只替换 marker 之间的托管块。

## 三种 sync 模式

`.openapi-lark.yaml` 的 `services[].mode` 字段决定结构：

| mode | 飞书呈现 | 适用 |
|---|---|---|
| `single`（默认） | 单个 docx 装所有内容 | 小 openapi（<600 KB 渲染后），单文档够看 |
| `tree` | 父 docx + 每 tag 一个子 wiki 节点 | 中等规模，按 tag 分组够用 |
| `endpoint` | 父 docx + 每 tag 中间节点 + 每接口一个叶子 | 大规模 / 想每接口独立可链接（推荐） |

**endpoint mode 是默认推荐**：
- 用户在飞书 wiki 树侧栏看到的就是每个接口标题（中文 summary 在前）
- 每个接口独立 docx，单文档体积小、撞不到飞书 1MB 上限
- 修一个接口只重推一个 doc（hash 缓存）
- tag 中间节点只是 TOC（不会膨胀）

## endpoint mode 的两个安全输出（看 stderr）

1. **zombie 报告**：sync 结束后列出父节点下「本次没被任何接口认领」的旧节点
   （标题 + nodeToken + URL）。这些是 spec 里已删的接口 / 早期残留。**默认只警告、
   不动节点**；人工 review 后用 `lark-cli wiki +move` 移走，**或开启下面的 auto-prune**。
   - 身份匹配用 `METHOD + path`（不是标题）：改 `summary` / `tagAlias` 不会再制造
     新 zombie，旧节点原地更新 + 改名（靠 `.openapi-lark/node-map.json` 持久化映射）。
   - **auto-prune（已实现，opt-in）**：在 service 上配 `prune`（见下）后，sync 会
     自动清理 zombie 列表里的节点——**只动该列表里的节点**，绝不碰检测逻辑之外的任何节点。

### auto-prune 配置（`prune` / `pruneSpaceId`）

```yaml
services:
  - name: my-api
    mode: endpoint
    docToken: WIKI_NODE_TOKEN
    prune: off          # off（默认，只警告）| move | delete
    pruneSpaceId: "73…" # prune: move 时必填——zombie 移到的目标 wiki space（当回收站）
```

| 值 | 行为 | 用的 lark-cli 命令 | 需要 scope |
|---|---|---|---|
| `off`（默认） | 只检测 + 警告，**不动任何节点**（升级老用户行为完全不变） | — | — |
| `move` | 把每个 zombie 移到 `pruneSpaceId`（**可逆**，推荐） | `wiki +move --node-token <t> --target-space-id <pruneSpaceId> --source-space-id <src>` | `wiki:node:move` |
| `delete` | **不可逆**删除每个 zombie | `wiki +node-delete --node-token <t> --obj-type wiki --space-id <src> --yes`（`--obj-type` 是 token 种类，删 wiki 节点固定 `wiki`） | wiki 节点删除 scope |

- `prune: move` 缺 `pruneSpaceId` → 打清晰错误并**退回只警告**，绝不瞎删。
- prune 成功后会从 `node-map.json` + `sync-lock.json` 移除该节点条目，下次不再当 zombie。
- 单节点失败（权限 / 网络 / 已不存在）→ 记日志跳过，**不中断整个 sync**。
- `--dry-run` 下只打印 `(would) prune …`，**不真删 / 移**。
- ⚠ **误删不可逆**：飞书 wiki 托管的 docx 删了恢复不了。**强烈建议先用 `move` 到一个
  专门的回收 space**，确认无误再考虑 `delete`。`drive +delete` 对 wiki docx 返 forbidden，
  所以清理只能走 `wiki +move` / `wiki +node-delete`。
2. **docToken 误配警告**：若父节点下 ≥5 个子节点且 ≥80% 既不匹配本 spec 的 tag、
   也不像 API 文档 → 警告 docToken 可能指错到共享 / 空间根节点。纯警告不阻断。
   正常项目即使有历史 zombie（外来占比低）也不会误报。

## 工作流决策树

```
用户给了什么？
├─ 项目里还没 .openapi-lark.yaml
│   └─ 用上面「新项目快速开始」
│       init 现在默认写 mode:endpoint + 从 info.title 推 parentTitle
├─ 项目的 openapi 是 runtime 生成（chanfana / Hono / FastAPI / NestJS Swagger）
│   └─ 直接把 /openapi.json 的 URL 填进 services[].openapi
│       要鉴权就配 openapiHeaders；要 PR diff 就配 openapiSnapshot
├─ 已有 .openapi-lark.yaml，用户改了 openapi
│   └─ openapi-lark sync
│       内容没变的接口被 hash cache 自动 skip；想强推加 --force
├─ 用户问「飞书父节点标题被改成 Authentication / Untitled 了」
│   └─ 在 config 加 parentTitle: "<期望名>"；下次 sync 自动锁定
├─ 用户问「响应字段表只有 default 没有 200」/ 「字段不全」
│   └─ 已自动修复（v1.7+ 内置 allOf 扁平化 + 完整 schema 展开）
│       老的 sync-lock.json 删掉重跑一次即可
├─ 用户问「能不能给接口加请求/响应示例」
│   └─ v1.7+ 已自动从 schema 合成 JSON 响应示例
├─ 用户问「飞书呈现样式 / 段落看不懂」
│   └─ openapi-lark render <svc> → 看本地 md（render 命令零服务端调用）
│       中文优先标题 / 段落本地化 / operationId→summary 都已生效
├─ 用户问「环境配置对吗 / lark-cli 缺了 / 缺 scope」
│   └─ openapi-lark doctor（v1.10 起会真用 lark-cli auth check
│       预检 wiki:node:create / wiki:node:read / docx:document:write_only，
│       缺哪条直接告诉你；token 6 小时内过期还会警告）
├─ 用户问「lark-cli 提示 missing scope」
│   └─ 见下方「鉴权 scope」节
└─ 用户问「不推送只看效果 / 试一下不出意外」
    └─ openapi-lark sync --dry-run
        v1.10 起 endpoint/tree 模式 dry-run **真不会**创建 wiki 节点
        或推 docx，日志每行加 (would) / (dry-run) 前缀
```

## 配置参考（完整）

```yaml
engines:
  larkCli: ">=1.0.34"               # auth check 子命令需要 1.0.34+

# 可选：覆盖底层 lark-cli 二进制名（默认 lark-cli；旧发行版叫 lark）
# larkBin: lark

# 可选：每接口推送大小上限（默认 600 KB；endpoint mode 一般用不到）
# 注：飞书 docx server 实测 1MB+ 必超时；endpoint-split 之后每个 leaf
# 一般 10-30 KB
maxPushBytes: 1000000

# 可选：跨 repo 共用基础配置（单层 extends）
# extends: ./shared/lark-docs.yaml

# Lockfile 路径：.openapi-lark/sync-lock.json（自动生成；加进 .gitignore）

services:
  # 本地文件源（最常见）
  - name: voice-room                  # 服务名（lockfile + 输出目录用这个）
    openapi: api/openapi.yaml         # 相对项目根
    docToken: Uc6hwkXXXX              # 父 wiki 节点 token（不是 docx token！）
                                      # 用 ${LARK_DOC_X} env 引用更好
    mode: endpoint                     # single | tree | endpoint
    parentTitle: 语音房                 # 强制锁定父 wiki 标题（防止被偷）
    tagAliases:                        # 中文化 tag 显示名
      "voice-room": "语音房接口"
      "admin": "管理端接口"
    includeTags: [基础服务, 语音房]      # 可选：只同步这些 tag
    excludeTags: []                    # 可选：跳过这些 tag

  # URL 源（chanfana / Hono / FastAPI / NestJS Swagger 运行时拉，v1.10+）
  - name: ai-girls
    openapi: https://ai-girls.example.workers.dev/openapi.json
    openapiHeaders:                    # 可选：鉴权头；${ENV} 插值
      Authorization: "Bearer ${OPENAPI_TOKEN}"
    openapiSnapshot: api/openapi.snapshot.json  # 可选：落盘做 PR diff
    docToken: ${LARK_DOC_AI_GIRLS}
    mode: endpoint
    parentTitle: AI Girls API
```

## 多服务组织建议

- **同一团队多个微服务**：在每个服务的 repo 根放 `.openapi-lark.yaml`，每个 service 用自己的 docToken。不要把所有服务的 docToken 都塞进一个仓库
- **跨仓库共用 docToken 池**：用 `extends: ./shared/lark-docs.yaml` 引用同一份基础配置；子配置只覆盖差异
- **多环境（dev / staging / prod）**：docToken 用 `${LARK_DOC_VOICE_ROOM_PROD}` 之类的 env 引用；CI 注入不同环境的 token

## 团队 / CI 同步（重要）

**多人团队 sync 应该放 CI 跑，不是每个 dev 本地手敲。** 决策依据：

- ✅ wiki 永远跟 main 一致（唯一真理源 = main 分支）
- ✅ devs 不用各自申请 wiki 写权限 / 不用走开放平台审 scope
- ✅ lockfile 在 CI cache 跨 run 持久，团队共享增量缓存

**CI 鉴权（bot 身份，环境变量）：**

```bash
LARKSUITE_CLI_APP_ID=cli_xxxxxxxx
LARKSUITE_CLI_APP_SECRET=xxxxxxxxxxxxx
LARKSUITE_CLI_BRAND=feishu          # 或 lark
```

前置：bot 必须被加进目标 wiki 空间作为编辑协作者（飞书 wiki「成员管理」里添加）。

**GitHub Actions / Jenkins 完整范本**：见 [README 的「团队 / CI 同步」节](https://github.com/leeguooooo/openapi-lark#-%E5%9B%A2%E9%98%9F--ci-%E5%90%8C%E6%AD%A5%E6%8E%A8%E8%8D%90%E5%A7%BF%E5%8A%BF)。

**devs 本地做什么**（CI 接管 sync 之后）：

```bash
openapi-lark lint                 # PR 前校验 openapi + 配置
openapi-lark render <svc>         # 纯本地预览（零远程调用）
openapi-lark sync --dry-run       # 完整 dry-run（仍读 wiki 验解析）
```

不需要本地装 hook、不需要本地配 LARKSUITE_CLI_APP_*。

**git hook（仅推荐 solo dev / 小团队没 CI）**：

```bash
openapi-lark install-hook           # post-commit 非阻塞
openapi-lark install-hook --kind pre-push   # 阻塞型
OPENAPI_LARK_SKIP_HOOK=1 git commit ...     # 单次跳过
```

## 搜索 / 查接口（跨项目）

当 agent 在另一个项目里被问「voice-room 创建房间接口长啥样」「查一下 POST /api/xxx 的参数」时，**不要新装搜索工具**——直接用 lark-cli 搜飞书 wiki，配合本 skill 的命名规律就行。

**命名规律（openapi-lark 同步出的 wiki 节点）：**

| wiki 节点层级 | 标题格式 | 例子 |
|---|---|---|
| 项目根 | `<parentTitle>` 或服务名 | `语音房` |
| tag 中间节点 | `<tagAliases[tag]>` 或 tag id | `语音房接口` |
| path-prefix 子组（≥8 接口时自动产生） | 第一段路径名 | `voice-room` / `tags` / `badges` |
| **接口叶子** | **`<summary> — <METHOD> <path>`** | `创建语音房间 — POST /api/voice-room/create` |

agent 看到标题里有 ` — METHOD ` 就知道这是个接口叶子，不是组。

**典型搜索套路：**

```bash
# 按业务关键词搜（最常用）。drive +search 实测可命中 path / 中文 summary / 单词，
# 返回带 highlighted snippet。⚠ 不要加 --doc-types wiki 之外的过滤会清零结果时，
# 直接省略 --doc-types 让 wiki+docx 都参与召回。
lark-cli drive +search --query "创建房间" --doc-types docx
# 结果里 title 含 ` — POST ` / ` — GET ` 的就是接口叶子
# 拿 obj_token 后：
lark-cli docs +fetch --api-version v2 --doc <obj_token>
# 即可读到该接口完整文档（参数表、响应表、JSON 示例）

# 按方法+路径搜
lark-cli drive +search --query "POST /api/voice-room/create" --doc-types docx

# 列出某项目所有接口（先拿父节点 token，再列子节点递归）
lark-cli wiki +node-list --space-id <X> --parent-node-token <project parent> --page-all
# 再对每个 tag 中间节点递归列子节点 → 拿到所有接口标题
```

**agent 的最佳实践（写进对话脚本里）：**

1. 用户问「X 接口长啥样」→ `lark-cli drive +search --query "X" --doc-types docx`
2. 结果过滤：保留 title 匹配 ` — (GET|POST|PUT|DELETE|PATCH) ` 的条目
3. 没命中：换关键词；命中 1 条：直接 `docs +fetch` 展开
4. 命中多条：让用户选，或显示 title + path

**为什么这套行得通：**
- title 锁定（lockTitleInMarkdown）保证每个 docx 标题都是 `<summary> — <METHOD> <path>`
- 一行就能眼判是不是接口
- summary 是中文 → 自然语言搜索能命中
- METHOD + path 是英文 → 精确技术搜索也能命中

## 鉴权 scope

`lark-cli auth login` 默认 scope 够用于基础读写。但下列操作需要额外 scope。

**scope 名取自飞书开放平台官方文档**（实测：`wiki:node:write` 不存在，飞书会返回 invalid scope）。如果某条 API 提示 "missing scope"，按下表对应一次性补齐：

| 操作 | 推荐 scope（细粒度） | 兜底 scope（粗粒度） |
|---|---|---|
| 读 docx 内容 | `docx:document:readonly` | `docx:document` |
| 创建 / 更新 docx | `docx:document` | — |
| 读 wiki 节点信息 | `wiki:node:read` | `wiki:wiki:readonly` |
| 创建 wiki 子节点 | `wiki:node:create` | `wiki:wiki` |
| **移动 wiki 节点（prune: move 清理 zombie）** | `wiki:node:move` | `wiki:wiki` |
| **删除 wiki 节点（prune: delete 清理 zombie）** | wiki 节点删除 scope（`wiki:node` 写权限） | `wiki:wiki` |
| **删除 docx**（少见） | `space:document:delete`（但 wiki 托管的 docx 仍 forbidden，需用 move/node-delete） | — |

> 💡 `openapi-lark doctor` 现在会用 `lark-cli auth check --scope "..."` 预检关键 scope（需要 lark-cli ≥ 1.0.34），缺了会直接告诉你补哪条。

需要时跑（示例：把上面表里你缺的 scope 拼起来）：

```bash
# 预检（无浏览器跳转，秒返）
lark-cli auth check --scope "wiki:node:create wiki:node:read docx:document:write_only"

# 补缺（按 doctor 提示拼）
lark-cli auth login --scope "wiki:node:create wiki:node:move space:document:delete"

# 或一次开足官方推荐 scope（懒人模式）
lark-cli auth login --recommend
```

`auth login` 会输出 verification URL，浏览器打开授权后 CLI 自动拿新 token。

## 故障诊断序

按下面顺序，每一步通过再进下一步：

1. `openapi-lark doctor` — 环境层（lark-cli、auth tokenStatus + expiresAt、scope 探针、openapi reachability）
2. `openapi-lark lint` — 配置层（schema、openapi 语法、env 变量；URL 源走带鉴权 fetch）
3. `openapi-lark render <svc>` — 渲染层（widdershins 输出 + heading 越级 warning，零服务端调用）
4. `openapi-lark sync --dry-run` — 端到端**真不推**（v1.10 修复：endpoint/tree 模式之前会真创建 wiki 节点）
5. `openapi-lark sync <svc>` — 真推送（首次会 push 全部；之后只推内容变了的）
6. `openapi-lark sync --force` — 跳过 hash cache 强推（修复疑似不同步）

> 💡 默认 widdershins 的 doT 编译日志（"Loaded def..." / "Compiling code_csharp.dot..."）已被静默。想看回来：`OPENAPI_LARK_VERBOSE=1 openapi-lark sync`。

## 自动处理的渲染细节（v1.7+）

不需要你做任何配置，sync 时自动生效：

- **中文优先标题**：endpoint 标题是「<summary> — <METHOD> <path>」
- **allOf 扁平化**：BaseResponse + 业务字段的常见包装会被完整展开成单表
- **段落本地化**：Parameters→参数 / Responses→响应 / Response Schema→响应 Schema / Enumerated Values→枚举值 等
- **operationId → summary**：`## getXxx` 替换为 `## 获取 XXX`
- **响应 JSON 示例**：从 schema 合成真实示例值（用 example/format/enum/类型默认值），末尾 `### 响应示例 (200)`
- **鉴权段**（v0.4）：按 operation `security`（缺省回退全局 `security`）翻成中文指令，紧跟 METHOD/path 行，如 apiKey-in-header → `需在请求头携带 X-Api-Key: <key>`，http bearer → `需在 Authorization: Bearer <token> 头携带令牌`，`security: []` → `无需鉴权`
- **约束列回填**（v0.4）：参数表自动插入「约束」列并从 parsed schema 填充 widdershins 丢掉的校验（minimum/maximum/默认值/minLength/pattern/枚举/format 等），如 `limit` → `1–100，默认 20`
- **请求示例 curl**（v0.4）：从 METHOD/path（路径参数填 example）+ 必填 query 参数 + 鉴权头（+ 写操作的 JSON body）合成可复制 `### 请求示例`
- **DocxXML 富排版**（仅 endpoint 模式）：endpoint leaf 文档以 Lark DocxXML 推送（`docs +update --doc-format xml`），叠加可正常落地的富 block —
  - 📌 顶部速览 callout：METHOD/path · 鉴权 · 用途 · TTL/上限提示（一眼卡片，不复制正文）
  - 示例 caption：请求体 / 请求 / 响应代码块 `<pre lang caption="请求体示例 / 请求示例 / 响应示例 (200)">`
  - ☑️ 调用前检查 checkbox（**条件**）：`<checkbox>` 仅列 spec 可推导项（鉴权 / 必填参数 / 分页），最多 4 条，少于 2 条则整段跳过。
  - 轻量 `<hr/>` 分隔各主区块（参数 / 响应 / 响应 Schema / 示例 / 调用前检查）。
  - **v0.7 可读性**：① 响应 Schema 字段名 → 完整点路径（`data.activities[].activityId`，数组父级加 `[]`），不再用 `»»»`；② POST/PUT/PATCH 接口新增 pretty-print **请求体示例 (JSON)**（从 requestBody schema 合成，example/default/enum/format/类型默认值）置于 curl 请求示例之前，并 strip 掉 widdershins 的原始 `> Body parameter` schema dump；③ 单一鉴权方案时 drop 独立「鉴权」段（callout 已含），多方案（OR）才保留；④ 移除固定骨架的「调用流程」mermaid 图。
  - **v0.10 必填列 + 真彩色（post-push 块着色）**：所有字段表（参数 / 响应 Schema / 请求体）的「必填」列单元格 → 必填用「必填」(红字)、可选用 `—`。识别 `true`/`false` 与 `是`/`否`/`required` 取值；仅改该列单元格，列头与其他列不动。**颜色不走导入路径**（那会被剥离），而是 **post-push 块着色 pass**（`src/lark/block-style.ts`）：每个本次实际推送成功的文档，拉取 blocks → 按可插拔规则定位文本元素 → 一次 `docx/v1/documents/{id}/blocks/batch_update` 上色。当前规则 `ruleRequiredCellsRed`：定位字段表「必填」列，对**正文行**（跳过表头）值为「必填」的单元格设 `text_color:1`。best-effort：拉取/更新失败仅告警，不把 push 结果翻成 failed；dry-run / cache-skip 文档不跑（每个推送文档 +1 fetch +1 batch_update）。调色板 1红/2橙/3黄/4绿/5蓝…15灰；`background_color` 同理（留作后续 highlight 规则）。

  实现是 markdown→XML 转换（复用全部既有后处理），XML 生成或推送失败时自动回退 markdown 推送，绝不阻断 sync。single / tree 模式仍走 markdown。
  > ⚠️ Lark 文档导入 API 会剥离颜色属性（callout/th/span 的 bg + text-color，仅在编辑器内手动设置才生效）与 `<button>`，故不输出颜色 / 按钮——它们是 dead markup。可正常落地的：callout 结构+emoji、pre caption、checkbox、grid/column、whiteboard(mermaid)。表格单元格前导 ASCII 空格会被 trim（故 Schema 缩进用点路径而非空格）；U+3000 全角空格可存活但当前用不到。请勿再加回颜色属性或 button。
- **sync 进度输出**（v0.8）：endpoint 模式不再像卡死 —— 显示阶段标题（`📋 阶段 1/2 规划结构`、`🚀 阶段 2/2 待推送：共 N 个接口`，总数前置）、规划期滚动计数（`规划中：已对账 k 个节点…`，每 ~20 节点/~2s 节流）+ 结束 summary（`规划完成：对账 X 节点 / Y 标签 / Z 分组 / W 待清理 zombie`）、每个接口推送带 `[i/N] p%`（`[42/175] 24% ✓ <标题> — <METHOD path> … (2.5s)`）。dry-run 也走推送计数。失败/告警仍在结尾汇总。
- **sync 缓存纳入工具版本**（v0.6）：跳过缓存的 hash 现含 openapi-lark 自身版本号（`openapi-lark@<version>` 前缀）。渲染层升级（即使源 spec 未变）也会令所有接口的 hash 变化，普通 `sync` 自动重推，无需 `--force`。修复 v0.5.1 升级后 "175 skipped / 0 pushed"、清理后的输出没到 Lark 的问题。
- **删多余 boilerplate**：widdershins 的 Code samples / 200 Response 错误 dump / aside / 全局 Base URLs + Authentication 前言 / Generator 注释 / 空 H1 等全部 strip
- **docx title 锁定**：每个 docx 唯一 H1 = 我们的目标标题（lark 用 first H1 当 title）
- **XML NUL 泄漏 + partial_success 修复**（v0.10.3，issue #3）：① 行内标记嵌套（bold/link 内含 `code`）时占位符改为循环还原，不再把裸 NUL 泄进 XML（NUL 会让飞书 docx import 在 degrade_code=3001 处截断全文）；② `docs +update` 返回 `result=partial_success` 或非空 `warnings` 时视为推送失败（XML 路径自动回退 markdown 重推），不再误报 ✓；③ 兜底：最终 XML 输出剥离所有 XML 非法控制字符。
- **parentDocToken 跨用户去重**（v0.10.1）：auto-tokens 缓存 miss（换人 clone / 换机器 / 删 `.openapi-lark/`）时，先列 parent 已有子节点按标题（忽略大小写/首尾空白）认领并写回缓存，找不到才创建——修复"另一个用户跑 sync 整棵树重复建一份"。列子节点失败仅告警，退回创建行为不阻断 sync。
- **未共享状态警告**（v0.10.1）：sync 启动时检测「本机无任何 `.openapi-lark/` 状态文件 + 该目录被 .gitignore 忽略」（即换人 clone / 换机器首跑），stderr 警告：hash 缓存不随 git 共享，本次会按标题认领线上文档并全量重推；建议多人协作把 `.openapi-lark/` 移出 .gitignore 提交，或固定由 CI 执行 sync。只在首跑触发一次，本机有状态后不再出现。
- **path-prefix 自动分子组**（v1.9+）：同 tag 接口 ≥8 个时按 `/foo/bar/*` 路径前缀自动拆 4 级树，无需配置
- **createWikiChild 锁冲突自动重试**（v1.9+）：飞书 wiki 服务端 131009 错误自动退避重试

## 不要做的事

- **不要在被同步的 docx 里手写内容**：sync 会覆盖全文，手写部分会丢失。文档由本工具拥有。
- **不要在 CI 里 `--parallel` 超过 4**：飞书服务端会限速
- **不要用 `--engine native`**：v1 没实现，会 exit 2
- **不要把 docToken 直接硬编码进 yaml**：用 `${LARK_DOC_X}` env 引用，便于跨环境
- **不要在飞书 wiki 已有内容的节点上 init**：sync 会清空它。专门建一个新 docx 给本工具用。
- **endpoint mode 首次 sync 慢是正常的**（每接口要 createWikiChild + push，167 个 ~8-16 分钟）；之后 hash cache 让重跑变成秒级

## 退出码语义

| code | 含义 |
|---|---|
| 0 | 成功（含 warning / skipped） |
| 1 | 业务失败（per-service：渲染 / push 失败） |
| 2 | 配置错误（missing yaml / schema 失败 / env 未注入 / 不允许的参数） |
| 3 | 环境错误（lark-cli 缺失 / 版本不达标 / auth 失效） |

## 已知行为（不是 bug）

- **首次同步前应在飞书 wiki 手工创建一个项目专属父节点作为容器**；--doc-url 用它。别指向共享 / 空间根节点（endpoint sync 会自动检测并警告，见「endpoint mode 的两个安全输出」）
- **docx +update --command overwrite 会清空 docx**，评论 / 锚点会丢失。被 openapi-lark 拥有的 docx 不要参与协作讨论
- **删除 wiki zombie 节点**：drive +delete 对 wiki-托管 docx 返 forbidden；用 `lark-cli wiki +move --target-space-id <别处>` 移走是有效的「清除」手段
- **lark docx 不支持真正的「折叠块」**（markdown 和 XML 都不支持 collapse 容器）；JSON 示例放在 `### 响应示例` 子标题下，用户可通过 wiki 大纲折叠
- widdershins 渲染的某些 heading 越级（H2→H4）只能 warn，不能自动改 md
