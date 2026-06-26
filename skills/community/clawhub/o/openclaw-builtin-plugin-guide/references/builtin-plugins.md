# OpenClaw 内置插件说明

这份文档按 `openclaw-main/extensions` 的内置扩展整理，重点说明每个插件的用途、常见操作和使用注意事项，方便在 Web Panel 里快速判断它是做什么的。

## 使用约定

- 渠道类插件：通常围绕 `channels.<channelId>` 配置，重点是 `enabled`、鉴权凭证、群/私聊策略、Webhook 或长连接参数。
- Provider 类插件：负责接不同模型平台，常见操作是填写 `apiKey`、`baseUrl`、选默认模型，或通过 `openclaw models auth login` 做 OAuth 登录。
- 工具/能力类插件：一般挂在 `plugins.entries.<pluginId>` 下，按需启用，偏向命令、自动化、记忆、语音、诊断等能力。
- 运行时/基础设施类插件：更多是宿主能力适配，不一定需要在面板里频繁手动操作。

## acpx
ACPX 运行时后端，用于把 OpenClaw 接到 acpx 提供的执行环境。

- 作用：提供 ACP runtime backend，偏基础设施能力，不是聊天渠道或模型插件。
- 常见操作：确认宿主环境里 acpx 端可用，再让依赖 ACP runtime 的功能走这个后端。
- 说明：如果你只是接消息渠道或模型，通常不会单独配置它。

## amazon-bedrock
Amazon Bedrock Provider，负责把模型请求转到 AWS Bedrock。

- 作用：给 OpenClaw 增加 Bedrock 模型接入能力。
- 常见操作：配置 AWS 凭证、区域和默认模型，确认网络和 IAM 权限可用。
- 说明：适合已经把模型统一托管在 AWS 体系里的部署。

## anthropic
Anthropic Provider，用来接 Claude 等 Anthropic 模型。

- 作用：把 OpenClaw 的推理请求发送到 Anthropic。
- 常见操作：填写 `apiKey`、选择模型，必要时补 `baseUrl` 或代理。
- 说明：常用于 Claude 系列模型接入。

## bluebubbles
BlueBubbles 渠道插件，用于桥接苹果短信/iMessage 生态。

- 作用：让 OpenClaw 通过 BlueBubbles 转收发 Apple 侧消息。
- 常见操作：配置 BlueBubbles 服务地址、鉴权信息和对应渠道策略。
- 说明：依赖你先搭好 BlueBubbles 服务端。

## brave
Brave 搜索插件，用于给代理增加网页搜索能力。

- 作用：把 Brave Search 作为检索工具接给 OpenClaw。
- 常见操作：配置搜索 API 凭证并在代理工具权限里允许调用。
- 说明：适合需要稳定联网搜索的工作流。

## byteplus
BytePlus Provider，用于接入火山系托管模型服务。

- 作用：让 OpenClaw 使用 BytePlus 提供的模型接口。
- 常见操作：配置访问密钥、区域或网关地址，再选择默认模型。
- 说明：适合已经使用 BytePlus/火山系基础设施的环境。

## chutes
Chutes.ai Provider，用于把模型请求发到 Chutes.ai。

- 作用：扩展一个可选的第三方模型后端。
- 常见操作：填写平台密钥和访问地址，保存后在模型列表里选用。
- 说明：属于 Provider 扩展，操作方式和其他云模型插件类似。

## cloudflare-ai-gateway
Cloudflare AI Gateway Provider，用于把模型请求经由 Cloudflare 的 AI Gateway 转发。

- 作用：统一接入、审计或加速多模型请求。
- 常见操作：配置 Gateway 地址、令牌和目标模型。
- 说明：适合有网关治理、观测或成本审计诉求的环境。

## copilot-proxy
Copilot Proxy Provider，用于把 GitHub Copilot/兼容代理当成模型后端。

- 作用：提供 Copilot Proxy 的模型接入能力。
- 常见操作：按 README 配置代理地址、登录态或令牌，然后在模型设置里选它。
- 说明：更适合已经有现成 Copilot Proxy 环境的场景。

## deepgram
Deepgram 媒体理解 Provider，主要处理语音/音频相关能力。

- 作用：为转录、语音理解等场景提供后端。
- 常见操作：填写 Deepgram API Key，并把需要的语音功能切到这个 Provider。
- 说明：偏多媒体能力，不是普通文本大模型。

