# Energy Data — GPU 能耗实测数据集与方法论

> 源自 EcoCompute，适配 Green Vault 能效模块。

## 概述

本数据集包含 113+ 项实测数据，覆盖 3 款 GPU × 5 种精度方法 × 多个模型，为 Green Vault 的能效协议提供实证基础。

---

## 1. 测量环境

| 项目 | 规格 |
|------|------|
| GPU | NVIDIA RTX 5090, RTX 4090D, A800 |
| 精度方法 | FP16, FP8, NF4, INT8-mixed, INT8-pure |
| 模型 | Qwen (0.5B/1.5B/3B/7B), Mistral-7B, TinyLlama-1.1B, Phi-3-mini, Yi-6B |
| 参数范围 | 0.5B – 7B |
| 软件栈 | PyTorch, CUDA, transformers, bitsandbytes, torchao |
| 功率监测 | NVML 10Hz 采样 |
| 重复次数 | n=3–10 次/配置，CV < 2% |

## 2. 关键发现汇总

### 2.1 INT8 能耗悖论

| GPU | 模型 | INT8 vs FP16 能耗变化 |
|-----|------|----------------------|
| RTX 5090 | Qwen-7B | +89% |
| RTX 4090D | Qwen-7B | +147% |
| A800 | Qwen-7B | +17% |
| RTX 5090 | Qwen-3B | +63% |
| RTX 4090D | Mistral-7B | +121% |

**结论**：`load_in_8bit=True`（bitsandbytes 默认 INT8）在绝大多数测试场景下增加能耗。原因是 mixed-precision dequantization 的计算开销超过了内存带宽节省。

### 2.2 NF4 小模型陷阱

| GPU | 模型 | NF4 vs FP16 能耗变化 |
|-----|------|---------------------|
| RTX 5090 | Qwen-0.5B | +29% |
| RTX 4090D | TinyLlama-1.1B | +22% |
| A800 | Qwen-1.5B | +11% |

**结论**：≤3B 参数模型使用 NF4 量化反而浪费能耗。量化/反量化开销在小模型上占比过高。

### 2.3 Batch Size 杠杆效应

| GPU | 模型 | BS=1 能耗 | BS=64 能耗 | 降幅 |
|-----|------|-----------|-----------|------|
| A800 | Qwen-7B FP16 | 基准 | -95.7% | 95.7% |
| RTX 5090 | Qwen-7B FP16 | 基准 | -93.2% | 93.2% |
| RTX 4090D | Mistral-7B FP16 | 基准 | -91.8% | 91.8% |

**结论**：Batch size 是最强的能效优化杠杆。即使无法使用 BS=64，从 BS=1 提升到 BS=8 通常也能降低 70%+ 能耗。

### 2.4 FP8 Eager 惩罚

| GPU | 模型 | FP8 Eager vs FP16 |
|-----|------|--------------------|
| RTX 5090 | Qwen-7B | +158% |
| RTX 5090 | Qwen-3B | +701% |

**结论**：FP8 在 eager 模式下是测试中能耗最高的方案。如需使用 FP8，必须启用 `torch.compile`。

## 3. 推荐配置速查表

| 模型规模 | GPU | 推荐精度 | 推荐 BS | 备注 |
|---------|-----|---------|---------|------|
| ≤1B | Any | FP16 | ≥8 | 不要量化，模型已经很小 |
| 1B–3B | Any | FP16 | ≥16 | NF4 在此范围无收益 |
| 3B–7B | RTX 5090 | FP16 或 NF4 | ≥32 | NF4 仅在 VRAM 不足时使用 |
| 3B–7B | RTX 4090D | NF4 | ≥16 | VRAM 限制下 NF4 是最佳选择 |
| 3B–7B | A800 | FP16 | ≥32 | 80GB VRAM 足够，无需量化 |

## 4. 数据局限性

- 仅覆盖 3 款 GPU（不含 H100/H200/MI300X 等）
- 仅覆盖 ≤7B 参数模型
- 序列长度测试范围有限
- bitsandbytes / torchao 版本持续更新，结果可能随版本变化
- 未覆盖 vLLM / TGI 等推理框架的特定优化

## 5. 数据来源

- 实测数据集：Hugging Face + Zenodo（MIT-0 许可）
- 测量方法论详见 EcoCompute 原始论文
- 所有数据可复现
