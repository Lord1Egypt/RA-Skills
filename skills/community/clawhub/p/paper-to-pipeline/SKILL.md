---
name: paper-to-pipeline
description: 根据机器学习/深度学习论文的实验规划文档自动生成完整的 Python 实验 pipeline。支持数据预处理、模型构建、训练循环、评估指标、结果可视化。Use when user uploads an experiment plan document and wants to generate runnable PyTorch/TensorFlow/scikit-learn code.
---

# Paper to Pipeline

根据实验规划文档自动生成机器学习/深度学习实验的完整 Python 代码。

## 触发场景

用户上传实验规划文档（Markdown/PDF/TXT），包含以下内容时触发：
- 数据集描述
- 模型架构
- 训练配置（学习率、batch size、epoch 数）
- 评估指标
- 实验步骤

## 工作流程

### 1. 解析实验规划

读取用户上传的实验规划文档，提取关键信息：
- 数据集类型（图像/文本/表格/时间序列）
- 模型类型（CNN/RNN/Transformer/MLP 等）
- 训练参数
- 评估指标

### 2. 选择代码模板

根据实验类型选择对应的模板：
- **图像分类** → `assets/templates/image_classification.py`
- **文本分类** → `assets/templates/text_classification.py`
- **回归预测** → `assets/templates/regression.py`
- **聚类分析** → `assets/templates/clustering.py`
- **自定义架构** → 根据描述动态生成

### 3. 生成 Pipeline

生成包含以下模块的完整代码：

```python
# 1. 数据加载与预处理
# 2. 模型定义
# 3. 训练循环
# 4. 验证/测试
# 5. 评估指标计算
# 6. 结果可视化
# 7. 模型保存/加载
```

### 4. 输出文件结构

```
generated_experiment/
├── main.py              # 主入口
├── dataset.py           # 数据加载
├── model.py             # 模型定义
├── train.py             # 训练逻辑
├── evaluate.py          # 评估逻辑
├── config.yaml          # 配置文件
├── requirements.txt     # 依赖
└── README.md            # 使用说明
```

## 参考文档

- **数据格式规范**：详见 `references/data-format.md`
- **常用模型模板**：详见 `references/model-templates.md`
- **训练最佳实践**：详见 `references/training-best-practices.md`

## 代码生成规则

### 框架选择优先级

1. 用户明确指定 → 使用指定框架
2. 图像任务 → PyTorch + torchvision
3. NLP 任务 → PyTorch + transformers 或 TensorFlow
4. 表格数据 → scikit-learn 或 PyTorch
5. 时间序列 → PyTorch 或 TensorFlow

### 默认配置

```yaml
framework: pytorch
device: cuda if available else cpu
batch_size: 32
learning_rate: 0.001
epochs: 100
optimizer: adamw
loss: cross_entropy (分类) / mse (回归)
metrics: [accuracy, precision, recall, f1] (分类) / [mae, rmse] (回归)
```

## 使用示例

### 示例 1：图像分类

用户上传：
```
实验目标：CIFAR-10 图像分类
模型：ResNet-18
数据增强：随机翻转、随机裁剪
优化器：AdamW, lr=0.0001
训练：100 epochs, batch_size=64
评估指标：Top-1 Accuracy
```

生成：完整的 ResNet-18 训练 pipeline，包含数据增强

### 示例 2：文本情感分析

用户上传：
```
任务：电影评论情感分析（二分类）
模型：BERT-base-chinese
数据集：ChnSentiCorp
batch_size: 16
epochs: 5
```

生成：基于 HuggingFace transformers 的 BERT 微调代码

### 示例 3：时间序列预测

用户上传：
```
任务：股票价格预测
输入：过去 60 天的收盘价
输出：未来 5 天的预测
模型：LSTM (2 层，hidden=128)
```

生成：LSTM 时间序列预测 pipeline

## 注意事项

1. **代码可运行性**：生成的代码必须可直接运行，包含所有必要的 import
2. **配置分离**：超参数放入 config.yaml，便于调整
3. **日志记录**：包含训练进度日志和 TensorBoard 支持
4. **异常处理**：关键位置添加 try-catch 和错误提示
5. **注释充分**：关键代码段添加中文注释

## 相关文件

- `scripts/generate_pipeline.py` - 代码生成主脚本
- `references/data-format.md` - 数据格式规范
- `references/model-templates.md` - 模型模板参考
- `assets/templates/` - 代码模板文件
