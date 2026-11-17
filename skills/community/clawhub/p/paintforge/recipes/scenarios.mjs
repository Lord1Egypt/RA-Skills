const RAW_RECIPES = [
  {
    id: 'system-overview', type: 'architecture', proof: 'web-app',
    presentation: { preset: 'classic', motion: 'static', views: 'optional' },
    start: {
      en: { descriptionPrompt: 'Use PaintForge to turn this plain-language system description into a high-level architecture diagram: [describe the users, core components, primary path, external dependencies, and boundaries]. No repository is required. Ask only for missing facts that would materially change the diagram, mark any remaining unknowns instead of inventing them, and keep one obvious primary path across 8–12 core components.' },
      zh: { descriptionPrompt: '用 PaintForge 把下面这段自然语言系统描述画成高层架构图：[在这里描述用户、核心组件、主要路径、外部依赖和边界]。不需要代码库。只追问会实质影响图的缺失信息，其余不确定内容要标明而不是编造；保留 8–12 个核心组件和一条一眼可见的主路径。' },
    },
    signals: [['system overview', 12], ['architecture', 10], ['components', 6], ['services', 4], ['repository', 5], ['trust boundary', 8], ['架构', 10], ['系统总览', 12], ['组件', 6], ['服务', 4], ['仓库', 5], ['信任边界', 8]],
    en: {
      title: 'System overview', question: 'What exists, who owns it, and how is it connected?',
      summary: 'A bounded map of core components, external dependencies, primary paths, and trust boundaries.',
      useWhen: 'Onboarding, design reviews, repository orientation, or explaining a service landscape.',
      avoidWhen: 'The audience needs exact call order, state transitions, or row-level data lineage.',
      include: ['8–12 core components', 'one primary path', 'external dependencies', 'trust boundaries'],
      prompt: 'Analyze this repository, then use PaintForge to create a high-level architecture diagram. Show 8–12 core runtime components, one primary request or data path, external dependencies, ownership or trust boundaries, and put supporting detail in cards instead of adding more edges.',
    },
    zh: {
      title: '系统总览', question: '系统里有什么、归谁负责、彼此如何连接？',
      summary: '用一张有边界的图展示核心组件、外部依赖、主路径和信任边界。',
      useWhen: '适合新人上手、方案评审、仓库梳理和服务全景说明。',
      avoidWhen: '如果重点是精确调用顺序、状态流转或字段级血缘，请换其他配方。',
      include: ['8–12 个核心组件', '一条主路径', '外部依赖', '归属或信任边界'],
      prompt: '分析这个仓库，然后用 PaintForge 生成高层系统架构图。展示 8–12 个核心运行时组件、一条主要请求或数据路径、外部依赖、归属或信任边界；支持性细节放进卡片，不要继续堆连线。',
    },
  },
  {
    id: 'deployment-ownership', type: 'architecture', proof: 'deployment-ownership',
    presentation: { preset: 'blueprint', motion: 'trace', views: 'recommended' },
    signals: [['deployment topology', 14], ['region', 7], ['vpc', 9], ['cluster', 6], ['availability zone', 8], ['ownership', 7], ['cloud deployment', 12], ['部署拓扑', 14], ['区域', 6], ['集群', 6], ['可用区', 8], ['资源归属', 9], ['跨区', 8]],
    en: {
      title: 'Deployment ownership', question: 'Where does each workload run, and what crosses a boundary?',
      summary: 'A deployment-focused map of regions, networks, clusters, workloads, stores, and cross-boundary mechanisms.',
      useWhen: 'Cloud reviews, production readiness, multi-region planning, or infrastructure ownership handoffs.',
      avoidWhen: 'Deployment facts are unknown or the real question is application behavior rather than placement.',
      include: ['regions and networks', 'workload ownership', 'stateful services', 'named boundary crossings'],
      prompt: 'Use PaintForge to draw the production deployment topology. Group resources by region, network, cluster, and owner; show workloads and stateful services; label every cross-boundary mechanism. Do not invent deployment facts—mark unknown areas explicitly. If the user wants a fail-closed deployment review, ask before setting meta.engineering_profile to deployment-ownership; otherwise leave the engineering profile unset.',
    },
    zh: {
      title: '部署与归属', question: '每个工作负载运行在哪里，哪些连接跨越了边界？',
      summary: '围绕 Region、网络、集群、工作负载、存储和跨边界机制组织部署图。',
      useWhen: '适合云上评审、生产就绪、多区域规划和基础设施交接。',
      avoidWhen: '部署事实不清楚，或真正问题是应用行为而不是资源位置时不要使用。',
      include: ['区域与网络', '工作负载归属', '有状态服务', '明确的跨边界机制'],
      prompt: '用 PaintForge 绘制生产部署拓扑。按区域、网络、集群和负责人分组，展示工作负载与有状态服务，并标注每一种跨边界机制。不要编造部署事实，不确定的区域要明确标出。如果用户需要失败即阻断的部署评审，先征得确认，再把 meta.engineering_profile 设为 deployment-ownership；否则不要启用工程画像。',
    },
  },
  {
    id: 'agent-tool-call', type: 'workflow', proof: 'agent-tool-call',
    presentation: { preset: 'signal-flow', motion: 'trace', views: 'recommended' },
    start: {
      en: { descriptionPrompt: 'Use PaintForge workflow mode to turn this description into a diagram: [paste the actors, main steps, decisions, approvals, and exception paths]. Use lanes for distinct owners, keep one unmistakable happy path, and mark missing ownership or unresolved branches instead of inventing them.' },
      zh: { descriptionPrompt: '用 PaintForge 工作流模式把下面的描述画成图：[粘贴参与者、主要步骤、决策、审批和异常路径]。不同负责方使用独立泳道，保留一条明确的成功主路径，缺失的负责人或未定分支要标明而不是编造。' },
    },
    signals: [['agent tool call', 16], ['tool call', 12], ['approval gate', 10], ['human in the loop', 9], ['mcp', 7], ['planner', 6], ['agent loop', 10], ['智能体工具调用', 16], ['工具调用', 12], ['审批门', 10], ['人在回路', 9], ['规划器', 6], ['智能体循环', 10]],
    en: {
      title: 'Agent tool-call loop', question: 'How does an agent plan, get permission, act, recover, and report?',
      summary: 'A lane-based agent loop with policy gates, tool execution, exception recovery, evidence, and final response.',
      useWhen: 'Explaining agent runtimes, MCP/tool orchestration, approvals, retries, or observability.',
      avoidWhen: 'The goal is only to show static agent components or exact API message timing.',
      include: ['request and planning', 'policy or approval gate', 'tool execution', 'exception and evidence paths'],
      prompt: 'Use PaintForge workflow mode to explain this agent tool-call loop. Separate user surface, agent runtime, policy boundary, exception handling, tool execution, and observability into lanes. Make the successful path primary and show approval, retry, blocked, and evidence paths explicitly.',
    },
    zh: {
      title: '智能体工具调用', question: '智能体如何规划、获批、执行、恢复并汇报？',
      summary: '用泳道表达策略门、工具执行、异常恢复、证据和最终回复。',
      useWhen: '适合解释 Agent Runtime、MCP/工具编排、审批、重试和可观测性。',
      avoidWhen: '如果只想看静态组件，或重点是精确 API 消息时序，请换其他配方。',
      include: ['请求与规划', '策略或审批门', '工具执行', '异常与证据路径'],
      prompt: '用 PaintForge 工作流模式解释这段智能体工具调用。把用户界面、Agent Runtime、策略边界、异常处理、工具执行和可观测性分成泳道；突出成功主路径，并明确展示审批、重试、阻塞和证据路径。',
    },
  },
  {
    id: 'delivery-workflow', type: 'workflow', proof: 'delivery-workflow',
    presentation: { preset: 'classic', motion: 'trace', views: 'optional' },
    signals: [['ci/cd', 14], ['release workflow', 14], ['deployment pipeline', 11], ['pull request', 7], ['staging', 7], ['rollback', 8], ['发布流程', 14], ['流水线', 9], ['上线', 7], ['预发', 7], ['回滚', 8], ['审批发布', 10]],
    en: {
      title: 'Delivery workflow', question: 'How does a change move safely from commit to production?',
      summary: 'A delivery flow with build, checks, environments, approvals, smoke tests, rollback, and ownership lanes.',
      useWhen: 'CI/CD design, release reviews, deployment governance, or onboarding developers to delivery.',
      avoidWhen: 'The question is where infrastructure runs or what states a deployment object can occupy.',
      include: ['trigger and build', 'blocking checks', 'approval and environments', 'rollback and verification'],
      prompt: 'Use PaintForge workflow mode to draw this delivery process from commit to production. Separate developer, CI, approval, environment, and exception lanes; mark blocking checks, smoke tests, ownership, and the rollback path. Keep one unmistakable happy path.',
    },
    zh: {
      title: '研发交付流程', question: '一次变更如何安全地从提交走到生产？',
      summary: '展示构建、检查、环境、审批、冒烟、回滚和负责人泳道。',
      useWhen: '适合 CI/CD 设计、发布评审、部署治理和研发新人上手。',
      avoidWhen: '如果重点是基础设施位置或部署对象的状态集合，请换架构图或生命周期图。',
      include: ['触发与构建', '阻断检查', '审批与环境', '回滚与验证'],
      prompt: '用 PaintForge 工作流模式绘制从代码提交到生产发布的流程。拆分开发者、CI、审批、环境和异常泳道；标出阻断检查、冒烟测试、负责人和回滚路径，并保留一条一眼可见的成功主路径。',
    },
  },
  {
    id: 'incident-runbook', type: 'workflow', proof: 'incident-runbook',
    presentation: { preset: 'signal-flow', motion: 'trace', views: 'recommended' },
    signals: [['incident response', 15], ['runbook', 12], ['outage', 9], ['triage', 8], ['mitigation', 8], ['escalation', 7], ['事故处置', 15], ['故障', 9], ['应急预案', 12], ['排障', 9], ['缓解', 7], ['升级响应', 8]],
    en: {
      title: 'Incident runbook', question: 'How do responders detect, triage, mitigate, verify, and escalate?',
      summary: 'An operational workflow that separates signals, responders, mitigation, communications, and recovery proof.',
      useWhen: 'Incident playbooks, on-call handoffs, reliability reviews, and tabletop exercises.',
      avoidWhen: 'The audience needs live metrics or a post-incident component topology instead of response actions.',
      include: ['detection signal', 'triage owner', 'mitigation and rollback', 'verification and communication'],
      prompt: 'Use PaintForge workflow mode to turn this incident runbook into responder lanes. Show detection, triage, mitigation, escalation, communication, rollback, and recovery verification. Separate decision gates from actions and make missing ownership visible.',
    },
    zh: {
      title: '事故处置 Runbook', question: '响应者如何发现、分诊、缓解、验证并升级？',
      summary: '把信号、响应者、缓解动作、沟通和恢复证据拆成可执行流程。',
      useWhen: '适合故障预案、On-call 交接、稳定性评审和桌面演练。',
      avoidWhen: '如果受众需要实时指标仪表盘或事故后的组件拓扑，而不是响应动作，请换其他视图。',
      include: ['发现信号', '分诊负责人', '缓解与回滚', '恢复验证与沟通'],
      prompt: '用 PaintForge 工作流模式把事故处置预案画成响应者泳道。展示发现、分诊、缓解、升级、沟通、回滚和恢复验证；把决策门与操作分开，并让缺失的负责人清晰可见。',
    },
  },
  {
    id: 'api-request', type: 'sequence', proof: 'cache-miss',
    presentation: { preset: 'classic', motion: 'trace', views: 'optional' },
    start: {
      en: { descriptionPrompt: 'Use PaintForge sequence mode to draw this interaction: [paste the participants, calls, returns, fallback, and asynchronous side effects]. Keep message order unambiguous, labels short, and unknown behavior explicit. No repository is required.' },
      zh: { descriptionPrompt: '用 PaintForge 时序模式绘制下面的交互：[粘贴参与者、调用、返回、回退和异步副作用]。确保消息顺序无歧义、标签简短，并明确标注未知行为。不需要代码库。' },
    },
    signals: [['api request', 14], ['request response', 12], ['call chain', 11], ['cache miss', 13], ['jwt', 8], ['who calls whom', 12], ['api 请求', 14], ['请求响应', 12], ['调用链', 11], ['缓存未命中', 13], ['谁调用谁', 12], ['鉴权链路', 9]],
    en: {
      title: 'API request chain', question: 'Who calls whom, in what order, and what returns?',
      summary: 'A time-ordered request path with authentication, cache fallback, persistence, return traffic, and async trace.',
      useWhen: 'API documentation, debugging request latency, auth reviews, or explaining cache fallback.',
      avoidWhen: 'Order is unimportant and the audience only needs the stable service topology.',
      include: ['callers and callees', 'request and return messages', 'fallback or error path', 'async side effects'],
      prompt: 'Use PaintForge sequence mode to show this request from caller to final response. Include authentication, cache hit or miss, persistence fallback, return messages, and asynchronous trace or event emission. Keep message labels short and order unambiguous.',
    },
    zh: {
      title: 'API 请求链', question: '谁调用谁、顺序如何、最终返回什么？',
      summary: '按时间展示鉴权、缓存回退、持久化、返回流量和异步追踪。',
      useWhen: '适合 API 文档、请求耗时排查、鉴权评审和缓存回退说明。',
      avoidWhen: '如果顺序不重要，受众只需要稳定的服务拓扑，请用架构图。',
      include: ['调用方与被调用方', '请求与返回消息', '回退或错误路径', '异步副作用'],
      prompt: '用 PaintForge 时序模式展示从调用方到最终响应的完整请求。包含鉴权、缓存命中或未命中、持久化回退、返回消息，以及异步 Trace 或事件上报；消息标签保持简短，顺序必须明确。',
    },
  },
  {
    id: 'async-roundtrip', type: 'sequence', proof: 'async-roundtrip',
    presentation: { preset: 'signal-flow', motion: 'trace', views: 'recommended' },
    signals: [['async roundtrip', 14], ['webhook', 10], ['callback', 10], ['acknowledgement', 8], ['timeout', 7], ['retry message', 8], ['异步回调', 14], ['回调', 10], ['确认消息', 8], ['超时', 7], ['消息重试', 9], ['webhook', 10]],
    en: {
      title: 'Async roundtrip', question: 'What happens after the initial request returns?',
      summary: 'A sequence view of enqueue, acknowledgement, background work, callbacks, retries, timeout, and final consistency.',
      useWhen: 'Webhooks, jobs, queues, payment callbacks, eventual consistency, or async API contracts.',
      avoidWhen: 'The primary question is topic topology and consumer ownership rather than time order.',
      include: ['initial acknowledgement', 'queue or scheduler', 'background work', 'callback, retry, and timeout'],
      prompt: 'Use PaintForge sequence mode to explain this asynchronous roundtrip. Show the initial acknowledgement, enqueue or scheduling step, background processing, callback or polling, retry and timeout behavior, and the point where the caller can observe final consistency.',
    },
    zh: {
      title: '异步往返链路', question: '初始请求返回之后，后台还会发生什么？',
      summary: '按时间展示入队、确认、后台处理、回调、重试、超时和最终一致。',
      useWhen: '适合 Webhook、后台任务、队列、支付回调、最终一致和异步 API 契约。',
      avoidWhen: '如果重点是 Topic 拓扑和消费者归属，而不是时间顺序，请用事件数据流配方。',
      include: ['初始确认', '队列或调度器', '后台处理', '回调、重试与超时'],
      prompt: '用 PaintForge 时序模式解释这段异步往返链路。展示初始确认、入队或调度、后台处理、回调或轮询、重试与超时，以及调用方何时能观察到最终一致结果。',
    },
  },
  {
    id: 'data-lineage', type: 'dataflow', proof: 'product-analytics',
    presentation: { preset: 'classic', motion: 'trace', views: 'recommended' },
    signals: [['data lineage', 15], ['etl', 12], ['warehouse', 9], ['pii', 11], ['governance', 9], ['analytics pipeline', 12], ['数据血缘', 15], ['数据管道', 11], ['数仓', 9], ['治理', 9], ['隐私数据', 10], ['用户同意', 9]],
    en: {
      title: 'Data lineage', question: 'Where does data come from, how does it change, and who consumes it?',
      summary: 'A governed path from sources through consent, transforms, sensitive stores, warehouse, and consumers.',
      useWhen: 'Analytics architecture, ETL/ELT review, PII assessment, warehouse design, or model feature lineage.',
      avoidWhen: 'The audience needs request timing or operational task ownership rather than data assets.',
      include: ['sources and assets', 'transform stages', 'classification or consent', 'stores and consumers'],
      prompt: 'Use PaintForge dataflow mode to map this data lineage. Name every data asset and transform, show consent or classification boundaries, distinguish streaming from batch paths, and identify stores plus downstream consumers. Do not use unlabeled flows.',
    },
    zh: {
      title: '数据血缘', question: '数据从哪里来、如何变化、最终被谁消费？',
      summary: '从来源经过同意、转换、敏感存储、数仓直到消费者的治理路径。',
      useWhen: '适合分析架构、ETL/ELT 评审、PII 评估、数仓设计和特征血缘。',
      avoidWhen: '如果受众需要请求时序或操作负责人，而不是数据资产，请换其他配方。',
      include: ['数据来源与资产', '转换阶段', '分类或同意边界', '存储与消费者'],
      prompt: '用 PaintForge 数据流模式梳理这段数据血缘。为每个数据资产和转换命名，展示用户同意或数据分类边界，区分流式与批处理路径，并标明存储和下游消费者；所有数据流都必须有标签。',
    },
  },
  {
    id: 'event-stream', type: 'dataflow', proof: 'event-stream',
    presentation: { preset: 'signal-flow', motion: 'trace', views: 'recommended' },
    start: {
      en: { descriptionPrompt: 'Use PaintForge dataflow mode to map this data journey: [paste the sources, data assets, transforms, stores, boundaries, and consumers]. Label every flow, distinguish streaming from batch where relevant, and mark unknown classifications or ownership instead of inventing them.' },
      zh: { descriptionPrompt: '用 PaintForge 数据流模式梳理下面的数据路径：[粘贴来源、数据资产、转换、存储、边界和消费者]。为每条数据流标注名称，在有意义时区分流式与批处理，未知的分类或归属要标明而不是编造。' },
    },
    signals: [['event stream', 15], ['kafka topology', 14], ['topic', 8], ['consumer group', 11], ['dead letter', 10], ['dlq', 10], ['事件流', 15], ['kafka 拓扑', 14], ['主题', 7], ['消费者组', 11], ['死信', 10], ['事件地铁图', 12]],
    en: {
      title: 'Event-stream topology', question: 'Which events move through which topics, processors, groups, and failure paths?',
      summary: 'A stream map of producers, topics, ordered processors, consumer groups, state, replay, and DLQ.',
      useWhen: 'Kafka/event-platform design, stream processing reviews, ownership, replay, and failure handling.',
      avoidWhen: 'Topic names, consumer groups, and delivery semantics are not known—use a generic workflow instead.',
      include: ['producers and event names', 'topics and ordering', 'processors and consumer groups', 'state, replay, and DLQ'],
      prompt: 'Use PaintForge dataflow mode to draw this event-stream topology. Name producers, events, topics, ordered processors, consumer groups, state stores, replay paths, and the DLQ. Show ownership and delivery semantics only when supported by evidence.',
    },
    zh: {
      title: '事件流拓扑', question: '哪些事件经过哪些 Topic、处理器、消费者组和失败路径？',
      summary: '展示生产者、Topic、有序处理器、消费者组、状态、重放和 DLQ。',
      useWhen: '适合 Kafka/事件平台设计、流处理评审、归属、重放和失败处理。',
      avoidWhen: '如果 Topic、消费者组和投递语义都不清楚，请先用通用工作流，不要编造事件拓扑。',
      include: ['生产者与事件名', 'Topic 与顺序', '处理器与消费者组', '状态、重放与 DLQ'],
      prompt: '用 PaintForge 数据流模式绘制这段事件流拓扑。命名生产者、事件、Topic、有序处理器、消费者组、状态存储、重放路径和 DLQ；只有在证据充分时才标注归属和投递语义。',
    },
  },
  {
    id: 'object-lifecycle', type: 'lifecycle', proof: 'agent-run',
    presentation: { preset: 'classic', motion: 'trace', views: 'optional' },
    start: {
      en: { descriptionPrompt: 'Use PaintForge lifecycle mode to model this object: [paste its states, transition events, waits, retries, cancellation, and terminal outcomes]. Separate active, waiting, recoverable-failure, and terminal states, and never hide an ending. No repository is required.' },
      zh: { descriptionPrompt: '用 PaintForge 生命周期模式建模这个对象：[粘贴它的状态、转换事件、等待、重试、取消和终态]。分开执行、等待、可恢复失败和终态，不要隐藏任何结束方式。不需要代码库。' },
    },
    signals: [['state machine', 15], ['object lifecycle', 14], ['status transition', 11], ['terminal state', 9], ['retry state', 8], ['状态机', 15], ['生命周期', 13], ['状态流转', 11], ['终态', 9], ['等待态', 8], ['重试状态', 8]],
    en: {
      title: 'Object lifecycle', question: 'Which states exist, what events move between them, and how does it end?',
      summary: 'A state model with active work, waits, retries, cancellation, failure, and explicit terminal outcomes.',
      useWhen: 'Tasks, orders, tickets, subscriptions, jobs, agent runs, or any durable object with status.',
      avoidWhen: 'The object has no durable state and the real question is participant interaction over time.',
      include: ['start and active states', 'event-labelled transitions', 'wait and retry states', 'all terminal outcomes'],
      prompt: 'Use PaintForge lifecycle mode to model this object. Separate main progress, waiting or interruption states, and terminal outcomes. Label transitions with events, include retry, cancellation, timeout, success, and failure where real, and never hide an ending.',
    },
    zh: {
      title: '对象生命周期', question: '有哪些状态、什么事件触发流转、最终如何结束？',
      summary: '展示执行、等待、重试、取消、失败以及明确终态的状态模型。',
      useWhen: '适合任务、订单、工单、订阅、作业、Agent Run 等带持久状态的对象。',
      avoidWhen: '对象没有持久状态，真正问题是参与者随时间的交互时，请使用时序图。',
      include: ['开始与执行态', '带事件的转换', '等待与重试态', '所有终态'],
      prompt: '用 PaintForge 生命周期模式建模这个对象。分开主进度、等待或中断状态和终态；用事件标注转换，并在真实存在时展示重试、取消、超时、成功和失败，不能隐藏任何结束方式。',
    },
  },
  {
    id: 'deployment-lifecycle', type: 'lifecycle', proof: 'deployment-lifecycle',
    presentation: { preset: 'signal-flow', motion: 'trace', views: 'recommended' },
    signals: [['deployment lifecycle', 15], ['release state', 10], ['promotion state', 9], ['approval status', 8], ['rollback state', 10], ['部署生命周期', 15], ['发布状态', 10], ['晋级', 7], ['审批状态', 8], ['回滚状态', 10]],
    en: {
      title: 'Deployment lifecycle', question: 'What state is a release in, and what can happen next?',
      summary: 'A deployment state model covering queued, building, verifying, approval, promotion, rollback, and terminal outcomes.',
      useWhen: 'Release controllers, GitOps reconciliation, environment promotion, or deployment status APIs.',
      avoidWhen: 'The question is the human/CI sequence of delivery actions rather than the deployment object state.',
      include: ['queued and running states', 'verification and approval', 'promotion and rollback', 'success, failure, cancellation'],
      prompt: 'Use PaintForge lifecycle mode to model the deployment object. Show queued, building, verifying, waiting for approval, promoting, rolling back, and every terminal outcome. Label the events and guards that permit each transition.',
    },
    zh: {
      title: '部署生命周期', question: '一次发布当前处于什么状态，下一步可能发生什么？',
      summary: '覆盖排队、构建、验证、审批、晋级、回滚和终态的部署状态模型。',
      useWhen: '适合发布控制器、GitOps 对账、环境晋级和部署状态 API。',
      avoidWhen: '如果重点是人员与 CI 的交付动作顺序，而不是部署对象状态，请用交付工作流。',
      include: ['排队与执行态', '验证与审批', '晋级与回滚', '成功、失败与取消'],
      prompt: '用 PaintForge 生命周期模式建模部署对象。展示排队、构建、验证、等待审批、晋级、回滚以及所有终态，并标注允许每次状态转换的事件和守卫条件。',
    },
  },
  {
    id: 'entity-relationship', type: 'er', proof: 'order-system',
    presentation: { preset: 'classic', motion: 'static', views: 'optional' },
    start: {
      en: { descriptionPrompt: 'Use PaintForge er mode to model this data model: [paste the entities, attributes, primary/foreign keys, and relationships with cardinality]. Name every attribute and its type, mark PK/FK/UQ keys, and label every relationship with one/many cardinality on both ends. No repository is required.' },
      zh: { descriptionPrompt: '用 PaintForge ER 模式建模这个数据模型：[粘贴实体、属性、主/外键，以及带基数的关系]。为每个属性命名并标注类型，标出 PK/FK/UQ 键，并为每条关系在两端标注一对多/多对多基数。不需要代码库。' },
    },
    signals: [['entity relationship', 16], ['er diagram', 15], ['database schema', 14], ['data model', 13], ['foreign key', 11], ['primary key', 10], ['table relationship', 12], ['实体关系', 16], ['er 图', 15], ['数据库结构', 14], ['数据模型', 13], ['外键', 11], ['主键', 10], ['表关系', 12]],
    en: {
      title: 'Entity-relationship model', question: 'What entities exist, what fields define them, and how are they related?',
      summary: 'A data model of entities, typed attributes with PK/FK/UQ keys, and cardinality-labelled relationships.',
      useWhen: 'Database design, schema review, data modelling, or onboarding developers to a data model.',
      avoidWhen: 'The question is data movement between systems rather than the schema of one model.',
      include: ['entities with typed attributes', 'PK, FK, and UQ key markers', 'cardinality on both relationship ends', 'a clear parent-to-child layering'],
      prompt: 'Use PaintForge er mode to draw this data model. List each entity with its typed attributes and mark primary, foreign, and unique keys. Label every relationship with cardinality on both ends, and orient the graph so parents sit above children with no crossed edges.',
    },
    zh: {
      title: '实体关系模型', question: '有哪些实体、由哪些字段定义、彼此如何关联？',
      summary: '展示实体、带类型的属性、PK/FK/UQ 键标记，以及带基数的关系。',
      useWhen: '适合数据库设计、表结构评审、数据建模和让新同学理解数据模型。',
      avoidWhen: '如果重点是系统之间的数据流动，而不是单个模型的结构，请用数据流图。',
      include: ['带类型属性的实体', 'PK、FK、UQ 键标记', '关系两端的基数', '父实体在上、子实体在下的分层'],
      prompt: '用 PaintForge ER 模式绘制这个数据模型。列出每个实体及其带类型的属性，标记主键、外键和唯一键；为每条关系标注两端基数，并把图摆成父实体在上、子实体在下、无交叉连线的方向。',
    },
  },
  {
    id: 'dependency-graph', type: 'dependency', proof: 'web-app',
    presentation: { preset: 'classic', motion: 'static', views: 'optional' },
    start: {
      en: { descriptionPrompt: 'Use PaintForge dependency mode to map this module graph: [paste the modules, packages, or services and their dependencies with version and kind]. Mark runtime vs dev dependencies, name the shared leaves, and keep the graph acyclic where real. No repository is required.' },
      zh: { descriptionPrompt: '用 PaintForge 依赖模式梳理这个模块图：[粘贴模块、包或服务，以及它们的依赖、版本和类型]。区分运行时依赖和开发依赖，标出共享的底层库，并尽量保持无环。不需要代码库。' },
    },
    signals: [['dependency graph', 16], ['package dependency', 14], ['module dependency', 13], ['import graph', 12], ['dependency tree', 12], ['npm dependency', 11], ['依赖关系', 16], ['包依赖', 14], ['模块依赖', 13], ['依赖图', 15], ['依赖树', 12], ['导入关系', 11]],
    en: {
      title: 'Dependency graph', question: 'Which modules depend on which, and what is shared?',
      summary: 'A layered module graph with version tags and runtime-vs-dev dependency edges.',
      useWhen: 'Package architecture, module coupling review, import cycles, or onboarding developers to a codebase.',
      avoidWhen: 'The question is runtime request flow between services rather than code-level dependencies.',
      include: ['modules with version tags', 'runtime vs dev dependency edges', 'shared leaf libraries', 'acyclic parent-to-child layering'],
      prompt: 'Use PaintForge dependency mode to draw this module graph. Name each module with its version and kind, distinguish runtime dependencies from development-only imports, mark shared leaf libraries, and orient the graph acyclically with parents above children.',
    },
    zh: {
      title: '依赖关系图', question: '哪些模块依赖哪些模块，共享了什么？',
      summary: '带版本标签的分层模块图，区分运行时与开发依赖边。',
      useWhen: '适合包结构设计、模块耦合评审、循环依赖排查和让新同学理解代码库。',
      avoidWhen: '如果重点是服务之间的运行时请求流，而不是代码级依赖，请用架构图或时序图。',
      include: ['带版本标签的模块', '运行时与开发依赖边', '共享的底层库', '父在上子在下的无环分层'],
      prompt: '用 PaintForge 依赖模式绘制这个模块图。为每个模块标注版本和类型，区分运行时依赖与仅开发期导入，标出共享的底层库，并把图摆成父模块在上、子模块在下、无环的方向。',
    },
  },
  {
    id: 'organization-chart', type: 'org', proof: 'engineering-team',
    presentation: { preset: 'classic', motion: 'static', views: 'optional' },
    start: {
      en: { descriptionPrompt: 'Use PaintForge org mode to map this team: [paste the people, their titles, and who reports to whom]. One manager per person, mark teams, and keep the tree acyclic. No repository is required.' },
      zh: { descriptionPrompt: '用 PaintForge 组织架构模式梳理这个团队：[粘贴成员、职位，以及谁向谁汇报]。每人只有一个上级，标出所属团队，并保持树形无环。不需要代码库。' },
    },
    signals: [['organization chart', 16], ['org chart', 15], ['reporting structure', 14], ['team structure', 13], ['who reports to whom', 12], ['management hierarchy', 12], ['组织架构', 16], ['汇报关系', 14], ['团队结构', 13], ['管理层级', 12], ['人员架构', 12], ['谁向谁汇报', 13]],
    en: {
      title: 'Organization chart', question: 'Who reports to whom, and how is the team grouped?',
      summary: 'A tree of people with titles and team tags, connected by reporting lines.',
      useWhen: 'Team onboarding, reorg planning, span-of-control review, or explaining management hierarchy.',
      avoidWhen: 'The question is project ownership or task flow rather than people reporting.',
      include: ['people with titles', 'team tags', 'one manager per person', 'clean top-to-bottom tree'],
      prompt: 'Use PaintForge org mode to draw this team. List each person with a title and team tag, connect manager-to-report lines, and lay the tree out top-to-bottom with no crossing reporting lines.',
    },
    zh: {
      title: '组织架构图', question: '谁向谁汇报，团队如何分组？',
      summary: '带职位和团队标签的人员树，用汇报线连接。',
      useWhen: '适合团队入职、组织调整规划、管理幅度评审和说明管理层级。',
      avoidWhen: '如果重点是项目归属或任务流转，而不是人员汇报关系，请用架构图或工作流。',
      include: ['带职位的人员', '团队标签', '每人一个上级', '自上而下的清晰树形'],
      prompt: '用 PaintForge 组织架构模式绘制这个团队。列出每个成员及其职位和团队标签，连接上级到下级的汇报线，并把树自上而下摆开，避免汇报线交叉。',
    },
  },
  {
    id: 'mind-map', type: 'mindmap', proof: 'product-roadmap',
    presentation: { preset: 'classic', motion: 'static', views: 'optional' },
    start: {
      en: { descriptionPrompt: 'Use PaintForge mindmap mode to brainstorm this topic: [paste the central idea and its main branches, each with subtopics]. Keep the tree shallow and readable, one central topic with themed branches. No repository is required.' },
      zh: { descriptionPrompt: '用 PaintForge 思维导图模式梳理这个主题：[粘贴中心主题、主要分支，以及各分支的子主题]。保持层次浅而清晰，一个中心主题配上若干主题分支。不需要代码库。' },
    },
    signals: [['mind map', 16], ['mindmap', 15], ['brainstorm', 13], ['idea map', 12], ['topic outline', 11], ['central topic', 11], ['思维导图', 16], ['头脑风暴', 13], ['主题大纲', 12], ['想法图', 12], ['中心主题', 11], ['知识地图', 11]],
    en: {
      title: 'Mind map', question: 'What is the central idea, and how do its themes branch out?',
      summary: 'A central topic with themed branches flowing right into subtopics.',
      useWhen: 'Brainstorming, outlining, knowledge organization, or decomposing a topic.',
      avoidWhen: 'The question is a strict hierarchy of people or a process with gates.',
      include: ['one central topic', 'themed main branches', 'subtle subtopics', 'shallow readable depth'],
      prompt: 'Use PaintForge mindmap mode to brainstorm this topic. Put the central idea on the left, fan its main themes to the right, and keep each branch shallow with a few subtopics. Use emphasis variants for the main branches.',
    },
    zh: {
      title: '思维导图', question: '中心主题是什么，它的各个主题如何向外发散？',
      summary: '中心主题在左，主题分支向右发散到子主题。',
      useWhen: '适合头脑风暴、列大纲、知识组织和拆分主题。',
      avoidWhen: '如果重点是严格的人员层级或带门控的流程，请用组织架构图或工作流。',
      include: ['一个中心主题', '主题主干分支', '若干子主题', '浅而清晰的层次'],
      prompt: '用 PaintForge 思维导图模式梳理这个主题。把中心主题放在左侧，主干主题向右发散，每个分支保持浅层、只带几个子主题，并用 emphasis 变体突出主干分支。',
    },
  },
  {
    id: 'flowchart', type: 'flowchart', proof: 'signup-flow',
    presentation: { preset: 'classic', motion: 'static', views: 'optional' },
    start: {
      en: { descriptionPrompt: 'Use PaintForge flowchart mode to map this process: [paste the steps, decision points, inputs/outputs, and terminal outcomes]. Use decision diamonds for branches, process boxes for actions, and mark start/end. Keep one clear happy path. No repository is required.' },
      zh: { descriptionPrompt: '用 PaintForge 流程图模式梳理这个过程：[粘贴步骤、决策点、输入/输出和结束状态]。决策用菱形、操作用矩形、标记开始和结束，保留一条清晰的成功主路径。不需要代码库。' },
    },
    signals: [['flowchart', 16], ['flow chart', 15], ['process flow', 13], ['decision tree', 12], ['algorithm', 11], ['control flow', 11], ['流程图', 16], ['流程', 12], ['决策树', 12], ['算法流程', 11], ['控制流', 11], ['业务流程', 12]],
    en: {
      title: 'Flowchart', question: 'What are the steps, decisions, and outcomes of this process?',
      summary: 'Shape-differentiated steps (process, decision, io, start/end) with labelled branches.',
      useWhen: 'Algorithms, business processes, approval flows, or any decision-heavy procedure.',
      avoidWhen: 'The question is lane-based ownership (use workflow) or a strict data model.',
      include: ['decision diamonds', 'process boxes', 'io parallelograms', 'start and end terminals'],
      prompt: 'Use PaintForge flowchart mode to draw this process. Mark start and end, use decision diamonds for branches with labelled yes/no edges, process boxes for actions, and io shapes for inputs/outputs. Keep one obvious happy path.',
    },
    zh: {
      title: '流程图', question: '这个过程有哪些步骤、决策和结果？',
      summary: '用不同形状区分的步骤（流程/决策/输入输出/起止），带标注的分支。',
      useWhen: '适合算法、业务流程、审批流或任何决策密集的过程。',
      avoidWhen: '如果重点是泳道式职责归属（用工作流）或严格的数据模型，请换对应图。',
      include: ['决策菱形', '流程矩形', '输入输出平行四边形', '开始与结束端点'],
      prompt: '用 PaintForge 流程图模式绘制这个过程。标记开始和结束，决策用菱形并标注 yes/no 分支，操作用矩形，输入输出用平行四边形，保留一条一眼可见的成功主路径。',
    },
  },
  {
    id: 'network-topology', type: 'network', proof: 'office-network',
    presentation: { preset: 'classic', motion: 'static', views: 'optional' },
    start: {
      en: { descriptionPrompt: 'Use PaintForge network mode to map this topology: [paste the devices, their kinds, and the physical or logical links between them]. Mark firewalls, switches, routers, servers, and clients. No repository is required.' },
      zh: { descriptionPrompt: '用 PaintForge 网络拓扑模式梳理这个拓扑：[粘贴设备、类型，以及它们之间的物理或逻辑连接]。标出防火墙、交换机、路由器、服务器和客户端。不需要代码库。' },
    },
    signals: [['network topology', 16], ['network diagram', 15], ['infrastructure', 12], ['firewall', 10], ['switch', 10], ['router', 10], ['网络拓扑', 16], ['网络图', 15], ['基础设施', 12], ['防火墙', 10], ['交换机', 10], ['路由器', 10]],
    en: {
      title: 'Network topology', question: 'What devices exist and how are they physically or logically linked?',
      summary: 'A force-directed map of devices (firewall, switch, router, server, client) with links.',
      useWhen: 'Network documentation, infrastructure overview, security zoning, or device inventory.',
      avoidWhen: 'The question is application-level components (use architecture) or data flow (use dataflow).',
      include: ['device kinds (firewall/switch/router/server/client)', 'physical or logical links', 'a readable spread of nodes'],
      prompt: 'Use PaintForge network mode to draw this topology. Mark each device kind, connect them with undirected links, and let the force-directed layout spread the nodes for clarity. Note this layout is not geometrically verified — prioritize relationship readability.',
    },
    zh: {
      title: '网络拓扑', question: '有哪些设备，它们之间如何物理或逻辑连接？',
      summary: '用设备（防火墙/交换机/路由器/服务器/客户端）加连线的力导向图。',
      useWhen: '适合网络文档、基础设施总览、安全分区和设备清单。',
      avoidWhen: '如果重点是应用级组件（用架构图）或数据流（用数据流图），请换对应图。',
      include: ['设备类型（防火墙/交换机/路由器/服务器/客户端）', '物理或逻辑连线', '节点清晰铺开'],
      prompt: '用 PaintForge 网络拓扑模式绘制这个拓扑。标注每个设备的类型，用无向连线连接它们，让力导向布局把节点铺开以便阅读。注意此布局不做几何验收——优先保证关系可读。',
    },
  },
  {
    id: 'priority-matrix', type: 'matrix', proof: 'feature-priority',
    presentation: { preset: 'classic', motion: 'static', views: 'optional' },
    start: {
      en: { descriptionPrompt: 'Use PaintForge matrix mode to plot this 2x2: [paste the items with their x and y scores, plus axis labels and low/high ends]. Map value vs effort, impact vs likelihood, or any two dimensions. No repository is required.' },
      zh: { descriptionPrompt: '用 PaintForge 四象限矩阵模式绘制这个 2x2：[粘贴项目及其 x/y 分数，加上轴标签和低/高端]。映射价值 vs 投入、影响 vs 概率，或任意两个维度。不需要代码库。' },
    },
    signals: [['priority matrix', 15], ['quadrant', 13], ['2x2', 11], ['value effort', 12], ['impact likelihood', 12], ['impact effort', 12], ['优先级矩阵', 15], ['四象限', 13], ['价值投入', 12], ['影响概率', 12], ['影响投入', 12], ['决策矩阵', 13]],
    en: {
      title: 'Priority matrix', question: 'Where does each item fall on two scored dimensions?',
      summary: 'A 2x2 quadrant with items plotted by x and y scores on labelled axes.',
      useWhen: 'Feature prioritization, risk assessment, portfolio review, or any value-vs-cost decision.',
      avoidWhen: 'The dimensions are not numeric or the goal is a ranked list rather than relative position.',
      include: ['labelled x and y axes', 'low/high ends', 'items plotted by score', 'clear quadrant separation'],
      prompt: 'Use PaintForge matrix mode to plot this 2x2. Label both axes with a name and low/high ends, plot each item by its x and y score, and keep items spread so labels do not overlap.',
    },
    zh: {
      title: '四象限矩阵', question: '每个项目在两个评分维度上落在哪里？',
      summary: '用带标签坐标轴的 2x2 四象限，按 x/y 分数绘制项目。',
      useWhen: '适合功能优先级、风险评估、组合评审或任何价值-成本决策。',
      avoidWhen: '如果维度不是数值，或目标是排序列表而非相对位置，请换其他表达。',
      include: ['带标签的 x/y 轴', '低/高端标注', '按分数绘制的项目', '清晰的四象限分隔'],
      prompt: '用 PaintForge 四象限矩阵模式绘制这个 2x2。给两个轴命名并标注低/高端，按 x/y 分数绘制每个项目，保持项目分散避免标签重叠。',
    },
  },
  {
    id: 'kanban-board', type: 'kanban', proof: 'sprint-board',
    presentation: { preset: 'classic', motion: 'static', views: 'optional' },
    start: {
      en: { descriptionPrompt: 'Use PaintForge kanban mode to build this board: [paste the columns and the cards with their column assignment]. Group tasks by status, tag priority, and keep columns readable. No repository is required.' },
      zh: { descriptionPrompt: '用 PaintForge 看板模式构建这个看板：[粘贴列，以及带列归属的卡片]。按状态分组任务、标注优先级，保持各列可读。不需要代码库。' },
    },
    signals: [['kanban', 16], ['board', 12], ['sprint board', 14], ['task status', 12], ['to do', 10], ['in progress', 10], ['看板', 16], ['冲刺板', 14], ['任务状态', 12], ['待办', 10], ['进行中', 10], ['已完成', 10]],
    en: {
      title: 'Kanban board', question: 'What tasks exist and what status column is each in?',
      summary: 'Status columns with cards grouped by their current state.',
      useWhen: 'Sprint planning, task tracking, or status review.',
      avoidWhen: 'The question is a workflow with gates (use workflow) or a ranked timeline (use gantt).',
      include: ['status columns', 'cards grouped by column', 'priority tags', 'readable column widths'],
      prompt: 'Use PaintForge kanban mode to draw this board. Define the status columns, assign each card to a column, tag priorities, and keep cards inside their column with no overlap.',
    },
    zh: {
      title: '看板', question: '有哪些任务，各自处于什么状态列？',
      summary: '按状态列分组卡片的看板。',
      useWhen: '适合冲刺规划、任务跟踪或状态评审。',
      avoidWhen: '如果重点是带门控的流程（用工作流）或排序时间线（用甘特图），请换对应图。',
      include: ['状态列', '按列分组的卡片', '优先级标签', '列宽可读'],
      prompt: '用 PaintForge 看板模式绘制这个看板。定义状态列，把每张卡片分到对应列，标注优先级，并保持卡片在列内不重叠。',
    },
  },
  {
    id: 'venn-diagram', type: 'venn', proof: 'devops-shared',
    presentation: { preset: 'classic', motion: 'static', views: 'optional' },
    start: {
      en: { descriptionPrompt: 'Use PaintForge venn mode to map these sets: [paste the 2 or 3 sets and the labelled intersections between them]. Show shared and distinct zones. No repository is required.' },
      zh: { descriptionPrompt: '用 PaintForge 维恩图模式映射这些集合：[粘贴 2 或 3 个集合，以及它们之间的带标签交集]。展示共享区和互斥区。不需要代码库。' },
    },
    signals: [['venn diagram', 16], ['set overlap', 13], ['shared responsibility', 12], ['intersection', 11], ['union', 10], ['维恩图', 16], ['集合重叠', 13], ['交集', 11], ['并集', 10], ['共享职责', 12], ['集合关系', 12]],
    en: {
      title: 'Venn diagram', question: 'Which sets overlap, and what do the overlaps mean?',
      summary: 'Overlapping circles with labelled intersections for 2 or 3 sets.',
      useWhen: 'Set relationships, shared responsibility, or overlap analysis.',
      avoidWhen: 'There are more than 3 sets, or the values are quantitative (use a chart).',
      include: ['2-3 overlapping sets', 'labelled intersections', 'distinct set labels', 'clear overlap zones'],
      prompt: 'Use PaintForge venn mode to draw these sets. Label each set, mark every two-way and three-way intersection, and keep the overlap zones readable.',
    },
    zh: {
      title: '维恩图', question: '哪些集合重叠，重叠意味着什么？',
      summary: '2-3 个集合的相交圆，带交集标签。',
      useWhen: '适合集合关系、共享职责或重叠分析。',
      avoidWhen: '如果超过 3 个集合，或数值是定量的（用统计图），请换其他表达。',
      include: ['2-3 个重叠集合', '带标签的交集', '清晰的集合名', '重叠区可读'],
      prompt: '用 PaintForge 维恩图模式绘制这些集合。给每个集合命名，标注每个两两交集和三重交集，保持重叠区域可读。',
    },
  },
  {
    id: 'gantt-chart', type: 'gantt', proof: 'release-plan',
    presentation: { preset: 'classic', motion: 'static', views: 'optional' },
    start: {
      en: { descriptionPrompt: 'Use PaintForge gantt mode to plot this timeline: [paste the tasks with their YYYY-MM-DD start and end dates, plus optional group]. Mark parallel workstreams and overlapping windows. No repository is required.' },
      zh: { descriptionPrompt: '用 PaintForge 甘特图模式绘制这个时间线：[粘贴任务及其 YYYY-MM-DD 起止日期，可选分组]。标出并行工作流和重叠窗口。不需要代码库。' },
    },
    signals: [['gantt', 16], ['gantt chart', 15], ['timeline', 13], ['schedule', 12], ['project plan', 12], ['甘特图', 16], ['时间线', 13], ['排期', 12], ['项目计划', 12], ['里程碑', 11]],
    en: {
      title: 'Gantt chart', question: 'What runs when, and which tasks overlap?',
      summary: 'A timeline of tasks with start/end bars and date gridlines.',
      useWhen: 'Project scheduling, release planning, or timeline overview.',
      avoidWhen: 'The question is task ownership (use kanban) or process gates (use workflow).',
      include: ['dated task bars', 'time axis gridlines', 'parallel workstreams', 'clear start/end'],
      prompt: 'Use PaintForge gantt mode to draw this timeline. Plot each task as a bar from its start to end date, add gridlines on the time axis, and keep parallel tasks on separate rows.',
    },
    zh: {
      title: '甘特图', question: '什么任务在何时进行，哪些任务重叠？',
      summary: '带起止横条和日期网格线的任务时间线。',
      useWhen: '适合项目排期、发布计划或时间线总览。',
      avoidWhen: '如果重点是任务归属（用看板）或流程门控（用工作流），请换对应图。',
      include: ['带日期的任务横条', '时间轴网格线', '并行工作流', '清晰的起止'],
      prompt: '用 PaintForge 甘特图模式绘制这个时间线。把每个任务画成从开始到结束日期的横条，在时间轴上加网格线，并行任务放在不同行。',
    },
  },
  {
    id: 'sankey-diagram', type: 'sankey', proof: 'energy-flow',
    presentation: { preset: 'classic', motion: 'static', views: 'optional' },
    start: {
      en: { descriptionPrompt: 'Use PaintForge sankey mode to map this flow: [paste the nodes grouped by column, and the flows with their values]. Show how quantity moves left to right through stages. No repository is required.' },
      zh: { descriptionPrompt: '用 PaintForge 桑基图模式映射这个流向：[粘贴按列分组的节点，以及带数值的流]。展示数量如何从左到右流经各阶段。不需要代码库。' },
    },
    signals: [['sankey', 16], ['sankey diagram', 15], ['flow quantity', 12], ['energy flow', 12], ['budget flow', 11], ['桑基图', 16], ['流向', 12], ['能量流', 12], ['资金流', 11], ['流量图', 13]],
    en: {
      title: 'Sankey diagram', question: 'How does quantity flow from sources to sinks across stages?',
      summary: 'Proportional ribbons moving left to right through grouped columns.',
      useWhen: 'Energy, budget, or traffic flow across stages.',
      avoidWhen: 'The graph has cycles or flows do not move strictly left to right.',
      include: ['columns increasing left to right', 'flow-proportional node heights', 'ribbon widths matching value', 'labelled flows'],
      prompt: 'Use PaintForge sankey mode to draw this flow. Group nodes into left-to-right columns, size each node by its total flow, and connect them with ribbons whose width matches the flow value.',
    },
    zh: {
      title: '桑基图', question: '数量如何从源头流经各阶段到末端？',
      summary: '按列分组、从左到右流动的比例带宽。',
      useWhen: '适合能量、资金或流量在多个阶段间的流转。',
      avoidWhen: '如果图有环，或流不是严格从左到右，请换其他表达。',
      include: ['从左到右递增的列', '按流量比例缩放节点高度', '带宽匹配数值', '带标签的流'],
      prompt: '用 PaintForge 桑基图模式绘制这个流向。把节点按列从左到右分组，每个节点高度按其总流量缩放，用宽度匹配流量数值的带连接它们。',
    },
  },
];

