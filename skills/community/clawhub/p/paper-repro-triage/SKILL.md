---
name: paper-repro-triage
description: 中文论文复现执行工作流。用于用户上传或提供深度学习、机器学习、LLM、CV、NLP、多模态、数据集、benchmark、prompt 工程或 agent 论文的 PDF、arXiv 链接、论文主页、项目页、标题摘要或源码线索，并要求判断可复现性、搜索官方代码、检查本地源码、追踪数据集论文源码、定位数据处理代码、自动 clone 仓库，或在无线上/本地源码但具备复现条件时生成符合常见 PyTorch 开源项目直觉的复现工程。最终写入 Markdown 报告，聊天只返回极简中文摘要。
---

# 论文复现初筛、源码溯源与复现工程生成

## 总原则

本技能用于把论文分析从“聊天式建议”升级为“面向复现的执行工作流”。回答必须使用中文。除非工具权限、网络、审批或用户环境阻止，否则不要只告诉用户去执行命令；应优先使用可用工具完成可执行动作。

每次触发后，聊天回复第一行必须输出：

```text
[paper-repro-triage active]
```

详细结果必须写入 Markdown 文件，聊天只返回极简摘要。

## 强制行为

1. **详细结果写入 Markdown**：默认写到当前 agent workspace 下的 `paper-repro-workspace/<paper-slug>/repro-report.md`。
2. **聊天内容极简**：只输出报告路径、主论文源码状态、数据集源码状态、复现工程状态、是否需要复现、是否能复现、核心原因。
3. **不要输出“下一步建议”作为流程终点**：如果当前流程能继续执行，就继续执行；聊天摘要和报告末尾只写“未完成项/人工确认项”。
4. **先找源码，再谈复现**：必须按“线上官方代码 → 本地主论文源码 → 数据集论文源码 → 无主论文源码复现工程”的顺序执行。不能因为 GitHub 没搜到就立即从零复现。
5. **数据集源码或 baseline 源码不能替代主论文源码**：如果只找到数据集相关源码、baseline 代码、第三方实现或旧方法代码，必须继续判断是否要生成主论文复现工程。
6. **遇到代码仓库优先自动 clone**：主论文官方仓库、数据集论文官方仓库、项目页仓库都应优先 clone 到 workspace；但 clone 前必须先查本地是否已有相关源码。
7. **重复目录跳过 clone**：如果 clone 目标路径下已有同名源码文件夹，不要再次 clone，不要自动 `git pull`，不要覆盖，不要改用时间戳目录；应读取现有目录做只读检查，并在报告与聊天摘要中写明 `已存在，跳过 clone`。
8. **遇到数据集必须做源码溯源**：不用下载数据集论文 PDF，也不用下载数据集本体；只搜索数据集原论文、项目页、arXiv 摘要页、Papers with Code、GitHub/GitLab/Hugging Face 线索，判断是否有官方源码、处理脚本或 benchmark 代码。
9. **必须定位数据处理代码**：对主论文源码、baseline 源码和数据集相关源码，都要定位数据加载、预处理、划分、特征抽取、标注解析、benchmark 构建等代码位置，并写入报告。
10. **无主论文源码时必须尝试生成复现工程**：当线上没有官方源码、本地没有主论文源码，且论文证据支持“可以直接复现”或“部分可复现”时，必须生成 PyTorch 复现工程；不能只写方案。
11. **生成工程要符合常见开源直觉**：默认采用“根目录入口 + 四个代码目录 + 一个复现文档目录”的简洁 PyTorch 结构：根目录保留 `main.py`、`config.py`、`run.py`；代码放入 `data/`、`models/`、`engine/`、`utils/`；`requirements.txt`、`paper-spec.yaml`、`evidence-map.md`、`repro-notes.md` 统一放入 `repro-docs/`。该结构是最低基本盘，可按论文需要扩展，但不要默认生成 `configs/` 多 YAML 目录、独立 `losses/` 目录、`scripts/` 训练脚本或 `.sh` 文件。
12. **不要伪造复现结果**：可以生成代码和 smoke check，但不能声称已经复现论文结果。论文未给出的超参数、模块或处理步骤必须标注为 `ASSUMPTION` 或 `TODO`。
13. **主论文源码存在时必须停在代码导读阶段**：如果已找到、已 clone、已跳过 clone 或本地已存在主论文官方/高度可信源码，本次技能流程的终点是“仓库导读 + 数据处理代码定位 + 写入报告 + 极简摘要”。不得继续修复源码、配置数据目录、安装依赖、下载数据、运行训练、运行评测或执行 inference。
14. **“复现”默认表示复现分析与准备**：用户只说“复现这篇论文”“重新跑一遍”“处理这篇论文”时，不代表允许训练；只有用户明确说“运行训练/开始训练/跑通训练/执行评测/下载数据/修复代码并运行”，才进入运行类任务。
15. **运行类任务不属于本技能自动阶段**：即使 exec 权限是 full/ask=off，本技能也不能自动安装依赖、下载数据、改官方代码或跑训练。

