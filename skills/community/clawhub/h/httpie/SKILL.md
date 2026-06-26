---
name: httpie
description: HTTPie - 人性化的 HTTP 命令行客户端
version: 0.1.1
metadata:
  openclaw:
    requires:
      bins:
        - http
    emoji: 🌐
    homepage: https://httpie.io
---

# HTTPie 人性化 HTTP 命令行客户端

## 技能概述

本技能帮助用户通过命令行发送 HTTP 请求，调试 API 接口，适用于以下场景：

- **REST API 调试**: 发送 GET/POST/PUT/DELETE 等各类 HTTP 请求
- **接口测试**: 快速验证 API 端点的请求与响应
- **文件上传下载**: 通过命令行进行文件传输
- **身份认证**: 支持 Basic、Bearer Token、Digest 等多种认证方式
- **会话管理**: 跨请求保持 Cookie 与认证状态
- **格式化输出**: 自动语法高亮显示 JSON、XML 响应体

**主要特点**: 语法简洁、自动格式化、彩色输出、内置 JSON 支持、比 curl 更易读写

## 使用流程

AI 助手将引导你完成以下步骤：

1. 安装 HTTPie（如未安装）
2. 构建 HTTP 请求（方法、URL、请求头、请求体）
3. 执行请求并查看格式化响应
4. 根据响应调整请求参数
5. 将成功的命令保存为可复用脚本

## 关键章节导航

- [安装指南](./guides/01-installation.md)
- [快速开始](./guides/02-quickstart.md)
- [高级用法](./guides/03-advanced-usage.md)
- [常见问题](./troubleshooting.md)

## AI 助手能力

当你向 AI 描述请求需求时，AI 会：

- 自动识别请求类型（GET/POST/PUT/PATCH/DELETE）
- 根据描述构建正确的请求头和请求体
- 执行请求命令并解析响应
- 识别常见 HTTP 错误状态码并给出建议
- 自动处理 JSON 数据序列化
- 管理认证令牌和会话 Cookie
- 将复杂请求转换为可读的 HTTPie 命令

## 核心功能

- 支持全部 HTTP 方法（GET、POST、PUT、PATCH、DELETE、HEAD、OPTIONS）
- 自动 JSON 请求体序列化与响应格式化
- 彩色语法高亮（请求头、响应头、响应体）
- 内置多种认证方式（Basic、Digest、Bearer）
- 持久化 Session 管理（跨请求 Cookie）
- 文件上传与二进制下载支持
- HTTPS 与 SSL 证书验证
- 代理支持（HTTP/HTTPS/SOCKS）
- 离线模式（仅打印请求不发送）
- 与 curl 命令互转

## 命令速查表

### 基础请求

```bash
# GET 请求
http GET https://api.example.com/users

# 简写（默认 GET）
http https://api.example.com/users

# POST JSON（自动推断 Content-Type: application/json）
http POST https://api.example.com/users name="张三" age:=25

# PUT 更新
http PUT https://api.example.com/users/1 name="李四"

# PATCH 部分更新
http PATCH https://api.example.com/users/1 email="li@example.com"

# DELETE 删除
http DELETE https://api.example.com/users/1
```

### 请求参数与请求头

```bash
# URL 查询参数（== 语法）
http https://api.example.com/search q=="hello world" page==2

# 自定义请求头（: 语法）
http https://api.example.com/users "Authorization: Bearer mytoken123"

# 多个请求头
http https://api.example.com/data "X-API-Key: abc123" "Accept: application/json"
```

### 认证

```bash
# Basic 认证
http -a username:password https://api.example.com/protected

# Bearer Token
http https://api.example.com/me "Authorization: Bearer <token>"

# Digest 认证
http --auth-type=digest -a user:pass https://api.example.com/secure
```

### 输出控制

```bash
# 仅显示响应体
http --body https://api.example.com/users

# 仅显示响应头
http --headers https://api.example.com/users

# 显示请求+响应（调试用）
http --verbose https://api.example.com/users

# 安静模式（无输出，只看退出码）
http --quiet https://api.example.com/health

# 保存响应到文件
http https://api.example.com/file.pdf > file.pdf
```

## 安装要求

- Python 3.7+ 或直接使用独立二进制包
- 无其他强制依赖

## 许可证

BSD-3-Clause License

## 项目链接

- GitHub: https://github.com/httpie/cli
- 官网: https://httpie.io
- 文档: https://httpie.io/docs/cli
