---
name: liquid-neural-network
description: "Build, train, and inspect Liquid Neural Networks (LNNs) — liquid time-constant (LTC) and closed-form continuous-time (CfC) networks with Neural Circuit Policy (NCP) sparse wirings, using the ncps library on PyTorch. Activate when the user asks to build/train a liquid neural network, LNN, LTC, CfC, or NCP model, do continuous-time or ODE-based sequence modeling, or fit small robust recurrent models for time-series prediction. Provides scripts/train_lnn.py (synthetic or CSV time-series training, wiring options, model saving) plus theory and API references. | 构建、训练和检查液体神经网络（LNN）：基于 PyTorch 的 ncps 库，支持液体时间常数（LTC）与闭式连续时间（CfC）网络，以及神经回路策略（NCP）稀疏接线。当用户要求构建/训练液体神经网络、LNN、LTC、CfC 或 NCP 模型，进行连续时间或基于 ODE 的序列建模，或拟合小型稳健的时序预测循环模型时激活。提供 scripts/train_lnn.py（合成或 CSV 时序训练、接线选项、模型保存）以及理论与 API 参考。"
version: 1.0.0
license: MIT
homepage: https://ncps.readthedocs.io/en/latest/
metadata:
  clawdbot:
    emoji: 🧠
    requires:
      bins: [python3]
      packages: [ncps, torch, numpy, pandas]
      env: []
---

# 🧠 Liquid Neural Network (LNN) Skill | 液体神经网络技能

Build, train, and inspect **Liquid Neural Networks** — a class of continuous-time
recurrent networks in which every neuron is modeled by an ordinary differential
equation (ODE). The reference implementation used here is the **`ncps`**
(Neural Circuit Policies) library by Mathias Lechner et al., running on PyTorch.

构建、训练并检查**液体神经网络（LNN）**——一种连续时间循环网络，其中每个神经元由常微分方程（ODE）建模。本技能使用 Mathias Lechner 等人开发的 **`ncps`**（神经回路策略）库，基于 PyTorch 运行。

This skill covers: | 本技能覆盖：

- **LTC** — Liquid Time-Constant networks: universal approximators with input-adaptive timing behavior (how fast neurons react depends on the input). 液体时间常数网络：万能逼近器，时序行为随输入自适应（神经元反应快慢取决于输入）。
- **CfC** — Closed-form Continuous-time networks: fast closed-form approximation of the LTC dynamics (1–2 orders of magnitude faster to train/infer). 闭式连续时间网络：LTC 动力学的闭式快速近似（训练/推理快 1–2 个数量级）。
- **NCP wirings** — sparse, structured 4-layer connectivity (sensory → inter → command → motor) inspired by the nervous system of *C. elegans*, giving small, auditable, robust models. NCP 接线：受秀丽隐杆线虫神经系统启发的稀疏 4 层结构（感觉→中间→命令→运动），得到小型、可审计、稳健的模型。

## When to use this skill | 何时使用本技能

Activate when the user wants to: | 当用户需要以下能力时激活：

- build or train a liquid neural network, LNN, LTC, or CfC model | 构建或训练液体神经网络、LNN、LTC、CfC 模型
- use Neural Circuit Policies / NCP / AutoNCP wiring | 使用神经回路策略 / NCP / AutoNCP 接线
- model continuous-time dynamics or ODE-style sequence behavior | 对连续时间动力学或 ODE 式序列行为建模
- fit a small, robust recurrent model for time-series prediction (few-shot, multi-task, autonomous systems, control) | 为时序预测拟合小型稳健的循环模型（少样本、多任务、自动驾驶、控制）
- compare LTC vs CfC vs LSTM/GRU on a sequence task | 在序列任务上对比 LTC、CfC 与 LSTM/GRU
- inspect the wiring graph of an NCP | 检查 NCP 的接线图结构

Do **not** use for: static/feed-forward tasks with no time dimension, very long contexts (Transformers are better), or tasks where interpretability is not needed and standard RNNs suffice.

**不适用场景**：无时间维度的静态/前馈任务、超长上下文（Transformer 更合适）、或无需可解释性且标准 RNN 已够用的任务。

