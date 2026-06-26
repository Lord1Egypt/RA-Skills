---
name: interactive-architecture-diagram
description: 强大的AI自动化绘图与复杂信息可视化工具（基于 ContextWeave）。不仅支持代码与系统架构的可视化，更广泛适用于复杂逻辑梳理、知识库转换、业务流程图、思维导图及长文本的结构化信息图生成。通过深度的语义分析与请求编排，一键将晦涩文本与复杂知识转化为清晰直观的图形表达。
metadata: { "openclaw": { "emoji": "🧠", "requires": { "bins": ["node"] }, "primaryEnv": "CONTEXTWEAVE_MCP_API_KEY" } }
---

# ContextWeave Skill

本 Skill 的定位是“绘图请求客户端”，负责把用户需求转换为可执行的绘图意图，并通过基于文件生成的单一路径与后端协同完成产出。

## 哲学层

### 论证而非展示

- 图结构必须服务于语义论证，而非仅做视觉摆放
- 概念层级、因果关系、依赖链路需成为结构主线
- 当存在多种图形组织方式时，优先选择能解释“为什么这样组织”的方案

### 关系显式化

- 关系通过显式连线、依赖方向、分层归属表达
- 禁止用“元素靠得近”替代关系定义
- 关键关系必须可被复述为明确语句（例如“A 依赖 B”“C 触发 D”）

### 同构校验

- 结构方案应通过“去文字后仍可识别核心逻辑”的检验
- 若移除文本标签后关系含义丢失，说明结构设计不合格
- 每次复杂改动后都需重新校验结构与语义是否同构

## 术语语义补全规则

### 未知专有名词强制释义

- 对后端返回或用户输入中的未知专有名词，必须先完成语义释义再进入绘图请求编排
- 未释义术语不得直接作为节点标签、分组标题或关系端点输出
- 释义结论需可复述为完整语句，避免仅保留缩写或单词本体

### 最小补全信息集

- 角色：术语在当前系统中的对象类型与责任边界
- 层级：术语所属模块、抽象层或业务层位置
- 动作：术语触发、承载或约束的关键行为
- 上下游关系：术语与前置依赖、后续影响对象的连接关系

### 反模式约束

- 禁止“仅列词成框”：只把术语放入方框但不定义语义与关系
- 若输入仅包含术语清单，先补全最小信息集，再生成结构化图意图
- 替代写法必须体现“术语定义 + 关系链路 + 作用路径”，而非词汇堆叠

## 案例执行准则

### Good Case 准则

- 归纳为“链路完备输入”：输入已包含术语语义、关系方向、层级归属与关键动作
- 编排时直接进入结构决策与请求组织，重点优化论证路径与可读性

### Bad Case 准则

- 归纳为“术语不足输入先释义再出图”：输入语义不足时，先补全术语定义与上下游关系
- 补全完成前不得进入最终生成阶段

### 输出前自检

- 检查是否存在未释义专有名词
- 检查每个关键术语是否具备角色、层级、动作、上下游关系
- 检查图中是否出现“仅列词成框”且缺少关系链路
- 检查 good/bad case 准则是否被正确执行

## 会话规则

- 客户端本身无状态，状态由后端托管
- 首次生成后必须从返回 JSON 中提取 `session_id`
- 当前默认流程只要求完成基于文件的生成调用
- 不要求用户重复输入旧会话，优先复用上一步返回值
- 若会话缺失或过期，按错误策略重试当前生成调用

## 客户端职责边界

### 客户端负责

- 分析用户输入，抽取实体、关系、层级与叙事路径
- 将图表达意图组织为结构化文件，并触发基于 `input_file` 的后端调用
- 首次生成时：保留 `# CW` 段作为结构占位即可，不要求客户端预先写入非空的首版 CW
- 修改已有图时：在 `# CW` 段中放入现有 CW 文本，并连同本轮修改意图一起提交
- 从后端返回中提取关键字段并组织规整结果输出

### 后端负责

- 绘图引擎执行与渲染产出
- 图元布局、坐标计算、路由与格式化导出实现
- 运行时执行控制与图形生成细节

### 非职责范围

- 本地编译流程与执行管线设计
- 本地渲染实现或图形引擎运行细节
- 在 Skill 层定义坐标级布局算法与底层绘图执行逻辑

## 执行优先级规则

- 默认只走“请求编排为文件后，基于文件生成”这一种执行形式
- **特殊场景（导入已有文件）**：当用户在输入中明确提供了现成的绘图文件（如 `.cw`）并要求导入或绘图时，**禁止**重新生成结构化意图文件或调用 `generate_contextweave.cjs`，也**禁止**仅以文本形式输出命令，必须直接使用工具调用 `node scripts/import_contextweave_code.cjs --path "<绝对文件路径>"` 进行导入。
- 禁止只给语义分析或方案文本而不发起脚本调用
- 若脚本失败，先按错误策略重试；仅在重试后仍失败时，输出失败原因与下一步操作建议
- 路径应使用可移植定位：优先基于 Skill 根目录执行 `scripts/...`，避免依赖宿主固定绝对路径
- 推荐完成“落盘 + 执行 + 回填”闭环：先写 `input_file`，再执行脚本，最后回填结果
- 若当前环境无法执行脚本，需明确返回受限原因，并提供可执行替代步骤

