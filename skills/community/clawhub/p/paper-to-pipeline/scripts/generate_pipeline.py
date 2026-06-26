#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paper to Pipeline - 实验代码生成器

根据实验规划文档生成完整的 Python 机器学习/深度学习实验代码。

Usage:
    python generate_pipeline.py --plan <path_to_plan.md> --output <output_dir>
"""

import argparse
import os
import re
import yaml
from pathlib import Path
from datetime import datetime


def parse_experiment_plan(plan_path):
    """解析实验规划文档，提取配置信息"""
    with open(plan_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    config = {
        'task_type': 'classification',
        'dataset': {},
        'model': {},
        'training': {},
        'augmentation': [],
        'metrics': [],
        'environment': {},
    }
    
    # 解析任务类型
    task_match = re.search(r'任务类型 [:\s\n]+(.+?)(?:\n\n|\n##|$)', content, re.IGNORECASE)
    if task_match:
        task_text = task_match.group(1).lower()
        if '二分类' in task_text or 'binary' in task_text:
            config['task_type'] = 'binary_classification'
        elif '多分类' in task_text or 'multi' in task_text:
            config['task_type'] = 'multi_classification'
        elif '回归' in task_text or 'regression' in task_text:
            config['task_type'] = 'regression'
        elif '聚类' in task_text or 'clustering' in task_text:
            config['task_type'] = 'clustering'
        elif '检测' in task_text or 'detection' in task_text:
            config['task_type'] = 'detection'
        elif '分割' in task_text or 'segmentation' in task_text:
            config['task_type'] = 'segmentation'
    
    # 解析数据集
    dataset_section = re.search(r'数据集 [:\s\n](.+?)(?:\n\n|\n## 3|$)', content, re.DOTALL)
    if dataset_section:
        ds_text = dataset_section.group(1)
        name_match = re.search(r'名称 [:\s]+(.+)', ds_text)
        type_match = re.search(r'类型 [:\s]+(.+)', ds_text)
        scale_match = re.search(r'规模 [:\s]+(.+)', ds_text)
        input_match = re.search(r'输入形状 [:\s]+\[([^\]]+)\]', ds_text)
        output_match = re.search(r'输出形状 [:\s]+(.+)', ds_text)
        
        config['dataset'] = {
            'name': name_match.group(1).strip() if name_match else 'unknown',
            'type': type_match.group(1).strip() if type_match else 'unknown',
            'scale': scale_match.group(1).strip() if scale_match else 'unknown',
            'input_shape': input_match.group(1).strip() if input_match else None,
            'output_shape': output_match.group(1).strip() if output_match else None,
        }
    
    # 解析模型
    model_section = re.search(r'模型架构 [:\s\n](.+?)(?:\n\n|\n## 4|$)', content, re.DOTALL)
    if model_section:
        m_text = model_section.group(1)
        backbone_match = re.search(r'backbone[:\s]+(.+)', m_text)
        layers_match = re.search(r'层数 [:\s]+(\d+)', m_text)
        hidden_match = re.search(r'隐藏 [^\d]*(\d+)', m_text)
        
        config['model'] = {
            'backbone': backbone_match.group(1).strip() if backbone_match else 'resnet18',
            'num_layers': int(layers_match.group(1)) if layers_match else None,
            'hidden_size': int(hidden_match.group(1)) if hidden_match else 128,
        }
    
    # 解析训练配置
    train_section = re.search(r'训练配置 [:\s\n](.+?)(?:\n\n|\n## 5|$)', content, re.DOTALL)
    if train_section:
        t_text = train_section.group(1)
        optimizer_match = re.search(r'优化器 [:\s]+(.+)', t_text)
        lr_match = re.search(r'学习率 [:\s]+([0-9e.-]+)', t_text)
        batch_match = re.search(r'[Bb]atch [Ss]ize[:\s]+(\d+)', t_text)
        epochs_match = re.search(r'[Ee]pochs?[:\s]+(\d+)', t_text)
        loss_match = re.search(r'[Ll]oss[^\w]+(.+)', t_text)
        
        config['training'] = {
            'optimizer': optimizer_match.group(1).strip().lower() if optimizer_match else 'adamw',
            'learning_rate': float(lr_match.group(1)) if lr_match else 0.001,
            'batch_size': int(batch_match.group(1)) if batch_match else 32,
            'epochs': int(epochs_match.group(1)) if epochs_match else 100,
            'loss': loss_match.group(1).strip().lower() if loss_match else 'cross_entropy',
        }
    
    # 解析评估指标
    metrics_section = re.search(r'评估指标 [:\s\n](.+?)(?:\n\n|\n##|$)', content, re.DOTALL)
    if metrics_section:
        metrics_text = metrics_section.group(1)
        config['metrics'] = re.findall(r'[\u4e00-\u9fa5a-zA-Z][\u4e00-\u9fa5a-zA-Z0-9_-]*', metrics_text)
    
    return config


def generate_main_py(config):
    """生成 main.py"""
    return f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{config['dataset'].get('name', 'Experiment')} - 实验主入口
自动生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

import os
import yaml
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from tqdm import tqdm
from pathlib import Path

from dataset import create_dataset, get_dataloaders
from model import create_model
from train import train_one_epoch, validate
from evaluate import evaluate_metrics
from config import Config


def main():
    # 加载配置
    config = Config()
    print("=" * 50)
    print("实验配置")
    print("=" * 50)
    print(f"任务类型：{config.task_type}")
    print(f"数据集：{config.dataset_name}")
    print(f"模型：{config.model_name}")
    print(f"设备：{{'cuda' if torch.cuda.is_available() else 'cpu'}}")
    print("=" * 50)
    
    # 设置设备
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # 创建数据加载器
    print("加载数据集...")
    train_loader, val_loader, test_loader = get_dataloaders(
        batch_size=config.batch_size,
        num_workers=4
    )
    
    # 创建模型
    print("创建模型...")
    model = create_model(
        model_name=config.model_name,
        num_classes=config.num_classes,
        pretrained=config.pretrained
    ).to(device)
    
    # 创建优化器和损失函数
    if config.optimizer.lower() == 'adamw':
        optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=config.learning_rate,
            weight_decay=0.01
        )
    elif config.optimizer.lower() == 'adam':
        optimizer = torch.optim.Adam(
            model.parameters(),
            lr=config.learning_rate
        )
    elif config.optimizer.lower() == 'sgd':
        optimizer = torch.optim.SGD(
            model.parameters(),
            lr=config.learning_rate,
            momentum=0.9,
            weight_decay=1e-4
        )
    else:
        optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    
    # 学习率调度器
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=config.epochs
    )
    
    # 损失函数
    if config.task_type in ['binary_classification', 'multi_classification']:
        criterion = nn.CrossEntropyLoss()
    elif config.task_type == 'regression':
        criterion = nn.MSELoss()
    else:
        criterion = nn.CrossEntropyLoss()
    
    # 训练循环
    best_val_acc = 0.0
    save_dir = Path('checkpoints')
    save_dir.mkdir(exist_ok=True)
    
    print("\\n开始训练...")
    for epoch in range(1, config.epochs + 1):
        print(f"\\nEpoch {{epoch}}/{{config.epochs}}")
        print("-" * 40)
        
        # 训练
        train_loss, train_acc = train_one_epoch(
            model, train_loader, optimizer, criterion, device, epoch
        )
        
        # 验证
        val_loss, val_acc = validate(
            model, val_loader, criterion, device
        )
        
        # 更新学习率
        scheduler.step()
        
        # 保存最佳模型
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save({{
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_acc': val_acc,
            }}, save_dir / 'best_model.pth')
            print(f"✓ 保存最佳模型 (val_acc={{val_acc:.4f}})")
    
    # 测试集评估
    print("\\n在测试集上评估...")
    model.load_state_dict(torch.load(save_dir / 'best_model.pth')['model_state_dict'])
    test_metrics = evaluate_metrics(model, test_loader, device, config.task_type)
    
    print("\\n" + "=" * 50)
    print("最终结果")
    print("=" * 50)
    for k, v in test_metrics.items():
        print(f"{{k}}: {{v:.4f}}")
    print("=" * 50)
    
    print("\\n实验完成!")


if __name__ == '__main__':
    main()
'''


def generate_config_py(config):
    """生成 config.py"""
    dataset_info = config.get('dataset', {})
    model_info = config.get('model', {})
    training_info = config.get('training', {})
    
    # 根据任务类型推断类别数
    output_shape = dataset_info.get('output_shape', 'num_classes=10')
    num_classes_match = re.search(r'num_classes[=:]?\\s*(\\d+)', output_shape)
    num_classes = int(num_classes_match.group(1)) if num_classes_match else 10
    
    return f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实验配置文件
"""