## 输入

接受以下输入：论文 PDF、arXiv 链接、论文主页链接、项目页链接、论文标题/摘要/正文片段、GitHub/GitLab 链接，以及“判断是否值得复现”“找代码”“自动 clone”“读仓库”“整理实验配置”“查数据集论文源码”“生成复现工程”“写 md 报告”等请求。

## 必须优先使用的工具

根据当前 OpenClaw 环境中可用的工具执行：

1. 使用 PDF 工具或文件读取能力抽取论文正文、附录、脚注、表格、图注和参考文献。
2. 使用 web/search/fetch 类工具读取 arXiv 页面、项目页、论文中出现的外部链接、数据集原论文页面和公开代码页面。
3. 使用 exec/shell 工具执行仓库和文件相关命令，例如 `git clone`、`python scripts/bootstrap_repo.py`、`python scripts/find_local_code.py`、`python scripts/inspect_repo_data_processing.py`、`python scripts/build_paper_spec.py`、`python scripts/scaffold_repro_project.py`、`python scripts/inspect_repro_project.py`、`dir`、`find`、写入 `.md` 文件。
4. Windows cmd 环境优先使用 Python 脚本：`python ...`；如果 `python` 不可用，尝试 `py ...`。
5. 不使用 `.sh` 作为默认路径；本技能不生成 `.sh` 训练脚本。
6. 如果 exec 不可用、被拒绝、网络失败或 Python 不可用，必须在报告中说明失败原因和退化路径。

## 工作区约定

1. 优先在当前 agent workspace 下创建 `paper-repro-workspace/`。
2. 对每篇主论文创建安全目录名：`paper-repro-workspace/<paper-slug>/`。
3. 详细报告：`paper-repro-workspace/<paper-slug>/repro-report.md`。
4. 主论文代码：`paper-repro-workspace/<paper-slug>/main-code/<repo-name>/`。
5. 数据集论文或数据集项目代码：`paper-repro-workspace/<paper-slug>/dataset-code/<dataset-slug>/<repo-name>/`。
6. 本地手动放置源码可位于：`paper-repro-workspace/<paper-slug>/local-code/`。
7. 无代码生成工程目录不得固定为 `repro-implementation`。必须根据论文框架、方法、模型或任务名生成：`paper-repro-workspace/<paper-slug>/<framework-or-method-slug>-reproduction/`。如果只能做 baseline，目录名必须包含 `baseline`。
8. 不要在用户系统随机目录中 clone 或生成代码，不要覆盖已有目录。

## 执行边界与停止条件

- **主论文源码存在即停止在代码导读阶段**：主论文官方/高度可信源码已 clone、已存在或本地已找到时，只做仓库导读、入口定位、数据处理代码定位、写报告和极简摘要。
- **禁止自动运行阶段**：主论文源码存在时，不安装依赖、不下载数据、不修复源码路径、不设置真实数据目录、不运行训练/评估/推理、不生成新的 `<method-slug>-reproduction/` 工程。
- **无主论文源码才生成复现工程**：只有线上和本地都没有主论文源码，并且论文可直接复现或部分可复现时，才生成 `<method-slug>-reproduction/`。
- **数据集源码和 baseline 源码不能替代主论文源码**：它们只能作为数据处理或实现参考证据；如果主论文没有源码，仍需判断并生成主论文复现工程。
- **后续短句不自动跑训练**：报告产出后，用户只说“复现/继续/重新跑一遍”时，默认重新执行本技能流程，不得擅自开始训练；明确要求训练时才视为新的运行任务。

