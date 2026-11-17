> **这是 `SKILL.md` 的中文版参考文档，不是第二份 skill manifest。**
> 唯一权威的声明（name / version / metadata.openclaw / 触发词 / 环境变量）在仓库根目录的
> `SKILL.md` frontmatter 里；本文件只提供中文说明，刻意不带 frontmatter，以免出现两份
> 互相矛盾的声明。若本文与 `SKILL.md` 有出入，以 `SKILL.md` 为准。


# JobWatch — 求职监控 Agent 引擎

## 给人类：30 秒看懂（其余部分是给你 agent 的操作手册）

**它做什么**：让你的 OpenClaw agent 变成求职哨兵——7×24 盯你指定公司的 careers 页，
用 LLM 拿 JD 全文对照**你的**画像判级：强匹配（P1）实时提醒、次要的（P2）每天 9 点
打包成摘要、其余入库留档。还能记投递状态（「Stripe 那个我投了」）、答查询
（「本周有什么好岗位」）、识别挂了 90 天的 ghost job。

**怎么装**（唯一前提：装好的 OpenClaw）：

```
openclaw skills install jobwatch
```

**怎么开始**：对你的 agent 说一句「帮我做求职监控」。接下来是约 10 分钟的入职面试——
目标公司、你的背景（可以直接丢简历给它）、红线（visa/地域/岗位类型）、级别意向（IC 还是
管理线）、三项配置（通知渠道 / 知识库 / JD 抓取，可以回答「全部默认」一键跳过）。
然后它会自己探测各公司用的招聘系统、生成你的求职画像、抓一轮真实岗位试判、拿结果和你
校准（判错了直接说，它会改），最后发一条示例提醒给你看效果，征得你同意后注册定时任务
上岗。

**可选增强**（都不是必须）：Firecrawl 或 Jina key（JD 抓取更干净，监控 Google 系公司
基本必需）· Telegram 直连（独立于对话渠道的低延迟推送）· 2brain（云端知识库+图谱问答）。

**想重来一次 onboarding**：删掉 `<workspace>/jobwatch/` 目录 + 给 agent 开个新会话（频道里发 `/new`）——旧会话的对话记忆里还留着上次的入职记录。skill 本体不用动。

---

## 隐私与数据流（重要 · 安装前请读）

这个 skill 会**采集个人隐私、调用外部服务、注册定时任务**。以下是完整清单——每一项都在 onboarding 里征得你同意后才发生，你可以拒绝任一项或全部走默认最小配置。

**代码强制，不只是文档承诺（v1.2.0 起）**：每一条携带用户数据的出网调用都先过
`scripts/common.py` 的 `require_egress_consent()`，**没授权直接抛错**，不发。授权按目的地
分开给——`llm` / `firecrawl` / `jina` / `twobrain` / `telegram`——来源是
`JOBWATCH_EGRESS_ALLOW`（逗号分隔或 `all`）或入职写的 `state/egress_consent.json`。
每个目的地在一次运行里首次使用时，会往 stderr 打一行，说明**发了什么、发去哪**，
所以没有任何一次传输是悄悄发生的。发往公开 ATS 板（Greenhouse / Ashby / Lever）的请求
只带公司 slug（公开信息），不走这道门，但同样会在 stderr 报出目的地。

**① 采集并本地保存的个人数据**（存在 `<workspace>/jobwatch/profile/JOB_PROFILE.md` 与 `state/`）：
- 你的简历要点、目标级别、IC/管理线意向、地域/远程要求；
- **visa / sponsorship 需求、红线**等敏感就业信息；
- 投递状态记录（投了/面试/offer/拒）。

> **文件在本机，内容不一定全留在本机。** 画像文件本身不作为文件上传，但**它的正文**
> 会在两种情况下发给你配置的 LLM 端点：`judge.mode=api` 把 **`JOB_PROFILE.md` 全文**
> （简历要点、visa 需求、级别、红线）放进 system prompt 随每条 JD 发出，开了 stage-1 筛
> （`screen.enabled=true`）则发送同一份文件的前 ~1200 字。两条都受 `llm` 出网
> 许可管，且在默认配置下都不发生（`judge.mode=agent` + `screen.enabled=false`，判级在
> 宿主 agent 里做，没有任何画像内容经本 skill 出网）。另外开云知识库
> （`kb.backend=twobrain`）会上传归档 JD 和你的提问。想全清除：删 `<workspace>/jobwatch/` 目录。

