---
name: goto-cloudserver-manager
version: 1.0.4
description: 多云服务器自动化运维 Skill，支持阿里云/腾讯云/华为云服务器的数据库安装、表结构创建、监控巡检和健康报告
author: GotoPlan Team
license: MIT

trigger_keywords:
  - 云服务器
  - 安装数据库
  - 创建数据库
  - 表结构
  - 建表
  - 服务器状态
  - 巡检报告
  - 健康报告
  - SQL Server
  - MySQL
  - PostgreSQL
  - Redis
  - 阿里云 ECS
  - 腾讯云 CVM
  - 华为云 ECS
  - 服务器监控
  - 数据库健康检查
  - 日志分析
  - 服务重启

capabilities:
  - check_server_status      # 检查服务器 CPU/内存/磁盘/网络状态
  - install_database         # 在云服务器上安装数据库
  - create_database          # 创建数据库实例
  - create_user              # 创建数据库应用账号（需确认）
  - apply_schema             # 根据统一 Schema 创建表结构
  - create_index             # 创建索引（需确认）
  - seed_data                # 初始化基础数据
  - health_check             # 数据库健康检查（含连接数检查）
  - generate_report          # 生成中文健康/运维报告
  - restart_service          # 重启服务（需确认）
  - backup_database          # 备份数据库（需确认）
  - restore_database         # 恢复数据库（需确认）
  - configure_firewall       # 配置操作系统防火墙（需确认）
  - configure_winrm          # 启用并配置 WinRM HTTPS（需确认）
  - install_monitoring_agent # 部署 Windows/Node Exporter（需确认）
  - list_instances           # 列出云服务器实例
  - get_instance              # 获取单个实例详情
  - describe_security_groups  # 查看实例关联的安全组
  - modify_security_group     # 修改安全组规则（需确认）
  - reboot_instance           # 重启云服务器实例（需确认）
  - read_recent_logs         # 读取最近日志

supported_providers:
  - aliyun              # 阿里云 ECS + 云助手
  - tencent             # 腾讯云 CVM + TAT
  - tencent-lighthouse  # 腾讯云轻量应用服务器 + TAT
  - huawei              # 华为云 ECS + SSH

supported_os:
  - windows-server-2019
  - windows-server-2022
  - ubuntu-20.04
  - ubuntu-22.04
  - debian-11
  - debian-12
  - centos-7
  - rocky-linux-9
  - openeuler-22.03

supported_databases:
  - sqlserver   # SQL Server 2019/2022（主要用于 Windows）
  - mysql       # MySQL 8.0
  - postgresql  # PostgreSQL 15/16
  - redis       # Redis 7

entry_point: core/dispatcher.py
config_dir: config/

# OpenClaw 在 /skill install 时自动安装以下依赖，用户无需手动操作
dependencies:
  python: ">=3.9"
  packages:
    # 云厂商 SDK
    - alibabacloud-ecs20140526>=4.0.0
    - alibabacloud-tea-openapi>=0.3.0
    - tencentcloud-sdk-python-cvm>=3.0.0
    - tencentcloud-sdk-python-lighthouse>=3.0.0
    - tencentcloud-sdk-python-tat>=3.0.0
    - tencentcloud-sdk-python-vpc>=3.0.0
    - huaweicloudsdkcore>=3.1.0
    - huaweicloudsdkecs>=3.1.0
    - huaweicloudsdkvpc>=3.1.0
    # 远程执行
    - paramiko>=3.4.0
    - pywinrm>=0.4.3
    # 通用工具
    - pyyaml>=6.0.1
    - python-dotenv>=1.0.0
    - pydantic>=2.5.0
    - jinja2>=3.1.2
    - structlog>=23.0.0

requires_confirmation:
  - install_database
  - create_database
  - create_user
  - apply_schema
  - create_index
  - restart_service
  - install_monitoring_agent
  - configure_firewall
  - modify_firewall
  - configure_winrm
  - modify_security_group
  - backup_database
  - restore_database
  - reboot_instance

forbidden_actions:
  - delete_database
  - drop_table
  - truncate_table
  - format_disk
  - disable_firewall
  - open_database_port_to_public
  - reset_admin_password

example_prompts:
  - "请检查阿里云 Windows Server 服务器 aliyun-win-sql-001 的运行状态"
  - "请在 aliyun-win-sql-001 上安装 SQL Server 2022"
  - "请为 GotoPlan 项目创建会员、订单、支付记录表"
  - "请检查 tencent-linux-app-001 的 PostgreSQL 数据库健康状态"
  - "生成所有服务器的今日巡检报告"
---

# goto-cloudserver-manager

GotoPlan / OpenClaw 生态中的**多云服务器自动化运维能力层**——配置好云厂商凭证和服务器信息后，用自然语言对话就能让 OpenClaw 完成状态检查、装数据库、建表、备份恢复、防火墙/监控配置、生成巡检报告等运维动作，OPC 和小团队也能拥有一个 AI 云运维工程师。

## 功能概览

- 多云支持：阿里云 / 腾讯云（CVM + 轻量应用服务器） / 华为云
- 多系统：Windows Server 2019/2022 / Ubuntu / Debian / CentOS / Rocky Linux / openEuler
- 多数据库：SQL Server / MySQL / PostgreSQL / Redis
- 统一 Schema：用中文描述业务表结构，自动生成各数据库 SQL
- 21 个运维动作：状态检查、装库建表、健康巡检、备份恢复、防火墙/WinRM 配置、监控部署、日志分析、生成中文报告……（完整列表见上方 `capabilities`）
- 三级权限：只读操作自动执行 / 写操作需确认 / 危险操作（删库、清空表、格式化磁盘等）直接拒绝

## 快速使用

### 1. 安装

```
openclaw skills install @feixuelingcloud/goto-cloudserver-manager
```

### 2. 配置云厂商凭证（直接对话，不用手动改文件）

```
帮我配置阿里云凭证，AccessKey ID 是 LTAI5tXxxxxxxxx，AccessKey Secret 是 xxxxxxxxxxxxxx
```

OpenClaw 会把凭证写入本地 `.env`，不会上传或外传；腾讯云、华为云同理，直接把 SecretId/SecretKey 或 AK/SK 告诉它即可。

### 3. 添加服务器（直接对话）

```
添加一台阿里云 Windows 服务器，实例 ID 是 i-bp1xxxxxxxx，
在杭州区域，操作系统是 Windows Server 2022，
这台服务器用来跑 SQL Server，叫它"生产数据库服务器"
```

OpenClaw 会生成对应的 `config/servers.yaml` 条目并等你确认后写入。

### 4. 用自然语言下达运维指令

```
检查一下"生产数据库服务器"现在的运行状况
在"生产数据库服务器"上安装 SQL Server 2022
请为 GotoPlan 项目创建会员、订单、支付记录表
生成所有服务器的今日巡检报告
```

- 只读操作（状态检查、健康巡检等）直接执行并返回结果
- 写操作（装库、建表、重启、备份恢复等）先给出执行计划，等你回复确认后才执行
- 禁止类操作（删库、清空表、格式化磁盘、关闭防火墙等）会被直接拒绝，不会进入执行流程

完整的安装配置步骤、更多对话示例、权限策略和架构说明见仓库 [README.md](README.md)。
