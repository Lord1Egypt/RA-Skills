# DSH 人类写作与去 AI 味插件

<p align="center"><img src="../../assets/logo.png" width="280" alt="Human Writing：钢笔手写笔迹与终端代码"></p>

> 让 AI 写作更自然：支持多语言润色、长文分块协作与上下文一致性审查。

用于在 DeepSeek Harness 中生成小说、论文、报告、议论文和自媒体内容，并润色已有草稿。
插件在生成前提供精简写作协议，挂载文体提示编译、套话扫描、原意保真、声音保留和
长文分块审查工具。文字由当前 DSH 代理完成，插件不会额外调用模型。

## 安装

需要 Python 3.9+，以及有 tools / systemPrompt 服务的 DSH profile。
已用官方 0.2.1-rc.2 / 0.2.2-rc.3 包完成集成测试；声明的兼容范围还包括 0.2.0-rc.2 和
0.2.1 alpha 系列，其他版本尚未实测。Node 要求 ^22.19.0 或 >=24.0.0。
安装包自带本项目 Python 核心和写作模块，不需要额外 pip 安装 human-writing-skills。

```powershell
dsh plugin --profile web add https://github.com/whh110112/human-writing-skills/releases/download/dsh-v0.3.1/dsh-advanced-human-writing.tgz
```

桌面版把 `web` 换成 `desktop`，安装后重启对应 profile。如果解释器不叫 `python`，
在启动 DSH 前把 `PYTHON` 设置为 Python 可执行文件路径。
也可安装仓库根目录的固定标签：

```powershell
dsh plugin --profile web add github:whh110112/human-writing-skills#dsh-v0.3.1
```

真正可分发的 package.json 在仓库根目录；本适配子目录为 private，不单独发布。
当前分发渠道为 GitHub Release，不声称已经发布 npm 包。

## 在 DSH 中使用

- 小说：“使用 Human Writing 续写这个重逢场景，保留人物设定，让对白有回应，不要追加感悟式结尾。”
- 论文：“根据这些观察写结果段落，保留不确定性，不编造引文、数据或显著性检验。”
- 报告：“写本周进度报告，交代现状、阻碍、责任人与下一步，区分计划和已完成事项。”
- 润色：“保留我的原意和口吻，修改套话与重复结构，不添加不存在的经历。”
- 诊断：“只指出这篇文章的问题，不代写。”

插件向模型说明：仅在用户请求写作、改写或审稿时应用规则，实质写作前先调用
`mcp__human-writing__compile_generation_prompt`，根据返回的文体协议生产文字；
需要时调用 lint 和保真工具再交付。生成前约束空泛开头、机械对比、冗余解释、
装饰性细节、翻译腔和无意义升华。允许正式文风、直接情绪表达和必要重复。
规则依赖模型遵循，不能保证所有模型每次都执行，也不保证检测器分数。

事实材料用工作区相对路径 `source_paths`，文风样本用 `reference_paths`，两者不能混用。
工具拒绝越出工作区的路径；小说不会自动开启事实文档来源审查。
输入示例见 [examples](examples)，无 API 密钥的真实集成过程见 [DEMO.md](DEMO.md)。

## 长文多角色写作

当请求输出不少于 10,000 字符或单词，或明确要求多代理长文写作时，系统提示引导调用
`writing__human-writing__longform_guidance`，按需加载详细协议。阈值针对输出量，
不是输入材料长度；普通写作和长文审查不因此自动进入创作流程。工具名跟随 `serverName`。
关闭 `generationGuidance` 仅移除系统提示，仍保留按需协议工具和 MCP 工具。

例如：“根据 outline.md，用多代理写作完成 20,000 单词，审稿后保存为 manuscript.md。”
先保存双方确认的大纲，再用 [longform.json](examples/longform.json) 的参数调用
`mcp__human-writing__plan_long_form_writing`。`length_unit` 明确区分字符与单词。

