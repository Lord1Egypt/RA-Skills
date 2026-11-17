# 多 Agent 长篇写作与逐块审稿

这条流程从已确认的大纲开始生成长文，适用于小说、报道、论文和报告。
已有成稿的分块审查继续使用 `chunk-audit`。程序保存任务依赖、输入快照、草稿和回执；
实际写作与语义判断由宿主的模型和 Agent 完成。

## 五种角色

| 角色 | 工作 | 放行条件 |
| --- | --- | --- |
| 大纲检查 Agent | 检查每项大纲与设定、证据和前提是否一致。 | 逐项引用大纲；未解决的问题会阻止规划。 |
| 切块 Agent | 安排字数、内容职责、共同文风和各块起止状态。 | 所有大纲项均有归属，依赖不能成环。 |
| 每块写作 Agent | 写完整正文，并交接累计事实状态。 | 长度在目标的 80%–120% 内；不能漏掉前块已有的事实键。 |
| 每块审查 Agent | 逐段检查大纲遵循、上下文、人物口吻和套话等问题。 | 身份不同于写作者，引用每段证据，并核对当前草稿摘要值。 |
| 主 Agent / 统稿 Agent | 检查每一对相邻块，以及全局大纲、状态和文风。 | 所有块和相邻边界都有有效回执后才能组装。 |

新闻、论文和严肃报告额外检查来源、数字、归因和不确定性；小说才检查相应的人际动作承接、
空间连续性和场景收尾。共同文风契约控制语言和语域，用户明确提供的参考稿可用于校准声音。
事实资料与文风样本分别存放，不能从样本里借用事实。

## 六万字、每块五千字

```powershell
human-writing-skills plan-writing --outline outline.md --context ledger.md --style fiction --target-length 60000 --chunk-size 5000 --output-dir book-writing
human-writing-skills writing-tasks --package-dir book-writing
human-writing-skills claim-writing --package-dir book-writing --task-id outline-check --agent-id outline-checker
```

这里会建立 12 个写作任务、12 个逐块审稿任务，以及大纲检查、分块规划和最终统稿三个共享任务。
依次就绪的 ID 为 `outline-check`、`chunk-plan`、`write-0001` / `review-0001` 等，最后是
`continuity`。认领返回完整 `content` 和 `result_schema`；宿主把它们原样交给实际子 Agent。
收到真实 JSON 结果后，在结果中原样保留当前 `claim_token`，以同一身份提交，再查看下一批就绪任务：

```powershell
human-writing-skills submit-writing --package-dir book-writing --task-id outline-check --agent-id outline-checker --result outline-check-result.json
human-writing-skills writing-tasks --package-dir book-writing
human-writing-skills verify-writing --package-dir book-writing
human-writing-skills assemble-writing --package-dir book-writing --output manuscript.md
```

最后两步只有在所需角色全部通过后才会成功。组装按原定顺序连接正文，保留段落分隔，
不擅自添加章节小标题，也不改写已批准的文本；输出必须是新文件。

默认 `characters` 按非空白 Unicode 字符计数，包含标点；`--length-unit words` 则按单词计数，
适用于按词分隔的语言。这些都不是 token 数，六万英文单词与六万中文字符的体量不同。
每块长度应适应实际模型输出上限，不能靠重复和灌水凑足目标。

## 怎样并行又不丢上下文

默认 `--execution-mode sequential`：上一块通过独立编辑后，下一位写作者才拿到已确认的
状态和结尾。适合动作、人物关系或剧情具有前后因果的小说。不同块可以由不同 Agent 完成，
各自只接收本块所需内容。

用户明确要求并行、且内容能够约定起止状态时，使用 `--execution-mode contract`。
切块结果必须给出入口/出口状态，并为每块声明前序依赖；没有依赖的后续块还必须明确
`independent: true`。程序核对这些声明及 `--max-parallel` 上限，默认同时最多认领四个任务。
是否真的独立仍需规划者判断，不能为了提速就把连续剧情谎报为独立。12 块不等于必须同时
启动 12 个进程；报告中职责独立的章节通常更适合并行。

每块交接的 `state` 使用稳定键保存已知事实，前块已有的键必须保留。值发生变化时，
`state_changes` 必须写清前后值，并引用本块正文中实际发生变化的句子。
它能发现未记录的换位、道具易主或状态遗漏；引用中的事件在物理和逻辑上是否成立，仍由编辑判断。
并行分支对同一事实有不同交接值时，`state_changes.before` 必须列出全部冲突值，并给出正文中
解决冲突的证据。前块待承接事项须继续保留，或在 `resolved_threads` 中引用解决它的原句，不能悄悄删掉。

## 返修与中断恢复

逐块编辑或最终统稿提出 `revise` 后，对应写作任务会重新开放，依赖它的后续草稿与批准失效。
独立分支可以保留已通过结果。每个受影响块允许两轮返修，再次要求返修会阻塞该块，需调整
大纲或任务说明后建立新工作包。初始大纲存在矛盾时也应先修正输入，不能让写作者默默补设定。

认领归属于稳定的 `agent_id`；有效期内其他 Agent 不能抢走，原 Agent 可以继续。
认领一小时后到期，允许中断任务被重新接手。每次结果都必须匹配当前 `claim_token`，过期认领或
旧轮次的迟到结果会被拒绝。返修提示引用完整审稿报告的路径，避免为每位写作者重复塞入全局报告。
结果按版本保存并带摘要校验，原始快照或结果文件
被改动时旧批准失效。不要手动改工作包状态来绕过放行条件。

主 Agent 分页读取 `continuity-index.json`，其中包含各块当前摘要值、状态、待承接事项和
首尾摘录。使用 `read_project_context` 的 `offset` / `next_offset`，直到后者为 null；
摘录不足以支持判断时，再读其中引用的完整草稿结果。无需每个 Agent 都携带整本小说。
角色提示有 60,000 字符上限；逐块审稿材料超限时保存为完整分页文件，审查者须读完全部页面并
提交每段回执。其他角色上下文超限会明确报错，提交结果仍有传输大小限制。
使用精简、已确认的公共账本；特别大的工程按卷拆分。事实来源和风格参考只装载本块被分配的部分。

## Skill 与 DSH 插件

MCP 对应六个工具：`plan_long_form_writing`、`list_writing_tasks`、`claim_writing_task`、
`submit_writing_result`、`verify_writing_project`、`assemble_writing_project`。
它们的读写路径都限制在配置的工作区根目录中。

纯 Skill 的入口按需加载 `skills/long-form-writing.md`。DSH 在请求长文或明确多 Agent 写作时，
才加载 `writing__human-writing__longform_guidance` 返回的详细流程，工具名随 `serverName` 变化。
实际并行还要求 DSH 提供子 Agent 服务、提供者、委派工具和模型驱动，详见
[DSH 插件说明](../plugins/deepseek-harness/README.zh-CN.md)。缺少执行器时可以顺序进行多个
角色轮次，但必须如实说明并非独立 Agent。测试验证调度、存储和放行条件，不能据此保证
文学质量或检测器评分。