class Config:
    # 任务类型
    task_type = "{config.get('task_type', 'classification')}"
    
    # 数据集配置
    dataset_name = "{dataset_info.get('name', 'unknown')}"
    dataset_type = "{dataset_info.get('type', 'image')}"
    num_classes = {num_classes}
    
    # 模型配置
    model_name = "{model_info.get('backbone', 'resnet18')}"
    pretrained = True
    
    # 训练配置
    batch_size = {training_info.get('batch_size', 32)}
    learning_rate = {training_info.get('learning_rate', 0.001)}
    epochs = {training_info.get('epochs', 100)}
    optimizer = "{training_info.get('optimizer', 'adamw')}"
    
    # 数据增强
    use_augmentation = True
    
    # 其他配置
    num_workers = 4
    seed = 42
    log_interval = 10
'''


def generate_dataset_py(config):
    """生成 dataset.py"""
    dataset_type = config.get('dataset', {}).get('type', 'image')
    
    if dataset_type == 'image':
        return '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据加载模块
"""

import torch
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, datasets
from pathlib import Path


def get_transforms(augment=True, image_size=224):
    """获取数据变换"""
    normalize = transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
    
    if augment:
        train_transform = transforms.Compose([
            transforms.RandomResizedCrop(image_size),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            normalize,
        ])
    else:
        train_transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(image_size),
            transforms.ToTensor(),
            normalize,
        ])
    
    val_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(image_size),
        transforms.ToTensor(),
        normalize,
    ])
    
    return train_transform, val_transform


def create_dataset(root='data', augment=True):
    """创建数据集"""
    train_transform, val_transform = get_transforms(augment)
    
    train_dataset = datasets.ImageFolder(
        Path(root) / 'train',
        transform=train_transform
    )
    val_dataset = datasets.ImageFolder(
        Path(root) / 'val',
        transform=val_transform
    )
    test_dataset = datasets.ImageFolder(
        Path(root) / 'test',
        transform=val_transform
    )
    
    return train_dataset, val_dataset, test_dataset


def get_dataloaders(batch_size=32, num_workers=4):
    """获取数据加载器"""
    train_dataset, val_dataset, test_dataset = create_dataset()
    
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    
    return train_loader, val_loader, test_loader
'''
    elif dataset_type == 'text':
        return '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本数据加载模块
