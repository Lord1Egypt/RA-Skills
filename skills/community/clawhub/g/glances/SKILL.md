---
name: glances
description: Glances - 跨平台系统监控工具
version: 0.1.1
metadata:
  openclaw:
    requires:
      bins:
        - glances
    emoji: 📊
    homepage: https://nicolargo.github.io/glances/
---

# Glances 跨平台系统监控工具

## 技能概述

本技能帮助用户使用 Glances 进行系统性能监控与分析，支持以下场景：
- **实时监控**: 在终端实时查看 CPU、内存、磁盘、网络等资源使用情况
- **Web 界面**: 通过浏览器远程访问系统监控仪表板
- **API 服务**: 通过 REST API 获取系统指标数据，便于集成
- **告警配置**: 设置资源阈值，当超过时自动触发告警
- **导出分析**: 将监控数据导出到 CSV、InfluxDB、Prometheus 等存储系统
- **服务器模式**: 以客户端-服务端模式监控远程主机

**支持平台**: Linux、macOS、Windows、FreeBSD，支持 Docker 容器化部署

## 使用流程

AI 助手将引导你完成以下步骤：
1. 安装 Glances（如未安装）
2. 以合适的模式启动监控（终端/Web/API）
3. 解读监控数据和告警信息
4. 根据需要配置自定义参数
5. 集成到现有工作流或监控系统

## 关键章节导航

- [安装指南](./guides/01-installation.md)
- [快速开始](./guides/02-quickstart.md)
- [高级用法](./guides/03-advanced-usage.md)
- [常见问题](./troubleshooting.md)

## AI 助手能力

当你向 AI 描述监控需求时，AI 会：
- 自动检测系统环境并选择合适的安装方式
- 启动 Glances 并解读当前系统状态
- 识别高负载进程和资源瓶颈
- 配置 Web 服务器模式并提供访问地址
- 设置导出插件将指标写入时序数据库
- 分析告警日志并给出优化建议
- 生成监控配置文件以满足特定需求

## 核心功能

- 实时监控 CPU、内存、磁盘 I/O、网络流量
- 进程列表（支持排序、过滤、终止）
- Web UI 仪表板（内置 HTTP 服务器）
- REST API / XML-RPC API 远程数据获取
- 客户端-服务端模式（通过 SSH 隧道监控远程主机）
- 告警系统（Careful / Warning / Critical 三级）
- 插件化架构（支持 30+ 内置插件）
- 导出支持：CSV、InfluxDB、Prometheus、Elasticsearch、MQTT 等
- Docker 和 Kubernetes 容器监控
- 支持 Python API 二次开发

## 快速示例

```bash
# 启动终端交互模式
glances

# 启动 Web 服务器模式（浏览器访问）
glances -w

# 以服务端模式运行（等待客户端连接）
glances -s

# 连接远程服务端
glances -c 192.168.1.100

# 以 REST API 模式运行
glances -w --disable-webui

# 查看特定进程
glances --process-filter python

# 将数据导出到 CSV
glances --export csv --export-csv-file /tmp/glances.csv

# 静默模式（仅记录日志，无界面）
glances -q --export influxdb
```

## 监控指标说明

| 指标类别 | 描述 | 告警颜色 |
|---------|------|---------|
| CPU 使用率 | 总体和每核心使用率 | 绿/蓝/黄/红 |
| 内存 / Swap | 物理内存和交换空间使用 | 绿/蓝/黄/红 |
| 磁盘 I/O | 读写速率和等待时间 | 绿/蓝/黄/红 |
| 网络接口 | 上下行速率和数据包数 | 绿/蓝/黄/红 |
| 进程列表 | CPU/内存占用最高的进程 | 可排序 |
| 系统负载 | 1/5/15 分钟平均负载 | 绿/蓝/黄/红 |
| 传感器 | CPU 温度（需要硬件支持）| 绿/黄/红 |
| Docker | 容器状态和资源使用 | 绿/红 |

## 告警级别

Glances 使用四种颜色标识资源状态：
- **绿色 (OK)**: 正常，无需关注
- **蓝色 (Careful)**: 需要关注，资源使用偏高
- **黄色 (Warning)**: 警告，资源使用较高
- **红色 (Critical)**: 严重，需要立即处理

默认阈值可通过配置文件 `~/.config/glances/glances.conf` 自定义。

## 安装要求

- Python 3.8 或更高版本
- pip 包管理器
- （可选）psutil >= 5.3.0（核心依赖，通常自动安装）
- （可选）bottles/docker SDK（容器监控）
- （可选）InfluxDB / Prometheus 客户端（数据导出）

## 项目链接

- GitHub: https://github.com/nicolargo/glances
- 官网: https://nicolargo.github.io/glances/
- 文档: https://glances.readthedocs.io/
- Docker Hub: https://hub.docker.com/r/nicolargo/glances
