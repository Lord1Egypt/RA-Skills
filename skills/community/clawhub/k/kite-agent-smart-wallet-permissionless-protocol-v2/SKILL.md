# Kite AI Agent Smart Wallet Permissionless Protocol

> 让用户通过Telegram控制加密货币钱包 / Telegram wallet control for Kite AI

![Version](https://img.shields.io/badge/version-2.0.4-blue)
![Kite AI](https://img.shields.io/badge/Kite-AI-purple)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue)

## 简介 / Introduction

这是一个让用户通过Telegram管理Kite AI链上钱包的协议。  
A protocol for users to manage Kite AI wallet via Telegram.

- 用户本地运行Bot / Bot runs locally
- 私钥用户自己保管 / Private key stays with user
- 完全去中心化 / Fully decentralized

## 特性 / Features

- 📱 Telegram钱包控制 / Telegram wallet control
- 🔐 智能钱包 / Smart wallet
- 🔑 Session Keys / 授权密钥
- 💰 消费限额 / Spending limits
- 🌍 中英双语 / Bilingual

## 快速开始 / Quick Start

### 1. 创建Telegram机器人
1. 打开Telegram → @BotFather
2. 发送 `/newbot`
3. 给机器人起名
4. 复制Token

### 2. 安装
```bash
git clone <repo>
cd kite-wallet
npm install
```

### 3. 配置
```env
PRIVATE_KEY=你的私钥
TELEGRAM_BOT_TOKEN=你的Token
```

### 4. 运行
```bash
node telegram-bot.js
```

## 命令 / Commands

| 中文 | English | 功能 Function |
|------|---------|---------------|
| /create | /create | 创建钱包 |
| /wallet | /wallet | 查看地址 |
| /balance | /balance | 查看余额 |
| /session add | /session add | 添加授权 |
| /limit set | /limit set | 设置限额 |
| /send | /send | 转账 |

## 网络 / Network

| 网络 Network | Chain ID | RPC |
|-------------|----------|-----|
| Testnet | 2368 | https://rpc-testnet.gokite.ai |

## 合约 / Contracts

| 合约 Contract | 地址 Address |
|--------------|-------------|
| AgentSmartWalletFactory | `0x0fa9F878B038DE435b1EFaDA3eed1859a6Dc098a` |

## 相关链接 / Links

- 🌐 Website: https://gokite.ai
- 🔍 Explorer: https://testnet.kitescan.ai
- 🚰 Faucet: https://faucet.gokite.ai
- 📖 Docs: https://docs.gokite.ai

## 版本历史 / Version History

- v2.0.4 - 中英双语 Bilingual
- v2.0.3 - 用户手册 User guide
- v2.0.2 - 用户本地运行 User runs locally
- v1.0.0 - 初始版 Initial

---

**作者 / Author**: VandNi  
**许可证 / License**: MIT
