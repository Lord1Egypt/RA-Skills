# 🚀 PAO System - 个人AI操作系统

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-1.1.1-orange.svg)

**让您的 AI 助手在不同设备间无缝协作、共享记忆、自动进化**

[English](./README.md) | [功能介绍](#-核心功能) | [快速开始](#-快速开始) | [应用场景](#-应用场景)

</div>

---

## 💡 解决什么问题？

你有没有遇到过这些烦恼？

- 😩 **换了设备，AI 助手的"记忆"就没了** — 对话历史、技能配置全丢了
- 📱💻 **手机上的任务，想在电脑上继续做** — 没有简单的方法
- 🤖 **有多个 AI Agent，却不知道怎么让它们协作** — 各自为战
- 🔒 **不想把隐私数据传到第三方服务器** — 但本地部署又太复杂

**PAO System 就是来解决这些问题的！**

---

## ✨ 核心功能

### 🔗 跨设备记忆同步
```
手机 (08:30) ──▶ 记录想法
电脑 (09:15) ──▶ 继续工作，自动同步过来
平板 (11:00) ──▶ 继续处理，无缝衔接
```
AI 助手在不同设备间共享同一份记忆，一个设备学到新技能，所有设备都受益。

### 🤝 多 Agent 任务分发
```
你 ──▶ "帮我分析这份数据" ──▶ 自动分发到空闲的 Agent
                              ↓
                     [数据专家 Agent] ──▶ 返回分析结果
```
支持向指定 Agent 发送任务，结果自动聚合返回，就像指挥一个 AI 团队！

### 🌐 去中心化架构
- **不需要第三方服务器** — 点对点直连，保护隐私
- **自动发现设备** — 同网络下自动感知、连接
- **端到端加密** — 你的数据只有你能看到

### 🧠 技能自动进化
- AI 能力随使用自动改进
- 基于场景的记忆存储和检索
- 经验共享，一个设备学习，所有设备受益

---

## 🎯 应用场景

| 场景 | 说明 |
|------|------|
| **跨设备办公** | 手机记笔记、电脑整理、手机随时查看 |
| **多 Agent 协作** | 数据分析、代码审查、文档处理分工协作 |
| **隐私优先** | 所有数据本地存储，不依赖云服务 |
| **自动化工作流** | 任务自动分发到最合适的 Agent 执行 |

---

## 🚀 快速开始

### 安装

```bash
# 方式1: 从源码
git clone https://github.com/hansondong/pao-system.git
cd pao-system
pip install -r requirements.txt

# 方式2: 从 PyPI (即将上线)
pip install pao-system
```

### 启动

```bash
# 启动 PAO 系统
python pao.py start

# 或启动任务监听器（作为 Worker）
python task_listener.py --port 8765
```

### 发送任务（示例）

```python
import httpx

# 向其他 Agent 发送任务
response = httpx.post('http://localhost:8765/task', json={
    "task_action": "帮我分析销售数据",
    "task_params": {"file": "sales.csv"}
})
print(response.json())
```

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────┐
│                    PAO System                    │
├─────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌──────────┐ │
│  │  设备发现   │  │  WebSocket  │  │  任务    │ │
│  │  (zeroconf) │  │   实时通信   │  │  分发器  │ │
│  └─────────────┘  └─────────────┘  └──────────┘ │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────┐ │
│  │  记忆存储   │  │  CRDT 同步  │  │  技能    │ │
│  │  (本地优先) │  │  (冲突解决)  │  │  管理器  │ │
│  └─────────────┘  └─────────────┘  └──────────┘ │
└─────────────────────────────────────────────────┘
```

### 核心模块

| 模块 | 说明 |
|------|------|
| `task_listener.py` | 任务监听器 - 接收并执行任务 |
| `task_distributor.py` | 任务分发器 - 分发任务到目标 Agent |
| `src/core/heartbeat.py` | 心跳保活 - 监控连接状态 |
| `src/core/memory.py` | 记忆存储 - 跨设备同步 |
| `src/core/audit_log.py` | 审计日志 - 可追溯的操作记录 |
| `src/protocols/` | 通信协议定义 |

---

## 📚 文档

- [用户指南](./docs/user_guide.md) - 详细使用说明
- [API 参考](./docs/api_reference.md) - 接口文档
- [部署指南](./docs/deployment.md) - 安装部署
- [开发计划](./docs/development_plan.md) - 开发路线图

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

如果你有好的想法或发现 bug，欢迎：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

<div align="center">

**如果这个项目对你有帮助，欢迎 star ⭐ 和分享！**

</div>