"""

import torch
from torch.utils.data import DataLoader, Dataset
from transformers import BertTokenizer
from pathlib import Path


class TextDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }


def create_dataset(data_path='data', max_length=128):
    """创建文本数据集"""
    tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
    
    # 读取数据 (假设是 CSV 格式)
    import pandas as pd
    train_df = pd.read_csv(Path(data_path) / 'train.csv')
    val_df = pd.read_csv(Path(data_path) / 'val.csv')
    test_df = pd.read_csv(Path(data_path) / 'test.csv')
    
    train_dataset = TextDataset(
        train_df['text'].values,
        train_df['label'].values,
        tokenizer,
        max_length
    )
    val_dataset = TextDataset(
        val_df['text'].values,
        val_df['label'].values,
        tokenizer,
        max_length
    )
    test_dataset = TextDataset(
        test_df['text'].values,
        test_df['label'].values,
        tokenizer,
        max_length
    )
    
    return train_dataset, val_dataset, test_dataset


def get_dataloaders(batch_size=32, num_workers=4):
    """获取数据加载器"""
    train_dataset, val_dataset, test_dataset = create_dataset()
    
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers
    )
    
    return train_loader, val_loader, test_loader
'''
    else:
        # 通用/表格数据
        return '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用数据加载模块
"""

