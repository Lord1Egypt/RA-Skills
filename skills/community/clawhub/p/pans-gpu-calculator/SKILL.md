---
name: pans-gpu-calculator
description: |
  AI算力销售GPU配置计算器。输入模型参数量和需求，自动推荐最优GPU配置并估算成本。
  支持训练和推理场景，覆盖H100/A100/L40S/A10G等主流GPU。
  触发词：GPU计算, 算力配置, 模型部署成本, GPU选型, 显存估算, 训练成本, 推理成本, GPU推荐
---

# pans-gpu-calculator — GPU 配置计算器

输入模型参数量和需求参数，自动推荐最优 GPU 配置并估算成本。

## 支持的 GPU 型号

| GPU    | 显存    | FP16 TFLOPS | 云租赁价格 |
|--------|---------|-------------|-----------|
| H100   | 80 GB   | 989         | $2.5/hr   |
| A100   | 80 GB   | 624         | $1.8/hr   |
| A100   | 40 GB   | 624         | $1.2/hr   |
| L40S   | 48 GB   | 362         | $0.8/hr   |
| A10G   | 24 GB   | 200         | $0.5/hr   |

## 核心计算公式

- **模型显存需求** = 参数量 × 2 bytes (FP16) + KV Cache (batch × seq_len × 2 × layers × hidden) + 激活值
- **最小 GPU 数** = ⌈模型显存 / 单卡显存⌉
- **推理吞吐** = GPU TFLOPS × MFU / 模型 FLOPs_per_token
- **训练时间** = 8 × 参数量 × token数 / (GPU数 × TFLOPS × MFU)

## 使用方法

```bash
# 推理场景 — 对比所有 GPU
python3 scripts/calc.py --params 70B --mode inference --compare

# 推理场景 — 指定 GPU
python3 scripts/calc.py --params 7B --mode inference --gpu L40S --batch 32

# 训练场景
python3 scripts/calc.py --params 7B --mode train --tokens 100B --batch 256

# JSON 输出（便于程序调用）
python3 scripts/calc.py --params 70B --mode inference --compare --json
```

### CLI 参数

| 参数       | 说明                                      | 默认值 |
|------------|------------------------------------------|--------|
| --params   | 模型参数量，如 7B, 70B, 405B            | 必填   |
| --mode     | train / inference                        | inference |
| --gpu      | 指定 GPU 型号（可选，默认自动推荐最优）   | 自动   |
| --batch    | batch size                               | 1      |
| --latency  | 目标延迟 ms（推理模式）                   | 无     |
| --tokens   | 训练 token 数（训练模式）                 | 100B   |
| --json     | JSON 格式输出                            | false  |
| --compare  | 对比所有 GPU 型号                        | false  |
