# 模型模板参考

常用机器学习/深度学习模型的代码模板和配置。

---

## 图像模型 (PyTorch)

### ResNet 分类

```python
import torch
import torch.nn as nn
from torchvision import models

def create_resnet(num_classes=10, model_name='resnet18', pretrained=False):
    """创建 ResNet 分类模型"""
    weights = models.ResNet18_Weights.IMAGENET1K_V1 if pretrained else None
    model = models.__dict__[model_name](weights=weights)
    
    # 替换最后的全连接层
    in_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.4),
        nn.Linear(in_features, num_classes)
    )
    return model

# 使用
model = create_resnet(num_classes=10, model_name='resnet18', pretrained=True)
```

### ViT (Vision Transformer)

```python
from transformers import ViTForImageClassification

def create_vit(num_classes=10, model_name='google/vit-base-patch16-224'):
    """创建 ViT 分类模型"""
    model = ViTForImageClassification.from_pretrained(
        model_name,
        num_labels=num_classes,
        ignore_mismatched_sizes=True
    )
    return model
```

### CNN 自定义

```python
class SimpleCNN(nn.Module):
    """简单 CNN，适用于小图像数据集"""
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(128, num_classes)
        )
    
    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)
```

---

## NLP 模型

### BERT 分类

```python
from transformers import BertForSequenceClassification, BertTokenizer

def create_bert_classifier(num_labels=2, model_name='bert-base-chinese'):
    """创建 BERT 分类模型"""
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(
        model_name,
        num_labels=num_labels
    )
    return model, tokenizer

# 使用
model, tokenizer = create_bert_classifier(num_labels=2)
```

### LSTM 文本分类

```python
class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim=300, hidden_dim=128, 
                 num_classes=2, num_layers=2, dropout=0.3):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(
            embed_dim, hidden_dim, num_layers=num_layers,
            batch_first=True, dropout=dropout if num_layers > 1 else 0,
            bidirectional=True
        )
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim * 2, num_classes)
    
    def forward(self, x, lengths=None):
        embedded = self.embedding(x)
        packed = nn.utils.rnn.pack_padded_sequence(
            embedded, lengths.cpu(), batch_first=True, enforce_sorted=False
        ) if lengths else embedded
        output, (hidden, cell) = self.lstm(packed if lengths else embedded)
        hidden = torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1)
        return self.fc(self.dropout(hidden))
```

### Transformer Encoder

```python
class TransformerClassifier(nn.Module):
    def __init__(self, vocab_size, d_model=512, nhead=8, num_layers=6,
                 num_classes=2, dropout=0.1, max_len=512):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model, padding_idx=0)
        self.pos_encoder = nn.Parameter(torch.randn(1, max_len, d_model) * 0.02)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=nhead, dim_feedforward=d_model*4,
            dropout=dropout, batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.classifier = nn.Linear(d_model, num_classes)
        self.d_model = d_model
    
    def forward(self, x, mask=None):
        seq_len = x.size(1)
        embedded = self.embedding(x) * math.sqrt(self.d_model)
        pos = self.pos_encoder[:, :seq_len, :]
        output = self.transformer(embedded + pos, src_key_padding_mask=mask)
        cls_output = output.mean(dim=1)  # 平均池化
        return self.classifier(cls_output)
```

---

## 表格数据模型

### MLP 分类/回归

```python
class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dims=[128, 64], num_classes=1, 
                 dropout=0.3, activation='relu'):
        super().__init__()
        layers = []
        prev_dim = input_dim
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.BatchNorm1d(hidden_dim),
                nn.ReLU() if activation == 'relu' else nn.GELU(),
                nn.Dropout(dropout)
            ])
            prev_dim = hidden_dim
        
        layers.append(nn.Linear(prev_dim, num_classes))
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x)
```

### TabNet (简化版)