## 决策流表达

1. 解析需求：识别用户想表达的核心问题、受众和信息密度
2. 结构决策：基于哲学层原则选择图组织方式并显式定义关系
3. 请求编排：将结构化意图组织为文件并写入 `input_file`
4. 基于文件生成：`node scripts/generate_contextweave.cjs --input_file "<绝对文件路径>"`
5. 结果校验：检查结构是否仍满足“论证性、关系显式、同构可读”

## 附加文件链接（Link属性）

当用户要求在图中节点关联本地文件路径（即添加 `link` 属性）时，必须采用**两步法**以保证生成质量：
1. **第一步（结构生成）**：先忽略链接要求，仅根据语义和结构化要求生成核心图结构（使用 `generate_contextweave.cjs`）。
2. **第二步（属性注入）**：在用户确认生成的结构满足预期后，发起第二次编辑调用（使用 `edit_contextweave.cjs`），明确指示“请为图中的某某节点添加对应的 `link: <绝对文件路径>` 属性”。这种做法可利用后端的精确路由，将链接修改任务交由更适合处理结构化属性的工具完成。

## 意图到命令模板

- 请求编排：将结构化意图组织为文件后，向后端发起调用 - 基于文件生成：`node scripts/generate_contextweave.cjs --input_file "<绝对文件路径>"`
- 导入已有文件：当用户提供 `.cw` 等现成文件时，直接调用：`node scripts/import_contextweave_code.cjs --path "<绝对文件路径>"`

## 参数约束与回填规则
- 初始生成的 `user_request` 长度：默认必须在 50-500 字符之间。如果需要调整限制，可通过环境变量 `CONTEXTWEAVE_MIN_REQUEST_LENGTH` 与 `CONTEXTWEAVE_MAX_REQUEST_LENGTH` 自定义。
- `input_file`：必填，且必须为绝对路径
- `input_file`：执行前必须存在且可读；不存在时禁止调用脚本
- 文件内容：必须是结构化意图结果；禁止整个文件为空或仅放零散关键词；首次生成时允许 `# CW` 段为空
- 返回回填：每轮输出必须包含本轮脚本名、执行状态、核心返回字段
- 若未完成落盘或未实际执行脚本：返回 `status: error` 且标记 `code: EXECUTION_NOT_PERFORMED`
- 若 `input_file` 不存在：返回 `status: error` 且标记 `code: INPUT_FILE_NOT_FOUND`
- 若 `input_file` 非绝对路径：返回 `status: error` 且标记 `code: INPUT_FILE_NOT_ABSOLUTE`

## 回复格式硬约束

- 回复必须是单个 JSON 对象，禁止 markdown、标题、解释性段落、代码块
- 未执行脚本时禁止返回“方案说明”，必须返回错误 JSON
- JSON 字段顺序固定为：`script`、`input_file`、`status`、`session_id`、`result`、`error`
- `status` 仅允许 `ok` 或 `error`
- `status=ok` 时必须包含 `session_id` 与 `result`；`error` 置为 `null`
- `status=error` 时必须包含 `error.code` 与 `error.message`；`session_id` 置为 `null`

### 成功 JSON 模板

`{"script":"generate_contextweave.cjs","input_file":"/abs/path/request_xxx.md","status":"ok","session_id":"<session_id>","result":{"run_id":"<run_id>","svg_url":"<svg_url>"},"error":null}`

### 失败 JSON 模板

`{"script":"generate_contextweave.cjs","input_file":"/abs/path/request_xxx.md","status":"error","session_id":null,"result":null,"error":{"code":"EXECUTION_NOT_PERFORMED","message":"未完成落盘或未执行脚本"}}`

## 文件落盘与执行规范

- 默认落盘目录：`当前工作区目录下的 .cw_skill/requests`
- 文件名规范：`request_<timestamp>.md`
- 文件最小结构：包含 `# Request` 段（描述意图）和 `# CW` 段（携带可选的初始/现有 CW 上下文；首次生成可为空）
- **Markdown 模板示例**：为保证后端能够准确解析，在生成 `input_file` 时必须严格遵循以下结构（包含两部分）：
  ````markdown
  # Request
  [在这里详细描述修改指令、绘图意图或结构说明]

  # CW
  ```cw
  ```
  ````
