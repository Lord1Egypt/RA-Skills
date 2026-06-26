# Mac Reminder Bridge (苹果提醒事项桥接器) 🔔

> [!IMPORTANT]
> **本仓库内的所有代码及文档，完全由 Claude 4.6 Sonnet 自动生成。**

一个轻量级的 HTTP 桥接工具，允许运行在 Docker 容器（尤其是 OpenClaw 等 AI 智能体）中的程序，通过简单的 REST API 接口直接管理 macOS 原生的**提醒事项 (Reminders.app)**。

## 🌟 为什么在 Docker 中运行 OpenClaw？（以及为什么需要此工具）

在 macOS 上通过 Docker 而非原生环境运行 OpenClaw 等 AI 智能体具有显著优势：

1. **安全性与隔离性**：AI Agent 经常需要执行各种命令行。Docker 确保了即使是由于幻觉产生的错误指令也会被限制在容器黑盒中，无法访问你宿主机的个人文档、照片或敏感的 SSH 密钥。
2. **环境一致性**：避免“在我机器上能跑”的尴尬。Docker 提供了一个预配置好的、干净的环境，不受 macOS 系统升级或 Python/Node.js 版本冲突的影响。
3. **系统清洁度**：原生安装往往会产生大量碎片文件。Docker 可以随用随删，保持你的 macOS 系统清爽如新。
4. **突破“空气墙”限制**：虽然 Docker 很安全，但它也隔离了 AI 访问 macOS 原生功能的能力。

**Mac Reminder Bridge** 完美解决了这一痛点——在享受 Docker 安全隔离的同时，为 AI 打开了一扇通往苹果生态的高速通道。

## 🚀 主要功能
- **全功能管理**：支持提醒事项的增、删、改、查（CRUD）。
- **自然语言适配**：专为 AI Agent 的工具调用（Tool Calling）场景设计。
- **智能解析**：支持设定到期时间、优先级、备注信息以及指定列表分类。
- **安全保障**：
  - 支持 IP 白名单策略。
  - 支持共享密钥 (`X-Bridge-Secret`) 认证。
  - 内置 AppleScript 注入防护。
- **原生体验**：基于 AppleScript 实现，数据与你的 iCloud 账号完美同步。

## ⚙️ 配置（环境变量）
| 变量名 | 描述 | 默认值 |
|----------|-------------|---------|
| `BRIDGE_SECRET` | 用于鉴权的共享密钥 | (无) |
| `BRIDGE_PORT` | 监听端口 | `5000` |
| `BRIDGE_ALLOWED_IPS` | IP 白名单（逗号分隔，云用户必看） | `172.0.0.0/8,127.0.0.1` |

### ☁️ 云端部署（腾讯云/阿里云等）特别说明
如果你是在远程云服务器上运行 OpenClaw：
1. 请确保在 Mac 的防火墙/路由器中开放了 `5000` 端口。
2. 你**必须**将云服务器的公网 IP 加入白名单，或设置 `BRIDGE_SECRET`：
```bash
# 示例：允许特定的云服务器 IP 访问
export BRIDGE_ALLOWED_IPS="1.2.3.4,127.0.0.1"
python3 listener.py
```

### 检查服务状态
```bash
curl http://host.docker.internal:5000/health
```

### 创建一个提醒
```bash
curl -X POST http://host.docker.internal:5000/add_reminder \
     -H "Content-Type: application/json" \
     -d '{
       "task": "下午6点去拿快递",
       "due": "2026-03-14 18:00",
       "priority": "high",
       "notes": "这是由 AI 助手自动同步的提醒"
     }'
```

## 📜 开源协议
基于 MIT 协议开源。欢迎提交 Issue 或 Pull Request！