## Environment setup | 环境准备

Requires Python 3.9+ with PyTorch installed (CPU is fine for small models).
需要 Python 3.9+ 并安装 PyTorch（小模型 CPU 即可）。

```bash
pip install -r scripts/requirements.txt
```

The `ncps` package works on Windows, macOS, and Linux.

## Quick start | 快速开始

All training is driven by `scripts/train_lnn.py`
(run `python scripts/train_lnn.py --help` for the full reference).
所有训练都由 `scripts/train_lnn.py` 驱动（运行 `python scripts/train_lnn.py --help` 查看完整说明）。

### 1. Train a CfC model on synthetic data (default, no data files needed) | 在合成数据上训练 CfC 模型（默认，无需数据文件）

```bash
python scripts/train_lnn.py --model cfc --units 28 --output-size 1 --steps 1500
```

### 2. Train an LTC model with a sparse AutoNCP wiring | 用稀疏 AutoNCP 接线训练 LTC 模型

```bash
python scripts/train_lnn.py --model ltc --wiring autoncp --wiring-units 28 --output-size 2 --steps 1500
```

### 3. Train on your own CSV time series | 用你自己的 CSV 时序数据训练

```bash
python scripts/train_lnn.py --csv data.csv --features temperature,humidity --target power --steps 2000 --save model.pt
```

### 4. Evaluate and show a rolling forecast after training | 训练后评估并演示滚动预测

```bash
python scripts/train_lnn.py --model cfc --wiring autoncp --wiring-units 24 --output-size 1 --steps 800 --eval --rollout 10
```

## Command reference | 命令参考

| Argument 参数 | Default 默认 | Meaning 含义 |
|---|---|---|
| `--model` | `cfc` | neuron model: `cfc` (fast) or `ltc` (ODE solver) 神经元模型：`cfc`（快）或 `ltc`（ODE 求解） |
| `--wiring` | `fc` | wiring: `fc` (fully connected), `autoncp`, `random` 接线：`fc` 全连接、`autoncp`、`random` |
| `--units` | `28` | hidden units (for `fc`/`random`) 隐藏单元数（fc/random） |
| `--wiring-units` | — | total neurons for `autoncp` (defaults to `--units`) autoncp 总神经元数（默认同 `--units`） |
| `--output-size` | `1` | number of output variables 输出变量个数 |
| `--input-size` | `3` | number of input features (synthetic data) 输入特征数（合成数据） |
| `--seq-len` | `32` | history window (time steps) per training sample 每个训练样本的历史窗口（时间步） |
| `--steps` | `1000` | number of training iterations 训练迭代次数 |
| `--batch-size` | `64` | batch size 批大小 |
| `--lr` | `0.01` | learning rate 学习率 |
| `--sparsity` | `0.5` | sparsity for `autoncp`/`random` (0.0 dense – 0.9 sparse) autoncp/random 的稀疏度（0.0 稠密 – 0.9 稀疏） |
| `--seed` | `0` | random seed 随机种子 |
| `--solver` | — | LTC/CfC ODE solver: `euler`, `midpoint`, `rk4` ODE 求解器 |
| `--input-mapping` | — | `linear` or `affine` input encoding 输入编码：`linear` 或 `affine` |
| `--csv` | — | path to a CSV file (columns = features + target) CSV 文件路径 |
| `--features` | — | comma-separated CSV columns used as inputs 用作输入的 CSV 列（逗号分隔） |
| `--target` | — | comma-separated CSV columns to predict 要预测的 CSV 列（逗号分隔） |
| `--eval` | — | run validation MSE after training 训练后计算验证 MSE |
| `--rollout` | `5` | number of rolling-forecast steps to demo 滚动预测演示步数 |
| `--save` | — | save the trained model to a `.pt` file 保存训练好的模型到 `.pt` 文件 |
| `--no-cuda` | — | force CPU even if CUDA is available 即使有 CUDA 也强制使用 CPU |

`ncps` 支持 Windows、macOS 和 Linux。

## Outputs | 输出结果

