# JobWatch

把你的 OpenClaw agent 变成求职哨兵：定时盯目标公司 careers 页 → LLM 对照你的个人画像
判级 → 强匹配实时提醒 / 次要的每日摘要 / 全部沉淀知识库，外加投递状态跟踪和随口查询。

> ⚠️ **装之前先读这段（隐私）。** 这个 skill 要收集你的**简历内容、visa/签证需求、
> 级别意向、绝不看的岗位类型**这类敏感信息，并且**会向第三方发送数据**：按配置，你监控的
> **页面 URL** 会发给 Firecrawl / Jina，**JD 全文和你画像文件的全文**会发给你配的
> LLM 端点，**归档 JD 和你的提问**会发给 2brain，**通知正文**会发给 Telegram。它还会
> **注册定时任务**、在你显式开启后**读取宿主 OpenClaw 的凭证**。
>
> 默认配置是最保守的一档：判级交给你自己的 agent、通知发当前对话、知识库写本地文件——
> 这一档下没有任何画像内容通过本 skill 出网。所有出网通道**默认全部关闭**，代码里
> 硬性拦截（`require_egress_consent()`，没授权直接报错，不是只写在文档里）。
> 逐条清单见下面的**隐私**小节和 SKILL.md 的 *Privacy & Data Flow*。

## 安装

唯一前提：装好的 OpenClaw（gateway 运行中）。

```bash
openclaw skills install jobwatch
```

## 上手：一句话 + 一场面试

对你的 agent 说一句**明确的祈使句**：**「帮我设置求职监控」** / **「开启求职监控」**
（或 "set up jobwatch for me" / "start job monitoring for my search"）。

> 只有这类明确的开通请求才会启动它。随口聊到工作、求职、careers 页面**不会**触发——
> 因为一旦入职就会开始采集你的简历/visa/红线这类敏感信息并注册定时任务，所以门槛
> 故意设高。它也会在问第一个问题之前，先告诉你要收集什么、会发给谁，等你明确同意。

它会面试你（约 10 分钟，一次一组问题）：

| 面试环节 | 它会问什么 | 你怎么答 |
|---|---|---|
| 1. 目标域 | 盯哪些公司、什么方向 | 报公司名即可，招聘系统它自己探测 |
| 2. 背景 | 年限/领域/技术栈/差异化 | 口述几句，或直接丢简历文件 |
| 3. 红线 | visa？地域？绝不看的岗位类型？ | 想清楚，这是一票否决项 |
| 4. 级别意向 | 目标级别？IC 还是管理线？ | 单独问是因为现任职级≠求职意向 |
| 5. 配置 | 通知渠道 / 知识库 / JD 抓取 | 回答「全部默认」即可零配置 |

然后它自己干活：生成你的求职画像（`<workspace>/jobwatch/profile/JOB_PROFILE.md`，
**文件本身只写在你机器上，从不整份上传**；但开了 `judge.mode=api` 或 stage-1 筛之后，
你画像文件的**全文**会随每条 JD 一起发给你配的 LLM 端点——默认配置不走这条，
详见下面隐私一节）→ 探测信源写配置（会把你报的公司名猜成 slug 发给 Greenhouse /
Ashby / Lever 公开 API 探测，只发 slug）→ 抓一轮真实岗位试判 → **拿约 5 个判级结果和你
校准**（判错直接说，它改画像重判）→ 发一条示例 P1 提醒给你看效果 → 征得你同意后注册
定时任务（工作日每 15 分钟 + 周末每小时 + 每日 9:00 摘要）。

## 日常使用

上岗后你什么都不用做。P1 岗位会实时出现在你们的对话里，每天 9:00 一条摘要。想互动时：

- 「Databricks 那个 AI Engineer 我投了」→ 它记账；投递 7 天没动静，摘要里自动提醒跟进
- 「本周有什么好岗位？」「监控跑得怎么样？」→ 直接答
- 「以后 XX 类岗位算 P1」→ 它改画像，下轮生效

## 配置与增强（全部可选）

默认零配置：判级用你 agent 自己的模型，通知发对话渠道，知识库写本地文件。想升级：