执行顺序为：大纲检查、分块规划、每块作者、每块独立编辑、最终连续性审查、组装。
宿主通过 `list_writing_tasks` 查就绪任务，用 `claim_writing_task` 认领，必须原样传递
返回的完整角色提示及提交 schema。用相同 `agent_id` 和实际结构化 `result` 对象调用
`submit_writing_result`；作者与编辑使用不同身份，返修保留原身份。每次提交后重新查看
就绪状态；返修有次数上限，前序未批准不能解锁后序，不能篡改状态或伪造批准。
任务 ID 为 `outline-check`、`chunk-plan`、`write-0001` / `review-0001` 成对任务，
最后为 `continuity`；认领返回 `content` 与 `result_schema`。编辑身份必须不同于
对应作者，最终审查者必须不同于全部作者。顺序模式须上一块编辑批准后才能开始下一块作者任务。
认领同时返回 `claim_token`，并填入 `result_schema.claim_token`。必须原样转发完整提示、
完整结果 schema 和令牌，提交时把当前令牌复制到 `result.claim_token`；将令牌与子代理 ID、
任务 ID 和 `agent_id` 一起记录。同一代理恢复有效认领时令牌不变，重新认领或返修的新尝试
使用新令牌。旧尝试迟到的结果必须丢弃，不能换上新令牌后提交，也不能用于完成新尝试。
只有 `execution_mode: "contract"` 且独立块有明确、已批准的入口和出口契约时，
才能在 `max_parallel` 与宿主容量范围内并行就绪任务；默认顺序模式不能并行。
`max_parallel` 限制同时认领数，不保证进程并发数。60,000 / 5,000 表示十二个写作任务
及其编辑任务，不表示保证同时启动十二个代理进程；契约模式也必须遵守块间依赖。
全部角色通过后，先成功调用 `verify_writing_project`，再调用 `assemble_writing_project`。

### DSH 原生委派与降级

已检查官方 `@deepseek-ai/dsh-subagent` 与 `@deepseek-ai/dsh-tool-subagent`
0.2.1-rc.2 发布包文档和实现。宿主原生委派需要同时加载服务、提供者和委派工具：

```yaml
- name: '@deepseek-ai/dsh-subagent'
- name: '@deepseek-ai/dsh-subagent-spawn-in-process'
- name: '@deepseek-ai/dsh-tool-subagent'
  config:
    provider: spawn
    toolName: subagent
```

仍需宿主已有的代理驱动和模型配置。本插件不代装或配置提供者。默认 `subagent`
工具接收 `description`、`prompt`，改名时以宿主实际 schema 为准。启动仅返回子代理 ID，
不代表任务完成；宿主把子代理 ID 映射到认领身份，等待完成通知后原样提交结构化结果。
不能假设新子代理继承父对话，必须提供完整认领提示及 schema；权限、深度和容量限制仍有效。

底层 `ctx.agents.create()` 也需要已注册的代理驱动。仅有 MCP 或代理注册表不能启动子代理。
若无可用执行器或委派被拒绝，必须说明限制，降级为顺序执行的不同角色轮次；明确其不是
独立代理，不冒充并发。作者与编辑仍分开执行，不静默更换已认领身份，不伪造子代理 ID。

无密钥测试使用真实 Cordis 与 MCP，但未加载代理驱动和子代理提供者。测试验证按需协议、
六个真实写作工具的 schema、仅工具模式和卸载清理；不代表原生子代理执行或模型遵循已经实测。
真实 MCP 冒烟测试还验证两块规划、大纲批准门槛、完整认领提示与 schema、提交身份检查，
以及尚未完成时拒绝组装。
还验证有效认领恢复时令牌不变、缺少或过期令牌被拒，以及编辑要求返修后产生新令牌，
第一轮作者的迟到结果无法完成新的认领。

## 配置与权限

智能体模式先调用 `writing__human-writing__agent_capabilities`，获得当前调用智能体
可见的委派工具及参数。宿主使用其他工具名时设置 `delegationToolName`。
每次调用重新检查，支持提供者重载；不会启动代理、代装驱动、绕过工具限制或更改模型。
完整编排协议仍按需加载。认领返回有效期，超大材料分页读取，过期认领明确标识；
严肃文体审稿 schema 包含来源检查，小说不自动加载。

`root` 默认 DSH 启动工作目录，建议设置为写作项目目录；`pythonCommand` 默认
PYTHON 或 python；`serverName` 默认 human-writing；`generationGuidance: false`
可关闭系统提示，只保留工具；`toolCallTimeoutMs` 默认 60000。

启动本地 Python stdio 进程，隔离模式优先加载包内核心，避免项目文件冒充核心。
工具按调用读取文字和工作区资料，长文工具按调用写入审查包，不自动上传稿件、
不开放网络端口、不自动安装 Python 依赖，也不自动发布生成文章。
文本进入当前 DSH 模型上下文时，仍遵循用户现有模型供应商的隐私设置。

分类：Skills / Tools & Capabilities。许可证：MIT。社区插件，非 DeepSeek 官方产品。
可安装版本发布与市场审核收录是两个独立步骤。
