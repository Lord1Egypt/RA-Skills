# 数据集论文与数据集源码溯源流程

目标：从主论文中识别关键数据集，轻量检索这些数据集的原论文或项目页是否有官方源码、处理代码或 benchmark 仓库。如果找到可信仓库，先查本地是否已有相关源码；没有才自动 clone。不下载论文 PDF，不下载数据集本体。

## 触发条件

主论文中出现以下信息时触发：

- 使用多个公开数据集进行实验。
- 发布新数据集、benchmark 或标注资源。
- 数据集对复现结论至关重要。
- 用户明确要求“爬取相关数据集论文”“找数据集论文源码”“克隆数据集代码”。

## 数据集优先级

如果数据集很多，默认最多处理 5 个：

1. 主实验表格中反复出现的数据集。
2. 论文新发布的数据集。
3. 与核心结论直接相关的数据集。
4. 需要特殊预处理或标注流程的数据集。
5. benchmark 评测协议依赖的数据集。

## 检索策略

对每个数据集，优先查：

- 主论文参考文献里的数据集原论文标题。
- 数据集名称 + `github`。
- 数据集名称 + `official code`。
- 数据集名称 + `project page`。
- 数据集论文标题 + `code`。
- Papers with Code 数据集页或任务页。
- arXiv abstract 页面里的 comments/code 链接。

## 本地优先规则

找到数据集相关仓库 URL 后，clone 前必须先检查本地已有源码：

```text
python scripts/find_local_code.py --paper-slug <paper-slug> --name <dataset-name-or-repo-name> --workspace .
```

检查范围：

- `paper-repro-workspace/<paper-slug>/dataset-code/`
- `paper-repro-workspace/<paper-slug>/local-code/`
- 当前 agent workspace
- 环境变量 `PAPER_REPRO_LOCAL_CODE_ROOTS`

如果本地存在同名或高相关源码，记录为 `本地已存在，跳过 clone`，并直接进入源码导读和数据处理代码定位。

## 仓库可信度判断

- 官方：论文作者、项目组织、数据集官网明确链接。
- 可能官方：作者主页或机构页链接，但没有明确“official”字样。
- 第三方：非作者维护、复现性质、社区实现。
- 未验证：只能通过搜索结果推测，缺少直接证据。

只自动 clone “官方”或“可能官方”的仓库。第三方仓库默认只记录 URL，不自动 clone，除非用户明确同意。

## 数据处理代码定位

对每个已经找到或本地存在的数据集源码，必须定位数据处理相关代码。优先使用：

```text
python scripts/inspect_repo_data_processing.py <repo-path>
```

必须检查并记录：

- 数据集类：`Dataset`、`DataModule`、`DataLoader`、`torch.utils.data.Dataset`。
- 数据加载文件：`dataset.py`、`datasets/*.py`、`data/*.py`、`loader.py`、`dataloader.py`。
- 预处理脚本：`preprocess.py`、`prepare_data.py`、`process_*.py`、`extract_*.py`、`convert_*.py`。
- 标注解析：`annotation`、`label`、`split`、`metadata`、`json/csv/txt` parsing。
- 特征抽取：`feature`、`extract_frames`、`tokenize`、`crop`、`resize`、`augment`。
- README / docs 中的 data preparation、preprocess、dataset setup 命令。

如果无法明确判断数据处理入口，要报告“未定位到明确数据处理入口”，并说明仅找到哪些候选文件。

## 报告字段

每个数据集至少记录：

- 数据集名称。
- 是否是主实验依赖。
- 原论文或项目页。
- 是否找到源码。
- 仓库 URL。
- 仓库可信度。
- clone / 本地状态。
- 本地路径。
- 数据处理代码位置。
- 数据处理入口命令或函数。
- README / 文件证据。
- 数据访问限制。
- 对主论文复现的影响。

## 禁止事项

- 不下载数据集本体。
- 不批量下载论文 PDF。
- 不绕过登录、申请、验证码、付费墙或授权限制。
- 不把第三方复现仓库伪装成官方仓库。
- 不声称数据集可用，除非找到明确下载或申请路径。

## 重复目录处理

当数据集源码仓库需要 clone 到 `paper-repro-workspace/<paper-slug>/dataset-code/<dataset-slug>/<repo-name>/` 时，必须先检查目标路径是否已经存在同名源码文件夹。

- 如果目标路径不存在：可以自动 `git clone`。
- 如果目标路径已经存在：不要再次 clone，不要自动 `git pull`，不要覆盖，也不要改用时间戳新目录；直接读取现有目录并在报告中标记 `已存在，跳过 clone`。
- 如果现有目录是 git 仓库：记录其 `origin`，并说明是否与目标仓库一致。
- 如果现有目录不是 git 仓库：记录目录冲突，提示用户手动处理或指定新目录。

聊天极简摘要中也必须体现数据集源码状态，例如：`数据集源码：本地已存在 1 个，已存在，跳过 clone 2 个`。
