# 无主论文源码时的复现工程生成流程

当主论文没有官方源码、线上没有可信主仓库、本地也没有主论文源码时，本技能进入无主论文源码复现路径。目标不是伪造完整结果，而是在证据足够时生成一个符合多数 PyTorch 论文仓库直觉、可审查、可继续开发的最小复现工程。

## 进入本流程前的硬性前提

本流程只在“无主论文源码”时进入。如果主论文官方/高度可信源码已经 clone、已存在或本地已找到，必须停止在仓库导读和报告阶段，不得生成新的复现工程，也不得运行训练。数据集源码、baseline 源码或相关论文源码不算主论文源码；它们不能阻止本流程。

## 生成条件

同时满足以下条件时必须生成复现工程：

- 论文是方法论文、系统论文、可执行 benchmark 方法，或资源论文中的 benchmark 使用流程。
- 可复现性结论为“可以直接复现”或“部分可复现”。
- 论文中能提取出最小可行实现所需信息：输入、输出、模型或流程模块、loss/objective、数据集/替代数据、评测指标。
- 缺失信息可以用明确假设补齐，并且不会改变论文核心方法。

如果只找到数据集相关源码、baseline 源码或旧方法源码，仍然要继续生成主论文复现工程。它们只能作为数据处理、baseline 或实现参考证据，不能替代主论文源码。

## 不生成 paper reproduction 的情况

以下情况不能生成 paper reproduction，只能生成 baseline 或实验设计记录：

- 综述、观点或理论分析为主。
- 关键数据、权重、系统或闭源 API 不可获得，且没有合理缩小版。
- 模型结构、loss、评测协议都不清楚。
- 论文目标是 benchmark 定义而不是方法复现。

如果能构造一个合理 baseline，但不能构造论文方法，目录名必须包含 `baseline`，并在报告中说明不是论文原方法复现。

## 目录命名

工程目录不得固定为 `repro-implementation`。根据论文框架、方法、模型或任务名生成：

```text
paper-repro-workspace/<paper-slug>/<framework-or-method-slug>-reproduction/
```

示例：

- SGAN：`sgan-reproduction/`
- MI2LaTeX：`mi2latex-reproduction/`
- Diffusion Transformer：`dit-reproduction/`
- VideoMAE：`videomae-reproduction/`
- 无法判断方法名：`<paper-slug>-reproduction/`

## 最低基本盘工程结构

默认生成“有结构但不重”的 PyTorch 工程。基本盘采用根目录入口文件 + 四个职责明确的代码目录 + 一个复现文档目录。该结构是最低推荐结构，不是不可更改的硬性模板；如果论文需要 tokenizer、decoder、retrieval、beam search、多阶段训练或特殊评测，可以在此基础上增加目录或文件。

```text
<method-slug>-reproduction/
├── README.md
├── repro-docs/
│   ├── requirements.txt
│   ├── paper-spec.yaml
│   ├── evidence-map.md
│   └── repro-notes.md
├── config.py
├── main.py
├── run.py
├── data/
│   ├── __init__.py
│   ├── dataset.py
│   └── preprocess.py
├── models/
│   ├── __init__.py
│   └── model.py
├── engine/
│   ├── __init__.py
│   ├── train.py
│   └── evaluate.py
└── utils/
    ├── __init__.py
    ├── common.py
    └── metrics.py
```

`repro-docs/` 只存放复现文档和依赖清单，不放训练入口代码。根目录保留 `main.py`、`config.py`、`run.py`，让用户一眼看到如何运行；真正实现放入 `data/`、`models/`、`engine/`、`utils/`。

## `repro-docs/` 四个文件的作用

### `repro-docs/requirements.txt`

作用：记录最小依赖清单，方便用户创建环境。只写运行脚手架和最小复现所需依赖，例如 `torch`、`numpy`、`tqdm`。不要把尚未验证的重型依赖、系统依赖或数据下载工具随意塞进去；如需特殊依赖，在 `repro-notes.md` 中说明待确认。

### `repro-docs/paper-spec.yaml`

作用：记录从论文中抽取出的结构化规格，是生成代码的证据输入，不是训练配置文件。它应包含任务、模型模块、输入输出、数据集、loss、训练超参数、评测指标、缺失项和假设。训练时的命令行参数仍由 `config.py` 管理。

### `repro-docs/evidence-map.md`

