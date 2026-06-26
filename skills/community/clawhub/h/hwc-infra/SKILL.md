---
name: hwc-infra
description: |
  华为云基础设施管理助手，基于 KooCLI (hcloud)。
  支持查询、审计和监控华为云资源：ECS（弹性云服务器）、VPC（虚拟私有云）、RDS（关系型数据库服务）。
  触发条件：用户询问华为云资源、ECS 服务器、VPC 网络、RDS 数据库、云资源清单、安全审计、资源状态检查等。
  写操作/破坏性操作需要用户明确确认。
---

# 华为云基础设施管理

## 概述
使用本地 KooCLI (hcloud) 管理华为云资源。默认只读查询，写操作需确认。

## 前置检查
**每次触发时执行：**
```bash
# 检查 KooCLI 是否已安装
hcloud version
```

**如果未安装，先介绍 KooCLI 并询问用户：**

华为云命令行工具服务（Koo Command Line Interface，KooCLI，原名HCloud CLI）是为发布在API Explorer上的云服务API提供的命令行管理工具。您可以通过此工具调用API Explorer中各云服务开放的API，管理和使用您的各类云服务资源。KooCLI只提供了一种通过CLI调用云服务API的方法。


**安装方式：**
- 自动安装：执行 `python3 scripts/install_koocli.py`
- 手动安装：参考 https://support.huaweicloud.com/qs-hcli/hcli_02_003.html

**询问用户：** "KooCLI 未安装。是否需要自动安装？(y/n)"

- 如果用户同意，执行安装脚本：`python3 scripts/install_koocli.py`
- 如果用户拒绝，提示手动安装方式并终止当前任务

**安装完成后，初始化配置文件：**
```bash
hcloud configure init
```

交互式输入 AK/SK/区域，生成配置文件 `~/.hcloud/config.json`

## 初始化流程（安装/配置后执行）

**仅在以下情况执行身份验证：**
- 首次安装 KooCLI 后
- 配置/更新 AK/SK 后

```bash
hcloud IAM KeystoneListProjects
```

验证 AK/SK 是否正确，获取可用项目/区域列表。

---

## 查询流程（日常使用）

1. **确定区域** → 用户指定 或 `HWCLOUD_REGION` 或 `~/.hcloud/config.json`
2. **执行查询** → 只读命令直接执行
3. **变更确认** → 写操作需列出命令，请求用户确认

## 安全规则
- 默认**只读**，变更需用户确认
- 破坏性操作（删除/终止/修改）必须确认
- 不泄露密钥（AK/SK）

## 任务指南
- **资源清单**：`List*`/`Show*` 命令
- **健康检查**：查询资源状态字段
- **安全检查**：查询安全组规则
- **变更操作**：显示命令并确认

## 区域处理
- 如果用户指定区域，遵循用户指定
- 否则使用 `HWCLOUD_REGION` 或 `~/.hcloud/config.json`
- 结果有区域范围时，说明使用的区域

## 参考
常用命令见 `references/hcloud-queries.md`