## deepseek
DeepSeek Provider，用于接入 DeepSeek 模型。

- 作用：给 OpenClaw 增加 DeepSeek 系列模型能力。
- 常见操作：配置 `apiKey`、接口地址和默认模型。
- 说明：和 OpenAI/Anthropic Provider 属于同类能力。

## device-pair
设备配对插件，用于生成设备配对入口、二维码和临时引导令牌。

- 作用：帮助终端设备或外部客户端与当前 OpenClaw 网关完成配对。
- 常见操作：通过插件命令生成二维码、配对链接或 bootstrap token，再在目标设备上确认。
- 说明：适合首次入网、扫码绑定、设备授权这类场景。

## diagnostics-otel
OpenTelemetry 诊断导出插件，用于把运行诊断、追踪和指标送到观测系统。

- 作用：为网关和插件运行态提供可观测性导出。
- 常见操作：配置 OTEL Collector/Endpoint，再观察链路和报错。
- 说明：更偏运维和排障，普通业务使用不一定会启用。

## diffs
Diff 查看插件，用于展示或处理代码/文本差异。

- 作用：帮助代理输出补丁、对比变化、查看前后差异。
- 常见操作：按 README 启用插件，在需要展示变更的工作流里调用它。
- 说明：适合代码代理、审阅和变更说明场景。

## discord
Discord 渠道插件，用于接入 Discord 机器人消息。

- 作用：负责 Discord 频道、私聊、线程里的收发消息。
- 常见操作：配置 Bot Token、Intent、频道权限和群组策略。
- 说明：属于成熟渠道插件，常和线程、提及、分组策略一起使用。

## duckduckgo
DuckDuckGo 搜索插件，用于联网检索公开网页。

- 作用：给代理提供一个轻量级网页搜索工具。
- 常见操作：启用插件并允许代理使用搜索工具。
- 说明：适合补充公开信息检索，不直接承担模型推理。

## elevenlabs
ElevenLabs 语音插件，用于语音合成或语音相关处理。

- 作用：把 ElevenLabs 的 TTS/语音能力接入 OpenClaw。
- 常见操作：填写 API Key，选 voice 或配合 Talk/Voice 能力使用。
- 说明：适合语音播报、电话语音、语音角色化场景。

## exa
Exa 搜索插件，用于高质量网页和知识检索。

- 作用：给代理增加面向网页/文档的检索能力。
- 常见操作：配置 Exa Key，在代理工具白名单里允许使用。
- 说明：适合研究、搜索、资料收集类任务。

## fal
fal Provider，用于接入 fal 的模型与生成能力。

- 作用：扩展一个面向 fal 平台的模型后端。
- 常见操作：填写平台密钥和所需模型名。
- 说明：常见于多模态或生成类任务。

## feishu
飞书/Lark 渠道插件，用于接入飞书机器人消息。

- 作用：收发飞书私聊、群聊消息，并支持账号、多群组策略。
- 常见操作：配置 `appId`、`appSecret`、`encryptKey`、`verificationToken`，设置 `dmPolicy`、`groupPolicy`、`groups`。
- 说明：通常还会和群白名单、提及要求、Webhook/长连接模式一起配置。

## firecrawl
Firecrawl 插件，用于抓取网页正文、清洗页面内容。

- 作用：把网页抓取和内容提炼能力接给代理。
- 常见操作：填写 Firecrawl Key，在工具权限里允许调用。
- 说明：适合网页抽取、抓取正文、批量站点读取场景。

## github-copilot
GitHub Copilot Provider，用于把 Copilot 模型能力接入 OpenClaw。

- 作用：让代理通过 GitHub Copilot 的模型通道进行推理。
- 常见操作：完成登录态或访问配置，然后把默认模型切过去。
- 说明：适合已有 GitHub Copilot 订阅或企业接入的环境。

## google
Google 插件，主要用于接入 Google 侧能力或模型相关能力。

- 作用：提供 Google 相关服务集成入口。
- 常见操作：配置 API Key/OAuth 资料，并在代理或模型设置里启用。
- 说明：具体能力会随接入面不同而变化，常见是模型或工具扩展。

## googlechat
Google Chat 渠道插件，用于接入 Google Chat 机器人消息。

- 作用：收发 Google Chat 的房间和会话消息。
- 常见操作：配置服务账号、Webhook 或应用鉴权参数。
- 说明：适合企业 Google Workspace 协作场景。