**② 发往第三方的数据**（仅针对你显式配置的目标公司/信源）：
| 外部服务 | 收到什么 | 何时 | 可否关掉 |
|---|---|---|---|
| Greenhouse / Ashby / Lever 官方 API | 你选的公司 slug（公开信息） | 每轮 cron | 是（换信源） |
| 同上三个 ATS，仅入职时 | 从你报的公司名**猜**出来的 slug（`discover_board.py`） | 每加一家公司跑一次，不上定时 | 是（跳过探测，自己贴 board slug） |
| Firecrawl `api.firecrawl.dev` / Jina `r.jina.ai` | 你监控的 JD 页 **URL** | 抓取 JD 时 | 是（不配 key 走降级/不抓） |
| 你配置的 LLM 端点（OpenAI 兼容） | **JD 全文 + `JOB_PROFILE.md` 全文**（stage-1 筛发前 ~1200 字） | 判级时 | 是（默认 agent 模式不发；或指自建/本地端点） |
| 2brain 知识库 `test/portal.2brain.ai` | 归档的 JD 文档、你的提问 | 入库/问答时 | 是（默认本地知识库，不发云） |
| Telegram `api.telegram.org` | 推送消息内容 | 通知时 | 是（默认发当前对话渠道，不用 TG） |

**③ 凭证读取（默认最小权限）**：脚本**默认只读** `HOME/.env` 里**你自己填的** key，
且只读 SKILL.md `metadata.openclaw.envVars` 声明过的那些变量名。key 值不会被打印、
写盘或转发，只作为对应服务的 `Authorization` 头发出去。

为省事复用宿主凭证**默认关闭**，而且**按单把凭证授权**：在
`JOBWATCH_ALLOW_HOST_CREDS` 里点名你真正要的那一把——`openrouter`（OpenClaw 存的
OpenRouter key，auth store 只读打开，不读其它 profile）、`telegram_token`
（`openclaw.json` 里的 bot token）、`telegram_chat`（allowFrom 名单），逗号分隔；
给了一把不等于给了另外两把（旧写法 `1` 仍等于全给，向后兼容）。可读的**就这三样**，
没有别的。不点名对应函数直接返回 None 或抛错，skill 绝不碰自己目录之外的密钥。
**开了也不是静默的**：每读一样都会往 stderr 打一行指名读了哪一把。

建议：给这个 skill 单独申请权限最小、可单独吊销的 key，别把主账号总 key 丢进来；
不需要宿主凭证就别设 `JOBWATCH_ALLOW_HOST_CREDS`。

**凭证与端点绑定（v1.2.1 起代码强制，`common.py:credential_for_endpoint`）**：判级和
stage-1 筛都能指向任意 OpenAI 兼容端点，所以「给 A 家用的 key 绝不能发给 B 家」这条
写进了代码：
- `LLM_API_KEY` 是你为 `LLM_BASE_URL` / `judge.base_url` 配的，发给那个端点。
- `OPENROUTER_API_KEY` 和宿主 OpenClaw 的 OpenRouter key **只发给 `openrouter.ai`**。
  把 `LLM_BASE_URL` 指到别处又没配 `LLM_API_KEY`，就**不带任何凭证**发出去，并在
  stderr 说明——不会拿你的 OpenRouter key 顶上。
- `screen.base_url` 覆盖后就是**另一个端点**，不继承 judge 的 key：要凭证配
  `SCREEN_LLM_API_KEY`，指向本地模型则不需要。screen 和 judge 解析到同一个 host 时
  才会复用同一把 key。
- 回环地址 / `.local` 端点永远不会收到云端凭证。

**④ 自主行为（cron）**：注册定时任务(周期抓取+判级+通知)是**写操作**,
只有你在 onboarding 里明确同意后才跑 `setup_cron.py`;上岗后每天会抓取信源、
持续发通知——这个"持续足迹"你要知情。随时可停:关掉对应 cron job。

**⑤ 只读边界**：skill 目录本身只读；不代替你投递；除入库/摘要/告警外不主动发消息。
数据目录之外**只写一个文件**：`~/.openclaw/cron/jobs.json`（且仅在你同意注册定时任务时，
先备份再追加三条 `jobwatch-*`，不动你已有的 job）。**`openclaw.json` 不改**，
其它基础设施配置一律不碰。

---

## 给 Agent：引擎概览

一条可 cron 运行的「岗位抓取 → 画像比对 → 分级行动」流水线，加上投递跟踪与查询。
**零必配依赖**：判级由你（agent）完成——用的就是主人给你配的模型；通知发到你们对话的
渠道；知识库默认本地文件。Firecrawl / Telegram 直连 / 2brain 均为可选增强。

```
① 感知  Greenhouse/Ashby/Lever 官方 API + Google Careers/RSS（Firecrawl 渲染 SPA）
② 推理  去重 + 硬过滤 + [可选]stage-1 标题筛 + 岗位年龄计算 → 你 × 主人画像判级 P1/P2/P3
③ 行动  知识库入库 · P1 即时提醒 · P2 每日摘要 · 投递跟进提醒
```

