# PAO 用户指南

## 简介

PAO (Personal AI Operating System) 是一个跨设备、去中心化的AI协同系统。

## 快速开始

### 安装

```bash
cd pao-system
python deployment/installer.py
```

### 配置

```bash
python deployment/config_wizard.py
```

### 运行

```bash
python -m pao
```

## 核心功能

### 设备发现
PAO会自动发现局域网内的其他PAO设备。

### 技能管理
系统会自动管理和进化AI技能。

### 情境感知
根据使用场景自动调整行为。

### 数据同步
多设备间自动同步数据和状态。

## 故障排除

### 设备无法发现
- 检查网络连接
- 确认防火墙设置
- 重启PAO服务

### 同步失败
- 检查网络延迟
- 确认端口未被占用
- 查看日志获取详细信息