export const SCENARIO_RECIPES = Object.freeze(RAW_RECIPES.map((recipe) => Object.freeze({
  ...recipe,
  presentation: Object.freeze({ ...recipe.presentation }),
  ...(recipe.start ? { start: Object.freeze({
    en: Object.freeze({ ...recipe.start.en }),
    zh: Object.freeze({ ...recipe.start.zh }),
  }) } : {}),
  signals: Object.freeze(recipe.signals.map((signal) => Object.freeze(signal.slice()))),
  en: Object.freeze({ ...recipe.en, include: Object.freeze(recipe.en.include.slice()) }),
  zh: Object.freeze({ ...recipe.zh, include: Object.freeze(recipe.zh.include.slice()) }),
})));

export function detectGuideLanguage(value = '') {
  return /[\u3400-\u9fff]/u.test(value) ? 'zh' : 'en';
}

export function startPromptsFor(recipe, lang = 'en') {
  const language = lang === 'zh' ? 'zh' : 'en';
  const copy = recipe[language];
  const descriptionPrompt = recipe.start?.[language]?.descriptionPrompt;
  if (!descriptionPrompt) {
    throw new Error(`Scenario recipe ${JSON.stringify(recipe.id)} does not define a ${language} start prompt.`);
  }
  const repositoryPrompt = recipe.type === 'architecture'
    ? copy.prompt
    : language === 'zh'
      ? `先检查这个仓库里的相关证据，然后${copy.prompt}不要编造代码无法支持的行为。`
      : `Inspect this repository for evidence, then ${copy.prompt.charAt(0).toLowerCase()}${copy.prompt.slice(1)} Do not invent behavior that the code does not support.`;
  return { descriptionPrompt, repositoryPrompt };
}