import torch
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
import numpy as np
from pathlib import Path


def load_data(data_path='data'):
    """加载数据"""
    # 假设数据是 numpy 格式
    X = np.load(Path(data_path) / 'X.npy')
    y = np.load(Path(data_path) / 'y.npy')
    
    # 划分数据集
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42
    )
    
    return (X_train, y_train), (X_val, y_val), (X_test, y_test)


def create_dataset(data_path='data'):
    """创建数据集"""
    (X_train, y_train), (X_val, y_val), (X_test, y_test) = load_data(data_path)
    
    train_dataset = TensorDataset(
        torch.FloatTensor(X_train),
        torch.LongTensor(y_train) if y_train.dtype in [np.int32, np.int64] else torch.FloatTensor(y_train)
    )
    val_dataset = TensorDataset(
        torch.FloatTensor(X_val),
        torch.LongTensor(y_val) if y_val.dtype in [np.int32, np.int64] else torch.FloatTensor(y_val)
    )
    test_dataset = TensorDataset(
        torch.FloatTensor(X_test),
        torch.LongTensor(y_test) if y_test.dtype in [np.int32, np.int64] else torch.FloatTensor(y_test)
    )
    
    return train_dataset, val_dataset, test_dataset


def get_dataloaders(batch_size=32, num_workers=4):
    """获取数据加载器"""
    train_dataset, val_dataset, test_dataset = create_dataset()
    
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers
    )
    
    return train_loader, val_loader, test_loader
'''


def generate_model_py(config):
    """生成 model.py"""
    model_name = config.get('model', {}).get('backbone', 'resnet18').lower()
    num_classes = 10  # 默认值
    
    if 'resnet' in model_name:
        return f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型定义模块
"""

import torch
import torch.nn as nn
from torchvision import models


def create_model(model_name='resnet18', num_classes={num_classes}, pretrained=True):
    """
    创建 ResNet 模型
    
    Args:
        model_name: 模型名称 (resnet18/34/50/101/152)
        num_classes: 分类数量
        pretrained: 是否使用预训练权重
    
    Returns:
        nn.Module: 创建好的模型
    """
    weights = models.ResNet18_Weights.IMAGENET1K_V1 if pretrained else None
    
    if model_name == 'resnet18':
        model = models.resnet18(weights=weights)
    elif model_name == 'resnet34':
        model = models.resnet34(weights=weights)
    elif model_name == 'resnet50':
        model = models.resnet50(weights=weights)
    elif model_name == 'resnet101':
        model = models.resnet101(weights=weights)
    elif model_name == 'resnet152':
        model = models.resnet152(weights=weights)
    else:
        model = models.resnet18(weights=weights)
    
    # 替换最后的全连接层
    in_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.4),
        nn.Linear(in_features, num_classes)
    )
    
    return model


if __name__ == '__main__':
    # 测试模型
    model = create_model()
    x = torch.randn(1, 3, 224, 224)
    y = model(x)
    print(f"输入形状：{{x.shape}}")
    print(f"输出形状：{{y.shape}}")
'''
    elif 'bert' in model_name:
        return f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型定义模块 - BERT
"""

import torch
import torch.nn as nn
from transformers import BertForSequenceClassification, BertTokenizer


def create_model(model_name='bert-base-chinese', num_classes={num_classes}, pretrained=True):
    """
    创建 BERT 分类模型
    
    Args:
        model_name: 模型名称
        num_classes: 分类数量
        pretrained: 是否使用预训练权重
    
    Returns:
        model, tokenizer: 模型和分词器
    """
    tokenizer = BertTokenizer.from_pretrained(model_name)
    
    model = BertForSequenceClassification.from_pretrained(
        model_name,
        num_labels=num_classes,
        ignore_mismatched_sizes=not pretrained
    )
    
    return model, tokenizer


if __name__ == '__main__':
    # 测试模型
    model, tokenizer = create_model()
    
    text = "这是一个测试句子"
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=128)
    
    outputs = model(**inputs)
    print(f"输入形状：{{inputs['input_ids'].shape}}")
    print(f"输出形状：{{outputs.logits.shape}}")
'''
    else:
        # 通用模型
        return f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型定义模块
"""