```python
class TabNet(nn.Module):
    """简化版 TabNet，适用于表格数据"""
    def __init__(self, input_dim, output_dim, d_model=64, n_steps=3, dropout=0.1):
        super().__init__()
        self.input_bn = nn.BatchNorm1d(input_dim)
        self.steps = nn.ModuleList()
        for _ in range(n_steps):
            self.steps.append(nn.Sequential(
                nn.Linear(input_dim, d_model),
                nn.BatchNorm1d(d_model),
                nn.ReLU(),
                nn.Dropout(dropout)
            ))
        self.output = nn.Linear(d_model * n_steps, output_dim)
    
    def forward(self, x):
        x = self.input_bn(x)
        outputs = []
        for step in self.steps:
            x = step(x)
            outputs.append(x)
        return self.output(torch.cat(outputs, dim=1))
```

---

## 时间序列模型

### LSTM 预测

```python
class LSTMPredictor(nn.Module):
    def __init__(self, input_size=1, hidden_size=128, num_layers=2,
                 prediction_horizon=5, dropout=0.2):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size, hidden_size, num_layers=num_layers,
            batch_first=True, dropout=dropout if num_layers > 1 else 0
        )
        self.fc = nn.Linear(hidden_size, prediction_horizon)
    
    def forward(self, x):
        # x: [batch, seq_len, features]
        lstm_out, _ = self.lstm(x)
        last_output = lstm_out[:, -1, :]  # 取最后一步
        return self.fc(last_output)
```

### Temporal CNN

```python
class TCN(nn.Module):
    def __init__(self, input_size, num_channels=[64, 128, 256], 
                 kernel_size=3, dropout=0.2):
        super().__init__()
        layers = []
        for i, channels in enumerate(num_channels):
            dilation = 2 ** i
            padding = (kernel_size - 1) * dilation
            layers.extend([
                nn.Conv1d(input_size if i == 0 else num_channels[i-1], 
                         channels, kernel_size, padding=padding, dilation=dilation),
                nn.BatchNorm1d(channels),
                nn.ReLU(),
                nn.Dropout(dropout)
            ])
        self.network = nn.Sequential(*layers)
        self.global_pool = nn.AdaptiveAvgPool1d(1)
    
    def forward(self, x):
        # x: [batch, features, seq_len]
        x = self.network(x)
        return self.global_pool(x).squeeze(-1)
```

---

## 通用组件

### 训练循环模板

```python
def train_one_epoch(model, dataloader, optimizer, criterion, device, epoch):
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    for batch_idx, (data, target) in enumerate(dataloader):
        data, target = data.to(device), target.to(device)
        
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        pred = output.argmax(dim=1)
        correct += pred.eq(target).sum().item()
        total += target.size(0)
    
    avg_loss = total_loss / len(dataloader)
    accuracy = 100. * correct / total
    print(f'Epoch {epoch}: Loss={avg_loss:.4f}, Acc={accuracy:.2f}%')
    return avg_loss, accuracy
```

### 评估函数

```python
@torch.no_grad()
def evaluate(model, dataloader, criterion, device):
    model.eval()
    total_loss = 0
    all_preds = []
    all_targets = []
    
    for data, target in dataloader:
        data, target = data.to(device), target.to(device)
        output = model(data)
        total_loss += criterion(output, target).item()
        all_preds.extend(output.argmax(dim=1).cpu().numpy())
        all_targets.extend(target.cpu().numpy())
    
    from sklearn.metrics import accuracy_score, precision_recall_fscore_support
    accuracy = accuracy_score(all_targets, all_preds)
    precision, recall, f1, _ = precision_recall_fscore_support(
        all_targets, all_preds, average='weighted'
    )
    
    return {
        'loss': total_loss / len(dataloader),
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }
```

---

## 选择指南

| 任务类型 | 数据规模 | 推荐模型 |
|----------|----------|----------|
| 图像分类 (<10k) | 小 | ResNet-18/34 |
| 图像分类 (>100k) | 大 | ResNet-50, ViT |
| 文本分类 | 任意 | BERT, RoBERTa |
| 文本生成 | 大 | GPT, T5 |
| 表格分类 | 小 (<10k) | XGBoost, LightGBM |
| 表格分类 | 大 | MLP, TabNet |
| 时间序列 | 任意 | LSTM, TCN, Transformer |
| 无标签数据 | 任意 | KMeans, Autoencoder |