## 总体流程

### 第 1 步：读取论文证据

从论文 PDF、arXiv 页面或用户提供文本中提取：标题、作者、年份、会议或期刊、摘要、核心贡献、方法、实验、附录、脚注、代码可用性声明、数据集、指标、baseline、训练细节、图表标题和图注、明确的 GitHub/GitLab/项目页/Hugging Face/数据集链接。

如果无法读取 PDF 或附件，先说明缺失的工具或输入，不要编造论文内容。

### 第 2 步：论文类型分类

必须给出一个主类型，必要时给出次类型。可选类型：综述论文、方法论文、提示词工程论文、基准评测论文、资源论文、理论论文、系统论文。

### 第 3 步：可复现性判定

使用 `references/reproducibility-rubric.md`。只能输出以下四个标签之一：可以直接复现、部分可复现、不具备实际可复现性、不是复现目标。

必须区分“能不能复现”和“需不需要复现”。不要把“有论文描述”误判成“可以直接复现”。

### 第 4 步：主论文代码线索搜索

必须主动搜索论文证据中的代码线索：PDF URL、脚注、附录、作者说明、arXiv abstract 页面、project page、supplementary material、OpenReview 页面、`code is available`、`source code`、`implementation`、`official repository`、`github`、`project page` 等。

如果发现多个仓库，优先判断作者官方仓库。无法确认时，标记为“官方性未验证”。

### 第 5 步：本地主论文源码检查

在进入无代码复现前，必须检查本地是否已有主论文相关源码。优先使用：

```text
python scripts/find_local_code.py --paper-slug <paper-slug> --name <paper-title-or-method> --workspace .
```

检查范围包括：`paper-repro-workspace/<paper-slug>/main-code/`、`paper-repro-workspace/<paper-slug>/local-code/`、当前 agent workspace、环境变量 `PAPER_REPRO_LOCAL_CODE_ROOTS`。数据集代码目录可以作为辅助证据，但不能直接判定为主论文源码。

如果本地找到高可信主论文源码，不进入无代码复现路径，而是进入“本地代码路径”：读取 README、依赖、训练入口、评测入口、配置、模型、数据处理代码，并写入报告。

### 第 6 步：数据集论文与数据集源码溯源

当主论文使用或发布数据集、benchmark 或标注资源时，必须执行此步骤。详细流程见 `references/dataset-source-tracing.md`。

对每个关键数据集，必须：

1. 提取数据集名称、简称、引用编号、数据集论文标题、项目页、数据下载页和脚注。
2. 检索数据集原论文、项目页、Papers with Code、GitHub/GitLab/Hugging Face 线索。
3. clone 前先检查本地是否已有相关源码。
4. 找到官方或可能官方源码后 clone 或跳过 clone。
5. 使用 `scripts/inspect_repo_data_processing.py` 或等价只读检查定位数据处理代码。
6. 报告数据处理代码文件、入口命令、关键函数/类、README 证据和对主论文复现的影响。

### 第 7 步：有主论文代码时自动执行并导读

如果发现主论文官方/高度可信代码，必须：

1. 记录“检测到主论文代码仓库，进入自动仓库路径”。
2. clone 前判断目标路径是否已有同名源码文件夹；若已有，跳过 clone，只读检查。
3. Windows 优先执行：`python scripts/bootstrap_repo.py <repo-url> <paper-slug> main-code`；如 `python` 不可用，尝试 `py scripts/bootstrap_repo.py ...`。
4. clone 成功或发现现有目录后，继续做仓库导读，不能停在“已经 clone”或“已存在”。
5. 使用 `scripts/inspect_repo_data_processing.py <repo-path>` 定位数据处理代码。
6. 报告本地路径、clone 状态、重复目录提醒、依赖文件、安装命令候选、训练/推理/评测入口、数据集准备方式、配置文件、模型文件、训练文件、评测文件、数据处理文件。
7. 完成第 6 项后必须写入报告并结束本技能流程；不得继续安装依赖、修复源码、设置真实数据路径、下载数据、运行训练、运行评测或执行 inference。
8. “可以直接复现”只表示具备复现条件，不表示现在开始执行训练。

### 第 8 步：无主论文源码时生成复现工程

只要满足以下条件，就必须生成复现工程，而不是只给建议：

