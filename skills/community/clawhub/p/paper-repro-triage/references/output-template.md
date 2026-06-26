# Markdown 报告模板

本文件用于指导详细报告写入 `paper-repro-workspace/<paper-slug>/repro-report.md`。聊天回复只保留极简摘要，不要把本报告全文贴到聊天里，除非文件写入失败。

# 论文复现报告：<论文标题>

生成时间：<时间>  
主论文输入：<PDF / arXiv / URL / 用户文本>  
报告目录：`paper-repro-workspace/<paper-slug>/`

## 1. 结论摘要

| 项目 | 结论 |
|---|---|
| 论文类型 | 综述 / 方法 / 提示词工程 / 基准评测 / 资源 / 理论 / 系统 |
| 是否需要复现 | 需要 / 不需要 / 建议只做部分复现 |
| 是否能复现 | 可以直接复现 / 部分可复现 / 不具备实际可复现性 / 不是复现目标 |
| 主论文源码 | 已 clone / 已存在，跳过 clone / 本地已存在 / 未找到 / 等待审批 / clone 失败 |
| 数据集源码 | 已 clone N 个 / 已存在，跳过 clone N 个 / 本地已存在 N 个 / 未找到 / 部分找到 / 未检索 |
| 数据处理代码 | 已定位 N 处 / 未定位 / 不适用 |
| 复现工程 | 已生成 / 仅生成 skeleton / 未生成 |
| 核心阻碍 | 一句话说明 |
| 执行边界 | 未运行训练 / 未安装依赖 / 未下载数据 / 已停在代码导读阶段 |
| 报告文件 | `paper-repro-workspace/<paper-slug>/repro-report.md` |

## 2. 论文基础信息

- 标题：
- 作者：
- 年份：
- 会议/期刊/arXiv：
- 论文链接：
- 项目页：
- 主仓库：
- 相关数据集：

## 3. 论文分类

- 主类型：
- 次类型：
- 判断依据：

## 4. 可复现性结论

- 结论：可以直接复现 / 部分可复现 / 不具备实际可复现性 / 不是复现目标
- 是否建议复现：需要 / 不需要 / 建议只做部分复现
- 原因：

## 5. 证据摘要

| 维度 | 结论 | 证据 |
|---|---|---|
| 主论文官方代码 |  |  |
| 本地主论文源码 |  |  |
| 数据集源码 |  |  |
| 数据处理代码 |  |  |
| 训练配置 |  |  |
| 评测协议 |  |  |
| 硬件需求 |  |  |
| 主要阻碍 |  |  |

## 6. 主论文代码与自动执行结果

- 是否找到主论文代码：
- 仓库可信度：官方 / 可能官方 / 第三方 / baseline / 相关代码 / 未验证
- 仓库 URL：
- 自动执行状态：已 clone / 已存在，跳过 clone / 本地已存在 / 等待审批 / 执行失败 / 无代码可执行
- 本地路径：
- 重复目录提醒：
- 执行过的命令：

### 6.1 重复目录与跳过 clone 记录

- 是否出现同名源码文件夹：是 / 否
- 跳过 clone 的仓库：
- 使用的现有本地路径：
- 现有目录是否为 git 仓库：是 / 否 / 未知
- 现有 origin：
- 是否继续完成只读仓库检查：是 / 否

### 6.2 仓库导读

- README 关键信息：
- 依赖文件：
- 配置方式：
- 命令行入口：
- 训练入口：
- 评测入口：
- 推理入口：
- 数据集准备：
- 模型实现：
- 训练逻辑：
- 论文与代码差异：

### 6.3 主论文源码存在时的停止记录

- 是否停止在代码导读阶段：是 / 否
- 是否安装依赖：否
- 是否下载数据：否
- 是否修改官方源码：否
- 是否运行训练/评估/推理：否
- 停止原因：主论文源码已存在，本技能只完成复现准备、仓库导读和报告写入；运行训练属于新的显式运行任务。

## 7. 数据集论文与数据集源码溯源

| 数据集 | 是否主实验依赖 | 原论文/项目页 | 是否找到源码 | 仓库 URL | clone 状态 | 本地路径 | 数据处理代码位置 | 数据处理入口/命令 | 对主论文复现的影响 |
|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  | 已 clone / 已存在，跳过 clone / 本地已存在 / 未 clone |  |  |  |  |

### 7.1 数据处理代码定位明细

| 来源仓库 | 文件 | 类型 | 关键函数/类 | 证据 | 可复用方式 | 风险 |
|---|---|---|---|---|---|---|
|  |  | dataset / preprocess / tokenizer / split / feature / benchmark |  | README / 文件名 / 代码片段 |  |  |

### 7.2 数据集访问限制

- 需要申请的数据集：
- 闭源或私有数据：
- 只提供数据下载但无处理代码：
- 对复现的影响：

## 8. 架构或流程解读

- 图示类型：标准模型架构 / prompt 或 agent 流程 / 系统架构 / 不确定
- 模型或流程类型：
- 关键模块：
- 输入输出：
- loss / objective：
- 是否可按代码实现：

