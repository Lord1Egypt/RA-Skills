# Harness Check 的产品定位与对标边界

## 一句话定位

DeepSeek Harness 负责把 Agent 跑起来；`hekouwang-harness-check-skill` 负责回答：这个 Harness 的规则、权限、验证、恢复和交付证据，是否足以让别人相信它真的可用。

产品名可以使用 **Harness Integrity Score**，中文名为“Harness 完整性评分器”。它不是另一个 Agent Runtime，也不是某个模型的 SDK，而是运行时之上的独立验收层。

### 产品展示名

当前推荐产品展示名为 **hekouwang Harness Doctor**，简称 **Harness Doctor**：

- `Doctor` 直接对应“体检、诊断、处方、复查”的产品闭环，比 `Check` 更有记忆点，也能承载网页、CLI 和 GIF 演示；
- `hekouwang` 把产品和你的内容工程实践绑定，形成独立于某个模型或宿主的品牌来源；
- 不使用 `Audit`，避免与 ContextOS 的运行时审计叙事重叠；
- 不把 `Proof` 作为主名：GitHub 上已经存在与 DeepSeek Harness 相关的同名 `fieldnote-ops/harnessproof` 项目，容易造成品牌与搜索混淆；
- 仓库名、Skill 名和安装入口继续保留 `hekouwang-harness-check-skill`，展示名与技术包名解耦；未来 CLI 可使用 `hekouwang-harness-doctor`。

备选名为 `HarnessLedger`（证据台账方向）和 `BoundaryProof`（跨状态/宿主边界方向）。

## 与 DeepSeek Harness 的关系

DeepSeek Harness 的公开架构主线是 Cordis 插件树：模型适配器、工具注册、会话日志和 Agent Loop 都可以通过插件和 Profile 组合；它的 README 也明确将项目定位为 developer preview，并提醒兼容性会快速变化。参考：[DeepSeek Harness README](https://github.com/deepseek-ai/deepseek-harness/blob/master/README.md)、[DeepSeek Harness architecture](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md)。

这是一种“构建和运行 Harness”的产品。我们的核心对象则是一个已经存在的 Harness 仓库及其运行证据：它有没有唯一验证入口、CI 是否复现本地门禁、Hook 是否模型外执行、正反例是否真的拦截、恢复状态是否可重放、宿主烟测和人工验收是否被诚实区分。

| 对比轴 | DeepSeek Harness 的主问题 | Harness Check 的主问题 |
| --- | --- | --- |
| 首要动作 | 运行 Agent、组合插件、挂载 Profile | 检查一个 Harness 仓库是否值得信任 |
| 核心对象 | Plugin tree、Agent loop、Session log | 规则、Hook、CI、契约、回归、证据链 |
| 主要输出 | Web / headless Agent 运行结果 | 0–100 分、成熟度、硬门槛、置信度、修复队列 |
| 证据来源 | 运行时自己的测试、日志和快照 | 独立扫描 + 目标仓库真实退出码 + 文件/行号证据 |
| 失败语义 | Agent 或插件运行失败 | 缺验证、缺反例、缺安全边界会触发硬上限，不能用文档数量掩盖 |
| 宿主边界 | 提供 Claude Code / Codex 等桥接能力 | 验证宿主配置存在，并把真实宿主触发标为 `unknown`，不冒充通过 |
| 适用对象 | 主要是 DeepSeek Harness 运行时 | DeepSeek、Claude、Codex、Cursor、CodeBuddy 以及自定义 Agent Harness |
| 内容工作流 | 通用 Agent 运行能力 | 可挂接内容 Agent 的发布状态、来源、渠道合同、视觉和人工验收 Profile |

## 必须坚持的差异化

### 1. 从“能力展示”转向“可信度证明”

不要与 DeepSeek 比谁的插件更多、界面更酷、Agent 跑得更快。展示一个 Harness 能做什么很容易；展示它在失败时会不会停、在换宿主后是否仍然成立、在提交前后证据是否一致，才是检测器的价值。

### 2. 评分不是测试计数

评分器使用 12 个治理维度、硬上限、置信度和成熟度等级。没有反例回归、没有模型外安全边界或没有完成证据契约时，即使 README 很长、测试数量很多，也不能获得对应成熟度。

### 3. “No artifact, no pass”

每个重要结论都需要至少一个可定位证据：仓库相对路径、行号、真实命令、退出码或结构化人工记录。关键词只作为发现线索，自动降权，不能单独把一个维度刷满。

### 4. 评分对象跨宿主、跨状态、跨时间

`working-tree`、`staged`、`ci` 是不同状态，不允许互相冒充。四端宿主矩阵只说明配置存在；没有真实触发记录就保持 `unknown`。后续再加 baseline/diff，把“这次变好还是变坏”纳入报告。

### 5. 垂直领域治理

通用 Harness 只解决运行时和工程控制面；内容 Agent 还要验证已发布门、来源卡、渠道内容合同、生成物边界、人工视觉验收和平台外部副作用。`content-agent` Profile 是我们的纵向壁垒，应该建立在通用评分器之上，而不是把品牌规则硬编码进通用 Skill。

## 对外演示顺序

网页和 GIF 不要从“安装 Skill”开始，而从一个真实仓库的证据变化开始：

1. 输入一个 Harness 仓库；
2. 扫出当前分数、置信度和硬门槛；
3. 打开某个维度，看到文件/行号证据；
4. 展示一个反例被阻断、一个真实退出码为非零的情况；
5. 切换到 CI 或宿主矩阵，显示哪些仍然是 `unknown`；
6. 修复后重新扫描，展示分数变化和可复核报告。

这样用户看到的不是“又一个 Agent Demo”，而是一台可以给 Agent Harness 做体检、验收和回归的仪器。

## 不能声称的内容

- 不声称 DeepSeek Harness 没有测试、安全或恢复能力；它的公开仓库明确展示了这些工程能力。
- 不把本 Skill 的静态分数说成运行时质量证明；真实宿主和人工验收仍然必须单独留证。
- 不把两个产品的分数直接排名；它们的主任务不同。可以比较的是同一评分器对不同仓库暴露出的治理证据缺口。
