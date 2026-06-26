# Hopola Skill 规划方案（Plan）

## 1. Summary
- 目标：创建一个名为 `Hopola` 的 Skill，支持「网页搜索（基于 web-access）→ 图片生成（通过你提供的 MCP）→ 结果上传（通过你提供的接口）→ Markdown 返回」。
- 交付形态：先交付“可运行骨架”，确保流程与扩展点完整；待你补充 MCP 与上传接口细节后可快速切换为完整可执行版。
- 触发方式：同时支持“单入口全流程”和“分阶段单独调用”。

## 2. Current State Analysis
- 当前工作目录下未发现现有项目文件与技能目录，需要从零创建 Skill 结构。
- 已确认需求关键决策：
  - Skill 名称：`Hopola`
  - 运行平台：同时兼容 Trae / Claude Code 场景
  - 搜索能力来源：`https://github.com/eze-is/web-access`
  - 图片生成：使用你后续提供的 MCP
  - 结果上传：使用你后续提供的上传接口
  - 最终输出：Markdown 报告
  - 交付策略：先做可运行骨架

## 3. Proposed Changes

### 文件 1：`/Users/youpengtu/Hopola-Skills/.trae/skills/Hopola/SKILL.md`
- 做什么：
  - 新建 Skill 元数据（name/description）与完整说明。
  - 写清调用时机：当用户需要“联网检索 + 生成图片 + 上传结果 + 输出报告”时触发。
  - 定义两种执行模式：
    - 模式 A：全流程一键执行（Search → Generate → Upload → Report）
    - 模式 B：阶段化执行（仅搜索 / 仅生图 / 仅上传 / 仅报告）
  - 预留配置节：
    - `IMAGE_MCP_TOOL`、`IMAGE_MCP_ARGS_SCHEMA`
    - `UPLOAD_ENDPOINT`、`UPLOAD_AUTH_MODE`、`UPLOAD_PAYLOAD_SCHEMA`
  - 定义标准输入输出契约（草案）：
    - 输入：查询词、图片风格/尺寸、上传开关、报告偏好
    - 输出：Markdown，包含搜索摘要、生成结果、上传结果、失败重试说明
- 为什么：
  - 先把“能力边界 + 调用协议 + 失败策略”固化，后续替换 MCP/API 只需改配置，不改主流程。
- 怎么做：
  - 参考 web-access 的能力边界与调度理念，写成可直接执行的步骤指令与回退策略。

### 文件 2：`/Users/youpengtu/Hopola-Skills/.trae/skills/Hopola/examples.md`
- 做什么：
  - 新建示例文档，提供全流程与分阶段调用样例（中文）。
  - 给出“占位参数版”示例，标注你后续需要提供的 MCP 与上传接口字段。
- 为什么：
  - 降低你后续对接成本，便于快速验证 Skill 行为。
- 怎么做：
  - 每个示例包含：输入示例、预期 Markdown 输出片段、错误场景示例。

### 文件 3：`/Users/youpengtu/Hopola-Skills/.trae/skills/Hopola/config.template.json`
- 做什么：
  - 新建配置模板，集中管理可替换项（MCP 工具名、参数映射、上传接口 URL、鉴权字段、超时与重试）。
- 为什么：
  - 将环境差异从指令层剥离，便于跨平台复用。
- 怎么做：
  - 用清晰键名与默认空值，占位等待你提供真实参数。

## 4. Assumptions & Decisions
- 决策：先实现“可运行骨架”，不绑定任何未给定的真实 MCP 名称与上传 URL。
- 假设：你将在下一轮提供图片 MCP 的工具名、参数格式，以及上传接口字段与鉴权方式。
- 决策：Markdown 作为唯一对外结果格式；内部状态可保留结构化字段供拼装。
- 决策：失败处理采用“阶段内重试 + 阶段间可降级 + 报告中显式告警”。
- 非目标（当前阶段不做）：
  - 不接入具体第三方模型密钥
  - 不写死任何私有接口地址
  - 不做部署与发布脚本

## 5. Verification Steps
- 结构校验：
  - 确认目录存在：`.trae/skills/Hopola/`
  - 确认文件存在：`SKILL.md`、`examples.md`、`config.template.json`
- 内容校验：
  - `SKILL.md` frontmatter 合法，`name` 与目录一致，`description` 清晰说明“做什么 + 何时调用”。
  - 全流程与分阶段两种模式均有明确输入、输出、错误处理说明。
  - Markdown 输出模板包含四段：搜索结果、图片生成结果、上传结果、最终结论。
- 可用性校验：
  - 用“占位参数”进行一次文档级走查，确保后续只需替换 MCP/API 配置即可执行。

## 6. Next Inputs Needed From You（执行前补充）
- 图片 MCP：工具名称、必填参数、返回字段（尤其是图片 URL/二进制标识）。
- 上传接口：请求方法、URL、鉴权方式、请求体结构、成功/失败响应样例。
- 是否需要在报告中附加原始检索链接清单与失败重试日志明细。
