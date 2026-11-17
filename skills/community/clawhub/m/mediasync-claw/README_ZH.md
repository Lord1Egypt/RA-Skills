<div align="center">

# MediaSync-Claw: 基于 OpenClaw 的远程 P2P 媒体服务与流媒体 Skill

[English](README.md) | [简体中文](README_ZH.md) | [日本語](README_JA.md) | [Deutsch](README_DE.md) | [Español](README_ES.md)

</div>

---

## 📖 概述与核心价值

**MediaSync-Claw** 设计目的为提供个人媒体文件的远程共享与点对点流媒体服务。

其核心价值在于：通过 WhatsApp 接入 OpenClaw AI 代理后，用户可以随时随地远程获取并检索本地电脑上的媒体文件列表。生成的媒体列表原生支持通过 **AIpollo Player** 进行高速 P2P 穿透播放。

---

## ⚙️ 使用前提

* **OpenClaw**: 本地已成功部署并运行 OpenClaw 环境。
* **安全软件加白**: 在系统安全软件（如 Windows Defender）中添加信任例外 `frpc.exe`。*我们保证官方提供的 `frpc.exe` 绝对安全无篡改。*

---

## 🚀 具体使用步骤

1. **下载与安装**：下载并安装 MediaSync-Claw skill 至 OpenClaw 的 skills 目录下。
2. **构建本地片源库**：在本 skill 的根目录中创建 `videos` 文件夹，并将需要远程访问的 MP4 视频文件放入其中。
3. **配置 WhatsApp**：在 OpenClaw 中接入并完成 WhatsApp 通道配置。
4. **运行 Skill**：在 OpenClaw 平台中启动并运行本 skill。
5. **WhatsApp 远程交互**：在 WhatsApp 对话中发送自然语言指令（例如：当您想要查看、列出、搜索或播放本地视频库/播放列表时），触发本 skill 获取媒体列表。
6. **调起播放**：点击媒体列表中返回的专属安全链接，即可在 AIpollo Player 中开始播放。

---

## 🔒 安全说明与风险披露

### 风险 1：本地服务公网穿透访问
本 skill 旨在提供便捷的远程媒体共享体验。为了实现跨局域网穿透，它通过 FRP（Fast Reverse Proxy）客户端（`frpc`）与远程中继服务器（`frps`）建立一条出站隧道，从而使您的本地媒体服务可通过 `*.yunfrp.net` 域名进行公网指令调度。

### 风险 2：HTTP 明文传输与 P2P 播放架构
本 skill 的核心视频流播放采用 **P2P 点对点传输**。HTTP 协议仅用于接收轻量控制指令，传输过程绝不涉及或上传任何用户的敏感个人隐私数据。

### 风险 3：下载与拉起 `frpc.exe` 二进制组件
为了支持跨网域 NAT 穿透与反向代理，本 skill 所需的 `frpc.exe` 均直接从官方 GitHub Releases 渠道获取，最大程度保证开源供应链的安全透明。

---

## 🛡️ 安全实践建议

* **专用设备与隔离环境**：为了确保绝对安全，建议使用单独的闲置电脑或 NAS 作为媒体服务器，而非在主力工作设备上运行。若必须在主力机上运行，推荐使用虚拟机（VM）进行环境隔离。
* **系统安全维护**：建议定期更新并升级您的操作系统补丁与 OpenClaw 运行环境，防范潜在安全漏洞。

---

## 💻 平台兼容性

* **当前支持**：Windows (x64)
* **后续规划**：Linux 与 macOS 平台支持正在积极适配中。

*如需其他平台支持或在网络穿透中遇到问题，欢迎提交 GitHub Issue 或联系我们。感谢您的支持与信任！*