## groq
Groq 媒体理解 Provider，用于接入 Groq 平台的高速模型/多媒体能力。

- 作用：把 OpenClaw 请求转发到 Groq。
- 常见操作：填写 API Key、选模型，并验证速率限制和返回格式。
- 说明：在低延迟推理场景比较常见。

## huggingface
Hugging Face Provider，用于接入 Hugging Face 的推理服务。

- 作用：让 OpenClaw 直接使用 Hugging Face 托管模型。
- 常见操作：填写 Token、推理地址和模型名。
- 说明：适合实验性模型或社区模型较多的场景。

## imessage
iMessage 渠道插件，用于接入 iMessage 生态消息。

- 作用：让 OpenClaw 处理苹果消息通道。
- 常见操作：配合外部桥接服务或本机消息桥，完成账号和路由配置。
- 说明：通常不是纯云侧配置，依赖本地桥接环境。

## irc
IRC 渠道插件，用于接入 IRC 频道和私聊。

- 作用：让代理在传统 IRC 网络中收发消息。
- 常见操作：配置服务器、昵称、频道、鉴权和重连策略。
- 说明：更适合老牌社区或内部 IRC 网络。

## kilocode
Kilo Gateway Provider，用于接入 Kilo 相关模型/网关能力。

- 作用：把 Kilo 网关作为模型后端使用。
- 常见操作：配置网关地址和鉴权信息，再选默认模型。
- 说明：属于 Provider 适配层。

## kimi-coding
Kimi Provider，用于接入 Kimi/Kimi Coding 模型能力。

- 作用：给 OpenClaw 增加月之暗面/Kimi 模型支持。
- 常见操作：填写平台密钥、模型名，必要时配代理。
- 说明：适合中文和代码场景较多的部署。

## line
LINE 渠道插件，用于接入 LINE Bot 消息。

- 作用：处理 LINE 私聊、群组或会话消息。
- 常见操作：配置 Channel Access Token、Secret、Webhook 和群策略。
- 说明：适合东亚地区常用的 LINE 场景。

## llm-task
JSON-only LLM 任务插件，用于把某些任务约束成结构化 LLM 调用。

- 作用：将任务输出限制为可解析的 JSON/结构化结果。
- 常见操作：按 README 启用后，在需要严格结构输出的流程中调用。
- 说明：适合自动化编排、提取和后处理链路。

## lobster
Lobster 工作流插件，提供强类型流水线和可恢复执行能力。

- 作用：把复杂任务拆成可恢复、可追踪的工作流步骤。
- 常见操作：按 README 启用，在复杂自动化或多阶段任务里接入。
- 说明：更像编排工具，不是普通聊天渠道。

## matrix
Matrix 渠道插件，用于接入 Matrix 房间和私聊。

- 作用：收发 Matrix 生态消息。
- 常见操作：配置 homeserver、访问令牌、房间权限和策略。
- 说明：适合开源协作或自建 IM 环境。

## mattermost
Mattermost 渠道插件，用于接入 Mattermost 消息。

- 作用：负责 Mattermost 中的机器人消息交互。
- 常见操作：配置 Bot Token、服务器地址、团队/频道权限。
- 说明：常见于企业内部自建协作系统。

## memory-core
核心记忆插件，为 OpenClaw 提供统一的记忆搜索接口。

- 作用：提供记忆能力抽象层，让代理可以检索长期记忆。
- 常见操作：启用插件，并搭配具体存储后端如 `memory-lancedb` 使用。
- 说明：它是记忆能力的核心，不等于真正的存储引擎。

## memory-lancedb
LanceDB 记忆后端插件，用于存储和检索长期记忆。

- 作用：把长期记忆落到 LanceDB，并支持向量检索。
- 常见操作：配置数据库路径、嵌入设置或索引策略。
- 说明：通常与 `memory-core` 配合使用。

## microsoft
Microsoft 语音插件，用于接入微软语音能力。

- 作用：提供 Azure/Microsoft 语音识别或语音合成能力。
- 常见操作：配置密钥、区域和 voice 参数。
- 说明：适合企业语音、TTS、ASR 场景。

## minimax
MiniMax Provider/OAuth 插件，用于接入 MiniMax 模型。

- 作用：提供 MiniMax 模型调用和鉴权能力。
- 常见操作：按 README 或平台文档完成 OAuth/API Key 配置，再选模型。
- 说明：既能承担 Provider 角色，也涉及授权流程。

