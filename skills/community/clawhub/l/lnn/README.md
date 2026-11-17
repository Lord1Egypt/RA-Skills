# 🧠 Liquid Neural Network (LNN) Skill | 液体神经网络技能

A [ClawHub](https://clawhub.com) / OpenClaw skill for building, training, and
inspecting **Liquid Neural Networks (LNNs)** using the
[`ncps`](https://ncps.readthedocs.io/en/latest/) library on PyTorch.

一个基于 PyTorch `ncps` 库，用于构建、训练和检查**液体神经网络（LNN）**的
ClawHub / OpenClaw 技能。

## ✨ Features | 特性

- ⏱️ **Two neuron models** — LTC (liquid time-constant, ODE-based) and CfC (closed-form, fast) | 两种神经元模型：LTC（液体时间常数，基于 ODE）与 CfC（闭式解，快速）
- 🧬 **Neural Circuit Policy wirings** — sparse 4-layer NCP (sensory → inter → command → motor), inspired by *C. elegans* | 神经回路策略接线：稀疏 4 层 NCP（感觉→中间→命令→运动），受秀丽隐杆线虫启发
- 📈 **Time-series training** — synthetic data or your own CSV | 时序训练：内置合成数据或自己的 CSV
- 💾 **Model saving** — save trained models to `.pt` | 模型保存：保存训练好的模型为 `.pt`
- 📊 **Evaluation** — validation MSE + rolling forecast demo | 评估：验证 MSE + 滚动预测演示
- 🔍 **Wiring inspection** — print layer sizes / synapse counts, render the graph to PNG | 接线检查：打印层规模/突触数，渲染接线图为 PNG
- 🤝 **Interoperable** — combine LTC/CfC with any PyTorch layer | 可组合：LTC/CfC 可与任意 PyTorch 层组合

## 📦 Installation | 安装

```bash
pip install -r scripts/requirements.txt
```

Requires Python 3.9+ and PyTorch. | 需要 Python 3.9+ 和 PyTorch。

## 🚀 Quick start | 快速开始

```bash
# CfC on synthetic data | 合成数据训练 CfC
python scripts/train_lnn.py --model cfc --units 28 --output-size 1 --steps 1500

# LTC with a sparse AutoNCP wiring | 稀疏 AutoNCP 接线训练 LTC
python scripts/train_lnn.py --model ltc --wiring autoncp --wiring-units 28 --output-size 2 --steps 1500

# Train on your own CSV | 用自己的 CSV 训练
python scripts/train_lnn.py --csv data.csv --features temperature,humidity --target power --save model.pt

# Inspect an NCP wiring | 检查 NCP 接线
python scripts/inspect_wiring.py --type autoncp --units 28 --output-size 4 --draw wiring.png
```

## 📁 Directory structure | 目录结构

```
lnn/
├── SKILL.md                     # Skill definition for ClawHub | 技能定义
├── LICENSE                      # MIT license | MIT 许可证
├── scripts/
│   ├── train_lnn.py             # Train LTC/CfC models | 训练 LTC/CfC 模型
│   ├── inspect_wiring.py        # Inspect/render NCP wirings | 检查/渲染 NCP 接线
│   └── requirements.txt         # Python dependencies | Python 依赖
└── references/
    ├── lnn_theory.md            # LNN theory (LTC, CfC, NCP, papers) | LNN 理论
    └── api_cheatsheet.md        # ncps API patterns | ncps API 速查
```

## 📚 References | 参考

- `ncps` library: <https://ncps.readthedocs.io/en/latest/>
- Papers: *Neural circuit policies enabling auditable autonomy* (2020),
  *Closed-form continuous-time neural networks* (2022).
- This skill's full docs live in [`SKILL.md`](SKILL.md) (bilingual).

## 📄 License | 许可证

[MIT](LICENSE)