- **场景 A（首次生成）**：允许保留空的 `# CW` 代码块；后端会主要根据 `# Request` 生成首版 `cw_code`
- **场景 B（修改已有 CW）**：应在 `# CW` 代码块中放入当前已有的 CW 文本，例如：
  ````markdown
  # Request
  [在这里描述要如何修改现有图]

  # CW
  ```cw
  [在这里放入当前已有的 CW 文本]
  ```
  ````
- 完整执行顺序：生成结构化内容 → 写文件 → 校验路径绝对性与文件存在 → 执行脚本 → 解析 JSON → 输出回填
- 成功输出至少包含：`script`、`input_file`、`status`、`session_id`、关键产物字段，且 `input_file` 必须是实际存在路径
- 失败输出至少包含：`script`、`input_file`、`status:error`、`error.code`、`error.message`
- **默认代码落盘行为**：在执行 `generate_contextweave.cjs` 和 `edit_contextweave.cjs` 成功后，脚本会自动将后端返回的最新 `cw_code` 保存为当前执行路径下的 `<session_id>.cw` 文件，省去了用户手动导出的繁琐步骤，且避免了多个会话间的文件覆盖冲突。

## 脚本能力映射

- `scripts/generate_contextweave.cjs`：用于基于 `input_file` 执行生成；输出包含可复用的 `session_id`
- `scripts/edit_contextweave.cjs`：用于基于 `session_id` 提交修改意图
- `scripts/import_contextweave_code.cjs`：用于导入现有的 `.cw` 设计文件，使用 `--path "<文件路径>"` 传入
- `scripts/export_contextweave_code.cjs`：**必须使用此脚本**来响应用户“导出/找回/恢复某个 session_id 的 CW 代码”的请求。**严禁**直接在对话中以文本生成的方式输出代码。命令格式：`node scripts/export_contextweave_code.cjs --session_id "<session_id>"`
- `scripts/cw_client.cjs`：用于统一后端请求与响应适配；承载鉴权、错误归一和返回结构解析

## 错误策略
- `INVALID_REQUEST_LENGTH`：检查请求字数是否在允许范围内（默认 50-500 字符），调整请求的详细程度后重试
- `MISSING_SESSION_ID`：视为不可继续迭代，立即重试当前请求并校验返回
- `SESSION_INVALID_OR_EXPIRED`：先重建会话，再回放当前意图
- `AUTH_ERROR`：校验密钥与配置后重试
- `PAYMENT_REQUIRED`：完成额度恢复后重试
- `API_ERROR`：检查网络与服务状态后重试

## 输入约束

- `input_file`：来自当前回合请求编排产物，必须为绝对路径
- 文件内容：需要体现结构化意图与关系，不使用空文件或纯术语清单
- 首次生成时允许 `# CW` 段为空；修改已有图时应在该段提供现有 CW 文本
- 其他请求参数：按脚本参数要求透传，不在 Skill 层定义渲染实现细节

## 安全边界与隐私声明

- 后端地址与数据路由：本 Skill 在运行时会读取 `CONTEXTWEAVE_EDITOR_PROTOCOL`，若未显式设置，将使用内置默认值 `trae`。代码会将带有 API Key 和绘图数据的请求发送至内置的官方服务器（`https://pptx.chenxitech.site`）。用户明确知悉其数据会被路由至该默认配置的地址。
- 凭据获取：凭据优先读取环境变量 `CONTEXTWEAVE_MCP_API_KEY`，若未显式设置，将使用内置的默认匿名凭据。不得通过扫描本地目录自动发现密钥。
- 文件访问：只读取当前任务明确指定的输入文件；禁止遍历用户目录、工作区或无关配置文件；所有文件路径必须是绝对路径且被严格限制在当前执行工作区目录范围内。
- 数据最小化：仅向后端发送完成当前绘图请求所必需的数据，禁止附带无关本地文件内容。

## Scenarios (多视图/链路拆分)

### 场景抽象与单一数据源
- 当用户要求“区分不同业务链路展示”或“在同一架构上高亮不同流程”（例如区分 Query 链路和 Callback 链路）时，**必须** 使用 ContextWeave/D2 的 `scenarios` 原生语法。
- **禁止** 复制或拼接多个完整的文件。应首先定义一个完整的“基础架构图（Base Layer）”，然后在同一个代码块底部使用 `scenarios` 定义各个视图的增量覆盖。

### 场景构建规范
- 基础层必须包含所有节点和连线。
- 在 `scenarios: {}` 块中，针对每个独立链路定义一个子块（如 `QueryFlow: {}`）。
- 在场景子块中，通过修改无关组件的透明度（如 `style.opacity: 0.2`）进行淡化，并通过修改目标链路的连线样式（如 `stroke: red, stroke-width: 4`）进行高亮。
- 场景定义完成后，可以告知用户后续可通过指定 ScenarioName 提取特定视图。
