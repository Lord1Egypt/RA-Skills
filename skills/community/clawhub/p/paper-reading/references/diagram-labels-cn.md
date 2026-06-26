# 图示标签中文对照表

当使用 `--showcase-language cn` 时加载本文件。含义：图示中的结构性标签使用中文，通用技术术语保留英文。

## 字体注意事项

中文标签的字体栈必须包含中文字体：

```css
font-family: 'JetBrains Mono', 'Noto Sans SC', 'Courier New', monospace;
```

Google Fonts 引入：

```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
```

## 通用结构性标签

| 英文 | 中文 |
|---|---|
| Training Pipeline | 训练流水线 |
| Inference Pipeline | 推理流水线 |
| Input / Output | 输入 / 输出 |
| Encoder / Decoder | 编码器 / 解码器 |
| Core Contribution | 核心贡献 |
| Key Insight | 关键洞察 |
| Prior Work | 先前工作 |
| Baseline | 基线 |
| Ablation | 消融 |
| Method Overview | 方法概览 |
| System Architecture | 系统架构 |
| Dataset | 数据集 |
| Model | 模型 |
| Policy | 策略 |
| Reward / Loss | 奖励 / 损失 |
| Gradient Update | 梯度更新 |
| Feedback Loop | 反馈回路 |
| Legend | 图例 |
| Step 1 / Step 2 / Step 3 | 步骤 1 / 步骤 2 / 步骤 3 |

## 数据流 / 流程语义

| 英文 | 中文 |
|---|---|
| Data flow | 数据流 |
| Training loop | 训练循环 |
| Auth flow | 认证流 |
| Feedback / Propagation | 反馈 / 传播 |
| Sample / Sampling | 采样 |
| Evaluate | 评估 |
| Aggregate | 聚合 |
| Normalize | 归一化 |
| Update | 更新 |

## 机器学习常见术语

| 英文 | 中文 |
|---|---|
| Reinforcement Learning | 强化学习 |
| Supervised Fine-tuning | 监督微调 |
| Policy Optimization | 策略优化 |
| Advantage | 优势 |
| Rollout | 采样轨迹（或保留 rollout） |
| Rollout trajectory | 采样轨迹 |
| Batch | 批次 |
| Group | 组 |
| Per-reward / Per-sample | 逐奖励 / 逐样本 |
| Weighted sum | 加权求和 |
| Mean / Std (statistics) | 均值 / 标准差 |
| Clipping | 裁剪 |
| KL divergence | KL 散度 |
| PPO-clipped objective | PPO 裁剪目标 |
| Importance ratio | 重要性比率 |

## 保留英文（请勿翻译）

这些术语在中文语境下通常不翻译，保留英文更清晰：

- Transformer / Attention / Self-Attention
- Softmax / Sigmoid / ReLU / GELU
- LoRA / QLoRA / PEFT
- MoE (Mixture of Experts)
- RLHF / DPO / GRPO / PPO
- Tokenizer / Token / Embedding
- Logits / Probits
- Adam / AdamW / SGD
- Batch norm / Layer norm (这些是标准英文简写)
- Fine-tune (有时作动词使用时保留)

## 警告 / 结果语义（图示中经常出现）

| 英文 | 中文 |
|---|---|
| ✗ IDENTICAL — information collapse | ✗ 相同 — 信息坍塌 |
| ✓ DISTINCT — differences preserved | ✓ 不同 — 差异保留 |
| Collapsed | 坍塌 / 退化 |
| Stable convergence | 收敛稳定 |
| Training instability | 训练不稳定 |
| Diverges | 发散 |
| Outperforms | 优于 |
| Trade-off | 权衡 |

## 图示页脚格式

中文图示推荐页脚格式：

```
[论文简称] · [作者], [机构] · arXiv:[编号] ([日期])
```

例如：`GDPO · Liu 等, NVIDIA · arXiv:2601.05242 (2026 年 1 月)`

## 常见排版陷阱

- **中英混排时的间距**：中文与英文之间建议加半角空格，例如 "使用 GRPO 训练" 而非 "使用GRPO训练"。
- **等宽字体中的中文**：JetBrains Mono 不覆盖中文字符，Noto Sans SC 字符宽度与拉丁字符不等宽，视觉上会有不齐——这是预期行为，不要强制拉伸。
- **标点符号**：中文正文优先使用中文标点（，。："），但表格和紧凑列表中保留英文标点避免视觉拥挤。
- **数字**：始终使用阿拉伯数字，不要用中文数字（"3 次运行" 而非 "三次运行"）。
