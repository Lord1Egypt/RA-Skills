# OpenClaw Setup Assistant Skill

帮助用户快速安装配置 OpenClaw，提供远程服务支持。

## 功能

- 一键安装 OpenClaw CLI
- 配置常用 Channel（微信/飞书/钉钉）
- 设置心跳和自动化任务
- 提供 Skills 推荐
- 故障排查指南

## 使用方式

```
帮我安装 OpenClaw
```

```
配置微信 Channel
```

```
设置每日简报心跳
```

## 安装流程

### 步骤 1：检查环境
```bash
# 检查 Node.js 版本
node -v  # 需要 >= 18

# 检查 npm
npm -v
```

### 步骤 2：安装 OpenClaw
```bash
npm install -g openclaw
```

### 步骤 3：初始化工作区
```bash
openclaw init
```

### 步骤 4：配置 Channel

#### 微信
```bash
openclaw channel add wechat
# 扫码登录
```

#### 飞书
```bash
openclaw channel add feishu
# 配置 App ID 和 Secret
```

#### 钉钉
```bash
openclaw channel add dingtalk
# 配置 Webhook
```

### 步骤 5：设置心跳
```bash
# 编辑 heartbeat.md
openclaw edit ~/.openclaw/workspace/HEARTBEAT.md

# 启动心跳服务
openclaw heartbeat start
```

## 定价

| 套餐 | 价格 | 内容 |
|------|------|------|
| 基础安装 | ¥99 | 远程安装 + 基础配置 |
| 完整配置 | ¥299 | 安装 + Channel配置 + 3个Skills |
| 企业定制 | ¥999 | 安装 + 多Channel + 自定义Skills + 培训 |

## 收款地址

USDT TRC20: `TYTvuzacfUgeei36NK9dmfUCKFqiQfYizp`

## 常见问题

### Q: 安装失败怎么办？
A: 检查网络连接，确保能访问 npm 仓库。中国大陆用户建议使用淘宝镜像：
```bash
npm config set registry https://registry.npmmirror.com
```

### Q: 微信登录不上？
A: 确保微信是最新版本，扫码后需要在手机上确认登录。

### Q: 心跳不执行？
A: 检查 HEARTBEAT.md 格式是否正确，确保 openclaw heartbeat start 已运行。

## 技术支持

- GitHub Issues: https://github.com/openclaw/openclaw/issues
- Discord: https://discord.com/invite/clawd
- 文档: https://docs.openclaw.ai

---

创建时间：2026-03-11
服务提供：ClawMart