**数据目录（HOME）**：`<workspace>/jobwatch/`（config.json、profile/、state/、queue/、
runs/、kb_local/）。skill 目录本身保持只读。以下所有命令都从 HOME 目录运行：
`cd <workspace>/jobwatch && python3 <skill目录>/scripts/xxx.py`（首次运行任何脚本会
自动创建 HOME 并落地默认 config.json）。

## First-Run Onboarding（首次使用：面试主人，10 分钟）

一次只问一组，别倒问卷：

1. **目标域**：盯哪些公司？什么方向的岗位？
2. **背景**：几句话介绍（年限/领域/核心技术栈/差异化优势），或直接读主人丢来的简历。
3. **红线**：绝对不看什么岗位？需要 visa sponsorship 吗？地域/远程硬性要求？
4. **级别意向**（必须单独问）：目标级别？IC 还是管理线？现任职级和求职意向经常不一致。
5. **配置选择（必须问，但给快捷选项）**：明确列出三项让主人选，同时告知
   「回复"全部默认"即可跳过」：
   - 通知：默认发到当前对话渠道；要独立低延迟推送可选 Telegram 直连
   - 知识库：默认本地文件（kb_local/）；有 2brain 账号可选 2brain（问答+图谱）
   - JD 抓取：有 Firecrawl 或 Jina key 更干净（Google Careers 信源基本必需），
     没有则用免 key 降级通道
   主人选了非默认项 → 写 config.json 对应字段，并告诉 TA 在 HOME/.env 里要填哪几行
   （参考 skill 目录 env.example），等 TA 填完再继续。

   **凭证与出网，按最小权限办（代码强制，不是文档约定；完整说明见上面的隐私与数据流）：**
   - 只让主人填**当前选项真正需要的那几个** key，别让 TA 把 env.example 一次填满；
     每把建议单独申请、可单独吊销，不要复用主账号总 key。
   - **默认不碰宿主凭证**，要用得在 `JOBWATCH_ALLOW_HOST_CREDS` 里点名，且**只点当前
     功能需要的那一把**，别用 `1` 一次全给。别替主人设这个变量，也别写进 .env。
   - **出网要单独授权**：`JOBWATCH_EGRESS_ALLOW`，或把主人同意的目的地写进
     `HOME/state/egress_consent.json` 的 `granted`。写之前先把「哪个目的地会收到什么」
     念给主人听并拿到明确同意。没授权就抛错是设计如此，**不要用 try/except 绕过去**。

然后动手（主人不写任何文件）：

1. 把 skill 目录的 `profile.template.md` 复制为 `HOME/profile/JOB_PROFILE.md`，按面试
   答案填全五节，复述要点让主人确认。**这个文件是判级质量的全部来源，写具体。**
2. 每家公司跑 `python3 scripts/discover_board.py "<公司名>" [slug猜测]`，把命中的信源
   写进 `HOME/config.json` 的 `sources`。探测不到的用 `gcareers`（Google 系）或 RSS。
3. 按画像生成 `config.json` 的 `prefilter.title_keywords`（20-30 个小写子串，宁宽勿窄）
   和 `exclude_keywords`。
4. **校准（不可跳过）**：跑一轮 `python3 scripts/pipeline.py`，按下方 Work Cycle 完成
   判级，挑 5 个代表性结果（P1/P2/P3 各有）问主人：这些判对了吗？按反馈修画像重验。
   **⚠️ 从跑 pipeline 到给出校准问题是一个连续动作——中途不要结束回合、不要停下来等
   主人说话**（跑完 pipeline 就直接判级、apply、然后带着结果开口）。如果待判清单里
   `jd_text` 全为空（没配抓取 key 的降级态），校准时必须告知主人：本轮是 title-only
   判级，配 Firecrawl/Jina key 后精度会明显提升。
5. **演示推送（必做）**：校准通过后，把本轮判级最高的一个岗位按 P1 消息格式
   （notify_telegram.render_p1_plain 的样式）完整发给主人，开头注明
   「📬 示例：以后 P1 岗位的实时提醒长这样」——让主人上岗前就见过推送的样子。
6. 征得主人同意后注册定时任务：`python3 scripts/setup_cron.py --agent <你的agentId>`，
   提醒主人跑 `openclaw gateway restart`。告诉主人上岗后会发生什么：P1 实时到这个
   对话、每日 9:00 摘要、投递说一声我就记账。

## Work Cycle（cron 唤醒时执行）

