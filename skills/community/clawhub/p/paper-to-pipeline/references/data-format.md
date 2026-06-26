# 数据格式规范

本文档定义实验规划文档的标准格式，便于代码生成器解析。

---

## 标准格式模板

```markdown
# 实验规划

## 1. 任务类型
- 分类 / 回归 / 聚类 / 目标检测 / 分割 / 生成

## 2. 数据集
- 名称：[数据集名称]
- 类型：图像 / 文本 / 表格 / 时间序列 / 音频
- 规模：[样本数量]
- 输入形状：[例如：224x224x3, sequence_length=512]
- 输出形状：[例如：num_classes=10, 1]
- 预处理要求：[归一化、标准化、分词等]

## 3. 模型架构
-  backbone: [ResNet-18 / BERT / LSTM / 自定义]
-  层数：[可选]
-  隐藏层维度：[可选]
-  特殊组件：[Attention / Dropout / BatchNorm 等]

## 4. 训练配置
- 优化器：[Adam / AdamW / SGD]
- 学习率：[数值]
- 学习率调度：[StepLR / CosineAnnealing / ReduceLROnPlateau]
- Batch Size: [数值]
- Epochs: [数值]
- Loss 函数：[CrossEntropy / MSE / BCE / 自定义]

## 5. 数据增强（如适用）
- [随机翻转 / 随机裁剪 / 颜色抖动 / Mixup / CutMix]

## 6. 评估指标
- [Accuracy / Precision / Recall / F1 / MAE / RMSE / IoU]

## 7. 实验环境
- 框架：[PyTorch / TensorFlow / scikit-learn]
- GPU 要求：[是/否]
- 其他依赖：[transformers / torchvision 等]

## 8. 输出要求
- [模型保存格式 / 日志格式 / 可视化要求]
```

---

## 字段详解

### 任务类型

| 类型 | 代码模板 | 默认 Loss | 默认指标 |
|------|----------|-----------|----------|
| 二分类 | classification_binary | BCE | Accuracy, F1 |
| 多分类 | classification_multi | CrossEntropy | Accuracy, Precision, Recall, F1 |
| 回归 | regression | MSE | MAE, RMSE, R² |
| 聚类 | clustering | - | Silhouette, Inertia |
| 目标检测 | detection | COCO losses | mAP |
| 分割 | segmentation | Dice/CrossEntropy | IoU, Dice |

### 数据集类型

#### 图像数据
```yaml
input_shape: [3, 224, 224]  # C, H, W
normalization: [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]  # ImageNet
```

#### 文本数据
```yaml
max_length: 512
tokenizer: bert-base-chinese
padding: max_length
truncation: true
```

#### 表格数据
```yaml
numerical_features: [feature1, feature2, ...]
categorical_features: [cat1, cat2, ...]
target_column: label
```

#### 时间序列
```yaml
sequence_length: 60
prediction_horizon: 5
features: [open, high, low, close, volume]
```

### 模型配置

#### ResNet 变体
```yaml
model: resnet18  # resnet18/34/50/101/152
pretrained: true
num_classes: 10
```

#### Transformer
```yaml
model: bert-base-chinese
num_labels: 2
dropout: 0.1
```

#### LSTM
```yaml
input_size: 1
hidden_size: 128
num_layers: 2
bidirectional: false
dropout: 0.2
```

### 优化器配置

#### Adam/AdamW
```yaml
optimizer: adamw
lr: 0.001
betas: [0.9, 0.999]
weight_decay: 0.01
```

#### SGD
```yaml
optimizer: sgd
lr: 0.01
momentum: 0.9
weight_decay: 0.0001
```

### 学习率调度

```yaml
scheduler:
  type: CosineAnnealingLR  # StepLR / CosineAnnealingLR / ReduceLROnPlateau
  T_max: 100  # for CosineAnnealing
  step_size: 30  # for StepLR
  gamma: 0.1
  patience: 5  # for ReduceLROnPlateau
```

---

## 解析规则

1. **必填字段**：任务类型、数据集、模型架构、训练配置
2. **可选字段**：数据增强、实验环境、输出要求
3. **默认值**：未指定时使用技能中定义的默认配置
4. **冲突处理**：用户指定优先于默认值

---

## 示例文档

### 示例 1：CIFAR-10 分类

```markdown
# 实验规划

## 1. 任务类型
- 多分类（10 类）

## 2. 数据集
- 名称：CIFAR-10
- 类型：图像
- 规模：60000 (50000 训练 / 10000 测试)
- 输入形状：[3, 32, 32]
- 输出形状：num_classes=10

## 3. 模型架构
- backbone: ResNet-18
- pretrained: false
- num_classes: 10

## 4. 训练配置
- 优化器：AdamW
- 学习率：0.0001
- Batch Size: 64
- Epochs: 100
- Loss: CrossEntropy

## 5. 数据增强
- 随机水平翻转 (p=0.5)
- 随机裁剪 (padding=4)
- 归一化：ImageNet

## 6. 评估指标
- Top-1 Accuracy
- Confusion Matrix

## 7. 实验环境
- 框架：PyTorch
- GPU: 是
```

### 示例 2：BERT 情感分析

```markdown
# 实验规划

## 1. 任务类型
- 二分类（正面/负面）

## 2. 数据集
- 名称：ChnSentiCorp
- 类型：文本
- 规模：12000
- max_length: 128

## 3. 模型架构
- model: bert-base-chinese
- num_labels: 2
- dropout: 0.1

## 4. 训练配置
- 优化器：AdamW
- 学习率：2e-5
- Batch Size: 16
- Epochs: 5
- Loss: CrossEntropy

## 5. 评估指标
- Accuracy
- Precision
- Recall
- F1
```