## mistral
Mistral Provider，用于接入 Mistral 模型。

- 作用：把推理请求发送到 Mistral 平台。
- 常见操作：填写 API Key、模型名和接口地址。
- 说明：属于标准 Provider 接入。

## modelstudio
Model Studio Provider，用于接入 Model Studio 类托管模型平台。

- 作用：扩展一个 Model Studio 模型来源。
- 常见操作：配置平台地址、鉴权和模型。
- 说明：更偏平台适配层。

## moonshot
Moonshot Provider，用于接入 Moonshot/Kimi 相关模型服务。

- 作用：提供 Moonshot 平台模型调用能力。
- 常见操作：填写 API Key、Base URL 和模型。
- 说明：常和中文对话/代码模型一起使用。

## msteams
Microsoft Teams 渠道插件，用于接入 Teams 机器人消息。

- 作用：收发 Teams 会话、频道和线程消息。
- 常见操作：配置 App/Bot 鉴权、回调地址和会话策略。
- 说明：适合 Microsoft 365 企业协作环境。

## nextcloud-talk
Nextcloud Talk 渠道插件，用于接入 Nextcloud Talk 消息。

- 作用：让 OpenClaw 在 Nextcloud Talk 中收发消息。
- 常见操作：配置服务器地址、机器人凭证和房间访问。
- 说明：适合自建协作平台。

## nostr
Nostr 渠道插件，用于处理 NIP-04 加密私信等 Nostr 生态消息。

- 作用：让代理进入去中心化 Nostr 网络收发消息。
- 常见操作：按 README 配置密钥、relay 和收发策略。
- 说明：更偏加密/去中心化社交场景。

## nvidia
NVIDIA Provider，用于接入 NVIDIA 提供的模型服务。

- 作用：让 OpenClaw 使用 NVIDIA 模型推理接口。
- 常见操作：填写访问密钥、服务地址和模型标识。
- 说明：常见于企业 GPU 平台或 NVIDIA API 环境。

## ollama
Ollama Provider，用于接本地或局域网内的 Ollama 模型服务。

- 作用：把 OpenClaw 的模型请求发到 Ollama。
- 常见操作：按 README 配置 Ollama 地址，确认模型已在宿主机拉取好。
- 说明：适合本地推理和离线部署。

## openai
OpenAI Provider，用于接入 OpenAI API 或相关登录通道。

- 作用：把模型请求转到 OpenAI，并承接常见 GPT 模型。
- 常见操作：填写 `OPENAI_API_KEY` 或走 `openclaw models auth login`，再把默认模型切到 `openai/...`。
- 说明：是最常见的 Provider 之一，适合直接接 GPT 系列模型。

## openclaw-web-panel
Web Panel 启动插件，用于拉起独立的 OpenClaw 管理面板。

- 作用：给 OpenClaw 提供 Web 管理后台入口。
- 常见操作：安装或启用后访问面板服务，进行环境、插件、渠道和配置管理。
- 说明：它更像管理入口插件，不直接参与消息收发。

## opencode
OpenCode Zen Provider，用于接入 OpenCode Zen 模型服务。

- 作用：扩展一个名为 OpenCode Zen 的模型后端。
- 常见操作：配置 API 地址、鉴权和模型名。
- 说明：属于 Provider 适配层。

## opencode-go
OpenCode Go Provider，用于接入 OpenCode Go 模型服务。

- 作用：提供另一个 OpenCode 家族模型后端。
- 常见操作：配置平台地址、凭证和模型。
- 说明：和 `opencode` 类似，面向不同后端实现。

## open-prose
OpenProse 技能包插件，提供 `/prose` 命令和 OpenProse VM 语义。

- 作用：让代理具备写作流程、`.prose` 程序和多代理编排能力。
- 常见操作：按 README 在 `plugins.entries.open-prose.enabled` 里启用，然后重启 Gateway。
- 说明：默认内置但关闭，适合写作、长文润色和编排场景。

## openrouter
OpenRouter Provider，用于接入 OpenRouter 聚合模型平台。

- 作用：通过 OpenRouter 统一访问多家模型。
- 常见操作：填写 OpenRouter Key、Base URL 和目标模型。
- 说明：适合希望通过一个平台调度多模型的部署。

## openshell
OpenShell 沙箱后端，用于承接 OpenClaw 的沙箱执行能力。