function normalized(value) {
  return String(value || '').normalize('NFKC').toLowerCase().replace(/[\s_]+/g, ' ').trim();
}

function localized(recipe, lang) {
  const copy = recipe[lang === 'zh' ? 'zh' : 'en'];
  return {
    id: recipe.id,
    type: recipe.type,
    proof: recipe.proof,
    presentation: { ...recipe.presentation },
    ...copy,
    include: copy.include.slice(),
  };
}

export function listScenarioRecipes(lang = 'en') {
  return SCENARIO_RECIPES.map((recipe) => localized(recipe, lang));
}

function scoreRecipe(recipe, query) {
  const text = normalized(query);
  if (!text) return { recipe, score: 0, matched: [] };
  if (text === recipe.id || text === recipe.id.replace(/-/g, ' ')) {
    return { recipe, score: 100, matched: [recipe.id] };
  }
  let score = 0;
  const matched = [];
  for (const [signal, weight] of recipe.signals) {
    if (text.includes(normalized(signal))) {
      score += weight;
      matched.push(signal);
    }
  }
  return { recipe, score, matched };
}

export function recommendScenario(query, options = {}) {
  const lang = options.lang === 'zh' || options.lang === 'en' ? options.lang : detectGuideLanguage(query);
  const ranked = SCENARIO_RECIPES.map((recipe) => scoreRecipe(recipe, query))
    .sort((left, right) => right.score - left.score || SCENARIO_RECIPES.indexOf(left.recipe) - SCENARIO_RECIPES.indexOf(right.recipe));
  const winner = ranked[0].score > 0 ? ranked[0] : { recipe: SCENARIO_RECIPES[0], score: 0, matched: [] };
  const confidence = winner.score >= 14 ? 'high' : winner.score >= 7 ? 'medium' : 'low';
  return {
    ok: true,
    mode: 'recommendation',
    lang,
    query: String(query || ''),
    confidence,
    matchedSignals: winner.matched.slice(),
    recommendation: localized(winner.recipe, lang),
    alternatives: ranked.filter((entry) => entry.recipe.id !== winner.recipe.id && entry.score > 0)
      .slice(0, 2)
      .map((entry) => ({ ...localized(entry.recipe, lang), score: entry.score })),
  };
}