## 9. 实验配置清单

| 项目 | 论文给出的信息 | 源码/数据集代码中的信息 | 缺失或需要确认 |
|---|---|---|---|
| 数据集 |  |  |  |
| 预处理 |  |  |  |
| 模型 |  |  |  |
| loss / objective |  |  |  |
| optimizer |  |  |  |
| learning rate |  |  |  |
| batch size |  |  |  |
| epoch / steps |  |  |  |
| GPU / 显存 |  |  |  |
| 指标 |  |  |  |

## 10. 无主论文源码复现工程生成结果

仅在无主论文源码时填写。即使找到数据集源码或 baseline 源码，只要主论文源码不存在且部分可复现，也必须填写本节。

| 项目 | 结论 |
|---|---|
| 是否生成复现工程 | 已生成 / 仅生成 skeleton / 未生成 |
| 工程路径 | `paper-repro-workspace/<paper-slug>/<method-slug>-reproduction/` |
| 生成依据 | 论文证据 / 数据集源码证据 / baseline 证据 / 明确假设 |
| 是否通过静态检查 | 通过 / 部分通过 / 未运行 |
| 是否运行训练 | 未运行，需用户确认 |

### 10.1 生成工程结构

以下为最低基本盘结构，不是不可更改的硬性目录。生成工程至少应包含这些职责清晰的模块；如果论文需要额外模块，可以在此基础上增加目录或文件。

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

### 10.2 `repro-docs/` 文件说明

| 文件 | 主要用途 | 注意事项 |
|---|---|---|
| `repro-docs/requirements.txt` | 最小依赖清单，用于创建复现环境 | 只写已确认或最小必要依赖；重型或未确认依赖写入 `repro-notes.md` |
| `repro-docs/paper-spec.yaml` | 论文证据规格，记录任务、模型、数据集、loss、训练和评测信息 | 不是训练配置；训练参数入口仍是 `config.py` |
| `repro-docs/evidence-map.md` | 映射每个代码文件对应的论文证据、数据集源码证据或假设 | 必须区分论文事实、源码证据和 ASSUMPTION |
| `repro-docs/repro-notes.md` | 记录复现限制、缺失信息、人工确认项和运行前注意事项 | 不要把未验证内容写成已完成结果 |

### 10.3 生成代码文件清单

| 文件 | 作用 | 依据 | 是否含假设 |
|---|---|---|---|
| `README.md` | 工程说明和运行命令 |  |  |
| `main.py` | 命令行入口，解析参数后交给 `Run(args).main()` |  |  |
| `config.py` | argparse 参数和超参数默认值 |  |  |
| `run.py` | 按 mode 调度 preprocess/train/eval/inference |  |  |
| `data/dataset.py` | 数据读取与 transform |  |  |
| `data/preprocess.py` | 数据处理脚本 |  |  |
| `models/model.py` | 模型定义 |  |  |
| `engine/train.py` | 训练循环与 loss/objective |  |  |
| `engine/evaluate.py` | 评测循环 |  |  |
| `utils/metrics.py` | 指标函数 |  |  |
| `utils/common.py` | seed、路径、日志等工具 |  |  |

### 10.4 config 参数

| 参数 | 默认值 | 来源 | 备注 |
|---|---|---|---|
|  |  | paper / dataset-code / baseline-code / assumption / todo |  |

### 10.5 model 定义

- 文件：`models/model.py`
- 类名：
- 输入：
- 输出：
- 关键模块：
- 论文依据：
- 缺失/假设：

### 10.6 train 定义

- 文件：`engine/train.py`
- loss / objective：
- optimizer：
- scheduler：
- checkpoint：
- logging：
- 论文依据：
- 缺失/假设：

### 10.7 evaluate 定义

- 文件：`engine/evaluate.py`
- 指标：
- protocol：
- checkpoint：
- 输出文件：
- 论文依据：
- 缺失/假设：

### 10.8 数据处理实现

| 数据集 | 数据处理文件 | 入口命令 | 来源证据 | 风险 |
|---|---|---|---|---|
|  | `data/preprocess.py` / `data/dataset.py` | `python main.py --mode preprocess ...` |  |  |

### 10.9 可执行命令

```cmd
python -m pip install -r repro-docs/requirements.txt
python main.py --mode preprocess --dataset <dataset> --data_root <path>
python main.py --mode train --dataset <dataset> --data_root <path>
python main.py --mode eval --checkpoint outputs/best.pt
```

### 10.10 未完成项 / 人工确认项

- 未下载数据：
- 未安装依赖：
- 论文缺失：
- 需要确认的假设：

## 11. 不能复现或不能精确复现的原因

- 原因 1：
- 原因 2：
- 原因 3：

## 12. 执行日志

| 时间 | 命令 / 工具 | 结果 | 备注 |
|---|---|---|---|
|  |  |  |  |

# 聊天极简摘要模板

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
```