- 作用：为工具执行、命令运行或隔离环境提供宿主能力。
- 常见操作：确认宿主环境能提供对应沙箱，再把相关任务绑定到它。
- 说明：属于基础执行层，不是普通业务插件。

## perplexity
Perplexity 插件，用于接入 Perplexity 的搜索/问答能力。

- 作用：给代理增加联网检索和答案增强能力。
- 常见操作：配置 API Key，并在允许联网查询的代理上启用。
- 说明：适合研究、问答和资料汇总类任务。

## phone-control
手机控制插件，用于临时放开相机、录屏、写入类手机指令权限。

- 作用：通过“arming”机制在一段时间内允许摄像头、屏幕录制、短信/提醒事项等操作。
- 常见操作：按插件命令选择 `camera`、`screen`、`writes` 或 `all` 分组，设置有效时长后执行手机相关动作。
- 说明：属于高权限能力，适合在明确授权后短时开启。

## qianfan
千帆 Provider，用于接入百度千帆模型服务。

- 作用：给 OpenClaw 增加百度系模型后端。
- 常见操作：配置 Access Key、Secret 或平台令牌，选默认模型。
- 说明：适合百度云/千帆生态用户。

## qwen-portal-auth
Qwen OAuth 插件，用于通过设备码流程登录 Qwen 免费层或门户授权。

- 作用：给 Qwen 模型提供 OAuth 登录能力。
- 常见操作：按 README 先启用插件，再运行 `openclaw models auth login --provider qwen-portal --set-default`。
- 说明：默认内置但关闭，适合走 Qwen 门户授权而不是手填 API Key 的场景。

## sglang
SGLang Provider，用于接入 SGLang 推理服务。

- 作用：把 OpenClaw 模型请求发到 SGLang 服务端。
- 常见操作：按 README 配置 SGLang 地址、模型和并发参数。
- 说明：适合自建高性能推理服务。

## signal
Signal 渠道插件，用于接入 Signal 消息。

- 作用：收发 Signal 私聊或群消息。
- 常见操作：配置桥接服务、号码、鉴权和路由策略。
- 说明：通常依赖外部 Signal bridge。

## slack
Slack 渠道插件，用于接入 Slack 频道、线程和私聊。

- 作用：负责 Slack 里的消息接收、发送和线程上下文处理。
- 常见操作：配置 Bot Token、Signing Secret、Socket/Webhook 模式、群策略和提及要求。
- 说明：和线程、群白名单、工作区路由经常一起用。

## synology-chat
Synology Chat 渠道插件，用于接入群晖聊天系统。

- 作用：让代理进入 Synology Chat 会话中工作。
- 常见操作：配置服务器地址、Bot Token 和目标会话权限。
- 说明：适合群晖/私有化协作环境。

## synthetic
Synthetic Provider，用于提供合成/测试型模型后端。

- 作用：在没有真实模型时提供模拟或合成结果。
- 常见操作：在测试、演示或离线验证时将默认模型切换到它。
- 说明：更适合联调和测试，不适合生产推理质量要求高的场景。

## talk-voice
Talk Voice 管理插件，提供 `/voice` 或 `/talkvoice` 命令来查看和切换语音。

- 作用：管理 Talk 语音配置、列出可用 voice、切换当前 voiceId。
- 常见操作：在支持的渠道里执行语音管理命令，查看当前语音状态或选择指定 voice。
- 说明：它本身不做语音合成，而是作为 Talk 语音能力的命令助手。

## tavily
Tavily 搜索插件，用于联网搜索和网页研究。

- 作用：给代理增加 Tavily 检索能力。
- 常见操作：填写 Tavily Key，并在搜索型代理里允许使用。
- 说明：适合研究型工作流。

## telegram
Telegram 渠道插件，用于接入 Telegram Bot 私聊、群聊和线程消息。

- 作用：负责 Telegram 机器人的消息收发、群组策略和账号路由。
- 常见操作：配置 `botToken`、`dmPolicy`、`groupPolicy`、`groups`，必要时加 `proxy`、Webhook 或多账号配置。
- 说明：如果消息进不来，常见原因是配对、白名单、群权限或 chatId，而不一定是代理本身。

## thread-ownership
Slack 线程归属插件，用于多代理场景下避免多个代理同时回复同一个线程。

- 作用：在消息发送前向 ownership forwarder 申请线程所有权，冲突时自动取消发送。
- 常见操作：配置 `forwarderUrl`、可选的 `abTestChannels`，并确保 Slack forwarder 服务可达。
- 说明：适合多代理共用一个 Slack 工作区或频道的部署。