1. `python3 scripts/pipeline.py`，读 stdout 的 JSON 摘要。
2. 若 `pending_judgment > 0`：**立即接着做，不要结束回合**。分批处理（一次读 5 行，
   判完追加写入，再读下 5 行——防止大 JD 撑爆上下文）：读 `HOME/queue/pending_judgment.jsonl`（每行
   `{item, jd_text, jd_tool}`，item 含 `posted_at`），逐条对照
   `HOME/profile/JOB_PROFILE.md` 判级，追加写 `HOME/queue/judgments.jsonl`，
   每行严格单行 JSON（无围栏无多余文字）：
   `{"doc_id":"...","match":"kill_shot|comfort_zone|wrong_scene",
     "visa_risk":"low|medium|high|unknown","summary_zh":"≤150字：岗位/要求/匹配点差距",
     "tags":["#3-5个"],"reasons":"1-2句依据"}`
   判级准则：kill_shot=核心能力高度重合+符合级别意向+零红线；comfort_zone=相关但一般，
   或高匹配但红线存疑；wrong_scene=触红线或错位。**挂出超 90 天的岗位视为疑似 ghost
   job，除非匹配极强否则封顶 comfort_zone 并在 reasons 注明。**判不了的跳过（下轮重现），
   不要编造。写完跑 `python3 scripts/apply_judgments.py`（校验/入库/通知入队/标已见）。
3. `python3 scripts/outbox.py list` → 有待发消息就把每条 `text` 通过你和主人的对话渠道
   原样发出，然后 `python3 scripts/outbox.py archive`。
4. 摘要 `errors` 非空：偶发静默；连续 3 次同类失败才向主人发简短告警（环节/诊断/建议）。
5. 一切正常且无待发消息 → 静默结束，不输出任何内容。

digest 唤醒（jobwatch-digest）：跑 `python3 scripts/daily_digest.py` 再执行第 3 步。

## Application Tracking（主人提到投递进展时）

- 「我投了 X」→ `python3 scripts/tracker.py find "<关键词>"` 拿 doc_id →
  `python3 scripts/tracker.py set <doc_id> applied [备注]`
- 「X 约面试了 / 拒了 / 拿 offer 了」→ status 用 interview / rejected / offer
- 状态一览 `tracker.py list [status]`；统计 `tracker.py stats`；
  投递 7 天无更新的会自动出现在每日摘要的跟进提醒里。

## Queries(主人问起时)

- 「本周有什么好岗位」→ `python3 scripts/query.py top 7`（P1/P2 列表），
  想看细节读 `HOME/kb_local/` 里对应文档。
- 「监控跑得怎么样」→ `python3 scripts/query.py stats 7` + 看 `HOME/runs/` 最新日志。
- 深度问题（对比两家公司的要求、某方向技能趋势）→ 检索 `HOME/kb_local/` 的 JD 全文库。

## Config 速查（HOME/config.json）

- `sources[]`: kind ∈ greenhouse|ashby|lever|gcareers|rss
- `judge.mode`: `agent`（默认）| `api`（OpenAI 兼容端点，.env 配 LLM_API_KEY /
  LLM_BASE_URL，更快更稳）
- `notify.mode`: `agent`（默认，outbox 播报）| `telegram`（直连，低延迟；.env 配
  `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID`）
- `kb.backend`: `local`（默认）| `twobrain`（.env 配 TWOBRAIN_*）

> 以上每个非默认项都会打开一条出网通道，因而都要拿到对应的出网许可。各自**发什么、
> 发给谁、用哪把凭证**，上面的**隐私与数据流**一节已经完整写过一次，这里刻意不重复——
> 只留一处描述，才只有一处需要维护为真。

- `prefilter`: 标题关键词硬过滤（stage-0，免费确定性），改完下轮生效
- `screen`: **stage-1 标题筛（默认关闭）**。开 `enabled:true` 后，抓 JD 前先用 LLM
  对 title 批量打分(0-10)，低于 `threshold`(默认4) 直接淘汰——省 Firecrawl 抓取 +
  全量判级，是最省钱的一段（借鉴 AI Digest 三段渐进打分）。`base_url`/`model` 留空
  复用 judge 端点；想**零成本**就把 `base_url` 指向本地 Ollama、`model` 填本地小模型。
  fail-open：筛选故障不误杀岗位。每轮 token 用量记进 summary.screen_usage（成本核算用）。

## 红线

- 不修改 openclaw.json / cron 配置（setup_cron.py 除外且须主人同意）；不直接编辑
  state 文件——行动一律走脚本。
- 不修改 JOB_PROFILE.md，除非主人在校准中明确要求。
- 只读公开信源；不代替主人投递；除 outbox 播报/摘要/告警外不主动发消息。
