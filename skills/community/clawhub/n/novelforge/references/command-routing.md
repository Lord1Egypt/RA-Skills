# Pipeline & Intent Routing

自然语言意图统一映射到标准作业程序 (SOP 流水线) 的自动流转与安全控制。用户无需执行各个底层的单步指令。

| 用户自然语言意图 | 流水线操作 | 行为描述 |
| --- | --- | --- |
| 写下一章 / 写第 X 章 / 创作本章 | `pipeline advance <root> [id]` | 自动检查并推进流水线（蓝图校验、上下文编译、草稿登记、质检、结算），遇到缺项安全挂起并提示 |
| 暂停 / 先别写正文 / 停在蓝图 | `pipeline advance --stop-at <phase>` 或 `pipeline interrupt` | 安全中断在指定阶段（如 `BLUEPRINT_VALID` 或 `CONTEXT_LOCKED`），保留现场与哈希 |
| 继续 / 恢复 / 接着写 | `pipeline resume <root> [id]` | 自动校验已有产物哈希，无缝从中断点继续推进下游流水线 |
| 当前进度 / 查看状态 / 怎么停了 | `pipeline status <root> [id]` | 返回当前所处阶段、已完成环节、当前待办与中断/阻塞原因 |
| 新书立项 / 故事筑基 / 设计世界观与主线 | `story genesis` / `project init` | 运行故事筑基 SOP，完成题材对齐、规模承载力评估、总纲与初始世界观构建 |
| 评估故事规模 / 测算篇幅承载力 | `project assess-capacity` | 量化评估动力源深度、体系纵深与阵营复杂度，双向诊断小马拉大车或大马拉小车风险 |
| 初始化新书骨架 | `pipeline advance <root>` 或 `project init` | 自动初始化项目骨架与规模画像，就绪后进入蓝图设计阶段 |
| 切换/安装引擎 | `engine install` / `engine use` | 独立扩展能力，安装或切换叙事引擎 |
| 参考文章或小说造引擎 / 提炼叙事引擎 | `engine distill <source>` | 提炼因果心智模型与场景技法卡，自动打包生成合规叙事引擎 |

章节 ID 为稳定的项目标识符。当用户说「下一章」时，流水线优先从 `.novelforge/state/chapters/` 中寻找最新的交付状态，自动推算目标 ID。

当流水线因缺失前置事实或依赖而中断时，Agent 必须提示用户登记缺失的依赖 ID，并在登记后恢复流水线。