- 线上没有官方/可信主论文源码；
- 本地没有主论文源码；
- 论文不是综述、纯理论或非复现目标；
- 论文证据支持“可以直接复现”或“部分可复现”；
- 数据集、模型结构、训练循环、loss、指标至少能构造最小可行版本。

如果找到数据集相关源码或 baseline 源码，要将其作为数据处理和 baseline 证据输入复现工程，但不能终止主论文复现工程生成。

详细规则见 `references/no-code-reproduction.md`。

生成前必须先写 `paper-spec.yaml`。可以使用：

```text
python scripts/build_paper_spec.py <evidence-md> --out paper-repro-workspace/<paper-slug>/paper-spec.yaml
```

然后生成工程：

```text
python scripts/scaffold_repro_project.py paper-repro-workspace/<paper-slug>/paper-spec.yaml --out paper-repro-workspace/<paper-slug>/<framework-or-method-slug>-reproduction
```

生成后运行静态检查：

```text
python scripts/inspect_repro_project.py paper-repro-workspace/<paper-slug>/<framework-or-method-slug>-reproduction
```

不自动安装依赖，不下载大数据，不运行训练。轻量 `py_compile` 和文件完整性检查可以自动执行。

### 第 9 步：写入 Markdown 报告

最终必须把详细内容写入：`paper-repro-workspace/<paper-slug>/repro-report.md`。

报告模板见 `references/output-template.md`。必须记录：论文信息、分类、可复现性、代码搜索、主论文源码、本地源码、数据集源码、数据处理代码位置、复现工程生成结果、执行过的命令、不能复现原因、未完成项/人工确认项。

## 聊天输出格式

聊天中不要输出长报告。聊天回复只输出：

```markdown
[paper-repro-triage active]

- 报告文件：`paper-repro-workspace/<paper-slug>/repro-report.md`
- 主论文源码：已 clone / 已存在，跳过 clone / 本地已存在 / 未找到 / 等待审批 / clone 失败
- 数据集源码：已 clone N 个 / 已存在，跳过 clone N 个 / 本地已存在 N 个 / 未找到 / 部分找到 / 未检索
- 数据处理代码：已定位 N 处 / 未定位 / 不适用
- 复现工程：已生成 / 仅生成 skeleton / 未生成，路径：`paper-repro-workspace/<paper-slug>/<implementation-slug>/`
- 是否需要复现：需要 / 不需要 / 建议只做部分复现
- 是否能复现：可以直接复现 / 部分可复现 / 不具备实际可复现性 / 不是复现目标
- 核心原因：一句话说明；如果能复现则写“无核心阻碍”
- 执行边界：未运行训练 / 未安装依赖 / 未下载数据；如已存在主论文源码，写“已停在代码导读阶段”
```

## 安全与诚实规则

- 不要伪造已经执行过的命令。
- 不要伪造仓库文件名。
- 不要伪造 Markdown 文件已经写入。
- 不要声称精确复现，除非代码、数据、配置和评测协议都足够充分。
- 不要把第三方复现仓库当成官方仓库。
- 不要自动安装未知依赖、下载大数据、修复官方源码路径、设置真实数据目录或运行训练/评测/推理脚本；clone、跳过重复 clone、只读仓库检查、生成复现工程、静态检查可以自动执行。
- 所有论文未明确给出的超参数、路径、模型维度、loss 权重、数据处理细节必须标注 `ASSUMPTION`。
- 如果只能生成 baseline，必须命名为 baseline，不能命名为 paper reproduction。
- 如果生成的代码含 `TODO` 或 `NotImplementedError`，报告必须列出。

## 资源

- 可复现性判定标准：`references/reproducibility-rubric.md`
- Markdown 报告模板：`references/output-template.md`
- 数据集论文源码溯源流程：`references/dataset-source-tracing.md`
- 无代码复现工程流程：`references/no-code-reproduction.md`
- 仓库 bootstrap 脚本：`scripts/bootstrap_repo.py`
- 本地源码查找：`scripts/find_local_code.py`
- 数据处理代码定位：`scripts/inspect_repo_data_processing.py`
- paper spec 草稿：`scripts/build_paper_spec.py`
- 复现工程生成：`scripts/scaffold_repro_project.py`
- 复现工程检查：`scripts/inspect_repro_project.py`
