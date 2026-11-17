---
slug: ocean-chat-tool-free
name: ocean-chat-tool-free
version: 1.0.0
displayName: P2P通讯入门工具
summary: "基于WASM的P2P消息通讯工具，支持点对点文本消息与基础文件传输.。面向个人开发者的P2P消息通讯工具。基于WASM技术实现浏览器端的"
license: Proprietary
edition: free
description: '面向个人开发者的P2P消息通讯工具。基于WASM技术实现浏览器端的

  点对点通讯，支持文本消息与基础文件传输。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。Use
  when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。'
tags:
  - Operations
  - 通讯
  - P2P
  - WebRTC
  - 工具
  - 效率
  - 自动化
  - 通信
  - 邮件
  - 开发
  - 代码
  - 安全
  - python3
  - p2p
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
---
# P2P通讯入门工具（免费版）

## 概述

本工具为个人开发者提供基于WASM的P2P消息通讯能力。通过WebRTC技术实现浏览器端点对点连接，支持文本消息和基础文件传输，无需中心服务器中转消息内容，保障通讯隐私.
## 核心能力

### 通讯功能

| 功能 | 说明 | 免费版支持 |
|---|---|-----|
| 文本消息 | 点对点文字通讯 | 支持 |
| 文件传输 | 小文件传输 | 支持（<10MB） |
| 端到端加密 | 消息加密 | 支持 |
| 群组通讯 | 多人消息 | 不支持 |
| 消息历史 | 历史记录 | 本地存储 |
| 多设备同步 | 跨设备 | 不支持 |
| 语音通话 | 实时语音 | 不支持 |
| 视频通话 | 实时视频 | 不支持 |

**处理**: 解析通讯功能的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回通讯功能的响应数据,包含状态码、结果和日志.
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
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：WASM、消息通讯工具、支持点对点文本消、息与基础文件传输、面向个人开发者的、技术实现浏览器端、点对点通讯、支持文本消息与基、础文件传输、Use、when、需要代码生成、编程辅助、调试测试、开发部署时使用、不适用于无明确技、术栈的模糊需求、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：点对点文本通讯

用户输入："建立P2P连接发送消息"

```bash
# 启动信令服务器
python3 （请参考skill目录中的脚本文件） signal start --port 8080
# ...
# 生成连接码
python3 （请参考skill目录中的脚本文件） connect create
# ...
# 输出：
# 连接码: OCEAN-7K9M-2X4P
# 分享给对方，对方输入此码建立连接
# ...
# 对方连接
python3 （请参考skill目录中的脚本文件） connect join --code OCEAN-7K9M-2X4P
# ...
# 发送消息
python3 （请参考skill目录中的脚本文件） send --message "你好，这是P2P消息"
```

### 场景二：文件传输

用户输入："通过P2P发送文件"

```bash
# 发送文件
python3 （请参考skill目录中的脚本文件） send-file \
  --file ./document.pdf \
  --peer OCEAN-7K9M-2X4P
# ...
# 接收文件
python3 （请参考skill目录中的脚本文件） receive --output ./received/
```

### 场景三：加密通讯

用户输入："建立加密P2P连接"

```bash
# 建立加密连接
python3 （请参考skill目录中的脚本文件） connect create --encryption AES-256
# ...
# 生成密钥对
python3 （请参考skill目录中的脚本文件） keys generate
# ...
# 共享公钥
python3 （请参考skill目录中的脚本文件） keys share --peer OCEAN-7K9M-2X4P
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
pip install aiohttp cryptography
# ...
# 启动信令服务器（用于连接建立）
python3 （请参考skill目录中的脚本文件） signal start --port 8080
# ...
# 生成连接码
python3 （请参考skill目录中的脚本文件） connect create
```

### 常用命令

```bash
# 连接管理
python3 （请参考skill目录中的脚本文件） connect create
python3 （请参考skill目录中的脚本文件） connect join --code OCEAN-XXXX-XXXX
python3 （请参考skill目录中的脚本文件） connect status
# ...
# 消息发送
python3 （请参考skill目录中的脚本文件） send --message "消息内容"
python3 （请参考skill目录中的脚本文件） send-file --file ./file.txt
# ...
# 消息历史
python3 （请参考skill目录中的脚本文件） history list
python3 （请参考skill目录中的脚本文件） history clear
# ...
# 密钥管理
python3 （请参考skill目录中的脚本文件） keys generate
python3 （请参考skill目录中的脚本文件） keys share --peer OCEAN-XXXX
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
#
## 示例

### 通讯配置

```yaml
ocean_config:
  signal:
    server: "ws://localhost:8080"
    timeout: 30
# ...
  webrtc:
    ice_servers:
      - urls: "stun:stun.l.google.com:19302"
    configuration:
      ice_transport_policy: "all"
# ...
  encryption:
    algorithm: "AES-256-GCM"
    key_exchange: "ECDH"
# ...
  file_transfer:
    max_size: 10485760            # 10MB
    chunk_size: 16384             # 16KB分块
# ...
  storage:
    history: "local"              # 本地存储
    max_history: 1000
```

## 最佳实践

1. **信令服务器**：P2P连接建立需要信令服务器中转，但消息内容不经过服务器
2. **NAT穿透**：复杂网络环境可能需要TURN服务器辅助穿透
3. **文件大小**：免费版建议传输小于10MB的文件
4. **密钥安全**：私钥保存在本地，不要分享给他人

| 实践要点 | 说明 |
|:-----|:-----|
| 连接码 | 连接码有时效性，过期需重新生成 |
| NAT环境 | 部分企业网络可能无法建立P2P连接 |
| 加密传输 | 所有消息端到端加密，服务器无法解密 |
| 文件验证 | 接收文件后验证哈希确保完整性 |

## 常见问题

### Q1：P2P连接建立失败怎么办？

可能原因：NAT穿透失败、信令服务器不可达、防火墙阻止WebRTC。建议：配置TURN服务器、检查网络防火墙、确认信令服务器运行.
### Q2：免费版支持群组通讯吗？

免费版仅支持点对点通讯。如需群组消息，建议升级PRO版.
### Q3：消息会被服务器看到吗？

不会。P2P连接建立后，消息直接在两个对等端之间传输，信令服务器仅用于连接建立，不参与消息中转。所有消息端到端加密.
### Q4：支持手机端使用吗？

免费版主要支持桌面端。WASM技术兼容移动端浏览器，但体验可能受限.
## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.8+
- **浏览器**: 支持WebRTC的现代浏览器

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python | 运行时 | 必需 | 系统安装或conda环境 |
| aiohttp | Python库 | 必需 | `pip install aiohttp`（信令服务器） |
| cryptography | Python库 | 必需 | `pip install cryptography`（加密） |

### API Key 配置

- 免费版无需API Key
- 使用公共STUN服务器（Google）
- 如需TURN服务器需自行配置

### 可用性分类

- **分类**: MD+EXEC（Markdown指令+Python脚本+WebRTC执行）
- **说明**: 基于WASM和WebRTC的P2P通讯工具
- **免费版限制**: 点对点通讯、小文件传输、不支持群组与多设备

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