export function formatScenarioList(lang = 'en') {
  const isZh = lang === 'zh';
  const heading = isZh
    ? `PaintForge 场景配方（${SCENARIO_RECIPES.length}）`
    : `PaintForge scenario recipes (${SCENARIO_RECIPES.length})`;
  const intro = isZh
    ? '先选择你要回答的问题，再选择图表类型。可运行：paintforge guide "你的场景"'
    : 'Choose the question before the diagram type. Run: paintforge guide "your scenario"';
  return [heading, '', intro, '', ...listScenarioRecipes(lang).flatMap((recipe) => [
    `${recipe.id}  [${recipe.type}]  ${recipe.title}`,
    `  ${recipe.question}`,
  ])].join('\n');
}

export function formatScenarioRecommendation(result) {
  const isZh = result.lang === 'zh';
  const recipe = result.recommendation;
  const labels = isZh ? {
    heading: '推荐', question: '要回答的问题', use: '适合', avoid: '不要这样用', include: '必须包含', presentation: '表现建议', prompt: '可直接复制的提示词', alternatives: '其他可能', confidence: '置信度',
  } : {
    heading: 'Recommendation', question: 'Question answered', use: 'Use when', avoid: 'Avoid when', include: 'Must include', presentation: 'Presentation', prompt: 'Copy-ready prompt', alternatives: 'Other possible fits', confidence: 'Confidence',
  };
  const lines = [
    `${labels.heading}: ${recipe.title}  [${recipe.type}]`,
    `${labels.confidence}: ${result.confidence}`,
    `${labels.question}: ${recipe.question}`,
    '',
    `${labels.use}: ${recipe.useWhen}`,
    `${labels.avoid}: ${recipe.avoidWhen}`,
    `${labels.include}: ${recipe.include.join(isZh ? '、' : '; ')}`,
    `${labels.presentation}: ${recipe.presentation.preset} · ${recipe.presentation.motion} · views ${recipe.presentation.views}`,
    '',
    `${labels.prompt}:`,
    recipe.prompt,
  ];
  if (result.alternatives.length) {
    lines.push('', `${labels.alternatives}: ${result.alternatives.map((item) => `${item.title} [${item.type}]`).join(' · ')}`);
  }
  return lines.join('\n');
}

export function publicGuideData() {
  return SCENARIO_RECIPES.map((recipe) => ({
    ...localized(recipe, 'en'),
    en: recipe.en,
    zh: recipe.zh,
    signals: recipe.signals.map(([signal, weight]) => [signal, weight]),
  }));
}