作用：记录“代码文件 ↔ 论文证据/数据集源码证据/明确假设”的映射。每个生成的核心文件都要能追溯依据，例如 `models/model.py` 来自方法章节或架构图，`data/preprocess.py` 来自数据集论文源码或主论文预处理描述。它用于防止把推测伪装成论文事实。

### `repro-docs/repro-notes.md`

作用：记录复现状态、限制、缺失信息和人工确认项。包括尚未下载的数据、没有安装的依赖、论文没给出的超参数、只能做 skeleton 的原因、数据访问限制、以及运行真实训练前必须确认的事项。

## 不默认生成的结构

不要默认生成以下内容，除非论文或用户明确需要：

- `configs/default.yaml`、`configs/debug.yaml`、`configs/ablation.yaml`：默认只用 `config.py` + argparse。复杂项目才可扩展配置文件。
- `losses/` 或 `loss.py`：默认把 loss 放在 `engine/train.py` 的 `build_criterion()` 中；只有多个可复用复杂 loss 时才拆出。
- `scripts/train.sh`、`scripts/eval.sh`、`.cmd`：默认只用 Python 命令行入口。
- `tests/`：默认不生成；如果用户要求工程测试，再生成 `tests/`。静态检查由 skill 自带 `inspect_repro_project.py` 完成。

## 代码文件职责

### `config.py`

唯一配置入口。使用 `argparse` 定义常用命令行参数、默认超参数和路径。不要默认生成多个 YAML 配置文件。

必须包含：

- `--mode train/eval/inference/preprocess`
- `--dataset`
- `--data_root`
- `--output_dir`
- `--epochs`
- `--batch_size`
- `--lr`
- `--seed`
- `--gpu`
- `--checkpoint`
- 论文特有参数，例如 `--alpha`、`--beta`、`--beam_size`、`--max_len` 等

论文未给出的默认值必须注释 `ASSUMPTION`。

### `main.py`

唯一命令行入口。负责解析参数、设置随机种子和 GPU，然后把配置交给 `Run(args).main()`。

推荐命令：

```cmd
python main.py --mode preprocess --dataset <dataset> --data_root <path>
python main.py --mode train --dataset <dataset> --data_root <path>
python main.py --mode eval --checkpoint outputs/best.pt
```

### `run.py`

统一调度文件。根据 `args.mode` 调用 `data.preprocess`、`engine.train`、`engine.evaluate` 或 inference 逻辑。

### `data/dataset.py`

数据集读取和基础 transform。数据集处理证据来自数据集源码溯源时，必须在文件头写明：相关仓库、处理脚本、README 证据和可复用部分。

### `data/preprocess.py`

数据准备、标注转换、tokenizer/vocab 构建、图像/视频/文本预处理、数据 split 构建等。只写代码和入口，不自动下载数据集本体。

### `models/model.py`

模型定义文件。包含论文核心模型类，例如 `PaperModel` 或具体方法名模型类。若某些模块缺少论文细节，可以写 TODO 或 baseline 模块，但必须在文件头标注 `ASSUMPTION`。

### `engine/train.py`

训练循环。loss 通常放在 `build_criterion()` 或训练步骤中，除非论文 loss 极其复杂或有多个可复用组件，否则不要生成独立 `loss.py` 或 `losses/` 目录。

必须包含：dataloader、model、optimizer/scheduler、loss/objective、epoch/step 循环、checkpoint 保存、logging。

### `engine/evaluate.py`

评测逻辑。包含 checkpoint 加载、test dataloader、指标计算和 `outputs/eval.json` 保存。指标必须来自论文；论文没给出时标注 TODO。

### `utils/metrics.py`

指标函数。只存放评估指标，不存放训练 loss。

### `utils/common.py`

随机种子、路径创建、JSON 保存、device 选择、简单 logging 等通用函数。

## 静态检查

生成后运行：

```text
python scripts/inspect_repro_project.py <implementation-path>
```

允许自动执行：文件完整性检查、`py_compile`、TODO/ASSUMPTION/NotImplementedError 统计。

禁止自动执行：安装依赖、下载大数据、运行训练、评测完整数据集。

## 报告要求

报告必须写：

- 是否生成复现工程。
- 工程路径。
- 文件清单。
- `repro-docs/` 四个文件的用途。
- 每个代码文件的作用。
- 每个代码文件依据的论文证据。
- 数据集相关源码如何影响 `data/dataset.py` 和 `data/preprocess.py`。
- 哪些超参数来自论文，哪些是 ASSUMPTION。
- 未完成项/人工确认项。