## tlon
Tlon/Urbit 渠道插件，用于接入 Tlon 或 Urbit 相关消息能力。

- 作用：让 OpenClaw 处理 Tlon/Urbit 通道消息。
- 常见操作：按 README 配置接入参数、路由和身份信息。
- 说明：适合特定生态场景，不是通用 IM 插件。

## together
Together Provider，用于接入 Together AI 模型。

- 作用：让代理通过 Together 平台访问模型。
- 常见操作：填写 API Key、目标模型和可选 Base URL。
- 说明：适合想快速试多家开源模型托管服务的场景。

## twitch
Twitch 渠道插件，用于接入 Twitch 聊天频道。

- 作用：让代理在 Twitch 直播聊天中收发消息。
- 常见操作：按 README 配置机器人账号、OAuth Token、频道名和权限。
- 说明：适合直播互动、频道机器人场景。

## venice
Venice Provider，用于接入 Venice 模型平台。

- 作用：提供一个 Venice 模型后端。
- 常见操作：配置 API Key、模型和接口地址。
- 说明：属于标准 Provider 扩展。

## vercel-ai-gateway
Vercel AI Gateway Provider，用于经由 Vercel AI Gateway 调用模型。

- 作用：统一转发模型请求，并获得网关治理能力。
- 常见操作：配置 Gateway URL、Token 和目标 Provider/Model。
- 说明：适合已有 Vercel AI Gateway 基础设施的环境。

## vllm
vLLM Provider，用于接入自建 vLLM 推理服务。

- 作用：把 OpenClaw 请求发到 vLLM 服务端。
- 常见操作：按 README 配置 `baseUrl`、模型名和并发参数，确认服务本身可用。
- 说明：适合自建 GPU 推理环境。

## voice-call
语音通话插件，用于把 OpenClaw 接到电话呼叫能力。

- 作用：支持 Twilio、Telnyx、Plivo、Mock 等呼叫提供商，处理来电、外呼和媒体流。
- 常见操作：按 README 在 `plugins.entries.voice-call.config` 下配置 `provider`、号码、Webhook 等参数。
- 说明：适合电话机器人、语音客服、呼入呼出自动化场景。

## volcengine
Volcengine Provider，用于接入火山引擎模型服务。

- 作用：把模型请求发送到火山引擎。
- 常见操作：填写访问密钥、Region、Base URL 和模型。
- 说明：适合国内云环境或豆包/火山系模型接入。

## whatsapp
WhatsApp 渠道插件，用于接入 WhatsApp 消息。

- 作用：让代理处理 WhatsApp 私聊和群消息。
- 常见操作：配置桥接服务、Webhook、令牌和消息策略。
- 说明：通常依赖 Meta 官方通道或第三方桥接。

## xai
xAI 插件，用于接入 xAI 相关模型或能力。

- 作用：为 OpenClaw 增加 xAI 侧模型通道。
- 常见操作：配置 API Key、Base URL 和模型标识。
- 说明：如果主要使用 Grok 等模型，这类插件会比较常见。

## xiaomi
Xiaomi Provider，用于接入小米模型或平台能力。

- 作用：给 OpenClaw 增加小米侧模型后端。
- 常见操作：配置访问地址、令牌和模型。
- 说明：属于平台适配型 Provider。

## zai
Z.AI Provider，用于接入 Z.AI 模型服务。

- 作用：让 OpenClaw 使用 Z.AI 相关模型能力。
- 常见操作：填写 API Key、Base URL 和默认模型。
- 说明：和其他 Provider 的接法一致。

## zalo
Zalo Bot 渠道插件，用于接入 Zalo 官方 Bot API。

- 作用：负责 Zalo Bot 的消息收发、Webhook 和策略控制。
- 常见操作：按 README 配置 `channels.zalo` 下的 `botToken`、`dmPolicy`、`proxy`、Webhook 等参数。
- 说明：适合越南市场或 Zalo Bot 场景。

## zalouser
Zalo 个人号插件，用于通过原生 `zca-js` 桥接接入 Zalo 个人账号。

- 作用：让 OpenClaw 不通过 Bot API，而是通过个人号桥接来收发消息。
- 常见操作：按 README 配置个人号登录态、桥接参数和路由。
- 说明：能力更强，但也更依赖本地运行环境与账号状态。
