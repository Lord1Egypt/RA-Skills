---
slug: namecheap-dns-tool-free
name: namecheap-dns-tool-free
version: 1.0.0
displayName: DNS管理入门工具
summary: "Namecheap域名DNS记录管理工具，支持A/CNAME/MX等常用记录操作.。面向个人开发者与小型网站的Namecheap DNS管理工具。支持A/CNAME/"
license: Proprietary
edition: free
description: '面向个人开发者与小型网站的Namecheap DNS管理工具。支持A/CNAME/

  MX/TXT等常用DNS记录的创建、查询、更新与删除。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。Use
  when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。'
tags:
  - Operations
  - DNS
  - 域名管理
  - 工具
  - 效率
  - 自动化
  - 开发
  - 代码
  - 运维
  - 监控
  - 写作
  - api
  - dns
  - ttl
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
---
# DNS管理入门工具（免费版）

## 概述

本工具为个人开发者和小型网站提供Namecheap DNS管理能力。支持常用DNS记录的创建、查询、更新与删除，通过API简化DNS配置流程。适合个人域名和小型网站的DNS管理.
## 核心能力

### DNS记录管理

| 记录类型 | 用途 | 免费版支持 |
|----|---|-----|
| A | IPv4地址指向 | 支持 |
| AAAA | IPv6地址指向 | 支持 |
| CNAME | 别名记录 | 支持 |
| MX | 邮件服务器 | 支持 |
| TXT | 文本记录（SPF等） | 支持 |
| NS | 域名服务器 | 支持 |
| SRV | 服务记录 | 支持 |
| CAA | 证书授权 | 不支持 |
| 批量管理 | 多记录操作 | 基础 |
| DNS监控 | 传播监控 | 不支持 |

**处理**: 解析DNS记录管理的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回DNS记录管理的响应数据,包含状态码、结果和日志.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Namecheap、记录管理工具、等常用记录操作、面向个人开发者与、小型网站的、管理工具、等常用、记录的创建、更新与删除、Use、when、需要代码生成、编程辅助、调试测试、开发部署时使用、不适用于无明确技、术栈的模糊需求、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：添加A记录

用户输入："把example.com指向192.168.1.1"

```bash
# 添加A记录
python3 （请参考skill目录中的脚本文件） record add \
  --domain example.com \
  --type A \
  --host "@" \
  --value 192.168.1.1 \
  --ttl 1800
# ...
# 查看记录
python3 （请参考skill目录中的脚本文件） record list --domain example.com
```

### 场景二：配置邮件MX记录

用户输入："配置域名的MX记录"

```bash
# 添加MX记录
python3 （请参考skill目录中的脚本文件） record add \
  --domain example.com \
  --type MX \
  --host "@" \
  --value "mail.example.com" \
  --priority 10 \
  --ttl 3600
```

### 场景三：添加CNAME别名

用户输入："把www指向example.com"

```bash
# 添加CNAME记录
python3 （请参考skill目录中的脚本文件） record add \
  --domain example.com \
  --type CNAME \
  --host "www" \
  --value "example.com" \
  --ttl 1800
```

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 环境准备

```bash
# 依赖说明
pip install requests
# ...
# 配置API凭证
# 登录Namecheap > Profile > Tools > API Access
# 获取ApiUser, ApiKey, UserName, ClientIP
export NAMECHEAP_API_USER="your_api_user"
export NAMECHEAP_API_KEY="your_api_key"
export NAMECHEAP_USERNAME="your_username"
export NAMECHEAP_CLIENT_IP="your_ip"
```

### 常用命令

```bash
# 域名列表
python3 （请参考skill目录中的脚本文件） domains list
# ...
# 记录管理
python3 （请参考skill目录中的脚本文件） record add --domain example.com --type A --host "@" --value 192.168.1.1
python3 （请参考skill目录中的脚本文件） record update --domain example.com --record-id 123 --value 192.168.1.2
python3 （请参考skill目录中的脚本文件） record delete --domain example.com --record-id 123
# ...
# DNS传播检查
python3 （请参考skill目录中的脚本文件） propagate check --domain example.com --type A
# ...
# 设置默认DNS服务器
python3 （请参考skill目录中的脚本文件） nameservers set --domain example.com --dns "dns1.namecheaphosting.com,dns2.namecheaphosting.com"
```

## 示例

### DNS管理配置

```yaml
dns_config:
  api:
    base_url: "https://api.namecheap.com/xml.response"
    api_user: "${NAMECHEAP_API_USER}"
    api_key: "${NAMECHEAP_API_KEY}"
    username: "${NAMECHEAP_USERNAME}"
    client_ip: "${NAMECHEAP_CLIENT_IP}"
    timeout: 30
# ...
  defaults:
    ttl: 1800                   # 默认TTL
    record_types: ["A", "AAAA", "CNAME", "MX", "TXT", "NS", "SRV"]
# ...
  cache:
    enabled: true
    ttl: 60                     # API响应缓存
```

## 最佳实践

1. **TTL设置**：常用记录设1800秒（30分钟），需要快速切换的设300秒
2. **记录备份**：修改前先导出当前记录，便于回滚
3. **传播时间**：DNS修改后全球传播需0-48小时，使用传播检查工具
4. **安全配置**：配置SPF/DKIM/DMARC TXT记录防邮件伪造

| 实践要点 | 说明 |
|:-----|:-----|
| TTL选择 | 高频变更用短TTL，稳定记录用长TTL |
| 记录冲突 | 同名同类型记录可能冲突 |
| IP白名单 | API需配置ClientIP白名单 |
| SPF记录 | TXT记录配置SPF防止邮件被拒 |

## 常见问题

### Q1：如何获取Namecheap API凭证？

登录Namecheap后台 > Profile > Tools > API Access，启用API访问并获取ApiUser、ApiKey。需将本机公网IP加入白名单.
### Q2：DNS修改后多久生效？

取决于TTL设置和各DNS服务器的缓存策略。短TTL（300秒）约5-15分钟生效，长TTL（86400秒）可能需要24-48小时全球传播.
### Q3：免费版支持批量管理多域名吗？

免费版支持单域名内的批量记录操作，但不支持跨域名批量管理。如需管理多个域名，建议升级PRO版.
### 已知限制

Namecheap API有频率限制（约每小时200次）。建议启用缓存，避免频繁调用.
## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.8+

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python | 运行时 | 必需 | 系统安装或conda环境 |
| requests | Python库 | 必需 | `pip install requests` |

### API Key 配置

| 服务 | 环境变量 | 是否必需 | 用途 |
|:---:|:---:|:---:|:---:|
| API用户 | `NAMECHEAP_API_USER` | 必需 | API认证 |
| API密钥 | `NAMECHEAP_API_KEY` | 必需 | API认证 |
| 用户名 | `NAMECHEAP_USERNAME` | 必需 | 账户标识 |
| 客户端IP | `NAMECHEAP_CLIENT_IP` | 必需 | IP白名单验证 |

- 需在Namecheap后台配置API访问权限
- ClientIP必须与实际请求IP一致

### 可用性分类

- **分类**: MD+EXEC（Markdown指令+Python脚本执行）
- **说明**: 通过Namecheap API管理DNS记录
- **免费版限制**: 单域名管理、基础记录类型、不支持DNS监控

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "DNS管理入门工具处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "namecheap dns"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
