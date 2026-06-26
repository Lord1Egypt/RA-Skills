#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图像分类实验模板
基于 PyTorch + ResNet
"""

import torch
import torch.nn as nn
from torchvision import models, transforms
from torch.utils.data import DataLoader
from pathlib import Path


# ==================== 配置 ====================

CONFIG = {
    'data_root': 'data',
    'model_name': 'resnet18',
    'num_classes': 10,
    'batch_size': 32,
    'learning_rate': 0.001,
    'epochs': 100,
    'image_size': 224,
}


# ==================== 数据变换 ====================

def get_transforms(image_size=224):
    """获取训练和验证的数据变换"""
    normalize = transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
    
    train_transform = transforms.Compose([
        transforms.RandomResizedCrop(image_size),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
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


# ==================== 模型 ====================

def create_model(model_name='resnet18', num_classes=10, pretrained=True):
    """创建 ResNet 模型"""
    weights = models.ResNet18_Weights.IMAGENET1K_V1 if pretrained else None
    model = models.__dict__.get(model_name, models.resnet18)(weights=weights)
    
    # 替换最后的全连接层
    in_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.4),
        nn.Linear(in_features, num_classes)
    )
    
    return model


# ==================== 训练函数 ====================

def train_one_epoch(model, dataloader, optimizer, criterion, device, epoch):
    """训练一个 epoch"""
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


@torch.no_grad()
def validate(model, dataloader, criterion, device):
    """验证模型"""
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    
    for data, target in dataloader:
        data, target = data.to(device), target.to(device)
        output = model(data)
        total_loss += criterion(output, target).item()
        pred = output.argmax(dim=1)
        correct += pred.eq(target).sum().item()
        total += target.size(0)
    
    avg_loss = total_loss / len(dataloader)
    accuracy = 100. * correct / total
    
    return avg_loss, accuracy


# ==================== 主函数 ====================

def main():
    # 设备
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'使用设备：{device}')
    
    # 数据
    train_transform, val_transform = get_transforms(CONFIG['image_size'])
    
    train_dataset = torch.utils.data.DataLoader(
        # TODO: 替换为实际数据集
        batch_size=CONFIG['batch_size'],
        shuffle=True,
    )
    
    # 模型
    model = create_model(
        CONFIG['model_name'],
        CONFIG['num_classes'],
        pretrained=True
    ).to(device)
    
    # 优化器
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=CONFIG['learning_rate'],
        weight_decay=0.01
    )
    
    # 学习率调度器
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=CONFIG['epochs']
    )
    
    # 损失函数
    criterion = nn.CrossEntropyLoss()
    
    # 训练循环
    best_val_acc = 0.0
    
    for epoch in range(1, CONFIG['epochs'] + 1):
        train_loss, train_acc = train_one_epoch(
            model, train_dataset, optimizer, criterion, device, epoch
        )
        
        # val_loss, val_acc = validate(model, val_loader, criterion, device)
        # scheduler.step()
        
        # if val_acc > best_val_acc:
        #     best_val_acc = val_acc
        #     torch.save(model.state_dict(), 'best_model.pth')
    
    print("训练完成!")


if __name__ == '__main__':
    main()