| 增强 | 作用 | 怎么开 |
|---|---|---|
| Firecrawl / Jina key | JD 全文抓取更干净；监控 Google 系公司基本必需 | `<workspace>/jobwatch/.env` 填 `FIRECRAWL_API_KEY` 或 `JINA_API_KEY` |
| API 判级 | 更快更稳、省 agent 会话 | config `judge.mode: api` + `.env` 填 `LLM_API_KEY`（任意 OpenAI 兼容端点，非 OpenRouter 加 `LLM_BASE_URL`） |
| Telegram 直连 | 独立低延迟推送 | config `notify.mode: telegram` + `.env` 填 `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID`；想复用 OpenClaw 已有的 bot 配置要**另外**在 `JOBWATCH_ALLOW_HOST_CREDS` 里点名 `telegram_token`（默认关；按单把凭证授权，读的时候会在 stderr 报一行） |
| 2brain 知识库 | 云端 RAG：图谱 + 溯源问答 | config `kb.backend: twobrain` + `.env` 填 `TWOBRAIN_*` |

> 开上面任何一项，都还要**再授权一次出网**：`JOBWATCH_EGRESS_ALLOW`（`llm` / `firecrawl` /
> `jina` / `twobrain` / `telegram`，逗号分隔或 `all`），或让入职流程写
> `state/egress_consent.json`。没授权就直接报错，不会偷偷发。建议给本 skill 单独申请
> 一把权限最小的 key，别复用你主账号的。

信源支持：Greenhouse / Ashby / Lever（官方 API）、Google Careers（Firecrawl 渲染）、
任意 RSS。加公司 = 让 agent 跑一次探测，加一行配置。

## 常见问题

- **重来一次 onboarding**：删掉 `<workspace>/jobwatch/` 目录，并给 agent 开个新会话（频道里发 `/new`，否则它的对话记忆还记得上次入职）。skill 本体不用动。
- **判级不准**：直接告诉 agent 哪里判错了，或自己改 `profile/JOB_PROFILE.md`——它是
  判级的唯一依据，写得越具体越准。
- **卸载**：`openclaw cron list` 删掉 3 个 jobwatch-* 任务，删除 skill 目录和
  `<workspace>/jobwatch/`。
- **隐私**：**这个 skill 会向第三方发送数据，请按需关闭。** 画像、密钥和运行状态本身
  只写在本地 HOME 目录，但下面这些是真的会出网的：
  - **LLM 端点**（OpenRouter 或你自己配的 OpenAI 兼容地址）：判级时会收到**完整 JD 文本
    和你 `JOB_PROFILE.md` 的全文**（简历要点、visa 需求、级别意向、红线；stage-1 筛
    发前 ~1200 字）。`judge.mode=agent`（默认）由宿主 agent 判，不走这条；
    `judge.mode=api` 才走。指到本地 Ollama 即可完全不出网。
  - **Firecrawl / Jina**：抓 JD 时收到你监控的**页面 URL**。不填 key 就不走。
  - **2brain 知识库**：`kb.backend=twobrain` 时收到**归档的 JD 文档和你的提问**。默认是
    `local`，不出网。
  - **Telegram**：`notify.mode=telegram` 时收到**通知正文**。默认走当前对话频道。
  - **ATS 公开 API**（Greenhouse / Ashby / Lever）：收到你配置的公司 slug（公开信息）。

  完整清单见 SKILL.md 的 *Privacy & Data Flow*。抓取只读公开信源并遵守速率限制。

## 工作原理（一图流）

```
cron 唤醒 agent
  ① 感知  官方 ATS API 抓列表 · Firecrawl 抓 SPA 详情页 JD（脚本，确定性）
  ② 推理  去重/硬过滤/岗位年龄（脚本）→ agent × 你的画像判级（LLM，可校准）
  ③ 行动  入库 + P1 实时 + P2 摘要 + 投递跟进（脚本，格式校验兜底）
```

脚本管确定性，agent 管判断，schema 校验兜底——判级失败降级进摘要，绝不静默丢岗位。