- **Trained model** — saved via `--save model.pt` (PyTorch `torch.save`). 训练好的模型，通过 `--save model.pt` 保存（PyTorch `torch.save`）。
- **Console metrics** — per-iteration loss, final validation MSE (`--eval`). 控制台指标：每轮迭代损失、最终验证 MSE（`--eval`）。
- **Rolling forecast** — a short multi-step forecast printed after training (`--rollout N`), useful for a quick sanity check. 滚动预测：训练后打印的多步预测演示（`--rollout N`），便于快速检查。
- **Wiring inspection** — use `scripts/inspect_wiring.py` to print the NCP layer sizes / synapse counts and optionally render the wiring graph to PNG. 接线检查：用 `scripts/inspect_wiring.py` 打印 NCP 各层规模/突触数，并可把接线图渲染为 PNG。

## References | 参考资料

| File 文件 | Contents 内容 |
|---|---|
| `references/lnn_theory.md` | LNN theory: liquid time-constants, ODE neurons, LTC vs CfC, NCP layers, papers LNN 理论：液体时间常数、ODE 神经元、LTC vs CfC、NCP 分层、论文 |
| `references/api_cheatsheet.md` | `ncps` API patterns (LTC/CfC, wirings, training loop skeleton) ncps API 模式（LTC/CfC、接线、训练循环骨架） |

## Important gotchas | 重要注意事项

- LNNs are **recurrent** and require **time-series data** — inputs must be shaped `(batch, time_steps, features)`; there is no valid feed-forward use. LNN 是**循环**模型，必须使用**时序数据**——输入形状为 `(batch, time_steps, features)`，没有合法的前馈用法。
- Initial state `h0` must match the model's state size: `units` for fully connected wiring, `wiring_units` for AutoNCP (total neuron count). 初始状态 `h0` 必须匹配模型状态大小：全连接用 `units`，AutoNCP 用 `wiring_units`（总神经元数）。
- The model output at step *t* is the prediction for step *t+1*; with `return_sequences=True` take `output[:, -1, :]` for the last step. 模型在 *t* 步的输出是对 *t+1* 步的预测；`return_sequences=True` 时取 `output[:, -1, :]` 得到最后一步。
- LTC uses a numerical ODE solver, so it is slower than CfC — prefer CfC for large datasets and LTC when you need the pure differential-equation behavior. LTC 使用数值 ODE 求解器，比 CfC 慢——大数据集优先用 CfC；需要纯微分方程行为时用 LTC。
- `output_size` must be smaller than `wiring_units − 2` for AutoNCP (good choices are ~0.3 × units). AutoNCP 的 `output_size` 必须小于 `wiring_units − 2`（好的选择约为 units 的 0.3 倍）。
- Normalize your CSV features (the script z-scores training data internally). 对 CSV 特征做归一化（脚本内部会对训练数据做 z-score）。

## Limitations | 局限性

- The `ncps` library provides LTC/CfC only; other "liquid" variants (e.g. liquid networks with different cell dynamics) are out of scope. `ncps` 库仅提供 LTC/CfC；其他"液体"变体（如不同单元动力学的液体网络）不在范围内。
- Very long sequences are slow (RNN structure) — window with `--seq-len`. 超长序列较慢（RNN 结构）——用 `--seq-len` 加窗。
- Sparse wirings are stochastic (seeded); different seeds change the wiring. 稀疏接线是随机的（有种子）；不同种子会改变接线结构。

## Troubleshooting | 故障排查

| Problem 问题 | Fix 解决方法 |
|---|---|
| `ModuleNotFoundError: ncps` | `pip install -r scripts/requirements.txt` |
| `ModuleNotFoundError: torch` | `pip install torch` (see pytorch.org for CUDA builds) |
| AutoNCP errors | Keep `--output-size` well below `--wiring-units − 2` 让 `--output-size` 远小于 `--wiring-units − 2` |
| NaN loss | Lower `--lr`, increase `--seq-len`, check CSV normalization 降低 `--lr`，增大 `--seq-len`，检查 CSV 归一化 |
| Training too slow | Use `--model cfc` instead of `ltc`; reduce `--seq-len`/`--units` 用 `--model cfc` 代替 `ltc`；减小 `--seq-len`/`--units` |