import torch
import torch.nn as nn


class MLP(nn.Module):
    """多层感知机"""
    def __init__(self, input_dim, hidden_dims=[128, 64], num_classes={num_classes}, dropout=0.3):
        super().__init__()
        layers = []
        prev_dim = input_dim
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.BatchNorm1d(hidden_dim),
                nn.ReLU(),
                nn.Dropout(dropout)
            ])
            prev_dim = hidden_dim
        
        layers.append(nn.Linear(prev_dim, num_classes))
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x)


def create_model(input_dim=None, hidden_dims=[128, 64], num_classes={num_classes}, dropout=0.3):
    """
    创建模型
    
    Args:
        input_dim: 输入维度
        hidden_dims: 隐藏层维度列表
        num_classes: 分类数量
        dropout: Dropout 比例
    
    Returns:
        nn.Module: 创建好的模型
    """
    return MLP(input_dim=input_dim or 784, hidden_dims=hidden_dims, 
               num_classes=num_classes, dropout=dropout)


if __name__ == '__main__':
    # 测试模型
    model = create_model()
    x = torch.randn(1, 784)
    y = model(x)
    print(f"输入形状：{{x.shape}}")
    print(f"输出形状：{{y.shape}}")
'''


def generate_train_py(config):
    """生成 train.py"""
    return '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
训练模块
"""

import torch
from tqdm import tqdm


def train_one_epoch(model, dataloader, optimizer, criterion, device, epoch):
    """
    训练一个 epoch
    
    Args:
        model: 模型
        dataloader: 数据加载器
        optimizer: 优化器
        criterion: 损失函数
        device: 设备
        epoch: 当前 epoch
    
    Returns:
        avg_loss, accuracy: 平均损失和准确率
    """
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    pbar = tqdm(dataloader, desc=f'Training Epoch {epoch}')
    for batch_idx, (data, target) in enumerate(pbar):
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
        
        if batch_idx % 10 == 0:
            pbar.set_postfix({
                'loss': f'{loss.item():.4f}',
                'acc': f'{100. * correct / total:.2f}%'
            })
    
    avg_loss = total_loss / len(dataloader)
    accuracy = 100. * correct / total
    
    return avg_loss, accuracy


@torch.no_grad()
def validate(model, dataloader, criterion, device):
    """
    验证模型
    
    Args:
        model: 模型
        dataloader: 数据加载器
        criterion: 损失函数
        device: 设备
    
    Returns:
        avg_loss, accuracy: 平均损失和准确率
    """
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    
    for data, target in tqdm(dataloader, desc='Validating'):
        data, target = data.to(device), target.to(device)
        output = model(data)
        total_loss += criterion(output, target).item()
        pred = output.argmax(dim=1)
        correct += pred.eq(target).sum().item()
        total += target.size(0)
    
    avg_loss = total_loss / len(dataloader)
    accuracy = 100. * correct / total
    
    return avg_loss, accuracy
'''


def generate_evaluate_py(config):
    """生成 evaluate.py"""
    return '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
评估模块
"""

import torch
import numpy as np
from tqdm import tqdm
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report,
    mean_absolute_error, mean_squared_error, r2_score
)


@torch.no_grad()
def evaluate_metrics(model, dataloader, device, task_type='classification'):
    """
    评估模型指标
    
    Args:
        model: 模型
        dataloader: 数据加载器
        device: 设备
        task_type: 任务类型 (classification/regression)
    
    Returns:
        metrics: 评估指标字典
    """
    model.eval()
    all_preds = []
    all_targets = []
    
    for data, target in tqdm(dataloader, desc='Evaluating'):
        data = data.to(device)
        output = model(data)
        
        if task_type == 'regression':
            preds = output.cpu().numpy().flatten()
        else:
            preds = output.argmax(dim=1).cpu().numpy()
        
        all_preds.extend(preds)
        all_targets.extend(target.numpy())
    
    all_preds = np.array(all_preds)
    all_targets = np.array(all_targets)
    
    metrics = {}
    
    if task_type == 'regression':
        metrics['mae'] = float(mean_absolute_error(all_targets, all_preds))
        metrics['rmse'] = float(np.sqrt(mean_squared_error(all_targets, all_preds)))
        metrics['r2'] = float(r2_score(all_targets, all_preds))
    else:
        metrics['accuracy'] = float(accuracy_score(all_targets, all_preds))
        metrics['precision'] = float(precision_score(all_targets, all_preds, average='weighted', zero_division=0))
        metrics['recall'] = float(recall_score(all_targets, all_preds, average='weighted', zero_division=0))
        metrics['f1'] = float(f1_score(all_targets, all_preds, average='weighted', zero_division=0))
        
        # 混淆矩阵
        cm = confusion_matrix(all_targets, all_preds)
        metrics['confusion_matrix'] = cm.tolist()
        
        # 分类报告
        print("\\n分类报告:")
        print(classification_report(all_targets, all_preds, zero_division=0))
    
    return metrics
'''


def generate_requirements(config):
    """生成 requirements.txt"""
    base_deps = [
        'torch>=2.0.0',
        'torchvision>=0.15.0',
        'numpy>=1.24.0',
        'pandas>=2.0.0',
        'scikit-learn>=1.3.0',
        'tqdm>=4.65.0',
        'pyyaml>=6.0',
    ]
    
    dataset_type = config.get('dataset', {}).get('type', 'image')
    model_name = config.get('model', {}).get('backbone', '').lower()
    
    if dataset_type == 'text' or 'bert' in model_name:
        base_deps.extend([
            'transformers>=4.30.0',
            'tokenizers>=0.13.0',
        ])
    
    return '\n'.join(base_deps)


def generate_readme(config):
    """生成 README.md"""
    return f'''# {config['dataset'].get('name', 'Experiment')} 实验代码

自动生成时间：{datetime.now().strftime('%Y-%m-%d')}

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 准备数据

将数据按以下结构组织：

```
data/
├── train/
│   ├── class1/
│   └── class2/
├── val/
│   ├── class1/
│   └── class2/
└── test/
    ├── class1/
    └── class2/
```

### 3. 运行实验

```bash
python main.py
```

## 配置

编辑 `config.py` 修改实验参数：

- `batch_size`: 批次大小
- `learning_rate`: 学习率
- `epochs`: 训练轮数
- `model_name`: 模型名称

## 输出

- `checkpoints/best_model.pth`: 最佳模型权重
- 训练日志输出到控制台

## 实验配置

| 配置项 | 值 |
|--------|-----|
| 任务类型 | {config.get('task_type', 'classification')} |
| 数据集 | {config['dataset'].get('name', 'unknown')} |
| 模型 | {config['model'].get('backbone', 'resnet18')} |
| 学习率 | {config['training'].get('learning_rate', 0.001)} |
| Batch Size | {config['training'].get('batch_size', 32)} |
| Epochs | {config['training'].get('epochs', 100)} |
'''


def generate_pipeline(plan_path, output_dir):
    """主函数：生成完整 pipeline"""
    print(f"解析实验规划：{plan_path}")
    config = parse_experiment_plan(plan_path)
    
    print(f"创建输出目录：{output_dir}")
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    files = {
        'main.py': generate_main_py(config),
        'config.py': generate_config_py(config),
        'dataset.py': generate_dataset_py(config),
        'model.py': generate_model_py(config),
        'train.py': generate_train_py(config),
        'evaluate.py': generate_evaluate_py(config),
        'requirements.txt': generate_requirements(config),
        'README.md': generate_readme(config),
    }
    
    for filename, content in files.items():
        filepath = output_path / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ 生成 {filename}")
    
    print(f"\\n✅ 实验 pipeline 生成完成！")
    print(f"输出目录：{output_path.absolute()}")
    print(f"\\n下一步：")
    print(f"  1. cd {output_path}")
    print(f"  2. pip install -r requirements.txt")
    print(f"  3. 准备数据")
    print(f"  4. python main.py")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='根据实验规划生成 Python 代码')
    parser.add_argument('--plan', required=True, help='实验规划文档路径')
    parser.add_argument('--output', required=True, help='输出目录')
    
    args = parser.parse_args()
    generate_pipeline(args.plan, args.output)
'''
